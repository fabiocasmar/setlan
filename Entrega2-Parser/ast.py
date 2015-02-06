

# To set indentation automatically
def indent(level):
    return "    " * level


class Program:
    """A program consists of running a statement"""
    def __init__(self, statement):
        self.statement = statement

    def __str__(self):
        return "PROGRAM\n" + self.statement.print_tree(1)


# For inheritance
class Statement: pass


class Assign(Statement):
    """The assign statement"""
    def __init__(self, variable, expression):
        # self.type = "assign"
        self.variable = variable
        self.expression = expression

    def print_tree(self, level):
        string = indent(level) + "ASSIGN\n" + indent(level + 1)
        string += "variable: " + str(self.variable)
        string += "\n" + indent(level + 1)
        string += "value:\n" + self.expression.print_tree(level + 2)
        return string


class Block(Statement):
    """Block statement, it's just a sequence of statements"""
    # def __init__(self, statements, declarations=[]):
    def __init__(self, statements):
        # self.type = "block"
        # self.declarations = declarations
        self.statements = statements

    def print_tree(self, level):
        string = indent(level) + "BLOCK\n"
        # if self.declarations:
        #     string += indent(level) + "DECLARATIONS\n"
        #     for decl in self.declarations:
        #         var_list = decl[0]
        #         var_type = decl[1]
        #         string += indent(level + 1) + var_type + ': '
        #         for variable in var_list:
        #             string += str(variable) + ', '
        #         string = string[:-2] + '\n'
        #         string += indent(level + 1) + "SEPARATOR\n"
        #     string = string[:(-10 - len(indent(level + 1)))]
        # string += indent(level) + "STATEMENTS\n"
        for stat in self.statements:
            string += stat.print_tree(level + 1) + '\n'
            string += indent(level + 1) + "SEPARATOR\n"
        string = string[:(-10 - len(indent(1)))]
        string += "BLOCK_END"
        return string


class Scan(Statement):
    """Scan statement, for user input"""
    def __init__(self, variable):
        # self.type = "read"
        self.variable = variable

    def print_tree(self, level):
        string = indent(level) + "SCAN\n"
        string += indent(level + 1) + "variable: " + str(self.variable)
        return string


class Print(Statement):
    """Write statement, for printing in standard output"""
    def __init__(self, elements):
        # self.type = "write"
        self.elements = elements

    def print_tree(self, level):
        string = indent(level) + "PRINT\n"
        for elem in self.elements:
            string += indent(level + 1) + "element:\n"
            string += elem.print_tree(level + 2) + '\n'
        return string[:-1]


class If(Statement):
    """If statement"""
    def __init__(self, condition, then_st, else_st=None):
        # self.type = "if"
        self.condition = condition
        self.then_st = then_st
        self.else_st = else_st

    def print_tree(self, level):
        string = indent(level) + "IF\n"
        string += indent(level + 1) + "condition:\n"
        string += self.condition.print_tree(level + 2) + '\n'
        string += indent(level + 1) + "then:\n"
        string += self.then_st.print_tree(level + 2)
        if self.else_st:
            string += '\n' + indent(level + 1) + "else:\n"
            string += self.else_st.print_tree(level + 2)
        return string


class For(Statement):
    """For statement, works in ranges"""
    def __init__(self, variable, in_range, statement, dire):
        # self.type = "for"
        self.variable = variable
        self.in_range = in_range
        self.statement = statement
        self.dire = dire

    def print_tree(self, level):
        string = indent(level) + "FOR\n"
        string += indent(level + 1) + "variable: " + str(self.variable) + '\n'
      # ERROR POSIBLE AQUI
        string += indent(level + 1) + str(self.dire) + ":\n"
        string += self.in_range.print_tree(level + 2) + '\n'
        string += indent(level + 1) + "DO statement:\n"
        string += self.statement.print_tree(level + 2)
        return string


