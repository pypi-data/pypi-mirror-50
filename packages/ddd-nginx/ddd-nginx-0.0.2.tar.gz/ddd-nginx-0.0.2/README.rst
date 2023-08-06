DDD Nginx Framework
===================

|Build Status| |Pypi Status| |Coveralls Status|

Installation
------------

From source code:

::

    python setup.py install

From pypi:

::

    pip install ddd-base

Usage
-----

::

    from ddd_base.value_object import ValueObject


    class TheValueObject(ValueObject):

        def __init__(self, name):
            super(TheValueObject, self).__init__()
            self.name = name

        def __eq__(self, other):
            if not isinstance(other, ValueObject):
                return NotImplemented

            return self.name == other.name


    def test_value_object_compare():
        a_value_object = TheValueObject("name")
        b_value_object = TheValueObject("name")

        assert a_value_object.same_as(b_value_object)



License
-------

This software is licensed under the `MIT license <http://en.wikipedia.org/wiki/MIT_License>`_

See `License file <https://github.com/sunwei/ddd-base/blob/master/LICENSE>`_

.. |Build Status| image:: https://travis-ci.com/sunwei/ddd-nginx.svg?branch=master
   :target: https://travis-ci.com/sunwei/ddd-nginx
.. |Pypi Status| image:: https://badge.fury.io/py/ddd-nginx.svg
   :target: https://badge.fury.io/py/ddd-nginx
.. |Coveralls Status| image:: https://coveralls.io/repos/github/sunwei/ddd-nginx/badge.svg?branch=master
   :target: https://coveralls.io/github/sunwei/ddd-nginx?branch=master
