"""Helper functions and decorators"""
import time
from functools import wraps

def retry_on_error(max_attempts=3, delay_seconds=1):
    """
    Decorator to retry a function on failure.
    
    Args:
        max_attempts (int): Maximum number of retry attempts
        delay_seconds (int): Delay between retries in seconds
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            last_error = None
            
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    last_error = e
                    
                    if attempts < max_attempts:
                        print(f"\n Attempt {attempts} failed. Retrying in {delay_seconds} seconds...")
                        time.sleep(delay_seconds)
                    else:
                        print(f"\n❌ All {max_attempts} attempts failed.")
                        raise last_error
                        
            return None
        return wrapper
    return decorator 