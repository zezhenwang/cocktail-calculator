import re 

class cocktail_ingredients:
    def __init__(self, amount, ingredient) -> None:
        self.ingredient = ingredient
        self.amount = amount.split()[0]
        self.unit = amount.split()[1]
        
    def info(self):
        return self.ingredient + ": " + self.amount + ' ' + self.unit

class Cocktail:
    def __init__(self, title, glass, garnish, recipe, ingredients) -> None:
        self.name = title
        self.glass = glass
        self.garnish = garnish
        self.recipe = recipe
        self.technique = list(set(re.findall(r'\b[A-Z]{2,}\b', recipe)))
        self.ingredients = [] # [(A, amount), (B, amount)]
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

    