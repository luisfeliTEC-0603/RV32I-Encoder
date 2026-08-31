#!/usr/bin/env python3
"""
Esqueleto del Codificador Educativo de Instrucciones RISC-V.
CE4301 Arquitectura de Computadores I — Proyecto Individual — 2026-II

Este esqueleto ya implementa el contrato de línea de comandos y de salida
requerido por la especificación. Usted debe completar las dos funciones
marcadas con TODO; puede modificar el resto del archivo si lo necesita,
siempre que se preserve el contrato de invocación y la línea "HEX: 0x...".

No es obligatorio usar este esqueleto ni Python: puede implementar su
propia herramienta desde cero, en el lenguaje que prefiera, siempre que
respete el mismo contrato (ver especificación, sección "Modo de operación").
"""
import sys

SOPORTADAS = ["add", "sub", "and", "or", "addi", "andi",
              "lw", "lb", "sw", "sb", "beq", "bne"]

from riscv_parser import RISCV_Parser
parser = RISCV_Parser(SOPORTADAS)

from riscv_encoder import RISCV_Encoder
encoder = RISCV_Encoder()

def encode_instruction(tokens: list) -> int:
    if not tokens:
        raise ValueError("Empty instruction")
    
    inst_name = tokens[0].lower()
    operands = tokens[1:]

    inst_info = parser.get_instruction_info(inst_name)
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
    """
    Debe retornar un texto (para imprimirse en pantalla) que muestre, de
    forma visual, los 32 bits de 'word' divididos en los campos del
    formato correspondiente (R, I, S o B) — indicando el rango de bits y
    el valor de cada campo — junto con una breve explicación de cada uno.
    El formato visual (colores, tabla, arte ASCII, etc.) queda a su
    criterio, siempre que sea claro.
    """
    # TODO: implementar.
    raise NotImplementedError("explain_instruction: pendiente de implementar")


def main():
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} "<instruction>"', file=sys.stderr)
        print(f'Example: {sys.argv[0]} "add x5, x6, x7"', file=sys.stderr)
        sys.exit(2)

    instruction = sys.argv[1]

    tokens = parser.tokenize(instruction)
    print(tokens)

    word = encode_instruction(tokens) & 0xFFFFFFFF
    print(f"{word:b}")
    print(f"HEX: 0x{word:08x}")

    print(explain_instruction(instruction, word))

    # No modificar el formato de la siguiente línea: la especificación la
    # requiere, literal, para permitir la validación automática.
    print(f"HEX: 0x{word:08x}")

if __name__ == "__main__":
    main()
