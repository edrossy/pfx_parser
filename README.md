# pfx_parser
A new PitchFX parser, written in python

***UPDATES***

SQL Tables Defs Updated for MySQL

Added Import Routine - importcsv.py (for importing CSV result files into MySQL DB)

TODO:

- Add in logging to DB/Files

- Daily Updates To DB

- If there is an issue with reading game.xml for data and it returns Unknown, there needs to be better error handling to retry xml pull and parsing of the data.  Alternatively, you can query database (

#Select  distinct year,month,day from atbats where retro_game_id like 'UNKNOWN%';

#delete from atbats where retro_game_id like 'UNKNOWN%';

) for bad values and requery the api for days with bad data after removing the bad data from the database.


