import dis

def test_function():
    k = 15
    evenInts = [
    ]
    for i in range(k):
        if i % 2 == 0:
            evenInts.append(i)
    print(evenInts)

# dis.disassemble(test_function.__code__)