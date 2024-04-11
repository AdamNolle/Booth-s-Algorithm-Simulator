def add(ac, add):
    carry = 0
    newac = ""
    
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

def twoscomp(value):
    newval = ""
    for i in range(len(value)):
        if value[i] == "1":
            newval += "0"
        elif value[i] == "0":
            newval += "1"
    plusone = ""
    for i in range(len(value)):
        if i == (len(value) - 1):
            plusone += "1"
        else:
            plusone += "0"
    return add(newval, plusone)

def shift_right(accumulator, multiplicand, extended_bit):
    length = len(accumulator)
    number = accumulator + multiplicand + extended_bit
    new_number = number[0]
    for i in range(len(number) - 1):
        new_number += number[i]
    extended_bit = new_number[-1]
    accumulator = new_number[0:length]
    multiplicand = new_number[length:length*2]
    # print(new_number)
    return accumulator, multiplicand, extended_bit

def round(multiplier, multiplicand):
    if len(multiplicand) % 2 != 0:
        multiplier = "0" + multiplier
        new_number = multiplicand[0]
        for i in range(len(multiplicand)):
            new_number += multiplicand[i]
    else:
        new_number = multiplicand
    return multiplier, new_number

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
    while shift_count < length:
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

def modified_booths(multiplier, multiplicand):
    shift_count = 0
    accumulator = ""
    extended_bit = "0"
    multiplier, multiplicand = round(multiplier, multiplicand)
    length = len(multiplicand)
    twos_comp_of_multiplier = twoscomp(multiplier)
    # computer would shift left, but we added multiplier to itself
    two_x_multiplier = add(multiplier, multiplier)
    twos_comp_two_x_multiplier = twoscomp(two_x_multiplier)
    additions_count = 0
    subtractions_count = 0
    for i in range(len(multiplicand)):
        accumulator += "0"
    last_digits = multiplicand[-2:] + extended_bit
    while shift_count < length:
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