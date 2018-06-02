from ..HIR import Variable
from . import Tree
NL = '\n'
module_name = None
module_vars_used = 0
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

apply_operator  ={
    '*': (lambda left, right: left * right),
    '/': (lambda left, right: left / right),
    '<<': (lambda left, right: left << right),
    '>>': (lambda left, right: left >> right),
    '>>>': (lambda left, right: (left % 0x100000000) >> right),
    '&': (lambda left, right: left & right),
    '|': (lambda left, right: left | right),
    '^': (lambda left, right: left ^ right),
    '+': (lambda left, right: left + right),
    '-': (lambda left, right: left - right),
}

def getStackPosition(var_name, var_stack)  -> (Variable, int):
    for i in range(len(var_stack)):
        if isinstance(var_stack[i], str):
            ret = (var_name == var_stack[i])
        else:
            ret = (var_name == var_stack[i].name)

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
    module_vars = None

    def __init__(self, var_name, var_stack):
        global module_vars_used
        (self.const, self.var_access, self.var) = (None, None, None)

        if isinstance(var_name, str) and not Variable.Variable.isLiteral(var_name):
            (self.var, self.var_access) = getStackPosition(var_name, var_stack)

            if self.var_access is None:
                if var_name in self.module_vars:
                    self.var = self.module_vars[var_name]
                    if self.var.altered > 0:
                        module_vars_used += 1
                else:
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
        self.var_name = var_name
        self.negative = (not is_positive)
        self.size = size
        if isinstance(self.var, Variable.NumberVariable) and self.var.altered is 0 and self.var.value is not None:
            self.const = self.var.value
            self.var = None
            self.var_access = None

    def __str__(self):
        global module_name
        final_str = ''
        if self.negative and self.const is None:
            final_str += 'iconst_0' + NL

        if isinstance(self.var, Variable.Variable):
            final_str += 'getstatic ' + module_name + '/' + self.var.name + ' ' + self.var.toLIR() + NL
        elif self.const is not None:
            if isinstance(self.const, int) or self.const[0] != '"':
                final_str += self.constSelector(int(self.const)) + NL
            else:
                final_str += 'ldc ' + self.const + NL
        else:
            if self.var.type == 'ARR':
                final_str += self.loadSelector('aload', int(self.var_access)) + NL

                if self.size:
                    final_str += 'arraylength' + NL
            else:
                final_str += self.loadSelector('iload', int(self.var_access)) + NL

        if self.negative and self.const is None:
            final_str += 'isub' + NL

        return final_str

    def stackCount(self, curr) -> (int, int):
        return (curr + 1, curr + 1)

    def constSelector(self, const_n) -> str:
        if const_n is -1:
            return 'iconst_m1'
        if 0 <= const_n <= 5:
            return 'iconst_' + str(const_n)
        elif -128 <= const_n <= 127:
            return 'bipush ' + str(const_n)
        elif -32768 <= const_n <= 32767:
            return 'sipush ' + str(const_n)
        else:
            return 'ldc ' + str(const_n)

    def loadSelector(self, load_type, access_n):
        if 0 <= access_n <= 3:
            return load_type + '_' + str(access_n)
        else:
            return load_type + ' ' + str(access_n)

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
        global module_name
        if isinstance(self.var, Variable.Variable):
            return 'putstatic ' + module_name + '/' + self.var.name + ' ' + self.var.toLIR() + NL
        else:
            if self.new_arr:
                return self.storeSelector('astore', int(self.var_access)) + NL
            elif self.in_array:
                return 'iastore' + NL
            else:
                return self.storeSelector('istore', int(self.var_access)) + NL


    def stackCount(self, curr) -> (int, int):
        if self.new_arr:
            ret = (curr - 1, curr)
        elif self.in_array:
            ret = (curr - 3, curr)
        else:
            ret = (curr - 1, curr)
        return ret

    def storeSelector(self, store_type, access_n):
        if 0 <= access_n <= 3:
            return store_type + '_' + str(access_n)
        else:
            return store_type + ' ' + str(access_n)

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
        self.operator = operator
        self.code.append(left)
        self.code.append(right)
        self.code.append(operators[operator])

    def stackCount(self, curr) -> (int, int):
        ret = Tree.Entry.countStackLimit(self.code)
        return (ret[0]-1, ret[1])

    def __str__(self) -> str:
        if self.operationUnfold(self.code[0], self.code[1]):
            return str(self.code[0])
        else:
            return super(Operator, self).__str__()

    def operationUnfold(self, left, right) -> bool:
        global apply_operator
        all_load = isinstance(left, Load) and isinstance(right, Load)
        all_const = left.const is not None and right.const is not None

        if all_load and all_const:
            del self.code[:]
            result = apply_operator[self.operator](int(left.const), int(right.const))
            self.code.append(Load(result))
            return True

        return False


    def canUnfoldConstant(self) -> bool:
        left = self.code[0]
        right = self.code[1]
        return (isinstance(left, Load) and left.const is not None) or (isinstance(right, Load) and right.const is not None)

    # def constantUnfold(self, constant_inst, store_pos) -> bool:
    #     if isinstance(constant_inst, Load) and constant_inst.const is not None:
    #         value = int(constant_inst.const)
    #         if -128 <= value <= 127:
    #             del self.code[:]
    #             self.code.append('iinc ' + str(store_pos) + ' ' + str(constant_inst.const))
    #             return True
    #
    #     return False


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
            if code_line != '':
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
            if code_line != '':
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
