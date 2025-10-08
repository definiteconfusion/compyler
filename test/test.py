import dis 


def test_function():
    name = "Jake"
    age = 18
    attrs = {
        "favorite color": "sage green",
        "car's age": 21
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

dis.disassemble(test_function.__code__)

# look at the class system from the cloudqlite project and try to make each action a class that only compiles to code from those classes at the very end