#!/usr/bin/env python
# -*- coding:utf-8 -*-
INDEX_DIR = "IndexFiles.index"

import sys, os, lucene, threading, time , re 
from urlparse import *
from datetime import datetime
import jieba
import json
from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

"""
This class is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""



class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)

class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, root, storeDir):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(File(storeDir))
        analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.indexDocs(root, writer)
        ticker = Ticker()
        print 'commit index',
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print 'done'

    def indexDocs(self, root, writer):

        t1 = FieldType() #title_nocut,price,class,parameter_nocut,platform
        t1.setIndexed(True) 
        t1.setStored(True)
        t1.setTokenized(False)
        
        t2 = FieldType() #text
        t2.setIndexed(True)
        t2.setStored(False)
        t2.setTokenized(True)
        t2.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        t3 = FieldType() #name,title,parameter,brand
        t3.setIndexed(True)
        t3.setStored(True)
        t3.setTokenized(True)
        t3.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        t4 = FieldType() #url
        t4.setIndexed(True)
        t4.setStored(True)
        t4.setTokenized(True)

        t5 = FieldType() #id,comment,images,price_num,rate
        t5.setIndexed(False)
        t5.setStored(True)
        t5.setTokenized(False)

        t6 = FieldType() #imghash
        t6.setIndexed(True)
        t6.setStored(False)
        t6.setTokenized(True)

        for root, dirnames, filenames in os.walk(root):
            for filename in filenames:
                #if not filename.endswith('.txt'):
                #    continue
                print "adding", filename
                try:
                    path = os.path.join(root, filename)
                    with open(path,'r') as fin:
                        tmpjs = json.load(fin,encoding='utf8')
                    comment,name,title,url,text,brand,Class,images,parameter,price,parameter_nocut,platform,lower_title,lower_name,rate,imghash = tmpjs['comment'],tmpjs['name'],tmpjs['title'],tmpjs['url'],tmpjs['text'],tmpjs['brand'],tmpjs['class'],tmpjs['images'],tmpjs['parameter'],tmpjs['price'],tmpjs['parameter_nocut'],tmpjs['platform'],tmpjs['lower_title'],tmpjs['lower_name'],tmpjs['rate'],tmpjs['imghash']
                    doc = Document()
                    doc.add(Field("name", ' '.join(jieba.cut(name)), t3))
                    doc.add(Field("title",' '.join(jieba.cut(lower_title)), t3))
                    doc.add(Field("title_nocut",title,t1))
                    doc.add(Field("url", url,t4))
                    doc.add(Field("text",text,t2))
                    doc.add(Field("brand_nocut",brand,t1))
                    doc.add(Field("brand",' '.join(jieba.cut(brand)),t3))
                    doc.add(Field("class",Class,t1))
                    doc.add(Field("id",filename.rstrip('.json'),t5))
                    doc.add(Field("parameter",parameter,t3))
                    doc.add(Field("price",price,t1))
                    doc.add(Field("platform",platform,t1))
                    doc.add(Field("parameter_nocut",parameter_nocut,t1))
                    doc.add(Field("images",'\n'.join(images),t5))
                    doc.add(Field("comment",'\n\n'.join(comment),t5))
                    doc.add(Field("rate",str(rate),t5))
                    doc.add(Field("imghash",imghash,t6))
                    writer.addDocument(doc)
                except Exception, e:
                    print "Failed in indexDocs:", e

if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    start = datetime.now()
    try:
        IndexFiles('/media/EE/Final/total', "index")
        end = datetime.now()
        print end - start
    except Exception, e:
        print "Failed: ", e
        raise e
