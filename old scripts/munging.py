
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import pyodbc
import re


connection = pyodbc.connect('Driver={SQL Server};'
                                'Server=PRAXIS\sql2017;'
                                'Database=TestDatabase;'
                                'uid=pyLogin;pwd=pyPassw0rd') 
"""
connection = pyodbc.connect('Driver={SQL Server};'
                                'Server=it-lt-11;'
                                'Database=TestDatabase;'
                                'uid=pyLogin;pwd=pyPassw0rd') 



"""
sql = """

SELECT * FROM myHome3 

"""

dataset = pd.read_sql(sql, connection)
# Importing the dataset

#dataset = pd.read_excel('property_for_sale.xlsx')


dataset.rename(columns ={'beds':'beds string',
                                   'baths':'baths string',
                                   'ber':'ber string',
                                   'size':'size string',
                                   'agent':'agent url',
                                   'increase':'increase string',
                                   'decrease':'decrease string'
                                   }, inplace = True)

dataset['beds'] = [pd.to_numeric(s, errors='coerce') for s in dataset['beds string'].str.strip().str.split(' ').str.get(0)]
dataset['bathrooms'] = [pd.to_numeric(s, errors='coerce')  for s in dataset['baths string'].str.strip().str.split(' ').str.get(0)]
dataset['size'] = [pd.to_numeric(s, errors='coerce')  for s in dataset['size string'].str.strip().str.replace('m2','', case=False)]
dataset['propertyType'] = dataset['propertyType'].fillna('unknown')
dataset['ber'] = dataset['ber string'].str.strip().str.split(' ').str.get(2)
dataset['ber'] = dataset['ber'].fillna('unk')
dataset['ber upper'] = [s.split('-')[0] if '-' in s else s  for s in dataset['ber']]
dataset['ber lower'] = [s.split('-')[1] if '-' in s else s  for s in dataset['ber']]
dataset['propertyType'] = dataset['propertyType'].fillna('unknown')
dataset['WebsiteRegionCategory'] = [subl[4] if len(subl) > 3 else ' ' for subl in [sub.split("/") for sub in dataset['webpage'].astype(str)]  ]# no longer reliable, use unknown region category instead
dataset['currentAskingPrice'] =  [int(re.sub("[^0-9]", "", str(p.split(' ')[0]))) if re.sub("[^0-9]", "", p.split(' ')[0]).isnumeric() else np.nan for p in dataset['price']]
dataset['IncreaseInPrice'] =     [int(re.sub("[^0-9]", "", str(p.strip().split(' ')[0]))) if re.sub("[^0-9]", "", str(p.strip().split(' ')[0])).isnumeric() else np.nan for p in dataset['increase string']]
dataset['DecreaseInPrice'] =     [int(re.sub("[^0-9]", "", str(p.strip().split(' ')[0]))) - (int(re.sub("[^0-9]", "", str(p.strip().split(' ')[0])))*2) if re.sub("[^0-9]", "", str(p.strip().split(' ')[0])).isnumeric() else np.nan for p in dataset['decrease string']]



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

 
dataset['CountyOrPostcode'] = ''
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
            
    

RegionFix1_NonDublin(dataset, locations)  

RegionFix1_DublinOnly(dataset, locations)      
        


