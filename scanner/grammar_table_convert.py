import csv
import os

input_filename = "../grammar/LL1_grammar.md"
output_folder = "../grammar"
output_filename = "../grammar/LL1_grammar_table.csv"

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Construct the full output file path
output_file_path = os.path.join(output_folder, output_filename)

# Open input file for reading
with open(input_filename, "r", encoding="utf-8") as input_file:
    lines = input_file.readlines()

# Modify lines by replacing "->" and "|" with ","
modified_lines = [line.replace("->", ",").replace("|", ",") for line in lines]

# Open output file for writing as CSV with UTF-8 encoding
with open(output_file_path, "w", newline="", encoding="utf-8") as output_file:
    writer = csv.writer(output_file)
    writer.writerows([line.strip().split(",") for line in modified_lines])