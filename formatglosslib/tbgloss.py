'''Toolbox gloss parser.

This module provides functions and classes for parsing and correcting
glosses within Toolbox files.

'''

# Encoding of the input file
INPUT_ENC = 'UTF-8'

# Combining diacritics in unicode
DIACRITICS = [u'\u0301',  # acute
              u'\u0300',  # grave
              u'\u030b',  # double acute
              u'\u030f',  # double grave
              u'\u030a',  # ring above
              u'\u0325',  # ring below
              u'\u0303',  # tilde above
              u'\u0334',  # tilde across
              u'\u0330',  # tilde below
              u'\u0308',  # trema above
              u'\u0324',  # trema below
              u'\u0304',  # bar above
              u'\u032c',  # hacek below
              u'\u0339',  # rounded
              u'\u031c',  # unrounded
              u'\u031f',  # advanced
              u'\u0320',  # retracted
              u'\u0329',  # syllabic
              u'\u032f',  # non-syllabic
              u'\u033c',  # linguolabial
              u'\u031d',  # raised
              u'\u031e',  # lowered
              u'\u0318',  # ATR
              u'\u0319',  # RTR
              u'\u032a',  # dental
              u'\u033a',  # apical
              u'\u033b',  # laminal
              u'\u033d',  # mid-centralised
              u'\u031a']  # unreleased


def true_len(string):
    r'''Return the 'true' length of a string without counting diacritics.

    :param string: input string
    :type  string: unicode
    :return:       length of the string
    :rtype:        unicode

    >>> true_len('Completely normal string')
    24
    >>> true_len(u'String with Diacritics: \xe9 e\u0301 \u0268 \u0268\u0301')
    31

    '''
    return len([char for char in string if char not in DIACRITICS])


def true_fill(string, length, filler=None):
    r'''Fill a string to a given length not counting diacritics.

    :param string: input string
    :type  string: unicode
    :param length: minimal length of the output string
    :type  length: int
    :param filler: character with which to fill the input string
    :type  filler: unicode
    :return:       lengthened string
    :rtype:        unicode

    >>> true_fill('ASCII', 10, '!')
    'ASCII!!!!!'
    >>> true_fill(u'dia\u0308critic', 15)
    u'dia\u0308critic      '

    '''
    if not filler:
        filler = ' '
    tail_len = max(0, length - true_len(string))
    return string + tail_len * filler


class MorphemeMapError(Exception):
    '''Error raised during the process of mapping morphemes to words.'''


class GlossError(Exception):
    '''Error raised during the interlinearisation process.'''


class MorphemeMap(object):
    r'''Two-way dictionary that maps words and morphemes to each other.

    This class scans a segmented line and assignes words to morphemes and vice
    versa:

    >>> word_line = '\\t das gut gebaute Haus'
    >>> morpheme_line = '\\mb das gut ge- bau -t -e Haus'
    >>> morph_map = MorphemeMap(word_line, morpheme_line)
    >>> morph_map.get_word(4)
    3
    >>> morph_map.get_morphemes(3)
    [3, 4, 5, 6]

    This mapping requires that every morpheme has to be assigned to exactly one
    word and that every word has to be assigned at least one morpheme,
    otherwise an exception is raised:

    >>> word_line = '\\t das sehr gut gebaute Haus'
    >>> morpheme_line = '\\mb das gut ge- bau -t -e Haus'
    >>> morph_map = MorphemeMap(word_line, morpheme_line)
    Traceback (most recent call last):
        ...
    MorphemeMapError: could not assign all words to morphemes

    '''

    def __init__(self, word_line, morpheme_line):
        '''Initialise morpheme map.

        :param word_line:     line containing complete words
        :type  word_line:     unicode
        :param morpheme_line: line containing single morphemes
        :type  morpheme_line: unicode

        '''
        words = word_line.split()
        morphemes = morpheme_line.split()
        word_index = 0
        word_end = False
        self.mapping = list()
        for morpheme in morphemes:
            # compound words are glossed 'first - second' in Toolbox
            if morpheme == '-':
                word_end = False
            if word_end and not morpheme.startswith('-'):
                word_index += 1
                word_end = False
            if not morpheme.endswith('-'):
                word_end = True
            self.mapping.append(word_index)
        if word_index < len(words) - 1:
            raise MorphemeMapError('could not assign all words to morphemes')
        if word_index > len(words) - 1:
            raise MorphemeMapError('could not assign all morphemes to a word')

    def get_word(self, index):
        '''Return the associated word for a given morpheme.

        :param index: index of the morpheme
        :type  index: int
        :return:      index of the associated word
        :rtype:       int

        '''
        return self.mapping[index]

    def get_morphemes(self, index):
        '''Return the associated morphemes for a given word.

        :param index: index of the word
        :type  index: int
        :return:      indices of all associated morphemes
        :rtype:       list of int

        '''
        return [morpheme
                for morpheme, word in enumerate(self.mapping)
                if word == index]


