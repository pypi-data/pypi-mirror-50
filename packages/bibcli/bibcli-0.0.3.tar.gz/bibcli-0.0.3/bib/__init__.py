#!/usr/bin/python3

# This file is part of bib.
#
# bib is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# bib is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with bib. If not, see <https://www.gnu.org/licenses/>.

import argparse
import json
import os
import sys # For general system interactions
from termcolor import colored # For coloring terminal output
import subprocess # For spawning subprocesses
import shutil # For copying files
import slugify # For transforming IDs into directory names
import logging
import bibtexparser
import hashlib # For computing paths to files (see the import command)
import re # For querying items
import confuse
from bibtexparser.bparser import BibTexParser

class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors
    Adapted from https://stackoverflow.com/a/56944256/11672072"""

    # format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    format = "%(levelname)s: %(message)s"

    FORMATS = {
        logging.DEBUG: colored(format, 'grey'),
        logging.INFO: colored(format, 'white'),
        logging.WARNING: colored(format, 'yellow'),
        logging.ERROR: colored(format, 'red'),
        logging.CRITICAL: colored(format, 'red', attrs=['bold'])
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# addfunc
def add(config, bib, logger):
    # 1. Try to parse file
    addbibparser = BibTexParser(common_strings = True)
    addbibparser.ignore_nonstandard_types = False
    addbibparser.homogenise_fields = False
    path = config['path'].as_filename()
    try:
        with open(path, 'r') as f:
            new_items = bibtexparser.load(f, addbibparser)
    except Exception as e:
        logger.warning('Couldn\'t parse {}: {}'.format(path, e))
        sys.exit(1)
    # 2. Add to library
    for b in new_items.entries:
        if b['ID'] in bib.entries_dict:
            logger.error('Item {} already in library'.format(b['ID']))
        else:
            bib.entries.append(b)
            logger.info('Added {}'.format(b['ID']))

# importfunc
def stringMD5(s):
    hash_object = hashlib.md5(s.encode('utf-8'))
    return hash_object.hexdigest()
def fileMD5(f):
    hash_md5 = hashlib.md5()
    with open(f, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
def importfunc(config, bib, logger):
    # 1. Check if item exists
    ID = config['id'].get()
    path = config['path'].as_filename()
    storage = config['storage'].as_filename()
    if not ID in bib.entries_dict:
        logger.critical('No item with id {}'.format(ID))
        sys.exit(1)
    # 2. Check if file exists
    if not os.path.isfile(path):
        logger.critical('{}: no such file'.format(path))
        sys.exit(1)
    # 3. Determine new path
    # 3.1 Determine base path
    base_path = os.path.join(storage, slugify.slugify(ID) + '-' + stringMD5(ID))
    if not os.path.exists(base_path):
        os.mkdir(base_path)
        logger.info('mkdir {}'.format(base_path))
    # 3.2 Determine hash
    file_hash = fileMD5(path)
    # 3.3 Determine extension
    filename, extension = os.path.splitext(path)
    extension = extension.lower()
    # 3.4 Calculate new path
    new_path = os.path.join(base_path, file_hash + extension)
    # 4. Copy or move file
    shutil.copy(path, new_path)
    # 5. Set `file` attribute
    bib.entries_dict[ID]['file'] = new_path
    # 6. Verbose output
    logger.info('Copy {} into {}'.format(path, new_path))

# listfunc
def parseFilter(f):
    if ':' in f:
        fields = f.split(':')
        key = fields[0]
        try:
            pattern = re.compile(fields[1])
        except Exception as e:
            logger.critical('Error when parsing filter {}: {}'.format(f, e))
            sys.exit(1)
        def filterFunc(i):
            try:
                return key in i and pattern.search(i[key])
            except Exception as e:
                logger.critical('Error when filtering list with filter {}: {}'.format(f, e))
                sys.exit(1)
        return filterFunc
    else:
        return (lambda x : True)
def filterItems(r, f):
    return filter(parseFilter(f), r)
def listfunc(config, bib, logger):
    filters = config['filters'].get()
    results = bib.entries
    # 1. Filter items
    for f in filters:
        results = filterItems(results, f)
    # 2. Print results
    for r in results:
        header_string = '{id} ({entrytype})'
        attribute_string = '  {key}: {value}'
        # header = colored(r['ID'], attrs=['bold']) + ' ' +  colored('(' + r['ENTRYTYPE'] + ')', attrs=['underline'])
        print(header_string.format(id=r['ID'], entrytype=r['ENTRYTYPE']))
        for k in r:
            if k != 'ID' and k != 'ENTRYTYPE':
                print(attribute_string.format(key=colored(k, attrs=['bold']), value=r[k]))

# readfunc
def readfunc(config, bib, logger):
    ID = config['id'].get()
    if ID in bib.entries_dict:
        if 'PDFREADER' in os.environ:
            if 'file' in bib.entries_dict[ID]:
                try:
                    reader = os.environ['PDFREADER']
                    filepath = bib.entries_dict[ID]['file']
                    subprocess.Popen([reader, filepath])
                except Exception as e:
                    logger.critical('Couldn\'t open PDF: {}'.format(e))
                    sys.exit(1)
            else:
                logger.critical('Item {} has no `file` field'.format(ID))
                sys.exit(1)
        else:
            logger.critical('Enviroment variable PDFREAD not set')
            sys.exit(1)
    else:
        logger.critical('No item with ID {} in library'.format(ID))
        sys.exit(1)

# notefunc
def notefunc(config, bib, logger):
    ID = config['ID'].get()
    storage = config['storage'].get()
    if ID in bib.entries_dict:
        if 'EDITOR' in os.environ:
            editor = os.environ['EDITOR']
            base_path = os.path.join(storage, slugify.slugify(ID) + '-' + stringMD5(ID))
            if not os.path.exists(base_path):
                os.mkdir(base_path)
                logger.info('mkdir {}'.format(base_path))
            path = os.path.join(base_path, 'note.md')
            subprocess.call([editor, path])
        else:
            logger.critical('No EDITOR enviroment variable set')
            sys.exit(1)
    else:
        logger.critical('No item with ID {}'.format(ID))
        sys.exit(1)

# fieldsfunc
def fieldsfunc(config, bib, logger):
    fields = []
    for e in bib.entries:
        for k in e:
            if not k in fields:
                fields.append(k)
    for k in sorted(fields):
        print(k)

def main():
    # Top-level parser ====================================================
    parser = argparse.ArgumentParser(description='Command-line bibliography\
            management utility.')
    parser.add_argument('-v', '--verbose',
            action = 'store_true',
            help = 'Verbose mode')
    parser.add_argument('-b', '--bibpath',
            metavar = 'PATH',
            help = 'Path to bib file')
    # parser.add_argument('-c', '--config',
    #         metavar = 'PATH',
    #         help = 'Path to config file',
    #         default = CONFIG_FILE)
    parser.add_argument('-d', '--directory',
            metavar = 'PATH',
            dest = 'storage',
            help = 'Base directory where to store files')
    subparsers = parser.add_subparsers(
            metavar = 'command')
    # ======================================================================
    
    # add parser ===========================================================
    addparser = subparsers.add_parser('add',
            help='Add item to bibliography.')
    addparser.add_argument('path',
            help = 'Path to the bib file to be added')
    addparser.set_defaults(command=add)
    # ======================================================================
    
    # import parser ========================================================
    importparser = subparsers.add_parser('import',
            help = 'Import file and associate with item')
    importparser.add_argument('id',
            help = 'BibTeX ID for item')
    importparser.add_argument('path',
            help = 'Path to file')
    importparser.set_defaults(command=importfunc)
    # ======================================================================
    
    # list parser ==========================================================
    listparser = subparsers.add_parser('list',
            help = 'Query and list items')
    listparser.add_argument('filters',
            nargs='*',
            help = 'Filters for the item list')
    listparser.set_defaults(command=listfunc)
    # ======================================================================
    
    # read parser ==========================================================
    readparser = subparsers.add_parser('read',
            help = 'Open PDF associated with an item')
    readparser.add_argument('id',
            help = 'PDF\'s item ID')
    readparser.set_defaults(command=readfunc)
    # ======================================================================
    
    # fieldsparser =========================================================
    fieldsparser = subparsers.add_parser('fields',
            help = 'List fields available for querrying')
    fieldsparser.set_defaults(command=fieldsfunc)
    # ======================================================================
    
    # noteparser ===========================================================
    noteparser = subparsers.add_parser('note',
            help = 'Edit notes associated with item')
    noteparser.add_argument('id',
            help = 'Note\'s item ID')
    noteparser.set_defaults(command=notefunc)
    # ======================================================================
    
    args = parser.parse_args()
    
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    handler.setFormatter(CustomFormatter())
    logger.addHandler(handler)

    # Handle verbose mode
    if args.verbose:
        logger.setLevel(logging.INFO)
        logger.info('Verbose mode set')
    else:
        logger.setLevel(logging.WARNING)

    # Read configurations
    try:
        logger.info('Reading config file...')
        config = confuse.Configuration('bib', __name__)
        config.set_args(args)
    except confuse.ConfigError as e:
        logger.critical('Couldn\'t read config file: {}'.format(e))
        sys.exit(1)
   
    parser = BibTexParser(common_strings = True)
    parser.ignore_nonstandard_types = False
    parser.homogenise_fields = False

    # Read bibliography file (or create it, if it doesn't exist)
    # First, test if file is empty
    # (this has been addressed in https://github.com/sciunto-org/python-bibtexparser/issues/241#issue-470579334)
    # bibtexparser fails on empty files, at least for version 1.1.0
    try:
        bibpath = config['bibpath'].as_filename()
        logger.info('Bibpath determined to be {}'.format(bibpath))
    except confuse.NotFoundError as e:
        logger.critical('No bibligraphy file path provided: {}'.format(e))
        sys.exit(1)

    if (not os.path.exists(bibpath)) or (os.path.isfile(bibpath) and os.stat(bibpath).st_size == 0):
        logger.info('bib file {} does not exist or has zero length'.format(args.bibpath))
        if not os.path.exists(os.path.dirname(bibpath)):
            os.makedirs(os.path.dirname(bibpath))
        with open(bibpath, 'w+') as f:
            f.write(' \n')
    try:
        with open(bibpath, 'r') as f:
            logger.info('Reading bib file {}'.format(bibpath))
            bib = bibtexparser.load(f, parser)
    except Exception as e:
        logger.critical('Can\'t read bib file: {}'.format(str(e)))
        sys.exit(1)

    # Determine file storage directory path
    try:
        directory = config['storage'].as_filename()
    except confuse.NotFoundError as e:
        logger.critical('No storage directory either provided as argument of found in config file: {}'.format(e))
        sys.exit(1)

    # Create file storage directory, if it doesn't exist
    if not os.path.exists(directory):
        logger.info('File storage directory {} does not exist. Creating it...'.format(directory))
        os.makedirs(directory)
    
    # Critically exit if file storage directory path exists and is not a directory
    if not os.path.isdir(directory):
        logger.critical('{} is not a directory'.format(directory))
        sys.exit(1)

    # Perform command, if one was provided
    try:
        command = config['command'].get()
        command(config, bib, logger)
    except Exception as e:
        logger.info('No command provided: {}'.format(e))
    
   # Write to bibliography file
    try:
        with open(bibpath, 'w') as f:
            bibtexparser.dump(bib, f)
    except Exception as e:
        logger.critical('Can\'t write to bib file: {}'.format(e))
        sys.exit(1)

if __name__ == '__main__':
    main()
