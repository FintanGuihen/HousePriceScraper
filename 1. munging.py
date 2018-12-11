

#**************************************************************************************
#Import Libraries
#**************************************************************************************


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import pyodbc
import re




#**************************************************************************************
#Read data from database into dataframe
#**************************************************************************************
"""
#connect to sql server
connection = pyodbc.connect('Driver={SQL Server};'
                                'Server=PRAXIS\sql2017;'
                                'Database=TestDatabase;'
                                'uid=pyLogin;pwd=pyPassw0rd') 
"""
connection = pyodbc.connect('Driver={SQL Server};'
                                'Server=it-lt-11;'
                                'Database=TestDatabase;'
                                'uid=pyLogin;pwd=pyPassw0rd') 

sql = """

SELECT * FROM myHome3 

"""

dataset = pd.read_sql(sql, connection)




#**************************************************************************************
#rename some columns
#************************************************************************************** 
dataset.rename(columns ={'beds':'beds string',
                                   'baths':'baths string',
                                   'ber':'ber string',
                                   'size':'size string',
                                   'agent':'agent url',
                                   'increase':'increase string',
                                   'decrease':'decrease string',
                                   'url': 'property url'
                                   }, inplace = True)





#**************************************************************************************
#Convert Strings to numeric
#**************************************************************************************
dataset['beds'] = [pd.to_numeric(s, errors='coerce') for s in dataset['beds string'].str.strip().str.split(' ').str.get(0)]
dataset['bathrooms'] = [pd.to_numeric(s, errors='coerce')  for s in dataset['baths string'].str.strip().str.split(' ').str.get(0)]
dataset['size'] = [pd.to_numeric(s, errors='coerce')  for s in dataset['size string'].str.strip().str.replace('m2','', case=False)]


#**************************************************************************************
#get ber value from string
#**************************************************************************************
dataset['ber'] = dataset['ber string'].str.strip().str.split(' ').str.get(2)
dataset['ber'] = dataset['ber'].fillna('unk')


#**************************************************************************************
#get ber value if in a range
#**************************************************************************************
dataset['ber upper'] = [s.split('-')[0] if '-' in s else s  for s in dataset['ber']]
dataset['ber lower'] = [s.split('-')[1] if '-' in s else s  for s in dataset['ber']]

#get category from website - not useful, full of duplicates
#dataset['WebsiteRegionCategory'] = [subl[4] if len(subl) > 3 else ' ' for subl in [sub.split("/") for sub in dataset['webpage'].astype(str)]  ]# no longer reliable, use unknown region category instead

#**************************************************************************************
#get asking price
#**************************************************************************************
dataset['currentAskingPrice'] =  [int(re.sub("[^0-9]", "", str(p.split(' ')[0]))) if re.sub("[^0-9]", "", p.split(' ')[0]).isnumeric() else np.nan for p in dataset['price']]

#**************************************************************************************
#get increase and decrease data if available. may be useful in future
#**************************************************************************************
dataset['IncreaseInPrice'] =     [int(re.sub("[^0-9]", "", str(p.strip().split(' ')[0]))) if re.sub("[^0-9]", "", str(p.strip().split(' ')[0])).isnumeric() else np.nan for p in dataset['increase string']]
dataset['DecreaseInPrice'] =     [int(re.sub("[^0-9]", "", str(p.strip().split(' ')[0]))) - (int(re.sub("[^0-9]", "", str(p.strip().split(' ')[0])))*2) if re.sub("[^0-9]", "", str(p.strip().split(' ')[0])).isnumeric() else np.nan for p in dataset['decrease string']]

#**************************************************************************************
#populate unknown for unknown property types
#**************************************************************************************
dataset['propertyType'] = dataset['propertyType'].fillna('unknown')

#**************************************************************************************
#function get numeric values from price increase/decrease columns
#**************************************************************************************
def PriceChange(df):
    for i, ppty in df.iterrows():

        if np.isnan(df.loc[i]['IncreaseInPrice']) == False:
            #print('in increase if')
            df.set_value(i,'PriceChange', ppty['IncreaseInPrice'])
            df.set_value(i,'PriceDirection', 'up')
            
        
        if np.isnan(df.loc[i]['DecreaseInPrice']) == False:
            #print('in decrease if')
            df.set_value(i,'PriceChange', ppty['DecreaseInPrice'])
            df.set_value(i,'PriceDirection', 'down')
            
            
        else:
            #print('in unchanged if')
            df.set_value(i,'PriceChange', 0)
            df.set_value(i,'PriceDirection', 'unchanged')
            
       
