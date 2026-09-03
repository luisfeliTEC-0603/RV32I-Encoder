#!/bin/bash
# Simple validation script

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

# Test cases - you can modify these
TEST_CASES=(
    "add x5, x6, x7"
    "addi x10, x1, -12"
    "lw x5, 8(x6)"
    "sw x8, -4(x2)"
    "beq x1, x2, .+8"
    "sub x5, x6, x7"
    "and x5, x6, x7"
    "or x5, x6, x7"
    "andi x5, x6, 10"
    "lb x5, 8(x6)"
    "sb x8, -4(x2)"
    "bne x1, x2, .+8"
)

echo "=========================================="
echo "RISC-V Encoder Validation"
echo "=========================================="
echo ""

total=0
passed=0
failed=0

for instr in "${TEST_CASES[@]}"; do
    total=$((total + 1))
    
    # Get my encoder output
    my_output=$(../run.sh "$instr" 2>/dev/null | grep "HEX:" | awk '{print $2}')
    
    # Get official toolchain output
    echo ".text" > test.s
    echo "$instr" >> test.s
    riscv64-elf-as -march=rv32i test.s -o test.o 2>/dev/null
    official_output=$(riscv64-elf-objdump -d test.o 2>/dev/null | \
                     grep -v "file format" | \
                     grep -v "Disassembly" | \
                     grep -v "^$" | \
                     tail -n +2 | \
                     awk '{print $2}' | \
                     tr -d ' ')
    
    # Pad official output to 8 chars
    if [ -n "$official_output" ]; then
        official_output=$(printf "0x%08s" "$official_output" | tr ' ' '0')
    else
        official_output="ERROR"
    fi
    
    # Compare
    if [ "$my_output" = "$official_output" ]; then
        echo -e "${GREEN}✅ PASS${NC}: $instr"
        echo "   My: $my_output"
        echo "   Official: $official_output"
        passed=$((passed + 1))
    else
        echo -e "${RED}❌ FAIL${NC}: $instr"
        echo "   My: $my_output"
        echo "   Official: $official_output"
        failed=$((failed + 1))
    fi
    echo ""
done

# Clean up
rm -f test.s test.o

echo "=========================================="
echo "RESULTS: $passed/$total passed"
if [ $failed -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
else
    echo -e "${RED}❌ $failed tests failed${NC}"
fi
echo "=========================================="
