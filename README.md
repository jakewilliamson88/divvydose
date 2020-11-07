# DivvyDOSE Coding Challenge

## Installation

```
git clone https://github.com/jakewilliamson88/divvydose.git
cd divvydose
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the code

### Start the service
```

python3 -m run.py
```

The Flask server will be running on `http://127.0.0.1:5000`

### Requests:

```
curl -i 'http://localhost:5000/health-check'
curl -i 'http://localhost:5000/profiles/mailchimp'
curl -i 'http://localhost:5000/profiles/pygame'
```

### Testing
Unit tests are written using `pytest` and can be found under `tests/`
The `test.py` script is the testing file used during development.
Run `python3 test.py --help` if you're interested in using this test script.
