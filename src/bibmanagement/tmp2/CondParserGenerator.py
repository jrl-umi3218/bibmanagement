import ply.lex as lex
import ply.yacc as yacc
import types

# List of token names.
tokens = ('CONSTANT',
          'PLACEHOLDER',
          'FORMAT',
          'LBRACE',
          'RBRACE',
          'LCOMP',          # <?xxx>
          'RCOMP',          # <xxx?>
          'LRCOMP',         # <?xxx?>
          'LNEG',           # <~xxx>
          'RNEG',           # <xxx~>
          'LRNEG',          # <~xxx~>
          'LNEGRCOMP',      # <~xxx?>
          'LCOMPRNEG',      # <?xxx~>
          'QMARK',
          'BAR'
         )

# States of the lexer
states = (
    ('escape', 'exclusive'),
    ('comp', 'exclusive'),
    ('format', 'exclusive'),
)

# Regular expression rules for simple tokens
t_CONSTANT    = r'[^%{}<>?|\[\]\\]+'
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
def t_begin_comp(t):
    r'\<'
    t.lexer.format_start = t.lexer.lexpos  #start position of the format string
    t.lexer.level = 1
    t.lexer.maxDepth = max(t.lexer.maxDepth, t.lexer.level)
    t.lexer.emit = False
    t.lexer.push_state('comp')

def t_comp_open(t):
    r'\<'
    t.lexer.level += 1
    t.lexer.maxDepth = max(t.lexer.maxDepth, t.lexer.level)

def t_comp_escape(t):
    r'\\'
    t.lexer.push_state('escape')

def t_comp_close(t):
    r'\>'
    t.lexer.level -= 1

    if t.lexer.level == 0:
        s = t.lexer.lexdata[t.lexer.format_start:t.lexer.lexpos-1]
        if not s or s=='?' or s=='??' or s=='~' or s=='~~' or s=='?~' or s=='~?':
            return # we ignore <>, <?>, <??>, <~>, <~~>, <?~> and <~?>
        if s[0] == '?':
            if len(s)>=2 and s[-1]=='?' and s[-2]!='\\':
                t.value = s[1:-1]
                t.type = 'LRCOMP'
            elif len(s)>=2 and s[-1]=='~' and s[-2]!='\\':
                t.value = s[1:-1]
                t.type = 'LCOMPRNEG'
            else:
                t.value = s[1:]
                t.type = 'LCOMP'
        elif s[0] == '~':
            if len(s)>=2 and s[-1]=='?' and s[-2]!='\\':
                t.value = s[1:-1]
                t.type = 'LNEGRCOMP'
            elif len(s)>=2 and s[-1]=='~' and s[-2]!='\\':
                t.value = s[1:-1]
                t.type = 'LRNEG'
            else:
                t.value = s[1:]
                t.type = 'LNEG'
        else:
            if len(s)>1 and s[-1]=='?' and s[-2]!='\\':
                t.value = s[:-1]
                t.type = 'RCOMP'
            elif len(s)>1 and s[-1]=='~' and s[-2]!='\\':
                t.value = s[:-1]
                t.type = 'RNEG'
            else:
                t.value = s
                t.type = 'CONSTANT'
        t.lexer.pop_state()
        return t

def t_comp_other(t):
    r'[^<>\\]+'
    pass

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
        t.value = t.lexer.lexdata[t.lexer.format_start-1:t.lexer.lexpos]
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

def t_comp_error(t):
    pass

def t_format_error(t):
    pass

# expression   : expression expression
#              | LBRACE expression RBRACE
#              | LBRACE RBRACE
#              | conditional
#              | lcomp
#              | rcomp
#              | lrcomp
#              | lneg
#              | rneg
#              | lrneg
#              | lcomprneg
#              | lnegrcomp
#              | PLACEHOLDER
#              | FORMAT PLACEHOLDER
#              | CONSTANT
#
# conditional  : expression QMARK expression
#              | expression BAR expression
#
# lcomp        : expression LCOMP
#
# rcomp        : RCOMP expression
#
# lrcomp       : expression LRCOMP expression
#
# lneg         : expression LNEG
#
# rneg         : RNEG expression
#
# lrneg        : expression LRNEG expression
#
# lcomprneg    : expression LCOMPRNEG expression
#
# lnegrcomp    : expression LNEGRCOMP expression

class Expr: pass

class Constant(Expr):
    def __init__(self, val):
        self.val = val

    def unparse(self):
        return self.val

