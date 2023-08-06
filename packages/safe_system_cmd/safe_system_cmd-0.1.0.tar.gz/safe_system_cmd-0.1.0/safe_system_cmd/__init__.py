# coding:utf-8

import os


invalid_char = '''$  &  ;  |  '  "  ( )  `'''.split()
invalid_char.append("\n")


def system(cmd):
    for char in cmd:
        if char in invalid_char:
            print("invalid cmd:{0}".format(cmd))
            return 255
    return os.system(cmd)


if __name__ == "__main__":

    assert system("ls") == 0
    assert system("ls \n") == 255
