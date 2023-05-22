import pandas as pd
from matplotlib import pyplot as plt
from itertools import product # cartesian product


def plot_total(species: pd.DataFrame, style = 'bmh') -> None:
    """
    Draws a summary chart of the Red List Categories
    """
    plt.style.use(style) # use a style of lines, colors, ...
    tmp = species.value_counts('redlistCategory', normalize = True)
    ### gather the smallest redlist categories 
    ### into the category "Extinct / Other Categories"
    gt_percentile = tmp[tmp>=0.01]
    gt_percentile['Extinct / Other Categories'] = tmp[tmp<0.01].sum()
    plt.figure()
    ### plots "donut" chart
    gt_percentile.plot.pie(title = 'IUCN Red List Categories', 
                           ylabel='', wedgeprops=dict(width=0.6))


def plot_all_classes(species: pd.DataFrame, style = 'bmh'):
    """
    Draws Red List Categories chart for each class
    """
    plt.style.use(style)

    sel = species[['className', 'redlistCategory']].copy()
    tmp = sel.value_counts('className')
    ### gather the smallest classes into the class "OTHERS"
    gt1300 = tmp[tmp>=1300]
    gt1300['OTHERS'] = tmp[tmp<1300].sum()
    sel.loc[~(sel['className'].isin(gt1300.index)), 'className'] = 'OTHERS'

    fig, axes = plt.subplots(2,3)
    plt.suptitle('CONSERVATION STATUS FOR EACH CLASS OF CHORDATA', size = 20, y=1)

    for cls, pos in zip(gt1300.index, product((0,1),(0,1,2))): # iterates over 6 classes and 6 positions
        tmp = sel.loc[sel['className'] == cls]
        tmp = tmp.value_counts('redlistCategory', normalize = True)
        ### gather the smallest redlist categories 
        ### into the category "Other Categories"
        gt_percentile = tmp[tmp>=0.01]
        gt_percentile['Other Categories'] = tmp[tmp<0.01].sum()
        ### plots a sub-chart at each iteration
        gt_percentile.plot.pie(title = cls, ylabel = '', ax = axes[*pos], 
                            figsize = (18, 10), fontsize = 7.5, 
                            labeldistance = 1.15, wedgeprops = dict(width=0.6))


def plot_class(species: pd.DataFrame, classname: str, style = 'bmh'):
    """
    Draws Red List Categories chart for a given class
    """
    plt.style.use(style)
    tmp = species.query(f"className == \'{classname}\'")
    ### from now implementation is the same as in plot_total()
    tmp = tmp.value_counts('redlistCategory', normalize = True)
    gt_percentile = tmp[tmp>=0.01]
    gt_percentile['Extinct / Other Categories'] = tmp[tmp<0.01].sum()
    plt.figure()
    gt_percentile.plot.pie(title = classname, 
                           ylabel='', wedgeprops=dict(width=0.6))
 

def classes_distribution(species: pd.DataFrame, style = 'bmh'):
    """
    Draws distribution of classes on a bar chart
    """
    plt.style.use(style)
    tmp = species.value_counts('className')
    plt.figure()
    fig = tmp.plot.bar(title = 'Distribution of chordata classes', xlabel='')
    fig.bar_label(fig.containers[0]) # writes the value above each bar
    fig.grid(axis = 'x') # shows only horizontal lines


# test library
if __name__ == "__main__":
    species = pd.read_csv("simple_summary.csv")
    plot_total(species)
    plot_all_classes(species)
    plot_class(species, 'AVES')
    classes_distribution(species)
    plt.show()