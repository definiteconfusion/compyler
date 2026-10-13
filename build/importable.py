import dis

def test_function():
    evenInts = [
    ]
    exs = 0
    rg = 10
    for i in range(rg):
        if i % 2 == 0:
            evenInts.append(i)
    for k in evenInts:
        if (k + 5) / 2 > 1:
            exs+=1
    print(exs)

# dis.disassemble(test_function.__code__)