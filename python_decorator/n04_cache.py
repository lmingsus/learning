import time

def cache(func):
    _cache = {}
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        print(key)
        if key in _cache:
            print(f"Cache hit for {func.__name__}{args, kwargs}")
            return _cache[key]
        
        print(f"Cache miss for {func.__name__}{args, kwargs}. Calling function...")
        result = func(*args, **kwargs)
        _cache[key] = result
        print(_cache)
        return result
    return wrapper

@cache
def expensive_function(a, b):
    time.sleep(2) # Simulate a time-consuming operation
    return a + b

print(expensive_function(1, 2))
print(expensive_function(2, 1))
print(expensive_function(1, 2)) # This call should use the cache
print(expensive_function(1, b = 2))
print(expensive_function(b = 2, a = 1))

# =========================================
import inspect

def cache_inspect(func):
    _cache = {}
    sig = inspect.signature(func)  # 取得函式的簽章 (Signature)
    # 定義了哪些參數、順序為何、以及預設值是什麼。

    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        # 將傳入的參數綁定到函式的參數名稱上
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()  # 填入預設值 (如果有)
        
        # 使用綁定後的參數 (OrderedDict) 轉成 tuple 作為 Key
        key = tuple(bound_args.arguments.items())
        
        print(key)
        if key in _cache:
            print(f"Cache hit for {func.__name__}{args, kwargs}")
            return _cache[key]
        
        print(f"Cache miss for {func.__name__}{args, kwargs}. Calling function...")
        result = func(*args, **kwargs)
        _cache[key] = result
        return result
    return wrapper

@cache_inspect
def expensive_function2(a, b):
    # time.sleep(2)
    return a + b

print(expensive_function2(1, 2))
print(expensive_function2(2, 1))
print(expensive_function2(b=2, a=1))