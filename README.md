# Wordle Player

## Description
A computer program that plays Wordle at a level equivalent to or better than most humans using information theory principles.

## How to Run

First, run the `generate_data.py` script using your version of Python,

```
python3.10 generate_data.py
```

This will create a `./data` directory in your current working directory with the word data required to play Wordle. In this Github repository, data is only provided for a single word—`aahed`, the past tense of the interjection "aah" and first valid 5-letter word in alphabetical order—due to Git commit size limits. You'll need about 1.1 GB of space on your own machine to store all of the required data.

Note that the data generation step can take several hours depending on your machine specs.

Once you're done, you're ready to run the main `wordle.py` script and play Wordle:

```
python3.10 wordle.py
```

The initial loading of the data computed in the data generation stage can take a few minutes. This only needs to be done once before the first game.

You will be prompted for the word you want the computer to guess. We promise you the computer doesn't cheat! This is done to make the user's job easier.  If you choose not to specify the word, return, and you'll be prompted to enter the infostring yourself every time the computer makes a guess. An infostring is a string of 5 characters selected from `_~!` or ⬛🟨🟩 that provides the computer with letter-position information according to the rules of Wordle every time it makes a guess.

After each game, you're given the chance to end the session (by entering `n`) or keep playing (by entering anything else or returning).

## How to Play

Refer to the [New York Times website](https://www.nytimes.com/games/wordle/index.html) or the [wiki article](https://en.wikipedia.org/wiki/Wordle) for instructions on how to play Wordle.

## How Does It Work?

This Wordle player is a very simple program that leverages Shannon entropy in order to come up with the best possible next guess from the list of all 12,000+ valid words.

For every word in `valid_words.txt` (a potential next guess), and every possible infostring out of the $3^5$ permutations (a potential information gain), the program determines the set of valid 5-letter solutions left if it guessed that word and got that infostring.

The computer does this for every guess/infostring combination, and calculates the Shannon entropy—a measure of information content—for every possible next guess. The formula for the average Shannon entropy of a guess is,

$\overline{E} = \sum_{}^{} p \ln{\frac{1}{p}}$

The probability $p$ is the ratio of the number of words left post information gain to the current number of words left. To get the average entropy of a guess candidate, we sum over the entropies associated with every possible infostring $\ln{\frac{1}{p}}$, weighted by their probability $p$.

The word with the greatest average entropy is the best possible guess.

## Complexity

The time complexity of our program is $O(n^2)$ where $n$ is the number of valid words.
This is because, to generate a guess, we must compute the average entropy for every word ($n$ times). And this requires taking the intersection of sets that have a maximum of $n$ words which is an $O(n)$ linear-time operation.

## Example Run

As you can see, the word `tares` is always the computer's first guess, because it always has the maximum initial average entropy. 

```
Loading files..........100%
Enter the word you'd like me to guess (return if unknown): states
Invalid word entered!
Please enter a valid 5-letter English word with no numbers or special characters
Play again (y/n)? y
Enter the word you'd like me to guess (return if unknown): state
Guess #1: T A R E S   
          🟨🟨⬛🟨🟨
Guess #2: S T A L K   
          🟩🟩🟩⬛⬛
Guess #3: D A N G S   
          ⬛🟨⬛⬛🟨
Guess #4: A A R T I   
          🟨⬛⬛🟩⬛
Guess #5: S T A T E
          🟩🟩🟩🟩🟩
The computer wins once again
Congratulations to me
^-^
Play again (y/n)? 
Enter the word you'd like me to guess (return if unknown): globe
Guess #1: T A R E S   
          ⬛⬛⬛🟨⬛
Guess #2: D O I L Y   
          ⬛🟨⬛🟨⬛
Guess #3: M E N G E   
          ⬛⬛⬛🟨🟩
Guess #4: A B O V E   
          ⬛🟨🟩⬛🟩
Guess #5: G L O B E
          🟩🟩🟩🟩🟩
The computer wins once again
Congratulations to me
^-^
Play again (y/n)? 
Enter the word you'd like me to guess (return if unknown): curvy
Guess #1: T A R E S   
          ⬛⬛🟩⬛⬛
Guess #2: C O L I N   
          🟩⬛⬛⬛⬛
Guess #3: C H A R D   
          🟩⬛⬛🟨⬛
Guess #4: C U R V Y
          🟩🟩🟩🟩🟩
The computer wins once again
Congratulations to me
^-^
Play again (y/n)?
Enter the word you'd like me to guess (return if unknown): horse
Guess #1: T A R E S   
          ⬛⬛🟩🟨🟨
Guess #2: S O U C E   
          🟨🟩⬛⬛🟩
Guess #3: D A W A H   
          ⬛⬛⬛⬛🟨
Guess #4: H O R S E
          🟩🟩🟩🟩🟩
The computer wins once again
Congratulations to me
^-^
Play again (y/n)? 
Enter the word you'd like me to guess (return if unknown): water
Guess #1: T A R E S   
          🟨🟩🟨🟩⬛
Guess #2: D O M A L   
          ⬛⬛⬛🟨⬛
Guess #3: C H E E P   
          ⬛⬛⬛🟩⬛
Guess #4: A G L O W   
          🟨⬛⬛⬛🟨
Guess #5: W A T E R
          🟩🟩🟩🟩🟩
The computer wins once again
Congratulations to me
^-^
Play again (y/n)? n
```

## Credits

Credit goes to math YouTube channel [3Blue1Brown](https://www.youtube.com/@3blue1brown) for giving me the idea of using information theory to solve Wordle.
