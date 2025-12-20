
class Base:
    def __init__(self):
        self.mainStack = [
            self.Object(None, 'k', "VAR", "NaV", None),#type: ignore
            self.Object("str", "ktx", "CONST", 2, None), #type: ignore
        ]
        self.variables = {
            'k':{
                'type': "VAR",
                'dataType': "NaV"
            }
        }
    class Object:
        def __init__(self, dataType, name="NAN", type:str="NAT", value="NAV", byteAddress="NaA") -> None:
            self.type = type
            self.name = name
            self.value = value
            self.dataType = dataType
            self.typeChanged = False
            self.isUsed = False
            self.preInit = False
            self.byteAddress = None
            pass
        def __repr__(self):
            return f'{self.__class__.__name__}({", ".join([f"{key}={repr(value)}" for key, value in self.__dict__.items()])})'
    def binary_op(self, instruction):
        if instruction.argrepr:
            isA = False
            if instruction.argrepr == "+":
                isA = True
            right = self.mainStack.pop()
            left = self.mainStack.pop()
            if right.name or left.name in self.variables:
                if right.name in self.variables:
                    for key, value in right.__dict__.items():
                        if value == None:
                            right.__dict__[key] = left.__dict__[key]
                else:
                    for key, value in left.__dict__.items():
                        if value == None:
                            left.__dict__[key] = right.__dict__[key]
            if left.dataType != right.dataType:
                raise TypeError(f"Expression types not consistent -> {left.dataType} | {right.dataType}")
            if left.dataType == "str":
                left.name = f'"{left.name}"' if left.value != "NaV" else left.name
                right.name = f'"{right.name}"' if right.value != "NaV" else right.name
                if isA:
                    self.mainStack.append(
                        self.Object(
                            name=f'format!("{{}}{{}}", {str(left.name)}, {str(right.name)})',
                            type="CONST",
                            value=f'format!("{{}}{{}}", {str(left.name)}, {str(right.name)})',
                            dataType="NaV"
                        )
                    )
                else:
                    raise TypeError("Cannot perform bollean operations on objects of type `str`")
            else:
                self.mainStack.append(
                    self.Object(
                        name=f"{str(left.name)} {instruction.argrepr} {str(right.name)}",
                        type="CONST",
                        value=f"{str(left.value)} {instruction.argrepr} {str(right.value)}",
                        dataType="NaV"
                    )
                )
                
class Instruction:
    def __init__(self, argrepr) -> None:
         self.argrepr = argrepr

Instrct = Instruction(
    argrepr='+'
)

B = Base()

B.binary_op(Instrct)
print(B.mainStack)