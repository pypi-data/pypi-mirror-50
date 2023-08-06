#!python3

import argparse
import sys
import os
import zipfile
import shutil
import venv
import subprocess

from os.path import join, abspath, dirname

EX_OK = getattr(os, "EX_OK", 0)
EX_USAGE = getattr(os, "EX_USAGE", 64)


IGNORE_FILE = ".robolab_ignore"

CURDIR = dirname(abspath(__file__))


class UsageError(Exception):
    def __init__(self, msg):
        self.msg = msg


def _list_files(root):
    res = list()
    for path, _, files in os.walk(root):
        for f in files:
            res.append(join(path, f)[len(root) + 1:])
    return res


def _curdir():
    return os.getcwd()


def _load_package_ignore():
    with open(join(_curdir(), IGNORE_FILE)) as f:
        return f.read().splitlines()


def version():
    with open(join(CURDIR, "..", "VERSION")) as f:
        ver = f.read().strip()

    return "robolab %s, python %s" % (ver, sys.version)


def package(args):
    project_dir = _curdir()

    all_files = set(_list_files(project_dir))
    ignored_files = set(_load_package_ignore())
    package_files = all_files - ignored_files

    archive_name = abspath(args.archive)

    with zipfile.ZipFile(archive_name, "w") as archive:
        for f in package_files:
            archive.write(f)

    print("Create package:\n  %s\n  -> %s" % (project_dir, archive_name))


def init(args):
    openrpa_path = dirname(os.path.abspath(__file__))
    template_path = join(openrpa_path, "template")

    project_dir = join(_curdir(), args.project)

    shutil.copytree(template_path, project_dir)

    os.chdir(args.project)
    venv.create(".venv", with_pip=True)

    with open(IGNORE_FILE, "w") as f:
        f.write("%s\n" % IGNORE_FILE)
        f.write("task.zip\n")
        for line in _list_files(join(project_dir, ".venv")):
            f.write("%s\n" % join(".venv", line))
    
    print("Init new project folder: %s" % (project_dir, ))

    if args.archive:
        with zipfile.ZipFile(join("..", args.archive), "r") as zip:
            zip.extractall()

        print("Deploy task archive: %s" % (args.archive, ))


def execute(args):
    if args.runtime:
        pass
    else:
        subprocess.call("run.bat", shell=True)


def main():
    parser = argparse.ArgumentParser(description="Command interface for Robolab tasks")
    parser.add_argument("--version", action="version", version=version(), help="print version information")
    subparsers = parser.add_subparsers()

    parser_init = subparsers.add_parser("init", help="Initialize new project folder here")
    parser_init.add_argument("project", help="project directory name")
    parser_init.add_argument("--archive", help="deploy with given task archive")
    parser_init.set_defaults(func=init)

    parser_package = subparsers.add_parser("package", help="Make task archive from current folder")
    parser_package.add_argument("archive", help="zip archive name")
    parser_package.set_defaults(func=package)

    parser_execute = subparsers.add_parser("execute", help="Execute task from current folder")
    parser_execute.add_argument("--runtime", help="execute in remote runtime")
    parser_execute.set_defaults(func=execute)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

    return EX_OK


if __name__ == "__main__":
    sys.exit(main())
