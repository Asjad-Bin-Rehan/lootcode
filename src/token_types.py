"""
Token types for AdventureScript language
"""

from enum import Enum, auto

class TokenType(Enum):
    # Data types
    ITEM = auto()
    STAT = auto()
    QTY = auto()
    TEXT = auto()
    
    # Operations
    COMBINE = auto()
    EQUIP = auto()
    REST = auto()
    NARRATE = auto()
    POWER_UP = auto()
    ACQUIRE = auto()
    DISCARD = auto()
    SHOW = auto()
    
    # Control flow
    LOOP = auto()
    FOR_EACH = auto()
    IF = auto()
    THEN = auto()
    ELSE = auto()
    ITERATIONS = auto()
    IN = auto()
    
    # Functions
    QUEST = auto()
    RETURN = auto()
    RETURNS = auto()
    
    # Input/Output
    INPUT = auto()
    
    # Prepositions
    TO = auto()
    WITH = auto()
    FOR = auto()
    AT = auto()
    FROM = auto()
    BY = auto()
    
    # Units - Currency
    GOLD = auto()
    TREASURE = auto()
    COIN = auto()
    LOOT = auto()
    GEMS = auto()
    
    # Units - Quantity
    QTY_UNIT = auto()
    COUNT = auto()
    
    # Units - Stats
    HP = auto()
    MP = auto()
    
    # Units - Time
    TURNS_UNIT = auto()
    SECONDS = auto()
    HOURS = auto()
    
    # Operators
    ASSIGN = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    EQ = auto()
    NEQ = auto()
    GT = auto()
    LT = auto()
    GTE = auto()
    LTE = auto()
    
    # Delimiters
    SEMICOLON = auto()
    COMMA = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    
    # Literals
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    
    # Special
    COMMENT = auto()
    EOF = auto()
    NEWLINE = auto()

class Token:
    def __init__(self, type, value, line=0, column=0):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.line}:{self.column})"
    
    def __str__(self):
        return self.__repr__()

# Keyword mapping
KEYWORDS = {
    'item': TokenType.ITEM,
    'stat': TokenType.STAT,
    'text': TokenType.TEXT,
    'combine': TokenType.COMBINE,
    'equip': TokenType.EQUIP,
    'rest': TokenType.REST,
    'narrate': TokenType.NARRATE,
    'power_up': TokenType.POWER_UP,
    'acquire': TokenType.ACQUIRE,
    'discard': TokenType.DISCARD,
    'show': TokenType.SHOW,
    'loop': TokenType.LOOP,
    'foreach': TokenType.FOR_EACH,
    'if': TokenType.IF,
    'then': TokenType.THEN,
    'else': TokenType.ELSE,
    'iterations': TokenType.ITERATIONS,
    'in': TokenType.IN,
    'quest': TokenType.QUEST,
    'return': TokenType.RETURN,
    'returns': TokenType.RETURNS,
    'input': TokenType.INPUT,
    'to': TokenType.TO,
    'with': TokenType.WITH,
    'for': TokenType.FOR,
    'at': TokenType.AT,
    'from': TokenType.FROM,
    'by': TokenType.BY,
    'gold': TokenType.GOLD,
    'treasure': TokenType.TREASURE,
    'coin': TokenType.COIN,
    'loot': TokenType.LOOT,
    'gems': TokenType.GEMS,
    'qty': TokenType.QTY_UNIT,
    'count': TokenType.COUNT,
    'hp': TokenType.HP,
    'mp': TokenType.MP,
    'turns': TokenType.TURNS_UNIT,
    'seconds': TokenType.SECONDS,
    'hours': TokenType.HOURS,
}
