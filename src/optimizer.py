"""
Code Optimizer for LootCode
Phase 5: Optimizes Three-Address Code
"""

class Optimizer:
    def __init__(self):
        self.optimizations_applied = []
    
    def optimize(self, instructions):
        """Apply optimizations to TAC"""
        optimized = instructions.copy()
        
        # Apply constant folding
        optimized = self.constant_folding(optimized)
        
        # Apply constant propagation
        optimized = self.constant_propagation(optimized)
        
        # Apply dead code elimination
        optimized = self.dead_code_elimination(optimized)
        
        return optimized
    
    def constant_folding(self, instructions):
        """Fold constant expressions at compile time"""
        optimized = []
        
        for instr in instructions:
            # Skip recipe boundaries and labels
            if instr.op in ['begin_recipe', 'end_recipe', 'label', 'goto', 'if_false', 'if_true']:
                optimized.append(instr)
                continue
            
            # Fold arithmetic operations with constant operands
            if instr.op in ['add', 'sub', 'mul', 'div'] and self.is_constant(instr.arg1) and self.is_constant(instr.arg2):
                try:
                    result = self.evaluate_op(instr.op, instr.arg1, instr.arg2)
                    # Replace with direct assignment
                    from intermediate_code import TACInstruction
                    optimized.append(TACInstruction('assign', str(result), None, instr.result))
                    self.optimizations_applied.append(f"Constant folding: {instr.arg1} {instr.op} {instr.arg2} = {result}")
                except:
                    optimized.append(instr)
            else:
                optimized.append(instr)
        
        return optimized
    
    def constant_propagation(self, instructions):
        """Propagate constant values through the code"""
        # First pass: find variables that are assigned multiple times (loop variables)
        assignment_count = {}
        for instr in instructions:
            if instr.op == 'assign':
                assignment_count[instr.result] = assignment_count.get(instr.result, 0) + 1
        
        constants = {}  # Track known constant values
        optimized = []
        
        for instr in instructions:
            # Track constant assignments (but not for variables assigned multiple times)
            if instr.op == 'assign' and self.is_constant(instr.arg1):
                # Only propagate if variable is assigned once (not a loop variable)
                if assignment_count.get(instr.result, 0) == 1:
                    constants[instr.result] = instr.arg1
                optimized.append(instr)
            # Replace variable references with constants where possible
            elif instr.op in ['add', 'sub', 'mul', 'div', 'eq', 'neq', 'gt', 'lt', 'gte', 'lte']:
                arg1 = constants.get(instr.arg1, instr.arg1)
                arg2 = constants.get(instr.arg2, instr.arg2)
                if arg1 != instr.arg1 or arg2 != instr.arg2:
                    from intermediate_code import TACInstruction
                    optimized.append(TACInstruction(instr.op, arg1, arg2, instr.result))
                    if arg1 != instr.arg1:
                        self.optimizations_applied.append(f"Constant propagation: {instr.arg1} -> {arg1}")
                    if arg2 != instr.arg2:
                        self.optimizations_applied.append(f"Constant propagation: {instr.arg2} -> {arg2}")
                else:
                    optimized.append(instr)
            else:
                optimized.append(instr)
        
        return optimized
    
    def dead_code_elimination(self, instructions):
        """Remove unused variable assignments"""
        # Build use-def chains
        used_vars = set()
        
        # First pass: find all used variables (including in assign operations)
        for instr in instructions:
            if instr.op in ['add', 'sub', 'mul', 'div', 'eq', 'neq', 'gt', 'lt', 'gte', 'lte']:
                if instr.arg1 and not self.is_constant(instr.arg1):
                    used_vars.add(instr.arg1)
                if instr.arg2 and not self.is_constant(instr.arg2):
                    used_vars.add(instr.arg2)
            elif instr.op == 'assign':
                # Check if the assigned value references a variable
                if instr.arg1 and not self.is_constant(instr.arg1):
                    used_vars.add(instr.arg1)
                # Also check if result is used (mark as used for now)
                if not instr.result.startswith('t'):
                    used_vars.add(instr.result)
            elif instr.op in ['display', 'return', 'if_false', 'if_true', 'wait', 'scale']:
                if instr.arg1 and not self.is_constant(instr.arg1):
                    used_vars.add(instr.arg1)
            elif instr.op == 'param':
                if instr.arg1 and not self.is_constant(instr.arg1):
                    used_vars.add(instr.arg1)
        
        # Second pass: remove assignments to unused temp variables
        optimized = []
        for instr in instructions:
            # Only remove temp variable assignments that are never used AND not assigned from another variable
            if (instr.op == 'assign' and 
                instr.result.startswith('t') and 
                instr.result not in used_vars and
                self.is_constant(instr.arg1)):
                self.optimizations_applied.append(f"Dead code elimination: Removed unused {instr.result}")
            else:
                optimized.append(instr)
        
        return optimized
    
    def is_constant(self, value):
        """Check if value is a constant"""
        if value is None:
            return False
        value_str = str(value)
        # Check if it's a number (int or float)
        try:
            float(value_str)
            return True
        except ValueError:
            return False
    
    def evaluate_op(self, op, arg1, arg2):
        """Evaluate arithmetic operation"""
        val1 = float(arg1)
        val2 = float(arg2)
        
        if op == 'add':
            return val1 + val2
        elif op == 'sub':
            return val1 - val2
        elif op == 'mul':
            return val1 * val2
        elif op == 'div':
            if val2 == 0:
                raise Exception("Division by zero in constant folding")
            return val1 / val2
        
        return 0
    
    def evaluate_comparison(self, op, arg1, arg2):
        """Evaluate comparison operation"""
        val1 = float(arg1)
        val2 = float(arg2)
        
        if op == 'eq':
            return 1 if val1 == val2 else 0
        elif op == 'neq':
            return 1 if val1 != val2 else 0
        elif op == 'gt':
            return 1 if val1 > val2 else 0
        elif op == 'lt':
            return 1 if val1 < val2 else 0
        elif op == 'gte':
            return 1 if val1 >= val2 else 0
        elif op == 'lte':
            return 1 if val1 <= val2 else 0
        
        return 0
    
    def display_optimizations(self):
        """Display applied optimizations"""
        if self.optimizations_applied:
            print("\n=== Optimizations Applied ===")
            for opt in self.optimizations_applied:
                print(f"  - {opt}")
        else:
            print("\n=== No Optimizations Applied ===")
