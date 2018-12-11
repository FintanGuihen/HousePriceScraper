

#**************************************************************************************
#seperate data into Dublin & OutsideDublin
#**************************************************************************************
websiteDublinOnly = HousingWebsiteData[(HousingWebsiteData.CountyOrPostcode.str.contains('dublin')==True ) ]
websiteEverywhereExceptDublin = HousingWebsiteData[(HousingWebsiteData.CountyOrPostcode.str.contains('dublin')==False)]

HousingWebsiteData[HousingWebsiteData['currentAskingPrice'] <= 2000000].to_csv('C:\Temp\FullDataset.csv')

FTB_Ind = 147100
FTB_Joint = 294100
STB_Ind = 160400
STB_Joint = 320800


#**************************************************************************************
#Histograms
#**************************************************************************************

b = np.arange(0,2000000, 20000)
minPrice = min(HousingWebsiteData[HousingWebsiteData['price bin'] <= 5000000]['price bin'])
maxPrice = max(HousingWebsiteData['price bin'])


#****************************************************************
#Price & availability comparison InDublin vs OutsideDublin
plt.hist(HousingWebsiteData['price bin'], b, color = 'red', label = 'Full Country')   
plt.hist(everywhereExceptDublin['price bin'], b, color = 'green', label = 'Outside Dublin') 
plt.hist(dublinOnly['price bin'], b, color = 'blue', label = 'Dublin Only')     
plt.xticks(rotation=90)
plt.grid(zorder=0)
plt.xticks(np.arange(0, 2000000, 40000))
#plt.yticks(np.arange(0, 1100, 100))
plt.legend(['All Ireland', 'Outside Dublin', 'Dublin Only'])
plt.show()



#**************************************************************************************
#Availability Statistics
#**************************************************************************************

#****************************************************************
#create dataframe
BuyerStats = pd.DataFrame( index=['FTB Individual', 'FTB Joint', 'STB Individual', 'STB Joint'], columns=['In Dublin Count','In Dublin %','Outside Dublin Count','Outside Dublin %'])

#****************************************************************
#populate dataframe - Outaide Dublin

#FTB individual
BuyerStats.at['FTB Individual','Outside Dublin Count'] = len(websiteEverywhereExceptDublin[websiteEverywhereExceptDublin['currentAskingPrice'] <= FTB_Ind])
BuyerStats.at['FTB Individual','Outside Dublin %'] = (len(websiteEverywhereExceptDublin[websiteEverywhereExceptDublin['currentAskingPrice'] < FTB_Ind]) / len(HousingWebsiteData['currentAskingPrice']) )*100

#FTB Joint
BuyerStats.at['FTB Joint','Outside Dublin Count'] = len(websiteEverywhereExceptDublin[websiteEverywhereExceptDublin['currentAskingPrice'] < FTB_Joint])
BuyerStats.at['FTB Joint','Outside Dublin %'] = (len(websiteEverywhereExceptDublin[websiteEverywhereExceptDublin['currentAskingPrice'] < FTB_Joint]) / len(HousingWebsiteData['currentAskingPrice']) )*100

#STB individual
BuyerStats.at['STB Individual','Outside Dublin Count'] = len(websiteEverywhereExceptDublin[websiteEverywhereExceptDublin['currentAskingPrice'] < STB_Ind])
BuyerStats.at['STB Individual','Outside Dublin %'] = (len(websiteEverywhereExceptDublin[websiteEverywhereExceptDublin['currentAskingPrice'] < STB_Ind]) / len(HousingWebsiteData['currentAskingPrice']) )*100

#STB Joint
BuyerStats.at['STB Joint','Outside Dublin Count'] =len( websiteEverywhereExceptDublin[websiteEverywhereExceptDublin['currentAskingPrice'] < STB_Joint])
BuyerStats.at['STB Joint','Outside Dublin %'] =(len(websiteEverywhereExceptDublin[websiteEverywhereExceptDublin['currentAskingPrice'] < STB_Joint]) / len(HousingWebsiteData['currentAskingPrice']) )*100

#****************************************************************
#populate dataframe - InDublin

