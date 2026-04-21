"""
RecipeScript Grammar for CLR Analysis
Format: Non-Terminal → Production
Use | for alternatives on separate lines
"""

grammar = """
Program → RecipeList StmtList
Program → StmtList

RecipeList → RecipeDecl RecipeListP

RecipeListP → RecipeDecl RecipeListP
RecipeListP → ε

StmtList → Stmt StmtListP

StmtListP → Stmt StmtListP
StmtListP → ε

RecipeDecl → 'recipe' IDENTIFIER '(' ParamList ')' RecipeRet '{' StmtList '}'

RecipeRet → 'returns' Type
RecipeRet → ε

ParamList → Parameter ParamListP
ParamList → ε

ParamListP → ',' Parameter ParamListP
ParamListP → ε

Parameter → Type IDENTIFIER

Stmt → InputStmt ';'
Stmt → Declaration ';'
Stmt → Operation ';'
Stmt → ControlFlow
Stmt → ReturnStmt ';'

ReturnStmt → 'return' ReturnVal

ReturnVal → Expr
ReturnVal → ε

InputStmt → 'input' IDENTIFIER

Declaration → Type IDENTIFIER '=' Value

Type → 'ingredient'
Type → 'time'
Type → 'temp'
Type → 'quantity'
Type → 'text'

Value → Expr ValueTail
Value → STRING

ValueTail → Unit
ValueTail → ε

Unit → 'cups'
Unit → 'tbsp'
Unit → 'tsp'

Operation → 'mix' IngrList
Operation → 'heat' IDENTIFIER 'to' Value
Operation → 'wait' Value

IngrList → IDENTIFIER IngrListP

IngrListP → 'with' IDENTIFIER IngrListP
IngrListP → ε

ControlFlow → RepeatStmt
ControlFlow → WhenStmt

RepeatStmt → 'repeat' NUMBER 'times' '{' StmtList '}'

WhenStmt → 'when' Condition 'then' '{' StmtList '}' WhenTail

WhenTail → 'else' '{' StmtList '}'
WhenTail → ε

Condition → Expr CompOp Expr

CompOp → '=='
CompOp → '!='
CompOp → '>'
CompOp → '<'

Expr → Term ExprP

ExprP → '+' Term ExprP
ExprP → '-' Term ExprP
ExprP → ε

Term → Factor TermP

TermP → '*' Factor TermP
TermP → '/' Factor TermP
TermP → ε

Factor → NUMBER
Factor → IDENTIFIER FactorTail
Factor → '(' Expr ')'

FactorTail → ε
"""
