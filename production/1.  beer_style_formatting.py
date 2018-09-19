
# coding: utf-8

# # Beer Style - Formatting


import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

beer_data = pd.read_csv('recipeData.csv', encoding = 'latin-1')

#Drop columns with >30% N/A's

beer_data.drop(columns = ['MashThickness', 'PitchRate', 'PrimaryTemp', 'PrimingMethod', 'PrimingAmount','UserId'], inplace = True)

beer_data.drop(columns = ['URL','SugarScale'], inplace = True)


boilgravity_mask = beer_data.BoilGravity.isna() == False

beer_data = beer_data[boilgravity_mask]


#Remove all Style NaN 111

beer_data = beer_data[beer_data['StyleID'] != 111]


#Create one-hot encoded version of brew method

beer_data = beer_data.join(pd.get_dummies(beer_data['BrewMethod']))


beer_data.rename(columns = {'All Grain':'AllGrain', 'Partial Mash': 'PartialMash'}, inplace = True)


#Create new csv with formatted df to use in psql

beer_data.to_csv('recipeData_formatted.csv', index = False, sep = ',')


beer_style = pd.read_csv('styleData.csv', encoding = 'latin-1')

#Group 175 styles into 10 style categories

style_list = ['IPA', 'Lager', 'Stout', 'Porter', 'Cider', 'Saison', 'Kölsch', 'Ale', 'Gose', 'Barleywine']
for item in style_list:
    beer_style[item] = np.where(beer_style['Style'].str.contains(item, regex = False), 1, 0)

beer_style['APA'] = np.where(beer_style['Style'].str.contains('American Pale Ale', regex = False), 1, 0)
beer_style['Ale'] = np.subtract(beer_style['Ale'], beer_style['APA'])    
beer_style['Wheat'] = np.add(np.add(
            np.where(beer_style['Style'].str.contains('Wheat', regex = False), 1, 0), 
            np.where(beer_style['Style'].str.contains('Witbier', regex = False), 1, 0)),
            np.where(beer_style['Style'].str.contains('Weiss', regex = False), 1, 0))
beer_style['Pilsner'] = np.add(
            np.where(beer_style['Style'].str.contains('Pilsner', regex = False), 1, 0), 
            np.where(beer_style['Style'].str.contains('Pilsener', regex = False), 1, 0))
            
other_beer = beer_style[(beer_style['IPA'] == 0) & (beer_style['Lager'] == 0) & (beer_style['Stout'] == 0) & (beer_style['Porter'] == 0)&(beer_style['Cider'] == 0)&(beer_style['Saison'] == 0)&(beer_style['Wheat'] == 0)&(beer_style['Kölsch'] == 0)&(beer_style['Ale'] == 0)&(beer_style['Gose'] == 0)&(beer_style['Barleywine'] == 0)&(beer_style['Pilsner'] == 0)]

beer_style['Other'] = np.where(beer_style['Style'].isin(other_beer.Style), 1, 0)


#Create new csv with formatted df to use in psql

beer_style.to_csv('styleData_formatted.csv', index = False, sep = ',')

beer_style_formatted = pd.read_csv('styleData_formatted.csv')

