from ..HIR import Variable
from . import Tree

NL = '\n'

operators = {
    '*':    ('imul ' + NL),
    '/':    ('idiv ' + NL),
    '<<':   ('ishl ' + NL),
    '>>':   ('ishr ' + NL),
    '>>>':  ('iushr' + NL),
    '&':    ('iand ' + NL),
    '|':    ('ior ' + NL),
    '^':    ('ixor ' + NL),
    '+':    ('iadd ' + NL),
    '-':    ('isub ' + NL),
}

def getStackPosition(var_name, var_stack)  -> (Variable, int):
    for i in range(len(var_stack)):
        if isinstance(var_stack[i], str):
            ret = var_name == var_stack[i]
        else:
            ret = var_name == var_stack[i].name

        if ret:
            return (var_stack[i], str(i))

    return (None, None)

def printStack(var_stack) -> str:
    final_str = ("\nSTACK = [\n")
    for var in var_stack:
        final_str += '  ' + str(var) + NL

    final_str += ("]\n")
    return final_str

class SimpleInstruction:
    def __init__(self, var_name, var_stack):
        (self.const, self.var_access) = (None, None)

        if isinstance(var_name, str) and not Variable.Variable.isLiteral(var_name):
            (self.var, self.var_access) = getStackPosition(var_name, var_stack)
            if self.var_access is None:
                raise AssertionError("SimpleInstruction: no var '" + var_name + "' in stack: " + printStack(var_stack))
        else:
            self.const = var_name

    def __str__(self):
        raise NotImplementedError("Should have implemented SimpleInstruction.__str__()")

    # Returns (new_count, maximum_count_inside_instruction)
    def stackCount(self, curr) -> (int, int):
        raise NotImplementedError("SimpleInstruction::stackCount() not implemented!")

# TODO Check constants
class Load(SimpleInstruction):
    def __init__(self, var_name, var_stack=None, is_positive=True, size=False):
        super(Load, self).__init__(var_name, var_stack)
        self.negative = (not is_positive)
        self.size = size

    def __str__(self):
        final_str = ''
        if self.negative:
            final_str += 'ldc 0' + NL


        if self.const is not None :
            final_str += 'ldc ' + str(self.const) + NL
        else:
            if self.var.type == 'ARR':
                final_str = 'aload ' + self.var_access + NL

                if self.size:
                    final_str += 'arraylength' + NL
            else:
                final_str = 'iload ' + self.var_access + NL

        if self.negative:
            final_str = final_str[:-1]
            final_str += 'isub' + NL

        return final_str

    def stackCount(self, curr) -> (int, int):
        if not self.negative:
            ret = (curr + 1, curr + 1)
        else:
            ret = (curr + 1, curr + 2)
        return ret

class Store(SimpleInstruction):
    def __init__(self, var_name, var_stack, in_array=False, new_arr=False):
        try:
            super(Store, self).__init__(var_name, var_stack)
        except AssertionError:
            self.var_access = str(len(var_stack))
            var_stack.append(var_name)

        self.new_arr = new_arr
        self.in_array = in_array

    def __str__(self):
        if self.new_arr:
            return 'astore ' + self.var_access + NL
        elif self.in_array:
            return 'iastore' + NL
        else:
            return 'istore ' + self.var_access + NL

    def stackCount(self, curr) -> (int, int):
        if self.new_arr:
            ret = (curr - 1, curr)
        elif self.in_array:
            ret = (curr - 3, curr)
        else:
            ret = (curr - 1, curr)
        return ret

class ComplexInstruction:
    def __init__(self):
        self.code = []

    def __str__(self) -> str:
        final_str = ''
        for code_line in self.code:
            final_str += str(code_line)

        return final_str

    # Returns (new_count, maximum_count_inside_instruction)
    def stackCount(self, curr) -> (int, int):
        raise NotImplementedError("ComplexInstruction::stackCount() not implemented!")

