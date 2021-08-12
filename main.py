import sys
import argparse

from interpreter import *
from output_formatter import *

__title__ = 'JMH Markdown Hierarchy Interpreter'
__version__ = '1.0.0'
__author__ = 'Jonah Hendler'


mode = 'run'


def process_file(**kwargs):
    filename = kwargs['filename']
    outfile = kwargs['outfile']
    showmargins = kwargs['showmargins']

    # print(kwargs)

    file_as_lines = open_file_as_lines(filename)
    formatted_lines = format_all_lines(file_as_lines)
    # for fl in formatted_lines:
    #     print(fl)

    for format_triple in formatted_lines:
        page_add_line(format_triple)
    output_page(outfile, print_margins=showmargins)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('## No input file.')
        sys.exit(1)
    elif len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description='Argument parser')
        parser.add_argument('-f', '--filename', help='Input filename')
        parser.add_argument('-o', '--outfile', help='Output filename')
        parser.add_argument('-m', '--showmargins', help='Show margins - (Y/y)ES/(N/n)O')
        parser.add_argument('-z', '--horizontal', help='Set horizontal margins in inches')
        parser.add_argument('-v', '--vertical', help='Set vertical margins in inches')
        parser.add_argument('-V', '--version', action='store_true', help='Get program\'s version')
        parser.add_argument('-s', '--pagesize', '--size', help='Set size of page')
        parser.add_argument('-w', '--pagewidth', '--width', help='Set width of page in inches')
        parser.add_argument('-l', '--pageheight', '--height', help='Set height of page in inches')

        args = parser.parse_args()

        if args.version is True:
            print(f'{__title__} - v{__version__} - By {__author__}')
            sys.exit(0)

        if args.filename is not None:
            filename = args.filename
            outfile = ''
            showmargins = False
            if args.outfile is not None:
                outfile = args.outfile
            else:
                outfile = filename.removesuffix('.fxmt') + '.png'
            # print(outfile)

            if args.showmargins is not None:
                showmargins = True if args.showmargins[0]=='y' or args.showmargins[0]=='Y' else False

            process_file(filename=filename, outfile=outfile, showmargins=showmargins)
        else:
            print('## Error - No input file.')
            sys.exit(1)

        print('## All done! :)')
        sys.exit(0)


    # if mode == 'mocktest':
    #     test_file_name = 'test2.fxmt'
    #     file_as_lines = open_file_as_lines(test_file_name)
    #     out_test_file_name = test_file_name.removesuffix('.fxmt')
    #     formatted_lines = format_all_lines(file_as_lines)
    #     for fl in formatted_lines:
    #         print(fl)
    #     # set_page(500, 500)
    #     # fit_page_to_lines(formatted_lines)
    #     for format_triple in formatted_lines:
    #         page_add_line(format_triple)
    #     output_page(out_test_file_name, print_margins=False)