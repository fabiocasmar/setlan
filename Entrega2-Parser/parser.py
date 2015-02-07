#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""Parser for RangeX Language
Fabio, Castro 10-10132
Antonio, Scaramazza 11-10957
"""

import ply.yacc as yacc
from lexer import tokens, lexer_error, find_column
from ast import *


# The first rule to evaluate
# A RangeX program always begins with the reserved word 'program'
# and has one, and only one statement next
def p_program(symbol):
    "program : PROGRAM statement"
    symbol[0] = Program(symbol[2])

###############################################################################
#############################     STATEMENTS      #############################
###############################################################################


# The assign statement
# ID '=' expression
def p_statement_assing(symbol):
    "statement : ID ASSIGN expression"
    symbol[0] = Assign(Variable(symbol[1]), symbol[3])



# The block statement
# starts with 'begin' and ends with 'end'
# It has an optional declarations list and a list of statements
# each declaration and each statement is separated by a ';'
def p_statement_block(symbol):
    """statement : OPENCURLY statement_list CLOSECURLY
                 | OPENCURLY USING declare_list IN statement_list CLOSECURLY"""
    if len(symbol) == 4:
        symbol[0] = Block(symbol[2])
    else:
        # symbol[0] = Block(symbol[4], symbol[3])
        symbol[0] = Block(symbol[5])


# A grammar rule to create multiple declarations in a block statement
def p_statement_declare_list(symbol):
    """declare_list : data_type declare_comma_list SEMICOLON
                    | declare_list data_type declare_comma_list SEMICOLON"""
    if len(symbol) == 4:
        symbol[0] = [(symbol[2], symbol[1])]
    else:
        symbol[0] = symbol[1] + [(symbol[3], symbol[2])]


# A grammar rule to create multiple variables in a declaration
def p_statement_declare_comma_list(symbol):
    """declare_comma_list : ID
                          | declare_comma_list COMMA ID"""
    if len(symbol) == 2:
        symbol[0] = [Variable(symbol[1])]
    else:
        symbol[0] = symbol[1] + [Variable(symbol[3])]


# Multiple statements in a block statement have a separation token, the ';'
def p_statement_statement_list(symbol):
    """statement_list : 
                      | statement_list statement SEMICOLON"""
    if len(symbol) == 1:
        symbol[0] = []
    else:
        symbol[0] = symbol[1] + [symbol[2]]


# For the 'as' part of a declaration
def p_data_type(symbol):
    """data_type : INT
                 | BOOL
                 | SET """
    symbol[0] = symbol[1]

###############################     IN/OUT      ###############################


# The scan statement, it works on a variable
def p_statement_scan(symbol):
    "statement : SCAN ID"
    symbol[0] = Scan(Variable(symbol[2]))


# The write statement, it prints on standard output the list of elements
# given to it, in order
def p_statement_print(symbol):
    """statement : PRINT comma_list
                 | PRINTLN comma_list"""
    if symbol[1].upper() == 'PRINT':
        symbol[0] = Print(symbol[2])
    else:
        if len(symbol) == 3:
            symbol[0] = Print(symbol[2] + [String('"\\n"')])
        else:
            symbol[0] = Print([String('"\\n"')])


# To generate the list of elements for a 'print' or a 'println'
def p_statement_comma_list(symbol):
    """comma_list : expression
                  | comma_list COMMA expression"""
    if len(symbol) == 2:
        symbol[0] = [symbol[1]]
    else:
        symbol[0] = symbol[1] + [symbol[3]]

############################     CONDITIONAL      #############################


# The if statement, it may or may not have an 'else'
def p_statement_if(symbol):
    """statement :  IF OPENPAREN expression CLOSEPAREN  statement ELSE statement
                  |   IF OPENPAREN expression CLOSEPAREN  statement  """
    if len(symbol) == 6:
        symbol[0] = If(symbol[3], symbol[5])
    else:
        symbol[0] = If(symbol[3], symbol[5], symbol[7])

# def p_statment_2(symbol):
#      """statement2 : statement ELSE statement
#                   |  statement """

###############################     LOOP      #################################


# The for statement, automatically declares an 'int' variable in the scope of
# the for, this variable has a value of every value in the range specified
def p_statement_for(symbol):
    """statement : FOR ID MAX expression DO statement
                 | FOR ID MIN expression DO statement"""
    symbol[0] = For(Variable(symbol[2]), symbol[4], symbol[6], symbol[3])


