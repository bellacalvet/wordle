'''
Run this preliminary script to generate the data files in /data
These files are required to compute the optimal next guess in wordle.py
Alternatively you can also download the pre-generated files from the /data folder in my GitHub repository
'''
import sys

#The list of accepted words
with open("valid_words.txt") as file:
	valid_words = [line.rstrip() for line in file]

NUM_WORDS = len(valid_words)

#Create all valid infostrings
infostrings = []
infos = ["⬛","🟨","🟩"]
for info1 in infos:
    for info2 in infos:
        for info3 in infos:
            for info4 in infos:
                for info5 in infos:
                    infostrings.append(info1+info2+info3+info4+info5)

#Returns the list of words left post information gain
#Every (guess, infostring) pair represents a different information gain
#So every (guess, infostring) pair can be associated with a unique sublist of all valid words
def removeWords(words, guess, infostring):
    #infostring is a 5-character string using either ⬛🟨🟩 or _~!
    new_words = []
    #Count how many black, yellow, and green squares we have for each distinct letter in our guess
    num_yellows_and_greens = {}
    letters = []
    for i in range(5):
        if guess[i] not in letters:
            letters.append(guess[i])
    for letter in letters:
        num_yellows_and_greens[letter] = 0
        for j in range(5):
            if guess[j] == letter:
                if infostring[j] == '🟨' or infostring[j] == '~' or infostring[j] == '🟩' or infostring[j] == '!':
                    num_yellows_and_greens[letter] +=1
    #Remove words
    for word in words:
        remove = False
        for i in range(5):
            letter = guess[i]
            num_letter = 0
            for j in range(5):
                if letter == word[j]:
                    num_letter += 1
            info = infostring[i]
            if info == '⬛' or info == '_':
                #Remove word if it contains letter in the same spot
                if word[i] == letter:
                    remove = True
                    break
                #Remove word if it contains letter more times than letter is yellow or green in guess
                if num_letter > (num_yellows_and_greens[letter]):
                    remove = True
                    break
            elif info == '🟨' or info == '~':
				#Remove word if it contains letter in the same spot
                if word[i] == letter:
                    remove = True
                    break
                #Remove word if it contains letter fewer times than letter is yellow or green in guess
                if num_letter < (num_yellows_and_greens[letter]):
                    remove = True
                    break
            elif info == '🟩' or info == '!':
                #Remove word if it doesn't contain letter in the same spot
                if word[i] != letter:
                    remove = True
                    break
        if not remove:
            new_words.append(word)
    return new_words

#Save the associated sublist of possible words to each (valid_word, infostring) pair in separate files in ./data
#Memory space used is approximately 1.1GB
#Note that calculations can take several hours depending on your machine
percent = 0
increment = 100 / NUM_WORDS
for valid_word in valid_words:
    for infostring in infostrings:
        words_left = removeWords(valid_words, valid_word, infostring)
        with open("data/" + valid_word + infostring, "w") as file:
            file.write("\n".join(words_left))
    percent += increment
    tens = int(percent // 10)
    loading_message = "Writing files" + "." * tens + " " * (10 - tens) + str(int(percent)) + "%"
    print(loading_message, end="\r")
print("Writing files..........100%")

print("Data was sucessfully saved and is available for later loading")
print("You can now run the wordle.py script")
print("Happy Wordling!")
sys.exit()
