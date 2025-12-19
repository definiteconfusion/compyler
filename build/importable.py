import dis

def test_function():
    for k in range(10):
        print(k%2==0)
# def test_function():
#     x = 2
#     y = 2
#     z = x + y
#     print(z)
#     return 1
# dis.disassemble(test_function.__code__)