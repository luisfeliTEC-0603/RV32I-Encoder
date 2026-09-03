import json
import os
import sys

class RISCV_Parser:
    """
    Parser for RISC-V assembly instructions.
    
    This class handles tokenization of assembly instructions, validation of
    instructions and registers, and provides access to instruction metadata
    loaded from JSON configuration files.
    
    Attributes:
        separators (str): Characters used as token separators (',', '(', ')')
        supported_inst (list): List of supported instruction mnemonics
        inst_data (dict): Instruction metadata loaded from riscv_inst.json
        reg_data (dict): Register mappings loaded from riscv_reg.json
        fmt_data (dict): Format field definitions loaded from riscv_fmt.json
    """

    def __init__(self, _supported_inst: list):
        self.separators = ',()'
        self.supported_inst = _supported_inst
    
        self.inst_data = {}
        self.reg_data = {}
        self.fmt_data = {}
        
        self._load_all_json_data()
        
    def _load_json_file(self, filename: str) -> dict:
        """
        Load and parse a JSON file from the same directory as this script.
        
        Args:
            filename (str): Name of the JSON file to load
            
        Returns:
            dict: Parsed JSON data
            
        Raises:
            FileNotFoundError: If the JSON file does not exist
            ValueError: If the JSON file contains invalid JSON
        """

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
        """
        Load all required JSON configuration files.
        
        Loads:
            + riscv_inst.json: Instruction metadata (opcode, funct3, funct7)
            + riscv_reg.json: Register name to number mappings
            + riscv_fmt.json: Format field definitions and descriptions
            
        Exits the program if any file cannot be loaded.
        """

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
        """
        Tokenize an assembly instruction string into a list of tokens.
        
        Handles:
            - Removing comments (lines starting with '#' or ';')
            - Splitting by separators: ',', '(', ')'
            - Removing label colons
            - Whitespace normalization
        
        Args:
            instruction (str): Assembly instruction string
            
        Returns:
            list: List of tokens, or empty list if instruction is empty
        """

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
        """
        Retrieve instruction metadata (format, opcode, funct3, funct7).
        
        Args:
            instruction_name (str): Instruction mnemonic (e.g., 'add')
            silence (bool): If False, print instruction information to stdout
            
        Returns:
            dict: Instruction metadata containing 'format', 'opcode', 'funct3', 'funct7'
            
        Raises:
            ValueError: If instruction is not supported
        """

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
        """
        Convert a register name to its numeric value (0-31).
        
        Supports both ABI names (e.g., 'sp') and numeric names (e.g., 'x2').
        
        Args:
            reg_name (str): Register name (e.g., 'x5', 'sp', 'ra')
            
        Returns:
            int: Register number (0-31)
            
        Raises:
            ValueError: If register name is unknown
        """

        if reg_name not in self.reg_data:
            raise ValueError(f"[ ERROR ] Unknown register: {reg_name}")

        data = self.reg_data[reg_name]
        print(f'├ ARG (REG): {reg_name} ({data:05b})')

        return data 
    
    def get_format_info(self, format_type: str) -> dict:
        """
        Retrieve format field definitions for a given instruction format.
        
        Args:
            format_type (str): Format type ('R', 'I', 'S', or 'B')
            
        Returns:
            dict: Format information containing field definitions with:
                + name: Field name
                + start_bit: Starting bit position
                + end_bit: Ending bit position
                + description: Field description
                
        Raises:
            ValueError: If format type is unknown
        """

        if format_type not in self.fmt_data:
            raise ValueError(f"[ ERROR ] Unknown format type: {format_type}")
        
        return self.fmt_data[format_type]
