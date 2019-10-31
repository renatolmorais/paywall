#!encoding: UTF-8

from requests import Session
import BeautifulSoup as bs
from re import match
from tags import tags_to_remove, tags_to_remove_by_host

def decompose(host,html_text):
	page = bs.BeautifulSoup(html_text.encode('utf-8'))
	# remover tags
	for tag in tags_to_remove:
		while page.find(tag): page.find(tag).decompose()
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
	return str(page)
	
if __name__ == '__main__':

	proxies = {'http':'http://proxy.almg.uucp:3128/','https':'http://proxy.almg.uucp:3128/'}
	#url = 'https://www.em.com.br/app/colunistas/luiz-carlos-azedo/2019/10/30/interna_luiz_carlos_azedo,1096859/a-tuitada-infeliz-dos-bolsonaro-sobre-leao-e-hienas.shtml'
	url = 'https://www.gazetadopovo.com.br/opiniao/bom-dia/a-morte-de-marielle-franco-e-o-que-o-principe-da-arabia-saudita-quer-com-o-brasil/'
	
	url_regex = 'htt(p|ps)://(?P<host>.*?)/.*'
	host = match(url_regex,url).group('host')
	
	ses = Session()
	resp = ses.get(url,proxies=proxies)
	with open('antes.html','w') as fp: fp.write(resp.text.encode('utf-8'))
	dec = decompose(host,resp.text)
	with open('depois.html','w') as fp: fp.write(dec)
	#print decompose(host,resp.text)
	