import requests
import re
import json
import os
class BaiduWK(object):
    def __init__(self, url):
        self.title = None
        self.url = url
        self.docType = None
        self.headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}
        self.get_response_content(self.url)
        self.get_doc_type_and_title()

    def get_response_content(self, url):
        try:
            response = requests.get(url,headers=self.headers)
            return response.content
        except Exception as e:
            print(e)
            pass
    def get_doc_type_and_title(self):
        source_html = self.get_response_content(self.url)
        content = source_html.decode('gbk')
        self.docType = re.findall(r"docType.*?\:.*?\'(.*?)\'\,", content)[0]
        self.title = re.findall(r"title.*?\:.*?\'(.*?)\'\,", content)[0]

class BDWKTXT(BaiduWK):
    def __init__(self, url):
        super().__init__(url)
        self.docId = None
        pass

    def get_txt(self, url):
        #调用初始url获取docId
        source_html = self.get_response_content(url)
        content = source_html.decode('gbk')
        self.docId = re.findall(r"docId':.*?'(.*?)'", content)[0]
        print("docId:",self.docId)

        #根据docId拼接成一个获取该文档的相关参数的url
        #根据这些参数可以拼接成真正加载该文档的url
        token_url = "https://wenku.baidu.com/api/doc/getdocinfo?callback=cb&doc_id=" + self.docId
        first_json = self.get_response_content(token_url).decode()
        #获取精确的字符串类型json
        str_first_json = re.match(r".*?\(({.*?})\)", first_json).group(1)
        the_first_json = json.loads(str_first_json)
        #此url为加载真实数据json
        #https://wkretype.bdimg.com/retype/text/de364c3d33d4b14e842468a8?md5sum=f0c070c037d8943289171ab3b61c54a1&sign=63bb6e8af8&callback=cb&pn=1&rn=17&type=txt&rsign=p_17-r_0-s_f5ba2&_=1530979131643
        md5sum = the_first_json["md5sum"]
        rn = the_first_json["docInfo"]["totalPageNum"]
        rsign = the_first_json["rsign"]
        print("self.docId:", self.docId)
        target_url = "https://wkretype.bdimg.com/retype/text/" + self.docId +"?" + md5sum[1:] + "&callback=cb" + "&pn=1&rn=" + rn + "&type=txt" + "&rsign=" + rsign        
        print("target_utl:", target_url)
       
        #返回真实url的json
        txtJson = self.get_response_content(target_url).decode()
        #匹配字典，把一些多余符号去掉
        strTxtJson = re.match(r'.*\(\[(.*?)\]\)$', txtJson).group(1)
        #匹配字典里面的数据
        a = re.findall(r'"parags":\[(.*?"txt"})],', strTxtJson)
        resultTxt = ''
        print("=========================================")
        print("=========================================")
        for i in a:
            i = json.loads(i)
            dateTxt = i["c"].strip()
            print("123:",i["c"])
            resultTxt = resultTxt + dateTxt

        print("resultTxt:", resultTxt)
        self.writeTxt(resultTxt)

    """
    保存Txt文件
    """
    def writeTxt(self, strTxt):
        try:
            path = "." + os.sep + self.docType
            print(type(path), "path:", path)
            os.makedirs(path)
        except Exception as e:
            print("创建文件目录出错或已存在！")
            pass
        try:
            fileName = "." + os.sep + self.docType + os.sep +self.title + '.txt'
            with open(fileName, 'w', encoding = 'utf-8') as f:
                f.write(strTxt)
                print(self.title + ".txt保存成功！")
        except Exception as e:
            print(self.title + ".txt保存失败！")
            pass
