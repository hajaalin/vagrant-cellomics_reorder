#!/usr/bin/python
import datetime
import glob
import logging
import math
from optparse import OptionParser
import os
import re
import string
import subprocess
import sys
import time
import traceback

from mdb_export import mdb_export

logger = None

DRY_RUN = False

# input directory
INPUT_ROOT = None

def _run_and_log(cmd):
    logger.info(cmd)
    if not DRY_RUN:
        os.system(cmd)

def _always_run_and_log(cmd):
    logger.info(cmd)
    os.system(cmd)

def reorder(dir_in):
    start_time = time.time()
    logger.debug(INPUT_ROOT + " " + dir_in)
    dir_in = os.path.join(INPUT_ROOT,dir_in)

    # skip items that are not directories
    if not os.path.isdir(dir_in):
        return

    metadataDir = os.path.join(dir_in,"metadata")
    if not os.path.isdir(metadataDir):
        os.makedirs(metadataDir)

    # convert the metadata in MS Access files to CSV
    logger.info("Converting metadata to " + metadataDir)
    mdbs = glob.glob(dir_in + "/*.MDB")
    mdbs.extend(glob.glob(dir_in + "/*.mdb"))
    for mdb in mdbs:
        logger.info("MDB: " + mdb)
        mdb_export(mdb, metadataDir)

    # find the csv with field info
    csv = os.path.join(dir_in,"metadata","FImage.csv")
    reordered_fields_csv = os.path.join(dir_in,"metadata","reordered_fields.csv")

    # find a well that was imaged
    csvFile = open(csv)
    well = "NO_WELL"
    reWell = re.compile("_([A-Z][0-9][0-9])f00d0.C01")
    for line in csvFile:
        result = re.search(reWell,line)
        if result:
            well = result.groups()[0]
            break

    _always_run_and_log("cat " + csv + " |grep " + well +" |grep d0|cut -d',' -f 21,31,32 |sort -t',' -k3nr,3nr -k2n,2n > " + reordered_fields_csv)

    imageList = open(reordered_fields_csv)
    images = imageList.readlines()
    imageList.close()
    j = 0
    reField = re.compile("f([0-9]*)d0.C01")
    field = "NO_FIELD"
    for i in images:
        image,x,y = i.split(",")
        image = image.replace('"','')
        field = re.search(reField,image).groups()[0]
        _run_and_log("rename 's/f" + field + "/fnew" + str(j).zfill(len(field)) + "/' " + os.path.join(dir_in, "*f" +  field + "*.C01"))
        j = j + 1

    # at this point, the file names look like PLATE_A01fnew00d0.CO1 etc.
    # comment out the following line, if you want to keep using
    # fnew to show that the files have been reordered.
    _run_and_log("rename 's/fnew/f/' " + os.path.join(dir_in, "*.C01"))

    logger.info("Total time elapsed: " + str(time.time() - start_time) + "s")


##
## Main part
##
if __name__=='__main__':

    usage = """%prog [options] input_dir staging_dir output_dir

                Stage and convert CellInsight data to TIF.
                RUN '%prog -h for options.'"""

    parser = OptionParser(usage=usage)
    parser.add_option('-n', '--dryrun', action="store_true", \
                      default=False, help="Print actions but do not execute.")
    parser.add_option('-i', '--input', default='/input', help="Input directory [default: %default].")
    parser.add_option('-d','--debug', action="store_true", help="Set log level to DEBUG.")

    opts,args = parser.parse_args()

    INPUT_ROOT = opts.input

    # log directory
    logdir = INPUT_ROOT

    # log file
    t = time.time()
    ft = datetime.datetime.fromtimestamp(t).strftime('%Y%m%d-%H%M%S')
    logfile = os.path.join(logdir,'cellomics_reorder_%s.log'%(ft))

    # logger
    loglevel = logging.INFO
    if opts.debug:
        loglevel = logging.DEBUG
    logformat = '[%(pathname)s:%(funcName)s:%(lineno)d] %(levelname)s - %(message)s'
    logging.basicConfig(filename=logfile,level=loglevel,format=logformat)
    logger = logging.getLogger(__name__)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(loglevel)
    formatter = logging.Formatter(logformat)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if opts.dryrun:
        logger.info("DRY RUN")
        DRY_RUN = True

    logger.info("INPUT_ROOT: " + INPUT_ROOT)

    # process all CellInsight datasets in the input directory
    datasets = []
    try:
        datasets = os.listdir(INPUT_ROOT)
    except Exception as e:
        logger.exception("Failed to read input directory.")

    logger.info("datasets:" + str(datasets))

    for dir_in in datasets:
        try:
            reorder(dir_in)
        except Exception as e:
            logger.exception("Failed to reorder " + dir_in)

    logger.info("Done.")
