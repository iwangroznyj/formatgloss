#! /usr/bin/env python

'''Formatgloss setup script.

Uses Distutils2 in order to install the formatgloss package or create
distributable packages.

'''


from distutils.core import setup
try:
    import py2exe
except ImportError:
    HAS_PY2EXE = False
else:
    HAS_PY2EXE = True


description = '''Reformatter of text files by the fieldwork software Toolbox.

The linguistic software Toolbox can produce interlinearised glosses of
data acquired during fieldwork.  However glosses containing combining
diacritics are often misaligned.

The present script scans text files for Toolbox glosses and realigns
them taking diacritics into consideration.  It comes with a command-line
as well as with a GUI written in wxPython.

'''

# TODO url, download_url
config = {'name': 'Formatgloss',
          'version': '1.0',
          'author': 'Johannes Englisch',
          'author_email': 'cyberjoe0815@hotmail.com',
          'description': 'Reformats glosses in Toolbox files',
          'long_description': description,
          'platform': 'any',
          'license': 'MIT License',
          'classifiers': ['Development Status :: 4 - Beta',
                          'Environment :: Console',
                          'Environment :: MacOS X :: Carbon',
                          'Environment :: Win32 (MS Windows)',
                          'Environment :: X11 Applications :: GTK',
                          'Intended Audience :: Science/Research',
                          'License :: OSI Approved :: MIT License',
                          'Operating System :: OS Independent',
                          'Programming Language :: Python :: 2',
                          'Topic :: Text Processing :: Linguistic'],
          'packages': ['formatglosslib'],
          'scripts': ['formatgloss_cli.py', 'formatgloss.pyw'],
          'requires': ['wxPython']}

config_py2exe = {'console': ['formatgloss_cli.py'],
                 'windows': ['formatgloss.pyw']}
py2exe_options = {'dist_dir': 'dist/%s-%s-win32' % (config['name'],
                                                    config['version']),
                  'bundle_files': 1}

if HAS_PY2EXE:
    config.update(config_py2exe)
    if not config.has_key('options'):
        config['options'] = dict()
    config['options']['py2exe'] = py2exe_options

setup(**config)
