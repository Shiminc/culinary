import pandas as pd

ingredients = pd.read_csv('../data/02_Ingredients.csv')


def process_cpd_ingredients():
    cpd_ingredients = pd.read_csv('../data/03_Compound_Ingredients.csv')
    cpd_ingredients.columns = ['cpd_ingredient_name','cpd_ingredient_synonyms','entity_id','constituents','category']
    cpd_ingredients.loc[cpd_ingredients['cpd_ingredient_name']=='Cake Mix','category']='Bakery'
    cpd_ingredients.loc[cpd_ingredients['cpd_ingredient_name']=='Self Rising Flour','category']='Bakery'
    # croissant

    # change = to -


    return cpd_ingredients

def main():

    print('finish')

main()