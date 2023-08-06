# Keras RNAdam

use of nesterov accelerated geadient instead of momentum in rectified-adam

## Install

```bash
pip install keras_rnadam
```

## Usage

```python
import keras
import numpy as np
from keras_rnadam import RNAdam

# Build toy model with RNAdam optimizer
model = keras.models.Sequential()
model.add(keras.layers.Dense(input_shape=(17,), units=3))
model.compile(RNAdam(), loss='mse')

# Generate toy data
x = np.random.standard_normal((4096 * 30, 17))
w = np.random.standard_normal((17, 3))
y = np.dot(x, w)

# Fit
model.fit(x, y, epochs=5)
```

### Use Warmup

```python
from keras_nradam import RNAdam
RNAdam(total_step=10000, warmup_proportion=0.1, min_lr=1e-5)
```
