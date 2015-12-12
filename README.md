EpiPy
========
A python package for epidemiology. Epipy is a Python package for epidemiology.
It contains tools for analyzing and visualizing epidemiology data.
Epipy can currently produce:

* stratified summary statistics
* case tree and checkerboard plots
* epicurves
* analysis of case attribute (e.g. sex) by generation
* 2x2 tables with odds ratio and relative risk
* summary of cluster basic reproduction numbers

Installation
------------
Install using pip:

    pip install epipy
    
Or clone the repository and install using setup.py:

    git clone https://github.com/cmrivers/epipy.git
    cd ./epipy
    pip install -r requirements.txt
    python setup.py install

EpiPy is in development. Please feel free to contribute.
Contact me at caitlin.rivers@gmail.com or [@cmyeaton](http://twitter.com/cmyeaton) with any questions.

Contributing/Development
------------
If you want to contribute in this great project. First fork this repo in github.

Clone your forked repo in your terminal using the appropriate command:

    git clone https://github.com/your-git-user-name/epipy.git
    cd ./epipy

Add this repo as upstream remote:

    git remote add upstream git@github.com:cmrivers/epipy.git

We use [gitflow](https://github.com/nvie/gitflow). Follow this [instructions](https://github.com/nvie/gitflow/wiki/Installation) to install.

    git branch master origin/master
    git flow init -d
    git flow feature start <your feature>

For install the tools for TDD use:
    
    pip install -r requirements.txt
    pip install -r requirements-tdd.txt

To run the test suit use:

    cd ./epipy
    py.test test

Then, do work and commit your changes. After finish your feature with coverage of test, please pull any change that ocurred from the upstream repo. You can use:

    git pull upstream master

If git fast-forward error is issue then use:

    git rebase upstream/master

Resolve the merge conflicts that couid exist using:

    git mergetool
    git rebase --continue

After everything is ok then:

    git flow feature publish <your feature>

When done, open a pull request to your feature branch.


Documentation
------------
The docs live at: [cmrivers.github.io/epipy](https://cmrivers.github.io/epipy)
