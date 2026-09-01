import json
import os
import sys

class RISCV_Parser:
    def __init__(self, _supported_inst: list):
        self.separators = ',()'
        self.supported_inst = _supported_inst
    
        self.inst_data = {}
        self.reg_data = {}
        self.fmt_data = {}
        
        self._load_all_json_data()
        
    def _load_json_file(self, filename: str) -> dict:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, filename)
        
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"[ ERROR ] Required JSON file not found: {json_path}")
        
        try:
            with open(json_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"[ ERROR ] Invalid JSON in file {filename}: {e}")
    
    def _load_all_json_data(self):
        try:
            inst_json = self._load_json_file('riscv_inst.json')
            self.inst_data = inst_json.get('inst', {})
            
            reg_json = self._load_json_file('riscv_reg.json')
            self.reg_data = reg_json.get('reg', {})

            fmt_json = self._load_json_file('riscv_fmt.json')
            self.fmt_data = fmt_json.get('fmt', {})

        except (FileNotFoundError, ValueError) as e:
            print(f"[ ERROR ] While loading JSON data: {e}", file=sys.stderr)
            sys.exit(1)

    def tokenize(self, instruction: str) -> list:
        if '#' in instruction:
            instruction = instruction.split('#')[0]
        if ';' in instruction:
            instruction = instruction.split(';')[0]
        
        instruction = instruction.strip()
        
        if not instruction:
            return []
        
        for sep in self.separators:
            instruction = instruction.replace(sep, ' ')
        
        tokens = [token for token in instruction.split() if token]
        
        if tokens and tokens[0].endswith(':'):
            tokens[0] = tokens[0][:-1]
        
        return tokens

    def get_instruction_info(self, instruction_name: str, silence: bool) -> dict:
        if instruction_name not in self.supported_inst or instruction_name not in self.inst_data:
            raise ValueError(f"[ ERROR ] Unsupported instruction: {instruction_name}")
        
        inst_info = self.inst_data[instruction_name]

        if not silence:
            print(f'├ MNEMONIC: {instruction_name}')
            print(f'│\t ├── OPCODE: {inst_info.get("opcode", "N/A")}')
            print(f'│\t ├── FUNCT7: {inst_info.get("funct7", "N/A")}') 
            print(f'│\t └── FUNCT3: {inst_info.get("funct3", "N/A")}') 

        return {
            "format": inst_info.get("format"),
            "opcode": inst_info.get("opcode"),
            "funct3": inst_info.get("funct3"),
            "funct7": inst_info.get("funct7")
        }
    
    def get_register_info(self, reg_name: str) -> int:
        if reg_name not in self.reg_data:
            raise ValueError(f"[ ERROR ] Unknown register: {reg_name}")

        data = self.reg_data[reg_name]
        print(f'├ ARG (REG): {reg_name} ({data:05b})')

        return data 
    
    def get_format_info(self, format_type: str) -> dict:
        if format_type not in self.fmt_data:
            raise ValueError(f"[ ERROR ] Unknown format type: {format_type}")
        
        return self.fmt_data[format_type]
