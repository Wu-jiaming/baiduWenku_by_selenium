百度文库爬取
法1：seleniumChrome.py
	直接使用selenium包模拟浏览器，获取文库相应的资料

法2：
	bdocCrawler.py
	用request获取文库资源信息，
	txt，pdf，doc，ppt
	每种类型的爬取方法都不是一模一样
	需要做出相应的变化
	txt类型：
	#根据docId拼接成一个获取该文档的相关参数的url
	token_url="https://wenku.baidu.com/api/doc/getdocinfo?callback=cb&doc_id=" + self.docId
	target_url = "https://wkretype.bdimg.com/retype/text/" + self.docId +"?" + md5sum[1:] + "&callback=cb" + "&pn=1&rn=" + rn + "&type=txt" + "&rsign=" + rsign        
	
	ppt类型：
	token_url = 'https://wenku.baidu.com/browse/getbcsurl?doc_id=%s&type=ppt' % self.docId
	拼接url
	
	doc和pdf类型：
	#https://wkbjbos.bdimg.com/v1/docconvert6526//wk/811fa4e8422c5de31d8c69f0f512bf43/0.json?responseCacheControl=max-age%3D3888000&responseExpires=Wed%2C%2022%20Aug%202018%2023%3A09%3A52%20%2B0800&authorization=bce-auth-v1%2Ffa1126e91489401fa7cc85045ce7179e%2F2018-07-08T15%3A09%3A52Z%2F3600%2Fhost%2F22d2d8ab9ec0758227e761e3798f9e657967696e1bef2912167455106e9f2522&x-bce-range=257041-265481&token=b78d8a9d681a5bf572be51e3f483d19d78f1edd7ea39a165be90418e159289b2&expire=2018-07-08T16:09:52Z
    #wkbjbos.bdimg.com\\\\\\/v1\\\\\\/docconvert6526\\\\\\/\\\\\\/wk\\\\\\/811fa4e8422c5de31d8c69f0f512bf43\\\\\\/0.json?responseCacheControl=max-age%3D3888000&responseExpires=Wed%2C%2022%20Aug%202018%2023%3A41%3A08%20%2B0800&authorization=bce-auth-v1%2Ffa1126e91489401fa7cc85045ce7179e%2F2018-07-08T15%3A41%3A08Z%2F3600%2Fhost%2F533c8343b33dbcf0b617ed050cb4a33372a5cf8e8ca645ee1c4d8c910efa2019&x-bce-range=0-26687&token=d752155c1dd7789a712e0670cf8e63e217f2d4efe36d00cbbd8821650bf4d5a9&expire=2018-07-08T16:41:08Z\\x22
	从初始url，返回的content中查找url
	
	至于这些url怎么找出来，基本上都是从浏览器的f12找出来的，可以先把初始的network信息清空，然后再点击继续阅读，再看看network里的链接变化