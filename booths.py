# Definition: This function takes two binary numbers, adds them together, and returns the result.
# Input: Two strings of 0's and 1's (binary).
# Output: One string of 0's and 1's (binary).
def add(ac, add):
    carry = 0
    newac = ""
    
    # Loops through the two numbers and performs the addition digit by digit
    for i in range(len(ac)-1, -1, -1):
        if (int(ac[i]) + int(add[i]) + carry) == 0:
            newac = "0" + newac
            carry = 0
        elif (int(ac[i]) + int(add[i]) + carry) == 1:
            newac = "1" + newac
            carry = 0
        elif (int(ac[i]) + int(add[i]) + carry) == 2:
            newac = "0" + newac
            carry = 1
        elif (int(ac[i]) + int(add[i]) + carry) == 3:
            newac = "1" + newac
            carry = 1
    return newac

# Definition: This function takes a binary number, finds the two's complement, and returns the result.
# Input: One string of 0's and 1's (binary).
# Output: One of 0's and 1's (binary).
def twoscomp(value):
    newval = ""
    # Loops through the digits of the number and flips each digit (0 to 1 or 1 to 0)
    # Result of this loop is 1's complement of number
    for i in range(len(value)):
        if value[i] == "1":
            newval += "0"
        elif value[i] == "0":
            newval += "1"
    plusone = ""
    # Adds one to the result of the previous loop to complete 2's complement calculation
    for i in range(len(value)):
        if i == (len(value) - 1):
            plusone += "1"
        else:
            plusone += "0"
    return add(newval, plusone)

# Definition: This function takes in the accumulator, multuplicand, and extended bit from the problem and performs an arithmetic shift right.
# Input: Three strings of 0's and 1's (binary).
# Output: Three strings of 0's and 1's (binary).
def shift_right(accumulator, multiplier, extended_bit):
    length = len(accumulator)
    number = accumulator + multiplier + extended_bit
    # Duplicates first digit to start off arithmetic shift right
    new_number = number[0]
    # Adds rest of digits except for last digit to complete arithmetic shift right
    for i in range(len(number) - 1):
        new_number += number[i]
    extended_bit = new_number[-1]
    accumulator = new_number[0:length]
    multiplier = new_number[length:length*2]
    # print(new_number)
    return accumulator, multiplier, extended_bit

def times_two(value):
    new_number = "0"
    for i in range(len(value)-1, 0, -1):
        new_number = value[i] + new_number
    return new_number

# Definition: this function takes the multiplicand and multiplier and, if there are an odd number of digits, it rounds the number of digits to the nearest even number.
# Input: Two strings of 0's and 1's (binary).
# Output: Two strings of 0's and 1's (binary).
def round(multiplicand, multiplier):
    # If statement checks if number of digits is even or odd
    if len(multiplier) % 2 != 0:
        # Padding of multiplicand
        new_multiplicand = multiplicand[0]
        for i in range(len(multiplicand)):
            new_multiplicand += multiplicand[i]
        # Padding of multiplier
        new_multiplier = multiplier[0]
        for i in range(len(multiplier)):
            new_multiplier += multiplier[i]
    else:
        new_multiplier = multiplier
        new_multiplicand = multiplicand
    return new_multiplicand, new_multiplier

# Definition: This Function performs the Booth's algorithm to find the result of the multiplication of two binary numbers.
# Input: Two strings of 0's and 1's (binary) and one integer.
# Output: Three integers and two strings of 0's and 1's (binary).
def booths(multiplicand, multiplier, length):
    shift_count = 0 
    accumulator = ""
    extended_bit = "0"
    twos_comp_of_multiplicand = twoscomp(multiplicand)
    additions_count = 0
    subtractions_count = 0
    for i in range(len(multiplicand)):
        accumulator += "0"
    last_digits = multiplier[-1:] + extended_bit
    # Performs the algorithms until number of shifts equals the number of digits of multiplier
    while shift_count < length:
        # If statement checks for each scenario of last two digits to perform appropriate steps for calculation
        if last_digits == "00" or last_digits == "11":
            accumulator, multiplier, extended_bit = shift_right(accumulator, multiplier, extended_bit)
            shift_count += 1
            step = "Last two digits are " + last_digits + " so shift right."
        elif last_digits == "01":
            accumulator = add(accumulator, multiplicand)
            additions_count += 1
            accumulator, multiplier, extended_bit = shift_right(accumulator, multiplier, extended_bit)
            shift_count += 1
            step = "Last two digits are " + last_digits + " so add multiplicand and shift right."
        elif last_digits == "10":
            accumulator = add(accumulator, twos_comp_of_multiplicand)
            subtractions_count += 1
            accumulator, multiplier, extended_bit = shift_right(accumulator, multiplier, extended_bit)
            shift_count += 1
            step = "Last two digits are " + last_digits + " so subtract multiplicand and shift right."
        last_digits = multiplier[-1:] + extended_bit
        print(accumulator, multiplier, extended_bit, "->", step)
    return shift_count, additions_count, subtractions_count, accumulator, multiplier

