import sys
import os

TOK_PUSH_START = '('
TOK_PUSH_END = ')'
TOK_PRINT_UTF8 = '<><>><<'
TOK_PRINT_INT = '<><>><>'
TOK_INPUT_UTF8 = '<><>>>'
TOK_INPUT_INT = '<><><'
TOK_END = '>>><<'
TOK_POP_MOVE = '>>><>'
TOK_POP_DISCARD = '<><<'
TOK_DUP = '>><<'
TOK_SWAP = '>><>'
TOK_SUB = '>>>>'
TOK_ADD = '<<<'
TOK_GT = '<<>'
TOK_EQ = '<>>'
TOK_NOT = '><<'
TOK_SELECT_STACK = '><>'
TOK_LABEL_LEFT = '['
TOK_LABEL_RIGHT = ']'
TOK_COMMENT = '#'
TOK_NUM = 'number'
TOK_BLANK = 'blank'
TOK_DEBUG = '%'

tok_name = {
    TOK_PUSH_START: 'push_start',
    TOK_PUSH_END: 'push_end',
    TOK_PRINT_UTF8: 'print_utf8',
    TOK_PRINT_INT: 'print_int',
    TOK_INPUT_UTF8: 'input_utf8',
    TOK_INPUT_INT: 'input_int',
    TOK_SELECT_STACK: 'select_stack',
    TOK_POP_MOVE: 'pop_move',
    TOK_POP_DISCARD: 'pop_discard',
    TOK_SWAP: 'swap',
    TOK_DUP: 'dup',
    TOK_SUB: 'sub',
    TOK_ADD: 'add',
    TOK_GT: 'gt',
    TOK_EQ: 'eq',
    TOK_NOT: 'not',
    TOK_END: 'end',
    TOK_LABEL_LEFT: 'left',
    TOK_LABEL_RIGHT: 'right',
    TOK_COMMENT: '#',
    TOK_NUM: 'number',
    TOK_BLANK: 'blank',
    TOK_DEBUG: 'debug'
}

codes = {
    TOK_PUSH_START,
    TOK_PUSH_END,
    TOK_PRINT_UTF8,
    TOK_PRINT_INT,
    TOK_INPUT_UTF8,
    TOK_INPUT_INT,
    TOK_SELECT_STACK,
    TOK_POP_MOVE,
    TOK_POP_DISCARD,
    TOK_DUP,
    TOK_SWAP,
    TOK_SUB,
    TOK_ADD,
    TOK_GT,
    TOK_EQ,
    TOK_NOT,
    TOK_END,
    TOK_LABEL_LEFT,
    TOK_LABEL_RIGHT,
    TOK_DEBUG
}

nums = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}

def debug(text):
    if os.getenv('DEBUG'):
        print(text)

class Token:
    def __init__(self, kind, line, cursor, value=None):
        self.kind = kind
        self.value = value
        if value is None:
            self.value = kind

        self.line = line
        self.cursor = cursor

class Lexer:
    def __init__(self, lines):
        self.lines = lines
        self.line = 0
        self.cursor = 0
        self.terminated = False

    def set_pos(self, line, cursor):
        self.line = line
        self.cursor = cursor

    def get_next_token(self):
        tok = self.read_token()
        self.process_token(tok)

        return tok

    def read_token(self):
        lead = self.read_current_char()
        # TODO: tab
        while lead == ' ':
            self.cursor = self.cursor + 1
            self.advance()
            lead = self.read_current_char()

        # debug('reading from ({},{})'.format(self.line, self.cursor))

        if lead == TOK_PUSH_START:
            return Token(TOK_PUSH_START, self.line, self.cursor, None)
        elif lead == TOK_PUSH_END:
            return Token(TOK_PUSH_END, self.line, self.cursor, None)
        elif lead == TOK_LABEL_LEFT:
            return Token(TOK_LABEL_LEFT, self.line, self.cursor, None)
        elif lead == TOK_LABEL_RIGHT:
            return Token(TOK_LABEL_RIGHT, self.line, self.cursor, None)
        elif lead == '<' or lead == '>':
            op = self.read_op()
            return Token(op, self.line, self.cursor, None)
        elif lead == '#':
            return Token(TOK_COMMENT, self.line, self.cursor, None)
        elif lead == '%':
            return Token(TOK_DEBUG, self.line, self.cursor, None)
        elif lead in nums:
            num = self.read_num()
            return Token(TOK_NUM, self.line, self.cursor, num)

        print('invalid token at ({},{})'.format(self.line, self.cursor))
        return

    def process_token(self, token):
        # debug('advancing from ({},{}) token is {}'.format(self.line, self.cursor, token.kind))
        if token.kind == TOK_COMMENT:
            # ignore the rest of the current line
            self.cursor = 0
            self.line = self.line + 1
            self.advance()
            return

        self.cursor = self.cursor + len(str(token.value))
        if token.kind == TOK_END:
            return

        self.advance()
        # debug('current is now ({},{})'.format(self.line, self.cursor))

    def seek_closing_label(self):
        label_stack = []

        tok = self.get_next_token()

        while True:
            if tok.kind == TOK_LABEL_LEFT:
                label_stack.append(TOK_LABEL_LEFT)
            if tok.kind == TOK_LABEL_RIGHT:
                if len(label_stack) == 0:
                    break
                else:
                    label_stack.pop()

            tok = self.get_next_token()

        return tok

    def get_max_cursor(self):
        return len(self.lines[self.line])-1

    def advance(self):
        maxCursor = self.get_max_cursor()

        while self.cursor > maxCursor:
            self.cursor = 0
            self.line = self.line + 1

            maxCursor = self.get_max_cursor()

    def read_current_char(self):
        return self.read_char_at(self.line, self.cursor)

    def read_char_at(self, line, cursor):
        # debug('reading {},{}'.format(line, cursor))
        return self.lines[line][cursor]

    def read_op(self):
        code = ""
        cursor = self.cursor

        while code not in codes:
            char = self.read_char_at(self.line, cursor)
            code = code + char
            cursor = cursor + 1

        return code

    def read_num(self):
        num = ""
        cursor = self.cursor

        while not self.terminated:
            char = self.read_char_at(self.line, cursor)
            if char not in nums:
                break
            else:
                num = num + char
                cursor = cursor + 1

        return int(num)

