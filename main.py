from DataStructure import CocktailGraph

def print_random_cocktail(graph):
    """
    Display a random cocktail from the given graph.

    Retrieves a random cocktail and displays it via built in method.

    Parameters
    ----------
    graph : object
            An CocktailGraph object that holds the information of a graph.
    """
    cocktail = graph.get_random_cocktail()
    cocktail.print_cocktail()

def search_cocktail(graph, cocktail_name):
    '''
    Search for a cocktail by name in the given graph.

    If the exact cocktail name is found in the graph, its details are displayed 
    using the built in method. If not, close matches are suggested using 
    a fuzzy search.

    Parameters
    ----------
    graph : object
        An CocktailGraph object that holds the information of a graph.
    cocktail_name : str
        The name of the cocktail to search for.
    '''
    if cocktail_name in graph.graph.nodes:
        cocktail = graph.graph.nodes[cocktail_name]['data']
        cocktail.print_cocktail()
    else:
        print(f"\nError: Cocktail '{cocktail_name}' not found in the graph. Searching for close matches...")
        matches = graph.fuzzy_search_cocktail(cocktail_name)

        if not matches:
            print(f"\nNo close matches found for '{cocktail_name}'. Please try a different name.")
            return
        
        print(f"\nBy '{cocktail_name}', did you mean:")
        for i, match in enumerate(matches, 1):
            print(f"{i}. {match}")


def find_shortest_path(graph, cocktail1, cocktail2):
    """
    Find and display the shortest path between two cocktails.

    Retrieves the shortest path between `cocktail1` and `cocktail2` from the graph. 
    If a path exists, it is displayed along with a comparison of cocktails on the path.

    Parameters
    ----------
    graph : object
        An CocktailGraph object that holds the information of the cocktail graph.
    cocktail1 : str
        The starting cocktail name.
    cocktail2 : str
        The ending cocktail name.

    """
    path = graph.find_shortest_path(cocktail1, cocktail2)
    if path:
        print(f"\nShortest path from '{cocktail1}' to '{cocktail2}': {' -> '.join(path)}")
        graph.display_cocktail_difference(path)
    else:
        print(f"\nNo path exists between '{cocktail1}' and '{cocktail2}'.")


def main():
    '''Main Function that controls user input/output'''

    print("Welcome to the Cocktail Calculator!")
    print("Loading Cocktails...")
    graph = CocktailGraph('cocktail.csv')
    
    while True:
        print("\nChoose an option:")
        print("0. Search a cocktail")
        print("1. View a random cocktail")
        print("2. Compare two cocktails")
        print("3. Find the shortest path between two cocktails")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '0':
            c0 = input("Enter the name of the cocktail to search: ")
            search_cocktail(graph, c0)
        elif choice == '1':
            print_random_cocktail(graph)
        elif choice == '2':
            c1 = input("Enter the first cocktail name: ")
            if not graph.cocktail_exists(c1):
                print("Invalid cocktail. Please try again.")
                continue
            c2 = input("Enter the second cocktail name: ")
            if not graph.cocktail_exists(c2):
                print("Invalid cocktail. Please try again.")
                continue
            print(f"\nSimilarity between {c1} and {c2}: {graph.graph.nodes[c1]['data'].get_similarity(graph.graph.nodes[c2]['data'])}")
            graph.display_cocktail_difference([c1, c2])
            
        elif choice == '3':
            c1 = input("Enter the origin cocktail name: ")
            if not graph.cocktail_exists(c1):
                print("Invalid cocktail. Please try again.")
                continue
            c2 = input("Enter the target cocktail name: ")
            if not graph.cocktail_exists(c2):
                print("Invalid cocktail. Please try again.")
                continue
            find_shortest_path(graph, c1, c2)
        elif choice == '4':
            print("Exiting. Cheers!")
            break
        elif choice == 'debug':
            graph.print_graph_summary()
        elif choice == 'advanced_debugging':
            input_content = eval(input("please input commands: "))
            input_content
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()


# print(graph.graph.nodes["Woodside"]['data'].get_similarity(graph.graph.nodes["Alfonso Martini"]['data']))