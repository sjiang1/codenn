# from bs4 import BeautifulSoup
import os
import antlr4
from java.JavaTemplate import parseJava
import re
import pdb
import pickle
from itertools import izip

import configparser, argparse

def parse_args():
    parser = argparse.ArgumentParser(description='prepare data files for nematus to run.')
    parser.add_argument('--config', nargs=1, help='the config file, see nematus.ini as an example', required=True)
    args = parser.parse_args()        
    configfile = args.config[0]
    logger.info("config file: " + configfile)
    
    return {'configfile':configfile,}

def parse_config_var(config, var_name):
    if not 'PREPDATA' in config:
        logger.error("config file does not have section: PREPDATA. Exit.")
        sys.exit(1)
        
    if config['PREPDATA'][var_name]:
        var_val = config['PREPDATA'][var_name]
        logger.info("parse config: " + var_name + "=" + var_val)
        return var_val
    else:
        logger.error("parse config: no " + var_name + " configured. Exit.")
        sys.exit(1)


def parse_config(configfile):
    config = configparser.ConfigParser()
    config.read(configfile)
    
    dataprep = parse_config_var(config, 'dataprep')
    outdir   = parse_config_var(config, 'outdir')
    # src_vocabsize = parse_config_var(config, 'vocabsize_src')
    # tgt_vocabsize = parse_config_var(config, 'vocabsize_tgt')
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    
    return {'dataprep': dataprep,
            'outdir'  : outdir,}
            # 'vocabsize_src':src_vocabsize,
            # 'vocabsize_tgt':tgt_vocabsize,}

def check_outputfiles(outputfiles):
    for key in outputfiles:
        fname=outputfiles[key]
        if not os.path.isfile(fname):
            return

    logger.info("!!!!\n!!!!the data files exists. Exit.\n!!!!")
    sys.exit()
    
if __main__ == '__main__':

    args      = parse_args()
    config    = parse_config(args['configfile'])
    outputdir = config['outdir'] # this is the output dir for prepdata_nematus, which is the input for this script.
    
    params = {
      "trainfile_src" : "train.src.txt",
      "trainfile_tgt" : "train.tgt.txt",
      "validfile_src" : "valid.src.txt",
      "validfile_tgt" : "valid.tgt.txt",
      "testfile_src"  : "test.src.txt",
      "testfile_tgt"  : "test.tgt.txt"}

    for key in params:
      params[key] = os.path.join(outputdir, params[key])
    
    
    def output(outputfile, inputfile_src, inputfile_tgt):
      f = open(outputfile, 'w')
      with open(inputfile_src, 'r') as src_f, open(inputfile_tgt, 'r') as tgt_f:
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
    output(os.path.join(outputdir, 'train.txt'), params['trainfile_src'], params['trainfile_tgt'])
    output(os.path.join(outputdir, 'valid.txt'), params['validfile_src'], params['validfile_tgt'])
    output(os.path.join(outputdir, 'test.txt'), params['testfile_src'], params['testfile_tgt'])
