
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
import re


import chardet
import pandas as pd

with open('PPR-ALL.csv', 'rb') as f:
    result = chardet.detect(f.readline())
    
rawDataset = pd.read_csv('PPR-ALL.csv', encoding=result['encoding'])

#list(rawDataset.columns.values)

rawDataset.columns = ['DateSold',
   'PropertyAddress',
   'PostCode',
   'County',
   'Price',
   'NotFullMarketPrice',
   'VATExclusive',
   'PropertyDescription',
   'SizeDescription']


rawDataset['DateSold'] =  pd.to_datetime(rawDataset['DateSold'], format='%d/%m/%Y')       
rawDataset['Price'] = [int(re.sub("[^0-9]", "", str(p.split('.')[0]))) if re.sub("[^0-9]", "", p.split(' ')[0]).isnumeric() else np.nan for p in rawDataset['Price']]


#add vat where necessary, for new builds
unkR =  [a + (a * 0.135) for a in rawDataset[(rawDataset['VATExclusive'] =='Yes') ]['Price']]
unkR_rowsIndex = rawDataset.index[(rawDataset['VATExclusive'] =='Yes') ]
rawDataset.loc[unkR_rowsIndex, 'PriceIncVat'] = unkR 

#populate rest of prices in PriceIncVat column
unkR =  [a  for a in rawDataset[(rawDataset['VATExclusive'] =='No') ]['Price']]
unkR_rowsIndex = rawDataset.index[(rawDataset['VATExclusive'] =='No') ]
rawDataset.loc[unkR_rowsIndex, 'PriceIncVat'] = unkR 



