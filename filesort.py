#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
scan a given directory for files an sort them by extension
for jessy lohmann who has lost important photos
"""

# TODO: pfad für die Suche
# TODO: dateiendungen die nicht erfasst werden sollen
# TODO: zielpfad, 'data' wird dort erstellt / prüfen wenn ziel existiert abbruch
# TODO: logfile mit allen files, hash und größe/datum
# TODO: erst ohne undelete danach mit
# TODO: immer dryrun nur parameter --DoIt macht wirklich was
# TODO: parameter für copy
# TODO: parameter für move

import configparser
import getpass
import hashlib as hs
import os
import pathlib
import shutil

__author__ = "Daniel Pust"
__copyright__ = "Copyright 2022, nightshadows"
__credits__ = [""]
__license__ = "all rights reserved"
__version__ = "0.0.1"
__maintainer__ = "Daniel Pust"
__email__ = "pust.daniel@outlook.com"
__status__ = "Development"

try:
    os.system('clear')
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
        #os.makedirs(target_path, mode = 0o777, exist_ok=True)
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
    print("")
    # create target pathes
    for ext in extensions:
        try:
            dummy = os.path.join(target_path, ext)
            os.makedirs(dummy, mode=0o777, exist_ok=True)
            pass
        except Exception as e:
            raise UserWarning(e)
        print("created path {}". format(dummy))

    # create logfile fs_date_time.log in folder 'target'
    # copy files to pathes with hash and logging in logfile
    for root, dirs, files in os.walk(source_path):
        for name in files:
            ext = pathlib.Path(name).suffix[1:].lower()
            if ext in extensions:
                source = os.path.join(root, name)
                target = os.path.join(target_path, name)
                # copy or move file
                print("copy file {} to {}".format(source, target))
                #TODO: copy or move
                #shutil.copyfile(source, target)
                # hash
                hash_md5 = hs.md5()
                with open(source, 'rb') as file:
                    buffer = file.read()
                    hash_md5.update(buffer)
                    print('hash', hash_md5.hexdigest())
                # logentry
                # count files

    # write counter to log

    raise UserWarning("\nend.")

except Exception as e:
    print(e)
