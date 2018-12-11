


#analysis

#******************************************************************************
#***************************run 1. Munging.py first ***************************
#******************************************************************************
deduplicatedDataset = deduplicatedDataset[deduplicatedDataset['currentAskingPrice'] <= 2000000]
dublinOnly = deduplicatedDataset[(deduplicatedDataset.CountyOrPostcode.str.contains('dublin') ) & (pd.notnull(deduplicatedDataset.currentAskingPrice)) & (deduplicatedDataset['price bin'] <= 2000000) ]
everywhereExceptDublin = deduplicatedDataset[ (np.isnan(deduplicatedDataset['currentAskingPrice']) == False) & ~(deduplicatedDataset.CountyOrPostcode.str.contains('dublin')) & (deduplicatedDataset['price bin'] <= 2000000)]


#*********************************************CENTRAL TENDANCY MEASURES**********************************
#Average Country Wide Asking Price.
totalCountryMean = deduplicatedDataset['currentAskingPrice'].mean()
#Median Country Wide Asking Price.
totalCountryMedian = deduplicatedDataset['currentAskingPrice'].median()
#Mode Country Wide Asking Price
totalCountryMode = deduplicatedDataset['price bin'].mode()[0]

#central tendency for everywhere except dub
outsideDublinMean = everywhereExceptDublin['currentAskingPrice'].mean()
outsideDublinMedian = everywhereExceptDublin['currentAskingPrice'].median()
outsideDublinMode = everywhereExceptDublin['price bin'].mode()[0]

#central tendancy for dub only
dublinOnlyMean = dublinOnly['currentAskingPrice'].mean()
dublinOnlyMedian = dublinOnly['currentAskingPrice'].median()
dublinOnlyMode = dublinOnly['price bin'].mode()[0]

d = {
'mean' : pd.Series([totalCountryMean, outsideDublinMean, dublinOnlyMean], index=['Total Country', 'Outside Dublin', 'Dublin Only']),
'median' : pd.Series([totalCountryMedian, outsideDublinMedian, dublinOnlyMedian], index=['Total Country', 'Outside Dublin', 'Dublin Only']),
'mode(binned)' : pd.Series([totalCountryMode, outsideDublinMode, dublinOnlyMode], index=['Total Country', 'Outside Dublin', 'Dublin Only'])

}

summaryDF = pd.DataFrame(d)

codub = deduplicatedDataset[deduplicatedDataset['CountyOrPostcode'] =='dublin']
summaryDF.to_csv('C:\Temp\output.csv')

#Import this into PowerBI




#************************************Properties available at average salaries
#single average earner, FTB

#Everywher except Dublin
#price less than mortgage limit for average salary ( 37500 x 3.5)
(len(everywhereExceptDublin[(everywhereExceptDublin['currentAskingPrice'] < 147400) ]) / len(everywhereExceptDublin)) * 100
#affordable price and house and greater than 1 bed
everywhereExceptDublin[(everywhereExceptDublin['currentAskingPrice'] < 147400) & (deduplicatedDataset['PropertyType'] =='House') & (deduplicatedDataset['beds'] >=2)]
#affordable and apartment
everywhereExceptDublin[(everywhereExceptDublin['currentAskingPrice'] < 147400) & (deduplicatedDataset['PropertyType'] =='Apartment')]





#dublin only
dublinOnly.count()#3217
dublinOnly[dublinOnly['currentAskingPrice'] <=142500].count()#699
(dublinOnly[dublinOnly['currentAskingPrice'] <=142500].count()/ dublinOnly.count())*100
          


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

minPrice = min(deduplicatedDataset[deduplicatedDataset['price bin'] <= 2000000]['price bin'])
maxPrice = max(deduplicatedDataset[deduplicatedDataset['price bin'] <= 2000000]['price bin'])


plt.hist(deduplicatedDataset[deduplicatedDataset['price bin'] < 2000000]['price bin'], b, color = 'red', label = 'Full Country')   
plt.hist(everywhereExceptDublin[everywhereExceptDublin['price bin'] < 2000000]['price bin'], b, color = 'green', label = 'Outside Dublin') 
plt.hist(dublinOnly[dublinOnly['price bin'] < 2000000]['price bin'], b, color = 'blue', label = 'Dublin Only')     
plt.xticks(rotation=90)
plt.grid(zorder=0)
plt.xticks(np.arange(0, maxPrice + 50000, 40000))
plt.yticks(np.arange(0, 1100, 100))
plt.legend(['All Ireland', 'Outside Dublin', 'Dublin Only'])
plt.show()








#Everywher except Dublin
#price less than mortgage limit for average salary ( 37500 x 3.5)
(len(everywhereExceptDublin[(everywhereExceptDublin['currentAskingPrice'] < 147400) ]) / len(everywhereExceptDublin)) * 100
#affordable price and house and greater than 1 bed
everywhereExceptDublin[(everywhereExceptDublin['currentAskingPrice'] < 147400) & (deduplicatedDataset['PropertyType'] =='House') & (deduplicatedDataset['beds'] >=2)]
#affordable and apartment
everywhereExceptDublin[(everywhereExceptDublin['currentAskingPrice'] < 147400) & (deduplicatedDataset['PropertyType'] =='Apartment')]


#price less than mortgage limit for 2 x average salary ( 75.4 x 3.5 = 264k)
everywhereExceptDublin[(everywhereExceptDublin['currentAskingPrice'] < 294000) ]
#affordable price and house and greater than 1 bed
everywhereExceptDublin[(everywhereExceptDublin['currentAskingPrice'] < 294000) & (deduplicatedDataset['PropertyType'] =='House')]

everywhereExceptDublin[(everywhereExceptDublin['currentAskingPrice'] < 294000) & (deduplicatedDataset['PropertyType'] =='House') & (deduplicatedDataset['beds'] >=2)]
#affordable and apartment
everywhereExceptDublin[(everywhereExceptDublin['currentAskingPrice'] < 294000) & (deduplicatedDataset['PropertyType'] =='Apartment') ]

everywhereExceptDublin[(everywhereExceptDublin['currentAskingPrice'] < 294000) & (deduplicatedDataset['PropertyType'] =='Apartment')]


#dublin only
#price less than mortgage limit for average salary ( 37500 x 3.5)
(len(dublinOnly[(dublinOnly['currentAskingPrice'] < 147400) ])/ len(dublinOnly) )*100


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