class ToolboxGloss(object):  # pylint: disable=R0903
    r'''Representation of a gloss in Toolbox.

    This class parses and realigns a single Toolbox gloss:

    >>> text_line = '\\t das blaue Haus'
    >>> gloss_lines = ['\\mb das blau -e Haus',
    ...                '\\gl the blue -N.SG house',
    ...                '\\ps no a -ai n']
    >>> print ToolboxGloss(text_line, gloss_lines)
    \t  das blaue      Haus
    \mb das blau -e    Haus
    \gl the blue -N.SG house
    \ps no  a    -ai   n

    Error handling:  When something goes wrong, the gloss is printed
    unchanged.

    >>> text_line = '\\t das blaue    Haus'
    >>> gloss_lines = ['\\mb das blau -e',
    ...                '\\gl   the blue -N.SG house',
    ...                '\\ps no a -ai n']
    >>> tb_gloss = ToolboxGloss(text_line, gloss_lines)
    >>> print tb_gloss
    \t das blaue    Haus
    \mb das blau -e
    \gl   the blue -N.SG house
    \ps no a -ai n
    >>> print tb_gloss.error
    could not assign all words to morphemes

    '''

    def __init__(self, text_line, gloss_lines):
        '''Initialise ToolboxGloss.

        :param text_line:   line containing complete words
        :type  text_line:   unicode
        :param gloss_lines: lines segmented into morphemes
        :type  gloss_lines: list of unicode

        '''
        self.is_faulty = False
        self.error = None
        self.text_line = text_line
        self.gloss_lines = gloss_lines
        self.word_width = None
        self.morph_width = None
        try:
            self.morph_map = MorphemeMap(text_line, gloss_lines[0])
            self._calc_morph_widths()
            self._calc_word_widths()
        except MorphemeMapError as index_error:
            self._error(str(index_error))
        except GlossError as gloss_error:
            self._error(str(gloss_error))

    def _error(self, message=None):
        '''Set error message and mark gloss as faulty.

        :param message: error message
        :type  message: str

        '''
        self.is_faulty = True
        if message:
            self.error = message
        elif not self.error:
            self.error = 'Error while interlinearising'

    def _calc_morph_widths(self):
        '''Calculate the morpheme column widths in the gloss'''
        morphemes = [line.split() for line in self.gloss_lines]
        if len(set(len(line) for line in morphemes)) > 1:
            raise GlossError('Numbers of morphemes did not match between segmented lines')  # pylint: disable=C0301
        self.morph_width = [max(true_len(line[i]) for line in morphemes)
                            for i in xrange(len(morphemes[0]))]

    def _calc_word_widths(self):
        '''Calculate the word column widths in the gloss'''
        words = self.text_line.split()
        self.word_width = list()
        for i in xrange(len(words)):
            morphemes = self.morph_map.get_morphemes(i)
            seg_length = sum(self.morph_width[j] for j in morphemes)
            seg_length += len(morphemes) - 1
            self.word_width.append(max(seg_length, true_len(words[i])))

    def __unicode__(self):
        '''Return Toolbox gloss as a unicode string'''
        if self.is_faulty:
            return '\n'.join([self.text_line] + self.gloss_lines)
        # format words
        words = self.text_line.split()
        wordsf = [true_fill(words[i], self.word_width[i])
                  for i in xrange(len(words))]
        wordsf = ' '.join(wordsf).strip()
        # format morphemes
        morphsf = list()
        for line in self.gloss_lines:
            morphemes = line.split()
            cols = list()
            for i in xrange(len(words)):
                column = self.morph_map.get_morphemes(i)
                columnf = [true_fill(morphemes[j], self.morph_width[j])
                           for j in column]
                columnf = true_fill(' '.join(columnf), self.word_width[i])
                cols.append(columnf)
            morphsf.append(' '.join(cols).strip())
        return '\n'.join([wordsf] + morphsf)

    def __str__(self):
        '''Return Toolbox gloss as a non-unicode string'''
        return self.__unicode__().encode(INPUT_ENC)


