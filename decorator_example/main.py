import time


def delay_decorator(function):
    def wrapper():
        time.sleep(1)
        function()

    return wrapper


def delay_decorator_with_args(sleep_seconds):
    def delay_decorator(func):
        def wrapper(*args, **kwargs):
            time.sleep(sleep_seconds)
            return func(*args, **kwargs)
        return wrapper
    return delay_decorator


current_time = time.time()


def timer_decorator(function):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        function(*args, **kwargs)
        diff_time = time.time() - start_time
        print(f"{function.__name__} ran {diff_time} seconds.")
    return wrapper


@timer_decorator
def long_running(number):
    for i in range(0, number):
        n = i


long_running(200000000)


@delay_decorator
@timer_decorator
def say_hello():
    print("Hello")


@delay_decorator_with_args(2)
def say(text):
    print(text)


decorated_say_hello = delay_decorator(say_hello)

say("huhuu")
say(text="yup")
say_hello()
decorated_say_hello()
