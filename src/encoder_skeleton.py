#!/usr/bin/env python3
import sys

SOPORTADAS = ["add", "sub", "and", "or", "addi", "andi",
              "lw", "lb", "sw", "sb", "beq", "bne"]

from riscv_parser import RISCV_Parser
parser = RISCV_Parser(SOPORTADAS)

from riscv_encoder import RISCV_Encoder
encoder = RISCV_Encoder()

def encode_instruction(tokens: list) -> int:
    print('ENCODING...') 
    if not tokens:
        raise ValueError("[ ERROR ] Empty instruction")
    
    inst_name = tokens[0].lower()
    operands = tokens[1:]
    print(f'├ TOKENS: {tokens}')

    inst_info = parser.get_instruction_info(inst_name, False)
    format_type = inst_info['format']
    
    opcode = int(inst_info['opcode'], 2)
    funct3 = int(inst_info['funct3'], 2) if inst_info['funct3'] else 0
    funct7 = int(inst_info['funct7'], 2) if inst_info['funct7'] else 0
    
    def parse_imm(imm_str: str) -> int:
        if imm_str.startswith('0x') or imm_str.startswith('0X'):
            return int(imm_str, 16)
        elif imm_str.startswith('0b') or imm_str.startswith('0B'):
            return int(imm_str, 2)
        else:
            return int(imm_str)
    
    if format_type == 'R':
        if len(operands) != 3:
            raise ValueError(f"R-format instruction '{inst_name}' expects 3 operands")
        
        params = {
            'rd': parser.get_register_info(operands[0]),
            'rs1': parser.get_register_info(operands[1]),
            'rs2': parser.get_register_info(operands[2]),
            'opcode': opcode,
            'funct3': funct3,
            'funct7': funct7
        }
        return encoder.encode_r_format(**params) 
    
    elif format_type == 'I':
        if len(operands) != 3:
            raise ValueError(f"I-format instruction '{inst_name}' expects 3 operands")
        
        params = {
            'rd': parser.get_register_info(operands[0]),
            'rs1': parser.get_register_info(operands[1]),
            'imm': parse_imm(operands[2]),
            'opcode': opcode,
            'funct3': funct3
        }
        return encoder.encode_i_format(**params)  
    
    elif format_type == 'S':
        if len(operands) == 2:
            params = {
                'rs2': parser.get_register_info(operands[0]),
                'imm': 0,
                'rs1': parser.get_register_info(operands[1]),
                'opcode': opcode,
                'funct3': funct3
            }
        elif len(operands) == 3:
            params = {
                'rs2': parser.get_register_info(operands[0]),
                'imm': parse_imm(operands[1]),
                'rs1': parser.get_register_info(operands[2]),
                'opcode': opcode,
                'funct3': funct3
            }
        else:
            raise ValueError(f"S-format instruction '{inst_name}' expects 2 or 3 operands")

        return encoder.encode_s_format(**params)  
    
    elif format_type == 'B':
        if len(operands) != 3:
            raise ValueError(f"B-format instruction '{inst_name}' expects 3 operands")
        
        params = {
            'rs1': parser.get_register_info(operands[0]),
            'rs2': parser.get_register_info(operands[1]),
            'imm': parse_imm(operands[2]),
            'opcode': opcode,
            'funct3': funct3
        }
        return encoder.encode_b_format(**params)  
    
    else:
        raise ValueError(f"Unsupported format: {format_type}")

def explain_instruction(instruction: str, word: int) -> str:
    tokens = parser.tokenize(instruction)
    if not tokens:
        return "Empty instruction"
    
    inst_name = tokens[0].lower()
    inst_info = parser.get_instruction_info(inst_name, True)
    format_type = inst_info['format']
    
    fmt_info = parser.get_format_info(format_type)
    
    result = []
    result.append(f"│")
    result.append(f"├ FORMAT:{format_type}")
    result.append(f'│\t └── {fmt_info['description']}')
    result.append("└" + "─" * 94)
    result.append(f"{'FIELD':<18} {'BITS':<12} {'BINARY':<16} {'VALUE':<12} {'DESCRIPTION'}")
    result.append("─" * 95)
    
    for field in fmt_info['fields']:
        name = field['name']
        start = field['start_bit']
        end = field['end_bit']
        desc = field['description']
        
        bit_range = f"{start}-{end}"
        if start == end:
            bit_range = str(start)
        
        mask = ((1 << (end - start + 1)) - 1) << start
        value = (word & mask) >> start
        
        field_bin = format(value, f'0{end - start + 1}b')
        
        if name == 'opcode':
            value_str = f"0x{value:02x}"
        elif name.startswith('imm'):
            value_str = f"{value} (0x{value:x})"
        else:
            value_str = str(value)
        
        result.append(f"{name:<18} {bit_range:<12} {field_bin:<16} {value_str:<12} {desc}")
    
    result.append("┌" + "─" * 94)
    result.append(f"└ ENCODING DONE (•ᴗ•)\n")
    
    return "\n".join(result)

def main():
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} "<instruction>"', file=sys.stderr)
        print(f'Example: {sys.argv[0]} "add x5, x6, x7"', file=sys.stderr)
        sys.exit(2)

    instruction = sys.argv[1]

    print('[ INSTRUCTION ]')
    box_width = len(instruction) + 6
    print("┌" + "─" * box_width + "┐")
    print("│" + " " * 3 + instruction.upper() + " " * 3 + "│")
    print("└" + "─" * box_width + "┘")
    print()

    tokens = parser.tokenize(instruction)
    word = encode_instruction(tokens) & 0xFFFFFFFF

    print(explain_instruction(instruction, word))
    print(f"BINARY: {word:032b}")

    # No modificar el formato de la siguiente línea: la especificación la
    # requiere, literal, para permitir la validación automática.
    print(f"HEX: 0x{word:08x}")
    print()

if __name__ == "__main__":
    main()
