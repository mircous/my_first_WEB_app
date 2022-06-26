from flask import Flask
from flask import redirect
from flask import url_for
from flask import request
from flask import render_template
from flask import session
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import sqlite3
import ipdb
import os, sys




def get_content():
    connection = sqlite3.connect(str(os.getcwd()) + "/phonebook.db")
    cursor = connection.cursor()
    query1 = "SELECT * from Phonebookk"
    result = cursor.execute(query1)
    result = result.fetchall()
    """returns content from certain page"""
    WEBSITE_URL = result[0][0]
    ipdb.set_trace()
    response = requests.get(WEBSITE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup



def find_pictures_hrefs(content):
    gird = content.select('div.swiper-wrapper')[0].contents
    lst=[]
    for x in gird:
        try:
            y = x.contents[0].contents[0].attrs['data-src']
            lst.append(y)
        except:
            pass
    return lst

#!!!!!!!@@@@@@@@  NEED TO CHANGE FOTOS VAR @@@@@@@@@@@@@@@@@!!!!!!!!!!!!!!!

def save_pictures():
    y=0
    for z in find_pictures_hrefs(get_content()):
        img_data = requests.get(z).content
        with open(str(y)+'image.jpg', 'wb') as handler:
            handler.write(img_data)
        y += 1
    return "pictures are saved"


def main():
    #save_pictures()
    name = 'chamatebuli_linki_aq.com'
    connection = sqlite3.connect(str(os.getcwd()) + "/phonebook.db")
    cursor = connection.cursor()
    query1 = "INSERT INTO Phonebookk VALUES('{n}')".format(n = name)
    cursor.execute(query1)
    connection.commit()
    content = get_content()
    #"""returns needed info from certain page"""
    addresss = content.select('div.statement-title > span.address')[0].text
    address = addresss[7:-6].split('თბილისი')[0][0:-2]
    details = content.select('div.main-features.row.no-gutters > div.col-6.col-lg-4.mb-0.mb-md-4.mb-lg-0.d-flex.align-items-center.mb-lg-0.mb-4.pr-2.pr-lg-0')
    #''' binis farti'''
    needed_details = int(details[0].contents[1].contents[0].text.split('.')[0])
    #'''otaxebis raodenoba'''
    otaxi = int(details[0].contents[1].contents[1].text.split(' ')[0])
    #'''sartulebis raodenoba da chveni sartuli'''
    sartulebi = details[2].contents[1].contents[0].text
    current_floor = int(sartulebi.split('/')[0])
    total_floors = int(sartulebi.split('/')[1])

    #print(address)
    try:
        price = content.select('div.price-toggler-wrapper > div.d-flex.mb-2.align-items-center.justify-content-between')[0].contents[0].text.strip()
        try:
            frice = int(price.split(',')[0]+price.split(',')[1])
        except:
            try:
                frice = int(price)
            except:
                logging.info('2 much big %s', price)
    except ValueError:
        logging.info('Invalid path to %s', price)
    buxari = content.select('div.amenities > div.row > div.col-6')[1]
    classname = str(buxari.contents[1].contents[3])
    clearclassname = classname.split('class')[2].split('>')[0].split('"')[1]
    #'''კომენტარი'''
    try:
        comment = content.select('div.description > div > div.shortened > p.pr-comment.translated')[0].text
    except:
        comment = ' '
#    '''sivrce'''
    sivrce = content.select('div.amenities > div.row > div.col-6')[0].contents[1].contents
    ketilmowyoba = content.select('div.amenities > div.row > div.col-6')[1].contents[1].contents


    #print(ketilmowyoba)
    bathrooms = 0
    bedrooms = 0
    home_high = 2
    LoggiaSize = 0
    BalconySize = 0
    VerandaSize = 0
    StoreType = 0
    Parking = 0
    HotWater = 0
    gatboba = 0
    buxari = 0
    Gas = 0
    ElevatorRegular = 0
    ElevatorBig = 0
    Internet = 0
    Phone = 0
    TV = 0
    Furniture = 0

    try:
        bdroom = content.select('div.main-features > div')[1]
        bdrooms = bdroom.select('div > span.d-block')[0]
        bedrooms = bdrooms.text
        ipdb.set_trace()
        #bdrm = driver.find_element(By.XPATH, "/html/body/div[7]/div/div[5]/div[4]/div[2]/div/span[1]")
        #print(bdrm)
        #bedrooms = int(sivrce[3].text.split(' ')[1])
    except:
        pass

    mdgomareoba = sivrce[0].text

    try:
        home_high = float(sivrce[2].text.split(' ')[2])
    except:
        pass
    try:
        try:
            bathrooms = int(sivrce[7].text[-41])
        except:
            bathrooms = int(sivrce[7].text[-42])
    except:
    #    '''if not chosen will be empty str'''
        #bathrooms = sivrce[7].text[-46:-40]
        pass
    try:
        LoggiaSize = int(sivrce[6].text.split(' მ')[0].split('\t')[-1])
    except:
        pass
    try:
        BalconySize = int(sivrce[4].text.split(' ')[0].split('\t')[-1])
    except:
        pass
    try:
        VerandaSize = int(sivrce[4].text.split(' ')[0].split('\t')[-1])
    except:
        pass
    try:
        StoreType = sivrce[10].text.split('\t')[-1]
    except:
        pass
    try:
        Parking = sivrce[9].text.split('\t')[-1]
        if Parking == 'პარკინგი':
            Parking = 0
    except:
        pass
    try:
        HotWater = ketilmowyoba[0].text.split('\t')[-1]
    except:
        pass
    try:
        gatboba = sivrce[8].text.split('\t')[-1]
    except:
        pass
    try:
        buxari = ketilmowyoba[3].text
        if buxari == 'ბუხარი':
            buxari = 0
        else:
            buxari = 1
    except:
        pass
    try:
        Gas = ketilmowyoba[1].text
        if Gas == 'ბუნებრივი აირი':
            Gas = 0
        else:
            Gas = 1
    except:
        pass
    try:
        ElevatorRegular = ketilmowyoba[5].text
        if ElevatorRegular == 'სამგზავრო ლიფტი':
            ElevatorRegular = 0
        else:
            ElevatorRegular = 1
    except:
        pass
    try:
        ElevatorBig = ketilmowyoba[6].text
        if ElevatorBig == 'სატვირთო ლიფტი':
            ElevatorBig = 0
        else:
            ElevatorBig = 1
    except:
        pass
    try:
        Internet = ketilmowyoba[2].text
        if Internet == 'ინტერნეტი':
            Internet = 0
        else:
            Internet = 1
    except:
        pass
    try:
        Phone = ketilmowyoba[7].text
        if Phone == 'ტელეფონი':
            Phone = 0
        else:
            Phone = 1
    except:
        pass
    try:
        TV = ketilmowyoba[8].text
        if TV == 'ტელევიზორი':
            TV = 0
        else:
            TV = 1
    except:
        pass
    try:
        conditioner = ketilmowyoba[9].text
        if conditioner == 'კონდიციონერი':
            conditioner = 0
        else:
            conditioner = 1
    except:
        pass
    try:
        Furniture = ketilmowyoba[4].text
        if Furniture == 'ავეჯი':
            Furniture = 0
        else:
            Furniture = 1
    except:
        pass

    current_dict = {
        'comment':comment,
        'Furniture':Furniture,
        'conditioner':conditioner,
        'TV':TV,
        'Phone':Phone,
        'Internet':Internet,
        'ElevatorBig':ElevatorBig,
        'ElevatorRegular':ElevatorRegular,
        'Gas':Gas,
        'buxari':buxari,
        'gatboba':gatboba,
        'HotWater':HotWater,
        'Parking':Parking,
        'StoreType':StoreType,
        'VerandaSize':VerandaSize,
        'BalconySize':BalconySize,
        'LoggiaSize':LoggiaSize,
        'bathroom':bathrooms,
        'bedrooms':bedrooms,
        'address':address,
        'mdgomareoba':mdgomareoba,
        'home_high':home_high,
        'total_price':frice,
        'total_rooms':otaxi,
        'current_floor':current_floor,
        'total_floors':total_floors,
        "apartment_area":needed_details
    }
    #print(current_dict)
    return current_dict


if __name__ == '__main__':
    main()
