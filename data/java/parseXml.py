# from bs4 import BeautifulSoup
import os
import antlr4
# from java.Java4Lexer import Java4Lexer
# from java.JavaTemplate import parseJava
import re
import pdb
import pickle
from itertools import izip

params = {
  "trainfile_src" : "/mnt/disks/funcom/data/train.src.txt",
  "trainfile_tgt" : "/mnt/disks/funcom/data/train.tgt.txt",
  "validfile_src" : "/mnt/disks/funcom/data/valid.src.txt",
  "validfile_tgt" : "/mnt/disks/funcom/data/valid.tgt.txt",
  "testfile_src"  : "/mnt/disks/funcom/data/test.src.txt",
  "testfile_tgt"  : "/mnt/disks/funcom/data/test.tgt.txt"}

def parseJava(line):
  # dummy
  return


def output(outputfile, inputfile_src, inputfile_tgt):
  f = open(outputfile, 'w')
  with open(params[inputfile_src], 'r') as src_f, open(params[inputfile_tgt], 'r') as tgt_f:
    for src_line, tgt_line in izip(src_f, tgt_f):
      src_line=src_line.strip()
      tgt_line=tgt_line.strip()
      try:
        parseJava(src_line)
        try:
          f.write('\t'.join(['0', '0', tgt_line, src_line, "0"]) + '\n')
        except:
          print("error")
      except:
        pass

      
  f.close()
  return



# Create training and validation and test sets
output('train.txt', 'trainfile_src', 'trainfile_tgt')
output('valid.txt', 'validfile_src', 'validfile_tgt')
output('test.txt' , 'testfile_src' , 'testfile_tgt' )
