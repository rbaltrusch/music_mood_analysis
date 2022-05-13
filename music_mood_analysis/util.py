# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 14:39:28 2021

@author: Korean_Crimson
"""

import time


def timeit(func):
    """Decorator that prints calling function name and execution time taken"""

    def wrapper(*args, **kwargs):
        time0 = time.time()
        result = func(*args, **kwargs)
        print(f"time elapsed in {func.__name__}: {time.time() - time0}")
        return result

    return wrapper
