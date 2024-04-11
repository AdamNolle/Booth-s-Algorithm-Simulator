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
def shift_right(accumulator, multiplicand, extended_bit):
    length = len(accumulator)
    number = accumulator + multiplicand + extended_bit
    # Duplicates first digit to start off arithmetic shift right
    new_number = number[0]
    # Adds rest of digits except for last digit to complete arithmetic shift right
    for i in range(len(number) - 1):
        new_number += number[i]
    extended_bit = new_number[-1]
    accumulator = new_number[0:length]
    multiplicand = new_number[length:length*2]
    # print(new_number)
    return accumulator, multiplicand, extended_bit

# Definition: this function takes the multiplier and multiplicand and, if there are an odd number of digits, it rounds the number of digits to the nearest even number.
# Input: Two strings of 0's and 1's (binary).
# Output: Two strings of 0's and 1's (binary).
def round(multiplier, multiplicand):
    # If statement checks if number of digits is even or odd
    if len(multiplicand) % 2 != 0:
        # Padding of multiplier
        multiplier = "0" + multiplier
        # Padding of multiplicand
        new_number = multiplicand[0]
        for i in range(len(multiplicand)):
            new_number += multiplicand[i]
    else:
        new_number = multiplicand
    return multiplier, new_number

# Definition: This Function performs the Booth's algorithm to find the result of the multiplication of two binary numbers.
# Input: Two strings of 0's and 1's (binary) and one integer.
# Output: Three integers and two strings of 0's and 1's (binary).
def booths(multiplier, multiplicand, length):
    shift_count = 0 
    accumulator = ""
    extended_bit = "0"
    twos_comp_of_multiplier = twoscomp(multiplier)
    additions_count = 0
    subtractions_count = 0
    for i in range(len(multiplier)):
        accumulator += "0"
    last_digits = multiplicand[-1:] + extended_bit
    # Performs the algorithms until number of shifts equals the number of digits of multiplicand
    while shift_count < length:
        # If statement checks for each scenario of last two digits to perform appropriate steps for calculation
        if last_digits == "00" or last_digits == "11":
            accumulator, multiplicand, extended_bit = shift_right(accumulator, multiplicand, extended_bit)
            shift_count += 1
            step = "Last two digits are " + last_digits + " so shift right."
        elif last_digits == "01":
            accumulator = add(accumulator, multiplier)
            additions_count += 1
            accumulator, multiplicand, extended_bit = shift_right(accumulator, multiplicand, extended_bit)
            shift_count += 1
            step = "Last two digits are " + last_digits + " so add multiplicand and shift right."
        elif last_digits == "10":
            accumulator = add(accumulator, twos_comp_of_multiplier)
            subtractions_count += 1
            accumulator, multiplicand, extended_bit = shift_right(accumulator, multiplicand, extended_bit)
            shift_count += 1
            step = "Last two digits are " + last_digits + " so subtract multiplicand and shift right."
        last_digits = multiplicand[-1:] + extended_bit
        print(accumulator, multiplicand, extended_bit, "->", step)
    return shift_count, additions_count, subtractions_count, accumulator, multiplicand

