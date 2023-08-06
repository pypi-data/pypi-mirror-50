python -m pip uninstall fdr
python -m pip uninstall rtm
python setup.py sdist bdist_wheel
python -m pip install -e .