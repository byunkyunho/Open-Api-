import json
import requests
import pygame as pg
import datetime
import time
import math
import xmltodict
from bs4 import BeautifulSoup
from xml.etree import ElementTree
import xml
from lxml import html
import random

dust_url = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureSidoLIst?serviceKey=qU6ZiWZWr9TyzBf4CSQePVRrLv656KwyxySrnDDH4o9I71HOfECubfmhWxHeIYMyg6X9yLyogSFQV0ucd9gFpA%3D%3D&numOfRows=25&pageNo=1&sidoName=%EC%84%9C%EC%9A%B8&searchCondition=DAILY&(&_returnType=json)"

# 일일 트래픽 다 썻을때 
# dust_url ="http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureSidoLIst?serviceKey=vd%2B2nNyF4R6cKQheiYx%2FnBKf3jBbnCb주urz0CpVI6lma62eC7DKIiVCvnIP8geQzI3muGUuDjvcWrKCKzrzyQhw%3D%3D&numOfRows=25&pageNo=1&sidoName=%EC%84%9C%EC%9A%B8&searchCondition=DAILY&(&_returnType=json)" #부

weather_url = "http://api.openweathermap.org/data/2.5/weather?lat=37&lon=126&appid=313d1d39ded06b928c0612edb94637a7"


dust_response = requests.get(dust_url)
weater_response = requests.get(weather_url)
json_data = dust_response.json()


weather_rescode = weater_response.status_code
dust_rescode = dust_response.status_code

load_sun = pg.image.load("image/태양.png")
load_cloud = pg.image.load("image/구름.png")
load_clouds = pg.image.load("image/구름많음.png")
load_rain = pg.image.load("image/비.png")
load_mist = pg.image.load("image/안개.png")
load_haze = pg.image.load("image/안개.png")
load_340 = pg.image.load("image/340.png")
load_3411 = pg.image.load("image/3411.png")
load_3412 = pg.image.load("image/3412.png")
load_N30 = pg.image.load("image/N30.png")
load_6300 = pg.image.load("image/6300.png")
botton_image = pg.image.load("image/버튼.png")
load_wd_background = pg.image.load("image/날씨미세배경.png")

bus_image_size = (130, 45)
bus_N30 = pg.transform.scale(load_N30, bus_image_size)
bus_340 = pg.transform.scale(load_340, bus_image_size)
bus_3412 = pg.transform.scale(load_3412, bus_image_size)
bus_6300 = pg.transform.scale(load_6300, bus_image_size)
bus_3411 = pg.transform.scale(load_3411, bus_image_size)

wd_background_image = pg.transform.scale(load_wd_background, (400, 490))

main_image_size = (90, 90)
sun_image = pg.transform.scale(load_sun, main_image_size)
clouds_image = pg.transform.scale(load_clouds, main_image_size)
rain_image = pg.transform.scale(load_rain, main_image_size)
cloud_image = pg.transform.scale(load_cloud, (100, 100))
mist_image = pg.transform.scale(load_mist, main_image_size)
haze_image = pg.transform.scale(load_haze, main_image_size)

okay = False
running = True
change_gu  = True
set_gu = True

set_information_one = True
nite = False

dust = 0
smalldust = 0
seoultemp = 0
reset_time = 0
news_x = 0
news2_x = -1700

news_list = []
grid = [1,1]
gu_list = []

# 혹시 필요할까봐
#["강남구", "강동구","강북구", "강서구", "관악구", "광진구", "구로구", "금천구", "노원구", "도봉구", "동대문구", "동작구", "마포구", "서대문구", "서초구", "성동구", "성북구", "송파구", "양천구", "영등포구", "용산구","은평구", "종로구", "중구", "중랑구"]

mygu = "강남구"

