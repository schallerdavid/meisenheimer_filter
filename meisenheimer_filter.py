import argparse
import os


description = "\n".join([
    r"               _              _        _                  __ _ _ _              ",
    r"     _ __  ___(_)___ ___ _ _ | |_  ___(_)_ __  ___ _ _   / _(_) | |_ ___ _ _    ",
    r"    | '  \/ -_) (_-</ -_) ' \| ' \/ -_) | '  \/ -_) '_| |  _| | |  _/ -_) '_|   ",
    r"    |_|_|_\___|_/__/\___|_||_|_||_\___|_|_|_|_\___|_|   |_| |_|_|\__\___|_|     "
    r"",
    r"     Filter molecules for substructures able to form a Meisenheimer complex.    ",
    r"                                   v. alpha                                     "])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='meisenheimer filter', description=description,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', dest='input_paths',
                        help='directory containing input files or paths to input files separated by comma '
                             '(*.smi, *.sdf)',
                        required=True)
    parser.add_argument('-o', dest='output_path', help='path to output file (*.smi, *.sdf)',
                        default='./meisenheimer.smi')
    if os.path.isdir(parser.parse_args().input_paths):
        input_directory = os.path.abspath(parser.parse_args().input_paths)
        input_paths = [os.path.join(input_directory, path) for path in os.listdir(input_directory)
                       if path[-4:] in ['.smi', '.sdf']]
    else:
        input_paths = [os.path.abspath(path) for path in parser.parse_args().input_paths.split(',')]
    output_path = os.path.abspath(parser.parse_args().output_path)
