from selenium import webdriver
import bs4
import re

def get_input(id):
    # id 부분에 정수를 입력하면 됨
    # https://www.nonograms.org/ 사이트 이용
    # id번호.txt 형식의 nonogram 입력 파일 생성해
    url = 'https://www.nonograms.org/nonograms/i/' + str(id)

    browser = webdriver.Chrome('/Users/lydiachung/Desktop/KHU/2019_1/DataBase/Project/chromedriver')
    browser.set_window_position(-10000, 0)
    browser.get(url)

    html = browser.page_source
    soup = bs4.BeautifulSoup(html,'html.parser')

    # regex 통해 데이터 추출
    tr = re.compile(r'<tr([\s\S]*?)>([\s\S]*?)</tr>')
    div = re.compile(r'<div>([\s\S]*?)</div>')

    # row에 해당하는 정보들 추출 위하여
    table1 = soup.find_all('td', {'class': 'nmtl'})
    count_tr1 = len(tr.findall(str(table1)))
    count_div1 = int(str(table1).count("div")) // 2
    rows = div.findall(str(table1))

    # col에 해당하는 정보들 추출 위하여
    table2 = soup.find_all('td', {'class': 'nmtt'})
    count_tr2 = len(tr.findall(str(table2)))
    count_div2 = int(str(table2).count("div")) // 2
    cols = div.findall(str(table2))

    w = open(str(id)+".txt", 'w')
    # 첫번째 줄인 size 작성
    first = str(count_tr1) + " " + str(count_div2 // count_tr2)
    w.write(first)

    # row constraint가 될 값들 입력
    num = count_div1 // count_tr1
    for i in range(count_tr1):
        line = ''
        temp = rows[num*i:num*(i+1)]
        for j in temp:
            if j=="\xa0":
                j = ""
        line = ' '.join(temp).strip()
        if len(line) == 0:
            line = '0'
        w.write('\n'+line)

    # col constraint가 될 값들 입력
    num = count_div2 // count_tr2
    lines = []
    for i in range(num):
        lines.append([])
    for i in range(count_tr2):
        temp = cols[num*i:num*(i+1)]
        for j in range(len(temp)):
            if temp[j] != '\xa0':
                lines[j].append(temp[j])

    for line in lines:
        line = ' '.join(line).strip()
        if len(line) == 0:
            line = '0'
        w.write('\n'+line)

    w.close()

    browser.close()