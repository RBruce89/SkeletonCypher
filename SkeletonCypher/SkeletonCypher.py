import sqlite3
import re
import base64
import sys

wordsConnection = sqlite3.connect('words.db')
commonWordsConnection = sqlite3.connect('commonWords.db')

solutions = []

alph = "abcdefghijklmnopqrstuvwxyz"
qwerty = "qwertyuiopasdfghjklzxcvbnm"

# Runs input through all 25 possible Rotation cyphers
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
                        decrypted += alph[adjustment].upper()
                        break
                    else:
                        decrypted += alph[adjustment]
                        break

        originalKey = 26 - key
        solutions.append((decrypted, "Rotation Cipher (key +" + str(originalKey) + ")"))
        decrypted = ""

# Runs input through all 25 possible Qwerty shift ciphers
def qwertyShift(message):
    decrypted = ""
    adjustment = 0
    for key in range(1, 26):
        for char in message:
            if not char.isalpha():
                decrypted += char
                continue
            for i in range(len(qwerty)):
                if char.lower() == qwerty[i]:
                    if i + key >= len(qwerty):
                        adjustment = (i + (key - 26))
                    else:
                        adjustment = (i + key)
                    if char.isupper():
                        decrypted += qwerty[adjustment].upper()
                        break
                    else:
                        decrypted += qwerty[adjustment]
                        break

        originalKey = 26 - key
        solutions.append((decrypted, "Qwerty Shift (key +" + str(originalKey) + ")"))
        decrypted = ""

# Switches message from alphabetical to qwerty order and vice versa
def alphQwertySwitcher(message):
    decryptedQwerty = ""
    decryptedAlph = ""
    for char in message:
        if not char.isalpha():
            decryptedQwerty += char
            decryptedAlph += char
            continue
        for i in range(len(alph)):
            if char.lower() == alph[i]:
                if char.isupper():
                    decryptedQwerty += qwerty[i].upper()
                else:
                    decryptedQwerty += qwerty[i]
                break
        for i in range(len(qwerty)):
            if char.lower() == qwerty[i]:
                if char.isupper():
                    decryptedAlph += alph[i].upper()
                else:
                    decryptedAlph += alph[i]
                break

    solutions.append((decryptedQwerty, "Qwerty to Alphabet"))
    solutions.append((decryptedAlph, "Alphabet to Qwerty"))

# Deciphers Atbash cipher
def atbash(message):
    decrypted = ""
    for char in message:
        if not char.isalpha():
            decrypted += char
            continue
        for i in range(len(alph)):
            if char.lower() == alph[i]:
                if char.isupper():
                    decrypted += chr(90 - i)
                else:
                    decrypted += chr(122 - i)
                break

    solutions.append((decrypted, "Atbash"))

# Deciphers Trithemius cipher
def trithemius(message):
    decrypted = ""
    keyCounter = 0
    pointer = 0
    for char in message:
        if not char.isalpha():
            decrypted += char
            continue
        if keyCounter > 25:
            keyCounter = 0
        for i in range(len(alph)):
            if char.lower() == alph[i]:
                if i - keyCounter < 0:
                    pointer = i - keyCounter + 26
                else:
                    pointer = i - keyCounter
                if char.islower():
                    decrypted += alph[pointer]
                else:
                    decrypted += alph[pointer].upper()
        keyCounter += 1

    solutions.append((decrypted, "Trithemius"))

# Deciphers the Kamasutra cipher
def kamasutra(message):
    letterPairOne = "fymqgvopdjrak"
    letterPairTwo = "cieubxtszwnlh"
    decrypted = ""
    for char in message:
        if not char.isalpha():
            decrypted += char
            continue
        for i in range(len(letterPairOne)):
            if char.lower() == letterPairOne[i]:
                if char.isupper():
                    decrypted += letterPairTwo[i].upper()
                else:
                    decrypted += letterPairTwo[i]
                break
        for i in range(len(letterPairTwo)):
            if char.lower() == letterPairTwo[i]:
                if char.isupper():
                    decrypted += letterPairOne[i].upper()
                else:
                    decrypted += letterPairOne[i]
                break

    solutions.append((decrypted, "Kamasutra"))

