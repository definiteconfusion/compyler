import dis

def test_function():
    t = 1
    tx = 1
    _x = ("test", "words")
    for k in range(10):
        t = tx
        tx = t + tx
        print(tx)
    return 1
# def test_function():
#     x = 2
#     y = 2
#     z = x + y
#     print(z)
#     return 1
# dis.disassemble(test_function.__code__)