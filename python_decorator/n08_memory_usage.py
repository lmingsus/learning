'''
import tracemalloc
tracemalloc.start()
res = # some operations
current, peak = tracemalloc.get_traced_memory()
'''
import time
import tracemalloc
from functools import wraps

def measure_memory_usage(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        result = func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        print(f"Memory usage for {func.__name__}: Current={current:.2f}B, Peak={peak / 10**6:.2f}MB")
        tracemalloc.stop()
        return result
    return wrapper

@measure_memory_usage
def create_large_list(size):
    return [i for i in range(size)]

@measure_memory_usage
def process_data(data):
    # Simulate some data processing
    time.sleep(0.1)
    # 為了展示記憶體變化，這裡建立一個新的列表 (例如將所有數字 * 2)
    # 原本的 sum(data) 幾乎不消耗額外記憶體，因為 data 是從外部傳入且未被複製
    processed_data = [x * 2 for x in data]
    return sum(processed_data)

if __name__ == "__main__":
    print("Measuring memory usage for create_large_list:")
    large_list = create_large_list(10**6) # Create a list of 1 million integers

    print("\nMeasuring memory usage for process_data:")
    process_data(large_list)

    # Example with a smaller list
    print("\nMeasuring memory usage for create_large_list (smaller):")
    small_list = create_large_list(10**3)

    print("\nMeasuring memory usage for process_data (smaller):")
    process_data(small_list)

'''
Measuring memory usage for create_large_list:
Memory usage for create_large_list: Current=40440448.00B, Peak=40.44MB

Measuring memory usage for process_data:
Memory usage for process_data: Current=32.00B, Peak=40.44MB

Measuring memory usage for create_large_list (smaller):
Memory usage for create_large_list: Current=32576.00B, Peak=0.03MB

Measuring memory usage for process_data (smaller):
Memory usage for process_data: Current=28.00B, Peak=0.04MB
'''