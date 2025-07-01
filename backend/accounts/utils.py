import random

def generate_otp():
    return random.randint(100_000, 999_999)

def forprint(*args):
    for i in args:
        print("PRINT -> ", i)