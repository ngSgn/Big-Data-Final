from pytrends.request import TrendReq
import pandas as pd
import statistics
import time
import json

def GetKeywordsTrend(keywordsList,timeFrame,pytrend):
    pytrend.build_payload(keywordsList, cat=47, timeframe=timeFrame, geo='', gprop='')
    interest_over_time_df = pytrend.interest_over_time()
    return interest_over_time_df

def FindTarget(pList,start):
    for i in range(start,len(pList)):
        for j in range(len(pList[i]['data'])):
            if(pList[i]['data'][j] == 100):
                return {"x":i,"y":j}

def mean_sort(t):
    return t['mean']

def GetTrendsData(carNames,timeFrame):
    pytrend = TrendReq()
    keywordList = []
    pList=[]
    targetXY = {"x":0,"y":0}
    endWord = carNames[len(carNames)-1]
    for keyword in carNames:
        keywordList.append(keyword)
        if(len(keywordList) == 5 or keyword==endWord):
            newTarget = False
            tempDF = GetKeywordsTrend(keywordList,timeFrame,pytrend)
            if(len(pList) == 0):
                newTarget = True
                pList.append({"carName":keywordList[0],"data":tempDF[keywordList[0]].tolist(),"mean":0})
            else:
                tempList = tempDF[keywordList[0]].tolist()
                if(tempList[targetXY['y']] != 100): # check if 100 is still 100, if not change all pList
                    newTarget = True
                    if(100 in tempList):
                        pList[i]['data'] = tempList
                    else:
                        tempP = tempList[targetXY['y']]/100
                        for i in range(len(pList)):
                            for j in range(len(pList[i]['data'])):
                                pList[i]['data'][j] =pList[i]['data'][j]*tempP
            
            for i in range (1,len(keywordList)): # Push all data into pList
                pList.append({"carName":keywordList[i],"data":tempDF[keywordList[i]].tolist(),"mean":0})

            if(newTarget):
                targetXY = FindTarget(pList,targetXY['x'])# Find the position of 100
            # Clean up keywordList, append the top of pList to keywordList
            keywordList = []
            keywordList.append(pList[targetXY['x']]['carName'])
            
    
    for i in range (len(pList)): # Cal the new mean of all pList
        pList[i]['mean'] = statistics.mean(pList[i]['data'])
    pList.sort(key = mean_sort,reverse = True)# Sort pList by mean 
    return pList
    

