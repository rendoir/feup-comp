from antlr_yal import yalParser
from antlr4.Token import Token
from antlr4.tree.Tree import *

class yalRealParser(yalParser):
    def consume(self):
        o = self.getCurrentToken()
        if o.type != Token.EOF:
            self.getInputStream().consume()
        hasListener = self._parseListeners is not None and len(self._parseListeners)>0
        if self.buildParseTrees or hasListener:
            if self._errHandler.inErrorRecoveryMode(self):
                node = self._ctx.addErrorNode(o)
            else:
                node = self._ctx.addTokenNode(o)

            if hasListener and node != None:
                for listener in self._parseListeners:
                    if isinstance(node, ErrorNode):
                        listener.visitErrorNode(node)
                    elif isinstance(node, TerminalNode):
                        listener.visitTerminal(node)
        return o
