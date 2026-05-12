"""
Syntax Analyzer (Parser) for AdventureScript
Phase 2: Builds Abstract Syntax Tree from tokens
"""

from token_types import TokenType

UNIT_TOKENS = {
    TokenType.GOLD, TokenType.TREASURE, TokenType.COIN, TokenType.LOOT, TokenType.GEMS,
    TokenType.QTY, TokenType.QTY_UNIT, TokenType.COUNT, TokenType.HP, TokenType.MP,
    TokenType.TURNS_UNIT, TokenType.SECONDS, TokenType.HOURS
}

IDENTIFIER_LIKE_TOKENS = {TokenType.IDENTIFIER} | UNIT_TOKENS

class ASTNode:
    """Base class for AST nodes"""
    pass

class Program(ASTNode):
    def __init__(self, recipes, statements):
        self.recipes = recipes
        self.statements = statements
        
    def __repr__(self):
        from parser import print_ast
        print_ast(self)
        return ""

class Declaration(ASTNode):
    def __init__(self, var_type, name, value, line=0):
        self.var_type = var_type
        self.name = name
        self.value = value
        self.line = line

class Assignment(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class CombineOperation(ASTNode):
    def __init__(self, items):
        self.items = items

class EquipOperation(ASTNode):
    def __init__(self, target, stat_value):
        self.target = target
        self.stat_value = stat_value

class RestOperation(ASTNode):
    def __init__(self, duration):
        self.duration = duration

class NarrateOperation(ASTNode):
    def __init__(self, message):
        self.message = message

class ShowOperation(ASTNode):
    def __init__(self, variable):
        self.variable = variable

class PowerUpOperation(ASTNode):
    def __init__(self, item, factor):
        self.item = item
        self.factor = factor

class AcquireOperation(ASTNode):
    def __init__(self, item, target):
        self.item = item
        self.target = target

class DiscardOperation(ASTNode):
    def __init__(self, item):
        self.item = item

class LoopStatement(ASTNode):
    def __init__(self, count, body):
        self.count = count
        self.body = body

class IfStatement(ASTNode):
    def __init__(self, condition, then_body, else_body=None):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body

class BinaryOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Number(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Number({self.value})"
class String(ASTNode):
    def __init__(self, value):
        self.value = value

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"Identifier({self.name})"

class Value(ASTNode):
    def __init__(self, number, unit=None):
        self.number = number
        self.unit = unit
        
    def __repr__(self):
        return f"Value({self.number}, {self.unit})"

class InputStatement(ASTNode):
    def __init__(self, var_name, line=0):
        self.var_name = var_name
        self.line = line

class QuestDeclaration(ASTNode):
    def __init__(self, name, params, return_type, body, line=0):
        self.name = name
        self.params = params
        self.return_type = return_type
        self.body = body
        self.line = line

class QuestCall(ASTNode):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

class ReturnStatement(ASTNode):
    def __init__(self, value=None):
        self.value = value

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def error(self, msg):
        if self.current_token:
            raise Exception(f"Syntax Error at line {self.current_token.line}: {msg}")
        raise Exception(f"Syntax Error: {msg}")
    
    def advance(self):
        """Move to next token"""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None
    
    def expect(self, token_type):
        """Consume expected token type"""
        if not self.current_token or self.current_token.type != token_type:
            self.error(f"Expected {token_type}, got {self.current_token.type if self.current_token else 'EOF'}")
        token = self.current_token
        self.advance()
        return token

    def expect_identifier_like(self):
        """Consume identifier-like token.

        We allow unit-keyword tokens as names in declaration/assignment contexts,
        so programs can use practical identifiers like `gold`.
        """
        if not self.current_token or self.current_token.type not in IDENTIFIER_LIKE_TOKENS:
            self.error(
                f"Expected identifier, got {self.current_token.type if self.current_token else 'EOF'}"
            )
        token = self.current_token
        self.advance()
        return token
    
    def parse(self):
        """Parse entire program"""
        quests = []
        statements = []
        
        # Parse quest declarations first
        while self.current_token and self.current_token.type == TokenType.QUEST:
            quest = self.parse_quest_declaration()
            if quest:
                quests.append(quest)
        
        # Parse main statements
        while self.current_token and self.current_token.type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        
        return Program(quests, statements)
    
    def parse_statement(self):
        """Parse a single statement"""
        if not self.current_token or self.current_token.type == TokenType.EOF:
            return None
        
        # Return statement
        if self.current_token.type == TokenType.RETURN:
            return self.parse_return()
        
        # Input statement
        if self.current_token.type == TokenType.INPUT:
            return self.parse_input()
        
        # Declaration
        if self.current_token.type in [TokenType.ITEM, TokenType.STAT, 
                                       TokenType.QTY, TokenType.TEXT]:
            return self.parse_declaration()
        
        # Operations
        if self.current_token.type == TokenType.COMBINE:
            return self.parse_combine()
        if self.current_token.type == TokenType.EQUIP:
            return self.parse_equip()
        if self.current_token.type == TokenType.REST:
            return self.parse_rest()
        if self.current_token.type == TokenType.NARRATE:
            return self.parse_narrate()
        if self.current_token.type == TokenType.SHOW:
            return self.parse_show()
        if self.current_token.type == TokenType.POWER_UP:
            return self.parse_power_up()
        if self.current_token.type == TokenType.ACQUIRE:
            return self.parse_acquire()
        if self.current_token.type == TokenType.DISCARD:
            return self.parse_discard()
        
        # Control flow
        if self.current_token.type == TokenType.LOOP:
            return self.parse_loop()
        if self.current_token.type == TokenType.IF:
            return self.parse_if()
        
        # Assignment or quest call
        if self.current_token.type in IDENTIFIER_LIKE_TOKENS:
            # Look ahead to check if it's a quest call
            if self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].type == TokenType.LPAREN:
                return self.parse_quest_call_statement()
            return self.parse_assignment()
        
        self.error(f"Unexpected token: {self.current_token.type}")
    
    def parse_input(self):
        """Parse input statement"""
        line = self.current_token.line
        self.expect(TokenType.INPUT)
        var_name = self.expect_identifier_like().value
        self.expect(TokenType.SEMICOLON)
        return InputStatement(var_name, line)
    
    def parse_declaration(self):
        """Parse variable declaration"""
        line = self.current_token.line
        var_type = self.current_token.type
        self.advance()
        
        name = self.expect_identifier_like().value
        self.expect(TokenType.ASSIGN)
        value = self.parse_value()
        self.expect(TokenType.SEMICOLON)
        
        return Declaration(var_type, name, value, line)
    
    def parse_assignment(self):
        """Parse assignment statement"""
        name = self.expect_identifier_like().value
        self.expect(TokenType.ASSIGN)
        value = self.parse_value()
        self.expect(TokenType.SEMICOLON)
        
        return Assignment(name, value)
    
    def parse_value(self):
        """Parse a value (number with optional unit or expression)"""
        # Try to parse as expression first (handles arithmetic)
        expr = self.parse_expression()
        
        # Check if there's a unit after the expression
        if self.current_token and self.current_token.type in [
            TokenType.GOLD, TokenType.TREASURE, TokenType.COIN, TokenType.LOOT, TokenType.GEMS,
            TokenType.QTY, TokenType.QTY_UNIT, TokenType.COUNT, TokenType.HP, TokenType.MP,
            TokenType.TURNS_UNIT, TokenType.SECONDS, TokenType.HOURS
        ]:
            unit = self.current_token.type
            self.advance()
            # Wrap expression with unit
            return Value(expr, unit)
        
        return expr
    
    def parse_combine(self):
        """Parse combine operation"""
        self.expect(TokenType.COMBINE)
        items = [self.expect_identifier_like().value]
        
        while self.current_token and self.current_token.type == TokenType.WITH:
            self.advance()
            items.append(self.expect_identifier_like().value)
        
        self.expect(TokenType.SEMICOLON)
        return CombineOperation(items)
    
    def parse_equip(self):
        """Parse equip operation"""
        self.expect(TokenType.EQUIP)
        target = self.expect_identifier_like().value
        self.expect(TokenType.TO)
        stat_value = self.parse_value()
        self.expect(TokenType.SEMICOLON)
        
        return EquipOperation(target, stat_value)
    
    def parse_rest(self):
        """Parse rest operation"""
        self.expect(TokenType.REST)
        duration = self.parse_value()
        self.expect(TokenType.SEMICOLON)
        
        return RestOperation(duration)
    
    def parse_narrate(self):
        """Parse narrate operation"""
        self.expect(TokenType.NARRATE)
        message = self.expect(TokenType.STRING).value
        self.expect(TokenType.SEMICOLON)
        
        return NarrateOperation(message)
    
    def parse_show(self):
        """Parse show operation"""
        self.expect(TokenType.SHOW)
        variable = self.expect_identifier_like().value
        self.expect(TokenType.SEMICOLON)
        
        return ShowOperation(variable)
    
    def parse_power_up(self):
        """Parse power_up operation"""
        self.expect(TokenType.POWER_UP)
        item = self.expect_identifier_like().value
        self.expect(TokenType.BY)
        factor = self.expect(TokenType.NUMBER).value
        self.expect(TokenType.SEMICOLON)
        
        return PowerUpOperation(item, factor)
    
    def parse_acquire(self):
        """Parse acquire operation"""
        self.expect(TokenType.ACQUIRE)
        item = self.expect_identifier_like().value
        self.expect(TokenType.TO)
        target = self.expect_identifier_like().value
        self.expect(TokenType.SEMICOLON)
        
        return AcquireOperation(item, target)

    def parse_discard(self):
        """Parse discard operation"""
        self.expect(TokenType.DISCARD)
        item = self.expect_identifier_like().value
        self.expect(TokenType.SEMICOLON)
        return DiscardOperation(item)
    
    def parse_loop(self):
        """Parse loop statement"""
        self.expect(TokenType.LOOP)
        count = self.expect(TokenType.NUMBER).value
        self.expect(TokenType.ITERATIONS)
        self.expect(TokenType.LBRACE)
        
        body = []
        while self.current_token and self.current_token.type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        
        self.expect(TokenType.RBRACE)
        return LoopStatement(count, body)
    
    def parse_if(self):
        """Parse if statement"""
        self.expect(TokenType.IF)
        condition = self.parse_condition()
        self.expect(TokenType.THEN)

        # Support both block styles:
        # 1) if cond then { ... } else { ... }
        # 2) if cond then ... else ... end
        then_body = []
        then_braced = False
        if self.current_token and self.current_token.type == TokenType.LBRACE:
            then_braced = True
            self.advance()
            while self.current_token and self.current_token.type != TokenType.RBRACE:
                stmt = self.parse_statement()
                if stmt:
                    then_body.append(stmt)
            self.expect(TokenType.RBRACE)
        else:
            while self.current_token and self.current_token.type not in [TokenType.ELSE, TokenType.END]:
                stmt = self.parse_statement()
                if stmt:
                    then_body.append(stmt)

        else_body = None
        else_braced = False
        if self.current_token and self.current_token.type == TokenType.ELSE:
            self.advance()
            else_body = []

            if self.current_token and self.current_token.type == TokenType.LBRACE:
                else_braced = True
                self.advance()
                while self.current_token and self.current_token.type != TokenType.RBRACE:
                    stmt = self.parse_statement()
                    if stmt:
                        else_body.append(stmt)
                self.expect(TokenType.RBRACE)
            else:
                while self.current_token and self.current_token.type != TokenType.END:
                    stmt = self.parse_statement()
                    if stmt:
                        else_body.append(stmt)

        uses_end_terminator = (not then_braced) or (else_body is not None and not else_braced)
        if uses_end_terminator:
            self.expect(TokenType.END)
        
        return IfStatement(condition, then_body, else_body)
    
    def parse_condition(self):
        """Parse condition expression"""
        left = self.parse_expression()
        
        if self.current_token and self.current_token.type in [
            TokenType.EQ, TokenType.NEQ, TokenType.GT, TokenType.LT, TokenType.GTE, TokenType.LTE
        ]:
            op = self.current_token.type
            self.advance()
            right = self.parse_expression()
            return BinaryOp(left, op, right)
        
        return left
    
    def parse_expression(self):
        """Parse arithmetic expression"""
        left = self.parse_term()
        
        while self.current_token and self.current_token.type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.current_token.type
            self.advance()
            right = self.parse_term()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_term(self):
        """Parse term (multiplication/division)"""
        left = self.parse_factor()
        
        while self.current_token and self.current_token.type in [TokenType.MULTIPLY, TokenType.DIVIDE]:
            op = self.current_token.type
            self.advance()
            right = self.parse_factor()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_factor(self):
        """Parse factor (number, identifier, quest call, or parenthesized expression)"""
        if self.current_token.type == TokenType.NUMBER:
            value = self.current_token.value
            self.advance()

            # Support unit-bearing literals inside expressions, e.g. 50 hp + 50 hp
            if self.current_token and self.current_token.type in UNIT_TOKENS:
                unit = self.current_token.type
                self.advance()
                return Value(Number(value), unit)

            return Number(value)
        
        if self.current_token.type in IDENTIFIER_LIKE_TOKENS:
            # Check if it's a quest call
            if self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].type == TokenType.LPAREN:
                return self.parse_quest_call()
            name = self.current_token.value
            self.advance()
            return Identifier(name)
        
        if self.current_token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        self.error(f"Unexpected token in expression: {self.current_token.type}")
    
    def parse_quest_declaration(self):
        """Parse quest declaration"""
        line = self.current_token.line
        self.expect(TokenType.QUEST)
        name = self.expect_identifier_like().value
        self.expect(TokenType.LPAREN)
        
        # Parse parameters
        params = []
        if self.current_token.type != TokenType.RPAREN:
            while True:
                param_type = self.current_token.type
                if param_type not in [TokenType.ITEM, TokenType.STAT, 
                                     TokenType.QTY, TokenType.TEXT]:
                    self.error(f"Expected type in parameter, got {param_type}")
                self.advance()
                param_name = self.expect_identifier_like().value
                params.append({'type': param_type, 'name': param_name})
                
                if self.current_token.type != TokenType.COMMA:
                    break
                self.advance()
        
        self.expect(TokenType.RPAREN)
        
        # Optional return type
        return_type = None
        if self.current_token and self.current_token.type == TokenType.RETURNS:
            self.advance()
            return_type = self.current_token.type
            if return_type not in [TokenType.ITEM, TokenType.STAT, TokenType.QTY, TokenType.TEXT] and return_type not in UNIT_TOKENS:
                self.error(f"Expected type after 'returns', got {return_type}")
            self.advance()
        
        # Parse body
        self.expect(TokenType.LBRACE)
        body = []
        while self.current_token and self.current_token.type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        self.expect(TokenType.RBRACE)
        
        return QuestDeclaration(name, params, return_type, body, line)
    
    def parse_quest_call(self):
        """Parse quest call (as expression)"""
        name = self.expect_identifier_like().value
        self.expect(TokenType.LPAREN)
        
        # Parse arguments
        arguments = []
        if self.current_token.type != TokenType.RPAREN:
            while True:
                arguments.append(self.parse_expression())
                if self.current_token.type != TokenType.COMMA:
                    break
                self.advance()
        
        self.expect(TokenType.RPAREN)
        return QuestCall(name, arguments)
    
    def parse_quest_call_statement(self):
        """Parse quest call as statement"""
        call = self.parse_quest_call()
        self.expect(TokenType.SEMICOLON)
        return call
    
    def parse_return(self):
        """Parse return statement"""
        self.expect(TokenType.RETURN)
        
        value = None
        if self.current_token.type != TokenType.SEMICOLON:
            value = self.parse_expression()
        
        self.expect(TokenType.SEMICOLON)
        return ReturnStatement(value)

