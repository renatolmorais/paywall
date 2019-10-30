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

'''
    URL do Estado de Minas possui uma DIV que mostra o paywall
    <div class="news-blocked-content">...</div>
    <div class="news-blocked js-news-blocked">...</div>
    <div class="news-blocked js-news-blocked-login">...</div>
    '''

tags_to_remove_by_host = {
	'www.em.com.br':
	{
		'div':{'class':	['login-signature-call-bottom hidden-no-important show-loginwall-login-active-inline','nav-side__container','news-card__content','news-blocked-content','news-blocked js-news-blocked','news-blocked js-news-blocked-login','img-mobile-full mb-20','pl-15 pr-15 pt-xs-10 header-border-underline no-negative-xs',] },
		'small':{'class':	['hidden-print txt-no-serif',] },
		'p':{'class':	['text-xs-center',] },
		'footer':{'class':	['footer bg-gray-extra',] },
		'nav':{'class':	['fixed-btn-uai','nav-main','nav-main pt-8 pb-8 pt-xs-7 pb-xs-7'] },
		'section':{'class':	['bg-gray-extra mt-20','bg-gray-extra'] },
        'header':{'class':   ['hidden-print header-fixed js-header-fix'] },
        'aside':{'class':['hidden-print col-sm-10 col-sm-offset-1 col-md-offset-0 col-md-3 mb-35 scroll-linked',] },
	},
	'super.abril.com.br':
	{
		'header':	{'class':	['header'] },
		'div':		{'class':	['sidebar-top hidden-xs hidden-sm','widget-cover-container'] },
		'section':	{'class':	['comments','sidebar-above-footer',] },
	},
	'www.gazetadopovo.com.br':
	{
		'div':		{'class':	['c-section-header','box-ads-header','header','wrapper','breadcrumb','js-touchpoint c-touchpoint-post-footer','js-touchpoint c-touchpoint-post-footerFixed','c-communication-errors user-report',] },
		'footer':	{'class':	['c-footer'],},
	},
	'gazetaonline.globo.com':
	{
		'iframe':	{},
	}
}

tags_to_remove = ['script','iframe','noscript','header','style']

def decompose(host,html_text):
	page = bs.BeautifulSoup(html_text.encode('utf-8'))
	# remover tags
	for tag in tags_to_remove:
		while page.find(tag): page.find(tag).decompose()
	# remover tags por host
	host_tags_to_remove = tags_to_remove_by_host.get(host,{})
	for tag,attrlist in host_tags_to_remove.iteritems():
		for attr,list_of_values in attrlist.iteritems():
			for value in list_of_values:
				while page.find(tag,attrs={attr:value}):
					page.find(tag,attrs={attr:value}).decompose()
	return str(page)

