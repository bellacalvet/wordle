'''
A simple Python script that plays Wordle and wins virtually every single game
(Make sure to run generate_data.py before running this if you don't already have your own data files)
'''
import re
import copy
import math
import sys

#The list of all words accepted by Wordle's spellcheck
with open("valid_words.txt") as file:
	valid_words = [line.rstrip() for line in file]

#A pruned version made up only of commonly used words
with open("commonly_used_words.txt") as file:
    commonly_used_words = [line.rstrip() for line in file]

#Create all 243 (3**5) valid infostrings
infostrings = []
infos = ["⬛","🟨","🟩"]
for info1 in infos:
    for info2 in infos:
        for info3 in infos:
            for info4 in infos:
                for info5 in infos:
                    infostrings.append(info1+info2+info3+info4+info5)

#Some globals
dict = {}
NUM_WORDS = len(valid_words)
NUM_INFOSTRINGS = len(infostrings)
NUM_DICT_ENTRIES = NUM_WORDS * NUM_INFOSTRINGS
NUM_ROUNDS = 6

#Store pre-computed word data into data structure
def load_data():
    percent = 0
    increment = 100 / NUM_WORDS
    for valid_word in valid_words:
        for infostring in infostrings:
            try:
                with open("data/" + valid_word + infostring) as file:
                    dict[(valid_word, infostring)] = [line.rstrip() for line in file]
            except FileNotFoundError:
                print("The data file data/" + valid_word + infostring + " cannot be found")
                print("Make sure to run generate_data.py once before you play")
                sys.exit()
        percent += increment
        tens = int(percent // 10)
        loading_message = "Loading files" + "." * tens + " " * (10 - tens) + str(int(percent)) + "%"
        print(loading_message, end="\r")
    print("Loading files..........100%")

#Determine if the infostring for a given word is unique or if it's the same as a previous infostring
def notRedundant(word, infostring):
    letters = {}
    for i in range(5):
        if word[i] not in letters:
            letters[word[i]] = [i]
        else:
            letters[word[i]].append(i)
    for letter, indices in letters.items():
        if len(indices) > 1:
            blackSquareSeen = False
            for index in indices:
                #Infostrings are identical if for a duplicate letter we have the same number of yellow squares
                if infostring[index] == "⬛":
                    blackSquareSeen = True
                if infostring[index] == "🟨" and blackSquareSeen:
                    return False
    return True

#Removes words based on one round's worth of information gain
def removeWords(data, guess, infostring, round):
    if round == 0:
        return copy.deepcopy(dict[(guess, infostring)])
    else:
        return copy.deepcopy(data[(guess, infostring)])

#Generate next guess
def generateGuess(words_left, data, round):
    #Calculate entropy for all valid words and pick the word with the highest entropy
    entropy = {}
    for valid_word in valid_words:
        entropy[valid_word] = 0
    percent = 0
    increment = 100 / NUM_DICT_ENTRIES
    if round == 0:
        for (valid_word, infostring), words in dict.items():
            if notRedundant(valid_word, infostring):
                probability = len(dict[(valid_word, infostring)]) / len(words_left)
                if probability > 0:
                    entropy[valid_word] += probability * math.log(1 / probability, 2)
            percent += increment
            tens = int(percent // 10)
            loading_message = "Guessing" + "." * tens + " " * (10 - tens) + str(int(percent)) + "%"
            print(loading_message, end="\r")
    elif round == 1:
        for (valid_word, infostring), words in dict.items():
            if notRedundant(valid_word, infostring):
                #Update data by removing eliminated words
                data[(valid_word, infostring)] = list(set(words_left) & set(words))
                probability = len(data[(valid_word, infostring)]) / len(words_left)
                if probability > 0:
                    entropy[valid_word] += probability * math.log(1 / probability, 2)
            percent += increment
            tens = int(percent // 10)
            loading_message = "Guessing" + "." * tens + " " * (10 - tens) + str(int(percent)) + "%"
            print(loading_message, end="\r")
    else:
        for (valid_word, infostring), words in data.items():
            if notRedundant(valid_word, infostring):
                #Update data by removing eliminated words
                data[(valid_word, infostring)] = list(set(words_left) & set(words))
                probability = len(data[(valid_word, infostring)]) / len(words_left)
                if probability > 0:
                    entropy[valid_word] += probability * math.log(1 / probability, 2)
            percent += increment
            tens = int(percent // 10)
            loading_message = "Guessing" + "." * tens + " " * (10 - tens) + str(int(percent)) + "%"
            print(loading_message, end="\r")
    print("                      ", end="\r")
    guess = max(entropy, key=entropy.get)
    return guess

def isValidInfostring(string):
    if len(string) != 5:
        return False
    regex = re.compile("[_~!⬛🟨🟩]")
    infostring = copy.deepcopy(string)
    for char in infostring:
        match = regex.search(infostring)
        if match is None:
            return False
        infostring = infostring[match.end():]
    return True

def iWon(infostring):
    for i in range(5):
        if infostring[i] != "🟩":
            return False
    return True

def play():
    isAnswerUnknown = True
    answer = input("Enter the word you'd like me to guess (return if unknown): ")
    #Check user-input answer is a valid 5-letter word
    if answer != "":
        answer = answer.lower()
        if answer not in valid_words:
            print("Invalid word entered!")
            print("Please enter a valid 5-letter English word with no numbers or special characters")
            return
        isAnswerUnknown = False
    # Count how many of each distinct letter there are in user-input answer
    num_answer = {}
    if not isAnswerUnknown:
        for i in range(5):
            letter = answer[i]
            num_answer[letter] = 0
            for j in range(5):
                if answer[j] == letter:
                    num_answer[letter] += 1

    words = copy.deepcopy(valid_words)
    data = {}

    for round in range(NUM_ROUNDS):
        #Compute next guess
        if len(words) == 0:
            print("ERROR")
            print("I can't find your word! 😡")
            print("There are two possible reasons for that:")
            print("1. Because it's not a valid Wordle word")
            print("2. Because you made a mistake when you entered the infostring")
            print("For the list of valid words, check out valid_words.txt")
            return
        elif len(words) == 1:
            guess = words[0]
        elif round + 1 == NUM_ROUNDS:
            commonly_used_words_left = list(set(words) & set(commonly_used_words))
            if len(commonly_used_words_left) > 0:
                guess = commonly_used_words_left[0]
            else:
                guess = words[0]
        else:
            guess = generateGuess(words, data, round)
        print("Guess #" + str(round + 1) + ": " + " ".join(guess.upper()))
        infostring = ""
        infostringList = ["","","","",""]
        if isAnswerUnknown:
            #Ask for user-input infostring
            validInfostring = False
            while not validInfostring:
                string = input("Result:   ")
                string = string.replace(" ", "")
                if not isValidInfostring(string):
                    print("Invalid infostring")
                    print("Enter five ⬛🟨🟩 or _~! characters")
                    print("⬛ or _ indicates the letter is not in the target word")
                    print("🟨 or ~ indicates the letter is in the wrong place")
                    print("🟩 or ! indicates the letter is correctly placed")
                else:
                    validInfostring = True
            for i in range(5):
                if string[i] == "_":
                    infostringList[i] = "⬛"
                elif string[i] == "~":
                    infostringList[i] = "🟨"
                else:
                    infostringList[i] = "🟩"
        else:
            #Automate infostring generation based on user-provided solution
            num_guess = {}
            num_greens = {}
            for i in range(5):
                letter = guess[i]
                num_guess[letter] = 0
                num_greens[letter] = 0
                for j in range(5):
                    if guess[j] == letter:
                        num_guess[letter] += 1
            for i in range(5):
                letter = guess[i]
                if answer[i] == letter:
                    infostringList[i] = "🟩"
                    num_greens[letter] += 1
                elif letter in answer and num_answer[letter] >= num_guess[letter]:
                    infostringList[i] = "🟨"
                elif letter in answer and num_answer[letter] < num_guess[letter]:
                    infostringList[i] = "?"
                else:
                    infostringList[i] = "⬛"
            for i in range(5):
                if infostringList[i] == "?":
                    letter = guess[i]
                    if num_answer[letter] == num_greens[letter]:
                        infostringList[i] = "⬛"
                    elif num_answer[letter] > num_greens[letter]:
                        infostringList[i] = "🟨"
                        num_greens[letter] += 1
        infostring = "".join(infostringList)
        print("          " + infostring)
        #Check if guess was correct
        if iWon(infostring):
            print("The computer wins once again")
            print("Congratulations to me")
            print("^-^")
            return
        if len(words) == 1:
            print("ERROR")
            print("I can't find your word! 😡")
            print("There are two possible reasons for that:")
            print("1. Because it's not a valid Wordle word")
            print("2. Because you made a mistake when you entered the infostring")
            print("For the list of valid words, check out valid_words.txt")
            return
        #Remove words based on this round's information gain
        words = removeWords(data, guess, infostring, round)
    print("The victory is not mine this time")
    print(":,(")
    return

#Time for Wordle!
if __name__ == '__main__':
    load_data()
    again = ""
    while again != "n":
        play()
        again = input("Play again (y/n)? ")
    sys.exit()
