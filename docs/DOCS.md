# RV32I Instruction Encoder - Technical Documentation

## 1. Architecture Overview

The encoder follows a modular architecture with three main components:

### 1.1 Parser Module (`riscv_parser.py`)

Responsible for:
- Tokenizing assembly instructions
- Loading instruction, register, and format metadata from JSON files
- Validating instruction syntax
- Converting register names to numeric values (0-31)

### 1.2 Encoder Module (`riscv_encoder.py`)

Responsible for:
- Encoding immediate values with sign extension
- Constructing 32-bit instructions for R, I, S, and B formats
- Validating immediate ranges

### 1.3 Main Module (`encoder_skeleton.py`)

Orchestrates the encoding process:
- Parses command-line arguments
- Tokenizes the instruction
- Dispatches to the appropriate encoder
- Displays formatted output with field breakdown

## 2. Supported Instructions

The encoder supports the following RV32I instructions:

| Instruction | Format | Opcode | Funct3 | Funct7 |
|-------------|--------|--------|--------|--------|
| `add`       | R      | 0110011| 000    | 0000000|
| `sub`       | R      | 0110011| 000    | 0100000|
| `and`       | R      | 0110011| 111    | 0000000|
| `or`        | R      | 0110011| 110    | 0000000|
| `addi`      | I      | 0010011| 000    | N/A    |
| `andi`      | I      | 0010011| 111    | N/A    |
| `lw`        | I      | 0000011| 010    | N/A    |
| `lb`        | I      | 0000011| 000    | N/A    |
| `sw`        | S      | 0100011| 010    | N/A    |
| `sb`        | S      | 0100011| 000    | N/A    |
| `beq`       | B      | 1100011| 000    | N/A    |
| `bne`       | B      | 1100011| 001    | N/A    |

### 2.1 Source of Encoding Fields


**The RISC-V Instruction Set Manual, Volume I: Unprivileged Architecture**
The format for each type of instruction:
- Document Version 20260120
- Chapter 1: RV32I Base Integer Instruction Set, Version 2.1
- Available at: https://docs.riscv.org/reference/isa/v20260120/unpriv/rv32.html

**RV32I "Green Card"**
All opcode, funct3, and funct7 values were obtained from:
- Available at: https://notes.cs61c.org/content/misc/rv32i-green-card/

## 3. Code Architecture

### 3.1 Data Flow

```
Instruction String → Tokenization → Format Detection → Operand Parsing → Encoding → Binary Output
```

### 3.2 Format Detection

The parser determines the instruction format from the metadata in `riscv_inst.json`:

```python
inst_info = parser.get_instruction_info(inst_name, False)
format_type = inst_info['format']
```

### 3.5 Operand Parsing

With help of the parser, the skeleton gathers the paramters necesary of the instrucciones.

> [!NOTE]
>
> **Immediate Parsing**
> The `parse_imm()` function in the skeleton supports:
>
> | Format | Example | Result |
> |--------|---------|--------|
> | Decimal | `10`, `-12` | `10`, `-12` |
> | Hexadecimal | `0x100`, `-0x100` | `256`, `-256` |
> | Binary | `0b1010`, `-0b1010` | `10`, `-10` |
> | PC-relative | `.+8`, `.-80` | `8`, `-80` |

### 3.4 Encoding Process

Based on the format the skeleton calls the respective encoder metod to build the instruccion. 

#### R-Format (32 bits)
```
[funct7(7)] [rs2(5)] [rs1(5)] [funct3(3)] [rd(5)] [opcode(7)]
```

#### I-Format (32 bits)
```
[imm(12)] [rs1(5)] [funct3(3)] [rd(5)] [opcode(7)]
```

#### S-Format (32 bits)
```
[imm[11:5](7)] [rs2(5)] [rs1(5)] [funct3(3)] [imm[4:0](5)] [opcode(7)]
```