#FTB individual
BuyerStats.at['FTB Individual','In Dublin Count'] = len(websiteDublinOnly[websiteDublinOnly['currentAskingPrice'] < FTB_Ind])
BuyerStats.at['FTB Individual','In Dublin %'] =(len(websiteDublinOnly[websiteDublinOnly['currentAskingPrice'] < FTB_Ind]) / len(HousingWebsiteData['currentAskingPrice']) )*100
#(len(websiteDublinOnly[websiteDublinOnly['currentAskingPrice'] < FTB_Ind]) / len(websiteDublinOnly['currentAskingPrice']) )*100

#FTB Joint
BuyerStats.at['FTB Joint','In Dublin Count'] =len( websiteDublinOnly[websiteDublinOnly['currentAskingPrice'] < FTB_Joint])
BuyerStats.at['FTB Joint','In Dublin %'] =(len(websiteDublinOnly[websiteDublinOnly['currentAskingPrice'] < FTB_Joint]) / len(HousingWebsiteData['currentAskingPrice']) )*100
#(len(websiteDublinOnly[websiteDublinOnly['currentAskingPrice'] < FTB_Joint]) / len(websiteDublinOnly['currentAskingPrice']) )*100

#STB individual
BuyerStats.at['STB Individual','In Dublin Count'] = len(websiteDublinOnly[websiteDublinOnly['currentAskingPrice'] < STB_Ind])
BuyerStats.at['STB Individual','In Dublin %'] = (len(websiteDublinOnly[websiteDublinOnly['currentAskingPrice'] < STB_Ind]) / len(HousingWebsiteData['currentAskingPrice']) )*100

#STB Joint
BuyerStats.at['STB Joint','In Dublin Count'] = len(websiteDublinOnly[websiteDublinOnly['currentAskingPrice'] < STB_Joint])
BuyerStats.at['STB Joint','In Dublin %'] = (len(websiteDublinOnly[websiteDublinOnly['currentAskingPrice'] < STB_Joint]) / len(HousingWebsiteData['currentAskingPrice']) )*100





#**************************************************************************************
#Central Tendancy.
#Get mean median and mode of data to build up a view of the distribution
#**************************************************************************************

#Average Country Wide Asking Price.
totalCountryMean = HousingWebsiteData['currentAskingPrice'].mean()
#Median Country Wide Asking Price.
totalCountryMedian = HousingWebsiteData['currentAskingPrice'].median()
#Mode Country Wide Asking Price
totalCountryMode = HousingWebsiteData['price bin'].mode()[0]

#central tendency for everywhere except dub
outsideDublinMean = websiteEverywhereExceptDublin['currentAskingPrice'].mean()
outsideDublinMedian = websiteEverywhereExceptDublin['currentAskingPrice'].median()
outsideDublinMode = websiteEverywhereExceptDublin['price bin'].mode()[0]

#central tendancy for dub only
dublinOnlyMean = websiteDublinOnly['currentAskingPrice'].mean()
dublinOnlyMedian = websiteDublinOnly['currentAskingPrice'].median()
dublinOnlyMode = websiteDublinOnly['price bin'].mode()[0]

#create dictionary
d = {
'mean' : pd.Series([totalCountryMean, outsideDublinMean, dublinOnlyMean], index=['Total Country', 'Outside Dublin', 'Dublin Only']),
'median' : pd.Series([totalCountryMedian, outsideDublinMedian, dublinOnlyMedian], index=['Total Country', 'Outside Dublin', 'Dublin Only']),
'mode(binned)' : pd.Series([totalCountryMode, outsideDublinMode, dublinOnlyMode], index=['Total Country', 'Outside Dublin', 'Dublin Only'])

}

#create dataframe from dictionary
summaryDF = pd.DataFrame(d)


#*************************************************************
#Output sumary to CSV
summaryDF.to_csv('C:\Temp\output.csv')



#**************************************************************************************
#Breakdown of property by room. get properties with more than 1 room available in and 
#outside dublin, within budget of FTB & STB
#Plot data on a bar chart
#**************************************************************************************
RoomBreakdown = pd.DataFrame( index=['FTB Individual', 'FTB Joint'], columns=['1 Room Dublin','1 Room Outside Dublin', '2+ Rooms Dublin', '2+ Rooms Outside Dublin'])


