#!/usr/bin/env python3
"""
brainfuck.py - A Brainfuck interpreter.

Brainfuck is a minimalist esoteric programming language created by
Urban Müller in 1993. It has only 8 commands:

    >  Move pointer right
    <  Move pointer left
    +  Increment cell
    -  Decrement cell
    .  Output cell as ASCII
    ,  Input character to cell
    [  Jump forward to ] if cell is 0
    ]  Jump back to [ if cell is nonzero

Everything else is a comment. That's it. That's the whole language.
"""

import sys

def interpret(code: str, input_data: str = "") -> str:
    """
    Interpret Brainfuck code.

    Args:
        code: The Brainfuck program
        input_data: Input string for , commands

    Returns:
        The output produced by the program
    """
    # Clean code - remove non-commands
    code = ''.join(c for c in code if c in '><+-.,[]')

    # Memory tape (30,000 cells, standard)
    tape = [0] * 30000
    ptr = 0  # Data pointer
    pc = 0   # Program counter

    # Pre-compute bracket matches for efficiency
    brackets = {}
    stack = []
    for i, c in enumerate(code):
        if c == '[':
            stack.append(i)
        elif c == ']':
            if stack:
                j = stack.pop()
                brackets[j] = i
                brackets[i] = j

    output = []
    input_ptr = 0

    while pc < len(code):
        cmd = code[pc]

        if cmd == '>':
            ptr = (ptr + 1) % 30000
        elif cmd == '<':
            ptr = (ptr - 1) % 30000
        elif cmd == '+':
            tape[ptr] = (tape[ptr] + 1) % 256
        elif cmd == '-':
            tape[ptr] = (tape[ptr] - 1) % 256
        elif cmd == '.':
            output.append(chr(tape[ptr]))
        elif cmd == ',':
            if input_ptr < len(input_data):
                tape[ptr] = ord(input_data[input_ptr])
                input_ptr += 1
            else:
                tape[ptr] = 0
        elif cmd == '[':
            if tape[ptr] == 0:
                pc = brackets.get(pc, pc)
        elif cmd == ']':
            if tape[ptr] != 0:
                pc = brackets.get(pc, pc)

        pc += 1

    return ''.join(output)


# Some example programs
HELLO_WORLD = """
++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]
>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.
"""

CAT = """
,[.,]
"""

ADD = """
,>,[-<+>]<.
"""


def main():
    if len(sys.argv) > 1:
        # Run code from command line
        code = sys.argv[1]
        if code.endswith('.bf'):
            with open(code) as f:
                code = f.read()
        print(interpret(code))
    else:
        # Demo mode
        print("Brainfuck Interpreter")
        print("=" * 40)
        print()
        print("Running Hello World:")
        print(interpret(HELLO_WORLD))
        print()
        print("The program was:")
        print(HELLO_WORLD.strip())
        print()
        print("That's the whole thing. 8 commands.")
        print("Everything else is a comment.")


if __name__ == '__main__':
    main()
