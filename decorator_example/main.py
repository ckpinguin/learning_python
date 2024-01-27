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


@delay_decorator
def say_hello():
    print("Hello")


@delay_decorator_with_args(2)
def say(text):
    print(text)


decorated_say_hello = delay_decorator(say_hello)

say("huhuu")
say_hello()
decorated_say_hello()
