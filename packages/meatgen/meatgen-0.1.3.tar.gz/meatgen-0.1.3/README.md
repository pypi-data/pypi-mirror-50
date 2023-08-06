# Meatspace Password Generator

Generate passwords from real world phenomena

# Usage
``` $ meatgen --help
usage: meatgen [-h] [-d DELIMITER] [--wordlist WORDLIST] key [key ...]

Generate passwords from real world phenomena

positional arguments:
  key                   A sequence of keys from the wordlist

optional arguments:
  -h, --help            show this help message and exit
  -d DELIMITER, --delimiter DELIMITER
                        The string that separates keys and values in the
                        wordlist
  --wordlist WORDLIST   Path to a file container a wordlist
```

The wordlist is also accepted over `STDIN`.

## Wordlist
A wordlist is simple a textfile containing lines in the form of "{KEY}{DELIMITER}{VALUE}\n", this list is parsed at the beginning of execution and used to generate the output.
Any lines not matching this format will simply be ignored.

Typically each password generation technique comes with it's own wordlists. The most well known is [diceware](http://world.std.com/~reinhold/diceware.html), but alternative techniques exist as well, such as [pokerware](https://github.com/skeeto/pokerware).

## Examples
```
$ meatgen --wordlist /home/example-user/Documents/pokerware-formal.txt ACADD ACTCC 3C4CH 5STHS
abide anemia fake peace
$ cat /home/example-user/Documents/pokerware-formal.txt | meatgen ACADD ACTCC 3C4CH 5STHS
abide anemia fake peace
$ meatgen --wordlist /home/example-user/Documents/diceware.wordlist.asc 11136
abbot
```