class Label:
    def __init__(self, line, cursor):
        self.line = line
        self.cursor = cursor

class VM:
    def __init__(self, filename):
        with open(filename) as src:
            self.code = src.read()
            lines = self.code.split('\n')
            self.lexer = Lexer(lines)


        self.s0 = []
        self.s1 = []
        self.label_left = []
        self.terminated = False

        self.current_stack = 0

    def run(self):
        while not self.terminated:
            tok = self.lexer.get_next_token()
            kind = tok.kind
            debug(f"======= current tok: {tok_name[tok.kind]} {tok.value}")
            debug(f"current stacks: {self.s0} {self.s1}")

            if kind == TOK_PUSH_START:
                self.op_push()
            elif kind == TOK_PRINT_UTF8:
                num = self.pop_stack()
                out = bytes([num]).decode('utf-8')

                print(out, end='')
            elif kind == TOK_PRINT_INT:
                print(self.get_current_stack().pop(), end='')
            elif kind == TOK_END:
                self.terminated = True
            elif kind == TOK_LABEL_LEFT:
                val = self.pop_stack()
                if val == 0:
                    label = self.lexer.seek_closing_label()
                    self.lexer.set_pos(label.line, label.cursor+1)
                    self.lexer.advance()
                else:
                    self.label_left.append(Label(tok.line, tok.cursor))



            elif kind == TOK_LABEL_RIGHT:
                label = self.label_left.pop()
                val = self.pop_stack()
                if val != 0:
                    # save the label
                    self.label_left.append(Label(label.line, label.cursor))

                    self.lexer.set_pos(label.line, label.cursor+1)
                    self.lexer.advance()
            elif kind == TOK_DUP:
                s = self.get_current_stack()
                self.push_stack(s[-1])
            elif kind == TOK_EQ:
                rhs = self.pop_stack()
                lhs = self.pop_stack()

                if rhs == lhs:
                    self.push_stack(1)
                else:
                    self.push_stack(0)

            elif kind == TOK_SUB:
                rhs = self.pop_stack()
                lhs = self.pop_stack()
                res = lhs - rhs

                self.push_stack(res)
            elif kind == TOK_ADD:
                rhs = self.pop_stack()
                lhs = self.pop_stack()
                res = lhs + rhs

                self.push_stack(res)
            elif kind == TOK_SELECT_STACK:
                val = self.pop_stack()
                if val == 0:
                    self.current_stack = 0
                else:
                    self.current_stack = 1
            elif kind == TOK_NOT:
                val = self.pop_stack()
                if val == 0:
                    self.push_stack(1)
                elif val == 1:
                    self.push_stack(0)
            elif kind == TOK_INPUT_INT:
                val = input("input: ")
                self.push_stack(int(val))
            elif kind == TOK_INPUT_UTF8:
                val = input("input: ")
                char = val[0]
                num = int.from_bytes(char.encode('utf-8'), byteorder=sys.byteorder)
                self.push_stack(num)
            elif kind == TOK_POP_MOVE:
                val = self.pop_stack()
                dest = self.get_other_stack()
                dest.append(val)
            elif kind == TOK_POP_DISCARD:
                self.pop_stack()
            elif kind == TOK_SWAP:
                val1 = self.pop_stack()
                val2 = self.pop_stack()

                self.push_stack(val1)
                self.push_stack(val2)
            elif kind == TOK_DEBUG:
                print(f"breakpoint ({tok.line},{tok.cursor})")
                print(f"current stacks: {self.s0} {self.s1}")
                input("Continue")


    def push_stack(self, val):
        s = self.get_current_stack()
        return s.append(val)

    def pop_stack(self):
        s = self.get_current_stack()
        return s.pop()

    def peek_stack(self):
        s = self.get_current_stack()
        return s[len(s)-1]

    def toggle_stack(self):
        self.current_stack = not self.current_stack

    def get_other_stack(self):
        if self.current_stack == 0:
            return self.s1

        return self.s0

    def get_current_stack(self):
        if self.current_stack == 0:
            return self.s0

        return self.s1

    def op_push(self):
        tok = self.lexer.read_token()
        if tok.kind != TOK_NUM:
            print("invalid token")
            return

        num = tok.value
        # debug(f"pushing {num} to s{self.current_stack}")
        self.push_stack(num)


if __name__ == '__main__':
    vm = VM(sys.argv[1])
    vm.run()
