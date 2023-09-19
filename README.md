# secstructartist

This package allows to include pretty secondary structure schemes in 
matplotlib plots.

![example_rmsf.png](https://github.com/bickeld/secstructartist/blob/main/examples/example_rmsf.png)

## Table of content

* [Installation](#installation)
    * [Prerequisites](#prerequisites)
    * [Installation from PyPI](#installation-from-pypi)
    * [installation-from-github](#installation-from-github)
* [Usage](#usage)
    * [A simple example](#a-simple-example)
    * [Customizing your plots](#customizing-your-plots)
* [License](#license)
* [Contributing](#contributing)
* [Authors](#authors)

## Installation

### Prerequisites

* **General prerequisites:**
    * Python 3.8 or higher
    * pip
* **Third-party python packages:**
    * matplotlib
    * numpy

### Installation from PyPI

This is the recommended way to install the package.

1. Create a virtual environment (optional but recommended):
    ```
    python3 -m venv secstructartist
    source secstructartist/bin/activate
    ```

2. Install python module
    ```
    pip install secstructartist
    ```

### Installation from GitHub

Here, you will download the repository, and manually build and install the
package.

1. Create a virtual environment (optional but recommended):
    ```
    python3 -m venv secstructartist
    source secstructartist/bin/activate
    ```

2. Clone the repository:
    ```
    git clone https://github.com/bickeld/secstructartist.git
    cd secstructartist
    ```

3. Build package and install
    ```
    make build
    make install
    ```

## Usage

In the `examples/` directory there is a Jupyter notebook ([link](https://github.com/bickeld/secstructartist/blob/main/examples/examples.ipynb))
with plenty of code examples for simple and advanced use cases. Therefore, only 
the  basics usage will be shown here.

### A simple example

The simplest possible use case:

```python
import matplotlib.pyplot as plt
import secstructartist as ssa

secstruct_str = "LLLSSSSSLLLLLHHHHHHHHLLLHHHHHHHHLLLLLLLLLSSSSSSLLLL"
fig, _objs = ssa.draw(secstruct_str)
fig.savefig("example0.png")
```

![example0.png](https://github.com/bickeld/secstructartist/blob/main/examples/example0.png)

### Customizing your plots

Plots can be modified by initializing a custom `SecStructArtist`.

```python
import matplotlib.pyplot as plt
import secstructartist as ssa

secstruct_str = "LLLSSSSSLLLLLHHHHHHHHLLLHHHHHHHHLLLLLLLLLSSSSSSLLLL"
nres = len(secstruct_str)

# Initialize a custom SecStructArtist istance to modify settings 
artist = ssa.SecStructArtist()
# Set global settings
artist.height = .7
artist.linewidth = .8
# Set settings of "H" - Helices
artist["H"].fillcolor = (.9, 0., 0.)
artist["H"].shadecolor = (.7, 0., 0.)
artist["H"].ribbon_period = 3.6
artist["H"].ribbon_width = 2.2
# Set settings of "S" - beta-Sheets
artist["S"].arrow_length = 2.7
artist["S"].fillcolor = "#ddcc00"
artist["S"].height = .5
# Set settings of "L" - loop
artist["L"].linecolor = "blue"
artist["L"].linewidth = 1.8

# Generate figure and axis
fig, ax = plt.subplots(figsize=(4,.4), dpi=150)

# Include secondary structure scheme above the plot
artist.draw(secstruct_str, xpos=list(range(3, 3+nres)), ypos=3.5, ax=ax)

ax.set_xlabel("Residue index")
ax.set_ylim([3, 4])

fig.savefig("example1.png")
```

![example1.png](https://github.com/bickeld/secstructartist/blob/main/examples/example1.png)

## License

Distributed under the GNU General Public License v3 (GPLv3) License.

## Contributing

If you find a bug :bug:, please open a [bug report](https://github.com/bickeld/secstructartist/issues/new?labels=bug).
If you have an idea for an improvement or new feature :rocket:, please open a [feature request](https://github.com/bickeld/secstructartist/issues/new?labels=enhancement).

## Authors

[![ORCID](https://orcid.org/sites/default/files/images/orcid_16x16.png)](https://orcid.org/0000-0003-0332-8338) - David Bickel
