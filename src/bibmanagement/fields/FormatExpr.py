# Copyright 2019-2022 CNRS-AIST JRL

import re
import warnings
from enum import IntEnum

def unusedChar(string, forbidden=[], n=1):
    '''
    Return n characters neither in string nor in forbidden.
    No special character from regular expression can be returned.
    '''
    assert(n>0)
    l = []
    for c in '#@!%&-_=,0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
        if c not in string and c not in forbidden:
            if n == 1:
                return c
            else:
                l.append(c)
                if len(l) == n:
                    return l
    raise ValueError('Cannot find ' + str(n) + ' unused characters')


class FormatExpr:
    '''
    Let # denote the empty set.
    A format expr can be
     - #
     - a constant expr: any string without [, ], % unless escaped
     - a placeholder expr with the form %placeholder%
     - a general expr as a concatenation of the above
     - a conditional expr [G] where G is a general expr
     - a separator expr [C] where C is a constant expr.
       Separator expr must be between two expr, each of which should be a placeholder or a conditional expr.
    Note that [] can only contain a constant or general expr. In particular brackets cannot be nested.

    A format expr is reduced as follows:
     - first, placeholders are replaced by their value, possibly # if there is no value
     - each conditional expr [G] is replaced by G if G doesn't contain #, or by # otherwise
     - each separator expr [C] is replaced: by C if the first non # before is a placeholder or conditional expr and it 
       is not followed by #, by # otherwise
     - finally all # are replaced by ''
    '''

    class _ExprType(IntEnum):
        EMPTY = 0
        CONSTANT = 1
        PLACEHOLDER = 2
        GENERAL = 3
        SEPARATOR = 4
        CONDITIONAL = 5

    def __init__(self, placeholders, formatExpr):
        for p in placeholders:
            if '\\' in p or '[' in p or ']' in p or '%' in p:
                raise ValueError('Incorrect placeholder name: ' + p)
        self._placeholders = placeholders
        self._parse(formatExpr)

    def placeholderList(self):
        return self._toBeReplaced

    def reduce(self, replacementList):
        if len(replacementList) != len(self._toBeReplaced):
            raise ValueError('replacement list does not contains the correct number of elements')

        # First reduction: replace placeholders
        k = 0
        red1 = []
        for s,t,n in self._subExpr:
            for i in range(k,k+n):
                r = replacementList[i]
                s = s.replace('%'+self._toBeReplaced[i]+'%', r if r else self._emptyChar)
            red1.append((s,t))
            k += n
            
        # Second reduction: conditional expressions and replace self._emptyChar by ('',EMPTY)
        red2 = []
        for s,t in red1:
            if t == FormatExpr._ExprType.CONDITIONAL:
                if self._emptyChar in s:
                    red2.append(('', FormatExpr._ExprType.EMPTY))
                else:
                    red2.append((s[1:-1], FormatExpr._ExprType.CONDITIONAL))
            else:
                if t == FormatExpr._ExprType.PLACEHOLDER and s == self._emptyChar:
                    red2.append(('', FormatExpr._ExprType.EMPTY))
                else:
                    red2.append((s,t))

        # Third reduction: separator expressions
        last = FormatExpr._ExprType.EMPTY
        string = ''
        n = len(red2)
        for i in range(0,n):
            s,t = red2[i]
            if t == FormatExpr._ExprType.SEPARATOR:
                # i+1 is ok here because the last element of red2 cannot be a separator
                if last != FormatExpr._ExprType.EMPTY and red2[i+1][1] != FormatExpr._ExprType.EMPTY:
                    string = string + s[1:-1]
            else:
                if t != FormatExpr._ExprType.EMPTY:
                    string = string + s
                    last = t

        # Lastly, we need to correct the escape characters
        string = string.replace(self._escapeChar, '')

        return string            
                

    def _parse(self, formatExpr):
        # We find unused chars to be used as empty char and escape char
        unused = unusedChar(formatExpr, '[]%', 2)
        self._emptyChar = unused[0]
        self._escapeChar = unused[1]
        self._noEscPattern = '(?<!' + unused[1] + ')'

        # Replace \ used for escaping by self._escapeChar
        fe = ''
        escaped = False
        for c in formatExpr:
            if escaped:
                fe += c
                escaped = False
            else:
                if c == '\\':
                    fe += self._escapeChar
                    escaped = True
                else:
                    fe += c

        # Match [x]
        subExprPattern = '(' + self._noEscPattern + '\[.*?' + self._noEscPattern + '\])'
        splitSub = re.split(subExprPattern, fe)
        
        # Parse sub expr
        self._toBeReplaced = []
        self._subExpr = []
        for e in splitSub:
            if len(e)==0:
                continue
            bracket =  e[0]=='[' and e[-1]==']'
            l = self._parseSubExpr(e)
            n = len(l)
            if n>0:
                if bracket:
                    self._subExpr.append((e, FormatExpr._ExprType.CONDITIONAL, n))
                else:
                    # We split a general expression into constant and placeholder expressions
                    spl = re.split('(' + self._noEscPattern + '%.*?' + self._noEscPattern + '%)', e)
                    for s in spl:
                        if s:
                            if s[0] == '%' and s[1:-1] in self._placeholders:
                                self._subExpr.append((s, FormatExpr._ExprType.PLACEHOLDER, 1))
                            else:
                                self._subExpr.append((s, FormatExpr._ExprType.CONSTANT, 0))
            else:
                if bracket:
                    self._subExpr.append((e, FormatExpr._ExprType.SEPARATOR, n))
                else:
                    self._subExpr.append((e, FormatExpr._ExprType.CONSTANT, n))

            self._toBeReplaced.extend(l)

        # We check if a separator is between two placeholder or conditional expr
        if self._subExpr[0][1] == FormatExpr._ExprType.SEPARATOR:
            raise ValueError('A separator cannot start an expression: ' + self._subExpr[0][0])
        if self._subExpr[-1][1] == FormatExpr._ExprType.SEPARATOR:
            raise ValueError('A separator cannot end an expression: ' + self._subExpr[-1][0])
        for i in range(1,len(self._subExpr)-1):
            if self._subExpr[i][1] == FormatExpr._ExprType.SEPARATOR:
                if not (self._subExpr[i-1][1] in [FormatExpr._ExprType.PLACEHOLDER, FormatExpr._ExprType.CONDITIONAL]):
                    raise ValueError('A separator can only appear after a placeholder or conditional expression: ' + self._subExpr[i][0])
                if not (self._subExpr[i+1][1] in [FormatExpr._ExprType.PLACEHOLDER, FormatExpr._ExprType.CONDITIONAL]):
                    raise ValueError('A separator can only appear before a placeholder or conditional expression: ' + self._subExpr[i][0])


    def _parseSubExpr(self, subExpr):
        # Check first that there is no [ other than the first one
        if re.search('(' + self._noEscPattern + '\[)', subExpr[1:-1]):
            raise ValueError('Sub-expression contains a non escaped [: ' + subExpr)

        # Check that there is an even number of %
        if (subExpr.count('%') - subExpr.count(self._escapeChar + '%'))%2== 1:
            raise ValueError('Sub-expression contains an uneven number of %')

        if self._placeholders:
            placeholderPattern = self._noEscPattern + '%(.*?)' + self._noEscPattern + '%'
            ph = re.findall(placeholderPattern, subExpr)
            l = []
            for p in ph:
                if  p in self._placeholders:
                    l.append(p)
                else:
                    warnings.warn('Unknown placeholder: ' + p)
        else:
            l = []
        return l
    