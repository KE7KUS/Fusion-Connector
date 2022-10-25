#!/usr/bin/python3

# Fusion Connector
# Utility to interface with Yaesu System Fusion radios via the SD card
# Copyright 2022 Kurt Kochendarfer, KE7KUS

# ===SD CARD FILE LIST===
# QSOMNG.DAT:       Contains a counter of all the messages/images/group messages stored on the SD card. Counter does not change if messages/images are deleted. Empty = 0xff.
# QSOMSG.DAT:       Plaintext message body data for each message.  If a message is deleted from the radio, it is NOT deleted from this file.  Each message is 80 bytes.  Empty = 0x20.
# QSOMSGDIR.DAT:    Contains metadata about each message contained in the QSOMSG.DAT file.  Each metadata block is 128 bytes long.  Each block starts with 0x61.  Empty = 0x20 except at end of 128 byte block = 0x00.
# QSOMSGFAT.DAT:    Pointer to each individual message in QSOMSG.DAT.  Each message pointer is 4 bytes.  If message is deleted via radio UI, values replaced with 0xff.  File does not shrink.

# QSOPCTDIR.DAT:   Contains metadata about each picture contained on the SD card.  Each metadata block is 128 bytes long. Each block starts with 0x70.  Empty = 0x20 except at end of block = 0x00.
# QSOPCTFAT.DAT:   Pointer to each individual picture in the PICTURE folder.  Each pointer is 4 bytes.  If picture deleted via radio UI, values replaced with 0xff.  File does not shrink.

# ===FORMATS===
# DATE:  YMDHMS (6 byte HEX)
# GPS:   NDDDMMMMWDDDMMMM (LAT 10 bytes ASCII / LON 10 bytes ASCII - decimal secs with no .)
# PCT FILENAME:  M<xxxxx><nnnnnn>.JPG (xxxxx = Radio Hex ID / nnnnnn = incremental number) (16 bytes ASCII)

#===FILE STRUCTURE===

#-0 FTM400D-
#         |
#         |-1 BACKUP-
#                  |
#                  |-2 CLONE
#                  |-2 MEMORY
#                  |-2 SETUP
#         |-1 GPSLOG
#         |-1 PHOTO
#-0 GM-----
#         | - ???
#-0 PHOTO--
#         |-INDIV PHOTO FILES
#-0 QSOLOG-
#         |-QSOMNG.DAT
#         |-QSOMSG.DAT
#         |-QSOMSGDIR.DAT
#         |-QSOMSGFAT.DAT
#         |-QSOPCTDIR.DAT
#         |-QSOPCTFAT.DAT 

# ===NOTES===
# 1)  In general, with the Yaesu file system, deleting data via the radio UI does not actually delete the data from the SD card.  Rather, pointers to the data are deleted in associated files on the SD card.

import binascii
import os
from pathlib import Path, PurePath
from datetime import datetime
from yaesu_directory import ds

directory = []

def parse(L, path = PurePath() / 'ROOT'):

  for i in L:
    if type(i) == list:
      parent_index = L.index(i) - 1
      path = path / PurePath(L[parent_index])
      parse(i, path)
      path = path.parent
    else:
      directory.append(path / PurePath(i))    
  return directory
  
class FileSystem:

  """Class for manipulating System Fusion SD card file/directory structure."""

  def makeSdDirectoryStruct(location = PurePath(), radio = 'FTM400XDR'):

    """Function to create System Fusion directory structure at specified location. """
  
    fs = ds["ftm400xdr"]
    structure = parse(fs)
    print(structure)
    for s in structure:
      os.makedirs(s, exist_ok=True)
      print(s)
    print('File system complete.')

class Message:

  """Class for file handling of System Fusion text messages."""

  def makeQsoMng(msg_count = 0, pic_count = 0, gm_count = 0):

    """Function to create QSOMNG.dat system file."""
    
  def makeQsoMsg(msg = b''):

    """Function to create QSOMSG.dat system file."""

    pass

  def makeQsoMsgDir():

    """Function to create QSOMSGDIR.dat system file."""

    pass

  def makeQsoMsgFat():

    """Function to create QSOMSGFAT.dat system file."""

    pass

class Picture:
  
  """Class to handle System Fusion image files."""

  def makeQsoPctDir():

    """Function to create QSOPCTDIR.dat system file."""

    pass

  def makeQsoPctFat():
  
    """Function to create QSOPCTFAR.dat system file."""

    pass

if __name__ == "__main__":
  FileSystem.makeSdDirectoryStruct()