def print_ast(node, indent=0):
    """Pretty print AST as a tree"""

    prefix = "  " * indent

    if node is None:
        print(prefix + "None")
        return

    # Program
    if isinstance(node, Program):
        print(prefix + "Program")
        print(prefix + "  Recipes:")
        for r in node.recipes:
            print_ast(r, indent + 2)
        print(prefix + "  Statements:")
        for s in node.statements:
            print_ast(s, indent + 2)

    # Declarations
    elif isinstance(node, Declaration):
        print(prefix + f"Declaration({node.var_type}, {node.name}, {node.value})")

    elif isinstance(node, Assignment):
        print(prefix + f"Assignment({node.name})")
        print_ast(node.value, indent + 1)

    # Operations
    elif isinstance(node, CombineOperation):
        print(prefix + f"Combine({node.items})")

    elif isinstance(node, EquipOperation):
        print(prefix + f"Equip({node.target})")
        print_ast(node.stat_value, indent + 1)

    elif isinstance(node, RestOperation):
        print(prefix + "Rest")
        print_ast(node.duration, indent + 1)

    elif isinstance(node, NarrateOperation):
        print(prefix + f"Narrate(\"{node.message}\")")

    elif isinstance(node, ShowOperation):
        print(prefix + f"Show({node.variable})")

    elif isinstance(node, PowerUpOperation):
        print(prefix + f"PowerUp({node.item}, {node.factor})")

    elif isinstance(node, AcquireOperation):
        print(prefix + f"Acquire({node.item} -> {node.target})")

    elif isinstance(node, DiscardOperation):
        print(prefix + f"Discard({node.item})")

    # Control flow
    elif isinstance(node, LoopStatement):
        print(prefix + f"Loop({node.count})")
        for stmt in node.body:
            print_ast(stmt, indent + 1)

    elif isinstance(node, IfStatement):
        print(prefix + "If")
        print(prefix + " Condition:")
        print_ast(node.condition, indent + 2)
        print(prefix + " Then:")
        for stmt in node.then_body:
            print_ast(stmt, indent + 2)
        if node.else_body:
            print(prefix + " Else:")
            for stmt in node.else_body:
                print_ast(stmt, indent + 2)

    # Expressions
    elif isinstance(node, BinaryOp):
        print(prefix + f"BinaryOp({node.op})")
        print_ast(node.left, indent + 1)
        print_ast(node.right, indent + 1)

    elif isinstance(node, Number):
        print(prefix + f"Number({node.value})")

    elif isinstance(node, Identifier):
        print(prefix + f"Identifier({node.name})")

    elif isinstance(node, Value):
        print(prefix + f"Value({node.number}, {node.unit})")

    elif isinstance(node, String):
        print(prefix + f"String({node.value})")

    # Quests
    elif isinstance(node, QuestDeclaration):
        print(prefix + f"Quest({node.name})")
        print(prefix + " Params:")
        for p in node.params:
            print(prefix + f"  - {p['type']} {p['name']}")
        print(prefix + " Body:")
        for stmt in node.body:
            print_ast(stmt, indent + 2)

    elif isinstance(node, QuestCall):
        print(prefix + f"QuestCall({node.name})")
        for arg in node.arguments:
            print_ast(arg, indent + 1)

    elif isinstance(node, ReturnStatement):
        print(prefix + "Return")
        if node.value:
            print_ast(node.value, indent + 1)

    else:
        print(prefix + f"UnknownNode({type(node).__name__})")