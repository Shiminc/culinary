# extract only allrecipes recipes from recipes table, and recipe-ingredients table
import pandas as pd
from itertools import combinations
from utils import load_data
import os,json

def reorganise_data(all_recipe, recipe_ingredient):
    json_array = []
    recipes = recipe_ingredient.recipe_id.unique()
    for recipe in recipes:
        ingredients = recipe_ingredient.loc[recipe_ingredient.recipe_id == recipe,'aliased_ingredient']

        recipe_dict = {'recipe_id': str(recipe),
                    #    strange pandas to just extract string
                       'title': all_recipe.loc[all_recipe.recipe_id==recipe,'title'].values[0],
                       'cuisine': all_recipe.loc[all_recipe.recipe_id==recipe,'cuisine'].values[0],
                       'number_of_ingredients': str(ingredients.shape[0]),
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


def write_to_json(path, list_of_dict):
    # too big file to write to disk
    with open(path,'w') as file:
        json.dump(list_of_dict,file)

def main():
    all_recipe, recipe_ingredient = load_data()
    data_json = reorganise_data(all_recipe, recipe_ingredient)
    # write_to_json("data.json", data_json)

    print('finish')

main()