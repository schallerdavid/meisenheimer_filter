import argparse
from rdkit import Chem
import os
import sys
import time


logo = "\n".join([
    r"               _              _        _                  __ _ _ _              ",
    r"     _ __  ___(_)___ ___ _ _ | |_  ___(_)_ __  ___ _ _   / _(_) | |_ ___ _ _    ",
    r"    | '  \/ -_) (_-</ -_) ' \| ' \/ -_) | '  \/ -_) '_| |  _| | |  _/ -_) '_|   ",
    r"    |_|_|_\___|_/__/\___|_||_|_||_\___|_|_|_|_\___|_|   |_| |_|_|\__\___|_|     "
    r"",
    r"     Filter molecules for substructures able to form a Meisenheimer complex.    ",
    r"                                   v. alpha                                     "])


def get_meisenheimer_smarts():
    """
    This function reads SMARTS from the meisenheimer.smarts file shipped with this repository.
    Returns
    -------
    smarts : list
        List of smarts.
    """
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'meisenheimer.smarts')
    smarts = []
    with open(file_path, 'r') as rf:
        for line in rf.readlines():
            smarts.append(Chem.MolFromSmarts(line.strip()))
    return smarts


def count_mols(file_path):
    """
    This function returns the number of molecules in an sdf- or smiles-file.
    Parameters
    ----------
    file_path : str
        Full path to sdf- or smiles file.
    Returns
    -------
    counter : int
        Number of molecules.
    """
    counter = 0
    with open(file_path, 'r', errors='backslashreplace') as mol_file:
        if '.sdf' in file_path:
            for line in mol_file:
                if '$$$$' in line:
                    counter += 1
        elif '.smi' in file_path:
            for line in mol_file:
                counter += 1
    return counter


def time_to_text(seconds):
    """
    This function converts a time in seconds into a reasonable format.
    Parameters
    ----------
    seconds : float
        Time in seconds.
    Returns
    -------
    time_as_text: str
        Time in s, min, h, d, weeks or years depending on input.
    """
    if seconds > 60:
        if seconds > 3600:
            if seconds > 86400:
                if seconds > 1209600:
                    if seconds > 62899252:
                        time_as_text = 'years'
                    else:
                        time_as_text = '{} weeks'.format(round(seconds / 1209600, 1))
                else:
                    time_as_text = '{} d'.format(round(seconds / 86400, 1))
            else:
                time_as_text = '{} h'.format(round(seconds / 3600, 1))
        else:
            time_as_text = '{} min'.format(round(seconds / 60, 1))
    else:
        time_as_text = '{} s'.format(int(seconds))
    return time_as_text


def update_progress(progress, progress_info, eta):
    """
    This function writes a progress bar to the terminal.
    Parameters
    ----------
    progress: float
        Progress of process described by number between 0 and 1.
    progress_info: str
        Info text that should be placed before the progress bar.
    eta: float
        Estimated time needed for finishing the process.
    """
    bar_length = 10
    block = int(bar_length * progress)
    if progress == 1.0:
        status = '         Done\n'
    else:
        status = '  ETA {:8}'.format(time_to_text(eta))
    text = '\r{}: [{}] {:>5.1f}%{}'.format(progress_info, '=' * block + ' ' * (bar_length - block), progress * 100,
                                           status)
    sys.stdout.write(text)
    sys.stdout.flush()
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='meisenheimer filter', description=logo,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', dest='input_paths',
                        help='directory containing input files or paths to input files separated by comma '
                             '(*.smi, *.sdf)',
                        required=True)
    parser.add_argument('-o', dest='output_path', help='path to output file (*.smi, *.sdf)',
                        default='./meisenheimer.smi')
    print(logo)
    if os.path.isdir(parser.parse_args().input_paths):
        input_directory = os.path.abspath(parser.parse_args().input_paths)
        input_paths = [os.path.join(input_directory, path) for path in os.listdir(input_directory)
                       if path[-4:] in ['.smi', '.sdf']]
    else:
        input_paths = [os.path.abspath(path) for path in parser.parse_args().input_paths.split(',')]
    num_molecules = sum([count_mols(input_path) for input_path in input_paths])
    output_path = os.path.abspath(parser.parse_args().output_path)
    meisenheimer_smarts = get_meisenheimer_smarts()
    if '.smi' in output_path:
        writer = Chem.SmilesWriter(output_path)
    else:
        writer = Chem.SDWriter(output_path)
    mol_counter = 0
    start_time = time.time()
    for input_path in input_paths:
        if '.smi' in input_path:
            supplier = Chem.SmilesMolSupplier(input_path)
        else:
            supplier = Chem.SDMolSupplier(input_path)
        for mol in supplier:
            for smarts_index in range(len(meisenheimer_smarts)):
                pattern = meisenheimer_smarts[smarts_index]
                if mol.HasSubstructMatch(pattern):
                    writer.write(mol)
                    break
            mol_counter += 1
            update_progress(mol_counter / num_molecules, 'Progress', ((time.time() - start_time) / mol_counter) *
                            (num_molecules - mol_counter))
    writer.close()
    print('Finished after {}.'.format(time_to_text(time.time() - start_time)))
