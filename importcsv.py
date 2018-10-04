from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table, inspect
import pandas as pd
import datetime as dt
import datetime
import time
import os
import unicodecsv as csv
import zipfile
import logging.config

def importfile(prefix):
    logfile = (prefix + '_importlog_').upper() + str(time.strftime('%Y%m%d')) + '.log'
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s.%(msecs)03d|%(levelname)s|{%(module)s}%(message)s',
                        datefmt='%Y-%m-%d,%H:%M:%S',
                        filename=logfile,
                        filemode='a')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s|%(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
    constring = 'mysql+mysqldb://username:password@127.0.0.1:3306/pitchfx'
    chunksize = 50000
    delimiter = ","
    textqualifier = '"'
    tfolder = "import/"
    startscript = time.time()
    xx = 1
    for root, dirs, files in os.walk(tfolder):
        for file in files:
            if file.startswith(prefix):
                if file.endswith('.csv'):
                    tfile = (tfolder + file)
                    #Set MySQL Table Name - Note Tables (pitchfx.pitches & pitchfx.atbats) in MySQL DB must already be created - see SQL Scripts
                    mytable = file.replace('.csv', '').replace(prefix,'')
                    #Open CSV File
                    f = open(tfile, 'rb')
                    engine = create_engine(constring)
                    if xx == 1:
                        mytable = file.replace('.csv', '').replace(prefix,'')
                    else:
                        None
                    start = dt.datetime.now()
                    j = 0
                    index_start = 1
                    logging.info((str(datetime.datetime.now()) + ' ;Importing File: ' + tfile))
                    #Get rows from CSV file and being import into MySQL DB
                    for df in pd.read_csv(f, chunksize=chunksize, iterator=True, encoding='utf-8',
                                          delimiter=str(delimiter), quotechar=str(textqualifier),
                                          quoting=csv.QUOTE_NONNUMERIC, low_memory=False):
                        df = df.rename(columns={c: c.replace(' ', '') for c in df.columns})  # Remove spaces from columns
                        #This set index column value for MySQL import
                        df.index += index_start
                        j += 1 #Row Count
                        df.to_sql(mytable, engine, if_exists='append')
                        logging.info(str(datetime.datetime.now()) + ' ;{} seconds: completed {} rows'.format((dt.datetime.now() - start).seconds, j * chunksize))
                        index_start = df.index[-1] + 1
                    f.close()
                    xx += 1
                    logging.info(str(datetime.datetime.now()) + ' ;Completed Importing File to Database: ' + tfile)
                    #Zip File For Archiving Purposes And To Avoind Further Processing
                    try:
                        import zlib
                        compression = zipfile.ZIP_DEFLATED
                    except:
                        compression = zipfile.ZIP_STORED
                    modes = {zipfile.ZIP_DEFLATED: 'deflated', zipfile.ZIP_STORED: 'stored', }
                    logging.info(str(datetime.datetime.now()) + ' ;Archiving File: ' + tfile)
                    zf = zipfile.ZipFile(tfile.replace('.csv','') + '.zip', mode='w')
                    try:
                        logging.info(str(datetime.datetime.now()) + ' ;Archiving File: ' + tfile + ' with compression mode',
                                modes[compression])
                        zf.write(tfile, compress_type=compression)
                    finally:
                        zf.close()
                    # Delete the imported CSV file
                    logging.info(str(datetime.datetime.now()) + ' ;Deleting File: ' + tfile)
                    os.remove(tfile)
    logging.info(str(datetime.datetime.now()) + ' ;End of job')
    endscript = time.time()
    logging.info(str(datetime.datetime.now()) + ' ;Elapsed time: '+'{:10.2f}'.format(endscript - startscript) + ' seconds or ' + '{:10.2f}'.format((endscript - startscript) / 60) + ' minutes')
