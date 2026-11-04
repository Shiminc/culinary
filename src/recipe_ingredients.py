import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

def remove_number(reduced_recipe_ingredient):
    reduced_recipe_ingredient['original_ingredient'] = reduced_recipe_ingredient['original_ingredient'].str.replace(r'\d+[A-Za-z]*\d*', '', regex=True)
    return reduced_recipe_ingredient

def remove_accompaniment(reduced_recipe_ingredient):
    # 606 of them
    # temporary
    reduced_recipe_ingredient = reduced_recipe_ingredient[~reduced_recipe_ingredient['original_ingredient'].str.contains("accompaniment|accompaniments",flags=re.IGNORECASE,regex=True)]
    return reduced_recipe_ingredient

def create_bow_df(ingredients_in_string):
    bow_counter= CountVectorizer()

    bow_df = pd.DataFrame(bow_counter.fit_transform(ingredients_in_string).toarray())

    vocab_df = pd.DataFrame({'terms':bow_counter.vocabulary_.keys(), 'indices':bow_counter.vocabulary_.values()})
    vocab_df.sort_values(by='indices',inplace=True)
    bow_df.columns = vocab_df['terms']
    return bow_df

def recipe_with_rare_ingredients(recipe_ingredient):
    # to exclude ingredients that appear less than 10 times
    ingredient_recipe_presence_count = pd.DataFrame(recipe_ingredient.groupby(by='aliased_ingredient')['recipe_id'].nunique())
    ingredient_recipe_presence_count.reset_index(inplace=True)
    ingredient_recipe_presence_count.columns = ['aliased_ingredient','recipe_count']
    ingredient_recipe_presence_count.sort_values(by='recipe_count',inplace=True)
    ingredient_excluded = ingredient_recipe_presence_count.loc[ingredient_recipe_presence_count['recipe_count']<10]
    recipe_excluded = pd.merge(recipe_ingredient,ingredient_excluded,on='aliased_ingredient',how='right')
    
    return recipe_excluded['recipe_id']

def recipe_with_problematic_original_ingredients(recipe_ingredient):
    # long string of ingredients could be just some notes about some ingredients or long list of ingredients which the aliased ingredients did not recognised correctly
    recipe_ingredient['length'] = recipe_ingredient['original_ingredient'].str.len()
    Q1 = recipe_ingredient['length'].quantile(0.25)
    Q3 = recipe_ingredient['length'].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outlier = recipe_ingredient[recipe_ingredient['length']>upper_bound]
    return outlier['recipe_id']

def exclude_recipe(recipe_ingredient):
    total_excluded_id = set(list(recipe_with_rare_ingredients(recipe_ingredient)) + list(recipe_with_problematic_original_ingredients(recipe_ingredient)))
    return total_excluded_id


def combine_ingredients_to_str(reduced_recipe_ingredient):
    return reduced_recipe_ingredient.groupby('recipe_id')['original_ingredient'].apply(lambda x: ','.join(x))

def main():
    recipe_ingredient = pd.read_csv('../data/CulinaryDB/04_Recipe-Ingredients_Aliases.csv')
    recipe_ingredient.columns = ['recipe_id','original_ingredient','aliased_ingredient','entity_id']

    recipe = pd.read_csv('../data/CulinaryDB/01_Recipe_Details.csv')
    recipe.columns = ['recipe_id','title','source_site','cuisine']


    total_excluded_id = exclude_recipe(recipe_ingredient)
    reduced_recipe = recipe[~recipe['recipe_id'].isin(total_excluded_id)]  
    reduced_recipe_ingredient = recipe_ingredient [~recipe_ingredient['recipe_id'].isin(total_excluded_id) ]
    reduced_recipe_ingredient = remove_accompaniment(reduced_recipe_ingredient)
    reduced_recipe_ingredient = remove_number(reduced_recipe_ingredient)
    ingredients_in_string = combine_ingredients_to_str(reduced_recipe_ingredient) 
    ingredients_bow = create_bow_df(ingredients_in_string)
    print('finish')


main()