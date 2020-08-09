import os
import sys

code = {
        "<": "60",
        ">": "62",
        "(": "40",
        ")": "41",
        "[": "91",
        "]": "93",
}

cur = ""

if __name__ == '__main__':

    abspath = os.path.abspath(sys.argv[1])
    with open(abspath) as src:
        content = src.read()

        out = []

        for char in content:
            if char in code:
                if cur != "":
                    out.append("(" + str(cur) + ")")
                    cur = ""

                out.append("("+code[char]+")")
            else:
                cur = cur + str(char)

        if cur != "":
            out.append("(" + str(cur) + ")")

        #out.reverse()
        res = ''.join(out)
        print(res)