def set_bus_information():
    global bus_list, bus_response, bus_xml_data
    #bus_url = "http://ws.bus.go.kr/api/rest/stationinfo/getStationByUid?ServiceKey=qU6ZiWZWr9TyzBf4CSQePVRrLv656KwyxySrnDDH4o9I71HOfECubfmhWxHeIYMyg6X9yLyogSFQV0ucd9gFpA%3D%3D&arsId=25139"
    bus_url = "http://ws.bus.go.kr/api/rest/stationinfo/getStationByUid?ServiceKey=vd%2B2nNyF4R6cKQheiYx%2FnBKf3jBbnCburz0CpVI6lma62eC7DKIiVCvnIP8geQzI3muGUuDjvcWrKCKzrzyQhw%3D%3D&arsId=25139"
    bus_response = requests.get(bus_url).text.encode("utf-8")
    bus_xml_data = BeautifulSoup(bus_response, 'lxml-xml')
    bus_list = []

    for bus_num in bus_xml_data.find_all("rtNm")[1:4]:
        bus_list.append([bus_num.text])


    for a in bus_list:
        a.append("고덕역")

    #다음역
    b = 0
    for station in bus_xml_data.find_all("sectNm")[1:4]:
        bus_list[b].append(station.text.split("~")[0])
        b += 1
    
    b = 0
    #현재구간
    for itemlist in bus_xml_data.find_all("itemList")[1:4]:
        if itemlist.find("stationNm1") == None:
            bus_list[b].append("운행종료")
        else:
            bus_list[b].append(itemlist.find("stationNm1").text)
        b += 1
    

    #남은 시간
    b = 0
    for time in bus_xml_data.find_all("arrmsg1")[1:4]:
        if time.text == "운행종료":
            bus_list[b].append("운행종료")
        else:
            bus_list[b].append(time.text.split("분")[0])
        b += 1    

    for bus in bus_list:
        if bus[3] == bus[1]:
            bus.append(0)
        elif bus[3] == bus[2]:
            bus.append(1)
        else:
            bus.append(2)

    # 버스 이미지
    b = 0
    for bus in bus_list:
        if bus[0] == "6300":
            bus.append(bus_6300)
        if bus[0] == "3412":
            bus.append(bus_3412)
        if bus[0] == "3411":
            bus.append(bus_3411)
        if bus[0] == "N30":
            bus.append(bus_N30)
        if bus[0] == "340":
            bus.append(bus_340)



    # 운행종료 지우기
    if not nite:
        for a in range(3):
            for bus in bus_list:
                if bus[3] == "운행종료":
                    bus_list.remove(bus)






    # bus_list[0] 버스번호 bus_list[1] 고덕역  bus_list[2] 현재 위치  bus_list[3] 전역 bus_list[4] 남은 시간(분) bus_list[5]위치 0 ~ 2 bus_list[6] 버스 이미지

def set_news():
    global news, t_news, news2
    news_url = "https://www.yna.co.kr/"
    news_response = requests.get(news_url).text.encode("utf-8")
    news_soup = BeautifulSoup(news_response, 'html.parser')
    news_first_pasing = news_soup.find_all("div", class_ = "list-type063")
    news_list = []
    news2_list = []
    for a in news_first_pasing:
        for b  in a.find_all("strong", class_ = "tit-news"):
            news_list.append(b.text)
    news = ""
    news2 = ""
    for a in news_list[:3]:
        news = "{}     {}".format(news,a)
    for a in news_list[4:]:
        news2 = "{}     {}".format(news2,a)
  
def set_dust_level():
    global dust, dust_level, t_dust_color
    try:
        if dust < 31:
            dust_level = "좋음"
            t_dust_color = (0, 0, 255)
        elif dust > 30 and dust < 81:
            dust_level = "보통"
            t_dust_color = (0, 255, 0)
        elif dust> 80 and dust < 151:
            dust_level = "나쁨"
            t_dust_color = (255, 255, 0)
        elif dust> 150:
            dust_level = "매우나쁨"
            t_dust_color = (255, 0, 0)
    except:
        dust_level = ""
        t_dust_color = (0,0,0)

def set_smalldust_level():
    global smalldust, smalldust_level, t_smalldust_color
    
    try:
        if smalldust < 16:
            smalldust_level = "좋음"
            t_smalldust_color = (0, 0, 255)
        elif smalldust > 15 and smalldust < 35:
            smalldust_level = "보통"
            t_smalldust_color = (0, 255, 0)
        elif smalldust > 34 and smalldust < 76:
            smalldust_level = "나쁨"
            t_smalldust_color = (255, 255, 0)
        elif smalldust > 75:
            smalldust_level = "매우나쁨"
            t_smalldust_color = (255, 0, 0)
    except:
        smalldust_level = ""
        t_smalldust_color = (0,0,0)

