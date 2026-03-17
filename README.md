# secstructartist

This package allows to include pretty secondary structure schemes in 
matplotlib plots.

![plddt_plot.png](_dev/images/plddt_plot.png)


## Table of content

* [Installation](#installation)
    * [Prerequisites](#prerequisites)
    * [Installation from PyPI](#installation-from-pypi)
    * [Installation from GitHub](#installation-from-github)
* [Usage](#usage)
    * [A simple example](#a-simple-example)
    * [Additional styles](#additional-styles)
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

```shell
# 1. Create a virtual environment (optional but recommended)
python3 -m venv secstructartist
source secstructartist/bin/activate

# 2. Install the Python module
pip install secstructartist
```

### Installation from GitHub

Here, you will download the repository, and manually build and install the
package.

```shell
# 1. Create a virtual environment (optional but recommended)
python3 -m venv secstructartist
source secstructartist/bin/activate

# 2. Clone the repository
git clone https://github.com/bickeld/secstructartist.git
cd secstructartist

# 3. Install the package
make install

# 4. Test installation (optional)
make test
```

## Usage

In the `examples/` directory there are 
[Jupyter notebooks](https://github.com/bickeld/secstructartist/blob/main/examples/example_plots.ipynb) 
with plenty of code examples on how for simple and advanced use cases. 
Therefore, only the basic usage will be covered here.

### A simple example

```python
import secstructartist as ssa

secstruct_str = (
    'LLHHHHHHHHHHHHHHHHHHLLLLLLLLLLLLLLLLLLLLHHHHHHHLSSSSSSSSSSLL'
    'LLSSSSSSSSLLLLSSSSSSLLLLLHHHHHHLLLLLSSSLLLLLLLLSSSHHHHHHHHHH'
    'HHHHHHHHHHHHHHHLLLSSSSSSSHHHHHHHHHHHHHHHLLLLLSSSSSSLLLLLL'
)

ssa.draw_secondary_structure(secstruct_str)
```

![simple_example.png](_dev/images/simple_example.png)


### Additional styles

The module comes with a couple of preset styles to choose from. These preset 
styles come in two categories: 
- **HSL style** only use three secondary structure class (Helix, Sheet, Loop) as shown in the example above.
- **DSSP styles** on the other hand can parse the eight secondary structure classes returned by programs like DSSP or STRIDE.

Moreover, users are free to define their own styles, and save them as custom configuration styles
for later use. For examples in how to create custom styles, check this [Jupyter notebook](https://github.com/bickeld/secstructartist/blob/main/examples/example_artistdef.ipynb).

![styles_overview.png](_dev/images/styles_overview.png)


## License

Distributed under the GNU General Public License v3 (GPLv3) License.


## Contributing

If you find a bug, please open a [bug report](https://github.com/bickeld/secstructartist/issues/new?labels=bug).
If you have an idea for an improvement or new feature, please open a [feature request](https://github.com/bickeld/secstructartist/issues/new?labels=enhancement).


## Authors

[![ORCHiD](https://orcid.org/sites/default/files/images/orcid_16x16.png)](https://orcid.org/0000-0003-0332-8338) - David Bickel
