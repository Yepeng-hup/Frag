class Security(object):
    cmdKeyword = ['rm', '.sh', '.py', 'bash', 'sh', 'python']
    command_str = ['||', '&&', 'and', 'or', '|']

    def __init__(self, clientCmd):
        self.clientCmd = clientCmd

    def cmdSecurity(self) -> bool:

        for i in self.cmdKeyword:
            self.bools = i in self.clientCmd
            if self.bools == True:
                break
        return self.bools
    
    def cmdSpecialStrSecurity(self) -> bool:
        for i in self.command_str:
            self.bools = i in self.clientCmd
            if self.bools == True:
                break
        return self.bools
