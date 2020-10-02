from urllib import request
import requests
import datetime
import urllib
import json
import time

token = "a627e66551df975403f1786cbf19c311d7ff20b23d84010fd866c5ce9a9c0077f88b445a68dfa6a8e01fd" #Сюда вводим свой токен.
timeKD = 30 #Сюда вводим время обновления статуса.(Время в секундах)

def startStatus():
    getCountry = requests.get(f"https://api.vk.com/method/account.getProfileInfo?v=5.95&access_token={token}").json()
    try:
        city = getCountry["response"]["city"]["title"]
    except KeyError:
        print("У профиля не указан город, по умолчанию была выбрана Москва.")
        city = "Москва"

    data = requests.get("http://api.openweathermap.org/data/2.5/weather",
    params = {"q": city,
              "appid": "778d98cf94b6609bec655b872f24b907",
              "units": "metric",
              "lang": "ru"}).json()
    try:
        getLikes = requests.get(f"https://api.vk.com/method/photos.get?album_id=profile&rev=1&extended=1&count=1&v=5.95&access_token={token}").json()
        getLikes = getLikes["response"]["items"][0]["likes"]["count"]
    except IndexError:
        print("У профиля отсутсвует аватар или лайки.")
        getLikes = 0

    getValuts = requests.get("https://currate.ru/api/?get=rates&pairs=USDRUB,EURRUB&key=6780a6de85b0690a6e0f02e6fc5bfd4f").json().get("data")
    Dollar = getValuts.get("USDRUB")
    Euro = getValuts.get("EURRUB")
    Dollar = Dollar[:Dollar.find('.')]
    Euro = Euro[:Euro.find('.')]

    today = datetime.datetime.today()
    nowTime = today.strftime("%H:%M")
    nowDate = today.strftime("%d.%m.%Y")

    statusSave = ("Время: {0} | Дата: {1} | Погода в '{2}': {3}℃ | Лайков на аве: {4} | Доллар: {5}р | Евро: {6}р".format(nowTime, nowDate,
        data["name"], str(data["main"]["temp"]), getLikes, Dollar, Euro))
    statusOut = requests.get(f"https://api.vk.com/method/status.set?text={statusSave}&v=5.95&access_token={token}").json()
    if statusOut.get("error", None):
        print(f"Не удалось обновить статус сервер вернул неверный код ответа: {statusOut}")
    else:
        print(f"Статус был обновлен")

while True:
    startStatus()
    time.sleep(timeKD)
