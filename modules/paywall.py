#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *

import sys,os
import requests
import re
import hashlib
import BeautifulSoup as bs
from bs4 import BeautifulSoup
import json

def decompose(host,html_text):
    from tags import tags_to_remove,tags_to_remove_by_host
    page = bs.BeautifulSoup(html_text)
    # remover tags
    for tag in tags_to_remove:
        while page.find(tag):
            page.find(tag).decompose()
    # remover tags por host
    host_tags_to_remove = tags_to_remove_by_host.get(host,{})
    for tag,attrlist in host_tags_to_remove.iteritems():
        if tag == 'remove':
            for tagname in attrlist:
                while page.find(tagname): page.find(tagname).decompose()
        else:
            for attr,list_of_values in attrlist.iteritems():
                for value in list_of_values:
                    while page.find(tag,attrs={attr:value}):
                        page.find(tag,attrs={attr:value}).decompose()
    return str(page.body)

def pw_break(url,proxies={}):

    url_regex = 'htt(p|ps)://(?P<host>.*?)/.*'
    host = re.match(url_regex,url).group('host')
    filename = '{0}.html'.format( hashlib.md5(url).hexdigest() )
    metafilename = '{0}.json'.format( hashlib.md5(url).hexdigest() )
    page = None
    html_page = ''
    meta = {}
    path_filename = os.path.join('/web/web2py/applications/paywall/static/pages', filename)
    path_metafilename = os.path.join('/web/web2py/applications/paywall/static/pages', metafilename)

    if not os.path.exists(path_filename):

        session = requests.Session()
        session.cookies.clear_session_cookies()
        resp = session.get(url,proxies=proxies)
        html_page = ''
        page = None
        try:
            from tags import utf8hosts
            if host in utf8hosts: raise Exception()
            html_page = decompose(host,resp.text.encode('iso-8859-1'))
            page = bs.BeautifulSoup(resp.text.encode('iso-8859-1'))
            meta['charset'] = 'iso-8859-1'
        except:
            html_page = decompose(host,resp.text.encode('utf-8'))
            page = bs.BeautifulSoup(resp.text.encode('utf-8'))
            meta['charset'] = 'utf-8'

        meta['title'] = page.title.text
        meta['description'] = page.find(attrs={'property':'og:description'}).attrs[1][1] if page.find(attrs={'property':'og:description'}) != None else ''
        if page.find(attrs={'property':'og:image'}): meta['image'] = page.find(attrs={'property':'og:image'}).attrs[1][1]
        meta['width'] = page.find(attrs={'property':'og:image:width'}).attrs[1][1] if page.find(attrs={'property':'og:image:width'}) != None else '400'
        meta['height'] = page.find(attrs={'property':'og:image:height'}).attrs[1][1] if page.find(attrs={'property':'og:image:height'}) != None else '400'
        meta['url'] = page.find(attrs={'property':'og:url'}).attrs[1][1] if page.find(attrs={'property':'og:url'}) != None else url

        with open(path_filename,'w') as fp: fp.write( html_page )
        with open(path_metafilename,'w') as fp: json.dump( meta,fp )
    else:
        meta = json.load( file( path_metafilename ) ) if os.path.exists( path_metafilename ) else {}

    return filename,meta

if __name__ == '__main__':
    pass
