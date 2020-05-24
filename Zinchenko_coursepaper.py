#!/usr/bin/env python
# coding: utf-8

# In[28]:


import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')


# Загрузка данных и их обработка

# In[29]:


dt = pd.read_csv('SBER_190101_200101.txt', sep = ',')


# In[30]:


data = dt.drop(['<TICKER>', '<PER>', '<TIME>', '<VOL>'], axis = 1)
data.head(5)


# In[31]:


print(f'В выборке представлена информация об акциях Сбербанка за {data.shape[0]} торговых дня')


# Вычисление спреда по Роллу

# In[32]:


data['delta Pt'] = data['<CLOSE>'].diff()
data['delta Pt-1'] = data['<CLOSE>'].diff().shift(periods = 1)


# In[33]:


Rspread = 2*(-data.cov().loc['delta Pt','delta Pt-1'])**(0.5)


# In[34]:


Rspread


# Расчеты по Глостену-Милгому

# In[35]:


theta = 0.5
mu = 0.25
gamma = 0.5


# In[36]:


vH = data['<HIGH>'].mean()
vL = data['<LOW>'].mean()


# In[37]:


Prior_Exp = theta*vH + (1-theta)*vL


# In[38]:


P_buy_vH = mu*1 + (1-mu)*gamma
P_buy_vL = mu*0 + (1-mu)*gamma


# In[39]:


P_buy = P_buy_vH*theta + P_buy_vL*(1-theta)


# In[40]:


P_vH_buy = P_buy_vH*theta/P_buy


# In[41]:


Exp_buy = P_vH_buy*vH + (1-P_vH_buy)*vL
Exp_buy


# In[42]:


P_vH_sell = (1-P_vH_buy)*theta/(1-P_buy)


# In[43]:


Exp_sell = P_vH_sell*vH + (1-P_vH_sell)*vL
Exp_sell


# Bid-ask спред

# In[44]:


S = Exp_buy - Exp_sell
S


# In[45]:


#все предыдущие вычисления в виде функции
def GlMSpread(data, theta = 0.5, mu = 0.25, gamma = 0.5):
    
    vH = data['<HIGH>'].mean()
    vL = data['<LOW>'].mean()
    
    Prior_Exp = theta*vH + (1-theta)*vL
    P_buy_vH = mu*1 + (1-mu)*gamma
    P_buy_vL = mu*0 + (1-mu)*gamma
    P_buy = P_buy_vH*theta + P_buy_vL*(1-theta)
    
    P_vH_buy = P_buy_vH*theta/P_buy
    P_vH_sell = (1-P_vH_buy)*theta/(1-P_buy)
    
    Exp_buy = P_vH_buy*vH + (1-P_vH_buy)*vL
    Exp_sell = P_vH_sell*vH + (1-P_vH_sell)*vL
    
    S = Exp_buy - Exp_sell
    
    return S


# In[46]:


d = {}


# In[47]:


for mu in np.arange(0.2, 0.55, 0.05):
    d[round(mu, 2)]= GlMSpread(data, mu = mu)


# In[48]:


d


# In[49]:


import matplotlib.pylab as plt

lists = sorted(d.items()) 
x, y = zip(*lists)

plt.plot(x, y)
plt.grid(color='grey', linestyle='-', linewidth=1, alpha = 0.5)
plt.title('Зависимость спреда от доли инсайдеров на рынке')
plt.xlabel('Доля трейдеров')
plt.ylabel('Bid-ask спред')
plt.show()


# Расчеты по модели Кейла

# In[50]:


dt = pd.read_csv('SBER_190101_200101.txt', sep = ',')
data = dt.drop(['<TICKER>', '<PER>', '<TIME>'], axis = 1)
data.head(5)


# In[51]:


data['delta Pt'] = data['<CLOSE>'].diff()
data['lambda'] = abs(data['delta Pt'])/data['<VOL>']
data['<DATE>'] = data['<DATE>'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))

data.head(10)


# In[52]:


data['lambda'].mean()


# In[53]:


fig = plt.figure(figsize = (15, 7))
fig = plt.hist(data['lambda'], edgecolor = 'black', bins = 50)

plt.show()


# In[54]:


fig = plt.figure(figsize = (15, 7))
fig = plt.plot(data['<DATE>'], data['lambda'])

plt.show()


# In[ ]:




