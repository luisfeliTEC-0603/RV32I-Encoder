# RV32I Instruction Encoder

<div align="center">

![RISC‑V Logo](docs/riscv.png)

**Encoding and validation tool for the RISC-V RV32I instruction set architecture**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Arch Linux](https://img.shields.io/badge/Arch_Linux-1793D1?logo=arch-linux&logoColor=white)](https://archlinux.org/)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

</div>

## Overview

Command-line tool that encodes individual RISC-V RV32I assembly instructions into 32-bit binary and hexadecimal, with detailed visual field breakdowns and semantic explanations. Designed for education.

## Supported Instructions

The encoder supports 12 RV32I instructions:
- **R-format**: `add`, `sub`, `and`, `or`
- **I-format**: `addi`, `andi`, `lw`, `lb`
- **S-format**: `sw`, `sb`
- **B-format**: `beq`, `bne`

## Requirements

- Python 3.6 or higher
- No external Python dependencies required

## Installation

1. Clone or download the project
2. Ensure `run.sh` is executable:
   
```bash
chmod +x run.sh
```

## Usage

```bash
./run.sh "<instruction>"
```

### Examples

```bash
./run.sh "add x5, x6, x7"
./run.sh "addi x10, x1, -12"
./run.sh "lw x5, 8(x6)"
./run.sh "sw x8, -4(x2)"
./run.sh "beq x1, x2, 8"
./run.sh "bne x1, x2, .+16"
```

### Supported Immediate Formats

The encoder accepts immediates in multiple formats:
- **Decimal**: `10`, `-12`
- **Hexadecimal**: `0x100`, `-0x100`
- **Binary**: `0b1010`, `-0b1010`
- **PC-relative** (for branches): `.+8`, `.-80`

## Output

The tool outputs:
- A visual breakdown of instruction fields with descriptions in a detailed table
- 32-bit binary representation
- Hexadecimal representation (format: `HEX: 0xXXXXXXXX`)

## Project Structure

```
.
├── run.sh                      # Entry point
├── validate.sh                 # Automatic validation script
├── src/
│   ├── encoder_skeleton.py     # Main encoder logic
│   ├── riscv_encoder.py        # Instruction encoding methods
│   ├── riscv_parser.py         # Tokenization and parsing
│   ├── riscv_inst.json         # Instruction metadata (opcode, funct3, funct7)
│   ├── riscv_reg.json          # Register mappings
│   └── riscv_fmt.json          # Format field definitions
└── tests/
    └── vectores_ejemplo.txt    # Tests to run with the validation script
```

## Validation

To validate against the official RISC-V toolchain -ensure `validate.sh` is executable:

```bash
./validate.sh <test.txt>
```

> [!CAUTION]
>
> **Script Execution Notice**
>
> Both scripts (`./run.sh` and `./validate.sh`) must be executable and are intended to be run from the project root directory.
>
> ```bash
> # Make scripts executable
> chmod +x run.sh validate.sh
>
> # Run from project root
> ./run.sh "add x5, x6, x7"
> ./validate.sh tests/suite_36.txt
> ```
