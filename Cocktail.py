class cocktail_ingredients:
    def __init__(self, ingredient, amount) -> None:
        self.ingredient = ingredient
        self.amount = amount
    def info(self):
        return self.ingredient + "   " + self.amount

class Cocktail:
    def __init__(self, title, glass, garnish, recipe, ingredients) -> None:
        self.name = title
        self.glass = glass
        self.garnish = garnish 
        self.recipe = recipe
        self.ingredients = [] # [(A, amount), (B, amount)]
        for item in ingredients:
            self.ingredients.append(cocktail_ingredients(item[0], item[1]))

    def print_cocktail(self):
        print("Name: " + self.name)
        print("Ingredients: ")
        for item in self.ingredients:
            print(item.info())
        print("Glass: " + self.glass)
        print("Garnish: " + self.garnish)
        print("Recipe: " + self.recipe)

    