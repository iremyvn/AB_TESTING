
#Kontrol Grubu:Maximum Bidding
#Test Grubu:Average Bidding

#Impression : Reklam görüntüleme sayısı
#Click : Görüntülenen reklama tıklama sayısı
#Purchase : Tıklanan reklamlar sonrası satın alınan ürün sayısı
#Earning :Satın alınan ürünler sonrası elde edilen kazanç

pip install statsmodels

import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)



df_control=pd.read_excel("/Users/irem/Desktop/ab_testing.xlsx",sheet_name="Control Group")
df_test=pd.read_excel("/Users/irem/Desktop/ab_testing.xlsx",sheet_name="Test Group")
df_control.head()
df_test.head()

df_control.columns=[col + "_CG" for col in df_control.columns]
df_test.columns=[col + "_TG" for col in df_test.columns]



df_control.describe().T
df_test.describe().T

df_control.isnull().sum()
df_test.isnull().sum()



df=pd.concat([df_control,df_test],axis=1)
df.head()



df["Purchase_CG"].mean()
df["Purchase_TG"].mean()



test_stat,pvalue = shapiro(df["Purchase_CG"])
print('Test Stat = %.4f , p-value = %.4f' %(test_stat,pvalue))



test_stat,pvalue = shapiro(df["Purchase_TG"])
print('Test Stat = %.4f , p-value = %.4f' %(test_stat,pvalue))



test_stat,pvalue = levene(df["Purchase_CG"],df["Purchase_TG"])
print('Test Stat = %.4f , p-value = %.4f' %(test_stat,pvalue))



test_stat,pvalue=ttest_ind(df["Purchase_CG"],df["Purchase_TG"],equal_var=True)
print('Test Stat = %.4f , p-value = %.4f' %(test_stat,pvalue))

