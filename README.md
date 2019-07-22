# simplestocks

A fun toy stock exchange with some basic functionality for trading stocks. 

## Installation

1. Clone the repo
2. Set up a python3 virtualenv (written and tested in 3.6)
3. If you want to use the CLI, you'll need to `pip install -r requirements/cli-requirements.txt`

## Using the Exchange

### CLI
You can access the exchange from the command line using `python cli.py` as long as you've
installed the requirements file.

### Python Shell
You can use the Exchange directly from the python shell if you `from exchange import ExchangeBuilder`. 
Then `exchange = ExchangeBuilder.build()` to get a usable exchange object with some stocks loaded. 

## Running tests
Tests should be picked up automatically just by running: `python -m unittest` 

Otherwise they can by run individually from the command line. 
