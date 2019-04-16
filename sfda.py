from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import pymssql

print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 开始执行...')

chrome_options = Options()

prefs = {
    'profile.default_content_setting_values': {
        'images': 2
    }
}

chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.binary_location = r'D:\Programs\Chrome\Application\chrome.exe'
driver = webdriver.Chrome(executable_path='D:/Apps/chromedriver.exe', chrome_options=chrome_options)

conn = pymssql.connect('ip', 'user', 'pwd', 'db')
curs = conn.cursor()
sql = "INSERT INTO ImportDrugs(RegCert,OldRegCert,RegCertRemark,PackageNum,CompanyNameZh,CompanyNameEn," \
      "AddressZh,AddressEn,RegionZh,RegionEn,ProductNameZh,ProductNameEn,GoodsNameZh,GoodsNameEn,ShapeType," \
      "Specification,PackSpecification,ManufacturerZh,ManufacturerEn,ManufacturerAddrZh,ManufacturerAddrEn," \
      "ManufacturerRegionZh,ManufacturerRegionEn,IssueDate,ExpireDate,PackCompanyName,PackCompanyAddr," \
      "PackBeginDate,PackExpireDate,ProductType,StandardCode) VALUES(" \
      "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

baseUrl = 'http://qy1.sfda.gov.cn/datasearchcnda/face3/'
baseSearch = 'search.jsp?tableId=36&bcId=152904858822343032639340277073&tableName=TABLE36&viewtitleName=COLUMN361&viewsubTitleName=COLUMN354,COLUMN823,COLUMN356,COLUMN355&tableView=%25E6%259D%25A9%25E6%25B6%2598%25E5%25BD%259B%25E9%2591%25BD%25EE%2588%259A%25E6%2590%25A7&State=1&curstart='
urls = []
contents = []
n = 0

try:
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 开始获取药品目录...')

    for i in range(134, 268):
        driver.get(baseUrl + baseSearch + str(i))

        e_urls = driver.find_elements_by_xpath("//table//a")

        for e_url in e_urls:
            urls.append(e_url.get_attribute("href").split(',')[1].strip("'"))

    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 开始获取药品详细信息...')

    for url in urls:
        n += 1
        try:
            driver.get(baseUrl + url)

            row_data = []
            for t in range(2, 33):
                row_data.append(driver.find_element_by_xpath(
                    "/html/body/div/div/table[1]/tbody/tr[" + str(t) + "]/td[2]").text)
            contents.append(tuple(row_data))

            if n % 1000 == 0:
                curs.executemany(sql, [row for row in contents])
                conn.commit()
                contents = []
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 已经入库' + str(n) + '条')

        except Exception as ex:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 解析页面出错：' + str(ex))

    if contents:
        curs.executemany(sql, [row for row in contents])
        conn.commit()

    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 入库成功！！！累计' + str(n) + '条')

except Exception as e:
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 执行出错：' + str(e))
finally:
    conn.close()
    driver.close()
    driver.quit()
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 执行结束')
