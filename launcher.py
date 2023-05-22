'''
FILE NAME:  launcher.py
LAST EDIT:  24/04/2023
AUTHOR:     Giovanni Zedda
DESCRIPTION:    control panel of the entire software
                related to IUCN_redlist_analysis.ipynb
CHANGELOG:
'''

import pandas as pd
import matplotlib.pyplot as plt
import sys
from time import time
from trees import TaxonTree
from animals import Animal
from menu import Menu

import explore, charts, downloader



if sys.version_info.major < 3 or sys.version_info.minor < 10:
    raise SyntaxError(f"Python version running: {sys.version}\n"
                      f"Python 3.10 or newer is required")

def search(animal: Animal):
    search_options = [('1', 'View on the website', explore.watch_online),
                      ('2', 'View full information offline', explore.watch_offline),
                      ('3', 'Download image', downloader.download),
                      ('X', 'Back to the main menu', lambda x: None)]
    search_menu = Menu('SEARCH MENU', search_options)

    print(f"\n{animal}")
    choice = ''
    while choice != 'X' and animal.is_listed:
        search_menu.print()
        choice = input("Choose action: ").upper()
        search_menu.execute(choice, animal)

    choice = '' # setting choice back to void character in order not to quit main()


def graphics():
    def plot_a_class(species: pd.DataFrame):
        classes = set(species['className']) # set of all available classes
        print(*classes, sep = ', ')
        class_to_plot = input("Digit a class to be plotted: ").upper()
        if class_to_plot not in classes:
            print('Non-listed class. Retry.')
        else:
            charts.plot_class(species, class_to_plot) 

    graphics_options = [('1', 'Show a summary chart of the Red List Categories', charts.plot_total),
                       ('2', 'Show distribution of classes', charts.classes_distribution),
                       ('3', 'Show Red List Categories per class', charts.plot_all_classes),
                       ('4', 'Show Red List Categories for a given class', plot_a_class),
                       ('X', 'Back to the main menu', lambda x: None)]
    graphics_menu = Menu('GRAPHICS MENU', graphics_options)

    choice = ''
    while choice != 'X':
        graphics_menu.print()    
        choice = input("Choose action: ").upper()
        graphics_menu.execute(choice, Animal.species)       

    choice = '' # setting choice back to void character in order not to quit main()


def print_tree(species: pd.DataFrame, filename = 'taxonomic-tree.txt', verbose = True) -> bool:
    if verbose:
        print('Wait a few seconds...')
    try:
        tree = TaxonTree('Animal')
        start = time()
        tree.add_animals(species)
        with open(filename, 'w') as output:
            output.write(str(tree))
        end = time()
        if verbose:
            print(f"Taxonomic tree successfully saved as '{filename}' in {end-start:.2f}s")
        return True # positive exit-status
    except: 
        if verbose:
            print('Failed attempt to save the taxonomic tree')
        return False # negative exit-status


def main():
    main_options = [('1', 'Find animal', search),
                    ('2', 'Show data graphics', graphics),
                    ('3', 'Save taxonomic tree into a txt file', print_tree),
                    ('X', 'Exit', lambda x: None)]
    main_menu = Menu('MAIN MENU', main_options)
    choice = ''
    while choice != 'X':
        main_menu.print()
        choice = input("Choose action: ").upper()
        plt.ion() # interactive: on. 
        # It allows to keep all matplotlib windows open without any pausing

        if choice == '1':
            animal = Animal(input('Enter common or scientific name: '))
            main_menu.execute('1', animal)
        if choice == '2':
            main_menu.execute('2')
        if choice == '3':
            main_menu.execute('3', Animal.species)


if __name__ == '__main__':
    Animal.species = pd.read_csv("simple_summary.csv")
    Animal.names = pd.read_csv("common_names.csv")
    Animal.assessments = pd.read_csv("assessments.csv", index_col = 'assessmentId')
    main()