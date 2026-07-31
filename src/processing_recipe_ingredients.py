# extract only allrecipes recipes from recipes table, and recipe-ingredients table
import pandas as pd
from itertools import combinations

def load_data():
    recipe = pd.read_csv('../data/01_Recipe_Details_reencode.csv')
    recipe.columns = ['recipe_id','title','source_site','cuisine']
    all_recipe = recipe[recipe['source_site']=='ALLRECIPES']

    recipe_ingredient = pd.read_csv('../data/04_Recipe-Ingredients_Aliases.csv')
    recipe_ingredient.columns = ['recipe_id','original_ingredient','aliased_ingredient','entity_id']
    recipe_ingredient_all_recipe = recipe_ingredient[recipe_ingredient['recipe_id'].isin(all_recipe['recipe_id']) ]

    return all_recipe, recipe_ingredient_all_recipe

def recategorise_olive(data):
    # the database categorise olive and olive oil as the same thing
    # not yet change the entity
    data.loc[data['original_ingredient'].str.contains('olive oil'),'aliased_ingredient'] = 'olive oil'
    return data

def reorganise_data(all_recipe, recipe_ingredient):
    json_array = []
    recipes = recipe_ingredient.recipe_id.unique()
    for recipe in recipes:
        ingredients = recipe_ingredient.loc[recipe_ingredient.recipe_id == recipe,'aliased_ingredient']

        recipe_dict = {'recipe_id': recipe,
                    #    strange pandas to just extract string
                       'title': all_recipe.loc[all_recipe.recipe_id==recipe,'title'].values[0],
                       'cuisine': all_recipe.loc[all_recipe.recipe_id==recipe,'cuisine'].values[0],
                       'number_of_ingredients': ingredients.shape[0],
                       }

        recipe_dict = calculate_combination(ingredients, recipe_dict)
        json_array.append(recipe_dict)
    return json_array 

def calculate_combination(ingredients, recipe_dict):
    for i in [2,3,4]:
        if ingredients.shape[0]>i:
            combination_string = 'combination' + '_' + str(i)
            recipe_dict[combination_string] = list(combinations(ingredients,i)) 

    return recipe_dict

def main():
    all_recipe, recipe_ingredient = load_data()
    recipe_ingredient = recategorise_olive(recipe_ingredient)
    data_json = reorganise_data(all_recipe, recipe_ingredient)
    print('finish')

main()