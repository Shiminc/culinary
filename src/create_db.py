from pathlib import Path
import sqlite3
import pandas as pd

#create a data base
# Path('../data/culinary.db').touch()

#create a connection
conn = sqlite3.connect('../data/culinary.db')

# load the data into a Pandas DataFrame
# recipe = pd.read_csv('../data/01_Recipe_Details.csv')
# write the data to a sqlite table
# recipe.to_sql('recipes', conn, if_exists='append', index = False)

ingredients = pd.read_csv('../data/02_Ingredients.csv')
cpd_ingredients = pd.read_csv('../data/03_Compound_Ingredients.csv')
alias = pd.read_csv('../data/04_Recipe-Ingredients_Aliases.csv')

ingredients.to_sql('ingredients', conn, if_exists='append', index = False)
cpd_ingredients.to_sql('cpd_ingredients', conn, if_exists='append', index = False)
alias.to_sql('alias', conn, if_exists='append', index = False)