# Definition: This Function performs the modified Booth's algorithm (group of 3 digits) to find the result of the multiplication of two binary numbers.
# Input: Two strings of 0's and 1's (binary).
# Output: One float, two integers, and two strings of 0's and 1's (binary).
def modified_booths(multiplicand, multiplier):
    shift_count = 0
    accumulator = ""
    extended_bit = "0"
    multiplicand, multiplier = round(multiplicand, multiplier)
    length = len(multiplier)
    twos_comp_of_multiplicand = twoscomp(multiplicand)
    # computer would shift left, but we added multiplicand to itself to make code simpler
    two_x_multiplicand = times_two(multiplicand)
    twos_comp_two_x_multiplicand = twoscomp(two_x_multiplicand)
    additions_count = 0
    subtractions_count = 0
    for i in range(len(multiplier)):
        accumulator += "0"
    last_digits = multiplier[-2:] + extended_bit
    # Performs the algorithms until number of shifts equals half number of digits of multiplier (since you always shift right twice for Modified Booth's)
    while shift_count < length:
        # If statement checks for each scenario of last two digits to perform appropriate steps for calculation
        if last_digits == "000" or last_digits == "111":
            accumulator, multiplier, extended_bit = shift_right(accumulator, multiplier, extended_bit)
            accumulator, multiplier, extended_bit = shift_right(accumulator, multiplier, extended_bit)
            shift_count += 2
            step = "Last two digits are " + last_digits + " so shift right twice."
        elif last_digits == "001" or last_digits == "010":
            accumulator = add(accumulator, multiplicand)
            additions_count += 1
            accumulator, multiplier, extended_bit = shift_right(accumulator, multiplier, extended_bit)
            accumulator, multiplier, extended_bit = shift_right(accumulator, multiplier, extended_bit)
            shift_count += 2
            step = "Last two digits are " + last_digits + " so add multiplicand and shift right twice."
        elif last_digits == "101" or last_digits == "110":
            accumulator = add(accumulator, twos_comp_of_multiplicand)
            subtractions_count += 1
            accumulator, multiplier, extended_bit = shift_right(accumulator, multiplier, extended_bit)
            accumulator, multiplier, extended_bit = shift_right(accumulator, multiplier, extended_bit)
            shift_count += 2
            step = "Last two digits are " + last_digits + " so subtract multiplicand and shift right twice."
        elif last_digits == "011":
            accumulator = add(accumulator, two_x_multiplicand)
            additions_count += 1
            accumulator, multiplier, extended_bit = shift_right(accumulator, multiplier, extended_bit)
            accumulator, multiplier, extended_bit = shift_right(accumulator, multiplier, extended_bit)
            shift_count += 2
            step = "Last two digits are " + last_digits + " so add 2*multiplicand and shift right twice."
        elif last_digits == "100":
            accumulator = add(accumulator, twos_comp_two_x_multiplicand)
            subtractions_count += 1
            accumulator, multiplier, extended_bit = shift_right(accumulator, multiplier, extended_bit)
            accumulator, multiplier, extended_bit = shift_right(accumulator, multiplier, extended_bit)
            shift_count += 2
            step = "Last two digits are " + last_digits + " so subtract 2*multiplicand and shift right twice."
        last_digits = multiplier[-2:] + extended_bit
        print(accumulator, multiplier, extended_bit, "->", step)

    return shift_count/2, additions_count, subtractions_count, accumulator, multiplier

# Definition: Pads the result to make the number of digits a multiple of 4 so it can be converted to hex.
# Input: Accumulator and multiplier value as string of 0's and 1's (binary).
# Output: String of 0's and 1's (binary).
def conversion_prep(value1, value2):
    done = False
    value = value1 + value2
    while done == False:
        # Checks if number of digits is a multiple of 4
        if len(value) % 4 != 0:
            # Pads value if number of digits is not a multiple of 4
            value = value[0] + value
        else:
            done = True
    return value

# Definition: Main function that controls the flow of the program.
# input: None
# Output: None
def main():
    multiplicand = input("Please enter the multiplicand: ")
    multiplier = input("Please enter the multiplier: ")
    print("-----------------------------")
    length = len(multiplicand)
    print("Booth's Algorithm Steps:")
    booth_count, booths_additions, booths_subtractions, booth1, booth2 = booths(multiplicand, multiplier, length)
    print("-----------------------------")
    print("Modified Booth's Algorithm Steps:")
    mbooth_count, mbooths_additions, mbooths_subtractions, mbooth1, mbooth2 = modified_booths(multiplicand, multiplier)
    print("-----------------------------")
    print("Booth's: ", booth1, booth2)
    booth_hex = conversion_prep(booth1, booth2)
    print("Booth's value in hex: ", format(int(booth_hex, 2), 'x'))
    print("Number of iterations for Booth's Algorithm: ", booth_count)
    print("Number of additions for Booth's Algorithm: ", booths_additions)
    print("Number of subtractions for Booth's Algorithm: ", booths_subtractions)
    print("-----------------------------")
    print("Modified Booth's: ", mbooth1, mbooth2)
    mbooth_hex = conversion_prep(mbooth1, mbooth2)
    print("Modified Booth's value in hex: ", format(int(mbooth_hex, 2), 'x'))
    print("Number of iterations for Modified Booth's Algorithm: ", int(mbooth_count))
    print("Number of additions for Modified Booth's Algorithm: ", mbooths_additions)
    print("Number of subtractions for Modified Booth's Algorithm: ", mbooths_subtractions)

if __name__ == "__main__":
    main()