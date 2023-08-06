:: First, delete the dist directory
python setup.py sdist bdist_wheel
twine upload dist/*

python -m pip install --upgrade fdr

