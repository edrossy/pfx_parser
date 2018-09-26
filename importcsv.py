from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table, inspect
import pandas as pd
import datetime as dt
import datetime
import time
import os
import unicodecsv as csv

def importfile(constring,tfolder,textqualifier,delimiter,chunksize,sametable,appendtable,year):
    startscript = time.time()
    print (str(datetime.datetime.now()) + ' ;Start Time: ' + str(datetime.datetime.now()))

    xx = 1
    for root, dirs, files in os.walk(tfolder):
        for file in files:
            if file.endswith(".csv"):
                tfile = (tfolder + file)
                print (tfile)
                mytable = file.replace('.csv', '').replace(year,'')
                # with open(tfile, 'rb') as inf:
                #     with open('New_'+tfile, 'wb') as fixed:
                #         for line in inf:
                #             fixed.write(line)
                #  perform calculation
                f = open(tfile, 'rb')
                engine = create_engine(constring)
                if sametable == 'Yes':
                    if xx == 1:
                        mytable = file.replace('.csv', '').replace(year,'')
                    else:
                        None
                if appendtable == 'replace':
                    if xx == 1:
                        try:
                            connection = engine.raw_connection(pool_recycle=3600)
                            cursor = connection.cursor()
                            command = "DROP TABLE " + mytable
                            cursor.execute(command)
                            print (str(
                                datetime.datetime.now()) + ' ;Database Table: ' + mytable + ' has been dropped.')
                            connection.commit()
                            cursor.close()
                        except:
                            print (str(datetime.datetime.now()) + ' ;Database Table: ' + mytable + ' did not exist.')

                start = dt.datetime.now()
                j = 0
                index_start = 1
                print ('Blah' + (str(datetime.datetime.now()) + ' ;Processing File: ' + tfile))

                for df in pd.read_csv(f, chunksize=chunksize, iterator=True, encoding='utf-8',
                                      delimiter=str(delimiter), quotechar=str(textqualifier),
                                      quoting=csv.QUOTE_NONNUMERIC, low_memory=False):
                    df = df.rename(columns={c: c.replace(' ', '') for c in df.columns})  # Remove spaces from columns

                    df.index += index_start
                    j += 1
                    print (str(datetime.datetime.now()) + ' ;{} seconds: completed {} rows'.format((dt.datetime.now() - start).seconds, j * chunksize))
                    df.to_sql(mytable, engine, if_exists='append')
                    index_start = df.index[-1] + 1
                f.close()
                xx += 1
    print (str(datetime.datetime.now()) + ' ;End of job')
    endscript = time.time()
    print (str(datetime.datetime.now()) + ' ;Elapsed time: '+'{:10.2f}'.format(endscript - startscript) + ' seconds or ' + '{:10.2f}'.format((endscript - startscript) / 60) + ' minutes')