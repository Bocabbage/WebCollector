import threading
import functools
from typing import Set

def singleton(cls):
    instances: dict = dict()
    lock = threading.Lock()
    
    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper


def bitmap2numset(bitmap: int) -> Set[int]:
    result: Set[int] = set()
    for i in range(64):
        if bitmap & (1 << i):
            result.add(i)
    return result


def numset2bitmap(num_set: Set[int]) -> int:
    bitmap = 0
    for value in num_set:
        if 0 <= value < 64:
            bitmap |= 1 << value
    return bitmap