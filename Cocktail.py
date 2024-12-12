import re 

class cocktail_ingredients:
    def __init__(self, amount, ingredient) -> None:
        self.ingredient = ingredient
        try:
            self.amount = amount.split()[0]
            self.unit = amount.split()[1]
        except:
            self.ingredient = ingredient
            self.unit = None 
    def info(self):
        return self.ingredient + ": " + self.amount + ' ' + "" if not self.unit else self.unit

class Cocktail:
    def __init__(self, title, glass, garnish, recipe, ingredients) -> None:
        self.name = title
        self.glass = glass
        self.garnish = garnish
        self.recipe = recipe
        self.technique = list(set(re.findall(r'\b[A-Z]{2,}\b', recipe)))
        self.ingredients = []
        for item in ingredients:
            self.ingredients.append(cocktail_ingredients(item[0], item[1]))

    def print_cocktail(self):
        print("Name: " + self.name)
        print("Ingredients: ")
        for item in self.ingredients:
            print(item.info())
        print("Glass: " + self.glass)
        print("Garnish: " + ("None" if type(self.garnish) is not str else self.garnish))
        print("Recipe: " + self.recipe)
        print("Technique: " + str(self.technique))
        print()

    
class Cocktail_Graph:
    
    def __init__(self) -> None:
        pass