#get room counts for FTB outside Dublin
RoomBreakdown.at['FTB Individual','1 Room Outside Dublin'] = len(websiteEverywhereExceptDublin[(websiteEverywhereExceptDublin['currentAskingPrice'] < FTB_Ind) & (websiteEverywhereExceptDublin['beds'] <=1)])
RoomBreakdown.at['FTB Individual','2+ Rooms Outside Dublin'] = len(websiteEverywhereExceptDublin[(websiteEverywhereExceptDublin['currentAskingPrice'] < FTB_Ind) & (websiteEverywhereExceptDublin['beds'] >1)])

#get room counts for FTB in Dublin
RoomBreakdown.at['FTB Individual','1 Room Dublin'] = len(websiteDublinOnly[(websiteDublinOnly['currentAskingPrice'] < FTB_Ind) & (websiteDublinOnly['beds'] <=1)])
RoomBreakdown.at['FTB Individual','2+ Rooms Dublin'] = len(websiteDublinOnly[(websiteDublinOnly['currentAskingPrice'] < FTB_Ind) & (websiteDublinOnly['beds'] >1)])

#get roomcounts for FTB outside Dublin
RoomBreakdown.at['FTB Joint','1 Room Outside Dublin'] = len(websiteEverywhereExceptDublin[(websiteEverywhereExceptDublin['currentAskingPrice'] < FTB_Joint) & (websiteEverywhereExceptDublin['beds'] <=1)])
RoomBreakdown.at['FTB Joint','2+ Rooms Outside Dublin'] = len(websiteEverywhereExceptDublin[(websiteEverywhereExceptDublin['currentAskingPrice'] < FTB_Joint) & (websiteEverywhereExceptDublin['beds'] >1)])

#get roomcounts for FTB in  Dublin
RoomBreakdown.at['FTB Joint','1 Room Dublin'] = len(websiteDublinOnly[(websiteDublinOnly['currentAskingPrice'] < FTB_Joint) & (websiteDublinOnly['beds'] <=1)])
RoomBreakdown.at['FTB Joint','2+ Rooms Dublin'] = len(websiteDublinOnly[(websiteDublinOnly['currentAskingPrice'] < FTB_Joint) & (websiteDublinOnly['beds'] >1)])



RoomBreakdown.plot.bar()




#**************************************************************************************
#Box Plots. Used for analysis, not used in presentation
#**************************************************************************************

#boxplots for dublin postcodes
bp = websiteDublinOnly.boxplot(column='currentAskingPrice', by='CountyOrPostcode')
plt.xticks(rotation=90)
axes = plt.gca()
axes.set_ylim([0,2000000])
plt.suptitle('Price Distribution by Postcode')
plt.title('')
plt.axhline(y=147100,color='red')
plt.axhline(y=294100,color='green')

plt.show()

#boxplots for counties
bp = HousingWebsiteData.boxplot(column='currentAskingPrice', by='County')
plt.xticks(rotation=90)
axes = plt.gca()
axes.set_ylim([0,2000000])
plt.suptitle('Price Distribution by Postcode')
plt.title('')
plt.axhline(y=147100,color='red')
plt.axhline(y=294100,color='green')

plt.show()


#gives individual boxplot with all step names
bp = websiteDublinOnly[websiteDublinOnly['CountyOrPostcode']=='dublin 14'].boxplot(column='currentAskingPrice', by='CountyOrPostcode')
plt.xticks(rotation=90)
axes = plt.gca()
axes.set_ylim([0,2000000])
#plt.suptitle('Price Distribution by Postcode')
plt.title('')
#plt.axhline(y=147100,color='red')
#plt.axhline(y=294100,color='green')

plt.show()



#****************************************ROUGH WORK****************************

codub = HousingWebsiteData[HousingWebsiteData['CountyOrPostcode'] =='dublin']
summaryDF.to_csv('C:\Temp\output.csv')



HousingWebsiteData.to_csv('C:\Temp\AskingPrices.csv')
PropetyPriceRegisterData.to_csv('C:\Temp\PriceRegisterSellingPrices.csv')
