import csv
import sys
from argparse import ArgumentParser
from typing import Dict, Callable

from .find_parser import parse_find_output, Directory


def main():
    parser = ArgumentParser(
        'Find outputs and seek common subdirectories. Output is written to STDOUT in the CSV format.')
    parser.add_argument('--find-output-filepath1', required=True)
    parser.add_argument('--find-output-filepath2', required=True)
    args = parser.parse_args()

    with open(args.find_output_filepath1) as f:
        find_output_1 = f.readlines()
    with open(args.find_output_filepath2) as f:
        find_output_2 = f.readlines()

    d1_root = parse_find_output(find_output_1, '/')
    d2_root = parse_find_output(find_output_2, '/')
    dict1 = directory_checksum_dict(d1_root, lambda d: len(d.directories) > 0)
    dict2 = directory_checksum_dict(d2_root, lambda d: len(d.directories) > 0)

    common_keys = dict1.keys() & dict2.keys()
    writer = csv.DictWriter(sys.stdout, ['d1_fullpath', 'd2_fullpath', 'checksum'])
    writer.writeheader()
    for ck in common_keys:
        d1 = dict1[ck]
        d2 = dict2[ck]
        writer.writerow({'d1_fullpath': d1.fullpath, 'd2_fullpath': d2.fullpath, 'checksum': ck})


def directory_checksum_dict(dir: Directory, filter_func: Callable[[Directory], bool]) -> Dict[int, Directory]:
    output: Dict[int, Directory] = dict()

    def _directory_checksum_dict(nested_dir: Directory) -> None:
        if filter_func(nested_dir):
            output[nested_dir.checksum] = nested_dir
            for d in nested_dir.directories:
                _directory_checksum_dict(d)

    _directory_checksum_dict(dir)
    return output


if __name__ == '__main__':
    main()
