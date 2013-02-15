#! /usr/bin/env python

'''Command-line interface to Formatgloss.

This script reads a Toolbox file and reformats glosses in it.  The
reformatted glosses are then printed out to standard output or written
into a text file.

'''


import sys
import formatglosslib.tbgloss as tbgloss


WARN_GLOSS = '''
========================= WARNING ==========================
Could not parse following gloss:
({error})
------------------------------------------------------------
{gloss}
============================================================
'''


def main(args):
    '''Read toolbox file and print reformatted file to stdout.

    :param args: command-line arguments
    :type  args: list of str

    '''
    if len(args) < 2:
        sys.stderr.write('Error: missing input file.\n')
        return
    if len(args) > 3:
        sys.stderr.write('Error: too much arguments.\n')
        return
    with open(args[1]) as input_file:
        lines = input_file.readlines()
    lines = [line.decode(tbgloss.INPUT_ENC).rstrip() for line in lines]
    toolbox_file = tbgloss.ToolboxFile(lines)
    if len(args) == 3:
        with open(args[2], 'w') as output_file:
            output_file.write(str(toolbox_file))
    else:
        print str(toolbox_file)
    for gloss in toolbox_file.get_glosses():
        if gloss.is_faulty:
            sys.stderr.write(WARN_GLOSS.format(gloss=gloss, error=gloss.error))


if __name__ == '__main__':
    main(sys.argv)
