# -*- coding: utf-8 -*-
import codecs
import os
import shutil


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)


def ig_f(directory, files):
    return [f for f in files if os.path.isfile(os.path.join(directory, f))]


class Converter:

    def __init__(self, **kwargs):
        self.block_size = kwargs.get("block_size", 1048576)
        self.input_encoding = kwargs.get("input_encoding", "cp1252")
        self.output_encoding = kwargs.get("output_encoding", "utf-8")

    def __convert(self, filename: str):
        with codecs.open(f"{filename}", "r", self.input_encoding) as sourceFile:
            print(filename)
            with codecs.open(f"output/{filename[5:]}", "w", "utf-8") as targetFile:
                try:
                    while True:
                        contents = sourceFile.read(self.block_size)
                        if not contents:
                            break
                        targetFile.write(contents)
                except:
                    pass

    def process(self):
        if not os.path.isdir("work"):
            print("work directory doesn't exist...")
            return
        if os.path.isdir("output"):
            print("Please delete the output directory")
            return

        copytree("work", "output", False, ig_f)

        for root, dirs, files in os.walk("work"):
            path = root.split(os.sep)
            for file in files:
                self.__convert(os.path.join(root, file))


if __name__ == "__main__":
    print("Utf-8 converter - Metin2")
    print("Please, put your file in 'work' directory, before starting")
    input("Press any key to continue...")
    print("Let's work !")

    c = Converter(
        block_size=1048567,
        input_encoding="cp1250",
        output_encoding="utf-8"
    )
    c.process()

    print("Done ! ")
