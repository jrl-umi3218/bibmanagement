import ply.lex as lex
import ply.yacc as yacc

# List of token names.
tokens = ('CONSTANT',
          'PLACEHOLDER',
          'LBRACE',
          'RBRACE',
          'FORMAT',
          'QMARK',
          'BAR'
         )

# States of the lexer
states = (
    ('escape', 'exclusive'),
    ('format', 'exclusive'),
)

# Regular expression rules for simple tokens
t_CONSTANT    = r'[^%{}?|\[\]\\]+'
t_PLACEHOLDER = r'(%[A-Za-z_]\w*(\.[A-Za-z_]\w*(\(\))?)?%)'
t_LBRACE      = r'\{'
t_RBRACE      = r'\}'
t_QMARK       = r'\?'
t_BAR         = r'\|'

# If we encounter a backlash, we pass in escape mode
def t_begin_escape(t):
    r'\\'
    t.lexer.emit = True
    t.lexer.push_state('escape')

# In escape mode, the next character is always considered as a constant
# As soon as we parse it, we go back to initial mode
def t_escape_CONSTANT(t):
    r'.'
    t.lexer.pop_state()
    if t.lexer.emit:
        return t

# If we encounter a [, we go to format mode
def t_begin_formatState(t):
    r'\['
    t.lexer.format_start = t.lexer.lexpos  #start position of the format string
    t.lexer.level = 1
    t.lexer.emit = False
    t.lexer.push_state('format')

def t_format_LBRACKET(t):
    r'\['
    t.lexer.level += 1

def t_format_escape(t):
    r'\\'
    t.lexer.push_state('escape')

def t_format_RBRACKET(t):
    r'\]'
    t.lexer.level -= 1

    if t.lexer.level == 0:
        t.value = t.lexer.lexdata[t.lexer.format_start:t.lexer.lexpos-1]
        t.type = 'FORMAT'
        t.lexer.pop_state()
        return t

def t_format_other(t):
    r'[^\[\]\\]+'
    pass

def t_error(t):
    pass

def t_escape_error(t):
    pass

def t_format_error(t):
    pass


# expression   : expression expression
#              | LBRACE expression RBRACE
#              | LBRACE RBRACE
#              | conditional
#              | PLACEHOLDER
#              | FORMAT PLACEHOLDER
#              | FORMAT FORMAT PLACEHOLDER
#              | CONSTANT
#
# conditional  : expression QMARK expression
#              | expression BAR expression
#              | LCOMP conditional RCOMP

class Expr: pass

class Constant(Expr):
    def __init__(self, val):
        self.val = val

    def eval(self, env):
        return self.val

class Concat(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        return self.left.eval(env) + self.right.eval(env)

class Braced(Expr):
    def __init__(self, expr):
        self.expr = expr

    def eval(self, env):
        return self.expr.eval(env)

class Conditional(Expr):
    def __init__(self, ifExpr, thenExpr, elseExpr):
        '''
        Conditional(e1, e2, e3) corresponds to if e1 then e2 else e3
        Conditional(e1, None, e3) corresponds to if e1 then e1 else e3
        Conditional(e1, e2, None) corresponds to if e1 then e2 else ''
        where e1 is true if not empty and false otherwise
        '''
        self.ifExpr = ifExpr
        self.thenExpr = thenExpr
        self.elseExpr = elseExpr

    def eval(self, env):
        cond = self.ifExpr.eval(env)
        if str(cond) :
            if self.thenExpr:
                return self.thenExpr.eval(env)
            else:
                return cond
        else:
            if self.elseExpr:
                return self.elseExpr.eval(env)
            else:
                return ''

class Variable(Expr):
    def __init__(self, placeholder, format = None, style=None):
        self.varName = placeholder[1:-1]
        self.format = format
        self.style = style

    def eval(self, env):
        ph = env.data.get(self.varName)
        if ph:
            if '.' in self.varName:
                return ph
            else:
                fmt = self.format if self.format else env.defaultFormat.get(self.varName)
                st = self.style if self.style else env.defaultStyle.get(self.varName)
                return ph.format(fmt, st)
        else:
            return ''

precedence = (
    ('left', 'CONCAT'),
    ('left', 'BAR'),
    ('left', 'QMARK'),
    ('right', 'FORMAT'),
)

def p_expression_concat(p):
    'expression : expression expression %prec CONCAT'
    p[0] = Concat(p[1], p[2])

def p_expression_braced(p):
    'expression : LBRACE expression RBRACE'
    p[0] = Braced(p[2])

def p_expression_emptyBraces(p):
    'expression : LBRACE RBRACE'
    p[0] = Braced(Constant(''))

def p_expression_conditional(p):
    'expression : conditional'
    p[0] = p[1]

def p_expression_placeholder(p):
    'expression : PLACEHOLDER'
    p[0] = Variable(p[1])

def p_expression_formmatted(p):
    'expression : FORMAT PLACEHOLDER'
    p[0] = Variable(p[2], p[1])

def p_expression_styled(p):
    'expression : FORMAT FORMAT PLACEHOLDER'
    p[0] = Variable(p[3], p[2], p[1])

def p_expression_constant(p):
    'expression : CONSTANT'
    p[0] = Constant(p[1])

def p_conditional_qmark(p):
    'conditional : expression QMARK expression'
    p[0] = Conditional(p[1],p[3],None)
    
def p_conditional_bar(p):
    'conditional : expression BAR expression'
    p[0] = Conditional(p[1],None,p[3])

def p_error(p):
    pass

def get():
    lexer = lex.lex()
    parser = yacc.yacc(tabmodule='FormatParserTab')
    return lexer, parser

def example():
    lexer = lex.lex()
    lexer.input(r"{%ph% and [azerty[\]]%another%{a|b}]%qh%} \\<?, ?> %rh%")
    #lexer.input(r"[azerty]")
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

    class DummyField:
        def __init__(self, val):
            self.val = val

        def format(self, fmt, st):
            return self.val

    class Env: pass

    env = Env()
    env.data = {'ph' : DummyField('a'), 'qh' : DummyField(''), 'rh' : DummyField('c')}
    env.defaultFormat = {}
    env.defaultStyle = {}

    parser = yacc.yacc()

    result = parser.parse(r"z{%ph% and [azerty[\]]%another%{a|b}]%qh%} %rh%?d")
    print(result.eval(env))
    print('----------------------------\n')
    
    result = parser.parse(r"%ph%{{%ph%?%qh%}?, }%qh%{{%ph%%qh%}?%rh%}?, %rh%")
    print(result.eval(env))
    print('----------------------------\n')

if __name__ == "__main__":
    example()
