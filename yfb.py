from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from lxml import etree
import pymssql


print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 开始执行...')

chrome_options = Options()

prefs = {
    'profile.default_content_setting_values': {
        'images': 2
    }
}

# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.binary_location = r'D:\Programs\Chrome\Application\chrome.exe'
driver = webdriver.Chrome(executable_path='D:/Apps/chromedriver.exe', chrome_options=chrome_options)


conn = pymssql.connect('ip', 'user', 'pwd', 'db')
curs = conn.cursor()
sql = "INSERT INTO YFB_TEMP VALUES('药用辅料',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
# 原料药 药用辅料 药包材
baseUrl = 'http://www.cde.org.cn/yfb.do?method=list&yfbType=药用辅料&pageMaxNumber=5000&currentPageNumber=1'

try:
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 请求页面...')

    driver.get(baseUrl)

    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 下载页面...')

    html = etree.HTML(driver.page_source)

    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 解析页面...')

    # contents = driver.find_elements_by_xpath("/html/body/form/table/tbody/tr/td/table[4]/tbody/tr")
    # all_data = []
    # for x in contents:
    #     row_data = []
    #     for t in x.find_elements_by_tag_name("td"):
    #         row_data.append(t.text)
    #     all_data.append(tuple(row_data))

    rows = html.xpath('/html/body/form/table/tbody/tr/td/table[4]/tbody/tr/td[@class="newsindex"]/text()')

    all_data = []
    row_data = []
    i = 0

    for data in rows:
        i += 1
        row_data.append(data.strip())

        if i % 10 == 0:
            all_data.append(tuple(row_data))
            row_data = []

    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 数据入库...')

    curs.executemany(sql, [row for row in all_data])
    conn.commit()

    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 入库成功！！！')
except Exception as e:
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 执行出错：' + str(e))
finally:
    driver.close()
    driver.quit()
    conn.close()
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 执行结束')
