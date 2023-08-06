import argparse
import pathlib
import sys

from meatgen.generate import generate

EXIT_FAILURE = 1

def main():
    parser = argparse.ArgumentParser(description="Generate passwords from real world phenomena")

    parser.add_argument('-d', '--delimiter', default='\t', help="The string that separates keys and values in the wordlist")
    parser.add_argument('key', nargs='+', help="A sequence of keys from the wordlist")
    parser.add_argument('--wordlist', type=argparse.FileType('r'),
                        default=sys.stdin, help="Path to a file container a wordlist")

    args = parser.parse_args()
    words = generate(args.wordlist, args.delimiter, args.key)
    print(' '.join(words))

if __name__ == '__main__':
    main()
