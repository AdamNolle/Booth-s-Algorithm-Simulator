def booth_multiplication(multiplicand, multiplier):
    # Convert to binary representation
    multiplicand_bin = int(multiplicand, 2)
    multiplier_bin = int(multiplier, 2)
    
    # Length of the numbers
    length = max(len(multiplicand), len(multiplier))
    
    # Extend multiplicand and initialize product
    multiplicand_ext = multiplicand_bin << length  # Shift left to allocate space for addition
    complement_multiplicand = ((~multiplicand_ext) + 1) & ((1 << (2 * length)) - 1)  # 2's complement
    
    product = 0
    operation_count = 0  # Track the number of additions/subtractions
    
    # Append a zero to the multiplier for the algorithm
    multiplier_ext = multiplier_bin << 1
    
    for i in range(length):
        two_bits = (multiplier_ext >> i) & 3  # Extract two bits
        
        if two_bits == 1:  # 01 => Add multiplicand
            product += multiplicand_ext
            operation_count += 1
        elif two_bits == 2:  # 10 => Subtract multiplicand
            product += complement_multiplicand
            operation_count += 1
        
        # Right shift (arithmetic) for next iteration
        product >>= 1
    
    # Adjust product based on the length and sign
    product &= (1 << (2 * length)) - 1  # Mask to the correct length
    
    # Convert back to binary string
    product_bin = bin(product)[2:].zfill(2 * length)
    
    return product_bin, length, operation_count

# Example usage
multiplicand = '1101'  # -3 in decimal
multiplier = '1011'    # -5 in decimal
result, iterations, operations = booth_multiplication(multiplicand, multiplier)
print(f"Result: {result} in binary")
print(f"Number of Iterations: {iterations}")
print(f"Number of Additions/Subtractions: {operations}")