def set_weather():
    global seoulweather, main_image
    if weather_json_data['weather'][0]['main'] == "Clear":
        seoulweather = "맑음"
        main_image = sun_image
    if weather_json_data['weather'][0]['main'] == "Clouds":
        seoulweather = "구름 많음"
        main_image = clouds_image
    if weather_json_data['weather'][0]['main'] == "Drizzle":
        seoulweather = "이슬비"
    if weather_json_data['weather'][0]['main'] == "Rain":
        seoulweather = "비"
        main_image = rain_image
    if weather_json_data['weather'][0]['main'] == "Mist":
        seoulweather = "안개"
        main_image = mist_image
    if weather_json_data['weather'][0]['main'] == "Haze":
        seoulweather = "안개"
        main_image = haze_image

def set_information():
    global okay, mygu, response, json, url, seoul, dust, smalldust, datatime, json_data, weather_url, response2, weather_json_data, seoulweather, main_image, seoultemp
    dust_response = requests.get(dust_url)
    weater_response = requests.get(weather_url)

    json_data = dust_response.json()
    weather_json_data = weater_response.json()

    seoul = json_data['list']

    set_weather()

    for gu in seoul:
        if mygu == gu['cityName']:

            okay = True
            print_information = False
            datatime = gu['dataTime']

            if gu['pm10Value'] == "":
                dust = "정보없음"
            else:
                if dust == int(gu['pm10Value']):
                    pass
                else:
                    dust = int(gu['pm10Value'])
                    print_information = True

            if gu['pm25Value'] == "":
                smalldust = "정보없음"
            else:
                if smalldust == int(gu['pm25Value']):
                        pass
                else:
                    smalldust = int(gu['pm25Value'])
                    print_information = True

            if seoultemp != (int(weather_json_data['main']['temp']) - 273) :
                seoultemp = (int(weather_json_data['main']['temp']) - 273)
                print_information = True

            if print_information:
                print_write()
            break

    set_dust_level()
    set_smalldust_level()

def print_write():

        #print("\n-----------------------------\n\n서울의 현재온도 : {}\n\n서울의 날씨 : {}\n\n{}의 미세먼지 농도 : {}\n\n{}의 초미세먼지 농도 : {}\n\n-----------------------------".format(seoultemp, seoulweather, mygu, dust ,mygu, smalldust))
        write = False
        dustfile = open("미세먼지기록.txt", "r")
        all_lines = dustfile.readlines()
        for line in all_lines:
            if line == "{}시에 측정한 서울의 온도는 {} 날씨는 {} {}의  미세먼지농도는 {}, 초미세먼지농도는 {}입니다.\n".format( datatime,seoultemp, seoulweather, mygu,dust, smalldust ):
                pass
                write = False
            else:
                write = True
        dustfile.close()
        if write:
            dustfile = open("미세먼지기록.txt", "a")
            dustfile.write("{}시에 측정한 서울의 온도는 {} 날씨는 {} {}의  미세먼지농도는 {}, 초미세먼지농도는 {}입니다.\n\n".format( datatime,seoultemp, seoulweather, mygu,dust, smalldust ))
            dustfile.close()    

def choose_gu():
    global mygu, okay, seoul, json_data
    while not okay:
        seoul = json_data['list']
        mygu = input("\n원하는 구를 입력하세요. ( 강동구, 강남구, 종로구, 관악구 ...) >>> ")
        for gu in seoul:
            if mygu == gu['cityName']:
                okay  = True
                break
            else:
                okay = False
        if not okay:
            print("\n잘못 입력하셨습니다.")

def set_time():
    global now, year, month, day, hour, minute, second
    now = datetime.datetime.now()
    year = now.strftime('%Y')
    month = now.strftime('%m')
    day = now.strftime("%d")
    hour = now.strftime('%H')
    minute = now.strftime('%M')
    second= now.strftime('%S')

set_bus_information()
set_news()

