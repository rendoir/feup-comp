from antlr4.Token import Token

prune = ['{', '}', ';', ',']

class yalRealParser(yalParser):
    def consume(self):
        o = self.getCurrentToken()
        if o.type != Token.EOF:
            self.getInputStream().consume()
        hasListener = self._parseListeners is not None and len(self._parseListeners)>0
        if self.buildParseTrees or hasListener:
            if self._errHandler.inErrorRecoveryMode(self):
                node = self._ctx.addErrorNode(o)
            elif o.text not in prune:
                node = self._ctx.addTokenNode(o)
            if hasListener:
                for listener in self._parseListeners:
                    if isinstance(node, ErrorNode):
                        listener.visitErrorNode(node)
                    elif isinstance(node, TerminalNode):
                        listener.visitTerminal(node)
        return o
