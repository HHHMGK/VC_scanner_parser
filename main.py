from scanner import tokenizer
from scanner import scanner
import argparse
from pathlib import Path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scanner phase of Compiling a file')
    parser.add_argument('--folder', type=str, default="./examples/", help='Path to the folder of the file')
    parser.add_argument('--filename', type=str, default="example_gcd", help='Name of the file')
    args = parser.parse_args()

    # Path to the source code file
    path = Path(args.folder) / f"{args.filename}.vc"
    # Read data from source code file
    data = ""
    with open(path, 'r') as file:
        data = file.read()
    
    tokens = tokenizer.tokenizer(data)
    with open('./examples/example_gcd.vctok', 'w+') as file:
    # with open('./examples/example_fib.vctok', 'w+') as file:
        file.write('\n'.join(tokens))

    verbose_tokens = scanner.scan_tokens(data)
    with open('./examples/example_gcd.verbose.vctok', 'w+') as file:
        for tok, state, kind in verbose_tokens:
            file.write(f"Spelling = \"{tok}\", kind = {state} [{kind}], position = ")
    
    