"""
Lexical Analyzer (Lexer) for AdventureScript
Phase 1: Converts source code into tokens
"""

from token_types import Token, TokenType, KEYWORDS

class Lexer:
    def __init__(self, source_code):
        self.source = source_code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.source[0] if source_code else None
    
    def error(self, msg):
        raise Exception(f"Lexical Error at line {self.line}, column {self.column}: {msg}")
    
    def advance(self):
        """Move to next character"""
        if self.current_char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        
        self.pos += 1
        if self.pos >= len(self.source):
            self.current_char = None
        else:
            self.current_char = self.source[self.pos]
    
    def peek(self, offset=1):
        """Look ahead without advancing"""
        peek_pos = self.pos + offset
        if peek_pos >= len(self.source):
            return None
        return self.source[peek_pos]
    
    def skip_whitespace(self):
        """Skip whitespace characters"""
        while self.current_char and self.current_char in ' \t\r\n':
            self.advance()
    
    def skip_comment(self):
        """Skip single-line comments starting with #"""
        if self.current_char == '#':
            while self.current_char and self.current_char != '\n':
                self.advance()
            if self.current_char == '\n':
                self.advance()
    
    def read_number(self):
        """Read numeric literal (integer or float)"""
        num_str = ''
        start_col = self.column
        
        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            num_str += self.current_char
            self.advance()
        
        # Validate number format
        if num_str.count('.') > 1:
            self.error(f"Invalid number format: {num_str}")
        
        return Token(TokenType.NUMBER, num_str, self.line, start_col)
    
    def read_string(self):
        """Read string literal"""
        start_col = self.column
        self.advance()  # Skip opening quote
        
        string_val = ''
        while self.current_char and self.current_char != '"':
            if self.current_char == '\n':
                self.error("Unterminated string literal")
            string_val += self.current_char
            self.advance()
        
        if not self.current_char:
            self.error("Unterminated string literal")
        
        self.advance()  # Skip closing quote
        return Token(TokenType.STRING, string_val, self.line, start_col)
    
    def read_identifier(self):
        """Read identifier or keyword"""
        start_col = self.column
        id_str = ''
        
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            id_str += self.current_char
            self.advance()
        
        # Check if it's a keyword
        token_type = KEYWORDS.get(id_str, TokenType.IDENTIFIER)
        return Token(token_type, id_str, self.line, start_col)
    
    def get_next_token(self):
        """Get next token from source"""
        while self.current_char:
            # Skip whitespace
            if self.current_char in ' \t\r\n':
                self.skip_whitespace()
                continue
            
            # Skip comments
            if self.current_char == '#':
                self.skip_comment()
                continue
            
            # Numbers
            if self.current_char.isdigit():
                return self.read_number()
            
            # Strings
            if self.current_char == '"':
                return self.read_string()
            
            # Identifiers and keywords
            if self.current_char.isalpha() or self.current_char == '_':
                return self.read_identifier()
            
            # Operators and delimiters
            start_col = self.column
            
            # Two-character operators
            if self.current_char == '=' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.EQ, '==', self.line, start_col)
            
            if self.current_char == '!' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.NEQ, '!=', self.line, start_col)
            
            if self.current_char == '>' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.GTE, '>=', self.line, start_col)
            
            if self.current_char == '<' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.LTE, '<=', self.line, start_col)
            
            # Single-character tokens
            char = self.current_char
            self.advance()
            
            if char == '=':
                return Token(TokenType.ASSIGN, '=', self.line, start_col)
            elif char == '+':
                return Token(TokenType.PLUS, '+', self.line, start_col)
            elif char == '-':
                return Token(TokenType.MINUS, '-', self.line, start_col)
            elif char == '*':
                return Token(TokenType.MULTIPLY, '*', self.line, start_col)
            elif char == '/':
                return Token(TokenType.DIVIDE, '/', self.line, start_col)
            elif char == '>':
                return Token(TokenType.GT, '>', self.line, start_col)
            elif char == '<':
                return Token(TokenType.LT, '<', self.line, start_col)
            elif char == ';':
                return Token(TokenType.SEMICOLON, ';', self.line, start_col)
            elif char == ',':
                return Token(TokenType.COMMA, ',', self.line, start_col)
            elif char == '(':
                return Token(TokenType.LPAREN, '(', self.line, start_col)
            elif char == ')':
                return Token(TokenType.RPAREN, ')', self.line, start_col)
            elif char == '{':
                return Token(TokenType.LBRACE, '{', self.line, start_col)
            elif char == '}':
                return Token(TokenType.RBRACE, '}', self.line, start_col)
            else:
                self.error(f"Unexpected character: '{char}'")
        
        return Token(TokenType.EOF, None, self.line, self.column)
    
    def tokenize(self):
        """Tokenize entire source code"""
        tokens = []
        while True:
            token = self.get_next_token()
            if token.type != TokenType.COMMENT:
                tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens

def test_lexer():
    """Test the lexer with sample code"""
    code = '''
    item health_potion = 2 qty;
    stat player_hp = 100 hp;
    equip player_hp to 100 hp;
    rest 15 turns;
    '''
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    print("Tokens:")
    for token in tokens:
        print(f"  {token}")

if __name__ == "__main__":
    test_lexer()
