def my_decorator(func):
    def wrapper():
        print("Before the function is called.")
        func()
        print("After the function is called.")
    return wrapper


@my_decorator
def print_abc():
    print("abc")

print_abc()
'''
Before the function is called.
abc
After the function is called.
'''


# ===============================
def debug(func):
    def print_name():
        print(f"Calling {func.__name__}")
        print(f"{func.__name__} returned: {func()}")

    return print_name

@debug
def return_xyz():
    return "xyz"

return_xyz()
'''
Calling return_xyz
return_xyz returned: xyz
'''


print(f"The function name seen from outside is: {return_xyz.__name__}")
'''
The function name seen from outside is: print_name
'''

# ===========================
# Write code here
def debug(func):
    def wrapper(x, y):
        print(f"Calling {func.__name__} with arguments ({x}, {y})")
        print(f"{func.__name__} returned: {func(x, y)}")
    return wrapper

@debug
def add(a, b):
    return a + b

add(1, 2)
'''
Calling add with arguments (1, 2)
add returned: 3
'''

# ===========================