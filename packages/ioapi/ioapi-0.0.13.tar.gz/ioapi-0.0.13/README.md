# ioexplorer-graphql-client
<p align="center">
<a href="https://circleci.com/gh/MSKCC-IPOP/ioexplorer-graphql-client"><img src="https://circleci.com/gh/MSKCC-IPOP/ioexplorer-graphql-client.svg?style=svg&circle-token=f3de460dff1dc04adbc426eaeed5e256d8b73a77"></a>
<a href="https://github.com/MSKCC-IPOP/ioexplorer-graphql-client"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<img alt="Pylint: 10" src=https://mperlet.github.io/pybadge/badges/10.svg>
</p>

Client for the IOExplorer API.

This is a Python module hosted in PyPi under the name [`ioapi`](https://pypi.org/project/ioapi/). It is auto-generated using [quiz](https://quiz.readthedocs.io/en/latest/), and should be re-built every time the functionality of the [`ioexplorer-graphql-server`](https://github.com/MSKCC-IPOP/ioexplorer-graphql-server) is updated. To re-build, follow these steps:

```
# 1. Make sure https://github.com/rmarren1/quiz is installed locally.
# This is a fork of https://github.com/ariebovenberg/quiz with some custom patching added.
# In the future, should be able to use the most recent version of `quiz`.
mkvirtualenv re-build-ioapi
git clone https://github.com/rmarren1/quiz
pip install ./quiz
rm -rf quiz

# 2. Update ioapi/schema.json
make build

# 3. Bump the version
vim setup.py  # Change the version argument

# 4. Re-build the module
python setup.py sdist

# 5. Upload the new version
twine upload dist/ioapi-<version>.tar.gz

# 6. Commit changes to github
git add -A
git commit -m 'release version <version>'
git tag v<version>
git push
git push --tags
```