# Deciphers Skip ciphers to a key of 6
def skip(message):
    decrypted = ""
    numberOfSkips = 0
    pointer = 0
    while numberOfSkips < 6:
        #If the first character is not skipped
        numberOfSkips += 1
        decrypted = ""
        pointer = 0
        while pointer < len(message):
            decrypted += message[pointer]
            pointer += numberOfSkips + 1

        solutions.append((decrypted, "Skip Cipher (key" + str(numberOfSkips) + ")"))

        #If the first character is skipped
        decrypted = ""
        pointer = 0
        while pointer + numberOfSkips < len(message):
            pointer += numberOfSkips
            decrypted += message[pointer]
            pointer += 1

        solutions.append((decrypted, "Skip Cipher (key" + str(numberOfSkips) + ")"))

# Deciphers Rail Fence ciphers
def railFence(message):
    # Solve Rail Fence with a key of 2
    decrypted = ""
    decryptedList = list(message)
    position = 0
    compensator = 0
    while compensator < len(message):
        decryptedList[compensator] = message[position]
        compensator += 2
        position += 1
    compensator = 1
    while compensator < len(message):
        decryptedList[compensator] = message[position]
        compensator += 2
        position += 1
    decrypted = "".join(decryptedList)

    solutions.append((decrypted, "Rail Fence (key 2)"))

    # Solve Rail Fence with a key of 3
    decrypted = ""
    decryptedList = list(message)
    position = 0
    compensator = 0
    while compensator < len(message):
        decryptedList[compensator] = message[position]
        compensator += 4
        position += 1
    compensator = 1
    while compensator < len(message):
        decryptedList[compensator] = message[position]
        compensator += 2
        position += 1
    compensator = 2
    while compensator < len(message):
        decryptedList[compensator] = message[position]
        compensator += 4
        position += 1
    decrypted = "".join(decryptedList)

    solutions.append((decrypted, "Rail Fence (key 3)"))

    # Solve Rail Fence with a key of 4
    decrypted = ""
    decryptedList = list(message)
    position = 0
    compensator = 0
    down = True
    while compensator < len(message):
        decryptedList[compensator] = message[position]
        compensator += 6
        position += 1
    compensator = 1
    while compensator < len(message):
        decryptedList[compensator] = message[position]
        if down == True:
            compensator += 4
            down = False
        else:
            compensator += 2
            down = True
        position += 1
    compensator = 2
    down = True
    while compensator < len(message):
        decryptedList[compensator] = message[position]
        if down == True:
            compensator += 2
            down = False
        else:
            compensator += 4
            down = True
        position += 1
    compensator = 3
    while compensator < len(message):
        decryptedList[compensator] = message[position]
        compensator += 6
        position += 1
    decrypted = "".join(decryptedList)

    solutions.append((decrypted, "Rail Fence (key 4)"))

    # Solve Rail Fence with a key of 5
    decrypted = ""
    decryptedList = list(message)
    position = 0
    compensator = 0
    down = True
    while compensator < len(message):
        decryptedList[compensator] = message[position]
        compensator += 8
        position += 1
    compensator = 1
    while compensator < len(message):
        decryptedList[compensator] = message[position]
        if down == True:
            compensator += 6
            down = False
        else:
            compensator += 2
            down = True
        position += 1
    compensator = 2
    while compensator < len(message):
        decryptedList[compensator] = message[position]
        compensator += 4
        position += 1
    compensator = 3
    down = True
    while compensator < len(message):
        decryptedList[compensator] = message[position]
        if down == True:
            compensator += 2
            down = False
        else:
            compensator += 6
            down = True
        position += 1
    compensator = 4
    while compensator < len(message):
        decryptedList[compensator] = message[position]
        compensator += 8
        position += 1
    decrypted = "".join(decryptedList)

    solutions.append((decrypted, "Rail Fence (key 5)"))

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

    solutions.append((decrypted, "Morse Code"))

