import sqlite3
import re
import base64
import sys

wordsConnection = sqlite3.connect('words.db')
commonWordsConnection = sqlite3.connect('commonWords.db')

solutions = []

alph = "abcdefghijklmnopqrstuvwxyz"
alphUpper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Runs every letter in input through all 25 possible rotation cyphers
def rot(message):
    decrypted = ""
    adjustment = 0
    for key in range(1, 26):
        for char in message:
            if not char.isalpha():
                decrypted += char
                continue
            for i in range(len(alph)):
                if char.lower() == alph[i]:
                    if i + key >= len(alph):
                        adjustment = (i + (key - 26))
                    else:
                        adjustment = (i + key)
                    if char.isupper():
                        decrypted += alphUpper[adjustment]
                        break
                    else:
                        decrypted += alph[adjustment]
                        break


        solutions.append((decrypted, "rot" + str(key)))
        decrypted = ""

# Deciphers Morse code
def morse(message):
    encrypted = re.sub("_", "-", message)
    encrypted = re.sub("\\|", "/", encrypted)
    decrypted = ""
    tempChar = ""
    for i in range(len(encrypted)):
        if encrypted[i] == "." or encrypted[i] == "-":
            tempChar += encrypted[i]
        if encrypted[i] != "-" and encrypted[i] != "."  or i == len(encrypted) - 1:
            if tempChar != "":
                morseSwitcher = {
                ".": "e",
                "-": "t",
                ".-": "a",
                "---": "o",
                "..": "i",
                "-.": "n",
                "...": "s",
                ".-.": "r",
                "....": "h",
                "-..": "d",
                ".-..": "l",
                "..-": "u",
                "-.-.": "c",
                "--": "m",
                "..-.": "f",
                "-.--": "y",
                ".--": "w",
                "--.": "g",
                ".--.": "p",
                "-...": "b",
                "...-": "v",
                "-.-": "k",
                "-..-": "x",
                "--.-": "q",
                ".---": "j",
                "--..": "z",
                "-----": "0",
                ".----": "1",
                "..---": "2",
                "...--": "3",
                "....-": "4",
                ".....": "5",
                "-....": "6",
                "--...": "7",
                "---..": "8",
                "----.": "9",
                ".-.-.-": ".",
                "--..--": ",",
                "..--..": "?",
                }
                decrypted += morseSwitcher.get(tempChar, " ")

                tempChar = ""

            if encrypted[i] == "/":
                decrypted += " "

    solutions.append((decrypted, "Morse code"))

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

# Converts ascii85 input to its Ascii and decimal translations
def ascii85Conversions(message):
    encrypted = re.sub("[^!-u]", "", message)
    decryptedAscii = ""
    decryptedDecimal = ""
    try:
        decryptedAscii = base64.a85decode(message).decode(errors='replace')
        decryptedDecimal = str(int.from_bytes(base64.a85decode(message), 'big'))
    except:
        pass

    solutions.append((decryptedAscii, "Ascii85 to Ascii"))
    solutions.append((decryptedDecimal, "Ascii85 to Decimal"))

# Checks if the given string is a valid word
def wordCheck(possibleWord):
    inputWord = possibleWord.lower()
    wordCur = wordsConnection.cursor()
    wordCur.execute("SELECT * FROM WORDS WHERE FIRSTLETTER=?", (inputWord[:1]))
    words = wordCur.fetchall()

    for word in words:
        if word[0] == inputWord:
            return True
    return False

# Checks if a possible solution contains enough valid words to be the correct solution
def solutionCheck(possibleSolution):
    wordsChecked = 0
    wordsConfirmed = 0
    consecutiveInvalidWords = 0
    possibleWord = ""

    # Checks solutions with separated words
    if re.search('[^a-zA-Z]', possibleSolution):
        if not re.search('[a-zA-Z]', possibleSolution):
            return False
        for i in range(len(possibleSolution)):
            if consecutiveInvalidWords == 3:
                return False
            if re.search('[\'a-zA-Z]', possibleSolution[i]):
                possibleWord += possibleSolution[i]
            if (re.search('[^\'a-zA-Z]', possibleSolution[i]) or i is len(possibleSolution) - 1) and possibleWord is not "":
                if wordCheck(possibleWord):
                    wordsConfirmed += 1
                    consecutiveInvalidWords = 0
                else:
                    consecutiveInvalidWords += 1
                wordsChecked += 1
                possibleWord = ""
        if wordsConfirmed >= 1 and (wordsConfirmed / wordsChecked) >= 0.60:
            return True

    # Checks solutions that are unbroken strings of letters
    else:
        comWordCur = commonWordsConnection.cursor()
        comWordCur.execute("SELECT * FROM WORDS")
        words = comWordCur.fetchall()
        for word in words:
            if word[0] in possibleSolution:
                wordsConfirmed += 1
        if (wordsConfirmed / len(possibleSolution)) >= 0.2:
            return True

    return False

# Prints most likely decrypted solution(s)
def display():
    print ("\n")
    solutionFound = False
    for entry in range(len(solutions)):
        if solutions[entry][0] == "":
            continue
        if re.search('[^\\\.\!\@\#\$\%\&\(\)\-\"\'\:\;\?\,\s\n\w]', solutions[entry][0]):
            continue
        if solutionCheck(solutions[entry][0]):
            print (solutions[entry][0] + " - " + solutions[entry][1])
            solutionFound = True
    if solutionFound == False:
        print("No probable solutions found. You can still press \"A\" for a full list of the rejected solutions.")
    print ("\n")
    optionsTree()

# Presents user with options on how to continue
def optionsTree():
    print ("To show all solutions press: A")
    print ("To decrypt another message press: M")
    print ("To exit press: E")
    choice = input(": ")
    if choice.upper() == "A":
        print ("\n")
        for entry in range(len(solutions)):
            if solutions[entry][0] == "":
                continue
            print (solutions[entry][0] + " - " + solutions[entry][1])
        print ("\n")
        optionsTree()
    if choice.upper() == "M":
        solutions.clear()
        print ("\n")
        main()
    if choice.upper() == "E":
        sys.exit(0)

# Accepts encrypted message, determines possible encryption types, and runs it through applicable decrypters
def main():
    message = input("Enter encrypted text: ")
    if re.search('[a-zA-Z]', message):
        rot(message)
    if re.search('[.-]', message):
        morse(message)
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
    if re.search('[!-u]', message):
        ascii85Conversions(message)
    
    display()

main()