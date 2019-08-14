#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *

import sys,os
import requests
import re
import hashlib
import BeautifulSoup as bs
from bs4 import BeautifulSoup

def pw_break(url):

    proxies = {
	'http':'http://proxy.almg.uucp:3128/',
	'https':'http://proxy.almg.uucp:3128/',
	}

    #url = 'https://www.valor.com.br/empresas/6175987/o-que-natura-ganha-se-decidir-comprar-avon'
    #url = 'https://www.valor.com.br/agro/6175611/usina-santa-terezinha-do-parana-pede-recuperacao-judicial'
    #url = 'https://super.abril.com.br/sociedade/temer-e-o-setimo-ex-presidente-brasileiro-preso/'
    #url = 'https://www.em.com.br/app/noticia/gerais/2019/03/28/interna_gerais,1041796/desaparecido-em-brumadinho-e-localizado-vivo-apos-dois-meses.shtml'

    '''
    URL do Estado de Minas possui uma DIV que mostra o paywall
    <div class="news-blocked-content">...</div>
    <div class="news-blocked js-news-blocked">...</div>
    <div class="news-blocked js-news-blocked-login">...</div>
    '''

    url_regex = 'htt(p|ps)://(?P<host>.*?)/.*'
    host = re.match(url_regex,url).group('host')
    #print host

    #filename = 'c:\\Temp\\{0}.html'.format( hashlib.md5(url).hexdigest() )
    filename = '{0}.html'.format( hashlib.md5(url).hexdigest() )
    page = None
    html_page = ''
    #path = os.path.join(request.folder, 'static', filename)
    #path = os.path.join('c:\\web2py\\applications\\paywall\\static', filename)
    path = os.path.join('/web/web2py/applications/paywall/static', filename)
    
    if not os.path.exists(path):

        #resp = requests.get(url,proxies=proxies,verify=False)
        session = requests.Session()
        session.cookies.clear_session_cookies()
        resp = session.get(url)
        #text = unicode( resp.text.decode('utf-8',errors='ignore') )
        text = resp.text.encode('utf-8')

        if host == 'politica.estadao.com.br':
            html_page = text
        else:
            page = bs.BeautifulSoup(text)
            n_scripts = len(page.findAll('script'))
            for i in range(0,n_scripts):
                page.script.decompose()
            if host == 'www.gazetaonline.com.br':
                n_iframes = len(page.findAll('iframe'))
                for i in range(0,n_iframes): page.iframe.decompose()
            if host == 'www.em.com.br':
                while page.find(attrs={'class':'news-blocked-content'}):
                    page.find(attrs={'class':'news-blocked-content'}).decompose()
                while page.find(attrs={'class':'news-blocked js-news-blocked'}):
                    page.find(attrs={'class':'news-blocked js-news-blocked'}).decompose()
                while page.find(attrs={'class':'news-blocked js-news-blocked-login'}):
                    page.find(attrs={'class':'news-blocked js-news-blocked-login'}).decompose()
            if host == 'super.abril.com.br':
                #while page.findAll('header'): page.header.decompose()
                while page.findAll('ul'): page.ul.decompose()
            html_page = str(page.body)
            #html_page = ''
            #for elem in page.body.contents: html_page += str(elem)
            #html_page = str(page)

        with open(path,'w') as fp: fp.write( html_page )
    else:
        #page = bs.BeautifulSoup( unicode( file(path).read().decode('utf-8',errors='ignore') ) )
        html_page = file(path).read()

    return filename,html_page

    #return str(page)
