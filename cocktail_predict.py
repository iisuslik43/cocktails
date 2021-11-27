from typing import List

import pandas as pd


def read_data():
    df = pd.read_csv('all_drinks.csv')

    def ingredients_from_columns(values):
        res = []
        for v in values:
            if not pd.isna(v):
                res.append(v.lower())
        return ','.join(res)

    df['ingredients'] = df[[f'strIngredient{i}' for i in range(1, 16)]].apply(ingredients_from_columns, axis=1)
    return df


cocktails_data = read_data()


def cocktail_description(ingredients: List[str]) -> str:
    def find_interception(cocktail):
        return sum([1 if ingr in cocktail else 0 for ingr in ingredients]) / len(cocktail.split(','))
    interception = cocktails_data['ingredients'].apply(find_interception)
    description = cocktails_data['strDrink'][interception.idxmax()]
    description = f'"{description}" - {cocktails_data["ingredients"][interception.idxmax()]}'
    return description


if __name__ == '__main__':
    print(cocktails_data['ingredients'])
    print(cocktail_description(['rum', 'juice']))
