from scanner import tokenizer
from scanner import scanner
import argparse
from pathlib import Path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scanner phase of Compiling a file')
    parser.add_argument('--input_folder', type=str, default="./examples/", help='Path to the folder of the file')
    parser.add_argument('--output_folder', type=str, default="./examples/", help='Path to the folder of the output file')
    parser.add_argument('--filename', type=str, default="example_gcd", help='Name of the file')
    args = parser.parse_args()

    # Path to the source code file
    inpath = Path(args.input_folder) / f"{args.filename}.vc"
    
    # Read data from source code file
    data = ""
    with open(inpath, 'r') as file:
        data = file.read()
    
    # Tokenize the data
    tokens, pos = tokenizer.tokenize(data)

    # Write the tokens to .vctok file
    tokpath = Path(args.output_folder) / f"{args.filename}.vctok"
    with open(tokpath, 'w+') as file:
        for tok in tokens:
            file.write(f"{tok}\n")

    # Write the verbose tokens to .verbose.vctok file
    verbosepath = Path(args.output_folder) / f"{args.filename}.verbose.vctok"
    with open(verbosepath, 'w+') as file:
        for i in range(len(tokens)):
            state, kind = scanner.scan(tokens[i])
            line, col = pos[i]
            # print("tok = ", tok," s,k = ", state, kind)
            file.write(f"Spelling = \"{tokens[i]}\", kind = {state} [{kind}], position = {line}({col})..{line}({col+len(tok)-1})\n")
    