from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import pymssql

print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 开始执行...')

chrome_options = Options()

prefs = {
    'profile.default_content_setting_values': {
        'images': 2,
        'notifications': 2,
    }
}

# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'ignore-certificate-errors'])
chrome_options.binary_location = r'D:\Programs\Chrome\Application\chrome.exe'
driver = webdriver.Chrome(
    executable_path='D:/Apps/chromedriver.exe',
    chrome_options=chrome_options,
)

conn = pymssql.connect('ip', 'user', 'pwd', 'db')
curs = conn.cursor()
sql = "INSERT INTO YPSCQY(Number,Code,Class,Province,CompanyName,LR,CR,QR,RAddr,PAddr,PScope,BeginDate,ExpireDate) " \
      "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

baseUrl = 'http://app1.sfda.gov.cn/datasearchcnda/face3/'
baseSearch = 'search.jsp?tableId=34&bcId=152911762991938722993241728138&tableName=TABLE34&viewtitleName=COLUMN322&viewsubTitleName=COLUMN321&tableView=药品生产企业&State=1&curstart='
urls = []
contents = []
n = 0

try:
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 开始获取生产企业目录...')

    for i in range(1, 523):
        driver.get(baseUrl + baseSearch + str(i))

        e_urls = driver.find_elements_by_xpath("//table//a")

        for e_url in e_urls:
            urls.append(e_url.get_attribute("href").split(',')[1].strip("'"))

    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 开始获取生产企业详细信息...')

    for url in urls:
        try:
            driver.get(baseUrl + url)

            row_data = []
            for t in range(2, 15):
                row_data.append(driver.find_element_by_xpath(
                    '/html/body/div/div/table[1]/tbody/tr[' + str(t) + "]/td[2]").text)
            contents.append(tuple(row_data))
            n += 1
        except Exception as e:
            urls.append(url)
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 解析页面出错：' + str(e))

        try:
            if n % 1000 == 0:
                curs.executemany(sql, [row for row in contents])
                conn.commit()
                contents = []
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 已经入库' + str(n) + '条')
        except Exception as e:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 入库失败：' + str(e))

    try:
        if contents:
            curs.executemany(sql, [row for row in contents])
            conn.commit()
    except Exception as e:
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 入库失败：' + str(e))

    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 入库成功！！！累计' + str(n) + '条')

except Exception as e:
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 执行出错：' + str(e))
finally:
    conn.close()
    driver.close()
    driver.quit()
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 执行结束')
