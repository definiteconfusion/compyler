import dis

def test_function():
    cnt = 1
    while cnt < 5:
        print(cnt)
        cnt += 1
# def test_function():
#     x = 2
#     y = 2
#     z = x + y
#     print(z)
#     return 1
# dis.disassemble(test_function.__code__)