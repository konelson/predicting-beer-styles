
# coding: utf-8

# Upload Beer Data to PostgresQL

import psycopg2 as pg
import pandas as pd
import pandas.io.sql as pd_sql

import pickle

#Postgres connection information

connection_args = {
    'host': '13.58.11.245', #Update IP here
    'user': 'ubuntu',
    'dbname':'beer_style',
    'port':5432
}

connection = pg.connect(**connection_args)


#Create beer style lookup tables:

ipa_query = 'SELECT style, styleid, ipa FROM styles WHERE ipa = 1'
apa_query = 'SELECT style, styleid, apa FROM styles WHERE apa = 1'
lager_query = 'SELECT style, styleid, lager FROM styles WHERE lager = 1'
stout_query = 'SELECT style, styleid, stout FROM styles WHERE stout = 1'
porter_query = 'SELECT style, styleid, porter FROM styles WHERE porter = 1'
saison_query = 'SELECT style, styleid, saison FROM styles WHERE saison = 1'
kolsch_query = 'SELECT style, styleid, kolsch FROM styles WHERE kolsch = 1'
ale_query = 'SELECT style, styleid, ale FROM styles WHERE ale = 1'
wheat_query = 'SELECT style, styleid, wheat FROM styles WHERE wheat = 1'
gose_query = 'SELECT style, styleid, gose FROM styles WHERE gose = 1'
barleywine_query = 'SELECT style, styleid, barleywine FROM styles WHERE barleywine = 1'
pilsner_query = 'SELECT style, styleid, pilsner FROM styles WHERE pilsner = 1'
other_query = 'SELECT style, styleid, other FROM styles WHERE other = 1'

ipa_styles = pd_sql.read_sql(ipa_query, connection)
apa_styles = pd_sql.read_sql(apa_query, connection)
lager_styles = pd_sql.read_sql(lager_query, connection)
stout_styles = pd_sql.read_sql(stout_query, connection)
porter_styles = pd_sql.read_sql(porter_query, connection)
saison_styles = pd_sql.read_sql(saison_query, connection)
kolsch_styles = pd_sql.read_sql(kolsch_query, connection)
ale_styles = pd_sql.read_sql(ale_query, connection)
wheat_styles = pd_sql.read_sql(wheat_query, connection)
gose_styles = pd_sql.read_sql(gose_query, connection)
barleywine_styles = pd_sql.read_sql(barleywine_query, connection)
pilsner_styles = pd_sql.read_sql(pilsner_query, connection)
other_styles = pd_sql.read_sql(other_query, connection)


#Print out style tables you want to look at:

#print("IPA Styles:", ipa_styles)
#print("APA Styles:",apa_styles)
#print("Lager Styles:", lager_styles)
#print("Stout Styles:", stout_styles)
#print("Porter Styles:", porter_styles)
#print("Saison Styles:", saison_styles)
#print("Kolsch Styles:", kolsch_styles)
#print("Ale Styles:",ale_styles)
#print("Wheat Styles:",wheat_styles)
#print("Gose Styles:",gose_styles)
#print("Other Styles:",other_styles)
#print("Barleywine Styles:",barleywine_styles)
#print("Pilsner Styles:", pilsner_styles)



"""

#Join beers and styles to select only styles from major category indicated

ipa_beers_query = '''

SELECT Name, a.Style, a.StyleID FROM beers as 
a INNER JOIN styles as b 
on a.StyleID = b.StyleID

WHERE ipa = 1
'''

pd_sql.read_sql(ipa_beers_query, connection)


#Lists "Other" Beers

other_beers_query = '''

SELECT Name, a.Style, a.StyleID FROM beers as 
a INNER JOIN styles as b 
on a.StyleID = b.StyleID

WHERE b.other = 1

'''

others_df = pd_sql.read_sql(other_beers_query, connection)


#Use this code to run simple logistic regression (can replace with any style)

beers_query = '''

SELECT BeerID, a.StyleID, Size, OG, FG, ABV,
       IBU, Color, BoilSize, BoilTime, BoilGravity, Efficiency,
       AllGrain, BIAB, PartialMash, extract, ipa FROM beers as 
a INNER JOIN styles as b 
on a.StyleID = b.StyleID

'''

pd_sql.read_sql(beers_query, connection)

"""


# Final model used in production

final_query = '''

SELECT *
FROM beers
LEFT JOIN styles ON beers.StyleID = styles.StyleID;

'''

beer_df = pd_sql.read_sql(final_query, connection)


with open ('beer.pickle', 'wb') as to_write:
    pickle.dump(beer_df, to_write)

beer_df.to_csv('beer_and_styles.csv', index = False, sep = ',')

