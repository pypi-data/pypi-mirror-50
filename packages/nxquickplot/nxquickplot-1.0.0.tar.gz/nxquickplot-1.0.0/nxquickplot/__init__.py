name = 'nxquickplot'

import networkx
import matplotlib.pyplot as plt
from distutils.version import StrictVersion

def plot_force(g):
    plt.clf()
    networkx.draw_networkx(g, pos=networkx.kamada_kawai_layout(g))
    plt.show()

def plot_random_deterministic(g):
    plt.clf()

    if StrictVersion(networkx.__version__) > StrictVersion('2.1'):
        networkx.draw_networkx(g, pos=networkx.random_layout(g, seed=0))
    else:
        networkx.draw_networkx(g, pos=networkx.random_layout(g, random_state=0))

    plt.show()

def plot_with_attr(g, attr):
    plt.clf()
    labels = networkx.get_node_attributes(g, attr)
    networkx.draw_networkx(g, labels=labels, pos=networkx.kamada_kawai_layout(g))
    plt.show()   
