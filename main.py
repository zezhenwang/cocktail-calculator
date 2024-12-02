import pandas as pd
from Cocktail import Cocktail

def parse_csv(file_path):
    df = pd.read_csv(file_path)
    column_names = list(df.columns)
    cocktails = []
    for index, row in df.iterrows():
        cocktails.append(Cocktail(row[column_names[0]], row[column_names[1]], row[column_names[2]], row[column_names[3]], eval(row[column_names[5]])))
        if index > 10:
            break
        

    return cocktails

file_path = 'train.csv'  
cocktails = parse_csv(file_path)
for cocktail in cocktails:
    cocktail.print_cocktail()
    