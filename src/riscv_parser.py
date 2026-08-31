class RISCV_Parser:
    def __init__(self):
        self.separators = ',()'
    
    def tokenize(self, instruction: str) -> lst:
        if '#' in instruction:
            instruction = instruction.split('#')[0]
        
        instruction = instruction.strip()
        
        if not instruction:
            return []
        
        for sep in self.separators:
            instruction = instruction.replace(sep, ' ')
        
        tokens = [token for token in instruction.split() if token]
        
        if tokens and tokens[0].endswith(':'):
            tokens[0] = tokens[0][:-1]
        
        return tokens

    def analyse_tokens(self, tokens: list, supported_inst: list):
        raise NotImplementedError("[ ERROR ] token analysis missing...")