#### B-Format (32 bits)
```
[imm[12](1)] [imm[10:5](6)] [rs2(5)] [rs1(5)] [funct3(3)] [imm[4:1](4)] [imm[11](1)] [opcode(7)]
```

## 4. Output Examples

### 4.1 R-Format Example: `add x5, x6, x7`

```
[ INSTRUCTION ]
┌────────────────────┐
│   ADD X5, X6, X7   │
└────────────────────┘

ENCODING...
├ TOKENS: ['add', 'x5', 'x6', 'x7']
├ MNEMONIC: add
│	├── OPCODE: 0110011
│	├── FUNCT7: 0000000
│	└── FUNCT3: 000
├ ARG (REG): x5 (00101)
├ ARG (REG): x6 (00110)
├ ARG (REG): x7 (00111)
│
├ FORMAT:R
│	└── Register-to-register operations. All operands are registers, result stored in rd.
└──────────────────────────────────────────────────────────────────────────────────────────────
FIELD              BITS         BINARY           VALUE        DESCRIPTION
───────────────────────────────────────────────────────────────────────────────────────────────
funct7             25-31        0000000          0            Specifies exact operation with funct3. Contains opcode modifiers.
rs2                20-24        00111            7            Source register 2 - second operand.
rs1                15-19        00110            6            Source register 1 - first operand.
funct3             12-14        000              0            Specifies operation variant (ADD, SUB, etc.).
rd                 7-11         00101            5            Destination register - stores the result.
opcode             0-6          0110011          0x33         Operation code - 0x33 for R-format.
┌──────────────────────────────────────────────────────────────────────────────────────────────
└ ENCODING DONE (•ᴗ•)

BINARY: 00000000011100110000001010110011
HEX: 0x007302b3
```

### 4.2 I-Format Example: `addi x10, x1, -12`

```
[ INSTRUCTION ]
┌───────────────────────┐
│   ADDI X10, X1, -12   │
└───────────────────────┘

ENCODING...
├ TOKENS: ['addi', 'x10', 'x1', '-12']
├ MNEMONIC: addi
│	├── OPCODE: 0010011
│	├── FUNCT7: None
│	└── FUNCT3: 000
├ ARG (REG): x10 (01010)
├ ARG (REG): x1 (00001)
├ ARG (IMM): -12 (111111110100)
│
├ FORMAT:I
│	└── Immediate operations. Uses rd = rs1 op imm[11:0].
└──────────────────────────────────────────────────────────────────────────────────────────────
FIELD              BITS         BINARY           VALUE        DESCRIPTION
───────────────────────────────────────────────────────────────────────────────────────────────
imm[11:0]          20-31        111111110100     4084 (0xff4) 12-bit signed immediate value.
rs1                15-19        00001            1            Source register - operand.
funct3             12-14        000              0            Specifies operation variant (addi, andi, etc.).
rd                 7-11         01010            10           Destination register - stores the result.
opcode             0-6          0010011          0x13         Operation code - 0x13, 0x03, 0x67, 0x73, etc.
┌──────────────────────────────────────────────────────────────────────────────────────────────
└ ENCODING DONE (•ᴗ•)

BINARY: 11111111010000001000010100010011
HEX: 0xff408513
```

### 4.3 S-Format Example: `sw x8, -4(x2)`