def pw_break(url):

    proxies = {
	'http':'http://proxy.almg.uucp:3128/',
	'https':'http://proxy.almg.uucp:3128/',
	}

    #url = 'https://www.valor.com.br/empresas/6175987/o-que-natura-ganha-se-decidir-comprar-avon'
    #url = 'https://www.valor.com.br/agro/6175611/usina-santa-terezinha-do-parana-pede-recuperacao-judicial'
    #url = 'https://super.abril.com.br/sociedade/temer-e-o-setimo-ex-presidente-brasileiro-preso/'
    #url = 'https://www.em.com.br/app/noticia/gerais/2019/03/28/interna_gerais,1041796/desaparecido-em-brumadinho-e-localizado-vivo-apos-dois-meses.shtml'

    url_regex = 'htt(p|ps)://(?P<host>.*?)/.*'
    host = re.match(url_regex,url).group('host')
    #print host

    #filename = 'c:\\Temp\\{0}.html'.format( hashlib.md5(url).hexdigest() )
    filename = '{0}.html'.format( hashlib.md5(url).hexdigest() )
    metafilename = '{0}.json'.format( hashlib.md5(url).hexdigest() )
    page = None
    html_page = ''
    meta = {}
    #path = os.path.join(request.folder, 'static', filename)
    #path = os.path.join('c:\\web2py\\applications\\paywall\\static', filename)
    path_filename = os.path.join('/web/web2py/applications/paywall/static', filename)
    path_metafilename = os.path.join('/web/web2py/applications/paywall/static', metafilename)

    if not os.path.exists(path_filename):

        #resp = requests.get(url,proxies=proxies,verify=False)
        session = requests.Session()
        session.cookies.clear_session_cookies()
        resp = session.get(url)
        #text = unicode( resp.text.decode('utf-8',errors='ignore') )
        #text = resp.text.encode('utf-8')
        html_page = decompose(host,resp.text)
        
        page = bs.BeautifulSoup(resp.text.encode('utf-8'))
        
        meta['title'] = page.find(attrs={'property':'og:title'}).attrs[1][1] if page.find(attrs={'property':'og:title'}) != None else ''
        meta['description'] = page.find(attrs={'property':'og:description'}).attrs[1][1] if page.find(attrs={'property':'og:description'}) != None else ''
        if page.find(attrs={'property':'og:image'}): meta['image'] = page.find(attrs={'property':'og:image'}).attrs[1][1]
        meta['width'] = page.find(attrs={'property':'og:image:width'}).attrs[1][1] if page.find(attrs={'property':'og:image:width'}) != None else '400'
        meta['height'] = page.find(attrs={'property':'og:image:height'}).attrs[1][1] if page.find(attrs={'property':'og:image:height'}) != None else '400'
        meta['url'] = page.find(attrs={'property':'og:url'}).attrs[1][1] if page.find(attrs={'property':'og:url'}) != None else url
        #charset = 'utf-8'

        '''
        if host == 'politica.estadao.com.br':
            html_page = text
        else:
            page = bs.BeautifulSoup(text)

            meta['title'] = page.find(attrs={'property':'og:title'}).attrs[1][1] if page.find(attrs={'property':'og:title'}) != None else ''
            meta['description'] = page.find(attrs={'property':'og:description'}).attrs[1][1] if page.find(attrs={'property':'og:description'}) != None else ''
            if page.find(attrs={'property':'og:image'}): meta['image'] = page.find(attrs={'property':'og:image'}).attrs[1][1]
            meta['width'] = page.find(attrs={'property':'og:image:width'}).attrs[1][1] if page.find(attrs={'property':'og:image:width'}) != None else '400'
            meta['height'] = page.find(attrs={'property':'og:image:height'}).attrs[1][1] if page.find(attrs={'property':'og:image:height'}) != None else '400'
            meta['url'] = page.find(attrs={'property':'og:url'}).attrs[1][1] if page.find(attrs={'property':'og:url'}) != None else url

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
                to_decompose = {
                        'div':['login-signature-call-bottom hidden-no-important show-loginwall-login-active-inline','nav-side__container','news-card__content',],
                        'small':['hidden-print txt-no-serif',],
                        'p':['text-xs-center',],
                        'footer':['footer bg-gray-extra',],
                        'nav':['fixed-btn-uai','nav-main','nav-main pt-8 pb-8 pt-xs-7 pb-xs-7'],
                        'section':['bg-gray-extra mt-20','bg-gray-extra'],
                }

                for p_tag,cssclasslist in to_decompose.iteritems():
                    for elem in page.findAll(p_tag):
                        for cssclass in cssclasslist:
                            if page.find(p_tag,attrs={'class':cssclass}) != None: page.find(p_tag,attrs={'class':cssclass}).decompose()
            if host == 'super.abril.com.br':
                #while page.findAll('header'): page.header.decompose()
                while page.findAll('ul'): page.ul.decompose()
                if page.find('header',attrs={'class':'header'}) != None: page.find('header',attrs={'class':'header'}).decompose()
                if page.find('div',attrs={'class':'sidebar-top hidden-xs hidden-sm'}) != None: page.find('div',attrs={'class':'sidebar-top hidden-xs hidden-sm'}).decompose()
                if page.find('div',attrs={'class':'widget-cover-container'}) != None: page.find('div',attrs={'class':'widget-cover-container'}).decompose()
                if page.find('section',attrs={'class':'comments'}) != None: page.find('section',attrs={'class':'comments'}).decompose()
                if page.find('section',attrs={'class':'sidebar-above-footer'}) != None: page.find('section',attrs={'class':'sidebar-above-footer'}).decompose()
            if host == 'www.gazetadopovo.com.br' or host == 'gazetadopovo.com.br':
                while page.findAll('svg'): page.svg.decompose()
                if page.find('div',attrs={'class':'header'}) != None: page.find('div',attrs={'class':'header'}).decompose()
                if page.find('div',attrs={'class':'wrapper'}) != None: page.find('div',attrs={'class':'wrapper'}).decompose()
                if page.find('div',attrs={'class':'breadcrumb'}) != None: page.find('div',attrs={'class':'breadcrumb'}).decompose()
                if page.find('div',attrs={'class':'js-touchpoint c-touchpoint-post-footer'}) != None: page.find('div',attrs={'class':'js-touchpoint c-touchpoint-post-footer'}).decompose()
                if page.find('div',attrs={'class':'js-touchpoint c-touchpoint-post-footerFixed'}) != None: page.find('div',attrs={'class':'js-touchpoint c-touchpoint-post-footerFixed'}).decompose()
                if page.find('div',attrs={'class':'c-communication-errors user-report'}) != None: page.find('div',attrs={'class':'c-communication-errors user-report'}).decompose()
                if page.find('footer',attrs={'class':'c-footer'}) != None: page.find('footer',attrs={'class':'c-footer'}).decompose()
            html_page = str(page.body)
            #html_page = ''
            #for elem in page.body.contents: html_page += str(elem)
            #html_page = str(page)'''

        with open(path_filename,'w') as fp: fp.write( html_page )
        with open(path_metafilename,'w') as fp: json.dump( meta,fp )
    else:
        #page = bs.BeautifulSoup( unicode( file(path).read().decode('utf-8',errors='ignore') ) )
        html_page = file(path_filename).read()
        meta = json.load( file( path_metafilename ) ) if os.path.exists( path_metafilename ) else {}

    return filename,meta

    #return str(page)