class While(Statement):
    """While statement, takes a condition"""
    def __init__(self, condition, statement):
        # self.type = "while"
        self.condition = condition
        self.statement = statement

    def print_tree(self, level):
        string = indent(level) + "WHILE\n"
        string += indent(level + 1) + "condition:\n"
        string += self.condition.print_tree(level + 2) + '\n'
        string += indent(level + 1) + "DO statement:\n"
        string += self.statement.print_tree(level + 2)
        return string

class Repeat(Statement):
    """While statement, takes a condition"""
    def __init__(self, statement, condition):
        # self.type = "while"
        self.condition = condition
        self.statement = statement

    def print_tree(self, level):
        string = indent(level) + "WHILE\n"
        string += indent(level + 1) + "DO statement:\n"
        string += self.statement.print_tree(level + 2)
        string += indent(level + 1) + "condition:\n"
        string += self.condition.print_tree(level + 2) + '\n'
        return string

class RepeatWhile(Statement):
    """While statement, takes a condition"""
    def __init__(self, statement, condition, statement2):
        # self.type = "while"
        self.condition  = condition
        self.statement  = statement
        self.statement2 = statement2

    def print_tree(self, level):
        string = indent(level) + "WHILE\n"
        string += indent(level + 1) + "DO statement:\n"
        string += self.statement.print_tree(level + 2)
        string += indent(level + 1) + "condition:\n"
        string += self.condition.print_tree(level + 2) + '\n'
        string += indent(level + 1) + "DO statement2:\n"
        string += self.statement2.print_tree(level + 2)
        return string

# For inheritance
class Expression: pass


class Variable(Expression):
    """Class to define a variable"""
    def __init__(self, name):
        # self.type = "var"
        self.name = name

    def __str__(self):
        return str(self.name)

    def print_tree(self, level):
        return indent(level) + "VARIABLE: " + str(self.name)


class Int(Expression):
    """Class to define an expression of int"""
    def __init__(self, value):
        # self.type = "int"
        self.value = value

    def __str__(self):
        return str(self.value)

    def print_tree(self, level):
        return indent(level) + "INT: " + str(self.value)


class Bool(Expression):
    """Class to define an expression of bool"""
    def __init__(self, value):
        # self.type = "bool"
        self.value = value

    def __str__(self):
        return str(self.value)

    def print_tree(self, level):
        return indent(level) + "BOOL: " + str(self.value)


class Set(Expression):
    """Class to define an expression of range"""
    def __init__(self, valores):
        # self.type = "range"
        self.valores = valores

    def __str__(self):
        return str(self.valores) + '..' + str(self.valores)

    def print_tree(self, level):
        string = indent(level) + "VALORES:\n" + indent(level+1) + " {" 
        for i in self.valores:
            string+= str(i)+','
        string +=  '} \n'
        return string


class String(Expression):
    """Class to define an expression of a printable string"""
    def __init__(self, value):
        # self.type = "string"
        self.value = value

    def __str__(self):
        return self.value

    def print_tree(self, level):
        return indent(level) + "STRING: " + str(self.value)


class Binary(Expression):
    """Binary expressions"""
    def __init__(self, operator, left, right):
        # self.type = "binary: "
        self.operator = operator
        self.left = left
        self.right = right

    def print_tree(self, level):
        string = indent(level) + "BINARY:\n" + indent(level + 1)
        string += "operator: " + self.operator + '\n'
        string += indent(level + 1) + "left operand:\n"
        string += self.left.print_tree(level + 2) + '\n'
        string += indent(level + 1) + "right operand:\n"
        string += self.right.print_tree(level + 2)
        return string


class Unary(Expression):
    """Unary expressions"""
    def __init__(self, operator, operand):
        # self.type = "unary: "
        self.operator = operator
        self.operand = operand

    def print_tree(self, level):
        string = indent(level) + "UNARY:\n" + indent(level + 1) + "operator: "
        string += str(self.operator) + '\n'
        string += indent(level + 1) + "operand:\n"
        string += self.operand.print_tree(level + 2)
        return string