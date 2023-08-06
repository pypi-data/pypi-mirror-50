# Jupyter Bindings

Integrate MLVis packages to Jupyter notebook.

## Installation

##### Javascript

```
cd js-lib
yarn
yarn run build
```

##### Python

Currently requires python 3, it can be managed via tools such as pyenv.
It is recommended to first start a virtual environment in the project folder:

```
python -m venv venv
source venv/bin/activate
```

Install python dependencies:

```
cd mlvis
pip install -r requirements.txt
```

To run the code directly under this directory, the Jupyter nbextension needs to be installed in this local environment:

```
python setup.py develop
```

To build the package into the example directly, please use the following command:

```
python setup.py sdist bdist_wheel
mv dist ../../examples/jupyter/
```

## Run

Start the Jupyter Notebook directly under this directory:

```
jupyter notebook
```

If the package has been built into the example folder, go to _mlvis-toolkit/examples/jupyter_, and perform the following stepts:

1. start a virtual environment
2. run `pip install -r requirements.txt`
3. run `pip install ./dist/mlvis-[version].tar.gz`
4. execute `jupyter notebook` there.
