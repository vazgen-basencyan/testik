import time

def wait_for(callback, condition, delay=15, timeout=300):
    start_time = time.time()

    while timeout is None or time.time() - start_time < timeout:
        result = callback()
        if condition(result):
            return result
        time.sleep(delay)

    if timeout is not None and time.time() - start_time >= timeout:
        raise TimeoutError("Timeout exceeded while waiting for condition.")