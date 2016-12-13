# !usr/bin/python
# coding=utf-8

'''
    a simple calculator using recursive descent parser

    EBNF:
        expr ::= term { (+|-) term }*
        term ::= factor { (*|/) factor }*
        factor ::= ( expr )
                | NUM
'''

import re
import collections

NUM = r'(?P<NUM>\d+)'
PLUS = r'(?P<PLUS>\+)'
MINUS = r'(?P<MINUS>-)'
TIMES = r'(?P<TIMES>\*)'
DIVIDE = r'(?P<DIVIDE>/)'
LPAREN = r'(?P<LPAREN>\()'
RPAREN = r'(?P<RPAREN>\))'
WS = r'(?P<WS>\s+)'

master_pat = re.compile('|'.join([NUM, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN, WS]))

Token = collections.namedtuple('Token', ['type', 'value'])

def generate_tokens(text):
    scaner = master_pat.scanner(text)
    for m in iter(scaner.match, None):
        tok = Token(m.lastgroup, m.group())
        if tok.type != "WS":
            yield tok

class ExpressionEvaluator:

    def parse(self, text):
        self.tokens = generate_tokens(text)
        self.tok = None
        self.nexttok = None
        self._advance()
        return self.expr()

    def _advance(self):
        self.tok, self.nexttok = self.nexttok, next(self.tokens, None)

    def _accept(self, toktype):
        if self.nexttok and self.nexttok.type == toktype:
            self._advance()
            return True
        else:
            return False

    def _except(self, toktype):
        if not self._accept(toktype):
            raise SyntaxError("Expected " + toktype)

    def expr(self):
        exprval = self.term()
        while self._accept("PLUS") or self._accept("MINUS"):
            op = self.tok.type
            right = self.term()
            if op == "PLUS":
                exprval += right
            elif op == "MINUS":
                exprval -= right
        return exprval

    def term(self):
        termval = self.factor()
        while self._accept("TIMES") or self._accept("DIVIDE"):
            op = self.tok.type
            right = self.factor()
            if op == "TIMES":
                termval *= right
            elif op == "DIVIDE":
                termval /= right
        return termval

    def factor(self):
        if self._accept("NUM"):
            return int(self.tok.value)
        elif self._accept("LPAREN"):
            exprval = self.expr()
            self._accept('RPAREN')
            return exprval
        else:
            raise SyntaxError("Expected NUMBER or LPRAREN")

if __name__ == '__main__':
    e = ExpressionEvaluator()
    print e.parse('2+(3+1)+3')


# import re
# import collections
# from operator import add, sub, mul, div

# Token = collections.namedtuple('Token', ['name', 'value'])
# RuleMatch = collections.namedtuple('RuleMatch', ['name', 'matched'])

# token_map = {'+': 'ADD', '-': 'ADD', '*': 'MUL',
#              '/': 'MUL', '(': 'LPAR', ')': 'RPAR'}
# rule_map = {
#     'add': ['mul ADD add', 'mul'],
#     'mul': ['atom MUL mul', 'atom'],
#     'atom': ['NUM', 'LPAR add RPAR', 'neg'],
#     'neg': ['ADD atom'],
# }
# fix_assoc_rules = 'add', 'mul'

# bin_calc_map = {'*': mul, '/': div, '+': add, '-': sub}


# def calc_binary(x):
#     while len(x) > 1:
#         x[:3] = [bin_calc_map[x[1]](x[0], x[2])]
#     return x[0]

# calc_map = {
#     'NUM': float,
#     'atom': lambda x: x[len(x) != 1],
#     'neg': lambda (op, num): (num, -num)[op == '-'],
#     'mul': calc_binary,
#     'add': calc_binary,
# }


# def match(rule_name, tokens):
#     if tokens and rule_name == tokens[0].name:   # Match a token?
#         return tokens[0], tokens[1:]
#     for expansion in rule_map.get(rule_name, ()):  # Match a rule?
#         remaining_tokens = tokens
#         matched_subrules = []
#         for subrule in expansion.split():
#             matched, remaining_tokens = match(subrule, remaining_tokens)
#             if not matched:
#                 break  # no such luck. next expansion!
#             matched_subrules.append(matched)
#         else:
#             return RuleMatch(rule_name, matched_subrules), remaining_tokens
#     return None, None  # match not found


# def _recurse_tree(tree, func):
#     return map(func, tree.matched) if tree.name in rule_map else tree[1]


# def flatten_right_associativity(tree):
#     new = _recurse_tree(tree, flatten_right_associativity)
#     if tree.name in fix_assoc_rules and len(new) == 3 and new[2].name == tree.name:
#         new[-1:] = new[-1].matched
#     return RuleMatch(tree.name, new)


# def evaluate(tree):
#     solutions = _recurse_tree(tree, evaluate)
#     return calc_map.get(tree.name, lambda x: x)(solutions)


# def calc(expr):
#     split_expr = re.findall('[\d.]+|[%s]' % ''.join(token_map), expr)
#     tokens = [Token(token_map.get(x, 'NUM'), x) for x in split_expr]
#     tree = match('add', tokens)[0]
#     tree = flatten_right_associativity(tree)
#     return evaluate(tree)

# if __name__ == '__main__':
#     # while True:
#     #     print(calc(raw_input('> ')))
