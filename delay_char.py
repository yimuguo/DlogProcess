import re
import os
import sys
import matplotlib.pyplot as plt
import numpy as np

gaussian_numbers = np.random.randn(1000)
print(gaussian_numbers)
plt.hist(gaussian_numbers)
plt.title("Gaussian Histogram")
plt.xlabel("Value")
plt.ylabel("Frequency")

fig = plt.gcf()
plt.show()