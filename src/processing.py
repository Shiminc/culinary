# extract only allrecipes recipes from recipes table, and recipe-ingredients table
import pandas as pd


recipe = pd.read_csv('../data/01_Recipe_Details_reencode.csv')
recipe.columns = ['recipe_id','title','source_site','cuisine']
all_recipe = recipe[recipe['source_site']=='ALLRECIPES']
all_recipe.to_csv('all_recipe.csv', index=False)
recipe_ingredient = pd.read_csv('../data/04_Recipe-Ingredients_Aliases.csv')
recipe_ingredient.columns = ['recipe_id','original_ingredient','aliased_ingredient','entity_id']
recipe_ingredient_all_recipe = recipe_ingredient[recipe_ingredient['recipe_id'].isin(all_recipe['recipe_id']) ]
recipe_ingredient_all_recipe.to_csv('recipe_ingredient.csv',index=False)

print('finish')