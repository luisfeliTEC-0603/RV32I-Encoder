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
    tokens[0] = tokens[0].lower()
    operands = tokens[1:]

    inst = parser.get_instruction_info(tokens[0])

    print(f'{tokens[0]} : {inst}')
    print(parser.get_register_info(tokens[1]))
    print(parser.get_format_info(inst["format"]))

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

    print(explain_instruction(instruction, word))

    # No modificar el formato de la siguiente línea: la especificación la
    # requiere, literal, para permitir la validación automática.
    print(f"HEX: 0x{word:08x}")

if __name__ == "__main__":
    main()
