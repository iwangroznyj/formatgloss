#! /usr/bin/env python

'''Command-line interface to Formatgloss.

This script reads a Toolbox file and reformats glosses in it.  The
reformatted glosses are then printed out to standard output.

'''


import sys
import formatglosslib.tbgloss as tbgloss


def format_faulty_gloss(gloss):
    '''Format a faulty gloss for printing.

    :param gloss: gloss to be formatted
    :type  gloss: tbgloss.ToolboxGloss
    :return:      formatted gloss
    :rtype:        str

    '''
    head = '\n{0:=^60}'.format(' WARNING ')
    error = '({0})'.format(gloss.error)
    msg = 'Could not parse following gloss:'
    line = 60 * '-'
    foot = 60 * '='
    return '\n'.join([head, msg, error, line, str(gloss), foot])


def main(args):
    '''Read toolbox file and print reformatted file to stdout.

    :param args: command-line arguments
    :type  args: list of str

    '''
    if len(args) != 2:
        sys.stderr.write('Error: needs exactly one text file.\n')
        return
    with open(args[1]) as input_file:
        lines = input_file.readlines()
    lines = [line.decode(tbgloss.INPUT_ENC).rstrip() for line in lines]
    toolbox_file = tbgloss.ToolboxFile(lines)
    print str(toolbox_file)
    for gloss in toolbox_file.get_glosses():
        if gloss.is_faulty:
            sys.stderr.write(format_faulty_gloss(gloss) + '\n')


if __name__ == '__main__':
    main(sys.argv)