# The while statement, while some condition holds, keep doing a statement
def p_statement_while(symbol):
    "statement : WHILE OPENPAREN expression CLOSEPAREN DO statement"
    symbol[0] = While(symbol[3], symbol[6])

# The while statement, while some condition holds, keep doing a statement
def p_statement_repeat(symbol):
    "statement : REPEAT statement WHILE OPENPAREN expression CLOSEPAREN "
    symbol[0] = Repeat(symbol[2], symbol[5])


# The while statement, while some condition holds, keep doing a statement
def p_statement_repeat_while(symbol):
    "statement : REPEAT statement WHILE OPENPAREN expression CLOSEPAREN DO statement"
    symbol[0] = RepeatWhile(symbol[2], symbol[5], symbol[8])


###############################################################################
#############################     EXPRESSIONS     #############################
###############################################################################


# Precedence defined for expressions
precedence = (
    # language
    ("right", 'CLOSEPAREN'),
    ("right", 'ELSE'),
    # bool
    ("left", 'OR'),
    ("left", 'AND'),
    ("right", 'NOT'),
    # ("left", 'EQUIVALENT', 'INEQUIVALENT'),
    # compare
    ("nonassoc", 'SETBELONG'),
    ("nonassoc", 'EQUAL', 'UNEQUAL'),
    ("nonassoc", 'LESS', 'LESSEQ', 'GREAT', 'GREATEQ'),
    # set 
    ("left", 'SETUNION','SETDIFFERENCE'),
    ("left",'SETINTERSECTION'),
    ("right",'SETMAX','SETMIN','SETLEN'),
    # int over set
    ("left", 'SETPLUS','SETMINUS'),
    ("left", 'SETTIMES','SETDIVITION','SETMOD'),
    # int
    ("left", 'PLUS', 'MINUS'),
    ("left", 'TIMES', 'DIVIDE', 'MODULE'), 
    ("right", 'UMINUS'),#revisar '-' para declarar un negativo
)

##############################     LITERALS     ###############################


# A number is a valid expression
def p_exp_int_literal(symbol):
    "expression : NUMBER"
    symbol[0] = Int(symbol[1])


# A boolean is a valid expression
def p_exp_bool_literal(symbol):
    """expression : TRUE
                  | FALSE"""
    symbol[0] = Bool(symbol[1].upper())


# A range is a valid expression
def p_exp_set_literal(symbol):
    "expression : OPENCURLY comma_list CLOSECURLY"
    symbol[0] = Set(symbol[2])


# A string is a valid expression
def p_exp_string_literal(symbol):
    "expression : STRING"
    symbol[0] = String(symbol[1])


# An ID is a variable expression, since an ID is an int, bool or range
def p_expression_id(symbol):
    "expression : ID"
    symbol[0] = Variable(symbol[1])


# An expression between parenthesis is still an expression
def p_expression_group(symbol):
    """expression : OPENPAREN expression CLOSEPAREN"""
    symbol[0] = symbol[2]

#############################     OPERATORS     ###############################


# Binary operators defined for int
def p_exp_int_binary(symbol):
    """expression : expression PLUS   expression
                  | expression MINUS  expression
                  | expression TIMES  expression
                  | expression DIVIDE expression
                  | expression MODULE expression"""
    operator = {
        '+': 'PLUS',
        '-': 'MINUS',
        '*': 'TIMES',
        '/': 'DIVIDE',
        '%': 'MODULE'
    }[symbol[2]]
    symbol[0] = Binary(operator, symbol[1], symbol[3])


# Unary minus, defined for int
def p_exp_int_unary(symbol):
    "expression : MINUS expression %prec UMINUS"  #REVISAR ESE %prec
    symbol[0] = Unary('MINUS', symbol[2])


# Binary operators defined for set
def p_exp_set_binary(symbol):
    """expression : expression SETUNION expression
                  | expression SETINTERSECTION expression 
                  | expression SETDIFFERENCE expression """
    operator = {
        '++': 'SETUNION',
        '><': 'SETINTERSECTION',
        '\\': 'SETDIFFERENCE'
    }[symbol[2]]
    # operator = 'INTERSECTION'
    symbol[0] = Binary(operator, symbol[1], symbol[3])  #REVISAR: no estoy seguro de esta parte


# Considered these functions as unary operators for range
def p_exp_set_unary(symbol):
    """expression : SETMAX   expression 
                  | SETMIN   expression 
                  | SETMINUS expression 
                  | SETLEN   expression """
                  
    symbol[0] = Unary(symbol[1].upper(), symbol[2])  #REVISAR: parentesis LPAREN y RPAREN

