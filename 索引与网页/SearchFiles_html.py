#!/usr/bin/env python

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene, jieba

from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause

"""
This script is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""


def parseCommand(command):
    '''
    input: C title:T author:A language:L
    output: {'contents':C, 'title':T, 'author':A, 'language':L}

    Sample:
    input:'contenance title:henri language:french author:william shakespeare'
    output:{'author': ' william shakespeare',
                   'language': ' french',
                   'contents': ' contenance',
                   'title': ' henri'}
    '''
    command = command.strip()
    if not command:
        command = "*"
    allowed_opt = ['title', 'platform', 'price', 'brand', 'parameter']
    command_dict = {}
    opt = 'title'
    command = command.lower()
    for i in command.split(' '):
        if ':' in i:
            opt, value = i.split(':')[:2]
            opt = opt.lower()
            if opt in allowed_opt and value != '':
                command_dict[opt] = command_dict.get(opt, '') + ' ' + value
        else:
            if opt == 'title':
                i = ' '.join(jieba.cut(i))
            command_dict[opt] = command_dict.get(opt, '') + ' ' + i
    return command_dict


def parseCommand_img(command):
    '''
    input: C title:T author:A language:L
    output: {'contents':C, 'title':T, 'author':A, 'language':L}

    Sample:
    input:'contenance title:henri language:french author:william shakespeare'
    output:{'author': ' william shakespeare',
                   'language': ' french',
                   'contents': ' contenance',
                   'title': ' henri'}
    '''
    command = command.strip()
    if not command:
        command = "*"
    allowed_opt = ['imghash', 'platform', 'price', 'brand', 'parameter']
    command_dict = {}
    opt = 'imghash'
    command = command.lower()
    for i in command.split(' '):
        if ':' in i:
            opt, value = i.split(':')[:2]
            opt = opt.lower()
            if opt in allowed_opt and value != '':
                command_dict[opt] = command_dict.get(opt, '') + ' ' + value
        else:
            if opt == 'imghash':
                i = ' '.join(jieba.cut(i))
            command_dict[opt] = command_dict.get(opt, '') + ' ' + i
    return command_dict


def run(searcher, analyzer):
    while True:
        print
        print "Hit enter with no input to quit."
        command = raw_input("Query:")
        command = unicode(command, 'utf-8')
        if command == '':
            return

        print
        print "Searching for:", command

        command_dict = parseCommand(command)
        print command_dict
        querys = BooleanQuery()
        for k, v in command_dict.iteritems():
            query = QueryParser(Version.LUCENE_CURRENT, k,
                                analyzer).parse(v)
            querys.add(query, BooleanClause.Occur.MUST)
        scoreDocs = searcher.search(querys, 100).scoreDocs
        print "%s total matching documents." % len(scoreDocs)

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            ##            explanation = searcher.explain(query, scoreDoc.doc)
            print "------------------------"
            print 'title:', doc.get("title_nocut")
            print 'platform:', doc.get('platform')
            print 'price:', doc.get('price')
            print 'parameter:\n', doc.get("parameter_nocut")
            print 'imgurl:', doc.get('images')
            print 'one comment:', doc.get('comment').split('\n\n')[0]
            print 'class:', doc.get('class')



def get_pri_up(mylist):
    return eval(mylist[2])


def get_pri_down(mylist):
    return -eval(mylist[2])


def get_rate(mylist):
    return -eval(mylist[9])


def retrieve(command, searchtype):
    STORE_DIR = "index"
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
    if command == '':
        return []
    command_dict = parseCommand(command)
    querys = BooleanQuery()
    for k, v in command_dict.iteritems():
        query = QueryParser(Version.LUCENE_CURRENT, k,
                            analyzer).parse(v)
        querys.add(query, BooleanClause.Occur.MUST)
    scoreDocs = searcher.search(querys, 100).scoreDocs
    ans = []
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        item = []
        item.append(doc.get("title_nocut"))  # 0
        item.append(doc.get('platform'))  # 1
        item.append(doc.get('price'))  # 2
        item.append(doc.get("parameter_nocut").split("\n"))  # 3
        item.append(doc.get('images').split("\n"))  # 4
        item.append(" ".join(doc.get('comment').split('\n\n')[0].split("\n")))  # 5
        item.append(doc.get('url'))  # 6
        item.append(doc.get('class'))  # 7
        item.append(doc.get('brand_nocut'))  # 8
        item.append(doc.get('rate'))  # 9
        ans.append(item)
    if searchtype == 2:
        ans.sort(key=get_pri_up)
    if searchtype == 3:
        ans.sort(key=get_pri_down)
    if searchtype == 4:
        ans.sort(key=get_rate)
    return ans


def retrieve_img(command):
    STORE_DIR = "index"
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
    if command == '':
        return []
    command_dict = parseCommand_img(command)
    querys = BooleanQuery()
    for k, v in command_dict.iteritems():
        query = QueryParser(Version.LUCENE_CURRENT, k,
                            analyzer).parse(v)
        querys.add(query, BooleanClause.Occur.MUST)
    scoreDocs = searcher.search(querys, 100).scoreDocs
    ans = []
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        item = []
        item.append(doc.get("title_nocut"))  # 0
        item.append(doc.get('platform'))  # 1
        item.append(doc.get('price'))  # 2
        item.append(doc.get("parameter_nocut").split("\n"))  # 3
        item.append(doc.get('images').split("\n"))  # 4
        item.append(" ".join(doc.get('comment').split('\n\n')[0].split("\n")))  # 5
        item.append(doc.get('url'))  # 6
        item.append(doc.get('class'))  # 7
        item.append(doc.get('brand_nocut'))  # 8
        item.append(doc.get('rate'))  # 9
        ans.append(item)
    return ans


if __name__ == '__main__':
    STORE_DIR = "index"
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    # base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
    run(searcher, analyzer)
    del searcher