# Deciphers Tap code
def tap(message):
    letters = [['a', 'b', 'c', 'd', 'e'], ['f', 'g', 'h', 'i', 'j'],
               ['l', 'm', 'n', 'o', 'p'], ['q', 'r', 's', 't', 'u'],
               ['v', 'w', 'x', 'y', 'z']]
    # Solves Tap code denoted by numerals
    encrypted = re.sub('[^1-5/]', "", message)
    encrypted = re.sub('/', '//', encrypted)
    decrypted = ""
    for i in range(0, len(encrypted), 2):
        if encrypted[i] == '/' or len(encrypted) > i + 1 and encrypted[i + 1] == '/':
            decrypted += " "
            continue
        if i + 1 < len(encrypted):
            row = int(encrypted[i]) - 1
            column = int(encrypted[i + 1]) - 1
            decrypted += letters[row][column]

    solutions.append((decrypted, "Tap Code"))

    # Solves Tap code denoted by .'s
    encrypted = message
    decrypted = ""
    row = 0
    column= 0
    i = 0
    while i < len(encrypted):
        if encrypted[i] == '/':
            decrypted += " "
            i += 1
            continue
        if encrypted[i] == '.':
            if row == 0:
                row += 1
                while i + 1 < len(encrypted) and encrypted[i + 1] == '.' and row < 5:
                    row += 1
                    i += 1
            else:
                column += 1
                while i + 1 < len(encrypted) and encrypted[i + 1] == '.' and column < 5:
                    column += 1
                    i += 1
                decrypted += letters[row - 1][column - 1]
                row = 0
                column = 0
        i += 1

    solutions.append((decrypted, "Tap Code"))

# Deciphers Baconian ciphers
def bacon(message):
    encrypted = ""
    decrypted = ""
    firstChar = ""
    secondChar = ""
    spaceChar = ""
    # Checks if input matches Bacon cipher format
    for i in range(1, len(message) + 1):
        if firstChar == "":
            firstChar = message[i - 1]
        if secondChar == "" and message[i - 1] != firstChar and i%6 != 0:
            secondChar = message[i - 1]
        if spaceChar == "" and message[i - 1] != firstChar and message[i - 1] != secondChar:
            spaceChar = message[i - 1]
        if message[i - 1] != firstChar and message[i - 1] != secondChar and message[i - 1] != spaceChar:
            return
    if secondChar == "":
        return
    # Standardised input
    encrypted = re.sub(spaceChar, "", message)
    if secondChar != "0":
        encrypted = re.sub(firstChar, "0", encrypted)
        encrypted = re.sub(secondChar, "1", encrypted)
    if secondChar == "0" and firstChar != "1":
        encrypted = re.sub(secondChar, "1", encrypted)
        encrypted = re.sub(firstChar, "0", encrypted)
    # Solves all four possible configurations of cipher
    for i in range(4):
        for j in range(0, len(encrypted), 5):
            tempOctet = encrypted[j:j + 5]
            tempOctet = int(tempOctet, 2)
            if i >= 2:
                if tempOctet > 8:
                    tempOctet += 1
                if tempOctet > 20:
                    tempOctet += 1
            if tempOctet > 25:
                continue
            decrypted += alph[tempOctet]
        if i < 2:
            solutions.append((decrypted, "Bacon Cipher (26 Character)"))
            decrypted = ""
        else:
            solutions.append((decrypted, "Bacon Cipher (24 Character)"))
            decrypted = ""
        encrypted = re.sub("1", "2", encrypted)
        encrypted = re.sub("0", "1", encrypted)
        encrypted = re.sub("2", "0", encrypted)

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

    solutions.append((decryptedAscii, "Ascii to Decimal"))
    solutions.append((decryptedAlph, "Alphabet to Decimal"))

