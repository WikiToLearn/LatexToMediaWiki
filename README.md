# LatexToMediaWiki
Latex to MediaWiki Markup Converter

This python script converts Latex documents into MediaWiki wiki-text format.
It runs on Python 2.7.x ans uses PlasTeX lib (https://github.com/tiarno/plastex)

##### Installation #####
* Add the dir that contains LatexToMediaWiki sources to your PYTHONPATH environment variable.
* Init submodules (plastex) with 'git submodule init && git submodule update'
* Enter plastex dir
* Install plastex on your system with 'python setup.py install'

##### Configuration #####
You can configure l2mw behaviour through a 'configs.txt' file. 
You can find a documented example in 'configs_example.txt'.

##### Execution #####
To run l2mw just execute 'l2mw.py' script with configs inside a 'configs.txt' file in the same working dir.

##### HELP!! #####
For every kind of question please contact Valsdav at <valsdav@wikitolearn.org>
