from backtester.trading_system_parameters import TradingSystemParameters
from backtester.features.feature import Feature
from datetime import timedelta
from sklearn.ensemble import RandomForestRegressor
from london_summer_challenge_toolbox.problem1_data_source import Problem1DataSource
from london_summer_challenge_toolbox.problem1_execution_system import Problem1ExecutionSystem
from backtester.timeRule.custom_time_rule import CustomTimeRule
from backtester.orderPlacer.backtesting_order_placer import BacktestingOrderPlacer
from backtester.trading_system import TradingSystem
from backtester.version import updateCheck
from backtester.constants import *
from backtester.features.feature import Feature
from backtester.logger import *
import pandas as pd
import numpy as np
from london_summer_challenge_toolbox.problem1_time_rule import DayTimeRule
import sys
from sklearn import linear_model
import copy
from sklearn import metrics as sm


## Make your changes to the functions below.
## SPECIFY the symbols you are modeling for in getSymbolsToTrade() below
## You need to specify features you want to use in getInstrumentFeatureConfigDicts() and getMarketFeatureConfigDicts()
## and create your predictions using these features in getPrediction()

## Don't change any other function
## The toolbox does the rest for you, from downloading and loading data to running backtest


class MyTradingParams(TradingSystemParameters):
    '''
    initialize class
    place any global variables here
    '''

    def __init__(self, tradingFunctions):
        self.__tradingFunctions = tradingFunctions
        self.__dataSetId = 'p1'
        self.__instrumentIds = ['A1']
        self.__targetVariable = 'A1'
        self.__priceKey = 'A1'
        self.__additionalInstrumentFeatureConfigDicts = []
        self.__additionalMarketFeatureConfigDicts = []
        self.__fees = {'brokerage': 0.00, 'spread': 0.00}
        self.__startDate = '1993/01/01'
        self.__endDate = '2016/01/01'
        self.__lookbackSize = 360
        self.__dataParser = None
        self.__featureKeys = []
        self.__maxFeatureLength = 5000
        self.__model = {}
        self.__params = self.__tradingFunctions.params
        self.trainModel()

        self.updateFrequency = 1
        self.burnData = 60
        self.predictionLogFile = open('predictions.csv', 'a')
        self.headerNotSet = True
        super(MyTradingParams, self).__init__()

    '''
    Returns an instance of class DataParser. Source of data for instruments
    '''

    def initDataParser(self):
        ds = Problem1DataSource(cachedFolderName='historicalData/',
                                dataSetId=self.__dataSetId,
                                instrumentIds=self.__instrumentIds,
                                downloadUrl='https://qq-12-data.s3.us-east-2.amazonaws.com',
                                targetVariable=self.__targetVariable,
                                featureList=self.__featureKeys,
                                timeKey='Date',
                                timeStringFormat='%Y-%m-%d',
                                startDateStr=self.__startDate,
                                endDateStr=self.__endDate,
                                liveUpdates=True,
                                pad=True)
        return ds

    def setDataParser(self):
        self.__dataParser = self.initDataParser()
        return self.__dataParser

    def getDataParser(self):
        # instrumentIds = ['trainingData']
        ds = self.setDataParser()
        ds.loadLiveUpdates()
        return ds

    '''
    Returns an instance of class TimeRule, which describes the times at which
    we should update all the features and try to execute any trades based on
    execution logic.
    For eg, for intra day data, you might have a system, where you get data
    from exchange at a very fast rate (ie multiple times every second). However,
    you might want to run your logic of computing features or running your execution
    system, only at some fixed intervals (like once every 5 seconds). This depends on your
    strategy whether its a high, medium, low frequency trading strategy. Also, performance
    is another concern. if your execution system and features computation are taking
    a lot of time, you realistically wont be able to keep upto pace.
    '''

    def getTimeRuleForUpdates(self):
        return DayTimeRule(startDate=self.__startDate, endDate=self.__endDate, frequency='Mo', sample='1',
                           startTime='00:00', endTime='17:00')

    '''
    Returns a timedetla object to indicate frequency of updates to features
    Any updates within this frequncy to instruments do not trigger feature updates.
    Consequently any trading decisions that need to take place happen with the same
    frequency
    '''

    def getFrequencyOfFeatureUpdates(self):
        return timedelta(60, 0)  # minutes, seconds

    def getStartingCapital(self):
        return 100 * len(self.__instrumentIds)

    def getPrediction(self, time, updateNum, instrumentManager):

        val = None
        predictions = pd.Series(val, index=instrumentManager.getAllInstrumentsByInstrumentId())

        # holder for all the instrument features for all instruments
        lookbackInstrumentFeatures = instrumentManager.getLookbackInstrumentFeatures()
        # holder for all the market features
        lookbackMarketFeatures = instrumentManager.getDataDf()

        # if you don't enough data yet, don't make a prediction

        if updateNum <= self.burnData * self.updateFrequency:
            return predictions

        # Once you have enough data, start making predictions

        # Loading the target Variable
        Y = lookbackInstrumentFeatures.getFeatureDf(self.getTargetVariableKey())

        # Creating an array to load and hold all features

        X = []  # 2D array timestamp x featureNames
        x_star = []  # 1D array Data point at time t (whose Value will be predicted) featureKeys

        for f in self.__featureKeys:  # Looping over all features

            data = lookbackInstrumentFeatures.getFeatureDf(f).fillna(0)
            X.append(data.values.T[0])

            x_star.append(np.array(data.iloc[-1]))

        X = np.nan_to_num(np.column_stack(X))  # shape = featureKeys x timestamp
        x_star = np.nan_to_num(np.column_stack(x_star))  # shape = featureKeys
        # Now looping over all stocks:
        ids = self.__instrumentIds

        # import pdb;pdb.set_trace()
        for i in range(len(ids)):
            s = ids[i]

            y_s = Y.values

            x_train = np.array(X)[:-1]
            x_star = np.array(x_star)  # shape = timestamps x numFeatures
            y_train = np.array(y_s)[:-1].astype(float).reshape(-1)  # shape = timestamps x 1

            mapped_x_train = self.__tradingFunctions.mapFeatures(x_train, y_train)

            self.trainModel(mapped_x_train, y_train)

            #####################################
            ####    Making Predictions      #####
            #####################################

            # make your prediction using your model
            # first verify none of the features are nan or inf
            # import pdb;#pdb.set_trace()
            if np.isnan(x_star).any():
                print('Data contains nan or inf, predicting 0')
                y_predict = val
            else:
                try:
                    x_star_mapped = self.__tradingFunctions.mapRow(x_star)
                    y_predict = self.__model[s].predict(x_star_mapped.reshape(1, -1))

                except Exception as e:
                    print(e)
                    y_predict = [[0]]

            predictions[s] = y_predict[0]  # [0]
            print('prediction for %s %s :%.3f' % (s, self.__targetVariable, y_predict[0]))

        self.logPredictions(time, predictions)

        return predictions

    def trainModel(self, df=None, y=None):
        TF_class = self.__tradingFunctions
        if df is None:
            if self.__dataParser is None:
                self.__dataParser = self.initDataParser()
            dataDict = self.__dataParser.getAllInstrumentUpdatesDict()

            df = dataDict[self.__instrumentIds[0]]

            if len(self.__featureKeys) == 0:
                self.__featureKeys = TF_class.pickFeatures(df, self.getTargetVariableKey())
                feature_list = copy.deepcopy(self.__featureKeys)
                feature_list = np.append(feature_list, [self.getTargetVariableKey()])
                self.__dataParser.setFeatureList(feature_list)
            if (len(self.__featureKeys) > self.__maxFeatureLength):
                print("Number of picked features should be less than %s, quitting now !!" % self.__maxFeatureLength)
                quit()
            features = self.__featureKeys
            corr_array = []
            targetKey = self.getTargetVariableKey()
            for feature in features:
                series_corr = list()
                series_corr.append(abs(df[feature].corr(df[targetKey], method="spearman")))
                series_corr.append(abs(df[feature].diff().corr(df[targetKey], method="spearman")))
                series_corr.append(abs(df[feature].rolling(window=3).mean().corr(df[targetKey], method="spearman")))
                corr = max(series_corr)
                corr_array.append(corr)
            self.setScore(np.mean(np.nan_to_num(corr_array)))
        if y is None:
            y = df[self.getTargetVariableKey()]
            df = df.drop([self.getTargetVariableKey()], axis=1)
            df = df[self.__featureKeys]

        for id in self.__instrumentIds:
            # clf = linear_model.Lasso(alpha=0.5)
            clf = RandomForestRegressor(n_estimators=500, max_depth=8, random_state=0)
            clf.fit(df, y)
            self.__model[id] = clf
            # y_predict=clf.predict(df)
            # self.__score=sm.mean_squared_error(y,y_predict)

    def getMetrics(self):
        return {'score': self.__score}

    def setScore(self, score):
        self.__score = score

    '''


    This is a way to use any custom features you might have made.
    Returns a dictionary where
    key: featureId to access this feature (Make sure this doesnt conflict with any of the pre defined feature Ids)
    value: Your custom Class which computes this feature. The class should be an instance of Feature
    Eg. if your custom class is MyCustomFeature, and you want to access this via featureId='my_custom_feature',
    you will import that class, and return this function as {'my_custom_feature': MyCustomFeature}
    '''

    def getCustomFeatures(self):
        customFeatures = {'ScoreCalculator': ScoreCalculator,
                          'prediction': TrainingPredictionFeature}
        try:
            customFeatures.update(self.__tradingFunctions.getCustomFeatures())
            return customFeatures
        except AttributeError:
            return customFeatures

    def getInstrumentFeatureConfigDicts(self):
        # ADD RELEVANT FEATURES HERE

        newFeatureList = []

        # maDict = {'featureKey': 'ma6',
        #                         'featureId': 'moving_average',
        #                          'params': {'period': 6, 'featureName': self.__featureKeys[1]}}

        # newFeatureList += [maDict['featureKey']]

        predictionDict = {'featureKey': 'prediction',
                          'featureId': 'prediction',
                          'params': {'tsParams': self}}
        scoreDict = {'featureKey': 'score',
                     'featureId': 'ScoreCalculator',
                     'params': {'predictionKey': 'prediction',
                                'targetVariable': self.getTargetVariableKey(),
                                'burn': self.getBurn}}

        # self.setFeatureKeys(self.getFeatureKeys()+newFeatureList)

        # stockFeatureConfigs = self.__tradingFunctions.getInstrumentFeatureConfigDicts()
        #
        #
        return {INSTRUMENT_TYPE_STOCK:
                # stockFeatureConfigs +
                    [predictionDict, scoreDict] + self.__additionalInstrumentFeatureConfigDicts}

    '''
    Returns an array of market feature config dictionaries
        market feature config Dictionary has the following keys:
        featureId: a string representing the type of feature you want to use
        featureKey: a string representing the key you will use to access the value of this feature.this
        params: A dictionary with which contains other optional params if needed by the feature
    '''

    def getMarketFeatureConfigDicts(self):
        # ADD RELEVANT FEATURES HERE
        scoreDict = {'featureKey': 'score',
                     'featureId': 'score_ll',
                     'params': {'featureName': self.getPriceFeatureKey(),
                                'instrument_score_feature': 'score'}}

        # marketFeatureConfigs = self.__tradingFunctions.getMarketFeatureConfigDicts()
        return [scoreDict] + self.__additionalMarketFeatureConfigDicts  # + marketFeatureConfigs

    '''
    Returns the type of execution system we want to use. Its an implementation of the class ExecutionSystem
    It converts prediction to intended positions for different instruments.
    '''

    def getExecutionSystem(self):
        return Problem1ExecutionSystem(enter_threshold=0.7,
                                       exit_threshold=0.55,
                                       longLimit=1,
                                       shortLimit=1,
                                       capitalUsageLimit=0.10 * self.getStartingCapital(),
                                       enterlotSize=1, exitlotSize=1,
                                       limitType='L', price=self.__priceKey)

    '''
    Returns the type of order placer we want to use. its an implementation of the class OrderPlacer.
    It helps place an order, and also read confirmations of orders being placed.
    For Backtesting, you can just use the BacktestingOrderPlacer, which places the order which you want, and automatically confirms it too.
    '''

    def getOrderPlacer(self):
        return BacktestingOrderPlacer()

    '''
    Returns the amount of lookback data you want for your calculations. The historical market features and instrument features are only
    stored upto this amount.
    This number is the number of times we have updated our features.
    '''

    def getLookbackSize(self):
        return max(150, self.__lookbackSize)

    def getPriceFeatureKey(self):
        return self.__priceKey

    def setPriceFeatureKey(self, priceKey='Adj_Close'):
        self.__priceKey = priceKey

    def getDataSetId(self):
        return self.__dataSetId

    def setDataSetId(self, dataSetId):
        self.__dataSetId = dataSetId

    def getInstrumentsIds(self):
        return self.__instrumentIds

    def setInstrumentsIds(self, instrumentIds):
        self.__instrumentIds = instrumentIds

    def getDates(self):
        return {'startDate': self.__startDate,
                'endDate': self.__endDate}

    def setDates(self, dateDict):
        self.__startDate = dateDict['startDate']
        self.__endDate = dateDict['endDate']

    def getTargetVariableKey(self):
        return self.__targetVariable

    def setTargetVariableKey(self, targetVariable):
        self.__targetVariable = targetVariable

    def setFees(self, feeDict={'brokerage': 0.00, 'spread': 0.00}):
        self.__fees = feeDict

    def setAdditionalInstrumentFeatureConfigDicts(self, dicts=[]):
        self.__additionalInstrumentFeatureConfigDicts = dicts

    def setAdditionalMarketFeatureConfigDicts(self, dicts=[]):
        self.__additionalMarketFeatureConfigDicts = dicts

    def getFeatureKeys(self):
        return self.__featureKeys

    def setFeatureKeys(self, featureList):
        self.__featureKeys = featureList

    def getBurn(self):
        return self.burnData

    def setBurn(self, burn=240):
        self.burnData = burn

    def setPredictionLogFile(self, logFileName):
        self.predictionLogFile = open(logFileName, 'a')

    def logPredictions(self, time, predictions):
        if (self.predictionLogFile != None):
            if (self.headerNotSet):
                header = 'datetime'
                for index in predictions.index:
                    header = header + ',' + index
                self.predictionLogFile.write(header + '\n')
                self.headerNotSet = False

            lineData = str(time)

            for prediction in predictions.get_values():
                lineData = lineData + ',' + str(prediction)

            self.predictionLogFile.write(lineData + '\n')


class TrainingPredictionFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        t = featureParams['tsParams']
        return t.getPrediction(time, updateNum, instrumentManager)


class ScoreCalculator(Feature):
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        ids = list(instrumentManager.getAllInstrumentsByInstrumentId())
        burn = featureParams['burn']()

        predictionData = instrumentLookbackData.getFeatureDf(featureParams['predictionKey']).iloc[-1]
        if updateNum <= burn or (predictionData.values[0] is None):
            return pd.Series(0, index=ids)
        trueValue = instrumentLookbackData.getFeatureDf(featureParams['targetVariable']).iloc[-1]

        previousValue = instrumentLookbackData.getFeatureDf(featureKey).iloc[-1]
        currentScore = pd.Series(0.5, index=previousValue.index)
        # yp = 1-predictionData.values[0]
        # yp = 0.001 if yp<0.001 else yp
        # yp = 0.999 if yp>0.999 else yp
        currentScore[predictionData != 0.5] = np.power((trueValue.values[0] - predictionData.values[0]), 2)
        score = (previousValue * (updateNum - 1 - burn) + currentScore) / (
                    updateNum - burn)  # sm.accuracy_score(predictionData, trueValue)
        print('True Value: %.4f' % trueValue.values[0])
        print('MSE: %.4f' % score.values[0])
        return score


class AccuracyCalculator(Feature):
    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        ids = list(instrumentManager.getAllInstrumentsByInstrumentId())
        if updateNum < 2:
            return pd.Series(0, index=ids)

        predictionData = instrumentLookbackData.getFeatureDf(featureParams['predictionKey']).iloc[-1]
        trueValue = instrumentLookbackData.getFeatureDf(featureParams['targetVariable']).iloc[-1]

        predictedValue = 0 if ((1 - predictionData.values[0]) < featureParams['threshold']) else 1

        previousValue = instrumentLookbackData.getFeatureDf(featureKey).iloc[-1]
        currentScore = pd.Series(0, index=previousValue.index)
        currentScore[predictionData != 0.5] = currentScore + (1 - np.abs(predictedValue - trueValue))
        score = (previousValue * (
                    updateNum - 1) + currentScore) / updateNum  # sm.accuracy_score(predictionData, trueValue)
        print('Accuracy: %.2f' % score.values[0])
        return score


