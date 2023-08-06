# onlaw_api_client

python client for api.onlaw.dk

# installation

## std usage

simply
`pip install onlaw_api_client`

For a minimal example see `examples/query.py`

## development

- clone the repo : `git clone https://github.com/Onlaw/onlaw_api_client.git`
- venv: `python3 -m venv venv`
- activate: `source venv/bin/activate`
- install: `pip install -r requirements.dev.txt`
- install onlaw api client from local source: `pip install -e .`
- install pre-commit hooks: `pre-commit install`

### new dependencies

- Add them to `setup.py` in `install_requires`.
- To generate a new `requirements.txt`: `pip-compile`

### testing package

- build package (remember if neccesary to change version in `setup.py`): `make pypitest`
- create new venv and activate it, and install package: `pip install --index-url https://test.pypi.org/simple/ onlaw_api_client --upgrade --extra-index-url https://test.pypi.org/simple/ --no-deps`. Note the `--no-deps` arguments which prevent dependencies to be installed. test.pypi does not have all packages and hence installation from test.pypi most likely fail.
