SHELL := /bin/bash

help:
    @echo "usage:"
    @echo "    make release -- push to the public pypi"
    @echo "    make release_private -- push to the incuna pypi"

release:
    python setup.py register -r pypi sdist upload -r pypi

release_private:
    python setup.py register -r incuna sdist upload -r incuna