class BDWKDOC(BaiduWK):
    def __init__(self, url):
        super().__init__(url)
        self.urlsList = list()

    def getUrlsList(self, url):
        source_html = self.get_response_content(url)
        content = source_html.decode('gbk')

        dataUrls = re.findall(r'wkbjbos\.bdimg\.com.*?json.*?expire.*?\}', content)
        # 从源码中批量提取数据url
        #https://wkbjbos.bdimg.com/v1/docconvert6526//wk/811fa4e8422c5de31d8c69f0f512bf43/0.json?responseCacheControl=max-age%3D3888000&responseExpires=Wed%2C%2022%20Aug%202018%2023%3A09%3A52%20%2B0800&authorization=bce-auth-v1%2Ffa1126e91489401fa7cc85045ce7179e%2F2018-07-08T15%3A09%3A52Z%2F3600%2Fhost%2F22d2d8ab9ec0758227e761e3798f9e657967696e1bef2912167455106e9f2522&x-bce-range=247560-257040&token=b78d8a9d681a5bf572be51e3f483d19d78f1edd7ea39a165be90418e159289b2&expire=2018-07-08T16:09:52Z
        #https://wkbjbos.bdimg.com/v1/docconvert6526//wk/811fa4e8422c5de31d8c69f0f512bf43/0.json?responseCacheControl=max-age%3D3888000&responseExpires=Wed%2C%2022%20Aug%202018%2023%3A09%3A52%20%2B0800&authorization=bce-auth-v1%2Ffa1126e91489401fa7cc85045ce7179e%2F2018-07-08T15%3A09%3A52Z%2F3600%2Fhost%2F22d2d8ab9ec0758227e761e3798f9e657967696e1bef2912167455106e9f2522&x-bce-range=257041-265481&token=b78d8a9d681a5bf572be51e3f483d19d78f1edd7ea39a165be90418e159289b2&expire=2018-07-08T16:09:52Z
        #wkbjbos.bdimg.com\\\\\\/v1\\\\\\/docconvert6526\\\\\\/\\\\\\/wk\\\\\\/811fa4e8422c5de31d8c69f0f512bf43\\\\\\/0.json?responseCacheControl=max-age%3D3888000&responseExpires=Wed%2C%2022%20Aug%202018%2023%3A41%3A08%20%2B0800&authorization=bce-auth-v1%2Ffa1126e91489401fa7cc85045ce7179e%2F2018-07-08T15%3A41%3A08Z%2F3600%2Fhost%2F533c8343b33dbcf0b617ed050cb4a33372a5cf8e8ca645ee1c4d8c910efa2019&x-bce-range=0-26687&token=d752155c1dd7789a712e0670cf8e63e217f2d4efe36d00cbbd8821650bf4d5a9&expire=2018-07-08T16:41:08Z\\x22
        #ba76f9e8c5da50e2534d7f12
        urlsList = list()        
        for url in dataUrls:
            url = "https://" + url.replace("\\\\\\/", "/")
            url = url[:-5]
            #print("url:", url)
            urlsList.append(url)
        #将处理好的urls列表保存成全局属性
        self.urlsList = urlsList
        return urlsList

    """
    从数据源的url列表提取数据
    """
    def getUrlsContent(self, urlsList):
        content = ''
        result = ''
        sum = len(urlsList)
        i = 1
        for url in urlsList:
            print("正在下载第%d条数据, 剩余%d条" % (i, sum - i))
            i += 1
            try:
                # 获取json数据
                content = self.get_response_content(url).decode()
                #print("urlContent:", content)
                #处理json数据
                content = re.match(r'.*?\((.*)\)$', content).group(1)

                # 将json数据中需要的内容提取出来
                urlDataBody = json.loads(content)["body"]
                #print("urlDataBody:", urlDataBody)
                #遍历获取所有信息,并将信息拼接到一起
                for bodyInfo in urlDataBody:
                    try:
                        result = result + bodyInfo["c"]
                        result =result.strip()
                        print(">>",result)
                    except Exception as e:
                        print(e)
                        pass

            except Exception as e:
                print(e)
                pass
        return result

    def writeDoc(self, strTxt):
        try:
            path = "." + os.sep + self.docType
            print(type(path), "path:", path)
            os.makedirs(path)
        except Exception as e:
            print("创建文件目录出错或已存在！")
            pass
        try:
            fileName = "." + os.sep + self.docType + os.sep +self.title + '.txt'
            with open(fileName, 'w', encoding = 'utf-8') as f:
                f.write(strTxt)
                print(self.title + ".txt保存成功！")
        except Exception as e:
            print(self.title + ".txt保存失败！")
            pass

