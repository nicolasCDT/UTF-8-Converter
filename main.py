#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Nicolas Coudert"
__copyright__ = "Copyright 2022"
__credits__ = ["Nicolas Coudert"]
__version__ = "0.1"
__maintainer__ = "Nicolas Coudert"
__email__ = "nicolas@coudert.pro"
__status__ = "Development"

# Imports
import codecs
import os
import shutil
import glob
from typing import TypeVar, Dict, AnyStr, List

INPUT_DIRECTORY: str = "work"
OUTPUT_DIRECTORY: str = "output"

# Encoding for each folder in input directory
ENCODING_FOR_PATH: Dict[str, str] = {
	'cz': 'cp1250',
	'ru': 'cp1251',
	'fr': 'cp1252',
	'pt': 'cp1252',
	'dk': 'cp1252',
	'gr': 'cp1253'
}


def ignore_files(directory: str, files: List) -> List:
	"""Uses to ignore all files in shutil.copytree (ignore function)"""
	return [f for f in files if os.path.isfile(os.path.join(directory, f))]


# Typing for FileConverter class
TFileConverter = TypeVar("TFileConverter", bound="FileConverter")


class FileConverter:
	"""Class uses to convert a file to an another encoding"""
	def __init__(self: TFileConverter, file_path: str, **kwargs) -> None:
		"""Initialization of FileConverter class"""
		self.file_path: str = file_path
		self.input_encoding = kwargs.get("input_encoding", "cp1250")
		self.output_encoding = "utf-8"
		self.block_size = kwargs.get("block_size", 1048576)
		self.content: AnyStr = ""

	def process(self: TFileConverter, output_file: str = "") -> None:
		"""Read old file and write the new with right encoding"""
		with codecs.open(self.file_path, "r+", encoding=self.input_encoding, errors="ignore") as current_file:
			with codecs.open(output_file, "w+", encoding=self.output_encoding) as new_file:
				try:
					while True:
						contents = current_file.read(self.block_size)
						if not contents:
							break
						new_file.write(contents)
				except Exception as e:
					print("Error on file: ", self.file_path, " encoding: ", self.input_encoding)
					raise e


def main() -> None:
	"""Main entry"""
	# Check if output folder exists
	if os.path.exists(OUTPUT_DIRECTORY):
		shutil.rmtree(OUTPUT_DIRECTORY)

	shutil.copytree(INPUT_DIRECTORY, OUTPUT_DIRECTORY, ignore=ignore_files)

	for filename in glob.iglob(f'{INPUT_DIRECTORY}/' + '**/*.txt', recursive=True):
		path = os.path.normpath(filename.replace(f"{INPUT_DIRECTORY}/", ""))

		encoding = ENCODING_FOR_PATH.get(path.split(os.sep)[0])
		if encoding:
			f: FileConverter = FileConverter(
				filename,
				input_encoding=encoding
			)
		else:
			f: FileConverter = FileConverter(
				filename
			)
		f.process(filename.replace(f"{INPUT_DIRECTORY}/", f"{OUTPUT_DIRECTORY}/", 1))


if __name__ == '__main__':
	main()
