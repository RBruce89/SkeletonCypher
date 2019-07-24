import re

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

        print (decrypted + " - rot " + str(key))
        decrypted = ""

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

    print (decryptedAscii + " - Binary to Ascii")
    print (decryptedDecimal + " - Binary to Decimal")
    print (decryptedAlph + " - Binary to Alphabet")

# Accepts encrypted message, determines possible encryption types, and runs it through applicable decrypters
def main():
    message = input("Enter encrypted text: ")
    if re.search('[a-zA-Z]', message):
        rot(message)
    if not re.search('[2-9a-zA-Z]', message):
        binary(message)
    main()

main()