# Definition: This Function performs the modified Booth's algorithm (group of 3 digits) to find the result of the multiplication of two binary numbers.
# Input: Two strings of 0's and 1's (binary).
# Output: One float, two integers, and two strings of 0's and 1's (binary).
def modified_booths(multiplier, multiplicand):
    shift_count = 0
    accumulator = ""
    extended_bit = "0"
    multiplier, multiplicand = round(multiplier, multiplicand)
    length = len(multiplicand)
    twos_comp_of_multiplier = twoscomp(multiplier)
    # computer would shift left, but we added multiplier to itself to make code simpler
    two_x_multiplier = add(multiplier, multiplier)
    twos_comp_two_x_multiplier = twoscomp(two_x_multiplier)
    additions_count = 0
    subtractions_count = 0
    for i in range(len(multiplicand)):
        accumulator += "0"
    last_digits = multiplicand[-2:] + extended_bit
    # Performs the algorithms until number of shifts equals half number of digits of multiplicand (since you always shift right twice for Modified Booth's)
    while shift_count < length:
        # If statement checks for each scenario of last two digits to perform appropriate steps for calculation
        if last_digits == "000" or last_digits == "111":
            accumulator, multiplicand, extended_bit = shift_right(accumulator, multiplicand, extended_bit)
            accumulator, multiplicand, extended_bit = shift_right(accumulator, multiplicand, extended_bit)
            shift_count += 2
            step = "Last two digits are " + last_digits + " so shift right twice."
        elif last_digits == "001" or last_digits == "010":
            accumulator = add(accumulator, multiplier)
            additions_count += 1
            accumulator, multiplicand, extended_bit = shift_right(accumulator, multiplicand, extended_bit)
            accumulator, multiplicand, extended_bit = shift_right(accumulator, multiplicand, extended_bit)
            shift_count += 2
            step = "Last two digits are " + last_digits + " so add multiplicand and shift right twice."
        elif last_digits == "101" or last_digits == "110":
            accumulator = add(accumulator, twos_comp_of_multiplier)
            subtractions_count += 1
            accumulator, multiplicand, extended_bit = shift_right(accumulator, multiplicand, extended_bit)
            accumulator, multiplicand, extended_bit = shift_right(accumulator, multiplicand, extended_bit)
            shift_count += 2
            step = "Last two digits are " + last_digits + " so subtract multiplicand and shift right twice."
        elif last_digits == "011":
            accumulator = add(accumulator, two_x_multiplier)
            additions_count += 1
            accumulator, multiplicand, extended_bit = shift_right(accumulator, multiplicand, extended_bit)
            accumulator, multiplicand, extended_bit = shift_right(accumulator, multiplicand, extended_bit)
            shift_count += 2
            step = "Last two digits are " + last_digits + " so add 2*multiplicand and shift right twice."
        elif last_digits == "100":
            accumulator = add(accumulator, twos_comp_two_x_multiplier)
            subtractions_count += 1
            accumulator, multiplicand, extended_bit = shift_right(accumulator, multiplicand, extended_bit)
            accumulator, multiplicand, extended_bit = shift_right(accumulator, multiplicand, extended_bit)
            shift_count += 2
            step = "Last two digits are " + last_digits + " so subtract 2*multiplicand and shift right twice."
        last_digits = multiplicand[-2:] + extended_bit
        print(accumulator, multiplicand, extended_bit, "->", step)

    return shift_count/2, additions_count, subtractions_count, accumulator, multiplicand

# Definition: Main function that controls the flow of the program.
# input: None
# Output: None
def main():
    multiplier = input("Please enter the Multiplier: ")
    multiplicand = input("Please enter the Multiplicand: ")
    print("-----------------------------")
    length = len(multiplier)
    print("Booth's Algorithm Steps:")
    booth_count, booths_additions, booths_subtractions, booth1, booth2 = booths(multiplier, multiplicand, length)
    print("-----------------------------")
    print("Modified Booth's Algorithm Steps:")
    mbooth_count, mbooths_additions, mbooths_subtractions, mbooth1, mbooth2 = modified_booths(multiplier, multiplicand)
    print("-----------------------------")
    print("Booth's: ", booth1, booth2)
    print("Booth's value in hex: ", format(int(booth1 + booth2, 2), 'x'))
    print("Number of iterations for Booth's Algorithm: ", booth_count)
    print("Number of additions for Booth's Algorithm: ", booths_additions)
    print("Number of subtractions for Booth's Algorithm: ", booths_subtractions)
    print("-----------------------------")
    print("Modified Booth's: ", mbooth1, mbooth2)
    print("Modified Booth's value in hex: ", format(int(mbooth1 + mbooth2, 2), 'x'))
    print("Number of iterations for Modified Booth's Algorithm: ", int(mbooth_count))
    print("Number of additions for Modified Booth's Algorithm: ", mbooths_additions)
    print("Number of subtractions for Modified Booth's Algorithm: ", mbooths_subtractions)

if __name__ == "__main__":
    main()