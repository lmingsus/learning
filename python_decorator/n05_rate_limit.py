import time

import time
from functools import wraps
import math

def rate_limit(max_calls):
    # Write code here
    # max_calls = max(max_calls, 1)
    def decorator(func):
        call_times = set()
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal call_times # 必須聲明 nonlocal 才能修改外部作用域的集合
            current_time = time.monotonic()

            call_times = set(x for x in call_times if current_time - x < 1)
            if len(call_times) >= max_calls:
                print("Function called too quickly")
                return None
            else:
                call_times.add(current_time)
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@rate_limit(3) # Allow 3 calls every 5 seconds
def send_notification(user_id, message):
    """Simulates sending a notification."""
    print(f"Sending notification to {user_id}: {message}")
    return f"Notification sent to {user_id}"

if __name__ == "__main__":
    print("Testing rate_limit decorator:")

    # First 3 calls should go through immediately
    for i in range(1, 4):
        send_notification(f"user_{i}", f"Hello {i}")
        time.sleep(0.15) # Simulate some work between calls

    # The 4th call should be delayed
    print("\nAttempting 4th call (should be delayed):")
    send_notification("user_4", "Hello 4")