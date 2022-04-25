MessageBird's REST API for Python
=================================
This repository contains the open source Python client for MessageBird's REST API. Documentation can be found at: https://developers.messagebird.com/.

Requirements
------------
- [Sign up](https://www.messagebird.com/en/signup) for a free MessageBird account
- Create a new access key in the developers sections
- An application written in Python >3.8

Installation
------------
The easiest way to install the messagebird package is either via pip:

```
$ pip install messagebird
```

or manually by downloading the source and run the setup.py script:

```
$ python setup.py install
```

Examples
--------
We have put some self-explanatory examples in the [examples](https://github.com/messagebird/python-rest-api/tree/master/examples) directory, but here is a quick example on how to get started. Assuming the installation was successful, you can import the messagebird package like this:

```python
import messagebird
```

Then, create an instance of **messagebird.Client**:

```python
client = messagebird.Client('YOUR_ACCESS_KEY')
```

Now you can query the API for information or send a request. For example, if we want to request our balance information you'd do something like this:

```python
try:
  # Fetch the Balance object.
  balance = client.balance()

  # Print the object information.
  print('Your balance:\n')
  print('  amount  : %d' % balance.amount)
  print('  type    : %s' % balance.type)
  print('  payment : %s\n' % balance.payment)

except messagebird.client.ErrorException as e:
  print('Error:\n')

  for error in e.errors:
    print('  code        : %d' % error.code)
    print('  description : %s' % error.description)
    print('  parameter   : %s\n' % error.parameter)

```

This will give you something like:
```shell
$ python example.py
Your balance:

  amount  : 9 
  type    : credits
  payment : prepaid
```

Please see the other examples for a complete overview of all the available API calls.

To run examples with arguments, try:
```shell script
$ python ./examples/voice_create_webhook.py --accessKey accessKeyWhichNotExist --url https://example.com --title HELLO_WEBHOOK --token HELLO_TOKEN
```

Documentation
-------------
Complete documentation, instructions, and examples are available at:
[https://developers.messagebird.com/](https://developers.messagebird.com/).

License
-------
The MessageBird REST Client for Python is licensed under [The BSD 2-Clause License](http://opensource.org/licenses/BSD-2-Clause). Copyright (c) 2022, MessageBird
