import pandas as pd
import re
import networkx as nx
import random
import difflib
from tabulate import tabulate


cocktail_techniques = [
    "SHAKE",
    "STIR",
    "MUDDLE",
    "STRAIN",
    "FLOAT",
    "LAYER",
    "BUILD",
    "ROLL",
    "BLEND",
    "SWIZZLE"
]

class Cocktail:
    """
    Represents an individual cocktail.

    Attributes
    ----------
    name : str
        The name/title of the cocktail.
    glass : str
        The type of glass in which the cocktail is served.
    garnish : str
        The garnish used for the cocktail. Defaults to "None" if not provided.
    recipe : str
        A textual description of the cocktail's preparation steps.
    ingredients : list of tuples
        A list of ingredients, where each element is a tuple (amount, ingredient_name).
    techniques : list of str
        Techniques extracted from the recipe. Defaults to "BUILD" if no techniques are found.

    Methods
    -------
    get_similarity(other)
        Calculates similarity with another cocktail based on shared ingredients 
        and techniques.
    print_cocktail()
        Prints the cocktail's details, including name, glass, garnish, ingredients, 
        and recipe.
    """
    def __init__(self, title, glass, garnish, recipe, ingredients):
        """
        Initialize a Cocktail instance.

        Parameters
        ----------
        title : str
            The name/title of the cocktail.
        glass : str
            The type of glass used for the cocktail.
        garnish : str or None
            The garnish for the cocktail. Defaults to "None" if not a string.
        recipe : str
            A string describing the steps to prepare the cocktail.
        ingredients : list of tuples
            A list of list containing [amount, ingredient_name].
        """
        self.name = title
        self.glass = glass
        self.garnish = garnish if isinstance(garnish, str) else "None"
        self.recipe = recipe
        self.ingredients = ingredients
        self.techniques = [tech for tech in set(re.findall(r'\b[A-Z]{2,}\b', recipe)) if tech in cocktail_techniques] or ["BUILD"]

    def get_similarity(self, other):
        """
        Calculate similarity with another cocktail.

        The similarity score is calculated based on:
        - Shared ingredients (weighted 3 points each)
        - Shared techniques (weighted 1 point each)

        Parameters
        ----------
        other : Cocktail
            Another Cocktail object to compare against.

        Returns
        -------
        int
            The similarity score between the two cocktails.
        """
        shared_ingredients = set(i[1] for i in self.ingredients).intersection(set(i[1] for i in other.ingredients))
        shared_techniques = set(self.techniques).intersection(set(other.techniques))
        return len(shared_ingredients) * 3 + len(shared_techniques) # This is tested for best performance and connectedness
    
    def print_cocktail(self):
        """Print the cocktail"""
        print(f"\nRandom Cocktail: {self.name}")
        print(f"Glass: {self.glass}")
        print(f"Garnish: {self.garnish}")
        print("Ingredients:", ', '.join([i[1] + ' ' + i[0] for i in self.ingredients]))
        print(f"Recipe: {self.recipe}")
        # print("Techniques:", ', '.join(self.techniques))

