import numpy as np


next_action = 5

next_action = (next_action // 4 + 1) * 6 + (next_action % 4 + 1)

print(next_action)

next_action = (next_action // 6 - 1) * 4 + (next_action % 6 -1)

print(next_action)