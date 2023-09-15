import sys

# Function to calculate the size of an object in bytes
def get_size(obj):
    return sys.getsizeof(obj)

# Creating and measuring memory usage of various objects
int_num = 42
str_text = "Hello, Python!"
list_data = [1, 2, 3, 4, 5]
dict_data = {'a': 1, 'b': 2, 'c': 3}
tuple_data = (1, 2, 3, 4, 5)

print(f"Size of an integer: {get_size(int_num)} bytes")
print(f"Size of a string: {get_size(str_text)} bytes")
print(f"Size of a list: {get_size(list_data)} bytes")
print(f"Size of a dictionary: {get_size(dict_data)} bytes")
print(f"Size of a tuple: {get_size(tuple_data)} bytes")

# Creating a large list to demonstrate memory allocation
large_list = [x for x in range(1, 10001)]
print(f"Size of a large list: {get_size(large_list)} bytes")

# Creating circular references to show garbage collection
a = [1]
b = [2]
a.append(b)
b.append(a)

# Deliberately breaking references to enable garbage collection
del a
del b

# Forcing garbage collection (not typically done in practice)
import gc
gc.collect()

print("Circular references have been collected by the garbage collector.")


