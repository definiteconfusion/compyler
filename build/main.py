import dis
from importable import test_function    

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
            "LOAD_ATTR": "self.load_global(instruction)",
            "FOR_ITER": "self.for_iter(instruction)",
            "END_FOR": "self.end_for(instruction)",
            "CALL": "self.call(instruction)",
            "POP_JUMP_IF_FALSE": "self.pop_jump_if_false(instruction)",
            "POP_JUMP_IF_TRUE": "self.pop_jump_if_true(instruction)",
            "COMPARE_OP": "self.compare_operation(instruction)",
            "BUILD_LIST": "self.build_list(instruction)",
            # "POP_TOP": "self.end_for(instruction)"
        }
        
        # map to hold variable data types and values
        self.variables = {}
        self.jumpOffset = None
        self.reqClosure = 0
        pass
    
    # Object Class to hold rust translation stack objects
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
            self.reqMut = False
            self.originByteAddress = byteAddress
            pass
        def __repr__(self) -> str:
            attributes = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
            return f"{self.__class__.__name__}({attributes})"

        
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
        ttx = None
        if instruction.argval in self.variables:
            ttx = self.variables[instruction.argval]["dataType"]
        self.mainStack.append(
            self.Object(
                name=instruction.argval,
                type="VAR",
                value="NaV",
                dataType=ttx,
                byteAddress=instruction.offset
            )
        )
    
    # Handler for storing variables from the stack
    
    
    # made an exception for loop variables since they are not stored in the same way as normal variables,
    # need to build a method from them
    
    def store_fast(self, instruction):
        if self.mainStack[-1].type != "LOOPSTART":
            if instruction.argval in self.variables:
                for index, value in enumerate(self.buildStack):
                    if value.name == instruction.argval:
                        self.buildStack[index].reqMut = True
            self.variables[instruction.argval] = {
                "type": "VAR",
                "value": self.mainStack[-1],
                "dataType": self.mainStack[-1].dataType
            }
            self.buildStack.append(
                self.Object(
                    name=instruction.argval,
                    type="VAR",
                    dataType=self.mainStack[-1].dataType,
                    value=self.mainStack.pop(),
                    byteAddress=instruction.offset
                )
            )
        else:
            self.variables[instruction.argval] = {
                "type": "VAR",
                "value": self.mainStack[-1],
                "dataType": self.mainStack[-1].dataType
            }
            self.mainStack.pop()
            self.buildStack.append(
                self.Object(
                    name=None, # type: ignore
                    type="LOOPSTART",
                    value=(instruction.argval, self.mainStack.pop()), # type: ignore, # type: ignore
                    dataType=str(type(instruction.argval).__name__),
                    byteAddress=instruction.offset
                )
            )
            
        
    # Handler for binary operations (`+`, `-`, `*`, `/`, etc)
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
            # if left.dataType != right.dataType:
            #     raise TypeError(f"Expression types not consistent -> {left.dataType} | {right.dataType}")
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
                if instruction.argrepr == "//":
                    self.mainStack.append(
                        self.Object(
                            name=f"{str(left.name)} / {str(right.name)}",
                            type="CONST",
                            value=f"{str(left.value)} {instruction.argrepr} {str(right.value)}",
                            dataType="NaV"
                        )
                    )
                else:
                    self.mainStack.append(
                        self.Object(
                            name=f"{str(left.name)} {instruction.argrepr} {str(right.name)}",
                            type="CONST",
                            value=f"{str(left.value)} {instruction.argrepr} {str(right.value)}",
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
        
        pass
    
    def end_for(self, instruction):
        if self.reqClosure>0:
            for k in range(self.reqClosure):
                self.buildStack.append(
                            self.Object(
                                name="}",
                                type="LOOPEND",
                                value="NaV",
                                dataType="NaV",
                                byteAddress=instruction.offset
                            )
                        )
            self.reqClosure=0
        self.buildStack.append(
            self.Object(
                name="}",
                type="LOOPEND",
                value="NaV",
                dataType="NaV",
                byteAddress=instruction.offset
            )
        )
        
        pass

    def pop_jump_if_false(self, instruction):
        self.jumpOffset = instruction.argval
        self.buildStack.append(
            self.Object(
                name="NaV",
                type="BOOLSTART",
                value=self.mainStack.pop(),
                dataType="NaV",
                byteAddress=instruction.argval
            )
        )
        pass
    def pop_jump_if_true(self, instruction):
        self.reqClosure +=1
        self.buildStack.append(
            self.Object(
                name="NaV",
                type="BOOLSTART",
                value=self.mainStack.pop(),
                dataType="NaV",
                byteAddress=instruction.argval
            )
        )
        pass
    
    def compare_operation(self, instruction):
        right = self.mainStack.pop()
        left = self.mainStack.pop()
        self.mainStack.append(
            self.Object(
                name=f"{str(left.name)} {instruction.argrepr} {str(right.name)}",
                type="CONST",
                value=f"{str(left.value)} {instruction.argrepr} {str(right.value)}",
                dataType="NaV"
            )
        )
        pass
    
    def call(self, instruction):
        globals = {
            "print":"_print(self.mainStack)",
            "range":"_range(self.mainStack)",
            "append":"_append(self.mainStack)"
        }
        def _print(mainStack):
            if mainStack[-1].dataType != "str":
                tX = self.Object(
                        name=f'println!("{{:?}}", ' + f"{mainStack[-1].name}" + ');',
                        type="GLOBAL",
                        value="NaV",
                        dataType="NaV",
                        byteAddress=mainStack[-1].originByteAddress
                    )
            else:
                tX = self.Object(
                        name=f'println!("{{}}", ' + f'"{mainStack[-1].name}"' + ');',
                        type="GLOBAL",
                        value="NaV",
                        dataType="NaV",
                        byteAddress=mainStack[-1].originByteAddress
                        
                    )
            
            self.buildStack.append(
                    tX
        )
        def _range(mainStack):
            pass
        def _append(mainStack):
            value_to_add = mainStack.pop()
            list_obj = mainStack.pop()
            for index, value in enumerate(self.buildStack):
                if value.name == list_obj.name:
                    self.buildStack[index].reqMut = True
            if value_to_add.type == "VAR":
                tX = self.Object(
                        name=f'{list_obj.name}.push({value_to_add.name});',
                        type="GLOBAL",
                        value="NaV",
                        dataType="NaV",
                        byteAddress=value_to_add.originByteAddress
                    )
            else:
                # add datatype check logic
                pass
            self.buildStack.append(
                tX
        )
        # for item in self.mainStack:
        #     print(item)
        for item in reversed(self.mainStack):
            if item.type == "GLOBAL":
                self.mainStack.remove(item)  # Remove the GLOBAL from stack
                if item.name in globals:
                    exec(globals[item.name])
                    break
                    
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
    def build_list(self, instruction):
        num_values = instruction.argval
        vals = []
        for i in range(num_values):
            value = self.mainStack.pop().name
            vals.append(value)
        vals.reverse()
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
                    if self.jumpOffset is not None:
                        if instruction.offset >= self.jumpOffset: # type: ignore
                            self.buildStack.append(
                                self.Object(
                                    name="}",
                                    type="LOOPEND",
                                    value="NaV",
                                    dataType="NaV",
                                    byteAddress=instruction.offset # type: ignore
                                )
                            )
                            self.jumpOffset = None
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
                "GLOBAL": 'self.transform_global(obj)',
                "BOOLSTART": 'self.transform_bool_start(obj)',
            }
            self.buildMap = buildMap
            self.rsOut = []
            self.optionalImports = []
            self.optionalImportsMap = {
                "HashMap": "use std::collections::HashMap;"
            }
            self.preInitVars = []
            self.include_trace_address = False
            pass

        def transform_bool_start(self, obj):
            if self.include_trace_address:
                return f"/*{obj.originByteAddress}*/\nif {obj.value.name} {{"
            else:
                return f"if {obj.value.name} {{"

        # Handler to transform variable objects into Rust code
        def transform_var(self, obj):
            is_new_var = obj.name not in self.preInitVars
            
            if is_new_var:
                self.preInitVars.append(obj.name)
            
            # Handle dict type
            if obj.value.dataType == "dict":
                self.optionalImports.append(self.optionalImportsMap["HashMap"])
                value = f"HashMap::from({obj.value.name})"
            # Handle tuple type
            elif obj.value.dataType == "tuple":
                value = str(obj.value.name).replace("'", '"')
            # Handle string type
            elif obj.value.dataType == "str":
                value = f'"{obj.value.name}"'
            # Handle all other types
            elif obj.value.dataType == "list":
                value = f"vec!{obj.value.name}"
            else:
                value = obj.value.name
            
            # Add 'let mut' prefix only for new variables
            # prefix = "let mut " if is_new_var else ""
            if is_new_var:
                if obj.reqMut:
                    prefix = "let mut "
                else:
                    prefix = "let "
            else:
                prefix = ""
            if type(value) == str:
                if "+=" in value or "-=" in value or "*=" in value or "/=" in value:
                    if self.include_trace_address:
                        return f"/*{obj.originByteAddress}*/\n{value};"
                    else:
                        return f"{value};"
            if self.include_trace_address:
                return f"/*{obj.originByteAddress}*/\n{prefix}{obj.name} = {value};"
            else:
                return f"{prefix}{obj.name} = {value};"
        
        def transform_global(self, obj):
            if self.include_trace_address:
                return f"/*{obj.originByteAddress}*/\n{obj.name}"
            else:
                return f"{obj.name}"
        
        def transform_loop(self, obj):
            loop_var, loop_iterable = obj.value
            if loop_iterable.type == "CONST" or loop_iterable.dataType == "int":
                if self.include_trace_address:
                    return (
                            f"/*{obj.originByteAddress}*/\nfor {loop_var} in 0..{loop_iterable.name} {{"
                        )
                else:
                    return (
                            f"for {loop_var} in 0..{loop_iterable.name} {{"
                        )
            else:
                if self.include_trace_address:
                    return (
                            f"/*{obj.originByteAddress}*/\nfor {loop_var} in {loop_iterable.name}.iter() {{"
                        )
                else:
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
                    f.write(line + "\n") if mode == "development" else f.write(line.replace("\n", ""))

main = Compiler(test_function)
main.prePrep()
final = main.FinalPrep(main.buildStack)
final.include_trace_address=True
final.prep()
final.write_to_file(mode="development")
# final.write_to_file(mode="production")