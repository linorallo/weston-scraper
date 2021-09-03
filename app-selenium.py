import requests, os, json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import db
driver = webdriver.Firefox()


def scrapProduct(productLink):
    #driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
    driverProduct = webdriver.Firefox()
    driverProduct.get(productLink)
    #get name
    productName = driverProduct.find_element_by_class_name('item-main-title').text
    print(productName)
    #get images
    imagesContainer = driverProduct.find_element_by_class_name('product-images')
    productImgTags = imagesContainer.find_elements_by_tag_name('img')
    productImages=[]
    for image in productImgTags:
        imageHref = image.get_attribute('data-src')
        if imageHref is None:
            imageHref = image.get_attribute('src')
        if imageHref != None:
            productImages.append(imageHref)

    #get specs

    specContainer = driverProduct.find_element_by_class_name('specs-container')
    specLists = specContainer.find_elements_by_tag_name('ul')
    productSpecifications = {}
    for list in specLists:
        specItems = list.find_elements_by_tag_name('li')
        for specItem in specItems:
            specItemField, specItemValue = specItem.find_elements_by_tag_name('span')
            productSpecifications[specItemField.text]=specItemValue.text
    i=1
    for productImage in productImages:
        r = requests.get(productImage, allow_redirects=True)
        try:
            modelNumber = productSpecifications['MODEL NUMBER'].split('/')[0]
            os.mkdir('./photos/'+modelNumber)
        except:
            pass
        extension  =os.path.basename(productImage).split('.')[1]
        dir = './photos/{}/{}'.format(
            modelNumber, modelNumber + '_{}.{}'.format(i, extension))
        open(dir, 'wb').write(r.content)
        i+=1
    driverProduct.close()
    #driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
    return {'name':productName, 'specs':productSpecifications}


def nextPage():
    try:
        navs = driver.find_elements_by_class_name('filter-inline-nav-item')
        found_nav = False
        print('nav',len(navs))
        i=0
        while  True:
            buttons = navs[i].find_elements_by_tag_name('li')
            print('buttons', len(buttons))
            for button in buttons:
                arrows = button.find_elements_by_class_name('fa-caret-right')
                print('button')
                if len(arrows) == 1:
                    aTag = button.find_element_by_tag_name('a')
                    ActionChains(driver).click(aTag).perform()
                    print('encontre next page')
                    return True
            i+=1
    except Exception as e:
        print(e)
        return False

def nextPageV2(currentPage):
    try:
        navs = driver.find_elements_by_class_name('filter-inline-nav-item')
        found_nav = False
        print('nav',len(navs))
        i=0
        #while False:
        nav = driver.find_element_by_xpath(
            '/html/body/div[6]/div[2]/div[1]/div[3]/div/div[1]/div/div/div[1]/div[1]/div[4]'
        )
        buttons = nav.find_elements_by_tag_name('li')
        for button in buttons:
            page = int(button.find_element_by_tag_name('a').text)
            print('page', page)
            if page == currentPage+1:
                aTag = button.find_element_by_tag_name('a')
                ActionChains(driver).click(aTag).perform()
                print('moviendo a page:', page)
                return True
            i += 1
            #arrows = button.find_elements_by_class_name('fa-caret-right')
            #print('button')
            #if len(arrows) == 1:
            #    aTag = button.find_element_by_tag_name('a')
            #    ActionChains(driver).click(aTag).perform()
            #    print('encontre next page')
            #    return True

    except Exception as e:
        print(e)
        return False


def scrapCategory():
    driver.refresh()
    productContainer = driver.find_element_by_id('prod-container')
    productsElements = productContainer.find_elements_by_class_name('mainImg')
    productsData = []
    i=1
    for product in productsElements:
        print('*'*10, 'PRODUCT #{}/{}'.format(i, len(productsElements)), '*'*10)
        productLink = product.get_attribute('href')
        if productLink[0] == '/':
            productLink = 'https://www.westonjewelers.com' + productLink
        productsData.append(scrapProduct(productLink))
        i+=1
        #break
    print('*'*10,'Retourning to category page','*'*10)
    return productsData




try:
    categories = [line.split()[0] for line in open('./categories.txt', 'r')]
    for category in categories:
        if (category):
            initPage = input('Init page: ')
            lastPage = input('Last page: ')
            pages = [category+str(idx) for idx in range(int(initPage), int(lastPage))]
            allData = []
            for page in pages:
                driver.get(page)
                print('Scraping', page)
                allData.append(scrapCategory())
                print('SCRAPPING DONE')
                #while nextPageV2(currentPage):
                #    scrapCategory()
                #    currentPage += 1
            db.saveToJSON(allData, pages.index(page))
except Exception as err:
    print(err)
    driver.close()