PriceChange(dataset)

 
#**************************************************************************************
#create feature CountyOrPostcode. Within Dublin we use postcode and towns. 
#Only counties used for rest of country but breakdown may be useful at a future date.
#**************************************************************************************
dataset['CountyOrPostcode'] = ''


#**************************************************************************************
#list of location categories
#**************************************************************************************
locations = [ 'dublin 1'
,'dublin 2'
,'dublin 3'
,'dublin 4'
,'dublin 5'
,'dublin 6'
,'dublin 6w'
,'dublin 7'
,'dublin 8'
,'dublin 9'
,'dublin 10'
,'dublin 11'
,'dublin 12'
,'dublin 13'
,'dublin 14'
,'dublin 15'
,'dublin 16'
,'dublin 17'
,'dublin 18'
,'dublin 19'
,'dublin 20'
,'dublin 21'
,'dublin 22'
,'dublin 23'
,'dublin 24'
,'co dublin'
,'galway'
,'roscommon'
,'clare'
,'mayo'
,'cavan'
,'leitrim'
,'longford'
,'carlow'
,'donegal'
,'sligo'
,'kerry'
,'kildare'
,'kilkenny'
,'laois'
,'limerick'
,'louth'
,'meath'
,'westmeath'
,'wexford'
,'waterford'
,'wicklow'
,'tipperary'
,'offaly'
,'monaghan'
,'cork']



#**************************************************************************************
#function to set CountyOrPostcode to the  county for non dublin properties
#**************************************************************************************
def RegionFix1_NonDublin(df, correctValues):

    for i, ppty in df.iterrows():
        for locCat in correctValues:
            if  (locCat in df.loc[i]['PropertyAddress'].lower()) and  ('dublin' not in df.loc[i]['PropertyAddress'].lower()):
                #print('adsf')
                df.set_value(i,'CountyOrPostcode', locCat)
                break


#**************************************************************************************
#function to set CountyOrPostcode to the postCode county or in large postcodes, 
#the area within the postcode, only used on dublin properties
#**************************************************************************************
#for dublin properties, set CountyOrPostcode to the postcode, or in large postcodes, the area within the postcode
def RegionFix1_DublinOnly(df, correctValues):
    for i, ppty in df.iterrows():
        if ('dublin' in ppty['PropertyAddress'].lower() ) and (ppty['CountyOrPostcode'] == ''):
           # print(ppty['PropertyAddress'].lower())
            address = ppty['PropertyAddress'].split(',')[::-1]
            for line in address:
                for locCat in correctValues:
                   # print(line.lower().strip())
                   # print(locCat)
                    if  ( line.lower().strip() == locCat):
                        #print(line.lower().strip())
                        #print('adsf')
                        df.set_value(i,'CountyOrPostcode', locCat)
                        break
            
    
RegionFix1_NonDublin(dataset, locations)  
RegionFix1_DublinOnly(dataset, locations)      
        

#**************************************************************************************
#the following sections are to fix specific issues with the address
#**************************************************************************************


#**************************************************************************************
#Co Dublin is too big, need to subdivide it further into areas/townlands

