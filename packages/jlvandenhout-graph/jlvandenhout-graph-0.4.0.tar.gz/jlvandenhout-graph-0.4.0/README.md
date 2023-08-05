## Graph
This package provides a simple graph implementation for Python.

---
- [1. Installation](#1-installation)
  - [1.1. Using pip](#11-using-pip)
  - [1.2. From source](#12-from-source)
- [2. Basic usage](#2-basic-usage)
- [3. Support](#3-support)
- [4. Contributing](#4-contributing)
- [5. License](#5-license)
- [6. Changelog](#6-changelog)
---

### 1. Installation
#### 1.1. Using pip
Simply run the usual installation command for pip:

```
pip install jlvandenhout-graph
```

#### 1.2. From source
To install from the latest source code, clone this repository and install from the repository:

```
git clone https://gitlab.com/jlvandenhout/graph.git
cd graph
pip install .
```

### 2. Basic usage
```python
from jlvandenhout.graph import Graph

graph = Graph()
graph.nodes.add("Alice")
graph.edges.update("Bob", "Alice", 42)
graph.edges.update("Alice", "Charlie", 20)

for node in graph.nodes:
    print("name:", node)
    print("  from:", ", ".join(graph.nodes.preceding(node)))
    print("  to:", ", ".join(graph.nodes.succeeding(node)))

print("\nChecking balances...")
for node in graph.nodes:
    balance = 0
    for edge in graph.edges.preceding(node):
        balance += edge.value
    for edge in graph.edges.succeeding(node):
        balance -= edge.value
    print("name:", node)
    print("  balance:", balance)

print("\nRemoving Charlie from history...")
graph.nodes.remove("Charlie")

print("names:", ", ".join(graph.nodes))
print("transactions:", ", ".join(f"From {f} to {t}" for f, t in graph.edges))
```

### 3. Support
If you have any questions, suggestions or found a bug, please open an issue in [the issue tracker](https://gitlab.com/jlvandenhout/graph/issues).

### 4. Contributing
Refer to [CONTRIBUTING](https://gitlab.com/jlvandenhout/graph/blob/master/CONTRIBUTING.md).

### 5. License
Refer to [GNU General Public License v3 (GPLv3)](https://choosealicense.com/licenses/gpl-3.0/).

### 6. Changelog
Refer to [CHANGELOG](https://gitlab.com/jlvandenhout/graph/blob/master/CHANGELOG.md).