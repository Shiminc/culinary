import pandas as pd
from utils import load_data

def list_ingredients(data):
    ingredients = pd.DataFrame(data.groupby(by=['aliased_ingredient','cuisine'])['recipe_id'].count())
    ingredients.reset_index(inplace=True)
    ingredients=ingredients.pivot(index='aliased_ingredient',
                      columns='cuisine',
                      values='recipe_id',               
                      )
    ingredients.fillna(0,inplace=True)
    ingredients.reset_index(inplace=True)
    # ingredients.reset_index(inplace=True)
    ingredients['sum']=ingredients.sum(numeric_only=True,axis=1)
    return ingredients

def main():
    all_recipe, recipe_ingredient = load_data()
    data = recipe_ingredient.merge(all_recipe, on='recipe_id')
    data = data[['recipe_id','title','aliased_ingredient','entity_id', 'cuisine']]
    ingredients = list_ingredients(data)
    ingredients.to_csv('processed_ingredients.csv')
    # print(all_recipe.cuisine.value_counts(normalize=True))
    # print(all_recipe.cuisine.value_counts())

    print('finish')

    

main()