import dis

def test_function():
    name = "Jake"
    age = 18
    attrs = {
        "favorite color": 18,
        "cars age": 21
    }
    pets = [
        "Callie",
        "Mae",
        "Aiobh",
        "Thalia"
    ]
    
    for pet in pets:
        print(pet)
    
    for k in range(4):
        print(k)
    
    return 1

# dis.disassemble(test_function.__code__)