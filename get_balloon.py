import os
import sys
import time
import json
import codecs
import pickle
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import printer
# pip install selenium==4.8.3

def asr_main(contest_id):
    dict = {}
    # 读出
    with open("dict.pkl", "rb") as f:
        dict = pickle.load(f)

    #格式： 2023/05/07 17:59:08
    cnt=""
    with open("cnt.txt") as f:
        cnt = f.read()
    cnt = datetime.datetime.strptime(cnt, "%Y/%m/%d %H:%M:%S")
    maxCnt=cnt


    def out(team_id,team_name,problem_id,status,language,firstsolve):
        file = codecs.open('printer.txt','w','UTF-8')
        ball_id=team_name+problem_id
        if ball_id in dict:
            return
        dict[ball_id]=1
        file.write("----------------\n")
        file.write('BALLOON_STATUS\n')

        #气球颜色
        str_str = "气球颜色："+problem_id+"\n"
        file.write(str_str)

        #考场
        addr={}
        # 读入room文件
        with open("cfg_room.json", 'r', encoding='utf-8') as roomFile:
            addr = json.load(roomFile)



        #team_id
        room=team_id[0:1]
        if(room=="A" or room=="B" or room=="C" or room=="D" or room=="E" or room=="F" or room=="G"):
            str_str = "赛场："+addr[room]+"\n"
        else:
            str_str = "赛场："+"测试赛场"+"\n"
        file.write(str_str)
        addr.clear()
        #座位号
        str_str = "座位号："+team_id+"\n"
        file.write(str_str)
        #团队名称
        str_str = "团队名称："+team_name+"\n"
        file.write(str_str)
        #spilt
        file.write("----------------")
        file.close()
        printer.printer()





    # 获取部分
    problem_set_id = contest_id # problem set id为比赛id
    url = "https://pintia.cn/problem-sets/"+problem_set_id+"/submissions"


    executable_path = 'chromedriver.exe'
    service = webdriver.chrome.service.Service(executable_path)
    service.start()

    driver = webdriver.Chrome(service=service)
    driver.get(url)
    # 读取配置文件
    cfg={}
    with open('cfg.json', 'r') as f:
        cfg = json.load(f)
    cookies = [{'name': 'PTASession', 'value': cfg['cookie']}]
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get(url)


    time.sleep(1)




    html = driver.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(html, 'html.parser')
    # 找到所有数据
    titles = soup.find_all('tr')
    for title in titles:
        print(title.text)
        # 其中的一条数据
        if(title.text[0:1]=="提"):
            continue
        s=title.text[0:19]
        s = datetime.datetime.strptime(s, "%Y/%m/%d %H:%M:%S")
        if(s>maxCnt):
            maxCnt=s
        if(s<cnt):
            flag=False
        if(s>=cnt):
            position=title.text.index("详")
            position1=title.text.index("情")
            position2=title.text.index(")")

            status=title.text[19:position]
            problem_id=title.text[position1+1:position1+2]
            language=title.text[position1+2:position2+1]

            if "正确" in status:
                position3=title.text.index("ms")
                team_id=title.text[position3+2:position3+5]
                team_name=title.text[position3+6:]
                # print(team_id,team_name,problem_id,status,language)
                out(team_id,team_name,problem_id,status,language,"False")



    time.sleep(5)
    flag=True
    while True:
        if(flag==False):
            break
        next_page_button = driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[1]/div[3]/div[3]/button[2]')
        class_name = next_page_button.get_attribute("class")
        if "disabled" in class_name:
            break
        else:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            ActionChains(driver).move_to_element(next_page_button).click().perform()
        time.sleep(0.5)

        html = driver.execute_script("return document.documentElement.outerHTML")
        soup = BeautifulSoup(html, 'html.parser')
        titles = soup.find_all('tr')
        for title in titles:
            if(title.text[0:1]=="提"):
                continue
            s=title.text[0:19]
            s = datetime.datetime.strptime(s, "%Y/%m/%d %H:%M:%S")
            if(s>maxCnt):
                maxCnt=s
            if(s<cnt):
                flag=False
            if(s>=cnt):
                position = title.text.index("详")
                position1=title.text.index("情")
                position2=title.text.index(")")

                status=title.text[19:position]
                problem_id=title.text[position1+1:position1+2]
                language=title.text[position1+2:position2+1]

                if "正确" in status:
                    position3=title.text.index("ms")
                    team_id=title.text[position3+2:position3+5]
                    team_name=title.text[position3+6:]
                    # print(team_id,team_name,problem_id,status,language)
                    out(team_id,team_name,problem_id,status,language,"False")
                    


    maxCnt = maxCnt.strftime("%Y/%m/%d %H:%M:%S")
    with open('cnt.txt', 'w') as f:
        f.write(maxCnt)

    # 写入
    with open("dict.pkl", "wb") as f:
        pickle.dump(dict, f)