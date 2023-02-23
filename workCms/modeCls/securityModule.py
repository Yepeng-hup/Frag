# 安全类
class Security(object):
    cmdKeyword = ['rm', '.sh', '.py', '.go']

    def __init__(self, clientCmd):
        self.clientCmd = clientCmd

    def cmdSecurity(self) -> bool:

        for i in self.cmdKeyword:
            self.bools = i in self.clientCmd
            if self.bools == True:
                break
        return self.bools
