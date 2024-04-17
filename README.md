# VC_scanner_parser

Group assignment for VNU-UET's Compiler course.
Including a simple scanner for a simple language called VC, the transition graph and transition table for the for the VC language.

## How to run

Install python (Recommended version 3.11, but should work with 3.6+)
Run the main file with the following command:

```bash
python main.py --filename <filename>
```

Where `<filename>` is the name of the file you want to parse, the program will locate the `<filename>.vc` file in the default `./examples/` directory and write to the `<filename>.vctok` and `<filename>.verbose.vctok` files in the same directory
Example:

```bash
python main.py --filename example_fib
```

### More options:

```bash
python main.py --filename <filename> --input_folder <input_folder> --output_folder <output_folder>
```

Where `<input_folder>` is the folder where the input files are located and `<output_folder>` is the folder where the output files will be saved, the default value is `./examples/`