class BDWKPPT(BaiduWK):
    def __init__(self, url):
        self.allImg_url = list()
        super().__init__(url)

    def getPPTJson(self):
        #https://wkretype.bdimg.com/retype/zoom/7aade8627e21af45b307a8f0?pn=1&o=jpg_6&md5sum=ea6e93ac5dd7c3aa0b6aa07e751dc384&sign=e549743d8b&png=0-37189&jpg=0-54682
        #https://wkretype.bdimg.com/retype/zoom/7aade8627e21af45b307a8f0?pn=2&o=jpg_6&md5sum=ea6e93ac5dd7c3aa0b6aa07e751dc384&sign=e549743d8b&png=37190-37432&jpg=54683-218010
        pptSourceContent = self.get_response_content(self.url)
        content = pptSourceContent.decode('gbk')
        with open('ppt.html', 'w') as f:
            f.write(content)
        #获取文档id
        self.docId = re.findall(r"docId':.*?'(.*?)'", content)[0]
        
        #这个链接至关重要，找到这个链接，在preview找到各个图片的链接
        #https://wenku.baidu.com/browse/getbcsurl?doc_id=ccdf062c43323968011c9242&pn=1&rn=99999&type=ppt&callback=jQuery11010007564097554838778_1531049476358&_=1531049476359
        token_url = 'https://wenku.baidu.com/browse/getbcsurl?doc_id=%s&type=ppt' % self.docId
        
        #将该url的json资源返回，并加载出来
        imgJson = self.get_response_content(token_url).decode()
        #print(imgJson)
        imgStrJson = json.loads(imgJson)
        with open("img.txt", 'w') as f:
            f.write(str(imgStrJson))


        try:
            os.makedirs("./ppt/%s" % (self.title))
        except Exception as e:
            print("文件夹ppt已经创建")

        pptTotalNum = (len(imgStrJson))
        for img_url in imgStrJson:
            #print(img_url)
            page = (img_url['page'])
            print("正在下载第%s页ppt，(还剩%s页)" % (page, pptTotalNum-page))
            path = "./ppt/%s/%s" % (self.title, str(img_url['page'])+'.jpg')
            print("path:", path)
            img = self.get_response_content(img_url["zoom"])
            with open(path, 'wb') as f:
                f.write(img)
        print("下载成功！")
        
def main():
    try:
        #url = input("请输入资源所在的百度文库网址：")
        url = 'https://wenku.baidu.com/view/37338aebdd36a32d72758152.html?from=search'
        #txt
        url = 'https://wenku.baidu.com/view/de364c3d33d4b14e842468a8.html?from=search'        
        #ppt
        url = 'https://wenku.baidu.com/view/ccdf062c43323968011c9242.html'
        #word
        url = 'https://wenku.baidu.com/view/ba76f9e8c5da50e2534d7f12.html?from=search'
        #pdf
        url = 'https://wenku.baidu.com/view/8c28a62e0a4c2e3f5727a5e9856a561252d3211e.html?from=search'
        docType = BaiduWK(url).docType
    except Exception as e:
        print(e)
        print("你输入的url有误，请重新输入！")
    print("类型为", "-->" ,docType)
    #url_list = ['https://wkbjbos.bdimg.com/v1/docconvert8854//wk/00ee67dec84a0d86a3d997a301472def/0.json?responseCacheControl=max-age%3D3888000&responseExpires=Sat%2C%2011%20Aug%202018%2000%3A02%3A03%20%2B0800&authorization=bce-auth-v1%2Ffa1126e91489401fa7cc85045ce7179e%2F2018-06-26T16%3A02%3A03Z%2F3600%2Fhost%2Fa6c3117e6e36e649f96932db79407abf1f80be7fc830f41d9d7cd4c1137ebf1d&x-bce-range=34133-47147&token=f6e2447e7cda3eea863834e311d2e5d5c539a44ac827f7af765753fc39435ee4&expire=2018-06-26T17:02:03Z']
    #BDWKTXT(url).get_txt(url)
    if docType == 'ppt':
        ppt = BDWKPPT(url)
        print("你将要获取演示文稿(PPT)名称为：", ppt.title)
        ppt.getPPTJson()
    elif docType == 'txt':
        txt = BDWKTXT(url)
        print("你将要下载的文本文档(txt)名称为：", txt.title)
        txt.get_txt(url)
    elif docType == 'doc':
        doc = BDWKDOC(url)
        print("你将要下载的word文档名称为：", doc.title)
        urlsList = doc.getUrlsList(url)
        result = doc.getUrlsContent(urlsList)
        doc.writeDoc(result)
    elif docType == 'pdf':
        doc = BDWKDOC(url)
        print("你将要下载的pdf文档名称为：", doc.title)
        urlsList = doc.getUrlsList(url)
        result = doc.getUrlsContent(urlsList)
        doc.writeDoc(result)       
    else:
        other = BDWKPPT(url)
        print("暂时不支持下载%s类型" % (other.docType))
        pass
if __name__ == '__main__':
    main()