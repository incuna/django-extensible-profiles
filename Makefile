SHELL := /bin/bash

help:
    @echo "usage:"
    @echo "    make release -- push to the incuna pypi"
    @echo "    make release_public -- push to the public pypi"

release:
    python setup.py register -r incuna sdist upload -r incuna

release_public:
    python setup.py register -r pypi sdist upload -r pypi
