print("hello")

# x = 3
# y = 4

# def t(s):
#     z = 4
#     global x
#     x = 4

# t(y)
# # python uses reference counting
import sys

x = [1,2,3]
print(f"Ref count:{sys.getrefcount(x)}")

y = x
print(f"Ref count:{sys.getrefcount(x)}")

del y
print(f"Ref count:{sys.getrefcount(x)}")

print(f"Size:{sys.getsizeof(x)}")

y = [1,2,3,4,5,6,7,8]
print(f"Size:{sys.getsizeof(y)}")

numbers_list = [i for i in range(1000)]
numbers_tuple = tuple(numbers_list)
numbers_set = set(numbers_list)

print(f"List size: {sys.getsizeof(numbers_list)} bytes")
print(f"Tuple size: {sys.getsizeof(numbers_tuple)} bytes")
print(f"Set size: {sys.getsizeof(numbers_set)} bytes")

# Check individual object sizes
print(f"Integer: {sys.getsizeof(42)} bytes")
print(f"String: {sys.getsizeof('hello')} bytes")
print(f"Empty list: {sys.getsizeof([])} bytes")

import tracemalloc

tracemalloc.start()

data = []
for i in range(10000):
    data.append(f"Item {i}")

# Get current memory usage
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage: {current / 1024 / 1024:.2f} MB")
print(f"Peak memory usage: {peak / 1024 / 1024:.2f} MB")

# data = []
# # Get current memory usage
# current, peak = tracemalloc.get_traced_memory()
# print(f"Current memory usage: {current / 1024 / 1024:.2f} MB")
# print(f"Peak memory usage: {peak / 1024 / 1024:.2f} MB")

# Get top memory allocations
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print("\nTop 3 memory allocations:")
for stat in top_stats[:3]:
    print(stat)

tracemalloc.stop()

def get_squares_list(n):
    return [x**2 for x in range(n)]

def get_squares_generator(n):
    return (x**2 for x in range(n))

tracemalloc.start()
n = 100000
squares_list = get_squares_list(n)
print(f"First 5 from list: {squares_list[:5]}")
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage: {current / 1024 / 1024:.2f} MB")
print(f"Peak memory usage: {peak / 1024 / 1024:.2f} MB")
tracemalloc.stop()

tracemalloc.start()
n = 100000
squares_gen = get_squares_generator(n)
print(f"First 5 from generator: {list(next(squares_gen) for _ in range(5))}")
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage: {current / 1024 / 1024:.2f} MB")
print(f"Peak memory usage: {peak / 1024 / 1024:.2f} MB")
tracemalloc.stop()

squares_gen = get_squares_generator(n)

print(f"Generator memory: {sys.getsizeof(squares_gen)} bytes")
print(f"List memory: {sys.getsizeof(squares_list)} bytes")

print(f"First 5 from list: {squares_list[:5]}")

print(f"First 5 from generator: {list(next(squares_gen) for _ in range(5))}")

def process_large_file(filename):
    """Generator that processes file line by line without loading everything into memory."""
    with open(filename, 'r') as file:
        for line in file:
            # Process each line
            yield line.strip().upper()

# for processed_line in process_large_file('huge_data.txt'):
#     print(processed_line)

import sys

# Regular class with dynamic attributes
class RegularPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SlottedPoint:
    __slots__ = ['x', 'y']
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Compare memory usage
regular = RegularPoint(10, 20)
slotted = SlottedPoint(10, 20)

print(f"Regular point: {sys.getsizeof(regular)} bytes")
print(f"Regular point __dict__: {sys.getsizeof(regular.__dict__)} bytes")
print(f"Slotted point: {sys.getsizeof(slotted)} bytes")

# Memory difference becomes significant with many instances
regular_points = [RegularPoint(i, i*2) for i in range(1000)]
slotted_points = [SlottedPoint(i, i*2) for i in range(1000)]

print(f"\n1000 regular points: {sum(sys.getsizeof(p) + sys.getsizeof(p.__dict__) for p in regular_points)} bytes")
print(f"1000 slotted points: {sum(sys.getsizeof(p) for p in slotted_points)} bytes")

class Coordinate:
    __slots__ = ['latitude', 'longitude', 'altitude']
    
    def __init__(self, lat, lon, alt=0):
        self.latitude = lat
        self.longitude = lon
        self.altitude = alt
    
    def __repr__(self):
        return f"Coordinate({self.latitude}, {self.longitude}, {self.altitude})"

import array

numbers_list = [i for i in range(1000)]
numbers_array = array.array('i', range(1000))  # 'i' = signed int

print(f"List of 1000 integers: {sys.getsizeof(numbers_list)} bytes")
print(f"Array of 1000 integers: {sys.getsizeof(numbers_array)} bytes")

x = [1,2,3]

x.append(4)

removed = x[0]
x = x[1:]

from collections import deque
# deque is more memory-efficient for queue operations
regular_list = list(range(1000))
efficient_deque = deque(range(1000))

print(f"List memory: {sys.getsizeof(regular_list)} bytes")
print(f"Deque memory: {sys.getsizeof(efficient_deque)} bytes")

import timeit

# Benchmark adding to left side
list_time = timeit.timeit(lambda: regular_list.insert(0, 'new'), number=1000)
deque_time = timeit.timeit(lambda: efficient_deque.appendleft('new'), number=1000)

print(f"List insert(0): {list_time:.6f} seconds")
print(f"Deque appendleft: {deque_time:.6f} seconds")