unkR =  ['' for a in recentRawDataset[(recentRawDataset['CountyOrPostcode'] =='co dublin') | (recentRawDataset['CountyOrPostcode'] =='dublin')]['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[(recentRawDataset['CountyOrPostcode'] =='co dublin') ]
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR 

#get most recent data, from just last 3 months
recentRawDataset = rawDataset[rawDataset['DateSold']>= '2017-12-01']




recentRawDataset['CountyOrPostcode'] = ''
#get RegionCategory for records where website = # (i.e. website was not saved)
#dataset['CountyOrPostcode'] = [subl.split(',')[::-1][0].strip().lower() for subl in dataset['PropertyAddress']]

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



def RegionFix1_NonDublin(df, correctValues):

    for i, ppty in df.iterrows():
        for locCat in correctValues:
            if  (locCat in df.loc[i]['PropertyAddress'].lower()) and  ('dublin' not in df.loc[i]['PropertyAddress'].lower()):
                #print('adsf')
                df.set_value(i,'CountyOrPostcode', locCat)
                break


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
            
    

RegionFix1_NonDublin(recentRawDataset, locations)  

RegionFix1_DublinOnly(recentRawDataset, locations)  

#lots of blanks, more cleanup of region required.





#Co Dublin is too big, need to subdivide it further
unkR =  ['' for a in recentRawDataset[(recentRawDataset['CountyOrPostcode'] =='co dublin') | (recentRawDataset['CountyOrPostcode'] =='dublin')]['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[(recentRawDataset['CountyOrPostcode'] =='co dublin') | (recentRawDataset['CountyOrPostcode'] =='dublin')]
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR 

unkR =  ['co dublin blackrock' if 'Blackrock' in a and 'Dublin' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR 

unkR =  [' co dublin malahide' if 'Malahide' in a and 'Dublin' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR 
           
unkR =  ['co dublin skerries' if 'Skerries,' in a  else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR 
           
unkR =  ['co dublin swords' if 'Swords,' in a  else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR 
           
unkR =  ['co dublin howth' if 'Howth,' in a  else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR 

unkR =  ['co dublin dalkey' if 'Dalkey,' in a  else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR 

unkR =  ['co dublin killiney' if 'Killiney,' in a  else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR 
           
unkR =  ['co dublin booterstown' if 'Booterstown,' in a  else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR 
           
unkR =  ['co dublin dunlaoghaire' if 'Dun Laoghaire' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR
           
unkR =  ['co dublin santry' if 'Santry' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR
           
unkR =  ['co dublin monkstown' if 'Monkstown' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR

unkR =  ['co dublin lucan' if 'Lucan' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR

unkR =  ['co dublin saggart' if 'Saggart' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR

unkR =  ['co dublin rathcoole' if 'Rathcoole' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR

unkR =  ['co dublin balbriggan' if 'Balbriggan' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR

unkR =  ['co dublin portmarnock' if 'Portmarnock' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR

unkR =  ['co dublin ballybrack' if 'Ballybrack' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR           

unkR =  ['co dublin rush' if 'Rush' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR   

unkR =  ['dublin 18' if 'Stillorgan' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR   

unkR =  ['co dublin glenageary' if 'Glenageary' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR   

unkR =  ['co dublin cabinteeley' if 'Cabinteeley' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR   

unkR =  ['co dublin donabate' if 'Donabate' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR   

unkR =  ['dublin 24' if 'Tallaght' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR   

unkR =  ['dublin 1' if 'Drumcondra' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR   

unkR =  ['dublin 6w' if 'Terenure' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR   

unkR =  ['dublin 15' if 'Finglas' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR   

unkR =  ['dublin 18' if 'Sandyford' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR   

unkR =  ['dublin 24' if 'Clondalkin' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR   

unkR =  ['dublin 24' if 'Citywest' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR 

unkR =  ['co dublin lusk' if 'Lusk' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR 

unkR =  ['dublin 6w' if 'Rathmines' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR 


#Any residual properties in co dublin, leave in co dublin
unkR =  ['co dublin misc' if 'Co. Dublin' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR

#County Dublin
unkR =  ['co dublin misc' if 'County Dublin' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR

#properties within dublin but unsure where they belong
unkR =  ['dublin' if 'Dublin' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR

#lot of churchtown properties without a postcode, should be D16
unkR =  ['dublin 16' if 'Churchtown' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR

   
#fix cork properties that dont have cork in address
unkR =  ['cork' if 'Douglas' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR
           
unkR =  ['cork' if 'Mallow' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR

unkR =  ['cork' if 'Charleville' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR    

unkR =  ['cork' if 'Bandon' in a else '' for a  in recentRawDataset[recentRawDataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = recentRawDataset.index[recentRawDataset['CountyOrPostcode'] =='']
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR 


#get rows where countyorpostcode is empty but postcode is not
unkR = recentRawDataset[((pd.notnull(recentRawDataset['PostCode'])) & (recentRawDataset['CountyOrPostcode'] == ''))]['PostCode'].str.lower()
unkR_rowsIndex = recentRawDataset.index[((pd.notnull(recentRawDataset['PostCode'])) & (recentRawDataset['CountyOrPostcode'] == ''))]
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR

#get rows where countyorpostcode is empty but county is not
unkR = recentRawDataset[((pd.notnull(recentRawDataset['County'])) & (recentRawDataset['CountyOrPostcode'] == ''))]['County'].str.lower()
unkR_rowsIndex = recentRawDataset.index[((pd.notnull(recentRawDataset['County'])) & (recentRawDataset['CountyOrPostcode'] == ''))]
recentRawDataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR

recentRawDataset[recentRawDataset['CountyOrPostcode'] == '']['CountyOrPostcode'].count()


#reset index and remove outliers
recentRawDataset = recentRawDataset[recentRawDataset['PriceIncVat'] <= 1000000]
recentRawDataset = recentRawDataset.reset_index(drop=True)


#add price bins to dataset
allbins = np.linspace(start = 0, stop =30000000, num = 1501, dtype = 'int64')
digitized = np.digitize(recentRawDataset['PriceIncVat'], allbins)


#assign the price bucket to each property
for i, r in recentRawDataset.iterrows() :
   recentRawDataset.loc[i,'price bin'] = allbins[digitized[i]]


PropetyPriceRegisterData = recentRawDataset


