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
    
    tokens, pos = tokenizer.tokenizer2(data)
    tokpath = Path(args.output_folder) / f"{args.filename}.vctok"
    with open(tokpath, 'w+') as file:
        for tok in tokens:
            file.write(f"{tok}\n")

    # verbose_tokens = scanner.scan_tokens(tokens)
    # verbose_tokens = tokens
    verbosepath = Path(args.output_folder) / f"{args.filename}.verbose.vctok"
    with open(verbosepath, 'w+') as file:
        for i in range(len(tokens)):
            tok, state, kind = scanner.scan(tokens[i])
            line, col = pos[i]
            # print("tok = ", tok," s,k = ", state, kind)
            file.write(f"Spelling = \"{tok}\", kind = {state} [{kind}], position = {line}({col})..{line}({col+len(tok)-1})\n")
        # for i in range(len(verbose_tokens)):
        #     tok, state, kind = verbose_tokens[i]
        #     line, col = pos[i]
        #     # print("tok = ", tok," s,k = ", state, kind)
        #     file.write(f"Spelling = \"{tok}\", kind = {state} [{kind}], position = {line}({col})..{line}({col+len(tok)-1})\n")
        # for tok in verbose_tokens:
        #     tok, (line, col) = tok
        #     state = 0
        #     kind = "*"
        #     file.write(f"Spelling = \"{tok}\", kind = {state} [{kind}], position = {line}({col})..{line}({col+len(tok)-1})\n")
    
    