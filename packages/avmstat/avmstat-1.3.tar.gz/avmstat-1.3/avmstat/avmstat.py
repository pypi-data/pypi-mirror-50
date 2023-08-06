import pandas as pd
import numpy as np
import seaborn as sea

class pricePerformance:

    def __init__(self, URN, predictedPrice, confidence, actualPrice, modelName):

        self.urn = URN
        self.val = predictedPrice
        self.name = modelName
        self.fsd = confidence
        self.ref = actualPrice
        self.err = self.__error()
        self.absErr = self.__absError()
        self.perfB_stand = self.__performanceBand()
        self.fsdB_stand = self.__confidenceBand()

    #Error
    def __error(self):
        return ((self.val - self.ref)/self.ref)

    #Absolute Error
    def __absError(self):
        return abs(((self.val - self.ref)/self.ref))

    #FSD Bands
    def __confidenceBand(self):
        return pd.cut(self.fsd, [-1,0.1,0.15,0.20,0.30,1000], labels = ["0-10", "11-15", "16-20", "21-30", "30+"])

    #Performance Bands
    def __performanceBand(self):
        return pd.cut(self.absErr.values, [-1,0.1,0.15,0.20,0.30,1000], labels = ["0-10", "11-15", "16-20", "21-30", "30+"])

    def appendPerformance(self):
        df = pd.DataFrame()
        df['URN'] = self.urn
        df['predictedValue'] = self.val
        df['fsd'] = self.fsd
        df['comparePrice'] = self.ref
        df['error'] = self.err
        df['absoluteError'] = self.absErr
        df['performanceBands'] = self.perfB_stand
        df['fsdBand'] = self.fsdB_stand
        return df

    def pricePerformance(self):
        p = pd.DataFrame()
        f = pd.DataFrame()
        p['Performance#'] = self.absErr.groupby(self.perfB_stand).agg('count')
        p['Performance%'] = p['Performance#']/len(self.absErr)
        f['confidence#'] = self.absErr.groupby(self.fsdB_stand).agg('count')
        f['confidence%'] = f['confidence#']/len(self.fsd)

        perfStatTable = p.join(f, how = 'left')

        df_confPerfBands = pd.DataFrame({"Confidence" : self.fsdB_stand, "Performance" : self.perfB_stand})
        conf_by_perf = pd.crosstab(df_confPerfBands['Confidence'], df_confPerfBands['Performance'])
        rowPerc = pd.crosstab(df_confPerfBands.iloc[:,0], df_confPerfBands.iloc[:,1], normalize='index')
        colPerc = pd.crosstab(df_confPerfBands.iloc[:,0], df_confPerfBands.iloc[:,1], normalize='columns')
        totPerc = pd.crosstab(df_confPerfBands.iloc[:,0], df_confPerfBands.iloc[:,1], normalize='all')

        print('###########################################################################')
        print('PERFORMANCE STATATISTS FOR THE {} PRICE MODEL'.format(self.name))
        print('###########################################################################')
        print('')
        print('FSD and performance by band for the: {} avm'.format(self.name))
        print('')
        print(perfStatTable)
        print('')
        print('---------------------------------------------------------------------------')
        print('Fsd by performance band for {} price model'.format(self.name))
        print('#')
        print('')
        print(conf_by_perf)
        print('')
        print('---------------------------------------------------------------------------')
        print('Row Percentages%')
        print('')
        print(rowPerc)
        print('')
        print('---------------------------------------------------------------------------')
        print('Column Percentages%')
        print('')
        print(colPerc)
        print('')
        print('---------------------------------------------------------------------------')
        print('Total Percentages%')
        print('')
        print(totPerc)
        print('')

        return perfStatTable, conf_by_perf, df_confPerfBands

class priceCompare:

    def __init__(self, comparisonModels):
    #''' All inputs are objects of type pricePerformance class. comparionPrice can be an array of pricePerformance classes. comarisonPrices = ['pricePerformance1', 'pricePerformance2'] '''

        self.comparison = comparisonModels

    def comparePricePerformance(self):

        modelCompareList = list()
        for model in self.comparison:
            output = tuple(model.pricePerformance()) 
            modelCompareList.append(output)
        
        numModels = [x for x in range(len(self.comparison))]
        for i in numModels:
            for j in numModels:

                if (i == j):
                    continue

                else:
                    PerfConfBand = modelCompareList[i][0] - modelCompareList[j][0] 
                    ConfbyPerf = modelCompareList[i][1] - modelCompareList[j][1] 

                    print('###########################################################################')
                    print('PERFORMANCE COMPARISON OF {} AGAINST {} PRICE MODEL'.format(self.comparison[i].name, self.comparison[j].name))
                    print('###########################################################################')
                    print('')
                    print('Difference in performance: Model {} compared to {}'.format(self.comparison[i].name, self.comparison[j].name))
                    print('---------------------------------------------------------------------------')
                    print('Performance & confidence band comparison')
                    print('')
                    print(PerfConfBand)
                    print('')
                    print('---------------------------------------------------------------------------')
                    print('Confidence by performance band comparison')
                    print('')
                    print(ConfbyPerf)
                    print('')

                    df = modelCompareList[i][2].join(modelCompareList[j][2], how = 'left', lsuffix = self.comparison[i].name, rsuffix=self.comparison[j].name)
                    df['p1Num'] = df['Performance' + self.comparison[i].name].apply(lambda x: self.__numericCat(x))
                    df['p2Num'] = df['Performance' + self.comparison[j].name].apply(lambda x: self.__numericCat(x))

                    perfnum = pd.crosstab(df['Performance' + self.comparison[i].name], df['Performance' + self.comparison[j].name])
                    perfperc = pd.crosstab(df['Performance' + self.comparison[i].name], df['Performance' + self.comparison[j].name], normalize='all')

                    sumSame = df[df['Performance'+ self.comparison[i].name] == df['Performance' + self.comparison[j].name]]
                    sumHigh = df[df.p1Num < df.p2Num]
                    sumLow = df[df.p1Num > df.p2Num]


                    print('---------------------------------------------------------------------------')
                    print('{} by {} price performance matrix'.format(self.comparison[i].name, self.comparison[j].name))
                    print('---------------------------------------------------------------------------')
                    print('#')
                    print('')
                    print(perfnum)
                    print('')
                    print('---------------------------------------------------------------------------')
                    print('%')
                    print('')
                    print(perfperc)
                    print('')
                    print('---------------------------------------------------------------------------')
                    print('Performance is the same for {} of {} records. {}% of total'.format(len(sumSame),len(df),(len(sumSame)/len(df))))
                    print('Performance is better for {} on {} of {} records. {}% of total'.format(self.comparison[i].name,len(sumHigh),len(df),(len(sumHigh)/len(df))))
                    print('Performance is worse for {} on {} of {} records. {}% of total'.format(self.comparison[i].name,len(sumLow),len(df),(len(sumLow)/len(df))))
                    print('---------------------------------------------------------------------------')
    
    def __numericCat(self, perf):

        if (perf == '0-10'):
            output = 1
        elif (perf == '11-15'):
            output = 2
        elif (perf == '16-20'):
            output = 3
        elif (perf == '21-30'):
            output = 4
        elif (perf == '30+'):
            output = 5
        elif (perf == None):
            output = 6
        return output