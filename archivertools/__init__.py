import requests
import hashlib
from datetime import datetime
import json
import sqlalchemy as sqla
import sys
from sqlalchemy.ext.declarative import declarative_base

engine = sqla.create_engine('sqlite:///data.sqlite')
Base = declarative_base() # base class for sqlalchemy objects

class Archiver:
    """
    Class for interfacing with databases for Data Together's morph.io scraper integration
    """
    def __init__(self,url,UUID):
        #self.__makeTables()
        current_time = datetime.now()
        r = requests.get(url)
        self.headers = json.dumps(dict(r.headers))
        self.content = r.content #response body, TODO: may need to handle binary data differently vs html
        #hex representation of SHA-256 hash of body
        if sys.version_info.major == 2:
            # text is first encoded as utf-8 for python 2
            self.content_hash = hashlib.sha256(self.content.encode('utf-8')).hexdigest()
        elif sys.version_info.major == 3:
            # in python3 all strings are by default utf-8 encoded, and encode() method has been removed;
            self.content_hash = hashlib.sha256(self.content).hexdigest()
        self.__Session = sqla.orm.sessionmaker()
        self.__engine = engine
        self.__Session.configure(bind=self.__engine,expire_on_commit=False)
        payload = {'url':url,\
                'UUID':UUID,\
                'timestamp':current_time,\
                'body_content':self.content,\
                'body_SHA256':self.content_hash,\
                'headers':self.headers}
        # create instance of _RunMetadata and write to table
        self.run_metadata = _RunMetadata(**payload)
        self.__add(self.run_metadata)

    def __add(self,sqlalchemy_obj):
        """
        wrapper to add and commit sqlalchemy objects to the database. syntactic sugar to avoid having to repeat code to open and close sessions whenever we want to write
        """
        session = self.__Session()
        session.add(sqlalchemy_obj)
        session.commit()

    def addURL(self,url):
        """
        adds a child URL to the 'child_urls' table to be added back into the crawler
        """
        current_time = datetime.now()
        payload = {'run_id':self.run_metadata.run_id,\
                'url':url,\
                'timestamp':current_time}
        child_url = _ChildURL(**payload)
        try:
            self.__add(child_url)
        except sqla.exc.IntegrityError as e:
            if 'UNIQUE constraint failed' in str(e):
                pass
            else:
                raise


    def addFile(self,filename,comments=None,buffer_size=65536):
        """
        adds a local file named 'filename' as a binary blob into the 'files' table to be ingested into Data Together
        automatically hashes file contents and stores it in the db

        Args:
            filename: string representation of the filename of local file to be added to the database
            comments: [optional] string any details about encoding, format, or how the data was extracted that may be useful to anyone who examines the data
            buffer_size: [optional, default 64kb] size of buffer to use when computing SHA256 hash. Buffer should be used to keep the scraper memory-efficient. Setting buffer_size=0 hashes the file all at once

        """
        current_time = datetime.now()
        sha256_hasher = hashlib.sha256()
        with open(filename,'rb') as f:
            if buffer_size > 0:
                data = f.read(buffer_size)
                while data:
                    sha256_hasher.update(data)
                    data = f.read(buffer_size)
            else:
                data = f.read()
                sha256_hasher.update(data)
            file_contents_hash = sha256_hasher.hexdigest()
            f.seek(0)
            file_contents = f.read()
            payload = {'run_id':self.run_metadata.run_id,\
                    'file_contents':file_contents,
                    'filename':filename,
                    'file_SHA256':file_contents_hash,
                    'comments':comments,
                    'timestamp':current_time}
            file_object = _File(**payload)
            self.__add(file_object)

class _RunMetadata(Base):
    """
    Internal class to be used with sqlalchemy for writing scraper metadata to sqlite database
    """
    __tablename__ = "runs_metadata"
    run_id = sqla.Column(sqla.Integer, primary_key=True)
    url = sqla.Column(sqla.Text)
    UUID = sqla.Column(sqla.Text)
    timestamp = sqla.Column(sqla.DateTime)
    body_content = sqla.Column(sqla.Text)
    body_SHA256 = sqla.Column(sqla.Text)
    headers = sqla.Column(sqla.Text)

class _File(Base):
    """
    Internal class to be used with sqlalchemy for writing scraped files to sqlite db as blobs
    """
    __tablename__ = "files"
    file_id = sqla.Column(sqla.Integer, primary_key=True)
    run_id = sqla.Column(sqla.Integer, sqla.ForeignKey("runs_metadata.run_id"))
    file_contents = sqla.Column(sqla.LargeBinary)
    filename = sqla.Column(sqla.Text)
    file_SHA256 = sqla.Column(sqla.Text)
    comments = sqla.Column(sqla.Text)
    timestamp = sqla.Column(sqla.DateTime)

class _ChildURL(Base):
    """
    Internal class to be used with sqlalchemy for writing scraped child urls
    """
    __tablename__ = "child_urls"
    url_id = sqla.Column(sqla.Integer, primary_key=True)
    url = sqla.Column(sqla.Text, unique=True)
    run_id = sqla.Column(sqla.Integer, sqla.ForeignKey("runs_metadata.run_id"))
    timestamp = sqla.Column(sqla.DateTime)


Base.metadata.create_all(bind=engine)
