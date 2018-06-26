from selenium import webdriver
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
#options.add_argument('user-agent="Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"')
driver = webdriver.Chrome(chrome_options = options)
driver.get('https://wenku.baidu.com/view/aa31a84bcf84b9d528ea7a2c.html')
#之前一直没法模拟点击的原因是定位有误，以为定位越靠近鼠标点击的元素越好，其实不然，因为这样反而导致定位不正确（浏览器的左上角最上方是你定位元素的地方）
page = driver.find_elements_by_xpath("//div[@id='html-reader-go-more']")
driver.execute_script('arguments[0].scrollIntoView();', page[-1]) #拖动到可见的元素去
nextpage = driver.find_element_by_xpath("//span[@class='moreBtn goBtn']")
nextpage.click()

#test = driver.find_element_by_css_selector( '.clearfix.main-nav li  a')
#test.click()

html = driver.page_source

bs = BeautifulSoup(html, 'lxml')

#标题
#text没有()!!!
title = bs.find('title').text
print('title:', title)

#result = bs.select('')
result = bs.find_all(class_='ie-fix')

#页数
pageNums = len(result)
print('页数：',pageNums)
#获取每页的文库list
for each_result in result:
    bs2 = BeautifulSoup(str(each_result), 'lxml')
    texts = bs2.find_all('p')
    #print('texts', texts)
    #每页文库的p所有标签
    for each_text in texts:
        #print(each_text)
        #重新包装p标签，会有html把p标签抱起来，否则无法用下面的find_all方法
        main_body = BeautifulSoup(str(each_text), 'lxml')
        #print('main_body:', main_body)
        #抓取包装后标签里面的所有p标签
        for each in main_body.find_all('p'):
            #print(each)
            #print('each,name:', each.name)
            if each.name == 'span':
                #print('')
                #加end=""意味着后尾不换行
                print(each.string.replace('\xa0', ''), end='')
            #elif each.name == 'br':
            #    print('')
            #&ensp;这个在文库中意味着回车换行
            elif each.string == '&ensp;':
                print('\n')
            else:
                print(each.string, end='')
    print('------------------------------------')


#wait = WebDriverWait(driver, 10)

#schedule = driver.find_elements_by_xpath("//span[@class='pagerwg-arrow-lower']")
#driver.execute_script('arguments[0].scrollIntoView();', schedule[0])



#loadMore = driver.find_element_by_xpath("//span[@class='pagerwg-arrow-lower']")

#JavascriptExecuteScript execute =';';
#loadMore = driver.find_element_by_xpath("//div[@class='pagerwg-button']")
#loadMore = driver.find_element_by_xpath("//span[@class='pagerwg-arrow-lower']")
#loadMore.click()