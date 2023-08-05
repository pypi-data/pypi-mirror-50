#! /usr/bin/env python
import argparse
import subprocess

def run(args):
    filename = args.input
    command = "cc {0}.c -lcs50 -o {0}".format(filename)
    print(command)
    subprocess.run(command, shell=True)

def main():
    parser = argparse.ArgumentParser(description="Convert a fastA file to a FastQ file")
    parser.add_argument("input",help="The name of the source code file without the '.c' extension", type=str)
    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)

if __name__=="__main__":
	main()