#reset co dublin to blank, for testing only 
unkR =  ['' for a in dataset[(dataset['CountyOrPostcode'] =='co dublin') | (dataset['CountyOrPostcode'] =='dublin')]['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[(dataset['CountyOrPostcode'] =='co dublin') | (dataset['CountyOrPostcode'] =='dublin')]
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR 

           
#get category for addressess with variation & mistakes
#places in co dublin

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


#Co. Dublin
unkR =  ['co dublin misc' if 'Co. Dublin' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR

#County Dublin
unkR =  ['co dublin misc' if 'County Dublin' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR

#Dublin
unkR =  ['dublin' if 'Dublin' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR

unkR =  ['dublin 16' if 'Churchtown' in a else '' for a  in dataset[dataset['CountyOrPostcode'] =='']['PropertyAddress'].astype(str)]
unkR_rowsIndex = dataset.index[dataset['CountyOrPostcode'] =='']
dataset.loc[unkR_rowsIndex, 'CountyOrPostcode'] = unkR
           
#cork   
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
           

propertyTypes = set(dataset['propertyType'])

dataset['PropertyType'] = ''

housePattern = 'Bungalow|Cottage|Country House|Detached House|Dormer|Duplex|End of Terrace House|Holiday Home|House|Live-Work Unit|Mews|Period House|Semi-Detached House|Terraced House|Townhouse'
apartmentPattern = 'Apartment|Penthouse|Studio'


houseR = ['House' if a ==True else 'Apartment' for a in dataset.propertyType.str.contains(housePattern) ]
houseR_Index = dataset.index #dataset[dataset.propertyType.str.contains(housePattern)].index
dataset.loc[houseR_Index,'PropertyType'] = houseR

   #get county level           
dataset['County'] =  ['dublin' if 'dublin' in a else a for a  in dataset['CountyOrPostcode']] 


#get deduplicated  dataset
deduplicatedDataset = dataset.drop_duplicates(subset=[ 'currentAskingPrice','beds','bathrooms','size','ber lower','CountyOrPostcode','County','PropertyType' ],keep='first')[[ 'currentAskingPrice','beds','bathrooms','size','ber lower','CountyOrPostcode','County','PropertyType']]

#remove data with no nan for price
deduplicatedDataset = deduplicatedDataset[(pd.notnull(deduplicatedDataset.currentAskingPrice))].reset_index(drop=True)


#look for NAN's
#deduplicatedDataset.beds.isnull().sum()#274
#deduplicatedDataset.bathrooms.isnull().sum()#1172
#deduplicatedDataset.size = deduplicatedDataset['size'].astype(float)


#get mean beds, baths and size by CountyOrPostcode
avgBedsByCountyOrPostcode = deduplicatedDataset['beds'].groupby(deduplicatedDataset['CountyOrPostcode']).mean()
avgBathroomsByCountyOrPostcode = deduplicatedDataset['bathrooms'].groupby(deduplicatedDataset['CountyOrPostcode']).mean()
avgSizeByCountyOrPostcode =  deduplicatedDataset['size'].groupby(deduplicatedDataset['CountyOrPostcode']).mean()
 


#replace any rows that have nan, with appropriate mean 
for i, r in deduplicatedDataset[deduplicatedDataset['beds'].isnull() == True].iterrows():
    deduplicatedDataset.loc[i, 'beds'] = avgBedsByCountyOrPostcode.loc[r['CountyOrPostcode']]
    
for i, r in deduplicatedDataset[deduplicatedDataset['bathrooms'].isnull() == True].iterrows():
    deduplicatedDataset.loc[i, 'bathrooms'] = avgBathroomsByCountyOrPostcode.loc[r['CountyOrPostcode']]
    
for i, r in deduplicatedDataset[deduplicatedDataset['size'].isnull() == True].iterrows():
    deduplicatedDataset.loc[i, 'size'] = avgSizeByCountyOrPostcode.loc[r['CountyOrPostcode']]
    
  
#remove any rows that are still nan. probably as there are too few properties to get a mean
bedRowsDrop = deduplicatedDataset.ix[deduplicatedDataset['beds'].isnull() == True]
deduplicatedDataset = deduplicatedDataset.drop(bedRowsDrop.index)

bathRowsDrop = deduplicatedDataset[deduplicatedDataset['bathrooms'].isnull() == True]
deduplicatedDataset = deduplicatedDataset.drop(bathRowsDrop.index)

sizeRowsDrop = deduplicatedDataset.ix[deduplicatedDataset['size'].isnull() == True]
deduplicatedDataset = deduplicatedDataset.drop(sizeRowsDrop.index)




#add price bins to dataset
allbins = np.linspace(start = 0, stop =30000000, num = 15001, dtype = 'int64')
digitized = np.digitize(deduplicatedDataset['currentAskingPrice'], allbins)


#assign the price bucket to each property
for i, r in deduplicatedDataset.iterrows() :
   deduplicatedDataset.loc[i,'price bin'] = allbins[digitized[i]]
   

deduplicatedDataset = deduplicatedDataset[[

 'beds',
 'bathrooms',
 'size',
 'ber lower',
 'CountyOrPostcode',
 'County',
 'PropertyType',
 'price bin',
  'currentAskingPrice']]


"""
codub = deduplicatedDataset[deduplicatedDataset['CountyOrPostcode'] =='dublin']
codub.to_csv('C:\Temp\output.csv')
"""



#identify rows with no RegionCategory
sample = dataset[dataset['CountyOrPostcode'] =='']
#201 rows with no region category currently
multiListings = dataset[dataset['ber string'].str.contains('-')==True]
#83 listings of multiple properties









#examine a particular column
dataset['ber'].describe()
dataset['ber'].unique()
dataset.iloc[14553]['propertyURL']
dataset['ber'].str.contains('-')
dataset[dataset['ber string'] =='Energy Rating B2-D1']
db = db.sort(['CountyOrPostcode'])

#grouping and aggregating
agg = dataset.groupby('RegionCategory')['RegionCategory'].agg(['count'])





#***************************************Initial Analysis*********************************************************


#*****************************SUMMARY STATS************************************************************


#Average Country Wide Asking Price.
mean = deduplicatedDataset['currentAskingPrice'].mean()
#Median Country Wide Asking Price.
median =deduplicatedDataset['currentAskingPrice'].median()
#Mode Country Wide Asking Price
mode = deduplicatedDataset['currentAskingPrice'].mode()

individualResult = pd.DataFrame([['all', mean, median,mode]], columns=['Region', 'Mean', 'Median', 'Mode'])
counties = deduplicatedDataset.County.unique()
summaryStatsDF = pd.DataFrame(columns=['County','Mean','Median', 'Mode'])

#get summary stats. note mode is a series as it can have 0 or multiple values
for c in counties:
    aggData = deduplicatedDataset[deduplicatedDataset['County'] == c]['currentAskingPrice']
    mean = aggData.mean()
    median = aggData.median()
    mode = aggData.mode().astype('float64')
    print(c)
    print(mode)
    ##asdf =pd.DataFrame([[c, mean, median, mode[0]]],columns=['County','Mean','Median', 'Mode'])
    summaryStatsDF = summaryStatsDF.append(asdf)

    

#*****************************HISTOGRAMS************************************************************

def CreateHistogram(data, regionFilter, filterInverse,yMax):
    if filterInverse == True:
        d = data[ (np.isnan(data[regionFilter]) == False) & ~(data.CountyOrPostcode.str.contains(regionFilter) )]
        title = 'All Except ' + regionFilter
    else:
        d = data[(data['CountyOrPostcode'] == regionFilter ) & (pd.notnull(data.currentAskingPrice))]
        title = regionFilter
    
    plt.hist(d['currentAskingPrice'], b)
    if yMax != 0:
        plt.ylim(ymax = yMax, ymin = 0)
    plt.grid(zorder=0)
    plt.title(title)
    plt.show()
    

b = np.arange(0,2000000, 20000)

minPrice = min(deduplicatedDataset[deduplicatedDataset['price bin'] < 2000000]['price bin'])
maxPrice = max(deduplicatedDataset[deduplicatedDataset['price bin'] < 2000000]['price bin'])

dublinOnly = deduplicatedDataset[(deduplicatedDataset.CountyOrPostcode.str.contains('dublin') ) & (pd.notnull(deduplicatedDataset.currentAskingPrice))]
everywhereExceptDublin = deduplicatedDataset[ (np.isnan(deduplicatedDataset['currentAskingPrice']) == False) & ~(deduplicatedDataset.CountyOrPostcode.str.contains('dublin'))]




#Histogram for all of ireland
plt.hist(deduplicatedDataset[deduplicatedDataset['price bin'] < 1800000]['price bin'], b, color = 'red')   
plt.xticks(rotation=90)
plt.xticks(np.arange(0, maxPrice + 50000, 40000))
plt.yticks(np.arange(0, 1100, 100))

plt.grid(zorder=0)

#Histogram for just dublin
plt.hist(dublinOnly[dublinOnly['price bin'] < 1800000]['price bin'], b, color = 'blue', label = 'Dublin Only')   
plt.xticks(rotation=90)
plt.xticks(np.arange(0, maxPrice + 50000, 40000))
plt.yticks(np.arange(0, 1100, 100))
plt.legend(['Dublin Only','All Ireland'])
plt.show()

#whole country
#price less than mortgage limit for average salary ( 37500 x 3.5)
deduplicatedDataset[(deduplicatedDataset['currentAskingPrice'] < 132000) ]
#affordable price and house and greater than 1 bed
deduplicatedDataset[(deduplicatedDataset['currentAskingPrice'] < 132000) & (deduplicatedDataset['PropertyType'] =='House') & (deduplicatedDataset['beds'] >=2)]
#affordable and apartment
deduplicatedDataset[(deduplicatedDataset['currentAskingPrice'] < 132000) & (deduplicatedDataset['PropertyType'] =='Apartment')]


#price less than mortgage limit for 2 x average salary ( 75.4 x 3.5 = 264k)
deduplicatedDataset[(deduplicatedDataset['currentAskingPrice'] < 264000) ]
#affordable price and house and greater than 1 bed
deduplicatedDataset[(deduplicatedDataset['currentAskingPrice'] < 264000) & (deduplicatedDataset['PropertyType'] =='House')]

deduplicatedDataset[(deduplicatedDataset['currentAskingPrice'] < 264000) & (deduplicatedDataset['PropertyType'] =='House') & (deduplicatedDataset['beds'] >=2)]
#affordable and apartment
deduplicatedDataset[(deduplicatedDataset['currentAskingPrice'] < 264000) & (deduplicatedDataset['PropertyType'] =='Apartment') ]

deduplicatedDataset[(deduplicatedDataset['currentAskingPrice'] < 264000) & (deduplicatedDataset['PropertyType'] =='Apartment')]


#dublin only
#price less than mortgage limit for average salary ( 37500 x 3.5)
dublinOnly[(dublinOnly['currentAskingPrice'] < 132000) ].count()


#*****************************BOX PLOTS************************************************************
#box plots


dubOnly.boxplot(column='currentAskingPrice', by='CountyOrPostcode')

dubOnly['CountyOrPostcode'].count()

#gives individual boxplot with all step names
bp = dubOnly.boxplot(column='currentAskingPrice', by='CountyOrPostcode')
plt.xticks(rotation=90)
axes = plt.gca()
#axes.set_ylim([0,800])
plt.show()



groupedPostcodes = dubOnly.groupby('CountyOrPostcode')['CountyOrPostcode'].agg('count').sort_values()





plt.bar(groupedPostcodes.index,groupedPostcodes)
plt.xticks(rotation=90)
plt.show()




#*****************************SCATTER PLOTS************************************************************
x = deduplicatedDataset[(pd.notnull(deduplicatedDataset.currentAskingPrice))].sort_values(by=['currentAskingPrice'], ascending = False)['currentAskingPrice']
y = deduplicatedDataset[(pd.notnull(deduplicatedDataset.currentAskingPrice))].sort_values(by=['currentAskingPrice'], ascending = False)['size']

plt.xticks(rotation=90)
plt.scatter(x,y)
plt.show()
    

#*****************************MACHINE LEARNING************************************************************
#REMOVE BLANK ASKING PRICE
DS_CleanDependantVariable = deduplicatedDataset[deduplicatedDataset.currentAskingPrice.notnull()]

#reorder columns
DS_CleanDependantVariable = DS_CleanDependantVariable[[

 'beds',
 'bathrooms',
 'size',
 'ber lower',
 'CountyOrPostcode',
 'County',
 'PropertyType',
 'price bin',
  'currentAskingPrice']]

independent = DS_CleanDependantVariable.iloc[:, 0:7]
independent = DS_CleanDependantVariable.iloc[:, 0:7].values
dependent = DS_CleanDependantVariable.iloc[:, 8].values

from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder_X  = LabelEncoder()



#ber
berVariables = independent[:,3]
berVariables = labelencoder_X.fit_transform(berVariables[:])
onehotencoder = OneHotEncoder(categorical_features=[0])
berVariables = onehotencoder.fit_transform(berVariables.reshape(-1,1)).toarray()
#Avoid dummy variable trap
berVariables = berVariables[:,1:]

#countryOrPostcode
countryOrPostcodeVariables = independent[:,4]
countryOrPostcodeVariables = labelencoder_X.fit_transform(countryOrPostcodeVariables[:])
onehotencoder = OneHotEncoder(categorical_features=[0])
countryOrPostcodeVariables = onehotencoder.fit_transform(countryOrPostcodeVariables.reshape(-1,1)).toarray()
#Avoid dummy variable trap
countryOrPostcodeVariables = countryOrPostcodeVariables[:,1:]

#county
countyVariables = independent[:,5]
countyVariables = labelencoder_X.fit_transform(countyVariables[:])
onehotencoder = OneHotEncoder(categorical_features=[0])
countyVariables = onehotencoder.fit_transform(countyVariables.reshape(-1,1)).toarray()
#Avoid dummy variable trap
countyVariables = countyVariables[:,1:]

#PropertyType
PropertyTypeVariables = independent[:,6]
PropertyTypeVariables = labelencoder_X.fit_transform(PropertyTypeVariables[:])
onehotencoder = OneHotEncoder(categorical_features=[0])
PropertyTypeVariables = onehotencoder.fit_transform(PropertyTypeVariables.reshape(-1,1)).toarray()
#Avoid dummy variable trap
PropertyTypeVariables = PropertyTypeVariables[:,1:]

#concatenate all encoded categorical variable arrays
catVariables = np.concatenate((berVariables,countryOrPostcodeVariables),axis = 1)
catVariables = np.concatenate((catVariables,countyVariables),axis = 1)
catVariables = np.concatenate((catVariables,PropertyTypeVariables),axis = 1)


AllVariables = np.append(catVariables, independent[:,[0]], axis = 1)
AllVariables = np.append(AllVariables, independent[:,[1]], axis = 1)
AllVariables = np.append(AllVariables, independent[:,[2]], axis = 1)



#taken care of by the library


from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(AllVariables, dependent, test_size = 0.2, random_state = 0)



from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor(n_estimators = 10, random_state = 0)
regressor.fit(X_train, y_train)


y_pred = regressor.predict(X_test)

from sklearn.metrics import mean_squared_error
from math import sqrt

rms = sqrt(mean_squared_error(y_test, y_pred))
# = RMSE 583,206. very high, not accurate at all.


#----------------------------just dublin------------------------------------------

DS_CleanDependantVariable = deduplicatedDataset[deduplicatedDataset.currentAskingPrice.notnull()]
DS_CleanDependantVariable = DS_CleanDependantVariable[DS_CleanDependantVariable['County'] == 'dubin']
#reorder columns
DS_CleanDependantVariable = DS_CleanDependantVariable[[

 'beds',
 'bathrooms',
 'size',
 'ber lower',
 'CountyOrPostcode',
 'PropertyType',
 'price bin',
  'currentAskingPrice']]



independent = DS_CleanDependantVariable.iloc[:, 0:6]
independent = DS_CleanDependantVariable.iloc[:, 0:6].values
dependent = DS_CleanDependantVariable.iloc[:, 7].values

                                          
                                          
                                          


#ber
berVariables = independent[:,3]
berVariables = labelencoder_X.fit_transform(berVariables[:])
onehotencoder = OneHotEncoder(categorical_features=[0])
berVariables = onehotencoder.fit_transform(berVariables.reshape(-1,1)).toarray()
#Avoid dummy variable trap
berVariables = berVariables[:,1:]

#countryOrPostcode
countryOrPostcodeVariables = independent[:,4]
countryOrPostcodeVariables = labelencoder_X.fit_transform(countryOrPostcodeVariables[:])
onehotencoder = OneHotEncoder(categorical_features=[0])
countryOrPostcodeVariables = onehotencoder.fit_transform(countryOrPostcodeVariables.reshape(-1,1)).toarray()
#Avoid dummy variable trap
countryOrPostcodeVariables = countryOrPostcodeVariables[:,1:]



#PropertyType
PropertyTypeVariables = independent[:,5]
PropertyTypeVariables = labelencoder_X.fit_transform(PropertyTypeVariables[:])
onehotencoder = OneHotEncoder(categorical_features=[0])
PropertyTypeVariables = onehotencoder.fit_transform(PropertyTypeVariables.reshape(-1,1)).toarray()
#Avoid dummy variable trap
PropertyTypeVariables = PropertyTypeVariables[:,1:]

#concatenate all encoded categorical variable arrays
catVariables = np.concatenate((berVariables,countryOrPostcodeVariables),axis = 1)
catVariables = np.concatenate((catVariables,PropertyTypeVariables),axis = 1)


AllVariables = np.append(catVariables, independent[:,[0]], axis = 1)
AllVariables = np.append(AllVariables, independent[:,[1]], axis = 1)
AllVariables = np.append(AllVariables, independent[:,[2]], axis = 1)

AllVariables = AllVariables.astype(float)

#taken care of by the library


from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(AllVariables, dependent, test_size = 0.2, random_state = 0)



from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor(n_estimators = 10, random_state = 0)
regressor.fit(X_train, y_train)


y_pred = regressor.predict(X_test)

from sklearn.metrics import mean_squared_error
from math import sqrt

rms = sqrt(mean_squared_error(y_test, y_pred))
#344697 . very bad.



# backward elimination to see which variables to remove

import statsmodels.formula.api as sm

AllVariables = np.append(arr = np.ones((3294,1)).astype(int), values = AllVariables, axis = 1)

#X_opt will only contain optimal variables for the model. initialized with the index of all vaiables
X_opt = AllVariables[:, range(0,63)]


regressor_OLS = sm.OLS(endog = dependent, exog = X_opt).fit()

regressor_OLS.summary()


