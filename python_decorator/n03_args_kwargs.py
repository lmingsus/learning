def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before the function is called.")
        result = func(*args, **kwargs)
        print("After the function is called.")
        return result
    return wrapper

@my_decorator
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")
    return f"{greeting}, {name}!"

greet("Alice")
greet("Bob", greeting="Hi")

'''
Before the function is called.
Hello, Alice!
After the function is called.
Before the function is called.
Hi, Bob!
After the function is called.
'''

# ==================================
def debug(func):
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__}({signature})")
        result = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {result!r}\n")
        return result
    return wrapper

@debug
def add(a, b):
    return a + b

@debug
def multiply(x, y=1):
    return x * y

add(1, 2)
multiply(5)
multiply(3, y=4)

'''
Calling add(1, 2)
'add' returned 3
Calling multiply(5)
'multiply' returned 5
Calling multiply(3, y=4)
'multiply' returned 12
'''
