# -*- coding: utf-8 -*-

import requests
import json
from bs4 import BeautifulSoup

class GooglePlay:
    
    def __init__(self):
        pass
    
    def visitWebPage(self, urlPage):
        webInfo = requests.get(urlPage)
        return webInfo
    
    def getTitleOfApps(self, wC):
        titles = []
        appInfo = {}
        links = wC.find_all('a', {'class' : 'title'})
        numberOfApps = 10
        
        for x in range(0, numberOfApps):
            titles.append(links[x].get('title').encode('ascii', 'ignore'))
            appInfo[links[x].text.split()[0].replace('.', '')] = {'title':links[x].get('title').encode('ascii', 'ignore'), 'appLink':'https://play.google.com/'+links[x].get('href')}
        return (titles, appInfo)
        
    def getCompanies(self, aC):
        companies = aC.find_all('span', {'itemprop': 'name'})
        for a in companies:
            return str(a.text)
        
    def getGenre(self, aC):
        genres = aC.find_all('span', {'itemprop': 'genre'})
        for a in genres:
            return str(a.text)
    
    def getStarRating(self, aC):
        starRating = aC.find_all('div', {'class': 'score'})
        for a in starRating:
            return str(a.text)
    
    def getNumOfReviewers(self, aC):
        numOfReviews = aC.find_all('span', {'class': 'reviews-num'})
        for a in numOfReviews:
            return str(a.text)
    
    #screen scraping description is not used, immplement to use
    def getDescription(self, aC): 
        def getNumOfReviewers(self, aC):
            appDesc = aC.find_all('div', {'class': 'id-app-orig-desc'})
            for a in appDesc:
                return str(a.text)
    
    #this only gets 40 reviews at most per app
    def getReviews(self, aC):
        reviewDict = {}      
        reviewInfo = {}        
        counter = 0
            
        singleReviews = aC.findAll('div', {'class': 'single-review'})
        for eachReview in singleReviews:
            reviewInfo['user'] = eachReview.find('span', {'class': 'author-name'}).text
            reviewInfo['date'] = eachReview.find('span', {'class': 'review-date'}).text
            reviewInfo['rating'] = eachReview.find('div', {'class': 'tiny-star star-rating-non-editable-container'})['aria-label']
            reviewInfo['title'] = eachReview.find('span', {'class': 'review-title'}).text
            reviewInfo['comment'] = eachReview.find('span', {'class': 'review-title'}).next_sibling
            reviewDict['review_'+str(counter)] = reviewInfo
            reviewInfo = {}
            counter += 1
        counter = 0
        return reviewDict
    
    def getLastUpdated(self, aC):
        lastUpdated = aC.find_all('div', {'itemprop': 'datePublished'})
        for a in lastUpdated:
            return str(a.text)
        
    def getNumOfInstalls(self, aC):
        numDownloads = aC.find_all('div', {'itemprop': 'numDownloads'})
        for a in numDownloads:
            return str(a.text)
        
    def getAndrOSReq(self, aC):
        AndroidReq = aC.find_all('div', {'itemprop': 'operatingSystems'})
        for a in AndroidReq:
            return str(a.text)
            
    def getContentRating(self, aC):
        contentRating = aC.find_all('div', {'itemprop': 'contentRating'})
        for a in contentRating:
            return str(a.text)
            
    def getInAppPurch(self, aC):
        inAppPurch = aC.find_all('div', {'class': 'inapp-msg'})
        for a in inAppPurch:
            return str(a.text)
    
    def getAppInfo(self, appKey, appURL, allAppInfo):
        appContent = self.visitWebPage(appURL)
        aC = BeautifulSoup(appContent.content)  
        
        allAppInfo[appKey]['company'] = self.getCompanies(aC)
        allAppInfo[appKey]['genre'] = self.getGenre(aC)
        allAppInfo[appKey]['starRating'] = self.getStarRating(aC)
        allAppInfo[appKey]['numOfReviewers'] = self.getNumOfReviewers(aC)
        allAppInfo[appKey]['lastUpdated'] = self.getLastUpdated(aC)
        allAppInfo[appKey]['numOfInstalls'] = self.getNumOfInstalls(aC)
        allAppInfo[appKey]['androidOSReq'] = self.getAndrOSReq(aC)
        allAppInfo[appKey]['contentRating'] = self.getContentRating(aC)
        allAppInfo[appKey]['inAppPurchases'] = self.getInAppPurch(aC)
        allAppInfo[appKey]['reviews'] = self.getReviews(aC)
        return allAppInfo
        
    #implement to print results
    def printToJson(self, gpDict):
        with open('gp.txt', 'w') as outfile:
            json.dump(gpDict, outfile)
            
    #main controller
    def getGPInfo(self):
        #this is a link to the top free android apps on Google Play
        urlPage = 'https://play.google.com/store/apps/collection/topselling_free?hl=en'
        webContent = self.visitWebPage(urlPage)
        wC = BeautifulSoup(webContent.content)
        
        allAppInfo = {}
        topApps = {}
        
        titles = self.getTitleOfApps(wC)
        

        allAppInfo = titles[1]
        
        #loops through all the apps to get app Info
        for appKey in allAppInfo.keys():
            allAppInfo = self.getAppInfo(appKey, allAppInfo[appKey]['appLink'], allAppInfo)
    
        topApps['googlePlay'] = allAppInfo
        return topApps