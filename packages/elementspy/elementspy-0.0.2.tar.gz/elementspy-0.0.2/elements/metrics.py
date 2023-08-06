import collections
import imageio
import itertools
import json
import pathlib
import re
from concurrent import futures

import numpy as np
import ruamel.yaml


class Metrics:

  def __init__(self, directory, workers=None):
    assert workers is None or isinstance(workers, int)
    self._directory = pathlib.Path(directory).expanduser()
    self._managers = {}
    self._managers['scalars'] = Scalars(self._directory / 'scalars')
    self._managers['tensors'] = Tensors(self._directory / 'tensors')
    self._managers['images'] = Images(self._directory / 'images')
    self._managers['videos'] = Videos(self._directory / 'videos')
    self._categories = self._read_categories(self._directory)
    self._tags = {}
    if workers:
      self._pool = futures.ThreadPoolExecutor(max_workers=workers)
    else:
      self._pool = None
    self._last_futures = []

  def set_tags(self, **kwargs):
    reserved = ('value',)
    if any(key in reserved for key in kwargs):
      message = "Reserved keys '{}' and cannot be used for tags"
      raise KeyError(message.format(', '.join(reserved)))
    for key, value in kwargs.items():
      key = json.loads(json.dumps(key))
      value = json.loads(json.dumps(value))
      self._tags[key] = value

  def reset_tags(self):
    self._tags = {}

  def add_scalar(self, name, value):
    self._validate_record(name, 'scalars')
    self._managers['scalars'].add(name, self._tags, value)

  def add_tensor(self, name, value):
    self._validate_record(name, 'tensors')
    self._managers['tensors'].add(name, self._tags, value, 'npy')

  def add_image(self, name, value, format='png'):
    assert format in ('png', 'jpg', 'bmp')
    self._validate_record(name, 'images')
    self._managers['images'].add(name, self._tags, value, format)

  def add_video(self, name, value, format='gif'):
    assert format in ('gif', 'mp4')
    self._validate_record(name, 'videos')
    self._managers['videos'].add(name, self._tags, value, format)

  def flush(self):
    try:
      for future in self._last_futures:
        future.result()
    except Exception as e:
      message = 'Previous asynchronous flush failed.'
      raise RuntimeError(message) from e
    futures = []
    for manager in self._managers.values():
      for name in manager.unsaved():
        if self._pool:
          futures.append(self._pool.submit(manager.flush, name))
        else:
          manager.flush(name)
    self._last_futures = futures.copy()
    return futures

  def query(self, pattern, **tags):
    pattern = re.compile(pattern)
    for manager in self._managers.values():
      for name in manager.names():
        if not pattern.search(name):
          continue
        for record in manager.read(name):
          if {k: v for k, v in record.items() if k in tags} != tags:
            continue
          yield record

  def _read_categories(self, directory):
    categories = {}
    for category, manager in self._managers.items():
      for name in manager.names():
        if name in categories:
          message = 'Found duplicate name {} for categories {} and {}'
          message = message.format(name, categories[name], category)
          raise RuntimeError(message)
        categories[name] = category
    return categories

  def _validate_record(self, name, category):
    assert isinstance(name, str) and name
    assert category in self._managers
    if re.search(r'[^a-z0-9/-]+', name):
      raise NameError(
          'Metric names should only contain lower case letters, '
          'digits, dashes, and forward slashes.')
    if name not in self._categories:
      self._categories[name] = category
    if self._categories[name] != category:
      message = 'Name {} is already in use for category {}'
      raise TypeError(message.format(name, self._categories[name]))

  def _flush(self, name):
    for manager in self._managers.values():
      manager.flush()


