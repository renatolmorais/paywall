'''
js-touchpoint c-touchpoint-post-footer
js-touchpoint c-touchpoint-post-footerFixed
c-communication-errors user-report
breadcrumb

host1
	tag1 attr1 attr2 ...
	tag2 attr1 attr2 ...
host2
	tag1 attr1 attr2 ...
	tag2 attr1 attr2 ...
...
'''

tags_to_remove = ['script','iframe','noscript','header']

tags_to_remove_by_host = {
	'www.em.com.br':
	{
		'remove':	['aside'],
		'div':		{'class':	['login-signature-call-bottom hidden-no-important show-loginwall-login-active-inline','nav-side__container','news-card__content','news-blocked-content','news-blocked js-news-blocked','news-blocked js-news-blocked-login'] },
		'small':	{'class':	['hidden-print txt-no-serif',] },
		'p':		{'class':	['text-xs-center',] },
		'footer':	{'class':	['footer bg-gray-extra',] },
		'nav':		{'class':	['fixed-btn-uai','nav-main','nav-main pt-8 pb-8 pt-xs-7 pb-xs-7'] },
		'section':	{'class':	['bg-gray-extra mt-20','bg-gray-extra'] },
	},
	'super.abril.com.br':
	{
		'header':	{'class':	['header'] },
		'div':		{'class':	['sidebar-top hidden-xs hidden-sm','widget-cover-container'] },
		'section':	{'class':	['comments','sidebar-above-footer',] },
	},
	'www.gazetadopovo.com.br':
	{
		'remove':	['aside'],
		'div':		{'class':	['header','wrapper','breadcrumb','js-touchpoint c-touchpoint-post-footer','js-touchpoint c-touchpoint-post-footerFixed','c-communication-errors user-report',] },
		'footer':	{'class':	['c-footer'],},
	},
	'gazetaonline.globo.com':
	{
		'remove':	['iframe'],
	}
}