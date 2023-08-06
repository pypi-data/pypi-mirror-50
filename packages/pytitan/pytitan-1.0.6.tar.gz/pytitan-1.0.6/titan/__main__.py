# coding: utf-8
import click
import os
from shutil import copytree, copy2, copystat


@click.command()
def execute():
    dst = os.getcwd()
    src = os.path.join(os.path.dirname(__file__), "templates")
    names = os.listdir(src)

    for name in names:
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)


        if os.path.isdir(srcname):
            copytree(srcname, dstname)
        else:
            copy2(srcname, dstname)
        print("[INFO]:%s" % dstname)

    copystat(src, dst)


if __name__ == '__main__':
    execute()
