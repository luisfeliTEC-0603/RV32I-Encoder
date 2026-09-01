class RISCV_Encoder:
    def __init__(self):
        pass
    
    def encode_immediate(self, value: int, bits: int = 12, sign_extend: bool = True) -> int:
        original_value = value
        if sign_extend and value < 0:
            value = (1 << bits) + value
        
        print(f'├ ARG (IMM): {original_value} ({value:>{bits}b})')
        return value & ((1 << bits) - 1)
    
    def encode_r_format(self, rd: int, rs1: int, rs2: int, opcode: int, funct3: int, funct7: int) -> int:
        """
        Encode R-format instruction.
        Format: opcode(7) | rd(5) | funct3(3) | rs1(5) | rs2(5) | funct7(7)
        
        Args:
            rd: Destination register (0-31)
            rs1: Source register 1 (0-31)
            rs2: Source register 2 (0-31)
            opcode: 7-bit opcode
            funct3: 3-bit funct3
            funct7: 7-bit funct7
            
        Returns:
            int: 32-bit encoded instruction
        """
        instruction = 0
        instruction |= (funct7 & 0x7F) << 25   # funct7: bits 25-31
        instruction |= (rs2 & 0x1F) << 20      # rs2: bits 20-24
        instruction |= (rs1 & 0x1F) << 15      # rs1: bits 15-19
        instruction |= (funct3 & 0x7) << 12    # funct3: bits 12-14
        instruction |= (rd & 0x1F) << 7        # rd: bits 7-11
        instruction |= (opcode & 0x7F)         # opcode: bits 0-6
        
        return instruction

    def encode_i_format(self, rd: int, rs1: int, imm: int, opcode: int, funct3: int) -> int:
        """
        Encode I-format instruction.
        Format: opcode(7) | rd(5) | funct3(3) | rs1(5) | imm(12)
        
        Args:
            rd: Destination register (0-31)
            rs1: Source register (0-31)
            imm: 12-bit immediate value
            opcode: 7-bit opcode
            funct3: 3-bit funct3
            
        Returns:
            int: 32-bit encoded instruction
        """
        imm_encoded = self.encode_immediate(imm, 12)
        
        instruction = 0
        instruction |= (imm_encoded & 0xFFF) << 20   # imm: bits 20-31
        instruction |= (rs1 & 0x1F) << 15            # rs1: bits 15-19
        instruction |= (funct3 & 0x7) << 12          # funct3: bits 12-14
        instruction |= (rd & 0x1F) << 7              # rd: bits 7-11
        instruction |= (opcode & 0x7F)               # opcode: bits 0-6
        
        return instruction
    
    def encode_s_format(self, rs1: int, rs2: int, imm: int, opcode: int, funct3: int) -> int:
        """
        Encode S-format instruction.
        Format: opcode(7) | imm[4:0](5) | funct3(3) | rs1(5) | rs2(5) | imm[11:5](7)
        
        Args:
            rs1: Base address register (0-31)
            rs2: Source register to store (0-31)
            imm: 12-bit offset value
            opcode: 7-bit opcode
            funct3: 3-bit funct3
            
        Returns:
            int: 32-bit encoded instruction
        """
        imm_encoded = self.encode_immediate(imm, 12)
        imm_hi = (imm_encoded >> 5) & 0x7F   # bits 11:5
        imm_lo = imm_encoded & 0x1F          # bits 4:0
        
        instruction = 0
        instruction |= (imm_hi & 0x7F) << 25   # imm[11:5]: bits 25-31
        instruction |= (rs2 & 0x1F) << 20      # rs2: bits 20-24
        instruction |= (rs1 & 0x1F) << 15      # rs1: bits 15-19
        instruction |= (funct3 & 0x7) << 12    # funct3: bits 12-14
        instruction |= (imm_lo & 0x1F) << 7    # imm[4:0]: bits 7-11
        instruction |= (opcode & 0x7F)         # opcode: bits 0-6
        
        return instruction

    def encode_b_format(self, rs1: int, rs2: int, imm: int, opcode: int, funct3: int) -> int:
        """
        Encode B-format instruction.
        Format: opcode(7) | imm[11](1) | imm[4:1](4) | funct3(3) | rs1(5) | rs2(5) | imm[10:5](6) | imm[12](1)
        
        Args:
            rs1: Source register 1 (0-31)
            rs2: Source register 2 (0-31)
            imm: 13-bit branch offset
            opcode: 7-bit opcode
            funct3: 3-bit funct3
            
        Returns:
            int: 32-bit encoded instruction
        """
        imm_encoded = self.encode_immediate(imm, 13)
        
        # Split immediate for B-format
        imm_12 = (imm_encoded >> 12) & 0x1     # bit 12
        imm_11 = (imm_encoded >> 11) & 0x1     # bit 11
        imm_10_5 = (imm_encoded >> 5) & 0x3F   # bits 10:5
        imm_4_1 = (imm_encoded >> 1) & 0xF     # bits 4:1
        
        instruction = 0
        instruction |= (imm_12 & 0x1) << 31        # imm[12]: bit 31
        instruction |= (imm_10_5 & 0x3F) << 25     # imm[10:5]: bits 25-30
        instruction |= (rs2 & 0x1F) << 20          # rs2: bits 20-24
        instruction |= (rs1 & 0x1F) << 15          # rs1: bits 15-19
        instruction |= (funct3 & 0x7) << 12        # funct3: bits 12-14
        instruction |= (imm_4_1 & 0xF) << 8        # imm[4:1]: bits 8-11
        instruction |= (imm_11 & 0x1) << 7         # imm[11]: bit 7
        instruction |= (opcode & 0x7F)             # opcode: bits 0-6
        
        return instruction
