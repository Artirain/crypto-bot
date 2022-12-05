#импортируем aiogram для создания нашего бота
from aiogram import types, Dispatcher, executor, Bot

#дополнение к aiogram для корректирования текста
import aiogram.utils.markdown as fmt

#модуль selenium для парсинга
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#модуль time для обработки событий к selenium
from time import sleep


TOKEN = "5958748196:AAFZiSImCtblrpwU1wHpH_ajZ1zjm4i3pyw"

bot = Bot(token = TOKEN) #инициализируем бота

dp = Dispatcher(bot) #инициализируем обработчик событий бота

#обрабатываем команду старт, при нажатии бот будет выводить сообщение: 'Посмотреть текущие курсы известных криптовалют - /cryptocheck'
@dp.message_handler(commands = ["start"])
async def begin(message: types.Message):
    await bot.send_message(message.chat.id, "Посмотреть текущие курсы известных криптовалют - /cryptocheck")


#обработка команды /cryptocheck
@dp.message_handler(commands = ["cryptocheck"])
async def cryptocheck(message: types.Message):
    #Сообщение от бота про то, что идет прогрузка данных
    await bot.send_message(message.chat.id, "Идет прогрузка данных...")
    #переменная options, которая хранит стандартные настройки браузера Chrome
    options = webdriver.ChromeOptions()
    #параметр, который скрывает окно браузера Chrome
    options.headless = True

    browser = webdriver.Chrome(ChromeDriverManager().install(), options = options) #переменная browser, которая создает эмуляцию настоящего пользователя,
    #В options мы передаем все наши параметры для эмуляции браузера, которые мы указали выше

    #отправляем запрос на нам нужный сайт 
    browser.get("https://bitinfocharts.com/ru/crypto-kurs/")
    #делаем задержку для прогрузки сайта
    sleep(3)


    #Получаем все нужные нам элементы с помощью локатора xpath

    #получаем основной курс bitcoin на данный момент в долларах
    btc = browser.find_element('xpath', "//*[@id='tr_1']/td[2]/a")
    #получаем изменение курса в процентах за 12 часов
    btc2 = browser.find_element('xpath', "//*[@id='tr_1']/td[2]/span[1]")
    #получаем изменение курса в процентах за 7 дней
    btc3 = browser.find_element('xpath', "//*[@id='tr_1']/td[2]/span[2]")
    #забираем ссылку для большего ознакомления
    btc_href = browser.find_element('xpath', "//*[@id='tr_1']/td[2]/a") 
    

    #eth
    eth = browser.find_element('xpath', "//*[@id='tr_919']/td[2]/a")
    eth2 = browser.find_element('xpath', "//*[@id='tr_919']/td[2]/span[1]")
    eth3 = browser.find_element('xpath', "//*[@id='tr_919']/td[2]/span[2]")
    eth_href = browser.find_element('xpath', "//*[@id='tr_919']/td[2]/a")
    #смотрим какой знак(+ или -) у изменений курса bitcoin за 12 часов

    def btc_12h():
        #если первый знак равняется +
        if btc2.text[0] == "+":
            #тогда создаем словарь с заголовком title и сообщение бота с изменениями курса в процентах
            bit = {"title":fmt.text(f"Bitcoin повысился на {btc2.text}").replace(' в ', ' за ')}
            #выводим значение заголовка title из словаря bit
            return bit["title"]

        #если первый знак равняется -
        elif btc2.text[0] == "-":
            #тогда создаем словарь с заголовком title и сообщение бота с изменениями курса в процентах
            bit = {"title":fmt.text(f"Bitcoin опустился на {btc2.text}").replace(' в ', ' за ')}
            #выводим значение заголовка title из словаря bit
            return bit["title"]

    #смотрим какой знак(+ или -) у изменений курса bitcoin за 7 дней
    def btc_7d():
        if btc3.text[0] == "+":
            #тогда создаем словарь bit с заголовком title и сообщение бота с изменениями курса в процентах
            bit = {"title":fmt.text(f"Bitcoin повысился на {btc3.text}").replace(' в ', ' за ')}
            #выводим значение заголовка title из словаря bit
            return bit["title"]
        elif btc3.text[0] == "-":
            #тогда создаем словарь с заголовком title и сообщение бота с изменениями курса в процентах
            bit = {"title":fmt.text(f"Bitcoin опустился на {btc3.text}").replace(' в ', ' за ')}
            #выводим значение заголовка title из словаря bit
            return bit["title"]

    #eth
    def eth_12h():
        if eth2.text[0] == '+':
            eth = {"title":fmt.text(f"Ethereum повысился на {eth2.text}").replace(' в ', ' за ')}
            return eth["title"]
        elif eth2.text[0] == '-':
            eth = {"title":fmt.text(f"Ethereum опустился на {eth2.text}").replace(' в ', ' за ')}
            return eth["title"]

    def eth_7d():
        if eth3.text[0] == '+':
            eth2 = {"title":fmt.text(f"Ethereum повысился на {eth3.text}").replace(' в ', ' за ')}
            return eth2["title"]
        if eth3.text[0] == '-':
            eth2 = {"title":fmt.text(f"Ethereum опустился на {eth3.text}").replace(' в ', ' за ')}
            return eth2["title"]


    #Бот сообщает нам о курсе всех нам нужных криптовалют
    await message.answer(
        #создаем одно большое сообщения, в котором будет сообщаться подробности о нужных нам криптовалют
        fmt.text(
            #Бот выводит нам заголовок "---Bitcoin---" с "\n" для перехода на новою строку
            fmt.text("---Bitcoin---\n"),
            #Бот выводит нам текущий курс Bitcoin и переходим на новою строку
            fmt.text(f"Текущий курс:{btc.text}\n"),
            #Бот выводит нам изменения о курсе Bitcoin за 12 часов и переходим на новою строку
            btc_12h()+ "\n",
            #Бот выводит нам изменения о курсе Bitcoin за 7 дней и переходим на новою строку
            btc_7d() + "\n",
            #Бот дает нам ссылку для большего ознакомления
            fmt.text(f"Узнать больше о курсе Bitcoin можете по этой ссылке:\n", btc_href.get_attribute('href'))+"\n",

            fmt.text("---Ethereum---\n"),
            fmt.text(f"Текущий курс:{eth.text}\n"),
            eth_12h() + "\n",
            eth_7d() + "\n",
            fmt.text(f"Узнать больше о курсе Ethereum можете по этой ссылке:\n", eth_href.get_attribute('href'))+"\n",
        ),
        #скрываем панель ссылок
        disable_web_page_preview=True   
    )
    

#параметр, с помощью которого работает бот
executor.start_polling(dp)