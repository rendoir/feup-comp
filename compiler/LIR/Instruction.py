

class SimpleInstruction:
    def __init__(self, descriptor):
        pass

    def __str__(self):
        raise NotImplementedError("Should have implemented SimpleInstruction.__str__()")

class Store:
    def __init__(self, descriptor):
        pass

    def __str__(self):
        pass


class Load:
    def __init__(self, descriptor):
        pass

    def __str__(self):
        pass

class LDF(Load):
    def __init__(self, descriptor):
        pass

    def __str__(self):
        pass

class LDL(Load):
    def __init__(self, descriptor):
        pass

    def __str__(self):
        pass

class LDP(Load):
    def __init__(self, descriptor):
        pass

    def __str__(self):
        pass

class LDA(Load):
    def __init__(self, descriptor):
        pass

    def __str__(self):
        pass

class Call:
    def __init__(self, descriptor):
        pass

    def __str__(self):
        pass