class Concat(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def unparse(self):
        return self.left.unparse() + self.right.unparse()

class Braced(Expr):
    def __init__(self, expr):
        self.expr = expr

    def unparse(self):
        return '{' + self.expr.unparse() + '}'

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

    def unparse(self):
        s = self.ifExpr.unparse()
        if self.thenExpr:
            s += '?' + self.thenExpr.unparse()
        if self.elseExpr:
            s += '|' + self.elseExpr.unparse()
        return s

class Variable(Expr):
    def __init__(self, placeholder):
        self.placeholder = placeholder[1:-1]

    def unparse(self):
        return '%'+ self.placeholder + '%'

class LCond(Expr):
    def __init__(self,left,comp,neg):
        self.comp = comp
        self.left = left
        self.neg = neg

    def unparse(self):
        if self.neg:
            return self.left.unparse() + '{{{' + self.left.unparse() +  '}?{} | *}?' + self.comp + '}'
        else:
            return self.left.unparse() + '{{' + self.left.unparse() +  '}?' + self.comp + '}'

class RCond(Expr):
    def __init__(self,comp,right,neg):
        self.comp = comp
        self.right = right
        self.neg = neg

    def unparse(self):
        if self.neg:
            return '{{{' + self.right.unparse() +  '}? | *}?' + self.comp + '}' + self.right.unparse()
        else:
            return '{{' + self.right.unparse() +  '}?' + self.comp + '}' + self.right.unparse()

class LRCond(Expr):
    def __init__(self,left,comp,right,lneg,rneg):
        self.comp = comp
        self.left = left
        self.right = right
        self.lneg = lneg
        self.rneg = rneg

    def unparse(self):
        lcond = '{{' + self.left.unparse() +  '}?{} | *}' if self.lneg else '{' + self.left.unparse() +  '}'
        rcond = '{{' + self.right.unparse() +  '}?{} | *}' if self.rneg else '{' + self.right.unparse() +  '}'
        return self.left.unparse() + '{{' + lcond +  '?' + rcond + '}?' + self.comp + '}' + self.right.unparse()

precedence = (
    ('left', 'CONCAT'),
    ('left', 'LCOMP', 'LRCOMP', 'LNEG', 'LRNEG', 'LCOMPRNEG', 'LNEGRCOMP'),
    ('right', 'RCOMP', 'RNEG'),
    ('left', 'BAR'),
    ('left', 'QMARK'),
    ('right', 'FORMAT')
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

def p_expression_promote(p):
    '''expression : conditional
                  | lcomp
                  | rcomp
                  | lrcomp
                  | lneg
                  | rneg
                  | lrneg
                  | lcomprneg
                  | lnegrcomp'''
    p[0] = p[1]

def p_expression_placeholder(p):
    'expression : PLACEHOLDER'
    p[0] = Variable(p[1])

def p_expression_constant(p):
    'expression : CONSTANT'
    p[0] = Constant(p[1])
    
def p_expression_format(p):
    'expression : FORMAT PLACEHOLDER'
    p[0] = Concat(Constant(p[1]),Variable(p[2]))

def p_expression_style(p):
    'expression : FORMAT FORMAT PLACEHOLDER'
    p[0] = Concat(Constant(p[1]),Concat(Constant(p[2]),Variable(p[3])))

def p_conditional_qmark(p):
    'conditional : expression QMARK expression'
    p[0] = Conditional(p[1],p[3],None)
    
def p_conditional_bar(p):
    'conditional : expression BAR expression'
    p[0] = Conditional(p[1],None,p[3])

def p_lcomp(p):
    'lcomp : expression LCOMP'
    p[0] = LCond(p[1],p[2],False)
    
def p_rcomp(p):
    'rcomp : RCOMP expression'
    p[0] = RCond(p[1],p[2],False)

def p_lrcomp(p):
    'lrcomp : expression LRCOMP expression'
    p[0] = LRCond(p[1],p[2],p[3],False,False)

def p_lneg(p):
    'lneg : expression LNEG'
    p[0] = LCond(p[1],p[2],True)
    
def p_rneg(p):
    'rneg : RNEG expression'
    p[0] = RCond(p[1],p[2],True)

def p_lrneg(p):
    'lrneg : expression LRNEG expression'
    p[0] = LRCond(p[1],p[2],p[3],True,True)

def p_lcomprneg(p):
    'lcomprneg : expression LCOMPRNEG expression'
    p[0] = LRCond(p[1],p[2],p[3],False,True)

def p_lnegrcomp(p):
    'lnegrcomp : expression LNEGRCOMP expression'
    p[0] = LRCond(p[1],p[2],p[3],True,False)

def p_error(p):
    pass

def get():
    lexer = lex.lex()
    # patching the lexer:
    #  - we add a new field maxDepth
    #  - we change the input method so that it reset maxDepth to 0
    def newInput(self,s):
        self.input_(s)
        self.maxDepth = 0

    lexer.maxDepth = 0;
    lexer.input_ = lexer.input
    lexer.input = types.MethodType(newInput, lexer)
    parser = yacc.yacc(tabmodule='FormatParserTab', debug=False)
    return lexer, parser
    