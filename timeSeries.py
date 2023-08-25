import pandas as pd
from statsmodels.tsa.arima_model import ARIMA

def futureValue(df):
    model = ARIMA(df, order=(1, 1, 0))
    model_fit = model.fit(disp=False)
    yhat = model_fit.predict(len(df), len(df), typ='levels')
    predictedValue = yhat.tolist()
    return(predictedValue[0])

def demandPrediction():
    data = pd.read_csv('demandForecast.csv')
    df1 = data['whole milk']
    df2 = data['Vegetables']
    df3 = data['Fruits']
    df4 = data['Bottled Water']
    df5 = data['Soft Drinks ']
    df6 = data['Non Veg']
    df7 = data['Bath Soaps']
    df8 = data['Biscuits ']  
    df9 = data['Whole Grains']
    df10 = data['Cosmotics '] 

    result = [futureValue(df1),futureValue(df2),futureValue(df3),futureValue(df4),futureValue(df5),
    futureValue(df6),futureValue(df7),futureValue(df8),futureValue(df9),futureValue(df10)]
    return {'Product':['Whole Milk','Vegetables','Fruits','Bottled Water','Soft Drinks',
    'Non Veg','Bath Soaps','Biscuits','Whole Grains','Cosmotics'],'Predicted Demand':result}



 