# Binary operators defined for int
def p_exp_int_set_binary(symbol):
    """expression : expression SETPLUS   expression
                  | expression SETMINUS  expression
                  | expression SETTIMES  expression
                  | expression SETDIVITION expression
                  | expression SETMOD expression"""
    operator = {
        '<+>': 'SETPLUS',
        '<->': 'SETMINUS',
        '<*>': 'SETTIMES',
        '</>': 'SETDIVITION',
        '<%>': 'SETMOD'
    }[symbol[2]]
    symbol[0] = Binary(operator, symbol[1], symbol[3])


# Binary operators defined for bool
def p_exp_bool_binary(symbol):
    """expression : expression OR      expression
                  | expression AND     expression"""
                  # | expression EQUAL   expression %prec EQUIVALENT
                  # | expression UNEQUAL expression %prec INEQUIVALENT"""
    operator = {
        'or': 'OR',
        'and': 'AND',
        # '==': 'EQUIVALENT',
        # '/=': 'INEQUIVALENT'
    }[symbol[2]]
    symbol[0] = Binary(operator, symbol[1], symbol[3])


# Unary not, defined for bool
def p_exp_bool_unary(symbol):
    "expression : NOT expression"
    if isinstance(symbol[2], Bool):
        expr = eval(symbol[2].value.title())
        expr = str(not expr).upper()
        symbol[0] = Bool(expr)
    else:
        symbol[0] = Unary(symbol[1].upper(), symbol[2])


# Binary operators to compare
def p_exp_bool_compare(symbol):
    """expression : expression LESS    expression
                  | expression LESSEQ  expression
                  | expression GREAT   expression
                  | expression GREATEQ expression
                  | expression EQUAL   expression
                  | expression UNEQUAL expression"""
    operator = {
        '<': 'LESS',
        '<=': 'LESSEQ',
        '>': 'GREAT',
        '>=': 'GREATEQ',
        '==': 'EQUAL',
        '/=': 'UNEQUAL'
    }[symbol[2]]
    symbol[0] = Binary(operator, symbol[1], symbol[3])


# Binary oprator defined for an int and a range
def p_exp_bool_int_range(symbol):
    "expression : expression SETBELONG expression"
    symbol[0] = Binary('SETBELONG', symbol[1], symbol[3])


# Commented in case of need afterwards
########################
# def p_exp_bool_range_binary(symbol):
#     """expression : expression LESS    expression
#                   | expression LESSEQ  expression
#                   | expression GREAT   expression
#                   | expression GREATEQ expression
#                   | expression EQUAL   expression
#                   | expression UNEQUAL expression"""
#     operator = {
#         '<': 'RLESS',
#         '<=': 'RLESSEQ',
#         '>': 'RGREAT',
#         '>=': 'RGREATEQ',
#         '==': 'REQUAL',
#         '/=': 'RUNEQUAL'
#     }[symbol[2]]
#     symbol[0] = Binary(operator, symbol[1], symbol[3])

################################## ERROR ######################################


# Error to be shown if the parser finds a Syntax error
def p_error(symbol):
    if symbol:
        text = symbol.lexer.lexdata
        message = "ERROR: Syntax error at line %d, column %d: "
        message += "Unexpected token '%s'"
        data = (symbol.lineno, find_column(text, symbol), symbol.value)
        parser_error.append(message % data)
    else:
        parser_error.append("ERROR: Syntax error at EOF")


# Build the parser
parser = yacc.yacc(start='program')
parser_error = []


# The file (stored in a Python String) goes through the
# parser and returns an AST that represents the program
def parsing(data, debug=0):
    parser.error = 0
    ast = parser.parse(data, debug=debug)
    if parser.error:
        ast = None
    return ast

###############################################################################


# Only to be called if this is the main module
def main(argv=None):
    import sys      # argv, exit

    if argv is None:
        argv = sys.argv

    if len(argv) == 1:
        print "ERROR: No input file"
        return
    elif len(argv) > 3:
        print "ERROR: Invalid number of arguments"
        return

    if len(argv) == 3:
        debug = eval(argv[2])
    else:
        debug = 0

    # Opens file to interpret
    file_string = open(argv[1], 'r').read()

    ast = parsing(file_string, debug)

    if lexer_error:
        ast = None
        for error in lexer_error:
            print error
    elif parser_error:
        ast = None
        for error in parser_error:
            print error
    else:
        print ast

    return ast


# If this is the module running
if __name__ == "__main__":
    main()
