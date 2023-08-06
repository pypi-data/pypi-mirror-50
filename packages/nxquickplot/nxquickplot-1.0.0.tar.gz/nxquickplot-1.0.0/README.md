# nxquickplot

Convenient plotting for graphs in NetworkX.  These functions are rather
asymmetric/non-composable because they aim to literally capture concrete use
patterns rather than abstracting over them.  If you need other stuff, just use
the raw `draw_networkx` API.

## API

### Draw the graph with a force-directed layout

```
from nxquickplot import plot_force
import networkx

g = networkx.DiGraph()

g.add_node('Alice')
g.add_node('Bob')
g.add_edge('Alice', 'Bob')

plot_force(g)
```


### Draw the graph with a random deterministic layout

```
from nxquickplot import plot_random_deterministic
import networkx

g = networkx.DiGraph()

g.add_node('Alice')
g.add_node('Bob')
g.add_edge('Alice', 'Bob')

plot_random_deterministic(g)
```

### Draw the graph plotting a certain attribute rather than the node ID

```
from nxquickplot import plot_with_attr
import networkx

g = networkx.DiGraph()

g.add_node('Alice', age=42)
g.add_node('Bob', age=31)
g.add_edge('Alice', 'Bob')

plot_with_attr(g, 'age')
```

This must be force directed.
