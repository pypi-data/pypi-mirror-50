#!/usr/bin/env python
import sys, json, yaml, requests
import pkg_resources
version = pkg_resources.require("majime")[0].version

def getopts(argv):
    opts = {}
    while argv:
        if argv[0][0] == '-':
            try:
                opts[argv[0]] = argv[1]
            except:
                opts[argv[0]] = ""
        argv = argv[1:]
    return opts

def output(content, type=""):
    try:
        print(str(content))
    except:
        output("ERROR: output contains binary or UTF-8 content that this terminal cannot render.")

def main():

    args = getopts(sys.argv)
    if '-v' in args:
        output("Majime version " + str(version))
        sys.exit(0)

    print("This is majime")
if __name__ == '__main__':
    main()
