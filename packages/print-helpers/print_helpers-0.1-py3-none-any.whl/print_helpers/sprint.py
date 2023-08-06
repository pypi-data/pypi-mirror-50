def starry_print(*args):
    for i in args:
        print(i, end="*")


def tacky_print(*args):
    print("---", *args, "---", end="")