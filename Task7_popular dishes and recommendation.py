import json
import re
import pandas as pd
from pprint import pprint
import pickle
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog



def save(data, name):
    filehandler = open(name,"wb")
    pickle.dump(data, filehandler)
    filehandler.close()
def load(name):
    filehandler = open(name, "rb")
    return pickle.load(filehandler)


df = load('dataset_pd.pickle')
our_dishes = load('our_dishes.pickle')
our_restaurants = load('our_restaurants.pickle')

df = df[df['dishes'].map(len) != 0]

dish_df = pd.DataFrame(columns=['total','1 star', '2 star', '3 star', '4 star', '5 star'])
cnt=0

for dish in our_dishes:

    filtered_df = df[df['dishes'].apply(lambda x: dish in x)]
    total = len(filtered_df)
    one = len(filtered_df[filtered_df['star']==1])
    two = len(filtered_df[filtered_df['star']==2])
    thr = len(filtered_df[filtered_df['star']==3]) 
    fou = len(filtered_df[filtered_df['star']==4])
    fiv = len(filtered_df[filtered_df['star']==5])

    dish_df.loc[dish] = [total, one, two, thr, fou, fiv]

plot_dish_df = dish_df.sort_values(by='total', ascending=False).iloc[:50]
print('total max:', plot_dish_df['total'].max(), ', total min:',plot_dish_df['total'].min())
del plot_dish_df['total']


ax=plot_dish_df.plot.barh(stacked=True, 
                       figsize=(10,10), 
                       color=['yellow', 'plum', 'red', 'springgreen', 'darkblue'],
                       fontsize=13
                       )



plot_dish_df['total'] = plot_dish_df['1 star'] + plot_dish_df['2 star'] + plot_dish_df['3 star'] + plot_dish_df['4 star'] + plot_dish_df['5 star']
plot_scaled_df = pd.DataFrame(columns=['1 star', '2 star', '3 star', '4 star', '5 star'])
plot_scaled_df['1 star'] = plot_dish_df['1 star'] / plot_dish_df['total']
plot_scaled_df['2 star'] = plot_dish_df['2 star'] / plot_dish_df['total']
plot_scaled_df['3 star'] = plot_dish_df['3 star'] / plot_dish_df['total']
plot_scaled_df['4 star'] = plot_dish_df['4 star'] / plot_dish_df['total']
plot_scaled_df['5 star'] = plot_dish_df['5 star'] / plot_dish_df['total']\

plot_scaled_df.plot.barh(stacked=True, 
                       figsize=(10,15), 
                       color=['yellow', 'plum', 'red', 'springgreen', 'darkblue'],
                       fontsize=14
                       )
 
plt.show()

application_window = tk.Tk()

answer = simpledialog.askstring("Input", "Which Indian cuisine do you want to have ?",
                                parent=application_window)





pop_dish_df = df[df['dishes'].apply(lambda x: answer in x)]
restaurant_df = pd.DataFrame(columns=['total','1 star', '2 star', '3 star', '4 star', '5 star'])
cnt=0

for restaurant in our_restaurants:

    filtered_df = pop_dish_df[pop_dish_df['restaurant'].apply(lambda x: restaurant in x)]
    total = len(filtered_df)
    one = len(filtered_df[filtered_df['star']==1])
    two = len(filtered_df[filtered_df['star']==2])
    thr = len(filtered_df[filtered_df['star']==3]) 
    fou = len(filtered_df[filtered_df['star']==4])
    fiv = len(filtered_df[filtered_df['star']==5])

    restaurant_df.loc[restaurant] = [total, one, two, thr, fou, fiv]
plot_rest_df = restaurant_df.sort_values(by='total', ascending=False).iloc[:30]
print('total max:',plot_rest_df['total'].max(), ', total min:',plot_rest_df['total'].min())
del plot_rest_df['total']

plot_rest_df.plot.barh(stacked=True, 
                       figsize=(8,10), 
                       color=['yellow', 'plum', 'red', 'springgreen', 'darkblue'])
plt.title("Top 30 restaurnts serving: "+answer,fontsize = 16)
plt.show()
