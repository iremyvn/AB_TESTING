#AB Testi ile Bidding Yöntemlerinin Dönüşümünün Karşılaştırılması

#İş Problemi:

#  Facebook kısa bir süre önce mevcut "Maximum Bidding" adı verilen teklif verme türüne alternatif olarak yeni bir
#teklif türü olan "Average Bidding"i tanıttı.

#  Müşterilerimizden biri olan bombabomba.com, bu yeni özelliği test etmeye karar verdi ve average bidding'in maximum
#bidding'ten daha fazla dönüşüm getirip getirmediğini anlamak için A/B testi yapmak istiyor.

#  A/B testi 1 aydır devam ediyor ve bombabomba.com şimdi sizden bu A/B testinin sonuçlarını analiz etmenizi bekliyor.
#Bombabomba.com için nihai başarı ölçüsü "purchase"dir.Bu nedenle, istatistiksel testler için "purchase" metriğine
#odaklanılmalıdır.

#Kontrol Grubu:Maximum Bidding
#Test Grubu:Average Bidding

#Impression : Reklam görüntüleme sayısı
#Click : Görüntülenen reklama tıklama sayısı
#Purchase : Tıklanan reklamlar sonrası satın alınan ürün sayısı
#Earning :Satın alınan ürünler sonrası elde edilen kazanç

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

#GOREV1:VERİYİ HAZIRLAMA VE ANALİZ ETME

#ADIM1:

df_control=pd.read_excel("/Users/irem/Desktop/ab_testing.xlsx",sheet_name="Control Group")
df_test=pd.read_excel("/Users/irem/Desktop/ab_testing.xlsx",sheet_name="Test Group")
df_control.head()
df_test.head()

df_control.columns=[col + "_CG" for col in df_control.columns]
df_test.columns=[col + "_TG" for col in df_test.columns]

#ADIM2

df_control.describe().T
df_test.describe().T

df_control.isnull().sum()
df_test.isnull().sum()

#ADIM3:

df=pd.concat([df_control,df_test],axis=1)
df.head()

#GOREV2:A/B TESTİNİN HİPOTEZİNİN TANIMLANMASI

#H0=M1 == M2 (Kontrol grubu  ile test gruplarının
# purchase ortalamaları arasında istatistiksel olarak anlamlı bir fark yoktur.)
#H1=M1 != M2 (.... fark vardır.)

df["Purchase_CG"].mean()
df["Purchase_TG"].mean()

#Burada aralarında fark gözüküyor ancak bu fark şans eseri mi değil mi onu incelememiz gerekiyor.

#GOREV3:HİPOTEZ TESTİNİN GERÇEKLEŞTİRİLMESİ

#NORMALLİK VARSAYIMI (shapiro = Bir değişkenin dağılımının normal olup olmadığını test eder.)
#H0 = Normallik varsayımı sağlanmaktadır.
#H1 = Normallik varsayımı sağlanmamaktadır.

test_stat,pvalue = shapiro(df["Purchase_CG"])
print('Test Stat = %.4f , p-value = %.4f' %(test_stat,pvalue))

# p-value=0.5891 > 0.05 H0 reddedilemez.Normallik varsayımı sağlanmaktadır.

test_stat,pvalue = shapiro(df["Purchase_TG"])
print('Test Stat = %.4f , p-value = %.4f' %(test_stat,pvalue))

# p-value=0.1541 > 0.05 H0 reddedilemez.Normallik varsayımı sağlanmaktadır.


#VARYANS HOMOJENLİĞİ VARSAYIMI (LEVENE TESTİ)
#H0 = Varyanslar homojendir.
#HS = Varyanslar homojen değildir.

test_stat,pvalue = levene(df["Purchase_CG"],df["Purchase_TG"])
print('Test Stat = %.4f , p-value = %.4f' %(test_stat,pvalue))

# p-value = 0.1083 > 0.05 H0 reddedilemez.Varyanslar homojendir.

#Varsayımlar sağlandığından t testi yapıyoruz.(parametrik)

test_stat,pvalue=ttest_ind(df["Purchase_CG"],df["Purchase_TG"],equal_var=True)
print('Test Stat = %.4f , p-value = %.4f' %(test_stat,pvalue))

# p-value = 0.3493 > 0.05 H0 reddedilemez.Kontrol grubu "Maximum Biding" ile test grubu "Average Biding"in
# purchase ortalamaları arasında istatistiksel olarak anlamlı bir fark yoktur.

#Maximum Bidding kullanılmaya devam edilebilir.