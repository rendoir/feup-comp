from antlr_yal import *
from antlr4 import *
from pprint import pprint

def getCaller(children:yalParser.CallContext):
    caller = ""
    end = False
    for child in children:
        if end:
            return (caller, child)

        if str(child) == "(":
            end = True
        else:
            caller += str(child)

    print("Caller parenthesis not found!")
    for child in children:
        print("    " + str(child))
    return None

def eraseChilds(ctx:ParserRuleContext):
    for i in range(ctx.getChildCount()):
        ctx.removeLastChild()

def valid(ctx, min_childs):
    return ctx.children is not None and ctx.getChildCount() >= min_childs and ctx.exception is None

# TODO erase '[' ']' and replace by string
class yalParserListener(yalListener):

    # Holds [<name>, <declarations>*, <functions>*]
    def exitModule(self, ctx:yalParser.ModuleContext):
        print(valid(ctx, 4))
        if valid(ctx, 4):
            del ctx.children[0]
            del ctx.children[1]
            del ctx.children[ctx.getChildCount() - 1]

    # Holds [<element>]
    # OR
    # Holds [<element>, '[', <arr_size>, ']']
    # OR
    # Holds [<element>, <NUMBER>]
    def exitDeclaration(self, ctx:yalParser.DeclarationContext):
        ctx.children[0] = ctx.children[0].getText()
        if valid(ctx, 2):
            count = ctx.getChildCount()
            del ctx.children[ctx.getChildCount() - 1] # D_COMMA

            if count is 4:
                del ctx.children[1] #Erase '='
            if count is 6:
                ctx.children[3] = ctx.children[3].getText()
                del ctx.children[1] #Erase '='


    # Holds [<var_name>, <func_name>, <var_list>?, <stmt_list>]
    # OR
    # Holds [<func_name>, <var_list>?, <stmt_list>]
    # Note: If there are no var_list, the node is None
    def exitFunction(self, ctx:yalParser.FunctionContext):
        if ctx.children is not None:
            count = ctx.getChildCount()
            del ctx.children[count - 1]
            del ctx.children[count - 3]
            count = count - 2

            if ctx.children[2].getText() is '=':
                del ctx.children[6 if count is 7 else 5]
                del ctx.children[4]
                del ctx.children[2]
                ctx.children[1] = ctx.children[1].getText()
            else:
                del ctx.children[4 if count is 6 else 3]
                del ctx.children[2]
            del ctx.children[0]
            ctx.children[0] = ctx.children[0].getText()

    # Holds [<var1>, <var2> ...]
    # TODO double check
    def exitVar_list(self, ctx:yalParser.Var_listContext):
        if valid(ctx, 3):
            count = int(ctx.getChildCount() / 2)
            for i in range(1, count + 1, 1): # Delete ','
                del ctx.children[i]

            for i in range(ctx.getChildCount()):
                ctx.children[i] = ctx.children[i].getText()

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


    # # If there is only one child its an array access
    # # TODO check if it is needed to process left option
    # def exitRight_op(self, ctx:yalParser.Right_opContext):
    #     print("RIGHT OP")
    #     print(str(ctx.children))
    #     if isinstance(ctx.children[0], tree.Tree.TerminalNodeImpl): # Is '[' <arr_size> ']'
    #         eraseChilds(ctx)
    #         ctx.addChild(str(ctx.children[1]))

    # Holds [<ID> <index_access>]
    def exitArray_access(self, ctx:yalParser.Array_accessContext):
        if valid(ctx, 4):
            ctx.children[2] = ctx.children[2].children[0].getText()
            del ctx.children[1]
            del ctx.children[2]

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
            res = getCaller(ctx.getChildren())
            if res is not None:
                (caller, args) = (res[0], res[1])
                eraseChilds(ctx)
                ctx.addChild(caller)
                ctx.addChild(args)