class Scalars:

  def __init__(self, directory):
    self._directory = directory
    self._records = collections.defaultdict(collections.deque)

  def add(self, name, tags, value):
    record = tags.copy()
    record['name'] = name
    record['value'] = float(value)
    self._records[name].append(record)

  def names(self):
    names = set(self._records.keys())
    for path in self._directory.glob('**/*.yaml'):
      names.add(self._path_to_name(path))
    return sorted(names)

  def read(self, name):
    path = self._name_to_path(name)
    records = itertools.chain(
        self._records[name],
        _load_yaml(path, not_exist_ok=True))
    for record in records:
      yield record

  def unsaved(self):
    return [name for name, records in self._records.items() if records]

  def flush(self, name):
    if name not in self._records or len(self._records[name]) == 0:
      return
    records = list(self._records[name])
    self._records[name].clear()
    _append_yaml(self._name_to_path(name), records)

  def _name_to_path(self, name):
    return self._directory.joinpath(*name.split('/')).with_suffix('.yaml')

  def _path_to_name(self, path):
    return '/'.join(path.relative_to(self._directory).with_suffix('').parts)


class Files:

  FORMATS = None

  def __init__(self, directory):
    self._directory = directory
    self._records = collections.defaultdict(collections.deque)
    self._indices = self._load_indices()
    self._values = {}

  def add(self, name, tags, value, format):
    if self.FORMATS is not None and format not in self.FORMATS:
      message = 'Supports formats {} but not {} for name {}'
      raise TypeError(message.format(', '.join(self.FORMATS), format, name))
    if name not in self._indices:
      self._indices[name] = 1
    filename = '{:0>10}.{}'.format(self._indices[name], format)
    self._indices[name] += 1
    record = tags.copy()
    record['name'] = name
    record['filename'] = filename
    self._values[self._directory.joinpath(*name.split('/')) / filename] = value
    self._records[name].append(record)

  def names(self):
    names = set(self._records.keys())
    for path in self._directory.glob('**/tags.yaml'):
      names.add(self._path_to_name(path))
    return sorted(names)

  def read(self, name):
    path = self._name_to_path(name)
    records = itertools.chain(
        self._records[name],
        _load_yaml(path, not_exist_ok=True))
    for record in records:
      record['filename'] = path.parent / record['filename']
      yield record

  def unsaved(self):
    return [name for name, records in self._records.items() if records]

  def flush(self, name):
    records = list(self._records[name])
    self._records[name].clear()
    catalogue = self._name_to_path(name)
    _append_yaml(catalogue, records)
    for record in records:
      filename = catalogue.parent / record['filename']
      self._write(filename, self._values.pop(filename))

  def _write(self, filename, value):
    raise NotImplementedError

  def _load_indices(self):
    largest = {}
    for path in self._directory.glob('**/tags.yaml'):
      indices = [0]
      for filename in path.parent.glob('*'):
        try:
          indices.append(int(filename.stem))
        except ValueError:
          pass
      largest[self._path_to_name(path)] = max(indices) + 1
    return largest

  def _name_to_path(self, name):
    return self._directory.joinpath(*name.split('/')) / 'tags.yaml'

  def _path_to_name(self, path):
    return '/'.join(path.relative_to(self._directory).parent.parts)


class Tensors(Files):

  FORMATS = ('npy',)

  def _write(self, filename, value):
    np.save(filename, value)


class Images(Files):

  FORMATS = ('png', 'jpg', 'bmp')

  def _write(self, filename, value):
    imageio.imwrite(filename, value)


class Videos(Files):

  FORMATS = ('gif', 'mp4')

  def _write(self, filename, value):
    imageio.mimwrite(filename, value, fps=30)


def _append_yaml(filename, mappings):
  filename.parent.mkdir(parents=True, exist_ok=True)
  rows = []
  for mapping in mappings:
    items = []
    mapping = sorted(mapping.items(), key=lambda x: x[0])
    items = ['{}: {}'.format(k, json.dumps(v)) for k, v in mapping]
    rows.append('- {' + ', '.join(items) + '}\n')
  content = ''.join(rows)
  with open(filename, 'a') as f:
    f.write(content)


def _load_yaml(filename, not_exist_ok=False):
  if not_exist_ok and not filename.exists():
    return []
  yaml = ruamel.yaml.YAML(typ='safe')
  rows = yaml.load(filename)
  message = 'Metrics files do not contain lists of mappings'
  if not isinstance(rows, list):
    raise TypeError(message)
  if not all(isinstance(row, dict) for row in rows):
    raise TypeError(message)
  return rows
