# 裝飾器：限制被裝飾函數的所有位置參數必須落在範圍內。
def restrict_range(min_val, max_val):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for arg in args:
                if not (min_val <= arg <= max_val):
                    raise ValueError(f"Argument {arg} is out of allowed range [{min_val}, {max_val}]")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@restrict_range(1, 10)
def set_value(value):
    print(f"Value set to: {value}")

# 正常呼叫
set_value(5)

# 錯誤呼叫 (會拋出 ValueError)
try:
    set_value(0)
except ValueError as e:
    print(e)

try:
    set_value(11)
except ValueError as e:
    print(e)

'''
Value set to: 5
Argument 0 is out of allowed range [1, 10]
Argument 11 is out of allowed range [1, 10]
'''


@restrict_range(0, 100)
def process_percentage(percentage, factor=1):
    print(f"Processing {percentage}% with factor {factor}")
    return percentage * factor

process_percentage(50)
process_percentage(100, factor=2)

try:
    process_percentage(-5)
except ValueError as e:
    print(e)

try:
    process_percentage(101)
except ValueError as e:
    print(e)

'''
Processing 50% with factor 1
Processing 100% with factor 2
Argument -5 is out of allowed range [0, 100]
Argument 101 is out of allowed range [0, 100]
'''

