#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
scan a given directory for files an sort them by extension
for jessy lohmann who has lost important photos
"""

import argparse
import configparser
import getpass
import hashlib as hs
import logging
import os
import pathlib
import shutil

__author__ = "Daniel Pust"
__copyright__ = "Copyright 2022, nightshadows"
__credits__ = [""]
__license__ = "all rights reserved"
__version__ = "0.0.5"
__maintainer__ = "Daniel Pust"
__email__ = "pust.daniel@outlook.com"
__status__ = "Development"

try:
    FORMAT = "%(asctime)-15s %(levelname)s: %(message)s"
    logging.basicConfig(filename="filesort.log",
                        format=FORMAT, level=logging.INFO)
    logging.info('Start')
    os.system('clear')

    print('*'*80)
    print('* ' + __copyright__ + ' (w) ' +
          __author__ + ' / ' + __license__)
    print('*'*80+'\n')

    parser = argparse.ArgumentParser(description=__copyright__ + ' ->\
         filesort create directorys with the name of the file extensions\
         and copy the files there.')
    # dryrun default=false
    parser.add_argument("--no-dryrun", default=False, action="store_true",
                        help="set to deactivate dryrun")
    # debug default=false
    parser.add_argument("--debug", default=False, action="store_true",
                        help="activate debug mode")
    # actionmode copy/move
    parser.add_argument("-m", "--mode", choices=['copy', 'move'],
                        help="select mode 'copy' or 'move'", default='copy')
    args = parser.parse_args()

    if not args.no_dryrun:
        logging.info('!!! DRYRUN !!!')

    # read config file
    config = configparser.ConfigParser()
    config.read('filesort.ini')

    source_path = '~/'
    source_path = config.get('path', 'source')

    dummy = '~/filesort'
    dummy = config.get('path', 'target')
    target_path = os.path.join(dummy, "data")

    unwanted = []
    unwanted_raw = config.get('extensions', 'unwanted')
    unwanted = unwanted_raw.lower().split(",")

    # test source path
    if not os.path.isdir(source_path):
        msg = "non existing source path {}".format(source_path)
        raise UserWarning(msg)

    # test target path
    if os.path.isdir(target_path):
        msg = "existing target path {}".format(target_path)
        raise UserWarning(msg)

    # create target path
    try:
        # os.makedirs(target_path, mode = 0o777, exist_ok=True)
        pass
    except Exception as e:
        raise UserWarning(e)

    print("walking on \"{0}\" please wait".format(source_path))

    # create extensions list only with wanted and lower extensions
    extensions = []
    for root, dirs, files in os.walk(source_path):
        for name in files:
            ext = pathlib.Path(name).suffix[1:].lower()
            if (len(ext) > 0) and \
                (ext not in unwanted) and \
                    (ext not in extensions):
                extensions.append(ext)
                print("a", end='')
            else:
                print(".", end='')
    print("\n")

    # create target pathes
    for ext in extensions:
        try:
            dummy = os.path.join(target_path, ext)
            if args.no_dryrun:
                os.makedirs(dummy, mode=0o777, exist_ok=True)
        except Exception as e:
            raise UserWarning(e)
        msg = "created path {}". format(dummy)
        print(msg)
        logging.info(msg)
    print("")

    # copy files to pathes with hash and logging in logfile
    file_count = 0
    for root, dirs, files in os.walk(source_path):
        for name in files:
            ext = pathlib.Path(name).suffix[1:].lower()
            if ext in extensions:
                source = os.path.join(root, name)
                target = os.path.join(target_path, name)
                # copy or move file
                if args.no_dryrun:
                    if args.mode == 'copy':
                        shutil.copyfile(source, target)
                    if args.mode == 'move':
                        shutil.move(source, target)
                # hash
                hash_md5 = hs.md5()
                with open(source, 'rb') as file:
                    buffer = file.read()
                    hash_md5.update(buffer)
                    msg = "copy/moved file {} to {} [HASH;{}]".format(
                        source, target, hash_md5.hexdigest())
                    print(msg)
                    logging.info(msg)
                    # count files
                    file_count += 1
    # write counter to log
    logging.info("Number of moved/copied files: {}".format(file_count))

except Exception as e:
    logging.error(e)
    print(e)

if not args.no_dryrun:
    logging.info('!!! DRYRUN !!!')

logging.info('Stop')
