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
python3 -m run
```

The Flask server will be running on `http://127.0.0.1:5000`

### Requests

Run `curl -i 'http://localhost:5000/profiles/<profile>'` where `profile` is the Bitbucket team or Github organization
```
curl -i 'http://localhost:5000/profiles/mailchimp'
curl -i 'http://localhost:5000/profiles/pygame'
```

### Testing
Unit tests are written using `pytest` and can be found under `tests/`
To run these test just run `pytest` under the virtual environment.
The `test.py` script is the testing file used during development.
Run `python3 test.py --help` if you're interested in using this test script.

## What'd I'd like to improve on...
I'd like to add retry logic for handling network errors. Ideally there would be a set number of retries and if all of them fail, a standard response should be returned indicating failure.
This can probably be implemented using a decorator to make things simple.
I would also like to write unit tests for network failures to make sure the implementation works.
