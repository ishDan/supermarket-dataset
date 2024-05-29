import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as py
from mlxtend.frequent_patterns import apriori,association_rules

marketing_data = pd.read_csv("50_SupermarketBranches.csv")
customer_data = pd.read_csv("Supermarket_CustomerMembers.csv")
df_products = pd.read_csv("Market_Basket_Optimisation.csv",header=None)

marketing_data.head()

customer_data.head()

df_products.head()

df_products.info()

State = marketing_data.State.unique()
State

x0 = marketing_data['Profit']
x1 = marketing_data['Advertisement Spend']

fig = go.Figure(data=[
    go.Bar(name='Profit', x=State, y=x0),
    go.Bar(name='Advertisement', x=State, y=x1)
])
# Change the bar mode
fig.update_layout(barmode='group')
fig.update_layout(
    title='Profit and Advertisement in every state')
fig.show()

customer_data.info()

fig2 = go.Figure()
fig2.add_trace(go.Histogram(histfunc="sum", x=customer_data['Genre']))
fig2.update_layout(
    title='Gender ratio')

fig = px.scatter_matrix(customer_data,dimensions=["Age","Spending Score (1-100)","Annual Income (k$)"], color = "Genre")
fig.update_layout(
    title='Supermaket customers Dataset',
    dragmode='select',
    width=1000,
    height=600,
    hovermode='closest',
)
fig.show()

products = df_products.values.tolist()
name_col =['ID_client','item_description']
df_prod = pd.DataFrame(columns=name_col)
for i in range(len(products)):
    buy_list = set(products[i])
    for j in buy_list:
        n = len(df_prod.index)
        df_prod.loc[n,'ID_client'] = i
        df_prod.loc[n,'item_description'] = j

df_prod.dropna(inplace = True)

df_prod

list_products = set()
for i in range(len(products)):
    list_products = set(products[i]) | list_products
    
list_products = list(list_products)
# list_products.pop(0)
list_products.append('Count_products')
aa =np.zeros((len(products),len(list_products)))
df_prod2 = pd.DataFrame(aa, columns = list_products)

for i in range(len(products)-1):
    buy_list = set(products[i])
    for j in range(len(list_products)-1):
        for k in buy_list:
            if list_products[j] == k:
                df_prod2.iloc[i,j] = 1 + df_prod2.iloc[i,j]

    df_prod2.iloc[i,len(list_products)-1] = df_prod2.iloc[i,0:len(list_products)-2].sum()
    
pd.set_option('display.max_columns', None)
df_prod2.describe()

df_prod2

fig6 = px.histogram(df_prod, x="item_description", color="item_description").update_xaxes(categoryorder='total descending')
fig6.update_layout(
    title='Items purchased in the supermarket',
    dragmode='select',
    width=2000,
    height=600,
    hovermode='closest',
)
fig6.show()



df_prod2.drop(columns = ['Count_products'],inplace = True)

freq_item = apriori(df_prod2, min_support=0.01, use_colnames=True)
freq_item['length'] = freq_item['itemsets'].apply(lambda x: len(x))
freq_item

freq_item[ (freq_item['length'] == 2) & (freq_item['support'] >= 0.04) ]

freq_item[ (freq_item['length'] == 3)]

rules = association_rules(freq_item, metric="lift", min_threshold=1.3)
rules["antecedents_length"] = rules["antecedents"].apply(lambda x: len(x))
rules["consequents_length"] = rules["consequents"].apply(lambda x: len(x))
rules.sort_values("confidence",ascending=False).head(15)

fig7 = px.scatter(rules, x ='support', y =  'lift', color = 'confidence')
fig7.update_layout(
    title='Supermaket customers Dataset',
    dragmode='select',
    width=1000,
    height=600,
    hovermode='closest',
)
fig7.show()

rules[ (rules['antecedents_length'] == 1) ].sort_values("confidence",ascending=False).head(10)

## Ascending = True

rules[ (rules['antecedents_length'] == 1) & (rules['consequents_length'] == 1) ].sort_values("confidence",ascending=True).head(10)

