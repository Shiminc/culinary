import pandas as pd

def resampling_recipe():
    # the top 5 cuisine has more than 5000,so I decided to resampling
    
    # USA                    39650
    # Italy                  24341
    # Mexico                 20077
    # Canada                  9618
    # Indian Subcontinent     8201

    # and also take away those ingredienst used less than 5 times?
    # and some strange category
    # is it possible to match it to foodCA food

    top_five_cuisine = ['USA','Italy']

    return ...

# TODO dedup within each recipe, and get rid of info as duplicating ingredient 
# *
# **
# Ingredient info:
# Equipment:
# long ingredient details with a mixed of things, the aliased ended up just recognised one ingredient
def load_data():
    recipe = pd.read_csv('../data/01_Recipe_Details_reencode.csv')
    recipe.columns = ['recipe_id','title','source_site','cuisine']
    all_recipe = recipe[recipe['source_site']=='ALLRECIPES']


    # Group spain and portugal as one group
    # Group Dutch and Belgian as one group
    all_recipe.loc[all_recipe['cuisine'].isin(['Spain','Misc.: Portugal']),'cuisine']='Iberia'
    all_recipe.loc[all_recipe['cuisine'].isin(['Misc.: Dutch','Misc.: Belgian']),'cuisine']='Belgium-Netherlands'

    

    recipe_ingredient = pd.read_csv('../data/04_Recipe-Ingredients_Aliases.csv')
    recipe_ingredient.columns = ['recipe_id','original_ingredient','aliased_ingredient','entity_id']
    recipe_ingredient_all_recipe = recipe_ingredient[recipe_ingredient['recipe_id'].isin(all_recipe['recipe_id']) ]
    recipe_ingredient_all_recipe.aliased_ingredient=recipe_ingredient_all_recipe.aliased_ingredient.str.rstrip()
    # put zucchini green as zucchini since only one recipe
    recipe_ingredient_all_recipe.loc[recipe_ingredient_all_recipe['aliased_ingredient']=='zucchini green','aliased_ingredient']='zucchini'
    # probles of potatoes
    # did not change potato bread as only 3 recipes
    
    # put potato etc as potato
    recipe_ingredient_all_recipe.loc[recipe_ingredient_all_recipe['aliased_ingredient']=='potato chip','aliased_ingredient']='potato'
    recipe_ingredient_all_recipe.loc[recipe_ingredient_all_recipe['aliased_ingredient']=='potato gratin','aliased_ingredient']='potato'
    recipe_ingredient_all_recipe.loc[recipe_ingredient_all_recipe['aliased_ingredient']=='potato fried','aliased_ingredient']='potato'
    recipe_ingredient_all_recipe.loc[recipe_ingredient_all_recipe['aliased_ingredient']=='fried potato','aliased_ingredient']='potato'
    recipe_ingredient_all_recipe.loc[recipe_ingredient_all_recipe['original_ingredient'].str.contains('potato bread farls'),'aliased_ingredient'] = 'potato'

    # the database categorise olive and olive oil as the same thing
    # not yet change the entity
    recipe_ingredient_all_recipe.loc[recipe_ingredient_all_recipe['original_ingredient'].str.contains('olive oil'),'aliased_ingredient'] = 'olive oil'

    # problems of sauce soybean
    recipe_ingredient_all_recipe.loc[recipe_ingredient_all_recipe['original_ingredient'].str.contains('teriyaki'),'aliased_ingredient'] = 'teriyaki sauce'
    recipe_ingredient_all_recipe.loc[recipe_ingredient_all_recipe['original_ingredient'].str.contains('Teriyaki'),'aliased_ingredient'] = 'teriyaki sauce'

    # correcting typo
    recipe_ingredient_all_recipe.loc[recipe_ingredient_all_recipe['aliased_ingredient']=='tumeric','aliased_ingredient']='turmeric'
    recipe_ingredient_all_recipe=recipe_ingredient_all_recipe[recipe_ingredient_all_recipe['original_ingredient']!='Sauce']

    return all_recipe, recipe_ingredient_all_recipe

