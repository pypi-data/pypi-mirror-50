"""Functions for folders2json."""
import os
from pathlib import Path
import json
from collections import defaultdict
import argparse


currentdir = os.getcwd()


def prep(version):
    """Get all the argparse stuff setup."""
    parser = argparse.ArgumentParser(description='simple generate json\
                                     for folder format')
    parser.add_argument('-r', '--root', dest='rootpath',
                        help='Set the root path', default=currentdir,
                        required=False)
    parser.add_argument('-w', '--windows', dest='windows', action='store_true',
                        default=False, help='Adds extra slash for file path.')
    parser.add_argument('--version', '-V', action='version',
                        version="%(prog)s " + version)
    args = parser.parse_args()

    return args


def GetFullPathFiles(rootpath):
    """Get all the files into a list."""
    fullpathfiles = list()
    for root, _, filenames in os.walk(rootpath):
        rel_dir = os.path.relpath(root, rootpath)
        for filename in filenames:
            fullpathfiles.append(os.path.join(rel_dir, filename))
    return fullpathfiles


def GetDevices(pathlist, rootpath):
    """Get unique device ids as keys in default dictionary."""
    deviceiddict = defaultdict(list)
    abs_dir = os.path.abspath(rootpath)
    for fullpath in pathlist:
        pathchunks = Path(fullpath).parts
        if len(pathchunks) > 3:
            absfull = os.path.join(abs_dir, fullpath)
            deviceiddict[pathchunks[3]].append(absfull)
    return deviceiddict


def GenerateJson(deviceiddict, win, fullpathfiles):
    """For each deviceid key, generate json."""
    finaldict = dict()
    for key, value in deviceiddict.items():
        absfullfinal = list()
        if win:
            for item in value:
                absfullfinal.append(f"file://{item}")
        else:
            for item in value:
                absfullfinal.append(f"file:/{item}")
        finaldict["urls"] = absfullfinal
        partsofpath = Path(fullpathfiles[0]).parts
        if len(partsofpath) > 3:
            finaldict["metadata"] = {
                "objective": partsofpath[0],
                "batch": partsofpath[1],
                "device": key
            }
        else:
            finaldict["metadata"] = {
                "objective": fullpathfiles[1].parts[0],
                "batch": fullpathfiles[1].parts[1],
                "device": key
            }
        finaldict["params"] = {}
        if os.path.exists(f"{key}.json"):
            os.remove(f"{key}.json")
        with open(f"{key}.json", "w+") as f:
            f.write(json.dumps(finaldict))