```
[ INSTRUCTION ]
┌───────────────────┐
│   SW X8, -4(X2)   │
└───────────────────┘

ENCODING...
├ TOKENS: ['sw', 'x8', '-4', 'x2']
├ MNEMONIC: sw
│	├── OPCODE: 0100011
│	├── FUNCT7: None
│	└── FUNCT3: 010
├ ARG (REG): x8 (01000)
├ ARG (REG): x2 (00010)
├ ARG (IMM): -4 (111111111100)
│
├ FORMAT:S
│	└── Store operations. Stores rs2 at address rs1 + imm[11:0].
└──────────────────────────────────────────────────────────────────────────────────────────────
FIELD              BITS         BINARY           VALUE        DESCRIPTION
───────────────────────────────────────────────────────────────────────────────────────────────
imm[11:5]          25-31        1111111          127 (0x7f)   Upper 7 bits of 12-bit signed offset.
rs2                20-24        01000            8            Source register - contains value to store.
rs1                15-19        00010            2            Source register - base address.
funct3             12-14        010              2            Specifies store size: sw=010, sh=001, sb=000.
imm[4:0]           7-11         11100            28 (0x1c)    Lower 5 bits of 12-bit signed offset.
opcode             0-6          0100011          0x23         Operation code - 0x23 for S-format.
┌──────────────────────────────────────────────────────────────────────────────────────────────
└ ENCODING DONE (•ᴗ•)

BINARY: 11111110100000010010111000100011
HEX: 0xfe812e23
```

### 4.4 B-Format Example: `beq x1, x2, 8`

```
[ INSTRUCTION ]
┌───────────────────┐
│   BEQ X1, X2, 8   │
└───────────────────┘

ENCODING...
├ TOKENS: ['beq', 'x1', 'x2', '8']
├ MNEMONIC: beq
│	├── OPCODE: 1100011
│	├── FUNCT7: None
│	└── FUNCT3: 000
├ ARG (REG): x1 (00001)
├ ARG (REG): x2 (00010)
├ ARG (IMM): 8 (0000000001000)
│
├ FORMAT:B
│	└── Branch operations. PC-relative branch if condition (rs1, rs2) is true.
└──────────────────────────────────────────────────────────────────────────────────────────────
FIELD              BITS         BINARY           VALUE        DESCRIPTION
───────────────────────────────────────────────────────────────────────────────────────────────
imm[12]            31           0                0 (0x0)      Bit 12 (sign bit) of branch offset.
imm[10:5]          25-30        000000           0 (0x0)      Bits 10-5 of branch offset.
rs2                20-24        00010            2            Source register 2 - second operand.
rs1                15-19        00001            1            Source register 1 - first operand.
funct3             12-14        000              0            Branch condition: beq=000, bne=001, blt=100, bge=101, etc.
imm[4:1]           8-11         0100             4 (0x4)      Bits 4-1 of branch offset (bit 0 always 0).
imm[11]            7            0                0 (0x0)      Bit 11 of branch offset.
opcode             0-6          1100011          0x63         Operation code - 0x63 for B-format.
┌──────────────────────────────────────────────────────────────────────────────────────────────
└ ENCODING DONE (•ᴗ•)

BINARY: 00000000001000001000010001100011
HEX: 0x00208463
```

## 5. Validation Against Official Toolchain

### 5.1 Toolchain Installation

