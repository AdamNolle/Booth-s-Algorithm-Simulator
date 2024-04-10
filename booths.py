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

# print(add("011011", "000011"))

# print(twoscomp("0001"))