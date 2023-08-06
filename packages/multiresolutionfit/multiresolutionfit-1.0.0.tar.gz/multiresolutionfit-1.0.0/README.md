# Multiple Resolution Goodness of Fit.

The thesis of [cuevs2013]_ is that:

    "... there is no one 'proper' resolution, but rather a range of
         resolutions is necessary to adequately describe the fit of
         models with reality."


## Usage
```python
#!/usr/bin/env python3
# -*- Coding: UTF-8 -*-
"""
Example from [costanza89]_.

References
----------

.. [costanza89] COSTANZA, Robert. Model goodness of fit: a multiple resolution
                 procedure. Ecological modelling, v. 47, n. 3-4,
                 p. 199-215, 1989.
"""
from multiresolutionfit import Multiresoutionfit
from numpy import  arange, array
from numpy.random import randint
import matplotlib.pyplot as plt

scene1 = array([[1, 1, 1, 1, 2, 2, 2, 3, 3, 3],
                [1, 1, 1, 2, 2, 2, 3, 3, 3, 3],
                [1, 1, 2, 2, 2, 3, 3, 3, 3, 3],
                [3, 3, 2, 2, 3, 3, 3, 3, 3, 3],
                [1, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                [1, 1, 1, 3, 3, 3, 3, 3, 3, 3],
                [2, 2, 2, 2, 2, 2, 2, 2, 3, 3],
                [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                [3, 3, 3, 3, 2, 2, 3, 3, 3, 3],
                [3, 3, 3, 3, 2, 2, 2, 2, 3, 3]
                ])

scene2 = array([[1, 1, 2, 2, 2, 2, 2, 2, 3, 3],
                [1, 1, 1, 1, 2, 3, 3, 3, 3, 3],
                [1, 1, 1, 2, 3, 3, 3, 3, 3, 3],
                [3, 1, 2, 2, 3, 3, 3, 4, 4, 4],
                [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                [1, 1, 1, 3, 3, 3, 3, 3, 3, 3],
                [1, 1, 2, 2, 2, 2, 2, 2, 3, 3],
                [1, 2, 2, 3, 3, 2, 2, 3, 3, 3],
                [3, 3, 3, 3, 2, 2, 2, 3, 3, 3],
                [3, 3, 3, 3, 2, 2, 2, 2, 3, 3]
                ])


obj = Multiresoutionfit(scene1, scene2, verbose=True)
MAXW = 10
k = 0.1
wins = arange(1, 11, 1, dtype=int)
ftot, fw, wins = obj.ft(k=k, wins=wins)
print(f"\nWeighted fit: {ftot:.2f}\n")
z, fit = obj.zvalue(k=k, wins=wins, permutations=30)
print(f"z value {z:.2f}.")
plt.plot(wins, fw, marker='D')
plt.xticks(wins)
plt.ylim(ymax=0.95, ymin=0.75)
plt.xlim(xmax=MAXW, xmin=1)
plt.grid(True)
plt.show()
```

## References
----------

COSTANZA, Robert. Model goodness of fit: a multiple resolution
procedure. Ecological modelling, v. 47, n. 3-4,
p. 199-215, 1989.
