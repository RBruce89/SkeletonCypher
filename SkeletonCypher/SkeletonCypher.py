import re
import base64

solutions = []

alph = "abcdefghijklmnopqrstuvwxyz"

# Runs every letter in input through all 25 possible rotation cyphers
def rot(message):
    encrypted = message.lower()
    decrypted = ""
    for key in range(1, 26):
        for char in encrypted:
            if not char.isalpha():
                decrypted += char
                continue
            for i in range(len(alph)):
                if char == alph[i]:
                    if i + key >= len(alph):
                        decrypted += alph[i + (key - 26)]
                        break
                    else:
                        decrypted += alph[i + key]
                        break

        solutions.append((decrypted, "rot" + str(key)))
        decrypted = ""

# Converts decimal input to its Ascii and letter translations 
def decimal(message):
    encrypted = message
    decryptedAscii = ""
    decryptedAlph = ""
    tempNum = ""
    for i in range(len(encrypted)):
        if encrypted[i].isdigit():
            tempNum += encrypted[i]
        if not encrypted[i].isdigit() or i == len(encrypted) - 1:
            if tempNum != "":
                tempNum = int(tempNum)
                if tempNum > 255 or tempNum == 0:
                    tempNum = ""
                    continue
                decryptedAscii += chr(tempNum)
                while tempNum > 26:
                    tempNum = tempNum - 26
                decryptedAlph += alph[tempNum - 1]

                tempNum = ""

    solutions.append((decryptedAscii, "Decimal to Ascii"))
    solutions.append((decryptedAlph, "Decimal to Alphabet"))

# Converts binary input to its translation in Ascii, decimal, and letter
def binary(message):
    encrypted = re.sub("[^0-1]", "", message)
    decryptedAscii = ""
    decryptedDecimal = ""
    decryptedAlph = ""
    for i in range(0, len(encrypted), 8):
        tempOctet = encrypted[i:i + 8]
        tempOctet = int(tempOctet, 2)
        decryptedAscii += tempOctet.to_bytes((tempOctet.bit_length() + 7) // 8, 'big').decode(errors='replace')
        if decryptedDecimal == "":
            decryptedDecimal += str(tempOctet)
        else:
            decryptedDecimal += "-" + str(tempOctet)
        if tempOctet == 0:
            continue
        while tempOctet > 26:
            tempOctet = tempOctet - 26
        decryptedAlph += alph[tempOctet - 1]

    solutions.append((decryptedAscii, "Binary to Ascii"))
    solutions.append((decryptedDecimal, "Binary to Decimal"))
    solutions.append((decryptedAlph, "Binary to Alphabet"))

# Converts octal input to its translations in Ascii, decimal, and letter 
def octal(message):
    encrypted = message
    decryptedAscii = ""
    decryptedDecimal = ""
    decryptedAlph = ""
    tempNum = ""
    for i in range(len(encrypted)):
        if re.search('[0-7]', encrypted[i]):
            tempNum += encrypted[i]
        if not re.search('[0-7]', encrypted[i]) or len(tempNum) == 3 or i == len(encrypted) - 1:
            if tempNum != "":
                tempOctet = int(tempNum, 8)
                tempNum = ""
                if tempOctet > 511 or tempOctet == 0:
                    tempOctet = ""
                    continue
                decryptedAscii += chr(tempOctet)
                if decryptedDecimal == "":
                    decryptedDecimal += str(tempOctet)
                else:
                    decryptedDecimal += "-" + str(tempOctet)
                while tempOctet > 26:
                    tempOctet = tempOctet - 26
                decryptedAlph += alph[tempOctet - 1]

    solutions.append((decryptedAscii, "Octal to Ascii"))
    solutions.append((decryptedDecimal, "Octal to Decimal"))
    solutions.append((decryptedAlph, "Octal to Alphabet"))

# Converts hexadecimal input to its translations in Ascii, decimal, and letter
def hexadecimal(message):
    encrypted = re.sub("[^0-9a-fA-F]", "", message)
    decryptedAscii = ""
    decryptedDecimal = ""
    decryptedAlph = ""
    while len(encrypted) % 2 != 0:
        encrypted += "0"
    for i in range(0, len(encrypted), 2):
        tempOctet = encrypted[i:i + 2]
        decryptedAscii += bytes.fromhex(tempOctet).decode(errors='replace')
        tempOctet = int(tempOctet, 16)
        if decryptedDecimal == "":
            decryptedDecimal += str(tempOctet)
        else:
            decryptedDecimal += "-" + str(tempOctet)
        if tempOctet == 0:
            continue
        while tempOctet > 26:
            tempOctet = tempOctet - 26
        decryptedAlph += alph[tempOctet - 1]

    solutions.append((decryptedAscii, "Hexadecimal to Ascii"))
    solutions.append((decryptedDecimal, "Hexadecimal to Decimal"))
    solutions.append((decryptedAlph, "Hexadecimal to Alphabet"))

# Converts base32 input to its Ascii and decimal translations
def base32Conversions(message):
    encrypted = re.sub("[^2-7A-Z=]", "", message)
    decryptedAscii = ""
    decryptedDecimal = ""
    try:
        decryptedAscii = base64.b32decode(message).decode(errors='replace')
        decryptedDecimal = str(int.from_bytes(base64.b32decode(message), 'big'))
    except:
        pass

    solutions.append((decryptedAscii, "Base32 to Ascii"))
    solutions.append((decryptedDecimal, "Base32 to Decimal"))

# Converts base64 input to its Ascii and decimal translations
def base64Conversions(message):
    encrypted = re.sub("[^0-9a-zA-Z+/]", "", message)
    decryptedAscii = ""
    decryptedDecimal = ""
    try:
        decryptedAscii = base64.b64decode(message + "=====").decode(errors='replace')
        decryptedDecimal = str(int.from_bytes(base64.b64decode(message + "====="), 'big'))
    except:
        pass

    solutions.append((decryptedAscii, "Base64 to Ascii"))
    solutions.append((decryptedDecimal, "Base64 to Decimal"))

# print every decrypted solution
def display():
    for entry in range(len(solutions)):
        print (solutions[entry][0] + " - " + solutions[entry][1])
    print ("\n")
    solutions.clear()

# Accepts encrypted message, determines possible encryption types, and runs it through applicable decrypters
def main():
    message = input("Enter encrypted text: ")
    if re.search('[a-zA-Z]', message):
        rot(message)
    if re.search('[0-9]', message):
        decimal(message)
    if not re.search('[2-9a-zA-Z]', message):
        binary(message)
    if not re.search('[8-9a-zA-z]', message):
        octal(message)
    if not re.search('[g-zG-Z]', message):
        hexadecimal(message)
    if re.search('[A-Z2-7]', message):
        base32Conversions(message)
    if re.search('[A-Za-z0-9+/]', message):
        base64Conversions(message)
    
    display()

    main()

main()