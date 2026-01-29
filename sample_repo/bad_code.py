import os
import sys

def process_data(a, b, c, d, e, f):
    result = 0
    for i in range(a):
        if i % 2 == 0:
            for j in range(b):
                result += i * j
    print(result)
````````