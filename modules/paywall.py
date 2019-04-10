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
    #path = os.path.join(request.folder, 'static', filename)
    #path = os.path.join('c:\\web2py\\applications\\paywall\\static', filename)
    path = os.path.join('/home/www-data/web2py/applications/paywall/static', filename)
    
    if not os.path.exists(path):

        #resp = requests.get(url,proxies=proxies,verify=False)
        resp = requests.get(url)
        text = resp.text.encode('utf-8')

        page = bs.BeautifulSoup(text)

        n_scripts = len(page.findAll('script'))
        for i in range(1,n_scripts + 1): page.script.decompose()

        if host == 'www.gazetaonline.com.br':
            n_iframes = len(page.findAll('iframe'))
            for i in range(1,n_iframes + 1): page.iframe.decompose()
        
        if host == 'www.em.com.br':
            while page.find(attrs={'class':'news-blocked-content'}):
                page.find(attrs={'class':'news-blocked-content'}).decompose()
            while page.find(attrs={'class':'news-blocked js-news-blocked'}):
                page.find(attrs={'class':'news-blocked js-news-blocked'}).decompose()
            while page.find(attrs={'class':'news-blocked js-news-blocked-login'}):
                page.find(attrs={'class':'news-blocked js-news-blocked-login'}).decompose()

        #divs = page.findAll('div')

        #sys.exit(0)

        # retirar tags <script>
        #regex = '<script.*>.*</script>'
        #text = re.sub(regex,'',text)

        #regex_list = []
        #regex_list.append('<script.*>.*</script>')

        #if host == 'www.em.com.br':
        #	print 'estado de minas'
        #	regex = '<div class=.*blocked.*>.*?</div>'
        #	text = re.sub(regex,'',text)

        with open(path,'w') as fp:
            fp.write( str(page) )

        #print 'arquivo impresso em {0}.html'.format(filename)
    return filename

    #return str(page)
