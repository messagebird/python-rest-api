MessageBird's REST API for Python
=================================
This repository contains the open source Python client for MessageBird's REST API. Documentation can be found at: https://www.messagebird.com/developers/python.

Requirements
------------
- [Sign up](https://www.messagebird.com/en/signup) for a free MessageBird account
- Create a new access key in the developers sections
- An application written in Python (tested with Python 2.7 and Python 3.4)

Installation
------------
The easiest way to use the MessageBird API in your Python project is to install it using the setup.py file:

```
$ sudo python setup.py install
```

Examples
--------
We have put some self-explanatory examples in the [examples](https://github.com/messagebird/python-rest-api/tree/master/examples) directory, but here is a quick example on how to get started. Assuming the installation was successful, you can import the messagebird package like this:

```python
import messagebird
```

Then, create an instance of **messagebird.Client**:

```python
client = messagebird.Client('test_gshuPaZoeEG6ovbc8M79w0QyM')
```

Now you can query the API for information or send a request. For example, if we want to request our balance information you'd do something like this:

```python
try:
  # Fetch the Balance object.
  balance = client.balance()

  # Print the object information.
  print('\nThe following information was returned as a Balance object:\n')
  print('  amount  : %d' % balance.amount)
  print('  type    : %s' % balance.type)
  print('  payment : %s\n' % balance.payment)

except messagebird.client.ErrorException as e:
  print('\nAn error occured while requesting a Balance object:\n')

  for error in e.errors:
    print('  code        : %d' % error.code)
    print('  description : %s' % error.description)
    print('  parameter   : %s\n' % error.parameter)

```

This will give you something like:
```shell
$ python example.py

  amount  : 9 
  type    : credits
  payment : prepaid
```

Please see the other examples for a complete overview of all the available API calls.

Documentation
-------------
Complete documentation, instructions, and examples are available at:
[https://www.messagebird.com/developers/python](https://www.messagebird.com/developers/python).

License
-------
The MessageBird REST Client for Python is licensed under [The BSD 2-Clause License](http://opensource.org/licenses/BSD-2-Clause). Copyright (c) 2014, MessageBird