if dust_rescode == 200 and weather_rescode == 200:
    pg.init()
    pg.display.set_caption(" 변경호가 만듬 ")
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x = pg.mouse.get_pos()[0]
                mouse_y = pg.mouse.get_pos()[1]
                if mouse_x >= 140 and mouse_x <= 360:
                    if mouse_y >= 520 and mouse_y <= 594:
                        mouseclick = False
                        if change_gu:
                            change_gu = False
                            if not gu_list[(grid[1]-1)*5 + grid[0] - 1] == mygu:
                                set_information_one = True
                            mygu = gu_list[(grid[1]-1)*5 + grid[0] - 1]    
                        else:
                            change_gu = True
                    else:
                        mouseclick = True
                if mouseclick:
                    if change_gu:
                        grid = [((mouse_x - 80) // 70 ) + 1, ((mouse_y - 200)// 60) + 1]
                        if grid[0] > 5:
                            grid[0] = 5
                        if grid[0] < 1:
                            grid[0] = 1
                        if grid[1] > 5:
                            grid[1] = 5
                        if grid[1] < 1:
                            grid[1] = 1

        mouseclick = True

        screen = pg.display.set_mode((1000, 700))
        timefont = pg.font.SysFont("malgungothic", 40)
        font = pg.font.SysFont("malgungothic", 30)
        bigfont = pg.font.SysFont("malgungothic", 39)
        smallfont = pg.font.SysFont("malgungothic", 28)
        smallsmallfont = pg.font.SysFont("malgungothic", 16)
            
        if set_information_one:
            set_information()
            set_information_one = False

        if set_gu:
            seoul = json_data['list']
            for a in seoul:
                gu_list.append(a['cityName'])
            set_gu = False

        set_time()

        t_dust_level = smallfont.render(dust_level, True, t_dust_color)
        t_smalldust_level = smallfont.render(smalldust_level, True, t_smalldust_color)
        t_dust = smallfont.render("{} 미세먼지 : {}".format(mygu, dust), True, (0,0,0))
        t_smalldust = smallfont.render("{} 초미세먼지 : {}".format(mygu, smalldust) ,True, (0,0,0))
        t_seoulweather = smallfont.render("서울의 현재날씨 : {}".format(seoulweather), True, (0,0,0)) 
        t_seoultemp = smallfont.render("서울의 현재온도 : {}".format(seoultemp), True, (0,0,0))
        t_time = timefont.render("{}년 {}월 {}일 {}시 {}분 {}초".format(year, month, day, hour,minute, second), True, (0,0,0))
        t_botton = font.render("구 선택", True, (0,0,0))
        t_choose_gu = bigfont.render("구 선택", True, (0,0,0))
        t_okay = font.render("확인", True, (0,0,0))
        t_small_intro = bigfont.render("오늘의 날씨", True ,(0,0,0))
        t_news = font.render(news, True, (0,0,0))
        t_news2 = font.render(news2, True, (0,0,0))

        screen.fill((84, 195, 255))
        screen.blit(wd_background_image, (50, 120))
        screen.blit(t_time, (220, 30))
        #screen.blit(t_time, (490, 630))
        screen.blit(botton_image, (140, 520))
        screen.blit(t_news, (news_x, 630))
        screen.blit(t_news2, (news2_x, 630))

        if change_gu:
            screen.blit(t_okay, (220, 535))
            screen.blit(t_choose_gu, (190, 140))
            for a in range(5):
                for b in range(5):
                    if a + 1 == grid[0] and b + 1 == grid[1]:
                        pg.draw.rect(screen, (255,0,0), [80 +70*a,200 + 60*b ,70, 60], 3)
                    else:
                        pg.draw.rect(screen, (0,0,0), [80 + 70*a,200 + 60*b ,70, 60], 2)
            b = 0
            for a in gu_list:
                t_gu = smallsmallfont.render(a, True, (0,0,0))
                if b == 10 or b == 13 or b == 19:
                    screen.blit(t_gu, (83 + 70*(b%5), (b // 5) * 60 + 218))
                elif b == 23:
                    screen.blit(t_gu, (99 + 70*(b%5), (b // 5) * 60 + 218))
                else:
                    screen.blit(t_gu, (92 + 70*(b%5), (b // 5) * 60 + 218))
                b += 1

        else:
            screen.blit(t_botton, (200, 535))
            screen.blit(t_seoultemp, (80, 220)) 
            screen.blit(t_seoulweather, (80, 295))
            screen.blit(t_dust, (80, 370))
            if mygu =="영등포구" or mygu == "서대문구" or mygu == "동대문구":
                screen.blit(t_smalldust_level,(390, 445))
                screen.blit(t_dust_level, (380, 370))
            else:
                screen.blit(t_smalldust_level,(375, 445))
                screen.blit(t_dust_level, (360, 370))

            screen.blit(t_smalldust, (80, 445))
            screen.blit(t_small_intro, (145, 140))
            screen.blit(main_image, (350, 200))
        b = 1
        for bus in bus_list:
            pg.draw.line(screen, (0,0,0), (525, 30 +(b *(670/(len(bus_list) + 1)))),(925, 30 + (b *(670/(len(bus_list) + 1)))),3)
            cc = 0
            if bus[5] == 0:
                for circle in range(2):
                    pg.draw.circle(screen, (0,0,0),((525 + 400*cc), round(30 + (b *(670/(len(bus_list) + 1))))), 5)
                    cc += 1
            else:
                for circle in range(3):
                    pg.draw.circle(screen, (0,0,0),(525 + round((400/2)*cc), round(30 + (b *(670/(len(bus_list) + 1))))),5)
                    cc += 1

            screen.blit(bus[6], (460 + (400/2)*bus[5], (b *(670/(len(bus_list) + 1))) - 25 ))
            cc = 0 

            if bus[5] == 0:
                for station in bus[1:3]:
                    if len(station) > 10:
                        station = station.split(".")[0]
                    t_station_x = (len(station) - 3) * 7
                    t_staion = smallsmallfont.render(station, True, (0,0,0))
                    screen.blit(t_staion, (500 + 400*cc - t_station_x, 50 + (b *(670/(len(bus_list) + 1)))))
                    cc += 1
                
            else:
                for station in bus[1:4]:
                    if len(station) > 10:
                        station = station.split(".")[0]
                    t_station_x = (len(station) - 3) * 7
                    t_staion = smallsmallfont.render(station, True, (0,0,0))
                    screen.blit(t_staion, (500 + (400/2)*cc - t_station_x, 50 + (b *(670/(len(bus_list) + 1)))))
                    cc += 1

            if bus[4] == "곧 도착":
                t_left_tile = smallsmallfont.render("   곧 도착".format(bus[4]), True, (0,0,0))
            else:
                t_left_tile = smallsmallfont.render("약 {}분 남음".format(bus[4]), True, (0,0,0))
            screen.blit(t_left_tile, (680 ,90 + (b *(670/(len(bus_list) + 1)))))
            b += 1



        reset_time += 1
        if reset_time % 20000 == 0:
            set_information()
            set_news()

        if reset_time % 1000 == 0:
            set_bus_information()

        news_x += 2
        news2_x += 2
        if news_x > 1600:
            news_x = -3000
        if news2_x > 1600:
            news2_x = -3000
        
        pg.display.update()
 
else:
    print("연걸오류")

#고덕역 
    # arsid 25139
    # busrouteld = 100100224
    # 37.55503962, 127.15411576
#배재중고등학교 
    # arsid 25141
    # busrouteld = 100100055
#고덕평생학습관 
    # arsid 25137
    # busroutled = 

37.55503962, 127.15411576

# arsid 구하기
#http://ws.bus.go.kr/api/rest/stationinfo/getStationByName?ServiceKey=qU6ZiWZWr9TyzBf4CSQePVRrLv656KwyxySrnDDH4o9I71HOfECubfmhWxHeIYMyg6X9yLyogSFQV0ucd9gFpA%3D%3D&stSrch=고덕평생학습관

# busrouteld 구하기
#http://ws.bus.go.kr/api/rest/stationinfo/getLowStationByUid?ServiceKey=qU6ZiWZWr9TyzBf4CSQePVRrLv656KwyxySrnDDH4o9I71HOfECubfmhWxHeIYMyg6X9yLyogSFQV0ucd9gFpA%3D%3D&arsId=25137

#최종
#http://ws.bus.go.kr/api/rest/stationinfo/getStationByUid?ServiceKey=qU6ZiWZWr9TyzBf4CSQePVRrLv656KwyxySrnDDH4o9I71HOfECubfmhWxHeIYMyg6X9yLyogSFQV0ucd9gFpA%3D%3D&arsId=25139


