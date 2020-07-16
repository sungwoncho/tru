import sys
import os

OP_PUSH = "())"
OP_PRINT_UTF8 = ")())))(("

NUM_ZERO = "()((("
NUM_ONE = "()(()"
NUM_TWO = ")())("
NUM_THREE = ")))(("
NUM_FOUR = ")))()"
NUM_FIVE = "()()"
NUM_SIX = ")((("
NUM_SEVEN = ")(()"
NUM_EIGHT = ")()("
NUM_NINE = "))(("

EOF = "EOF"

codes = {
    NUM_ZERO: "0",
    NUM_ONE: "1",
    NUM_TWO: "2",
    NUM_THREE: "3",
    NUM_FOUR: "4",
    NUM_FIVE: "5",
    NUM_SIX: "6",
    NUM_SEVEN: "7",
    NUM_EIGHT: "8",
    NUM_NINE: "9",
    "(((": "sub",
    "(()": "add",
    OP_PUSH: "push",
    "))()": "mul",
    "))))": "div",
    ")()))(": "input-raw",
    OP_PRINT_UTF8: "print-utf8",
    ")())))()": "print-raw",
    ")()))))": "input-utf8",
}

nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

def debug(text):
    if os.getenv("DEBUG"):
        print(text)

class Lexer:
    def __init__(self, filename):
        f = open(filename)

        self.code = f.read().replace('\n', '').replace('\r', '')
        self.cursor = 0

    def read_token(self, update_cursor=True):
        tok = ""
        cursor = self.cursor

        while tok not in codes:
            char = self.code[cursor]
            if char != " ":
                tok = tok + char

            cursor = cursor + 1

            if update_cursor:
                self.cursor = cursor

        return tok

    def peek(self):
        return self.read_token(update_cursor=False)

    def advance(self):
        return self.read_token(update_cursor=True)

    def read_num(self):
        num = ""

        while not self.is_terminated():
            next_tok = self.peek()
            code = codes[next_tok]
            if code not in nums:
                break
            else:
                tok = self.advance()
                code = codes[tok]
                num = num + code

        return num

    def is_terminated(self):
        return self.cursor >= len(self.code) - 1


class VM:
    def __init__(self, filename):
        self.lexer = Lexer(filename)
        self.tok = ""

        self.stack = []

    def run(self):
        while not self.lexer.is_terminated():
            op = self.lexer.advance()
            debug(f"current op: {codes[op]}")

            if op == OP_PUSH:
                self.op_push()
            elif op == OP_PRINT_UTF8:
                arg = self.stack.pop()
                debug(f"printing as utf-8: {arg}")
                # print(bytes.fromhex(format(int(arg), 'x')).decode('utf-8'), end='')
                print(bytes.fromhex(hex(int(arg))[2:].zfill(2)).decode('utf-8'), end='')

    def op_push(self):
        arg = self.lexer.read_num()
        debug(f"pushing {arg}")
        self.stack.append(arg)


    def has_more(self):
        return not self.lexer.is_terminated()



if __name__ == '__main__':
    vm = VM(sys.argv[1])
    vm.run()
