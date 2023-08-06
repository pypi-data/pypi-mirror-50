import pandas as pd
import numpy as np
pd.set_option("display.precision", 2)
class Basic:
    def __init__(self,data):
        self.data = data
    
    def show(self):
        columns=[]
        datatypes=[]
        length=[]
        unique=[]
        nas =[]
        pmv = []
        for i in self.data.columns:
            columns.append(i)
            datatypes.append(self.data[i].dtypes)
            length.append(len(self.data[i]))
            unique.append(len(self.data[i].unique()))
            nas.append(self.data[i].isna().sum())
            pmv.append((self.data[i].isna().sum()/len(self.data[i]))*100)

        df = pd.DataFrame({'Column Name':columns,
                           'Data Type':datatypes,
                           'Count':length,
                           'No. of Unique':unique,
                          'Missing Values':nas,
                          '% Missing Values':pmv})
        display(df)
