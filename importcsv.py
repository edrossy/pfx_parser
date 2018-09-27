from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table, inspect
import pandas as pd
import datetime as dt
import datetime
import time
import os
import unicodecsv as csv
import zipfile

def importfile(prefix):
    constring = 'mysql+mysqldb://sqlusername:sqlpassword@127.0.0.1:3306/pitchfx'
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
                    print ((str(datetime.datetime.now()) + ' ;Importing File: ' + tfile))

                    #Get rows from CSV file and being import into MySQL DB
                    for df in pd.read_csv(f, chunksize=chunksize, iterator=True, encoding='utf-8',
                                          delimiter=str(delimiter), quotechar=str(textqualifier),
                                          quoting=csv.QUOTE_NONNUMERIC, low_memory=False):
                        df = df.rename(columns={c: c.replace(' ', '') for c in df.columns})  # Remove spaces from columns
                        #This set index column value for MySQL import
                        df.index += index_start
                        j += 1 #Row Count
                        print (str(datetime.datetime.now()) + ' ;{} seconds: completed {} rows'.format((dt.datetime.now() - start).seconds, j * chunksize))
                        df.to_sql(mytable, engine, if_exists='append')
                        index_start = df.index[-1] + 1
                    f.close()
                    xx += 1
                    print ((str(datetime.datetime.now()) + ' ;Completed Importing File to Database: ' + tfile))

                    #Zip File For Archiving Purposes And To Avoind Further Processing
                    try:
                        import zlib
                        compression = zipfile.ZIP_DEFLATED
                    except:
                        compression = zipfile.ZIP_STORED

                    modes = {zipfile.ZIP_DEFLATED: 'deflated', zipfile.ZIP_STORED: 'stored', }
                    print ((str(datetime.datetime.now()) + ' ;Archiving File: ' + tfile))
                    zf = zipfile.ZipFile(tfile.replace('.csv','') + '.zip', mode='w')
                    try:
                        print ((str(datetime.datetime.now()) + ' ;Archiving File: ' + tfile + ' with compression mode',
                                modes[compression]))
                        zf.write(tfile, compress_type=compression)
                    finally:
                        zf.close()

                    # Delete the imported CSV file
                    print ((str(datetime.datetime.now()) + ' ;Deleting File: ' + tfile))
                    os.remove(tfile)

    print (str(datetime.datetime.now()) + ' ;End of job')
    endscript = time.time()
    print (str(datetime.datetime.now()) + ' ;Elapsed time: '+'{:10.2f}'.format(endscript - startscript) + ' seconds or ' + '{:10.2f}'.format((endscript - startscript) / 60) + ' minutes')
