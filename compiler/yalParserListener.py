from antlr_yal import *
from antlr4 import *
from pprint import pprint

def eraseChilds(ctx:ParserRuleContext):
    for i in range(ctx.getChildCount()):
        ctx.removeLastChild()

def valid(ctx, min_childs):
    return ctx.children is not None and ctx.getChildCount() >= min_childs and ctx.exception is None

def varToString(node) -> str:
    if isinstance(node, tree.Tree.TerminalNodeImpl):
        ret = str(node)
    else:
        ret = str(node.children[0])

    if isinstance(node, yalParser.Array_elementContext):
        return ret + '[]'

    return ret

# TODO erase '[' ']' and replace by string
class yalParserListener(yalListener):

    # Holds [<name>, <declarations>*, <functions>*]
    def exitModule(self, ctx:yalParser.ModuleContext):
        if valid(ctx, 4):
            del ctx.children[0]
            del ctx.children[1]
            del ctx.children[ctx.getChildCount() - 1]

    # Holds [<element>]
    # OR
    # Holds [<element>, <arr_size>]
    # OR
    # Holds [<element>, <NUMBER>]
    def exitDeclaration(self, ctx:yalParser.DeclarationContext):
        if valid(ctx, 2):
            del ctx.children[-1] # D_COMMA

            if len(ctx.children) > 3:
                if str(ctx.children[2]) is '[':
                    del ctx.children[4]
                    del ctx.children[2]
                elif str(ctx.children[2]) is '+' or str(ctx.children[2]) is '-':
                    ctx.children[3] = int(str(ctx.children[2]) + str(ctx.children[3]))
                    del ctx.children[2]

                del ctx.children[1]


    # Holds [<var_name>, <func_name>, <var_list>?, <stmt_list>]
    # OR
    # Holds [<func_name>, <var_list>?, <stmt_list>]
    # Note: If there are no var_list, the node is None
    def exitFunction(self, ctx:yalParser.FunctionContext):
        if ctx.children is not None:
            del ctx.children[-1]
            del ctx.children[-2]
            del ctx.children[-2]

            # Delete left parenthesis
            if isinstance(ctx.children[-2], tree.Tree.TerminalNodeImpl):
                del ctx.children[-2]
            else:
                del ctx.children[-3]


            if str(ctx.children[2]) is '=':
                del ctx.children[2]

            del ctx.children[0]



    # Holds [<var1>, <var2> ...]
    def exitVar_list(self, ctx:yalParser.Var_listContext):
        if valid(ctx, 3):
            count = int(ctx.getChildCount() / 2)
            for i in range(1, count + 1, 1): # Delete ','
                del ctx.children[i]

    # Just removes the ';'
    def exitStmt(self, ctx:yalParser.StmtContext):
        if valid(ctx, 2):
            del ctx.children[1]

    def exitElse_yal(self, ctx:yalParser.Else_yalContext):
        if valid(ctx, 4):
            del ctx.children[1]
            del ctx.children[2]

    # Holds [<operator> <operator>]
    def exitAssign(self, ctx:yalParser.AssignContext):
        if valid(ctx, 4):
            del ctx.children[3]
            del ctx.children[1]

    # Holds [<ID> <index_access>]
    def exitArray_access(self, ctx:yalParser.Array_accessContext):
        if valid(ctx, 4):
            del ctx.children[-1]
            del ctx.children[-2]

    # Holds [<var_name>] or [<var_name>, <SIZE>]
    # Transforms scalar access into either a single node (no SIZE), or two nodes if it has SIZE
    def exitScalar_access(self, ctx:yalParser.Scalar_accessContext):
        if valid(ctx, 3):
            del ctx.children[1]

    # Holds [<expr>, <OPERATOR>, <expr>]
    def exitExprtest(self, ctx:yalParser.ExprtestContext):
        if valid(ctx, 5):
            del ctx.children[0]
            del ctx.children[3]

    # Holds [<condition>, <true_body>, <false_body>]
    def exitIf_yal(self, ctx:yalParser.If_yalContext):
        if valid(ctx, 5):
            del ctx.children[0]
            del ctx.children[1]
            del ctx.children[2]

    # Holds [<condition>, <body>]
    def exitWhile_yal(self, ctx:yalParser.While_yalContext):
        if valid(ctx, 5):
            del ctx.children[0]
            del ctx.children[1]
            del ctx.children[2]

    # Holds [<arg1>, <arg2> ....]
    def exitArg_list(self, ctx:yalParser.Arg_listContext):
        args = []
        for child in ctx.getChildren():
            if not isinstance(child, TerminalNode):
                for grandchild in child.getChildren():
                    args.append(grandchild)

        eraseChilds(ctx)
        for arg in args:
            ctx.addChild(arg)

    # Transforms `call` rule into:
    # call: name arg_list
    #  where name is a string which when split with '.' gives the access
    def exitCall(self, ctx:yalParser.CallContext):
        if valid(ctx, 4):
            del ctx.children[-1]
            del ctx.children[-2]

            # Check if it is a module call
            if len(ctx.children) is 4:
                ctx.children[0] = [ctx.children[0], ctx.children[1]]
                del ctx.children[2]
                del ctx.children[1]
            else:
                ctx.children[0] = [ctx.children[0]]