#### Arch Linux
```bash
sudo pacman -S riscv64-elf-binutils
```

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install gcc-riscv64-unknown-elf
```

#### macOS (Homebrew)
```bash
brew install riscv-tools
```

#### From Source
```bash
git clone https://github.com/riscv-collab/riscv-gnu-toolchain
cd riscv-gnu-toolchain
./configure --prefix=/opt/riscv --with-arch=rv32i
make
```

### 5.2 Validation Results

The validation script (`validate.sh`) compares the encoder output against the official RISC-V toolchain. As argument it requires at least a single text file with the instruccions to compare. 

This project include varios tests in the `test/` directry -which include `vectores_ejemplo.txt` (test file provided by the professor), individual test files for specific instrudctions, and a text file that contains 80+ test cases covering all 12 supported instructions (`suite.txt`).

#### Sample Validation Run (`tests/suite.txt`)

> [!TIP]
>
> **Running Validation**
> To run the validation use one of the follow commands
>
> ```bash
> ./validate.sh tests/suite.txt             # 80+ test for all 12 supported instructions
> ./validate.sh tests/vectores_ejemplo.txt  # test vectores given by the professor
> ./validate.sh tests/<instr>.txt           # individual test for instruction
> ./validate.sh test/*.txt                  # run all tests
> ```

```
────────────────────────────────
Testing: tests/suite.txt
────────────────────────────────

[ PASS ] Line 16: add x5, x6, x7
   My:  0x007302b3
   Off: 0x007302b3

[ PASS ] Line 18: add x0, x1, x2
   My:  0x00208033
   Off: 0x00208033

[ PASS ] Line 20: add x31, x30, x29
   My:  0x01df0fb3
   Off: 0x01df0fb3

[ PASS ] Line 22: add x15, x20, x25
   My:  0x019a07b3
   Off: 0x019a07b3

[ PASS ] Line 24: add x8, x0, x31
   My:  0x01f00433
   Off: 0x01f00433

[ PASS ] Line 28: sub x5, x6, x7
   My:  0x407302b3
   Off: 0x407302b3

[ PASS ] Line 30: sub x0, x1, x2
   My:  0x40208033
   Off: 0x40208033

[ PASS ] Line 32: sub x31, x30, x29
   My:  0x41df0fb3
   Off: 0x41df0fb3

[ PASS ] Line 34: sub x15, x20, x25
   My:  0x419a07b3
   Off: 0x419a07b3

[ PASS ] Line 36: sub x8, x0, x31
   My:  0x41f00433
   Off: 0x41f00433

[ PASS ] Line 40: and x5, x6, x7
   My:  0x007372b3
   Off: 0x007372b3

[ PASS ] Line 42: and x0, x1, x2
   My:  0x0020f033
   Off: 0x0020f033

[ PASS ] Line 44: and x31, x30, x29
   My:  0x01df7fb3
   Off: 0x01df7fb3

[ PASS ] Line 46: and x15, x20, x25
   My:  0x019a77b3
   Off: 0x019a77b3

[ PASS ] Line 48: and x8, x0, x31
   My:  0x01f07433
   Off: 0x01f07433

[ PASS ] Line 52: or x5, x6, x7
   My:  0x007362b3
   Off: 0x007362b3

[ PASS ] Line 54: or x0, x1, x2
   My:  0x0020e033
   Off: 0x0020e033

[ PASS ] Line 56: or x31, x30, x29
   My:  0x01df6fb3
   Off: 0x01df6fb3

[ PASS ] Line 58: or x15, x20, x25
   My:  0x019a67b3
   Off: 0x019a67b3

[ PASS ] Line 60: or x8, x0, x31
   My:  0x01f06433
   Off: 0x01f06433

[ PASS ] Line 69: addi x5, x6, 10
   My:  0x00a30293
   Off: 0x00a30293

[ PASS ] Line 71: addi x5, x6, -12
   My:  0xff430293
   Off: 0xff430293

[ PASS ] Line 73: addi x15, x20, 0x100
   My:  0x100a0793
   Off: 0x100a0793

[ PASS ] Line 75: addi x8, x0, 0b11111111
   My:  0x0ff00413
   Off: 0x0ff00413

[ PASS ] Line 77: addi x5, x6, 2047
   My:  0x7ff30293
   Off: 0x7ff30293

[ PASS ] Line 79: addi x10, x11, -2048
   My:  0x80058513
   Off: 0x80058513

[ PASS ] Line 81: addi x1, x2, -0x200
   My:  0xe0010093
   Off: 0xe0010093

[ PASS ] Line 83: addi x0, x0, 0
   My:  0x00000013
   Off: 0x00000013

[ PASS ] Line 87: andi x5, x6, 10
   My:  0x00a37293
   Off: 0x00a37293

[ PASS ] Line 89: andi x5, x6, -12
   My:  0xff437293
   Off: 0xff437293

[ PASS ] Line 91: andi x15, x20, 0x100
   My:  0x100a7793
   Off: 0x100a7793

[ PASS ] Line 93: andi x8, x0, 0b11111111
   My:  0x0ff07413
   Off: 0x0ff07413

[ PASS ] Line 95: andi x5, x6, 2047
   My:  0x7ff37293
   Off: 0x7ff37293

[ PASS ] Line 97: andi x10, x11, -2048
   My:  0x8005f513
   Off: 0x8005f513

[ PASS ] Line 106: lw x5, 8(x6)
   My:  0x00832283
   Off: 0x00832283

[ PASS ] Line 108: lw x5, -12(x6)
   My:  0xff432283
   Off: 0xff432283

[ PASS ] Line 110: lw x15, 0x100(x20)
   My:  0x100a2783
   Off: 0x100a2783

[ PASS ] Line 112: lw x8, 0b11111111(x0)
   My:  0x0ff02403
   Off: 0x0ff02403

[ PASS ] Line 114: lw x5, 2047(x6)
   My:  0x7ff32283
   Off: 0x7ff32283

[ PASS ] Line 116: lw x10, -2048(x11)
   My:  0x8005a503
   Off: 0x8005a503

[ PASS ] Line 118: lw x0, 0(x0)
   My:  0x00002003
   Off: 0x00002003

[ PASS ] Line 122: lb x5, 8(x6)
   My:  0x00830283
   Off: 0x00830283

[ PASS ] Line 124: lb x5, -12(x6)
   My:  0xff430283
   Off: 0xff430283

[ PASS ] Line 126: lb x15, 0x100(x20)
   My:  0x100a0783
   Off: 0x100a0783

[ PASS ] Line 128: lb x8, 0b11111111(x0)
   My:  0x0ff00403
   Off: 0x0ff00403

[ PASS ] Line 130: lb x5, 2047(x6)
   My:  0x7ff30283
   Off: 0x7ff30283

[ PASS ] Line 132: lb x10, -2048(x11)
   My:  0x80058503
   Off: 0x80058503

[ PASS ] Line 134: lb x0, 0(x0)
   My:  0x00000003
   Off: 0x00000003

[ PASS ] Line 143: sw x8, 8(x2)
   My:  0x00812423
   Off: 0x00812423

[ PASS ] Line 145: sw x8, -12(x2)
   My:  0xfe812a23
   Off: 0xfe812a23

[ PASS ] Line 147: sw x15, 0x100(x20)
   My:  0x10fa2023
   Off: 0x10fa2023

[ PASS ] Line 149: sw x8, 0b11111111(x0)
   My:  0x0e802fa3
   Off: 0x0e802fa3

[ PASS ] Line 151: sw x8, 2047(x2)
   My:  0x7e812fa3
   Off: 0x7e812fa3

[ PASS ] Line 153: sw x10, -2048(x11)
   My:  0x80a5a023
   Off: 0x80a5a023

[ PASS ] Line 155: sw x0, 0(x0)
   My:  0x00002023
   Off: 0x00002023

[ PASS ] Line 159: sb x8, 8(x2)
   My:  0x00810423
   Off: 0x00810423

[ PASS ] Line 161: sb x8, -12(x2)
   My:  0xfe810a23
   Off: 0xfe810a23

[ PASS ] Line 163: sb x15, 0x100(x20)
   My:  0x10fa0023
   Off: 0x10fa0023

[ PASS ] Line 165: sb x8, 0b11111111(x0)
   My:  0x0e800fa3
   Off: 0x0e800fa3

[ PASS ] Line 167: sb x8, 2047(x2)
   My:  0x7e810fa3
   Off: 0x7e810fa3

[ PASS ] Line 169: sb x10, -2048(x11)
   My:  0x80a58023
   Off: 0x80a58023

[ PASS ] Line 171: sb x0, 0(x0)
   My:  0x00000023
   Off: 0x00000023

[ PASS ] Line 180: beq x1, x2, 8
   My:  0x00208463
   Off: 0x00208463

[ PASS ] Line 182: beq x1, x2, -8
   My:  0xfe208ce3
   Off: 0xfe208ce3

[ PASS ] Line 184: beq x1, x2, 0
   My:  0x00208063
   Off: 0x00208063

[ PASS ] Line 186: beq x10, x11, 0x100
   My:  0x10b50063
   Off: 0x10b50063

[ PASS ] Line 188: beq x20, x21, 0b10000
   My:  0x015a0863
   Off: 0x015a0863

[ PASS ] Line 190: beq x1, x2, 4094
   My:  0x7e208fe3
   Off: 0x7e208fe3

[ PASS ] Line 192: beq x1, x2, -4096
   My:  0x80208063
   Off: 0x80208063

[ PASS ] Line 194: beq x30, x4, 60
   My:  0x024f0e63
   Off: 0x024f0e63

[ PASS ] Line 196: beq x0, x1, 16
   My:  0x00100863
   Off: 0x00100863

[ PASS ] Line 200: bne x1, x2, 8
   My:  0x00209463
   Off: 0x00209463

[ PASS ] Line 202: bne x1, x2, -8
   My:  0xfe209ce3
   Off: 0xfe209ce3

[ PASS ] Line 204: bne x1, x2, 0
   My:  0x00209063
   Off: 0x00209063

[ PASS ] Line 206: bne x10, x11, 0x100
   My:  0x10b51063
   Off: 0x10b51063

[ PASS ] Line 208: bne x20, x21, 0b10000
   My:  0x015a1863
   Off: 0x015a1863

[ PASS ] Line 210: bne x1, x2, 4094
   My:  0x7e209fe3
   Off: 0x7e209fe3

[ PASS ] Line 212: bne x1, x2, -4096
   My:  0x80209063
   Off: 0x80209063

[ PASS ] Line 214: bne x30, x4, 60
   My:  0x024f1e63
   Off: 0x024f1e63

[ PASS ] Line 216: bne x0, x1, 16
   My:  0x00101863
   Off: 0x00101863

[ PASS ] Line 224: add x0, x0, x0
   My:  0x00000033
   Off: 0x00000033

[ PASS ] Line 225: sub x0, x0, x0
   My:  0x40000033
   Off: 0x40000033

[ PASS ] Line 226: and x0, x0, x0
   My:  0x00007033
   Off: 0x00007033

[ PASS ] Line 227: or x0, x0, x0
   My:  0x00006033
   Off: 0x00006033

[ PASS ] Line 228: addi x0, x0, 0
   My:  0x00000013
   Off: 0x00000013

[ PASS ] Line 229: andi x0, x0, 0
   My:  0x00007013
   Off: 0x00007013

[ PASS ] Line 230: lw x0, 0(x0)
   My:  0x00002003
   Off: 0x00002003

[ PASS ] Line 231: sw x0, 0(x0)
   My:  0x00002023
   Off: 0x00002023

[ PASS ] Line 232: lb x0, 0(x0)
   My:  0x00000003
   Off: 0x00000003

[ PASS ] Line 233: sb x0, 0(x0)
   My:  0x00000023
   Off: 0x00000023

[ PASS ] Line 234: beq x0, x0, 0
   My:  0x00000063
   Off: 0x00000063

[ PASS ] Line 235: bne x0, x0, 0
   My:  0x00001063
   Off: 0x00001063

[ PASS ] Line 238: add x31, x31, x31
   My:  0x01ff8fb3
   Off: 0x01ff8fb3

[ PASS ] Line 239: addi x31, x31, 2047
   My:  0x7fff8f93
   Off: 0x7fff8f93

[ PASS ] Line 240: lw x31, 2047(x31)
   My:  0x7fffaf83
   Off: 0x7fffaf83

[ PASS ] Line 241: sw x31, 2047(x31)
   My:  0x7fffafa3
   Off: 0x7fffafa3

[ PASS ] Line 242: beq x31, x31, 4094
   My:  0x7fff8fe3
   Off: 0x7fff8fe3

[ PASS ] Line 245: add x0, x0, x0
   My:  0x00000033
   Off: 0x00000033

[ PASS ] Line 246: addi x0, x0, -2048
   My:  0x80000013
   Off: 0x80000013

[ PASS ] Line 247: lw x0, -2048(x0)
   My:  0x80002003
   Off: 0x80002003

[ PASS ] Line 248: sw x0, -2048(x0)
   My:  0x80002023
   Off: 0x80002023

[ PASS ] Line 249: beq x0, x0, -4096
   My:  0x80000063
   Off: 0x80000063

[ PASS ] Line 257: add x5, x20, x15
   My:  0x00fa02b3
   Off: 0x00fa02b3

[ PASS ] Line 258: sub x10, x28, x3
   My:  0x403e0533
   Off: 0x403e0533

[ PASS ] Line 259: and x17, x9, x22
   My:  0x0164f8b3
   Off: 0x0164f8b3

[ PASS ] Line 260: or x12, x25, x30
   My:  0x01ece633
   Off: 0x01ece633

[ PASS ] Line 261: addi x7, x14, 0x1FF
   My:  0x1ff70393
   Off: 0x1ff70393

[ PASS ] Line 262: andi x19, x6, -0x100
   My:  0xf0037993
   Off: 0xf0037993

[ PASS ] Line 263: lw x11, 0x200(x29)
   My:  0x200ea583
   Off: 0x200ea583

[ PASS ] Line 264: lb x23, -0x200(x18)
   My:  0xe0090b83
   Off: 0xe0090b83

[ PASS ] Line 265: sw x27, 0x400(x24)
   My:  0x41bc2023
   Off: 0x41bc2023

[ PASS ] Line 266: sb x13, -0x400(x26)
   My:  0xc0dd0023
   Off: 0xc0dd0023

[ PASS ] Line 267: beq x8, x16, 0x200
   My:  0x21040063
   Off: 0x21040063

[ PASS ] Line 268: bne x31, x5, -0x200
   My:  0xe05f90e3
   Off: 0xe05f90e3

[ PASS ] Line 271: add x7, x8, x9
   My:  0x009403b3
   Off: 0x009403b3

[ PASS ] Line 272: sub x20, x21, x22
   My:  0x416a8a33
   Off: 0x416a8a33

[ PASS ] Line 273: and x1, x2, x3
   My:  0x003170b3
   Off: 0x003170b3

[ PASS ] Line 274: or x4, x5, x6
   My:  0x0062e233
   Off: 0x0062e233

[ PASS ] Line 275: addi x11, x12, 0b11110000
   My:  0x0f060593
   Off: 0x0f060593

[ PASS ] Line 276: andi x13, x14, -0b10000000
   My:  0xf8077693
   Off: 0xf8077693

[ PASS ] Line 277: lw x15, 0b10101010(x16)
   My:  0x0aa82783
   Off: 0x0aa82783

[ PASS ] Line 278: lb x17, -0b11001100(x18)
   My:  0xf3490883
   Off: 0xf3490883

[ PASS ] Line 279: sw x19, 0b11111111(x20)
   My:  0x0f3a2fa3
   Off: 0x0f3a2fa3

[ PASS ] Line 280: sb x21, -0b10001000(x22)
   My:  0xf75b0c23
   Off: 0xf75b0c23

[ PASS ] Line 281: beq x23, x24, 0x400
   My:  0x418b8063
   Off: 0x418b8063

[ PASS ] Line 282: bne x25, x26, -0x400
   My:  0xc1ac90e3
   Off: 0xc1ac90e3

  PASSED: 126
  FAILED: 0

┌────────────────┐
│ FINAL SUMMARY  │
└────────────────┘
Total tests:  126
Passed:       126
Failed:       0

ALL TESTS PASSED! (•ᴗ•)
```

## 6. 
