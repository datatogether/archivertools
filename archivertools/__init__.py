import requests
import hashlib
import datetime
import json
import scraperwiki

class Archiver:
    """
    Class for interfacing with databases for Data Together's morph.io scraper integration
    """
    def __init__(self,url,UUID):
        self.__makeTables()
        current_time = str(datetime.now())
        r = requests.get(url)
        self.headers = json.dumps(dict(r.headers))
        self.content = r.content #response body, TODO: may need to handle binary data differently vs html
        self.content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest() #SHA-256 hash of body - text is first encoded as utf-8 b/c sha256 expects binary; output is then converted back as a hexadecimal string representation for storage
        payload = {'url':url,\
                'UUID':UUID,\
                'timestamp':current_time,\
                'body_content':content,\
                'body_SHA256':content_hash,\
                'headers':headers}
        scraperwiki.sqlite.save(unique_keys=[],data=payload,table_name='runs_metadata') #saves to sqlite
        self.__current_run_id = scraperwiki.sqlite.execute("""
                SELECT seq FROM sqlite_sequence WHERE NAME="runs_metadata"
                """) #Gets the most recent run_id associated w/ the entry we just added

    def __makeTables(self):
        """
        Creates tables in the sqlite db
        table runs_metadata stores the metadata associated whenever a new run is started
        table child_urls stores urls to be populated back into the Data Together crawler
        table files stores binary files of scraped data to be stored on Data Together
        """
        scraperwiki.sqlite.execute("""
                        CREATE TABLE IF NOT EXISTS runs_metadata (
                        run_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        url TEXT,
                        UUID TEXT,
                        timestamp TEXT,
                        body_content TEXT,
                        body_SHA256 TEXT,
                        headers TEXT
                        )""")
        scraperwiki.sqlite.execute("""
                        CREATE TABLE IF NOT EXISTS child_urls (
                        run_id INTEGER,
                        FOREIGN KEY(run_id) REFERENCES runs_metadata(run_id),
                        url TEXT UNIQUE NOT NULL,
                        timestamp TEXT
                        )""")
        scraperwiki.sqlite.execute("""
                        CREATE TABLE IF NOT EXISTS files (
                        run_id INTEGER,
                        FOREIGN KEY(run_id) REFERENCES runs_metadata(run_id),
                        file_contents BLOB NOT NULL,
                        filename TEXT NOT NULL,
                        file_SHA256 TEXT NOT NULL,
                        comments TEXT,
                        timestamp TEXT
                        )""")

    def addURL(self,url):
        """
        adds a child URL to the 'child_urls' table to be added back into the crawler
        """
        current_time = str(datetime.now())
        payload = {'run_id':self.__current_run_id,\
                'url':url,\
                'timestamp':current_time}
        scraperwiki.sqlite.save(unique_keys=[],data=payload,table_name='child_urls')

    def addFile(self,file_contents,filename,comments=None):
        """
        adds a file as a binary blob into the 'files' table to be ingested into Data Together
        automatically hashes the file_contents and stores it
        requires a filename with appropriate file extension
        additional comments, such as details about encoding or how the data was extracted should be passed as a string via the comments argument
        """
        current_time = str(datetime.now())
        file_contents_hash = hashlib.sha256(file_contents).hexdigest()
        payload = {'run_id':self.__current_run_id,\
                'file_contents':file_contents,
                'filename':filename,
                'file_SHA256':file_contents_hash,
                'comments':comments,
                'timestamp':current_time}
        scraperwiki.sqlite.save(unique_keys=[],data=payload,table_name='files')
