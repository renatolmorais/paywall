utf8hosts = ['www.em.com.br','super.abril.com.br','www.uai.com.br']

tags_to_remove = ['script','iframe','noscript','header','style',]

tags_to_remove_by_host = {
	'www.em.com.br':
	{
        'remove':['aside',],
		'div':{'class':	['login-signature-call-bottom hidden-no-important show-loginwall-login-active-inline','nav-side__container','news-card__content','news-blocked-content','news-blocked js-news-blocked','news-blocked js-news-blocked-login','img-mobile-full mb-20','pl-15 pr-15 pt-xs-10 header-border-underline no-negative-xs',] },
		'small':{'class':	['hidden-print txt-no-serif',] },
		'p':{'class':	['text-xs-center',] },
		'footer':{'class':	['footer bg-gray-extra',] },
		'nav':{'class':	['fixed-btn-uai','nav-main','nav-main pt-8 pb-8 pt-xs-7 pb-xs-7'] },
		'section':{'class':	['bg-gray-extra mt-20','bg-gray-extra'] },
        'header':{'class':   ['hidden-print header-fixed js-header-fix'] },
        'aside':{'class':['hidden-print col-sm-10 col-sm-offset-1 col-md-offset-0 col-md-3 mb-35 scroll-linked',] },
	},
    'www.uai.com.br':
    {
        'remove':['aside',],
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
        'remove':['aside',],
		'div':		{'class':	['c-section-header','box-ads-header','header','wrapper','breadcrumb','js-touchpoint c-touchpoint-post-footer','js-touchpoint c-touchpoint-post-footerFixed','c-communication-errors user-report',] },
		'footer':	{'class':	['c-footer'],},
	},
	'gazetaonline.globo.com':
	{
		'remove':['iframe',],
	},
    'www1.folha.uol.com.br':
    {
        'remove':['svg','path','header','fieldset',],
        'img':{'class': ['gallery-widget__loading-spin',] },
        'div':{'id': ['c-sidebar-menu__content',],'class':['gallery-widget-share is-hidden','c-more-options','col col--md-1-3 col-offset--md-1-3 u-visible-md','col col--lg-5-18','u-only-print rs_skip','u-global-margin-bottom-component','c-wildcard-box u-global-margin-bottom-component',], },
        'ul':{'class':['c-tools-share__list',], },
        'h3':{'class':['c-subscribe-ads__title',], },
        'p':{'class':['c-subscribe-ads__description'],},
    },
    'exame.abril.com.br':
    {
        'remove':['aside','footer','article',],
        'div':{'class':['widget-popular-posts row','widget-news widget-box no-margin no-border','wrapper-referrers',] },
        'section':{'class':['sidebar-above-footer'], },
    },
    'crusoe.com.br':
    {
        'remove': ['svg','style',],
        'div':{'id':['content-paywall'], 'class':['paywall'], },
    },
    'www.forbes.com':
    {
        'remove':['path','svg',],
        'ul':{'class':['header__channels','fs-text-xxs fs-responsive-text color-body light-text print-tips',],},
        'div':{'class':['header__nav',],},
    },
    'oglobo.globo.com':
    {
        'remove':['!script','!style','svg',],
        'div':{'id':['detecta-adblock','barra-globocom','pub-floating',],'class':['barra-globocom',],},
        'ul':{'class':['barra-itens',],},
        'a':{'class':['barra-logo no-show large',],},
    }
}
