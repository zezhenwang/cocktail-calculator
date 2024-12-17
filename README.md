### **README: Cocktail Calculator**

#### **Project Overview**

The **Cocktail Calculator** allows users to explore relationships between cocktails based on their ingredients and preparation techniques. By representing cocktails as nodes in a graph and their similarities as edges, this program enables interactive analysis, search, and comparison of cocktail recipes.

------

#### **User Interactions**

1. **Random Cocktail**
   - **Prompt**: None (called directly).
   - **Output**: Displays a randomly selected cocktail, including its name, glass type, garnish, ingredients, and recipe.
2. **Search for a Cocktail**
   - **Prompt**: Enter the name of a cocktail.
   - Responses:
     - If an exact match is found, the cocktail details are displayed.
     - If not, the program suggests similar names using fuzzy matching (e.g., *"Did you mean: 1.Mojito 2.Mimosa"*).
     - If no close matches are found, the user is informed to try a different name.
3. **Find Shortest Path Between Cocktails**
   - **Prompt**: Enter two cocktail names.
   - Responses:
     - The shortest path is computed using how similar the ingredients and mixing techniques used are. Two cocktails are considered "similar" if they share around 2 ingredients and 1 technique.
     - If a path exists, the shortest path is displayed (e.g., *"Mojito -> Daiquiri -> Margarita"*), along with a table comparing their ingredients and techniques.
     - If no path exists, the user is notified, and prompted for a different option.
4. **Compare Multiple Cocktails**
   - **Prompt**: Provide a list of cocktail names.
   - **Response**: Displays a comparison table highlighting shared and missing ingredients/techniques across the specified cocktails.
5. **Graph Summary**
   - **Prompt**: None (called directly).
   - **Output**: Outputs key graph statistics, including the number of nodes, edges, density, and clustering information.

------

#### **How the Graph is Organized**

- **Nodes**: Each node represents a cocktail.

- **Edges**: Edges are created between cocktails based on a 

  similarity score:

  - Shared ingredients (weighted as 3 points each).
  - Shared preparation techniques (1 point each).
  - The weight of each edge is calculated as `1 / similarity_score` to ensure that more similar cocktails are "closer" in the graph.

------

#### **Dependencies**

To run this program, ensure the following Python packages are installed:

- `pandas` (for reading and parsing data)
- `networkx` (for building network and analyzing)
- `tabulate` (for displaying comparison of cocktails)

------

#### **Running the Program**

1. Load the program with the cocktail CSV file.
2. Follow the prompt of the main function.