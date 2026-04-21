"""
Semantic Analyzer for LootCode
Phase 3: Type checking and symbol table construction
Validates adventure game syntax and semantics
"""

from token_types import TokenType
from parser import *

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.scope_level = 0
        self.current_quest = None
    
    def declare(self, name, var_type, line=0, is_parameter=False, quest_name=None, unit=None):
        """Declare a new variable"""
        # For quest parameters and local variables, include quest name in qualified name
        if self.scope_level > 0 and quest_name:
            qualified_name = f"{name}_quest_{quest_name}"
        elif self.scope_level > 0:
            qualified_name = f"{name}_scope{self.scope_level}"
        else:
            qualified_name = name
        
        # Check if variable already exists with same qualified name
        if qualified_name in self.symbols:
            raise Exception(f"Semantic Error at line {line}: Variable '{name}' already declared in current scope")
        
        # Store with qualified name to allow same name in different scopes
        self.symbols[qualified_name] = {
            'type': var_type,
            'scope': self.scope_level,
            'line': line,
            'original_name': name,
            'is_parameter': is_parameter,
            'quest_name': quest_name,
            'unit': unit,
        }
    
    def lookup(self, name, line=0):
        """Look up a variable - search from current scope outward"""
        # If in a quest scope, try quest-qualified name first
        if self.scope_level > 0 and self.current_quest:
            qualified_name = f"{name}_quest_{self.current_quest}"
            if qualified_name in self.symbols:
                return self.symbols[qualified_name]
        
        # Try current scope
        qualified_name = f"{name}_scope{self.scope_level}" if self.scope_level > 0 else name
        if qualified_name in self.symbols:
            return self.symbols[qualified_name]
        
        # Try outer scopes (search from current scope down to 0)
        for scope in range(self.scope_level - 1, -1, -1):
            qualified_name = f"{name}_scope{scope}" if scope > 0 else name
            if qualified_name in self.symbols:
                return self.symbols[qualified_name]
        
        # Not found in any scope
        raise Exception(f"Semantic Error at line {line}: Variable '{name}' not declared")

    
    def enter_scope(self):
        """Enter a new scope"""
        self.scope_level += 1
    
    def exit_scope(self):
        """Exit current scope"""
        # DON'T remove variables - keep them to show scope information
        # Just decrement scope level
        self.scope_level -= 1
    
    def display(self):
        """Display symbol table with proper formatting"""
        print("\n=== Symbol Table ===")
        print(f"{'Name':<20} {'Type':<15} {'Scope':<8} {'Line':<10} {'Context':<20}")
        print("-" * 75)
        
        # Sort by scope first, then by line
        sorted_symbols = sorted(self.symbols.items(), key=lambda x: (x[1]['scope'], x[1]['line']))
        
        for name, info in sorted_symbols:
            type_str = str(info['type']).split('.')[-1] if hasattr(info['type'], 'name') else str(info['type'])
            display_name = info.get('original_name', name)
            
            # Determine context
            if info['scope'] == 0:
                if type_str == 'QUEST':
                    context = "(function)"
                else:
                    context = "(global)"
            else:
                # For scope 1, check if it's marked as a parameter
                if info.get('is_parameter', False):
                    context = "(parameter)"
                else:
                    context = "(local)"
            
            print(f"{display_name:<20} {type_str:<15} {info['scope']:<8} {info['line']:<10} {context:<20}")

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.quest_table = {}  # Store quest definitions
        self.current_quest = None  # Track current quest being analyzed
        self.errors = []
        # Share current_quest with symbol table for lookups
        self.symbol_table.current_quest = None
    
    def error(self, msg):
        """Record semantic error"""
        self.errors.append(msg)
        raise Exception(f"Semantic Error: {msg}")
    
    def analyze(self, ast):
        """Analyze the AST"""
        self.visit(ast)
        return self.symbol_table
    
    def visit(self, node):
        """Visit AST node"""
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        """Default visitor"""
        pass
    
    def visit_Program(self, node):
        """Visit program node"""
        # First pass: Register all quests (just names, not bodies)
        # Note: Parser uses .recipes attribute but stores QuestDeclaration objects
        for quest in node.recipes:
            self.register_quest(quest)
        
        # Second pass: Analyze main statements (declare global variables)
        for stmt in node.statements:
            self.visit(stmt)
        
        # Third pass: Analyze quest bodies (now globals are declared)
        for quest in node.recipes:
            self.visit(quest)
    
    def visit_InputStatement(self, node):
        """Visit input statement"""
        # Declare input variable as quantity type
        line = getattr(node, 'line', 0)
        self.symbol_table.declare(node.var_name, TokenType.QTY, line)
    
    def visit_Declaration(self, node):
        """Visit declaration node"""
        unit = self._extract_declared_unit(node.value)
        # Declare variable in symbol table
        line = getattr(node, 'line', 0)
        self.symbol_table.declare(node.name, node.var_type, line, unit=unit)
        
        # Check value type compatibility
        self.visit(node.value)
    
    def visit_Assignment(self, node):
        """Visit assignment node"""
        # Check if variable exists
        self.symbol_table.lookup(node.name)
        self.visit(node.value)
    
    def visit_CombineOperation(self, node):
        """Visit combine operation (adventure theme: mixing items)"""
        # Check all items are declared as ITEM type
        for item in node.items:
            var_info = self.symbol_table.lookup(item)
            if var_info['type'] != TokenType.ITEM:
                self.error(f"Cannot combine non-item: {item}")
    
    def visit_EquipOperation(self, node):
        """Visit equip operation (adventure theme: equipping stats)"""
        # Check target exists
        self.symbol_table.lookup(node.target)
        self.visit(node.stat_value)
        
        # Validate stat range (0-999 for hp/mp)
        if isinstance(node.stat_value, Value):
            # Check if number is a simple value (not an expression)
            if isinstance(node.stat_value.number, str):
                try:
                    stat_val = float(node.stat_value.number)
                    if node.stat_value.unit in (TokenType.HP, TokenType.MP):
                        if stat_val < 0 or stat_val > 999:
                            self.error(f"Stat out of range: {stat_val} (0-999 for hp/mp)")
                except ValueError:
                    pass  # Skip validation for non-numeric values
    
    def visit_RestOperation(self, node):
        """Visit rest operation (adventure theme: waiting)"""
        self.visit(node.duration)
        
        # Validate positive duration (only for constant values)
        if isinstance(node.duration, Value):
            if isinstance(node.duration.number, str):
                try:
                    duration_val = float(node.duration.number)
                    if duration_val < 0:
                        self.error(f"Rest duration must be positive: {duration_val}")
                except ValueError:
                    pass  # Skip validation for non-numeric values
    
    def visit_NarrateOperation(self, node):
        """Visit narrate operation (adventure theme: serving/output)"""
        pass  # No semantic checks needed
    
    def visit_ShowOperation(self, node):
        """Visit show operation (adventure theme: display)"""
        # Check variable exists
        self.symbol_table.lookup(node.variable)
    
    def visit_PowerUpOperation(self, node):
        """Visit power up operation (adventure theme: scale)"""
        # Check item exists
        var_info = self.symbol_table.lookup(node.item)
        if var_info['type'] != TokenType.ITEM:
            self.error(f"Cannot power up non-item: {node.item}")
        
        # Validate positive factor
        factor_val = float(node.factor)
        if factor_val <= 0:
            self.error(f"Power up factor must be positive: {factor_val}")
    
    def visit_AcquireOperation(self, node):
        """Visit acquire operation (adventure theme: add/combine items)"""
        # Check both items exist
        self.symbol_table.lookup(node.item)
        self.symbol_table.lookup(node.target)

    def visit_DiscardOperation(self, node):
        """Visit discard operation"""
        var_info = self.symbol_table.lookup(node.item)
        if var_info['type'] != TokenType.ITEM:
            self.error(f"Cannot discard non-item: {node.item}")
    
    def visit_LoopStatement(self, node):
        """Visit loop statement (adventure theme: repeat)"""
        # Validate positive count
        count_val = int(node.count)
        if count_val <= 0:
            self.error(f"Loop count must be positive: {count_val}")
        
        # Visit body statements
        self.symbol_table.enter_scope()
        for stmt in node.body:
            self.visit(stmt)
        self.symbol_table.exit_scope()
    
    def visit_IfStatement(self, node):
        """Visit if statement (adventure theme: when)"""
        # Visit condition
        self.visit(node.condition)
        
        # Visit then body (create new scope)
        self.symbol_table.enter_scope()
        for stmt in node.then_body:
            self.visit(stmt)
        # Exit scope (but variables are kept in symbol table)
        self.symbol_table.exit_scope()
        
        # Visit else body if exists (create new scope)
        if node.else_body:
            self.symbol_table.enter_scope()
            for stmt in node.else_body:
                self.visit(stmt)
            # Exit scope (but variables are kept in symbol table)
            self.symbol_table.exit_scope()
    
    def visit_BinaryOp(self, node):
        """Visit binary operation"""
        self.visit(node.left)
        self.visit(node.right)
    
    def visit_Number(self, node):
        """Visit number node"""
        pass
    
    def visit_String(self, node):
        """Visit string node"""
        pass
    
    def visit_Identifier(self, node):
        """Visit identifier node"""
        self.symbol_table.lookup(node.name)
    
    def visit_Value(self, node):
        """Visit value node"""
        pass
    
    def register_quest(self, quest):
        """Register quest in quest table"""
        if quest.name in self.quest_table:
            self.error(f"Quest '{quest.name}' already defined")
        
        # Add quest to symbol table as a function
        line = getattr(quest, 'line', 0)
        self.symbol_table.declare(quest.name, 'QUEST', line)
        
        self.quest_table[quest.name] = {
            'params': quest.params,
            'return_type': quest.return_type,
            'body': quest.body,
            'line': line
        }
    
    def visit_QuestDeclaration(self, node):
        """Visit quest declaration (adventure theme: recipe)"""
        self.current_quest = node.name
        self.symbol_table.current_quest = node.name
        
        # Create new scope for quest
        self.symbol_table.enter_scope()
        
        # Add parameters to symbol table with quest name
        line = getattr(node, 'line', 0)
        for param in node.params:
            self.symbol_table.declare(param['name'], param['type'], line, is_parameter=True, quest_name=node.name)
        
        # Analyze quest body
        has_return = False
        for stmt in node.body:
            self.visit(stmt)
            if isinstance(stmt, ReturnStatement):
                has_return = True
        
        # Check if quest with return type has return statement
        if node.return_type and not has_return:
            self.error(f"Quest '{node.name}' must return a value")
        
        # Exit quest scope (but variables are kept in symbol table)
        self.symbol_table.exit_scope()
        self.current_quest = None
        self.symbol_table.current_quest = None
    
    def visit_QuestCall(self, node):
        """Visit quest call (adventure theme: recipe call)"""
        # Check if quest exists
        if node.name not in self.quest_table:
            self.error(f"Undefined quest '{node.name}'")
            return
        
        quest = self.quest_table[node.name]
        
        # Check argument count
        expected = len(quest['params'])
        actual = len(node.arguments)
        
        if expected != actual:
            self.error(
                f"Quest '{node.name}' expects {expected} arguments, got {actual}"
            )
            return
        
        # Visit arguments
        for arg in node.arguments:
            self.visit(arg)
    
    def visit_ReturnStatement(self, node):
        """Visit return statement"""
        if not self.current_quest:
            self.error("Return statement outside quest")
        
        expected = self.quest_table.get(self.current_quest, {}).get('return_type')

        if node.value:
            self.visit(node.value)
            if expected:
                actual_type, actual_unit = self.infer_expr_type(node.value)
                if not self._is_return_compatible(expected, actual_type, actual_unit):
                    self.error(
                        f"Quest '{self.current_quest}' return type mismatch: expected {expected}, got {actual_type}{f' ({actual_unit})' if actual_unit else ''}"
                    )
        elif expected:
            self.error(f"Quest '{self.current_quest}' must return a value")

    def _extract_declared_unit(self, value_node):
        """Extract declared unit from a declaration value when available."""
        if isinstance(value_node, Value):
            return value_node.unit
        return None

    def infer_expr_type(self, node):
        """Infer (base_type, unit) for an expression node."""
        if isinstance(node, Value):
            inner_type, _ = self.infer_expr_type(node.number)
            return inner_type, node.unit

        if isinstance(node, Number):
            return 'NUMBER', None

        if isinstance(node, String):
            return TokenType.TEXT, None

        if isinstance(node, Identifier):
            var_info = self.symbol_table.lookup(node.name)
            return var_info['type'], var_info.get('unit')

        if isinstance(node, QuestCall):
            quest = self.quest_table.get(node.name)
            if not quest:
                return 'UNKNOWN', None
            return quest.get('return_type') or 'UNKNOWN', None

        if isinstance(node, BinaryOp):
            left_type, left_unit = self.infer_expr_type(node.left)
            right_type, right_unit = self.infer_expr_type(node.right)

            if node.op in [TokenType.EQ, TokenType.NEQ, TokenType.GT, TokenType.LT, TokenType.GTE, TokenType.LTE]:
                return 'BOOL', None

            # Arithmetic operations
            if left_type == right_type:
                return left_type, left_unit or right_unit
            return 'NUMBER', left_unit or right_unit

        return 'UNKNOWN', None

    def _is_return_compatible(self, expected, actual_type, actual_unit):
        """Validate quest return compatibility for both type and unit-style declarations."""
        unit_like = {
            TokenType.QTY, TokenType.QTY_UNIT, TokenType.COUNT,
            TokenType.HP, TokenType.MP,
            TokenType.TURNS_UNIT, TokenType.SECONDS, TokenType.HOURS,
            TokenType.GOLD, TokenType.TREASURE, TokenType.COIN, TokenType.LOOT, TokenType.GEMS,
        }

        if expected in [TokenType.ITEM, TokenType.STAT, TokenType.QTY, TokenType.TEXT]:
            if actual_type == expected:
                return True
            if expected == TokenType.STAT and actual_unit in [TokenType.HP, TokenType.MP]:
                return True
            if expected == TokenType.QTY and (actual_unit in unit_like or actual_type == 'NUMBER'):
                return True
            return False

        if expected in unit_like:
            if actual_unit is not None:
                return actual_unit == expected

            # Allow typed variables whose unit is implicit by domain.
            if actual_type == TokenType.STAT and expected in [TokenType.HP, TokenType.MP]:
                return True
            if actual_type in [TokenType.ITEM, TokenType.QTY, 'NUMBER'] and expected in unit_like:
                return True
            return False

        return actual_type == expected
