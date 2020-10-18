import unittest
from io import BufferedWriter, BufferedReader


class TestCodec(unittest.TestCase):
    def writer(self) -> BufferedWriter:
        file: str = "/d/tmp/seria.test"
        return open(file, "wb")

    def reader(self) -> BufferedReader:
        file: str = "/d/tmp/seria.test"
        return open(file, "rb")