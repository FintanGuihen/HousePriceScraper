
#**************************************************************************************
#Import Libraries
#**************************************************************************************
import bs4
from bs4 import BeautifulSoup
from urllib.request import urlopen
from time import sleep # be nice
import lxml
import time
from selenium import webdriver  
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.common.by import By
import re
import random
import pyodbc



#**************************************************************************************
#Create database connection
#**************************************************************************************
connection = pyodbc.connect('Driver={SQL Server};'
                                'Server=PRAXIS\sql2017;'
                                'Database=TestDatabase;'
                                'uid=pyLogin;pwd=pyPassw0rd') 



#**************************************************************************************
#Function to create a browser instance with the chrome driver
#**************************************************************************************
def getBrowser():
    #browser = webdriver.Chrome('C:\\Users\\fintanguihen\\OneDrive\\projects\\Python\\housing scraper\\chromedriver_win32\\chromedriver.exe')
    browser = webdriver.Chrome('C:\\Users\\FGuih\\OneDrive\\projects\\Python\\housing scraper\\chromedriver_win32\\chromedriver.exe')
    
    return browser
    
#**************************************************************************************
#Function to load a page within the browser instance
#**************************************************************************************
def getPage(browser):
    html = browser.page_source
    soup = BeautifulSoup(html, "lxml")
    return soup




#**************************************************************************************
#Instantiate browser & call the website. Wait a random number of seconds between browser calls
#Waits allow time for the page to render and also ensure we dont look like a DOS attack or scraper.
#**************************************************************************************
webBrowser = getBrowser()
webBrowser.get("https://www.myhome.ie")
sleep(random.randint(5,8))
mainPage = getPage(webBrowser)
sleep(random.randint(5,8))


#**************************************************************************************
#Find the dropdown containing all the location categories and put categories in a list
#**************************************************************************************
CountySearchDropdown = mainPage.select("#mhSearchForm > section.mhSearchForm__searchFilters > div > div > div.col-sm-3.col-md-2.col-xs-12 > label > my-home-multi-select > span > div > div.checkBoxContainer")
CountyLinks = CountySearchDropdown[0].find_all("a")

countyURLs = []

#**************************************************************************************
#Append search parameters for houses and apartments
#**************************************************************************************
for a in CountyLinks:
   #append on parameters to get houses and apartments
    countyURLs.append(a.attrs['href'] + "?type=36%7C97")
    



#**************************************************************************************
#Loop through each location category
#Within each category, loop through each property listing on a page until all pages are processed
#Then start again with the next category
#
#**************************************************************************************                  
for url in countyURLs:
    webBrowser.get(url)
    sleep(random.randint(5,8))
    CountyPropertyListings = getPage(webBrowser)
    sleep(random.randint(5,8))
    
    properties = CountyPropertyListings.find_all(class_='mhPropertyListItem property')
    
    

    MorePages = True
    nextpage = url
    while  (MorePages == True):
        
        for i in properties:
            print(len(i))
            beds = ''
            bath = ''
            ber = ''
            size = ''
            propertyType = ''
            price = ''
            address = ''
            agent = ''
            increase = ''
            decrease = ''
            PropertyUrl = ''
            
            for t in i.descendants:
        
                if(type(t) is bs4.element.Tag):     
                    if(t.has_attr('ng-if')):
                        
                        #**************************************************************************************
                        #Find particular ng-if tags wiht specific properties indicating the data we are looking for
                        #if they exist, pull the value into a variable and then save each row to the database. 
                        #Example lines from the page are shown below
                        # <span class="search-result-price-up" ng-if="property.PriceChangeIsIncrease"><i class="fa fa-chevron-up"></i> €30,000 on 2nd Feb 18</span>
                        # <span class="search-result-price-down" ng-if="!property.PriceChangeIsIncrease"><i class="fa fa-chevron-down"></i> -€100,000 on 21st Feb 17</span>
                        #**************************************************************************************   
                      #  print(t[0]['value'])
                      
                     
                      
                      if(t['ng-if'] == 'property.PriceChangeIsIncrease'):
                          increase = t.text
                          
                      if(t['ng-if'] == '!property.PriceChangeIsIncrease'):
                          decrease = t.text
                          
                      if(t['ng-if'] == 'property.PriceAsString && !property.NewHomePriceString'):
                          price = t.text
            
                      if(t['ng-if'] == 'property.BedsString'):
                          beds =  t.text
                          
                      if(t['ng-if'] == 'property.BathString'):
                          bath =  t.text            
                
                      if(t['ng-if'] == 'property.SizeStringMeters'):
                          size =  t.text  
                          
                      if(t['ng-if'] == 'property.PropertyType'):
                          propertyType =  t.text
                          
                      if(t['ng-if'] == 'property.EnergyRatingMediaPath'):
                          for c in t.descendants:
                              if(c['class'][0] == 'ber'):
                                  ber= c['alt']
                            
                      if(t['ng-if'] == 'property.AdditionalLogoUrls.length == 0'):
                          for c in t.descendants:
                              if(c.has_attr('ng-href')):
                                  agent = c['ng-href']
      
                    if(t.has_attr('class')):
                        if(t['class'][0] == 'address'):
                            for d in t.descendants:
                                
                                if(type(d) is bs4.element.Tag): 
                                    address = d.text
                                    PropertyUrl = d['ng-href']
           

            cursor = connection.cursor() 
            SQLCommand = ("INSERT INTO MyHome3 "
                             "(PropertyAddress, beds, baths, ber, size, propertyType, price, agent, increase, decrease, webpage, PropertyUrl) "
                             "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)")
            Values = [address, beds, bath, ber, size, propertyType, price, agent,  increase, decrease, nextpage, PropertyUrl] 
            cursor.execute(SQLCommand,Values) 
            connection.commit() 
            #connection.close()
                    
            np = CountyPropertyListings.select('#next')
            
            
            
        if(len(np)==0):
            print("setting nextpage to # aritifically")
            nextpage = '#'
        else:
            print("setting nextpage to a legit value found on the page")
            nextpage = np[0]['href']
            
        print('next page')
        print(nextpage)
    
        if(nextpage == '#'):
            print("if nextpage == #")
            MorePages = False
        else:
            
            webBrowser.get(nextpage)
            sleep(random.randint(5,8))
            CountyPropertyListings = getPage(webBrowser)
            sleep(random.randint(5,8))
            properties = CountyPropertyListings.find_all(class_='mhPropertyListItem property')
          
        
