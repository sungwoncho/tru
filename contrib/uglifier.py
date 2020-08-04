import os
import sys

valid_char = {
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    '(',
    ')',
    '[',
    ']',
    '<',
    '>',
}

class Uglifier:
    def __init__(self, filepath):
        with open(filepath) as src:
            self.code = src.read()
            self.lines = self.code.split('\n')

        self.cursor = 0
        self.line = 0
        self.filepath = filepath
        self.terminated = False
        self.is_comment = False

        destPath = self.get_dest_filename()
        self.outfile = open(destPath, 'w')

    def advance(self):
        self.cursor = self.cursor + 1

        while self.cursor > len(self.lines[self.line]) - 1:
            self.cursor = 0
            self.line = self.line + 1
            self.is_comment = False

            if self.line >= len(self.lines) - 1 and self.cursor >= len(self.lines[self.line])-1:
                self.terminated = True
                return

    def write(self):
        while not self.terminated:
            char = self.lines[self.line][self.cursor]
            if char in valid_char and not self.is_comment:
                self.outfile.write(char)
            elif char == '#':
                self.is_comment = True
            self.advance()

        self.outfile.close()

    def get_dest_filename(self):
        parts = self.filepath.split('/')
        filename = parts[len(parts)-1]

        dirname = os.path.dirname(self.filepath)

        parts = filename.split('.')
        basename = parts[0]
        ext = parts[1]

        return '{}/{}.min.{}'.format(dirname, basename, ext)

if __name__ == '__main__':
    abspath = os.path.abspath(sys.argv[1])
    u = Uglifier(abspath)
    u.write()
