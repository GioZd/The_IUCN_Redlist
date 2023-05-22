from animals import Animal
import pandas as pd

class BSTree:
    """
    Binary Search Tree implemented like in
    'Data Structures and Algorithms with Python'
    by Kent D. Lee and Steve Hubbard
    with slight differences in the __getitem__ method
    """
    # This is a Node class that is internal to the BinarySearchTree class. 
    class Node:
        def __init__(self,val,left=None,right=None):
            self.val = val
            self.left = left
            self.right = right
            
        def __iter__(self):  ## IN-ORDER VISIT ##
            if self.left is not None:
                for elem in self.left: yield elem # LEFT            
            yield self.val # ITEM            
            if self.right is not None:
                for elem in self.right: yield elem # RIGHT
            
    # CONSTRUCTOR #
    def __init__(self, root=None):
        self.root = root

    def insert(self, val):        
        # internal recursive function
        def __insert(node):
            if node is None: 
                return BSTree.Node(val)
            if val < node.val: 
                node.left  = __insert(node.left)
            else:              
                node.right = __insert(node.right)
            return node
        self.root = __insert(self.root)
    
    def __binsearch(node, val):
        if node is None: 
            return None
        try:
            if node.val == val:
                return node
            elif val < node.val:
                return BSTree.__binsearch(node.left, val)
            elif val > node.val:
                return BSTree.__binsearch(node.right, val)
        except TypeError:
            print('WARNING: I can not compare: ',type(val),' with',type(node.val))
            return None
        return None

    def __contains__(self, val): # called by 'in' in O(logN)
        return BSTree.__binsearch(self.root, val) is not None            

    def __getitem__(self, key):
        item = BSTree.__binsearch(self.root, key)
        if item: # no KeyError raised
            return item.val

    def __iter__(self):
        if self.root is not None:
            return iter(self.root)
        else:
            return iter([])

    def __str__(self):
        return str(list(self))


class Tree:
    def __init__(self, value: str, parent = None):
        self.parent: Tree | None = parent
        self.value: str = value
        self.children: BSTree[Tree] = BSTree() # keeps the children ordered (alphabetically)

    def depth(self) -> int:
        """
        Returns
        -------
        int
            The depth of a Tree(node), namely
            how many ancestors we can find
            i.g.
            Charles III (depth: 0)
                William (depth: 1)
                    George (depth: 2)
                    Charlotte (depth: 2)
                    Louis (depth: 2)
                Henry (depth: 1)
                    Archie (depth: 2)
                    Lilibet (depth: 2)
        """
        if self.parent is None:
            return 0
        return 1 + self.parent.depth() # recursive call
    
    def __lt__(self, other) -> bool: # tree < other_tree
        return self.value.lower() < other.value.lower()
    
    def __gt__(self, other) -> bool: # tree > other_tree
        return self.value.lower() > other.value.lower()
    
    def __eq__(self, other) -> bool: # tree == other_tree
        return self.value.lower() == other.value.lower()

    def add_brench(self, new_brench) -> bool:
        if not isinstance(new_brench, Tree): # new_brench must be a Tree object
            new_brench = Tree(new_brench)

        if new_brench not in self.children: # binary search
            new_brench.parent = self
            self.children.insert(new_brench)
            return True
        return False

    def __str__(self) -> str:
        # pre-order visit
        texttree = f"{'  '*self.depth()}{self.value}\n" # visit root
        for child in self.children:
            texttree += str(child) # recursive call on each child
        return texttree

    def __getitem__(self, key):
        return self.children[key]

    def print(self): # pre-order visit and print
        print(self)


class TaxonTree(Tree):
    """
    TaxonTree inherits most properties from the class Tree,
    but contains methods more specific to save a set of animals
    """
    def __init__(self, highest_taxon):
        super().__init__(highest_taxon) # inheritance from Tree

    def add_animal(self, animal: Animal | pd.Series):
        """
        Appends an animal to the TaxonTree

        Parameters
        ----------
        animal: Animal | pd.Series
            can be an instance of Animal, or a row from a DataFrame      
        """

        taxonomic_levels = ()
        if isinstance(animal, Animal): # taxonomic_levels when animal is an Animal object
            taxonomic_levels = (
                animal.phylum,
                animal.classis,
                animal.order,
                animal.family,
                animal.genus,
                animal.name
            )

        if isinstance(animal, pd.Series): # taxonomic_levels when animal is a DataFrame row
            taxonomic_levels = (
                animal['phylumName'],
                animal['className'],
                animal['orderName'],
                animal['familyName'],
                animal['genusName'],
                animal['scientificName']
            )


        hierarchical_level = self # tmp variable to contain itself, its child, its grandchild and so on
        for taxon in taxonomic_levels:
            if Tree(taxon) not in hierarchical_level.children: # does not allow duplicates
                hierarchical_level.add_brench(taxon)
            hierarchical_level = hierarchical_level[Tree(taxon)]

    def add_animals(self, species: pd.DataFrame):
        """
        Appends multiple animals to the TaxonTree.

        Parameters
        ----------
        species: pd.DataFrame
            A DataFrame structured like 'simple_summary.csv'
        
        Notes
        -----
        For a large DataFrame it is not recommended to 
        instantiate an Animal object every time because 
        it takes a much longer time overall
        """
        for key, row in species.iterrows(): # iterates over the DataFrame's rows
            # animal = Animal(s['scientificName'])
            # self.add_animal(animal)
            self.add_animal(row) 

# test library
if __name__ == '__main__':
    Animal.species = pd.read_csv("simple_summary.csv")
    Animal.names = pd.read_csv("common_names.csv")
    taxonomic_tree = TaxonTree('ANIMALIA')
    taxonomic_tree.add_animals(Animal.species.head(5))
    taxonomic_tree.add_animal(Animal('Platypus'))
    taxonomic_tree.print()