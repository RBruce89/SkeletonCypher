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

# Accepts encrypted message, determines possible encryption types, and runs it through applicable decrypters
def main():
    message = input("Enter encrypted text: ")
    if re.search('[a-zA-Z]', message):
        rot(message)
    main()

main()