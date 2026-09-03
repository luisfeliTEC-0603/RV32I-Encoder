#!/bin/bash
# validate.sh - Compare encoder with official toolchain

# Check if run.sh exists in parent directory
if [ ! -f "../run.sh" ]; then
    echo "[ ERROR ] ../run.sh not found"
    exit 1
fi

# Check if test files were provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 [file1.txt file2.txt ...]"
    echo "       $0 *.txt"
    exit 1
fi

# Check for required toolchain
if ! command -v riscv64-elf-as &> /dev/null; then
    echo "[ WARNING ] riscv64-elf-as not found in PATH"
    echo "Install the RISC-V toolchain:"
    echo "    Arch: sudo pacman -S riscv64-elf-binutilss"
    echo ""
    echo "Continuing anyway, but tests will likely fail..."
fi

# Variables
total_passed=0
total_failed=0
failed_list=""

# Process each file passed as argument
for file in "$@"; do
    # Check if file exists
    if [ ! -f "$file" ]; then
        echo "[ WARNING ] File '$file' not found, skipping..."
        continue
    fi
    
    echo "────────────────────────────────"
    echo "Testing: $file"
    echo "────────────────────────────────"
    echo ""
    
    passed=0
    failed=0
    line_num=0

    # Read file line by line
    while IFS= read -r line; do
        line_num=$((line_num + 1))
        
        # Skip empty lines
        [ -z "$line" ] && continue
        
        # Skip comment lines (start with '#' or ';') 
        [[ "$line" =~ ^[[:space:]]*[#\;] ]] && continue
        
        # Extract instruction (ignore the ';')
        if [[ "$line" =~ \; ]]; then
            instruction=$(echo "$line" | cut -d';' -f1 | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
        else
            instruction="$line"
        fi
        
        # Remove inline comments
        instruction=$(echo "$instruction" | sed 's/[#;].*$//' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
        
        # Skip instruction fi empty
        [ -z "$instruction" ] && continue
        
        # Get my encoder output
        my_output=$(../run.sh "$instruction" 2>/dev/null | grep "HEX:" | sed 's/.*0x//' | tr '[:upper:]' '[:lower:]')
        [ -z "$my_output" ] && my_output="NO_HEX"
        
        # Get official toolchain output
        temp_s=$(mktemp --suffix=.s)
        temp_o=$(mktemp --suffix=.o)
        
        # Check if it's a branch instruction
        inst_name=$(echo "$instruction" | awk '{print $1}')
        if [[ "$inst_name" == "beq" || "$inst_name" == "bne" ]]; then
            # Extract registers and immediatse
            # Handle different formats: "beq x1, x2, 8" or "beq x1,x2,8"
            rs1=$(echo "$instruction" | awk -F'[, ]+' '{print $2}')
            rs2=$(echo "$instruction" | awk -F'[, ]+' '{print $3}')
            imm=$(echo "$instruction" | awk -F'[, ]+' '{print $4}')
            
            # Clean up: remove any whitespace
            rs1=$(echo "$rs1" | tr -d ' ')
            rs2=$(echo "$rs2" | tr -d ' ')
            imm=$(echo "$imm" | tr -d ' ')
            
            # Convert immediate to .+N or .-N format
            if [[ "$imm" =~ ^-?[0-9]+$ ]]; then
                # It's a plain number, convert to .+N or .-N
                if [[ "$imm" =~ ^- ]]; then
                    # Negative number: .-80
                    imm_clean=$(echo "$imm" | sed 's/^-//')
                    branch_imm=".-$imm_clean"
                else
                    # Positive number: .+80
                    branch_imm=".+$imm"
                fi
            else
                # Already has .+ or .- format, use as is
                branch_imm="$imm"
            fi
            
            # Build the branch instruction for the toolchain
            toolchain_instruction="$inst_name $rs1, $rs2, $branch_imm"
        else
            # Not a branch, use as is
            toolchain_instruction="$instruction"
        fi
        
        # Write to temp file
        echo ".text" > "$temp_s"
        echo "$toolchain_instruction" >> "$temp_s"
        
        # Use toolchain to compile obj
        riscv64-elf-as -march=rv32i -mno-relax "$temp_s" -o "$temp_o" 2>/dev/null
        
        # Disassemble and extract the instruction bytes
        official_output=$(riscv64-elf-objdump -d "$temp_o" 2>/dev/null | \
                         grep -v "file format" | \
                         grep -v "Disassembly" | \
                         grep -v "^$" | \
                         grep -v "\.\.\." | \
                         tail -n +2 | \
                         awk '{print $2}' | \
                         tr -d ' ' | \
                         head -1)
        
        # Remove temporary files
        rm -f "$temp_s" "$temp_o"
        
        [ -z "$official_output" ] && official_output="NO_HEX"
        
        # Compare
        if [ "$my_output" = "$official_output" ] && [ "$my_output" != "NO_HEX" ]; then
            echo "[ PASS ] Line $line_num: $instruction"
            echo "   My:  0x$my_output"
            echo "   Off: 0x$official_output"
            echo ""
            passed=$((passed + 1))
        else
            echo "[ FAIL ] Line $line_num: $instruction"
            echo "   My:  0x$my_output"
            echo "   Off: 0x$official_output"
            echo "   Toolchain instr: $toolchain_instruction"
            echo ""
            failed=$((failed + 1))
            failed_list="$failed_list\n  Line $line_num: $instruction\n    My:  0x$my_output\n    Off: 0x$official_output"
        fi
    done < "$file"
    
    echo "  PASSED: $passed"
    echo "  FAILED: $failed"
    
    total_passed=$((total_passed + passed))
    total_failed=$((total_failed + failed))
done

echo ""
echo "┌────────────────┐"
echo "│ FINAL SUMMARY  │"
echo "└────────────────┘"
echo "Total tests:  $((total_passed + total_failed))"
echo "Passed:       $total_passed"
echo "Failed:       $total_failed"

# Print detailed failed tests if any
if [ $total_failed -eq 0 ]; then
    echo ""
    echo "ALL TESTS PASSED! (•ᴗ•)"
    echo ""
    exit 0
else
    echo ""
    echo "Failed tests:"
    echo -e "$failed_list"
    echo ""
    exit 1
fi