class CocktailGraph:
    """
    Builds and manages a graph of cocktails.

    A cocktail graph is constructed using nodes to represent cocktails 
    and edges to represent similarities between cocktails based on ingredients 
    and techniques.

    Attributes
    ----------
    cocktails : list 
        A list of Cocktail objects parsed from the CSV file.
    graph : networkx.Graph
        A NetworkX graph representing the cocktail relationships.
    threshold : int
        Threshold used to compute the graph.

    Methods
    -------
    load_cocktails(file_path)
        Reads cocktail data from a CSV file and creates Cocktail objects.
    build_graph(threshold=3)
        Constructs the graph by connecting cocktails with similarity above the threshold.
    find_shortest_path(cocktail1, cocktail2)
        Finds the shortest path between two cocktails based on edge weights.
    get_random_cocktail()
        Returns a random cocktail from the graph.
    cocktail_exists(cocktail_name)
        Checks if a cocktail with the given name exists in the graph.
    fuzzy_search_cocktail(cocktail_name)
        Searches for close matches to a cocktail name using fuzzy matching.
    print_graph_summary(threshold)
        Prints a summary of the graph's properties.

    """
    def __init__(self, csv_file):
        """
        Initialize the CocktailGraph and build the graph from a CSV file.

        Parameters
        ----------
        csv_file : str
            Path to the CSV file containing cocktail data.
        """
        # for i in range(3,10):
        self.threshold = 7
        self.cocktails = []
        self.graph = nx.Graph()
        self.load_cocktails(csv_file)
        self.build_graph()
        # self.print_graph_summary()

    def load_cocktails(self, file_path):
        """
        Load cocktail data from a CSV file.

        Parameters
        ----------
        file_path : str
            Path to the CSV file containing cocktail data.
        """
        df = pd.read_csv(file_path).fillna("None")
        column_names = list(df.columns)
        for _, row in df.iterrows():
            title = row[column_names[0]]
            glass = row[column_names[1]]
            garnish = row[column_names[2]]
            recipe = row[column_names[3]]
            ingredients = eval(row[column_names[5]])  # Convert string to list
            self.cocktails.append(Cocktail(title, glass, garnish, recipe, ingredients))

    def build_graph(self):
        """
        Build a graph of cocktails based on their similarity.
        """
        for cocktail in self.cocktails:
            self.graph.add_node(cocktail.name, data=cocktail)

        for i, cocktail1 in enumerate(self.cocktails):
            for j, cocktail2 in enumerate(self.cocktails):
                if i < j:
                    similarity = cocktail1.get_similarity(cocktail2)
                    if similarity >= self.threshold:  # Add edge only if similarity exists
                        self.graph.add_edge(cocktail1.name, cocktail2.name, weight= 1 / similarity)
                        # print(cocktail1.name, cocktail2.name, similarity)

    def find_shortest_path(self, cocktail1, cocktail2):
        """
        Find the shortest path between two cocktails.

        Parameters
        ----------
        cocktail1 : str
            Name of the starting cocktail.
        cocktail2 : str
            Name of the target cocktail.

        Returns
        -------
        list of str or None
            A list of cocktail names representing the shortest path, or None if 
            no path exists.
        """
        try:
            return nx.shortest_path(self.graph, source=cocktail1, target=cocktail2, weight='weight')
        except nx.NetworkXNoPath:
            return None
        
    def display_cocktail_difference(self, cocktail_names):
        
        cocktails = []
        for name in cocktail_names:
            if name in self.graph.nodes:
                cocktails.append(self.graph.nodes[name]['data'])
            else:
                print(f"Error: '{name}' not found in the graph.")
                return

        all_ingredients = set()
        all_techniques = set()
        cocktail_ingredients = []
        cocktail_techniques = []
        
        for cocktail in cocktails:
            # Extract ingredients as a dictionary {ingredient: amount}
            ingredients = {i[1]: i[0] for i in cocktail.ingredients}
            all_ingredients.update(ingredients.keys())
            cocktail_ingredients.append(ingredients)

            # Extract techniques
            techniques = set(cocktail.techniques)
            all_techniques.update(techniques)
            cocktail_techniques.append(techniques)

        all_ingredients = sorted(all_ingredients)
        all_techniques = sorted(all_techniques)

        # Table construction
        headers = ["Element"] + cocktail_names
        table = []

        table.append(["--- INGREDIENTS ---"] + [""] * len(cocktail_names))
        for ingredient in all_ingredients:
            row = [ingredient]
            for i, ingredients in enumerate(cocktail_ingredients):
                amount = ingredients.get(ingredient, "X")
                row.append(amount)
            table.append(row)

        table.append(["--- TECHNIQUES ---"] + [""] * len(cocktail_names))
        for technique in all_techniques:
            row = [technique]
            for i, techniques in enumerate(cocktail_techniques):
                status = technique if technique in techniques else "X"
                row.append(status)
            table.append(row)

        print(tabulate(table, headers=headers, tablefmt="grid"))

    def get_random_cocktail(self):
        """
        Return a random cocktail from the graph.

        Returns
        -------
        Cocktail
            A randomly selected Cocktail object.
        """
        return random.choice(self.cocktails)

    
    def cocktail_exists(self, cocktail_name):
        """
        Check if a cocktail exists in the graph.

        Parameters
        ----------
        cocktail_name : str
            The name of the cocktail to check.

        Returns
        -------
        bool
            True if the cocktail exists, False otherwise.
        """
        return cocktail_name in self.graph.nodes
    
    def fuzzy_search_cocktail(self, cocktail_name):
        """
        Search for close matches to a cocktail name using fuzzy matching.

        Parameters
        ----------
        cocktail_name : str
            The name of the cocktail to search for.

        Returns
        -------
        list of str
            A list of cocktail names that match the input name.
        """
        all_cocktail = list(self.graph.nodes)
        matches = difflib.get_close_matches(cocktail_name, all_cocktail, n=5, cutoff=0.6)
        return matches
    
    def print_graph_summary(self):
        """
        Print a summary of the graph properties.

        """
        print(f"Similarity threshold: {self.threshold}")
        print("Graph Summary:")
        print(f"Number of Nodes: {self.graph.number_of_nodes()}")
        print(f"Number of Edges: {self.graph.number_of_edges()}")
        print(f"Density: {nx.density(self.graph):.4f}")
        print(f"Number of Connected Components: {nx.number_connected_components(self.graph)}")
        print(f"Average Clustering Coefficient: {nx.average_clustering(self.graph):.4f}")
        degrees = dict(self.graph.degree())
        print(f"Average Node Degree: {sum(degrees.values()) / self.graph.number_of_nodes():.2f}")
        
