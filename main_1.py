"""
Business REQ:
Split a huge file (file size varies in 5 - 20 gb) of any file format into small chunk of file from given
number of lines or file size.
"""

import os
import sys
import glob
from itertools import takewhile, repeat, islice

src_type = sys.argv[1]
file_split_by_lines_or_size = sys.argv[2]
file_path = sys.argv[3]

if src_type == 'Pull':
    for filename in glob.iglob('{}/**'.format(file_path), recursive=True):
        if os.path.isfile(filename):
            # Separate file name and extension
            file_title = os.path.splitext(os.path.basename(filename))[0]
            file_extension = os.path.splitext(os.path.basename(filename))[1]

            if not file_split_by_lines_or_size.endswith('gb'):
                # Get total number of lines from source file
                input_file = open(filename, 'rb')
                read_lines = takewhile(lambda line: line, (input_file.raw.read(1024 * 1024) for _ in repeat(None)))
                total_lines = sum(each_line.count(b'\n') for each_line in read_lines)

                if total_lines > int(file_split_by_lines_or_size):
                    # Create directory as same source directory
                    source_file_name = filename.split('/')[-2]
                    os.mkdir('target/{}'.format(source_file_name))

                    """
                    Split files into multiples based on line numbers
                    """
                    with open(filename) as target_file:
                        for index, lines in enumerate(iter(lambda: list(islice(target_file,
                                                                               int(file_split_by_lines_or_size))), []),
                                                      1):
                            with open('target/{}/{}_{}{}'.format(source_file_name, file_title, index, file_extension),
                                      'w') as write_to_target:
                                write_to_target.writelines(lines)

            else:
                # Gb to bytes conversions for given size
                # clean_input_file_size = file_split_by_lines_or_size.strip('gb')
                # provided_file_size = str(int(clean_input_file_size) * (1024 * 1024 ** 2))

                # currently mb to bytes conversions for given size
                clean_input_file_size = file_split_by_lines_or_size.strip('gb')
                provided_file_size = str(int(clean_input_file_size) * (1024 ** 2))

                # Actual file size
                actual_file_size = os.path.getsize(filename)

                if actual_file_size > int(provided_file_size):
                    # Create directory as same source directory
                    source_file_name = filename.split('/')[-2]
                    os.mkdir('target/{}'.format(source_file_name))

                    """
                    Split files into multiples based on bytes size
                    """
                    with open(filename, 'rb') as source_file:
                        content = bytearray(os.path.getsize(filename))
                        source_file.readinto(content)

                        for key, value in enumerate(range(0, len(content), int(provided_file_size))):
                            with open('target/{}/{}_{}{}'.format(source_file_name, file_title, key + 1, file_extension),
                                      'wb') as f:
                                f.write(content[value: value + int(provided_file_size)])