class ToolboxFile(object):  # pylint: disable=R0903
    r'''Representation of a Toolbox text file.

    This class takes a list of lines as an input and reformats them in order to
    correct the alignment of Toolbox glosses and remove unneeded white space.
    The input lines have to be in unicode which is the encoding used internally
    by the class.  The reformatted Toolbox file can be accessed by both the
    str() and the unicode() function.

    Within the ToolboxFile class, each line is a ToolboxLine object.  The class
    scans the file and wraps Toolbox lines belonging to a gloss in a
    ToolboxGloss object:

    >>> lines = ['\\ref 001',
    ...          '\\t das blaue Haus',
    ...          '\\mb das blau -e Haus',
    ...          '\\gl the blue -N.SG house',
    ...          '\\ps no a -ai n',
    ...          '\\f  The blue house']
    >>> tb_file = ToolboxFile(lines)
    >>> print tb_file.lines
    ['\\ref 001', <__main__.ToolboxGloss object ...>, '\\f  The blue house']
    >>> print tb_file
    \ref 001
    \t  das blaue      Haus
    \mb das blau -e    Haus
    \gl the blue -N.SG house
    \ps no  a    -ai   n
    \f  The blue house

    '''

    def __init__(self, lines=None):
        '''Initialise ToolboxFile.

        :param lines: lines of the file
        :type  lines: list of unicode

        '''
        self.lines = list()
        if lines:
            self.lines = lines
        index = 0
        while index < len(self.lines):
            try:
                if (self.lines[index].startswith('\\t ') and
                        self.lines[index + 1].startswith('\\mb ') and
                        self.lines[index + 2].startswith('\\gl ') and
                        self.lines[index + 3].startswith('\\ps ')):
                    gloss = ToolboxGloss(self.lines[index],
                                         self.lines[index + 1:index + 4])
                    self.lines = (self.lines[:index] +
                                  [gloss] +
                                  self.lines[index + 4:])
            except IndexError:
                break
            index += 1

    def __len__(self):
        '''Return length of the toolbox file'''
        return len(self.lines)

    def __delitem__(self, key):
        '''Delete line from a Toolbox file'''
        del self.lines[key]

    def __getitem__(self, key):
        '''Return line of a Toolbox file'''
        return self.lines[key]

    def __setitem__(self, key, new_line):
        '''Exchange a line in the Toolbox file'''
        self.lines[key] = new_line

    def __iter__(self):
        '''Return iterator of the toolbox file'''
        return self.lines

    def __str__(self):
        '''Return Toolbox file as a non-unicode string'''
        return self.__unicode__().encode(INPUT_ENC)

    def __unicode__(self):
        '''Return Toolbox file as a unicode string'''
        return '\n'.join(unicode(line) for line in self.lines)

    def get_glosses(self):
        '''Return list of glosses in the Toolbox file'''
        return [line for line in self.lines if isinstance(line, ToolboxGloss)]


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
