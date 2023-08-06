from backtester.dataSource.data_source import DataSource
from backtester.dataSource.csv_data_source import CsvDataSource
from backtester.instrumentUpdates import *
import os
import pandas as pd
from datetime import datetime
import csv
import copy
from backtester.logger import *
from collections import OrderedDict
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class Problem1DataSource(DataSource):
    def __init__(self, cachedFolderName, dataSetId, instrumentIds, downloadUrl = None, targetVariable = '', featureList=[], timeKey = None, timeStringFormat = None, startDateStr=None, endDateStr=None, liveUpdates=True, pad=True):
        self._cachedFolderName = cachedFolderName
        self._dataSetId = dataSetId
        self._downloadUrl = downloadUrl
        self._targetVariable = targetVariable
        self._timeKey = timeKey
        self._timeStringFormat = timeStringFormat
        self.ensureDirectoryExists(self._cachedFolderName, self._dataSetId)
        self.ensureAllInstrumentsFile(dataSetId)
        self.featureList= featureList
        self.__features = featureList
        super(Problem1DataSource, self).__init__(cachedFolderName, dataSetId, instrumentIds, startDateStr, endDateStr)
        # print(self._instrumentIds)

    def getAllInstrumentUpdates(self, chunks=None):
        allInstrumentUpdates = {instrumentId : None for instrumentId in self._instrumentIds}
        timeUpdates = []
        for instrumentId in self._instrumentIds:
            print('Processing data for stock: %s' % (instrumentId))
            fileName = self.getFileName(instrumentId)
            if not self.downloadAndAdjustData(instrumentId, fileName):
                continue
            ### TODO: Assumes file is a csv, this is should not be in base class but ds type specific
            allInstrumentUpdates[instrumentId] = pd.read_csv(fileName, index_col=0, parse_dates=True)
            timeUpdates = allInstrumentUpdates[instrumentId].index.union(timeUpdates)
            allInstrumentUpdates[instrumentId].dropna(inplace=True)
            # NOTE: Assuming data is sorted by timeUpdates and all instruments have same columns
        timeUpdates = list(timeUpdates)
        return timeUpdates, allInstrumentUpdates


    def getAllInstrumentUpdatesDict(self):
        times, bookDataByInstrument = self.getAllInstrumentUpdates()
        return bookDataByInstrument

    def loadLiveUpdates(self):
        self._allTimes, self._groupedInstrumentUpdates = self.getGroupedInstrumentUpdates()

    def getInstrumentUpdateFromRow(self, instrumentId, row):
        bookData = row
        keys = list(bookData.keys())
        # print(keys)
        # print(self.featureList)
        for key in keys:
            # if key not in self.featureList:
            #     print(key)

            #     bookData.pop(key, None)
            #     print(bookData.keys())
            if is_number(bookData[key]):
                bookData[key] = float(bookData[key])
        timeKey = self._timeKey
        # import pdb; pdb.set_trace()
        timeOfUpdate = datetime.strptime(row[timeKey], self._timeStringFormat)
        print('Processing for: '+row[timeKey])
        bookData.pop(timeKey, None)
        # print(bookData.keys())

        inst = StockInstrumentUpdate(stockInstrumentId=instrumentId,
                                     tradeSymbol=instrumentId,
                                     timeOfUpdate=timeOfUpdate,
                                     bookData=bookData)

        if self._bookDataFeatureKeys is None:
            self._bookDataFeatureKeys = bookData.keys()  # just setting to the first one we encounter
            # print(self._bookDataFeatureKeys)
        return inst

    def getFileName(self, instrumentId):
        return self._cachedFolderName + self._dataSetId + '/' + instrumentId + '.csv'

    def ensureAllInstrumentsFile(self, dataSetId):
        return True

    def downloadFile(self, instrumentId, downloadLocation):
        url = ''
        if self._dataSetId != '':
            url = '%s/%s/%s.csv' % (self._downloadUrl, self._dataSetId, instrumentId)
        else:
            url = '%s/%s.csv' % (self._downloadUrl, instrumentId)

        print('Downloading from %s'%url)
        response = urlopen(url)
        status = response.getcode()
        if status == 200:
            print('Downloading %s data to file: %s' % (instrumentId, downloadLocation))
            with open(downloadLocation, 'w') as f:
                f.write(response.read().decode('utf8'))
            return True
        else:
            logError('File not found. Please check settings!')
            return False

    def downloadAndAdjustData(self, instrumentId, fileName):
        if not os.path.isfile(fileName):
            if not self.downloadFile(instrumentId, fileName):
                logError('Skipping %s:' % (instrumentId))
                return False
        return True

    def getBookDataFeatures(self):
        if (len(self.__features)>0):
            od = OrderedDict()
            for feature in self.__features:
                od[feature]=1
            od['A1']=1
            return od.keys()
        else:
            return super(self).getBookDataFeatures()

    def setFeatureList(self, features):
        self.__features = copy.deepcopy(features)
        print(self.__features)


if __name__ == "__main__":
    ds = Problem1DataSource(cachedFolderName='historicalData/',
                             dataSetId='p1',
                             instrumentIds=['A1'],
                             downloadUrl = 'https://qq-12-data.s3.us-east-2.amazonaws.com/A1.csv',
                             targetVariable = 'A1',
                             timeKey = 'Date',
                             timeStringFormat = '%Y-%m-%d',
                             startDateStr='1993-01-01',
                             endDateStr='2015-01-01',
                             liveUpdates=True,
                             pad=True)
    t = ds.emitAllInstrumentUpdates()
    ds.loadLiveUpdates()
    groupedInstrumentUpdates = ds.emitInstrumentUpdates()
    timeOfUpdate, instrumentUpdates = next(groupedInstrumentUpdates)
    # print(timeOfUpdate, instrumentUpdates[0].getBookData())
    while True:
        try:
            timeOfUpdate, instrumentUpdates = next(groupedInstrumentUpdates)
            # print(timeOfUpdate, instrumentUpdates[0].getBookData())
        except StopIteration:
            break
    # print(ds.getBookDataFeatures(), ds.getInstrumentIds())
