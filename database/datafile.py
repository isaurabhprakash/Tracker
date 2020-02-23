import os
import struct
import numpy as np


# Right now we have fields that support just the int datatype
from PyQt5.QtWidgets import QMessageBox


class DataFile:
    def __init__(self, pFileName=None):

        self._fileName = pFileName
        if pFileName is None:
            self._file = None
        else:
            self.create_file(pFileName)

    def create_file(self, pFileName):
        self._fileName = pFileName

        # If the file already exists open it in read mode so that the existing data doesn't get erased. Else
        # create the file.
        if os.path.isfile(pFileName):
            self._file = open(pFileName, "rb+")

            # First we will bring all the data in memory and then write all back to the file
            # in case of modification
            self._file.seek(0, os.SEEK_SET)
        else:
            self._file = open(pFileName, "wb+")

        return self._file

    def write_field(self, pFieldId, pValue):
        self._file.write(struct.pack('i', int(pFieldId)))
        self._file.write(struct.pack('i', int(pValue)))
        self._file.flush()

    # Since everything is to be brought in-memory, we read the entire file.
    def read_file(self):
        # Move to the beginning of the file.
        self._file.seek(0, os.SEEK_SET)

        # Since the written data is packed, numpy is being used to read it.
        # Also, unlike struct, with numpy we can read the entire file into a list in one go.
        readData = np.fromfile(self._file, dtype=int)
        print("Read Data : ")
        return readData

    def read_ini_file(self):
        return self._file.read()

    def write_ini_file(self, pInstanceName):
        # So that we don't end up writing a number of last instances
        self._file.seek(0)
        self._file.truncate(0)

        self._file.write(pInstanceName.encode('ascii'))
        self._file.flush()

    def close_file(self):
        self._file.flush()
        self._file.close()
