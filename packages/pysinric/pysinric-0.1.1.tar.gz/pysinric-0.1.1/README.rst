SINRIC
===============

This is a python library for alexa home automation skill
 SINRIC (https://sinric.com/)

Functions:
----------
* Control your home appliances using alexa

Installation :
--------------

Python3
-------

::

    pip3 install pysinric --user

or

Python
------

::

    pip install pysinric --user


**Implementing :**
~~~~~~~~~~~~~~~~~~

::

    from sinric import Sinric
    from time import sleep

    apiKey = 'Replace with your api key'  # https://sinric.com

    response = any

    if __name__ == '__main__':
        obj = Sinric(apiKey)

        while True:
            response = obj.initialize()
            print(response)
            sleep(2)

