import pandas as pd
import numpy as np
pd.set_option("display.precision", 2)
pd.options.display.float_format = '{:.2f}'.format


class Basic:
    def __init__(self, data):
        self.data = data

    def show(self):
        columns = []
        datatypes = []
        length = []
        unique = []
        nas = []
        pmv = []
        mean = []
        median = []
        mode = []
        drange = []
        for i in self.data.columns:
            columns.append(i)
            datatypes.append(self.data[i].dtypes)
            length.append(len(self.data[i]))
            unique.append(len(self.data[i].unique()))
            nas.append(self.data[i].isna().sum())
            pmv.append((self.data[i].isna().sum()/len(self.data[i]))*100)
            if self.data[i].dtypes == 'int64' or self.data[i].dtypes == 'float64':
                mean.append(self.data[i].mean())
                median.append(self.data[i].median())
                mode.append('NA')
                drange.append(str(self.data[i].min())+'-'+str(self.data[i].max()))
            else:
                mean.append('NA')
                median.append('NA')
                mode.append(self.data[i].mode()[0])
                drange.append('NA')

        print("Dimensions of Dataframe-Rows:{},Columns:{}".format(self.data.shape[0], self.data.shape[1]))

        df = pd.DataFrame({'Column Name': columns,
                           'Data Type': datatypes,
                           'Count': length,
                           'No. of Unique': unique,
                          'Missing Values': nas,
                          '% Missing Values': pmv,
                          'Mean': mean,
                          'Median': median,
                          'Mode': mode,
                          'Range': drange})
        display(df)

    def Distributions(self):
        import matplotlib.pyplot as plt
        import seaborn as sns

        numeric_cols = self.data.select_dtypes(include=[np.number]).columns.tolist()
        cols = 3
        rows = int(np.ceil(len(numeric_cols)/3))
        fig, axes = plt.subplots(ncols=cols, nrows=rows,figsize=(20,12+rows))

        for i, ax in zip(numeric_cols, axes.flat):
            sns.distplot(self.data[i].dropna(), hist=True, ax=ax);
        plt.show()

        catogorical_cols = []
        higher_categories = []
        for i in self.data.select_dtypes(exclude=[np.number]).columns.tolist():
            if len(self.data[i].unique())<15:
                catogorical_cols.append(i)
            else:
                higher_categories.append(i)

        cols = 3
        rows = int(np.ceil(len(catogorical_cols)/3))
        if rows <=2:
            fig, axes = plt.subplots(ncols=cols, nrows=1,figsize=(20,12+rows))
        else:
            fig, axes = plt.subplots(ncols=cols, nrows=rows,figsize=(20,8))

        for i, ax in zip(catogorical_cols, axes.flat):
            sns.countplot(self.data[i].dropna(), ax=ax);
        plt.show()
        print('Categorical columns with more than 15 categories : {}'.format(higher_categories))
