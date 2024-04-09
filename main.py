def get_binary_input(prompt):
    while True:
        value = input(prompt)
        if all(c in ['0', '1'] for c in value) and 4 <= len(value) <= 12:
            return value
        else:
            print("Invalid input. Please enter a binary number between 4 and 12 bits long.")

def booth_multiplication(multiplicand, multiplier):
    multiplicand_bin = int(multiplicand, 2)
    multiplier_bin = int(multiplier, 2)
    length = max(len(multiplicand), len(multiplier))
    multiplicand_ext = multiplicand_bin << length
    complement_multiplicand = ((~multiplicand_ext) + 1) & ((1 << (2 * length)) - 1)
    product = 0
    operation_count = 0
    multiplier_ext = multiplier_bin << 1
    
    for i in range(length):
        two_bits = (multiplier_ext >> i) & 3
        if two_bits == 1:
            product += multiplicand_ext
            operation_count += 1
        elif two_bits == 2:
            product += complement_multiplicand
            operation_count += 1
        product >>= 1
    
    product &= (1 << (2 * length)) - 1
    product_bin = bin(product)[2:].zfill(2 * length)
    
    return product_bin, length, operation_count

def run_booth_simulator():
    print("Welcome to the Booth Multiplication Simulator.")
    multiplicand = get_binary_input("Enter the multiplicand (binary, 4-12 bits): ")
    multiplier = get_binary_input("Enter the multiplier (binary, 4-12 bits): ")
    result, iterations, operations = booth_multiplication(multiplicand, multiplier)
    print(f"\nResult: {result} in binary")
    print(f"Number of Iterations: {iterations}")
    print(f"Number of Additions/Subtractions: {operations}")

run_booth_simulator()
