secret-santa
------------

### Run

    # Test the secret santa message.
    python message-tester.py -v TEXT_BELT_API_KEY NUMBER

    # Test the recipiants.
    python sms-tester.py -v TEXT_BELT_API_KEY example.config

    # Perform the actual secret santa selection and message the assignment.
    python secret-santa.py -v TEXT_BELT_API_KEY example.config --dry-run


### Setup

    # Python 3
    python3 -m venv p3
    source p3/bin/activate
    
    # Libraries (pypi)
    pip install requests
    
    # Libraries (custom)
    curl -LO https://github.com/sawatzkylindsey/pytils/archive/master.zip
    cd pytils-master/
    make install