# Converts numbers to their corresponding letters on a T9 number pad
def multiTap(message):
    decrypted = ""
    alphabetPosition = 0
    i = 0
    while i < len(message):
        if not re.search('[2-9]', message[i]):
            i += 1
            continue
        if message[i] == "2":
            alphabetPosition = 0
        if message[i] == "3":
            alphabetPosition = 3
        if message[i] == "4":
            alphabetPosition = 6
        if message[i] == "5":
            alphabetPosition = 9
        if message[i] == "6":
            alphabetPosition = 12
        if message[i] == "7":
            alphabetPosition = 15
        if message[i] == "8":
            alphabetPosition = 19
        if message[i] == "9":
            alphabetPosition = 22
        while i + 1 < len(message) and message[i + 1] == message[i]:
            alphabetPosition += 1
            i += 1
        decrypted += alph[alphabetPosition]
        i += 1

    solutions.append((decrypted, "Multi-Tap Code"))

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

    solutions.append((decryptedAscii, "Ascii to Binary"))
    solutions.append((decryptedDecimal, "Decimal to Binary"))
    solutions.append((decryptedAlph, "Alphabet to Binary"))

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

    solutions.append((decryptedAscii, "Ascii to Octal"))
    solutions.append((decryptedDecimal, "Decimal to Octal"))
    solutions.append((decryptedAlph, "Alphabet to Octal"))

# Converts hexadecimal input to its translations in Ascii, decimal, and letter
def hexadecimal(message):
    encrypted = re.sub("[^0-9a-fA-F]", "", message)
    decryptedAscii = ""
    decryptedDecimal = ""
    decryptedAlph = ""
    while len(encrypted)%2 != 0:
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

    solutions.append((decryptedAscii, "Ascii to Hexadecimal"))
    solutions.append((decryptedDecimal, "Decimal to Hexadecimal"))
    solutions.append((decryptedAlph, "Alphabet to Hexadecimal"))

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

    solutions.append((decryptedAscii, "Ascii to Base32"))
    solutions.append((decryptedDecimal, "Decimal to Base32"))

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

    solutions.append((decryptedAscii, "Ascii to Base64"))
    solutions.append((decryptedDecimal, "Decimal to Base64"))

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

    solutions.append((decryptedAscii, "Ascii to Ascii85"))
    solutions.append((decryptedDecimal, "Decimal to Ascii85"))

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
    # Checks solutions with separated words
    wordsChecked = 0
    wordsConfirmed = 0
    consecutiveInvalidWords = 0
    possibleWord = ""
    if re.search('[^a-zA-Z]', possibleSolution):
        if not re.search('[a-zA-Z]', possibleSolution):
            return False
        for i in range(len(possibleSolution)):
            if consecutiveInvalidWords == 3:
                return False
            if re.search('[\'a-zA-Z]', possibleSolution[i]):
                possibleWord += possibleSolution[i]
            if (re.search('[^\'a-zA-Z]', possibleSolution[i]) or i is len(possibleSolution) - 1) and possibleWord != "":
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
            if len(word[0]) > 2:
                if word[0] in possibleSolution:
                    wordsConfirmed += 1
        if (wordsConfirmed / len(possibleSolution)) >= 0.1:
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
        print("No probable solution found. You can still press \"A\" for the full list of rejected solutions.")
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
    return

# Accepts encrypted message, determines possible encryption types, and runs it through applicable decrypters
def main():
    message = input("Enter encrypted text: ")
    bacon(message)
    if re.search('[a-zA-Z]', message):
        rot(message)
        qwertyShift(message)
        alphQwertySwitcher(message)
        atbash(message)
        trithemius(message)
        kamasutra(message)
        skip(message)
        railFence(message)
    if re.search('[.-]', message):
        morse(message)
    if re.search('[1-5.]', message):
        tap(message)
    if re.search('[0-9]', message):
        decimal(message)
    if re.search('[2-9]', message):
        multiTap(message)
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