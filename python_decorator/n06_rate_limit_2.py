import time
from functools import wraps
import math

def rate_limit_token_bucket(
    max_calls: float,  # 例如：5.0 (每秒 5 次)
    capacity: int = None
):
    if capacity is None:
        capacity = max_calls
    tokens = capacity
    last_reset_time = time.monotonic()

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal tokens, last_reset_time
            current_time = time.monotonic()
            time_passed = current_time - last_reset_time
            
            # 計算這段時間內應該補充多少 token
            # min(capacity, ...) 確保 token 不會超過桶的容量
            tokens_to_add = time_passed * max_calls
            tokens = min(capacity, tokens + tokens_to_add)
            last_reset_time = current_time

            if tokens >= 1:
                tokens -= 1  # 消耗一個 token
                print(f"Token available. Remaining tokens: {tokens:.2f}")
                return func(*args, **kwargs)
            else:
                print(f"Rate limit exceeded. No tokens available. Remaining tokens: {tokens:.2f}")
                return None
        return wrapper
    return decorator

@rate_limit_token_bucket(max_calls=1, capacity=3) # 每秒1次，桶容量3
def process_request(request_id):
    """模擬處理一個請求"""
    print(f"Processing request {request_id}")
    return f"Request {request_id} processed"

if __name__ == "__main__":
    print("Testing rate_limit_token_bucket decorator:")

    # 第一次測試：連續呼叫，觀察令牌桶機制
    print("\n--- Test 1: Burst calls ---")
    for i in range(1, 10):
        process_request(f"T1-{i}")
        time.sleep(0.2) # 每次呼叫間隔 0.2 秒

    # 第二次測試：等待一段時間後再次呼叫，觀察令牌補充
    print("\n--- Test 2: After a pause ---")
    print("Waiting for 3 seconds to allow tokens to replenish...")
    time.sleep(3)
    for i in range(1, 10):
        process_request(f"T2-{i}")
        time.sleep(0.5) # 每次呼叫間隔 0

'''
--- Test 1: Burst calls ---
Token available. Remaining tokens: 2.00
Processing request T1-1
Token available. Remaining tokens: 1.41
Processing request T1-2
Token available. Remaining tokens: 0.72
Processing request T1-3
Rate limit exceeded. No tokens available. Remaining tokens: 0.92
Token available. Remaining tokens: 0.17
Processing request T1-5
Rate limit exceeded. No tokens available. Remaining tokens: 0.44
Rate limit exceeded. No tokens available. Remaining tokens: 0.67
Rate limit exceeded. No tokens available. Remaining tokens: 0.89
Token available. Remaining tokens: 0.09
Processing request T1-9

--- Test 2: After a pause ---
Waiting for 3 seconds to allow tokens to replenish...
Token available. Remaining tokens: 2.00
Processing request T2-1
Token available. Remaining tokens: 1.50
Processing request T2-2
Token available. Remaining tokens: 1.00
Processing request T2-3
Token available. Remaining tokens: 0.52
Processing request T2-4
Token available. Remaining tokens: 0.02
Processing request T2-5
Rate limit exceeded. No tokens available. Remaining tokens: 0.50
Token available. Remaining tokens: 0.02
Processing request T2-7
Rate limit exceeded. No tokens available. Remaining tokens: 0.52
Token available. Remaining tokens: 0.02
Processing request T2-9
'''