class NewArr(ComplexInstruction):
    def __init__(self, var_name, var_stack, is_length):
        super(NewArr, self).__init__()
        self.code.append(Load(var_name, var_stack, True, is_length))
        self.code.append('newarray int' + NL)

    def stackCount(self, curr) -> (int, int):
        return (curr, curr)

class ArrAccess(ComplexInstruction):
    def __init__(self, arr_name, positive, var_stack, index):
        super(ArrAccess, self).__init__()

        # TODO negtivity here might not be correct
        self.code.append(Load(arr_name, var_stack, positive))
        self.code.append(Load(index, var_stack, True))
        self.code.append('iaload' + NL)

    def stackCount(self, curr) -> (int, int):
        return (curr + 1, curr + 2)

class Operator(ComplexInstruction):
    def __init__(self, left, right, operator):
        super(Operator, self).__init__()

        self.code.append(left)
        self.code.append(right)
        self.code.append(operators[operator])

    def stackCount(self, curr) -> (int, int):
        return Tree.Entry.countStackLimit(self.code)


class ConditionalBranch(ComplexInstruction):
    cmp_operators_neg = {
        '>': '<=',
        '<': '>=',
        '<=': '>',
        '>=': '<',
        '==': '!=',
        '!=': '==',
    }

    cmp_to_if = {
        '==': 'if_icmpeq ',
        '!=': 'if_icmpne ',
        '<': 'if_icmplt ',
        '<=': 'if_icmple ',
        '>': 'if_icmpgt ',
        '>=': 'if_icmpge ',
    }

    def __init__(self, left, right, operator, true_code, labels):
        super(ConditionalBranch, self).__init__()
        self.template = []

        # Add Conditional
        for left_op in left:
            self.template.append(left_op)
        for right_op in right:
            self.template.append(right_op)

        self.template.append(self.cmp_to_if[self.cmp_operators_neg[operator]] + labels[0] + NL + NL)

        # Add True Code
        for code_line in true_code:
            self.template.append(code_line)

        # Add goto and label
        self.template.append('goto ' + labels[1] + NL)
        self.template.append(NL + self._printLabel(labels[0]) + NL)



    def _printLabel(self, label_name) -> str:
        return label_name + ':'

class IfBranching(ConditionalBranch):
    # code = [true_code, false_code]
    # labels = [start_label, end_label]
    def __init__(self, left, right, operator, code, labels):
        (self.true_code, self.false_code) = code
        self.has_else = len(self.false_code) is not 0
        self.end_label = labels[1]
        super(IfBranching, self).__init__(left, right, operator, self.true_code, labels)
        if not self.has_else:
            del self.template[-2]

    def __str__(self) -> str:
        final_str = ''
        for code_line in self.template:
            final_str += str(code_line)

        for code_line in self.false_code:
            final_str += str(code_line)

        if self.has_else:
            final_str += self._printLabel(self.end_label) + NL

        return final_str

    def stackCount(self, curr) -> (int, bool):
        (curr, max_curr)      = Tree.Entry.countStackLimit(self.template)
        (true_curr, true_max) = Tree.Entry.countStackLimit(self.true_code)
        (else_curr, else_max) = Tree.Entry.countStackLimit(self.false_code)
        true_curr += curr
        else_curr += curr
        return (max(true_curr, else_curr), max(true_max, else_max, max_curr))

class WhileBranching(ConditionalBranch):
    # code = true_code
    # labels = start_label
    def __init__(self, left, right, operator, code, labels):
        self.code = code
        self.loop_label = labels[1]
        super(WhileBranching, self).__init__(left, right, operator, code, labels)

    def __str__(self) -> str:
        final_str = ''
        final_str += self._printLabel(self.loop_label) + NL

        for code_line in self.template:
            final_str += str(code_line)

        return final_str

    def stackCount(self, curr) -> (int, bool):
        (curr, max_curr)      = Tree.Entry.countStackLimit(self.template)
        (code_curr, code_max) = Tree.Entry.countStackLimit(self.code)
        return (curr + code_curr, max_curr + code_max)
