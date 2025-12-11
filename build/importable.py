import dis

def test_function():
    t = 2
    if t == 1:
        print("Hello, World!")
    print("Goodbye, World!")
    print(1 == 1)
    return 1
# def test_function():
#     x = 2
#     y = 2
#     z = x + y
#     print(z)
#     return 1
# dis.disassemble(test_function.__code__)