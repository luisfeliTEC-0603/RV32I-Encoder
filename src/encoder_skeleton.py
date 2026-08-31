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
    """
    Recibe una instrucción como texto, p. ej. "add x5, x6, x7", y debe
    retornar su codificación de 32 bits como entero (0 <= valor < 2**32).

    Debe soportar únicamente las instrucciones en SOPORTADAS. Los valores
    de opcode/funct3/funct7 de cada una NO se proveen aquí: deben
    investigarse en el manual oficial de la ISA RISC-V (ver referencia en
    la especificación) y documentarse en el README.
    """
    # TODO: implementar. Sugerencia: parsear el mnemónico y los operandos,
    # despachar según el formato (R/I/S/B), y ensamblar los campos con
    # operaciones de bits.
    inst_name = tokens[0].lower()
    operands = tokens[1:]

    inst_info = parser.get_instruction_info(inst_name)
    format_type = inst_info['format']
    
    opcode = int(inst_info['opcode'], 2)
    funct3 = int(inst_info['funct3'], 2) if inst_info['funct3'] else 0
    funct7 = int(inst_info['funct7'], 2) if inst_info['funct7'] else 0
    
    params = {
        'opcode': opcode,
        'funct3': funct3,
        'funct7': funct7
    }
    
    if format_type == 'R':
        # R-format: rd, rs1, rs2
        if len(operands) != 3:
            raise ValueError(f"R-format instruction '{inst_name}' expects 3 operands")
        
        params['rd'] = parser.get_register_info(operands[0])
        params['rs1'] = parser.get_register_info(operands[1])
        params['rs2'] = parser.get_register_info(operands[2])

        return encoder.encode_r_format(**params) 
    
    elif format_type == 'I':
        # I-format: rd, rs1, imm
        if len(operands) != 3:
            raise ValueError(f"I-format instruction '{inst_name}' expects 3 operands")
        
        params['rd'] = parser.get_register_info(operands[0])
        params['rs1'] = parser.get_register_info(operands[1])
        params['imm'] = int(operands[2]) if operands[2].lstrip('-').isdigit() else 0
        
        return encoder.encode_i_format(**params)  
    
    elif format_type == 'S':
        # S-format: rs2, offset(rs1) or rs1, rs2, imm
        if len(operands) != 3:
            raise ValueError(f"S-format instruction '{inst_name}' expects 3 operands")
        
        # Check if second operand contains parentheses (offset(rs1) format)
        if '(' in operands[1] and ')' in operands[1]:
            # Format: inst rs2, offset(rs1)
            params['rs2'] = parser.get_register_info(operands[0])
            
            offset_part = operands[1]
            offset_str = offset_part.split('(')[0]
            rs1_str = offset_part.split('(')[1].split(')')[0]
            
            params['rs1'] = parser.get_register_info(rs1_str)
            params['imm'] = int(offset_str) if offset_str and offset_str != '-' else 0
        else:
            # Format: inst rs1, rs2, imm
            params['rs1'] = parser.get_register_info(operands[0])
            params['rs2'] = parser.get_register_info(operands[1])
            params['imm'] = int(operands[2]) if operands[2].lstrip('-').isdigit() else 0

        return encoder.encode_s_format(**params)  
    
    elif format_type == 'B':
        # B-format: rs1, rs2, imm
        if len(operands) != 3:
            raise ValueError(f"B-format instruction '{inst_name}' expects 3 operands")
        
        params['rs1'] = parser.get_register_info(operands[0])
        params['rs2'] = parser.get_register_info(operands[1])
        params['imm'] = int(operands[2]) if operands[2].lstrip('-').isdigit() else 0

        return encoder.encode_b_format(**params)  
    
    else:
        raise ValueError(f"Unsupported format: {format_type}")
    
    raise NotImplementedError("encode_instruction: pendiente de implementar")

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

    print(explain_instruction(instruction, word))

    # No modificar el formato de la siguiente línea: la especificación la
    # requiere, literal, para permitir la validación automática.
    print(f"HEX: 0x{word:08x}")

if __name__ == "__main__":
    main()
