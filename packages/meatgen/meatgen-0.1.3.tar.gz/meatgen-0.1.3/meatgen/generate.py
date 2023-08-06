import csv
import os
import pathlib
import typing

def generate(file: 'FileLike', delimiter: str, keys: typing.List[str]) -> typing.List[str]:
    reader = csv.reader(file, delimiter=delimiter)
    lookup = {}
    for row in reader:
        if len(row) != 2:
            continue
        lookup[row[0]] = row[1]

    return [lookup[key] for key in keys]
