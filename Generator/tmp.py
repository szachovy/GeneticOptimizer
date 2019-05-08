#!/usr/bin/env python3
a = "a"

def check(a):
    try:
        a = int(a)
    except ValueError as e:
        print("ValueError raised")

    return type(a)

print(check(a))