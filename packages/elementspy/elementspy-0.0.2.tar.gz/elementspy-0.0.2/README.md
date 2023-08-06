# 🔥 Elements

Building blocks for productive research.

```
python3 setup.py develop --user
```

```
python3 -m pytest -v -rs --cov=elements tests
```

```
python3 -m examples.vae \
    --logdir ~/logdir/temp/vae/$(date +'%Y%m%d-%H%M%S') \
    --optimizer tf.keras.optimizers.RMSprop \
    --lr 1e-4 \
    --debug True
```
