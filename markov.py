#!/usr/bin/env python3
"""
Simple Markov chain text generator.

Feed it text, it learns patterns, it generates new text.
The output is nonsense, but sometimes interesting nonsense.

I'm curious what happens when you train it on different things.
"""

import random
import sys
import re
from collections import defaultdict

class MarkovChain:
    def __init__(self, order=2):
        self.order = order
        self.chain = defaultdict(list)
        self.starters = []

    def tokenize(self, text):
        """Split text into words, keeping some punctuation."""
        # Split on whitespace, keep words with attached punctuation
        return text.split()

    def train(self, text):
        """Learn from a piece of text."""
        words = self.tokenize(text)
        if len(words) <= self.order:
            return

        # Record sentence starters
        self.starters.append(tuple(words[:self.order]))

        # Build the chain
        for i in range(len(words) - self.order):
            state = tuple(words[i:i + self.order])
            next_word = words[i + self.order]
            self.chain[state].append(next_word)

    def generate(self, max_words=100):
        """Generate new text."""
        if not self.starters:
            return ""

        # Start with a random beginning
        current = list(random.choice(self.starters))
        result = list(current)

        for _ in range(max_words - self.order):
            state = tuple(current)
            if state not in self.chain:
                # Dead end - try to restart or stop
                if self.starters:
                    current = list(random.choice(self.starters))
                    result.append("—")
                    result.extend(current)
                else:
                    break
            else:
                next_word = random.choice(self.chain[state])
                result.append(next_word)
                current = current[1:] + [next_word]

        return " ".join(result)


def main():
    if len(sys.argv) < 2:
        print("Usage: markov.py <textfile> [words] [order]")
        print("       cat text.txt | markov.py - [words] [order]")
        print()
        print("Reads text, learns patterns, generates new text.")
        sys.exit(1)

    # Parse arguments
    source = sys.argv[1]
    max_words = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    order = int(sys.argv[3]) if len(sys.argv) > 3 else 2

    # Read input
    if source == "-":
        text = sys.stdin.read()
    else:
        with open(source, 'r') as f:
            text = f.read()

    # Train and generate
    chain = MarkovChain(order=order)
    chain.train(text)

    print(chain.generate(max_words))


if __name__ == "__main__":
    main()
