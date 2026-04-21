"""
Code Optimizer for LootCode
Phase 5: Optimizes Three-Address Code
"""

class Optimizer:
    def __init__(self):
        self.optimizations_applied = []
        self.control_ops = {
            'label', 'goto', 'if_false', 'if_true', 'begin_quest', 'end_quest'
        }
        self.side_effect_ops = {
            'narrate', 'show', 'rest', 'combine', 'equip', 'acquire', 'power_up',
            'input', 'call', 'return', 'param', 'print'
        }
    
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
            # Skip control-flow operations and quest boundaries
            if instr.op in self.control_ops:
                optimized.append(instr)
                continue
            
            # Fold arithmetic/comparison operations with constant operands.
            if instr.op in ['add', 'sub', 'mul', 'div', 'eq', 'neq', 'gt', 'lt', 'gte', 'lte'] and self.is_constant(instr.arg1) and self.is_constant(instr.arg2):
                try:
                    result = self.evaluate_op(instr.op, instr.arg1, instr.arg2)
                    from intermediate_code import TACInstruction
                    optimized.append(TACInstruction('assign', result, None, instr.result))
                    self.optimizations_applied.append(f"Constant folding: {instr.arg1} {instr.op} {instr.arg2} = {result}")
                except Exception:
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
                    constants[instr.result] = self.normalize_constant(instr.arg1)
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
                ref1 = self.extract_var_reference(instr.arg1)
                ref2 = self.extract_var_reference(instr.arg2)
                if ref1:
                    used_vars.add(ref1)
                if ref2:
                    used_vars.add(ref2)
            elif instr.op == 'assign':
                # Check if the assigned value references a variable.
                ref = self.extract_var_reference(instr.arg1)
                if ref:
                    used_vars.add(ref)
                # Also check if result is used (mark as used for now)
                if not instr.result.startswith('t'):
                    used_vars.add(instr.result)
            elif instr.op in self.side_effect_ops.union({'if_false', 'if_true'}):
                ref = self.extract_var_reference(instr.arg1)
                if ref:
                    used_vars.add(ref)
            elif instr.op == 'param':
                ref = self.extract_var_reference(instr.arg1)
                if ref:
                    used_vars.add(ref)
        
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
        return self.parse_constant(value) is not None

    def parse_constant(self, value):
        """Parse numeric constant with optional unit. Returns (number, unit|None)."""
        if value is None:
            return None

        value_str = str(value).strip()

        try:
            return float(value_str), None
        except ValueError:
            pass

        parts = value_str.split()
        if len(parts) == 2:
            try:
                return float(parts[0]), parts[1]
            except ValueError:
                return None

        return None

    def normalize_constant(self, value):
        """Normalize constant string representation for stable TAC output."""
        parsed = self.parse_constant(value)
        if not parsed:
            return value

        number, unit = parsed
        if number.is_integer():
            number_repr = str(int(number))
        else:
            number_repr = str(number)

        return f"{number_repr} {unit}" if unit else number_repr

    def extract_var_reference(self, operand):
        """Extract variable name from operand when operand is not a literal constant."""
        if operand is None:
            return None

        if self.is_constant(operand):
            return None

        text = str(operand).strip()
        if ' ' in text:
            first = text.split()[0]
            if first and not self.is_constant(first):
                return first

        return text
    
    def evaluate_op(self, op, arg1, arg2):
        """Evaluate arithmetic/comparison operation with unit-aware safety."""
        parsed1 = self.parse_constant(arg1)
        parsed2 = self.parse_constant(arg2)
        if not parsed1 or not parsed2:
            raise Exception("Non-constant operand")

        val1, unit1 = parsed1
        val2, unit2 = parsed2
        
        if op == 'add':
            if unit1 and unit2 and unit1 != unit2:
                raise Exception("Unit mismatch in add")
            if unit1 != unit2 and (unit1 or unit2):
                raise Exception("Cannot add unit and non-unit")
            return self.normalize_constant(f"{val1 + val2} {unit1}" if unit1 else str(val1 + val2))
        elif op == 'sub':
            if unit1 and unit2 and unit1 != unit2:
                raise Exception("Unit mismatch in sub")
            if unit1 != unit2 and (unit1 or unit2):
                raise Exception("Cannot subtract unit and non-unit")
            return self.normalize_constant(f"{val1 - val2} {unit1}" if unit1 else str(val1 - val2))
        elif op == 'mul':
            if unit1 and unit2:
                raise Exception("Unsupported unit * unit")
            out_unit = unit1 or unit2
            return self.normalize_constant(f"{val1 * val2} {out_unit}" if out_unit else str(val1 * val2))
        elif op == 'div':
            if val2 == 0:
                raise Exception("Division by zero in constant folding")
            if unit2:
                raise Exception("Unsupported division by unit value")
            return self.normalize_constant(f"{val1 / val2} {unit1}" if unit1 else str(val1 / val2))

        if op in ['eq', 'neq', 'gt', 'lt', 'gte', 'lte']:
            return str(self.evaluate_comparison(op, f"{val1} {unit1}" if unit1 else str(val1), f"{val2} {unit2}" if unit2 else str(val2)))

        raise Exception(f"Unsupported op: {op}")
    
    def evaluate_comparison(self, op, arg1, arg2):
        """Evaluate comparison operation"""
        parsed1 = self.parse_constant(arg1)
        parsed2 = self.parse_constant(arg2)
        if not parsed1 or not parsed2:
            raise Exception("Non-constant comparison operand")

        val1, unit1 = parsed1
        val2, unit2 = parsed2

        # Mixed units are not comparable in ordered comparisons.
        if op in ['gt', 'lt', 'gte', 'lte'] and unit1 != unit2:
            raise Exception("Unit mismatch in ordered comparison")

        # Equality with different units is deterministically false/true for neq.
        if op == 'eq' and unit1 != unit2:
            return 0
        if op == 'neq' and unit1 != unit2:
            return 1
        
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