unkR =  ['' for a in dataset[(dataset['CountyOrPostcode'] =='co dublin') | (dataset['CountyOrPostcode'] =='dublin')]['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[(dataset['CountyOrPostcode'] =='co dublin') | (dataset['CountyOrPostcode'] =='dublin')]
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR 

unkR =  ['co dublin blackrock' if 'Blackrock' in a and 'Dublin' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR 

unkR =  [' co dublin malahide' if 'Malahide' in a and 'Dublin' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR 
           
unkR =  ['co dublin skerries' if 'Skerries,' in a  else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR 
           
unkR =  ['co dublin swords' if 'Swords,' in a  else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR 
           
unkR =  ['co dublin howth' if 'Howth,' in a  else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR 

unkR =  ['co dublin dalkey' if 'Dalkey,' in a  else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR 

unkR =  ['co dublin killiney' if 'Killiney,' in a  else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR 
           
unkR =  ['co dublin booterstown' if 'Booterstown,' in a  else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR 
           
unkR =  ['co dublin dunlaoghaire' if 'Dun Laoghaire' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR
           
unkR =  ['co dublin santry' if 'Santry' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR
           
unkR =  ['co dublin monkstown' if 'Monkstown' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR

unkR =  ['co dublin lucan' if 'Lucan' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR

unkR =  ['co dublin saggart' if 'Saggart' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR

unkR =  ['co dublin rathcoole' if 'Rathcoole' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR

unkR =  ['co dublin balbriggan' if 'Balbriggan' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR

unkR =  ['co dublin portmarnock' if 'Portmarnock' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR

unkR =  ['co dublin ballybrack' if 'Ballybrack' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR           

unkR =  ['co dublin rush' if 'Rush' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR   

unkR =  ['dublin 18' if 'Stillorgan' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR   

unkR =  ['co dublin glenageary' if 'Glenageary' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR   

unkR =  ['co dublin cabinteeley' if 'Cabinteeley' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR   

unkR =  ['co dublin donabate' if 'Donabate' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR   

#**************************************************************************************
#some areas in dublin didnt include post code, code below individually fixes areas of greatest impact within the dataset

unkR =  ['dublin 24' if 'Tallaght' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR   

unkR =  ['dublin 1' if 'Drumcondra' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR   

unkR =  ['dublin 6w' if 'Terenure' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR   

unkR =  ['dublin 15' if 'Finglas' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR   

unkR =  ['dublin 18' if 'Sandyford' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR   

unkR =  ['dublin 24' if 'Clondalkin' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR   

unkR =  ['dublin 24' if 'Citywest' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR 

unkR =  ['co dublin lusk' if 'Lusk' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR 

unkR =  ['dublin 6w' if 'Rathmines' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR 


#**************************************************************************************
#county dublin areas where there are not enough present to go through individually.

unkR =  ['co dublin misc' if 'Co. Dublin' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR

unkR =  ['co dublin misc' if 'County Dublin' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR

unkR =  ['dublin' if 'Dublin' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR

#lot of churchtown properties without a postcode, should be D16
unkR =  ['dublin 16' if 'Churchtown' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR

   
#**************************************************************************************
#county cork areas htat dont have co Cork in the address

unkR =  ['cork' if 'Douglas' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR
           
unkR =  ['cork' if 'Mallow' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR

unkR =  ['cork' if 'Charleville' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR    

unkR =  ['cork' if 'Bandon' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR 

#**************************************************************************************
#get county for each property in dublin that may have a postcode but not a county       
dataset['County'] =  ['dublin' if 'dublin' in a else a for a  in dataset['CountyOrPostcode']] 


           
#**************************************************************************************
#assign either house or apartment type to each property
#**************************************************************************************


propertyTypes = set(dataset['propertyType'])


dataset['PropertyType'] = ''

housePattern = 'Bungalow|Cottage|Country House|Detached House|Dormer|Duplex|End of Terrace House|Holiday Home|House|Live-Work Unit|Mews|Period House|Semi-Detached House|Terraced House|Townhouse'
apartmentPattern = 'Apartment|Penthouse|Studio'


houseR = ['House' if a ==True else 'Apartment' for a in dataset.propertyType.str.contains(housePattern) ]
houseR_Index = dataset.index #dataset[dataset.propertyType.str.contains(housePattern)].index
dataset.loc[houseR_Index,'PropertyType'] = houseR

           

#**************************************************************************************
#remove duplicates from dataset
#**************************************************************************************
deduplicatedDataset = dataset.drop_duplicates(subset=[ 'PropertyAddress','propertyURL','currentAskingPrice','beds','bathrooms','size','ber lower','CountyOrPostcode','County','PropertyType' ],keep='first')[[ 'PropertyAddress','propertyURL','currentAskingPrice','beds','bathrooms','size','ber lower','CountyOrPostcode','County','PropertyType']]


#**************************************************************************************
#remove data with no nan for price
#most should already be populated but if not, they are in areas with very few properties
#**************************************************************************************
deduplicatedDataset = deduplicatedDataset[(pd.notnull(deduplicatedDataset.currentAskingPrice))].reset_index(drop=True)



#**************************************************************************************
#look for NAN's
#get mean for beds, bathrooms and size and use to fill in blanks/nan's
#**************************************************************************************
avgBedsByCountyOrPostcode = deduplicatedDataset['beds'].groupby(deduplicatedDataset['CountyOrPostcode']).mean()
avgBathroomsByCountyOrPostcode = deduplicatedDataset['bathrooms'].groupby(deduplicatedDataset['CountyOrPostcode']).mean()
avgSizeByCountyOrPostcode =  deduplicatedDataset['size'].groupby(deduplicatedDataset['CountyOrPostcode']).mean()
 
for i, r in deduplicatedDataset[deduplicatedDataset['beds'].isnull() == True].iterrows():
    deduplicatedDataset.loc[i, 'beds'] = avgBedsByCountyOrPostcode.loc[r['CountyOrPostcode']]
    
for i, r in deduplicatedDataset[deduplicatedDataset['bathrooms'].isnull() == True].iterrows():
    deduplicatedDataset.loc[i, 'bathrooms'] = avgBathroomsByCountyOrPostcode.loc[r['CountyOrPostcode']]
    
for i, r in deduplicatedDataset[deduplicatedDataset['size'].isnull() == True].iterrows():
    deduplicatedDataset.loc[i, 'size'] = avgSizeByCountyOrPostcode.loc[r['CountyOrPostcode']]
    
  
#**************************************************************************************
#remove any rows that are still nan. probably as there are too few properties to get a mean
    #**************************************************************************************
bedRowsDrop = deduplicatedDataset.ix[deduplicatedDataset['beds'].isnull() == True]
deduplicatedDataset = deduplicatedDataset.drop(bedRowsDrop.index)

bathRowsDrop = deduplicatedDataset[deduplicatedDataset['bathrooms'].isnull() == True]
deduplicatedDataset = deduplicatedDataset.drop(bathRowsDrop.index)

sizeRowsDrop = deduplicatedDataset.ix[deduplicatedDataset['size'].isnull() == True]
deduplicatedDataset = deduplicatedDataset.drop(sizeRowsDrop.index)


#**************************************************************************************
#reset index
#**************************************************************************************

deduplicatedDataset = deduplicatedDataset.reset_index(drop=True)


#**************************************************************************************
#add price bins to dataset.
#will be used for histogram
#**************************************************************************************
allbins = np.linspace(start = 0, stop =30000000, num = 1501, dtype = 'int64')
digitized = np.digitize(deduplicatedDataset['currentAskingPrice'], allbins)

#**************************************************************************************
#assign the price bucket to each property
#**************************************************************************************
for i, r in deduplicatedDataset.iterrows() :
   deduplicatedDataset.loc[i,'price bin'] = allbins[digitized[i]]

#**************************************************************************************
#rearrange columns
#**************************************************************************************
deduplicatedDataset = deduplicatedDataset[[
'PropertyAddress',
'propertyURL',
 'beds',
 'bathrooms',
 'size',
 'ber lower',
 'CountyOrPostcode',
 'County',
 'PropertyType',
 'price bin',
  'currentAskingPrice']]


#**************************************************************************************
#remove new line and carriage returns
#**************************************************************************************
deduplicatedDataset['PropertyAddress'] = deduplicatedDataset['PropertyAddress'].str.replace('\n',' ')
deduplicatedDataset['PropertyAddress'] = deduplicatedDataset['PropertyAddress'].str.replace('\r',' ')


#**************************************************************************************
#output final dataset with usable name
HousingWebsiteData = deduplicatedDataset

#NOTES:#Added PropertyAddress & propertyURL field to line 392 (deduplicate line) and to rearrange columns line. make sure this works



#**************************************************************************************
#output dataset to csv for exploration within powrbi & microsoft ML
#**************************************************************************************
HousingWebsiteData.to_csv('C:\Temp\FullDataset.csv')




    