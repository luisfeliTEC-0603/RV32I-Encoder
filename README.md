# RV32I Instruction Encoder

<div align="center">

![RISC‑V Logo](docs/riscv.png)

**Encoding and validation tool for the RISC-V RV32I instruction set architecture**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## Overview

...

---

## Official Tool Validation

```
sudo pacman -S riscv64-elf-binutils
```

echo "add x7, x20, x6" > test.s
ls
riscv64-elf-as -march=rv32i test.s -o test.o
riscv64-elf-objdump -d test.o

Required by Specification:

    □ Document code
    □ Validation against official toolchain (36 test cases)
    □ Documentation of opcode/funct3/funct7 sources (RISC-V spec reference)
    □ Complete Markdown documentation:
        □ Architecture overview
        □ Design decisions
        □ Toolchain installation instructions
        □ Tool installation instructions
        □ 4 output examples (R, I, S, B)
        □ Validation comparison table

Functional Improvements:

    □ Better error handling for invalid inputs
    □ Normalize load/store operand order
    □ Edge case testing (x0, min/max values)
    □ vectors_ejemplo.txt included
    □ Clear error messages for unsupported instructions

---

# Kit del proyecto

- `encoder_skeleton.py`: esqueleto en Python con el contrato de entrada/salida
  ya implementado. Complete `encode_instruction` y `explain_instruction`.
  Su uso es opcional; puede implementar la herramienta en otro lenguaje o
  desde cero, siempre que respete el mismo contrato (ver especificación).
- `run.sh`: punto de entrada fijo y obligatorio (`./run.sh "<instruccion>"`).
  Tal como se entrega, invoca `encoder_skeleton.py`. Si cambia de lenguaje o
  de estructura, ajuste este archivo para que siga invocando su solución de
  la misma forma.
- `vectores_ejemplo.txt`: instrucciones de ejemplo junto con su codificación
  correcta, para que pueda comprobar su herramienta desde el primer día.

## Cómo usar `vectores_ejemplo.txt`

El archivo tiene el formato `instruccion ; 0xHEX`, una por línea (las líneas
que empiezan con `#` son comentarios). Por ejemplo:

```
add x7, x20, x6 ; 0x006a03b3
```

Esto significa: al ejecutar `./run.sh "add x7, x20, x6"`, la línea `HEX:`
de su salida debe ser exactamente `HEX: 0x006a03b3`.

Puede comparar manualmente, o escribir un script propio corto que lea el
archivo línea por línea, ejecute `./run.sh` con cada instrucción, y compare
el resultado. Estos vectores son un conjunto de ejemplo para su propia
comprobación; **no sustituyen** los al menos 3 casos de prueba por
instrucción (36 en total) que la especificación pide construir y validar
usted mismo contra el toolchain oficial (`objdump -d`).
