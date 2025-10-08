import dis
from importable import test_function    
import subprocess

class Compiler:
    
    def __init__(self, input_function) -> None:
        self.INSTRUCTS = dis.get_instructions(input_function)
        
        # temp stacks for const modification
        self.mainStack = []
        
        # final stack to hold objects for rust translation
        self.buildStack = []
        
        # map of python bytecode instructions to handler functions
        self.callMap = {
            "LOAD_CONST": "self.load_const(instruction)",
            "LOAD_FAST": "self.load_fast(instruction)",
            "BINARY_OP": "self.binary_op(instruction)",
            "STORE_FAST": "self.store_fast(instruction)",
            "BUILD_CONST_KEY_MAP": "self.build_const_key_map(instruction)",
            "LIST_EXTEND": "self.list_extend(instruction)",
            "LOAD_GLOBAL": "self.load_global(instruction)",
            "FOR_ITER": "self.for_iter(instruction)",
            "END_FOR": "self.end_for(instruction)"
        }
        
        # map to hold variable data types and values
        self.variables = {}
        pass
    
    # Object Class to hold rust translation stack objects
    class Object:
        def __init__(self, dataType, name="NAN", type:str="NAT", value="NAV") -> None:
            self.type = type
            self.name = name
            self.value = value
            self.dataType = dataType
            self.typeChanged = False
            self.isUsed = False
            pass
        
    # Handler Functions
    def load_const(self, instruction) -> None:
        self.mainStack.append(
            self.Object(
                name=instruction.argval,
                type="CONST",
                value=instruction.argval,
                dataType=type(instruction.argval).__name__
            )
        )
        pass
    
    # Handler for loading variables onto the stack
    def load_fast(self, instruction):
        self.mainStack.append(
            self.Object(
                name=instruction.argval,
                type="VAR",
                value="NaV",
                dataType=None
            )
        )
    
    # Handler for storing variables from the stack
    
    
    # made an exception for loop variables since they are not stored in the same way as normal variables,
    # need to build a method from them
    
    def store_fast(self, instruction):
        if self.mainStack[-1].type != "LOOPSTART":
            self.variables[instruction.argval] = {
                "type": "VAR",
                "value": self.mainStack[-1],
                "dataType": self.mainStack[-1].dataType
            }
            self.buildStack.append(
                self.Object(
                    name=instruction.argval,
                    type="VAR",
                    value=self.mainStack.pop(),
                    dataType=None
                )
            )
        else:
            self.mainStack.pop()
            self.buildStack.append(
                self.Object(
                    name=None, # type: ignore
                    type="LOOPSTART",
                    value=(instruction.argval, self.mainStack.pop()), # type: ignore, # type: ignore
                    dataType=None
                )
            )
            print()
        
    # Handler for binary operations (`+`, `-`, `*`, `/`, etc)
    def binary_op(self, instruction):
        right = self.mainStack.pop()
        left = self.mainStack.pop()
        if self.variables[left.name]["dataType"] == "str" and self.variables[right.name]["dataType"] == "str":
            'format!("{}{}", nam, age);'
            self.mainStack.append(
                self.Object(
                    name=f'format!("{{}}{{}}", {str(left.name)}, {str(right.name)})',
                    type="CONST",
                    value=f'format!("{{}}{{}}", {str(left.name)}, {str(right.name)})',
                    dataType="NaV"
                )
            )
            print()
        elif self.variables[left.name]["dataType"] == "int" and self.variables[right.name]["dataType"] == "int":
            self.mainStack.append(
                self.Object(
                    name=f"{str(left.name)} {instruction.argrepr} {str(right.name)}",
                    type="CONST",
                    value=f"{str(left.value)} {instruction.argrepr} {str(right.value)}",
                    dataType="NaV"
                )
            )
        else:
            self.mainStack.append(
                self.Object(
                    name=f'format!("{{}}{{}}", {str(left.name)}, {str(right.name)})',
                    type="CONST",
                    value=f'format!("{{}}{{}}", {str(left.name)}, {str(right.name)})',
                    dataType="NaV"
                )
            )
        pass    
    
    def load_global(self, instruction):
        self.mainStack.append(
            self.Object(
                name=instruction.argval,
                type="GLOBAL",
                value="NaV",
                dataType=None
            )
        )
        print()
        pass
    
    def for_iter(self, instruction):
        self.mainStack.append(
            self.Object(
                name="NaV",
                type="LOOPSTART",
                value="NaV",
                dataType="NaV"
            )
        )
        print()
        pass
    
    def end_for(self, instruction):
        self.buildStack.append(
            self.Object(
                name="}",
                type="LOOPEND",
                value="NaV",
                dataType="NaV"
            )
        )
        print()
        pass
    
    # Handler for building constant key maps (dictionaries)
    def build_const_key_map(self, instruction):
        num_values = instruction.argval
        keys = self.mainStack.pop().name[::-1]
        pairs = []
        for i in range(num_values):
            value = self.mainStack.pop().name
            pairs.append((keys[i], value))
        self.mainStack.append(
            self.Object(
                name=str(pairs).replace("'", '"'),
                type="CONST",
                value=str(pairs),
                dataType="dict"
            )
        )
        
    # Handler for extending lists with multiple values
    def list_extend(self, instruction):
        vals = list(self.mainStack.pop().name)
        self.mainStack.append(
            self.Object(
                name=str(vals).replace("'", '"'),
                type="CONST",
                value=str(vals),
                dataType="list"
            )
        )
    
    
    # Main Prep Function to transform the instructions into stack objects    
    def prePrep(self):
        for instruction in self.INSTRUCTS:
            if instruction.opname in self.callMap:
                exec(self.callMap[instruction.opname])
        pass
                
    # Final Prep Class to transform stack objects into Rust code
    class FinalPrep:
        def __init__(self, buildMap) -> None:
            
            # All function within the map should return a string that is valid Rust code
            self.transMap = {
                "VAR": "self.transform_var(obj)",
                "LOOPSTART": "self.transform_loop(obj)",
                "LOOPEND": 'self.transform_loop_end(obj)',
            }
            self.buildMap = buildMap
            self.rsOut = []
            self.optionalImports = []
            self.optionalImportsMap = {
                "HashMap": "use std::collections::HashMap;"
            }
            pass

        # Handler to transform variable objects into Rust code
        def transform_var(self, obj):
            if obj.value.dataType == "dict":
                self.optionalImports.append(
                    self.optionalImportsMap["HashMap"]
                )
                return (
                    f"let {obj.name} = HashMap::from({obj.value.name});"
                )
            elif obj.value.dataType != "str":
                return (
                    f"let {obj.name} = {obj.value.name};"
                )
            else:
                return (
                    f'let {obj.name} = "{obj.value.name}";'
                )
            pass
        
        def transform_loop(self, obj):
            loop_var, loop_iterable = obj.value
            return (
                    f"for {loop_var} in {loop_iterable.name}.iter() {{"
                )
        
        def transform_loop_end(self, obj):
            return (
                f"}}"
            )

        # Main prep function to process the build map and generate Rust code
        def prep(self):
            for obj in self.buildMap:
                if obj.type in self.transMap:
                    self.rsOut.append(eval(self.transMap[obj.type]))
            self.rsOut = ["fn main() {"] + self.optionalImports + self.rsOut + ["}"]
        
        # Function to write the generated Rust code to a file    
        def write_to_file(self, filename="./build/package/output.rs", mode="development"):
            with open(filename, "w") as f:
                for line in self.rsOut:
                    f.write(line + "\n") if mode == "development" else f.write(line)

main = Compiler(test_function)
main.prePrep()
final = main.FinalPrep(main.buildStack)
final.prep()
final.write_to_file(mode="development")
subprocess.run(["bash", "./test.sh"])