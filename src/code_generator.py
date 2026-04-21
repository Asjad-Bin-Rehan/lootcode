"""
Code Generator / Interpreter for LootCode
Phase 6: Executes Three-Address Code
"""

class CodeGenerator:
    def __init__(self):
        self.variables = {}
        self.output = []
        self.pc = 0  # Program counter
        self.labels = {}  # Label positions
        self.recipes = {}  # Recipe definitions
        self.call_stack = []  # Function call stack
        self.param_stack = []  # Parameter stack
    
    def execute(self, instructions):
        """Execute TAC instructions"""
        # First pass: collect label positions and quest definitions
        for i, instr in enumerate(instructions):
            if instr.op == 'label':
                self.labels[instr.result] = i
            elif instr.op == 'begin_quest':
                self.recipes[instr.result] = i
        
        # Second pass: execute instructions (skip quest bodies initially)
        self.pc = 0
        max_iterations = len(instructions) * 100  # Safety limit
        iteration_count = 0
        
        while self.pc < len(instructions):
            iteration_count += 1
            if iteration_count > max_iterations:
                raise Exception(f"Infinite loop detected at PC={self.pc}, instruction: {instructions[self.pc]}")
            
            instr = instructions[self.pc]
            
            # Skip quest definitions during main execution
            if instr.op == 'begin_quest':
                # Find end of quest
                depth = 1
                self.pc += 1
                while self.pc < len(instructions) and depth > 0:
                    if instructions[self.pc].op == 'begin_quest':
                        depth += 1
                    elif instructions[self.pc].op == 'end_quest':
                        depth -= 1
                    self.pc += 1
                continue
            
            result = self.execute_instruction(instr, instructions)
            if result == 'return':
                break
            self.pc += 1
        
        return self.output
    
    def execute_instruction(self, instr, instructions=None):
        """Execute single TAC instruction"""
        if instr.op == 'begin_quest' or instr.op == 'end_quest':
            return None
        
        elif instr.op == 'param':
            # Push parameter onto stack
            value = self.get_value(instr.arg1)
            self.param_stack.append(value)
        
        elif instr.op == 'call':
            # Call quest
            quest_name = instr.arg1
            arg_count = instr.arg2
            
            if quest_name not in self.recipes:
                raise Exception(f"Runtime Error: Quest '{quest_name}' not defined")
            
            # Pop arguments from param stack
            args = []
            for _ in range(arg_count):
                if self.param_stack:
                    args.insert(0, self.param_stack.pop())
            
            # Execute quest
            result = self.execute_quest(quest_name, args, instructions)
            self.variables[instr.result] = result
        
        elif instr.op == 'return':
            # Return from recipe
            if instr.arg1:
                return_value = self.get_value(instr.arg1)
                return ('return', return_value)
            return ('return', None)
        
        elif instr.op == 'assign':
            value = self.get_value(instr.arg1)
            
            # Handle "variable_name unit" (e.g., "adjusted minutes")
            if isinstance(value, str) and ' ' in value:
                parts = value.split(None, 1)
                if parts[0] in self.variables:
                    resolved_value = self.variables[parts[0]]
                    value = f"{resolved_value} {parts[1]}"
                elif parts[0].startswith('t') and parts[0][1:].isdigit() and parts[0] in self.variables:
                    resolved_value = self.variables[parts[0]]
                    value = f"{resolved_value} {parts[1]}"
            elif isinstance(value, str) and value.startswith('t') and value[1:].isdigit():
                if value in self.variables:
                    value = self.variables[value]
            
            self.variables[instr.result] = value
        
        elif instr.op == 'add':
            val1 = self.get_value(instr.arg1)
            val2 = self.get_value(instr.arg2)
            self.variables[instr.result] = val1 + val2
        
        elif instr.op == 'sub':
            val1 = self.get_value(instr.arg1)
            val2 = self.get_value(instr.arg2)
            self.variables[instr.result] = val1 - val2
        
        elif instr.op == 'mul':
            val1 = self.get_value(instr.arg1)
            val2 = self.get_value(instr.arg2)
            # Handle string values (extract numeric part)
            if isinstance(val1, str) and ' ' in val1:
                try:
                    val1 = float(val1.split()[0])
                except (ValueError, IndexError):
                    pass
            if isinstance(val2, str) and ' ' in val2:
                try:
                    val2 = float(val2.split()[0])
                except (ValueError, IndexError):
                    pass
            self.variables[instr.result] = val1 * val2
        
        elif instr.op == 'div':
            val1 = self.get_value(instr.arg1)
            val2 = self.get_value(instr.arg2)
            # Handle string values (extract numeric part)
            if isinstance(val1, str) and ' ' in val1:
                try:
                    val1 = float(val1.split()[0])
                except (ValueError, IndexError):
                    pass
            if isinstance(val2, str) and ' ' in val2:
                try:
                    val2 = float(val2.split()[0])
                except (ValueError, IndexError):
                    pass
            if val2 == 0:
                raise Exception("Runtime Error: Division by zero")
            self.variables[instr.result] = val1 / val2
        
        elif instr.op == 'eq':
            val1 = self.get_value(instr.arg1)
            val2 = self.get_value(instr.arg2)
            self.variables[instr.result] = 1 if val1 == val2 else 0
        
        elif instr.op == 'neq':
            val1 = self.get_value(instr.arg1)
            val2 = self.get_value(instr.arg2)
            self.variables[instr.result] = 1 if val1 != val2 else 0
        
        elif instr.op == 'gt':
            val1 = self.get_value(instr.arg1)
            val2 = self.get_value(instr.arg2)
            # Handle string values (extract numeric part)
            if isinstance(val1, str) and ' ' in val1:
                try:
                    val1 = float(val1.split()[0])
                except (ValueError, IndexError):
                    pass
            if isinstance(val2, str) and ' ' in val2:
                try:
                    val2 = float(val2.split()[0])
                except (ValueError, IndexError):
                    pass
            self.variables[instr.result] = 1 if val1 > val2 else 0
        
        elif instr.op == 'lt':
            val1 = self.get_value(instr.arg1)
            val2 = self.get_value(instr.arg2)
            # Handle string values (extract numeric part)
            if isinstance(val1, str) and ' ' in val1:
                try:
                    val1 = float(val1.split()[0])
                except (ValueError, IndexError):
                    pass
            if isinstance(val2, str) and ' ' in val2:
                try:
                    val2 = float(val2.split()[0])
                except (ValueError, IndexError):
                    pass
            self.variables[instr.result] = 1 if val1 < val2 else 0
        
        elif instr.op == 'gte':
            val1 = self.get_value(instr.arg1)
            val2 = self.get_value(instr.arg2)
            # Handle string values (extract numeric part)
            if isinstance(val1, str) and ' ' in val1:
                try:
                    val1 = float(val1.split()[0])
                except (ValueError, IndexError):
                    pass
            if isinstance(val2, str) and ' ' in val2:
                try:
                    val2 = float(val2.split()[0])
                except (ValueError, IndexError):
                    pass
            self.variables[instr.result] = 1 if val1 >= val2 else 0
        
        elif instr.op == 'lte':
            val1 = self.get_value(instr.arg1)
            val2 = self.get_value(instr.arg2)
            # Handle string values (extract numeric part)
            if isinstance(val1, str) and ' ' in val1:
                try:
                    val1 = float(val1.split()[0])
                except (ValueError, IndexError):
                    pass
            if isinstance(val2, str) and ' ' in val2:
                try:
                    val2 = float(val2.split()[0])
                except (ValueError, IndexError):
                    pass
            self.variables[instr.result] = 1 if val1 <= val2 else 0
        
        elif instr.op == 'label':
            pass  # Labels are handled in first pass
        
        elif instr.op == 'goto':
            if instr.result in self.labels:
                self.pc = self.labels[instr.result] - 1  # -1 because pc will be incremented
            else:
                raise Exception(f"Runtime Error: Label {instr.result} not found")
        
        elif instr.op == 'if_false':
            condition = self.get_value(instr.arg1)
            if not condition or condition == 0:
                if instr.result in self.labels:
                    self.pc = self.labels[instr.result] - 1
                else:
                    raise Exception(f"Runtime Error: Label {instr.result} not found")
        
        elif instr.op == 'if_true':
            condition = self.get_value(instr.arg1)
            if condition and condition != 0:
                if instr.result in self.labels:
                    self.pc = self.labels[instr.result] - 1
                else:
                    raise Exception(f"Runtime Error: Label {instr.result} not found")
        
        elif instr.op == 'print':
            value = self.get_value(instr.arg1)
            self.output.append(str(value))
            print(value)
        
        elif instr.op == 'combine':
            items = ', '.join(instr.arg1)
            msg = f"Combining: {items}"
            self.output.append(msg)
            print(msg)
        
        elif instr.op == 'equip':
            target = instr.arg1
            stat_value = self.get_value(instr.arg2)
            msg = f"Equipping {target} to {stat_value}"
            self.output.append(msg)
            print(msg)
        
        elif instr.op == 'rest':
            duration = self.get_value(instr.arg1)
            msg = f"Resting for {duration}"
            self.output.append(msg)
            print(msg)
        
        elif instr.op == 'narrate':
            msg = instr.arg1
            self.output.append(msg)
            print(msg)
        
        elif instr.op == 'show':
            # Show variable name and value
            var_name = instr.arg1
            if var_name in self.variables:
                value = self.variables[var_name]
                # Resolve any temp variable references in the value
                if isinstance(value, str):
                    parts = value.split()
                    if len(parts) >= 2:
                        # Check if first part is a temp variable
                        if parts[0].startswith('t') and parts[0][1:].isdigit():
                            if parts[0] in self.variables:
                                resolved_val = self.variables[parts[0]]
                                value = f"{resolved_val} {' '.join(parts[1:])}"
                
                # Clean up floating point precision errors
                if isinstance(value, str):
                    parts = value.split()
                    if len(parts) >= 1:
                        try:
                            num = float(parts[0])
                            # Round to 1 decimal place if close to it
                            if abs(num - round(num, 1)) < 0.0001:
                                num = round(num, 1)
                            value = f"{num} {' '.join(parts[1:])}" if len(parts) > 1 else num
                        except ValueError:
                            pass
                elif isinstance(value, float):
                    if abs(value - round(value, 1)) < 0.0001:
                        value = round(value, 1)
                
                msg = f"{var_name}: {value}"
                self.output.append(msg)
                print(msg)
            else:
                msg = f"{var_name}: (not set)"
                self.output.append(msg)
                print(msg)
        
        elif instr.op == 'power_up':
            msg = f"Powering up {instr.arg1} by {instr.arg2}"
            self.output.append(msg)
            print(msg)
            # Update variable value
            if instr.arg1 in self.variables:
                current_val = self.variables[instr.arg1]
                # Extract numeric value if it's a string with units
                if isinstance(current_val, str):
                    parts = current_val.split()
                    if len(parts) >= 1:
                        try:
                            num_val = float(parts[0])
                            factor = float(instr.arg2)
                            new_val = num_val * factor
                            # Keep the unit if present
                            if len(parts) > 1:
                                self.variables[instr.arg1] = f"{new_val} {parts[1]}"
                            else:
                                self.variables[instr.arg1] = new_val
                        except ValueError:
                            pass
                else:
                    factor = float(instr.arg2)
                    self.variables[instr.arg1] = current_val * factor
        
        elif instr.op == 'acquire':
            msg = f"Acquiring {instr.arg1} to {instr.arg2}"
            self.output.append(msg)
            print(msg)
        
        elif instr.op == 'input':
            # Prompt user for input
            try:
                value = input(f"Enter value for {instr.result}: ")
                # Try to convert to number
                try:
                    if '.' in value:
                        self.variables[instr.result] = float(value)
                    else:
                        self.variables[instr.result] = int(value)
                except ValueError:
                    self.variables[instr.result] = value
            except EOFError:
                # For non-interactive mode, use default value
                self.variables[instr.result] = 4  # Default quest value
    
    def execute_quest(self, quest_name, args, instructions):
        """Execute a quest with given arguments"""
        # Save current state
        saved_pc = self.pc
        saved_vars = self.variables.copy()
        
        # Find quest declaration to get parameter names
        # We need to parse the quest to find parameter names
        # For now, we'll use a simple approach: pass args as local variables
        # In a full implementation, we'd need to track parameter names
        
        # Find quest start
        quest_start = self.recipes[quest_name]
        self.pc = quest_start + 1  # Skip begin_quest instruction
        
        # Execute quest body with arguments available
        # Store arguments in variables (they'll be referenced by name in the quest)
        return_value = None
        while self.pc < len(instructions):
            instr = instructions[self.pc]
            
            if instr.op == 'end_quest' and instr.result == quest_name:
                break
            
            result = self.execute_instruction(instr, instructions)
            if result and isinstance(result, tuple) and result[0] == 'return':
                return_value = result[1]
                # Resolve variable reference in return value
                if isinstance(return_value, str) and return_value in self.variables:
                    return_value = self.variables[return_value]
                break
            
            self.pc += 1
        
        # Restore state
        self.pc = saved_pc
        # Keep only global variables, restore locals
        for key in list(self.variables.keys()):
            if key not in saved_vars:
                del self.variables[key]
        
        return return_value if return_value is not None else 0
    
    def get_value(self, operand):
        """Get value of operand (variable or constant)"""
        if operand is None:
            return None
        
        operand_str = str(operand)
        
        # Remove quotes from strings
        if operand_str.startswith('"') and operand_str.endswith('"'):
            return operand_str[1:-1]
        
        # Check if it's a number
        try:
            if '.' in operand_str:
                return float(operand_str)
            return int(operand_str)
        except ValueError:
            pass
        
        # Check if it's a variable
        if operand_str in self.variables:
            return self.variables[operand_str]
        
        # Return as string (for units, etc.)
        return operand_str
    
    def display_output(self):
        """Display program output"""
        print("\n" + "=" * 60)
        print("QUEST EXECUTION OUTPUT")
        print("=" * 60)
        for line in self.output:
            print(line)
        print("=" * 60)
