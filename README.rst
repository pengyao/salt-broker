=====================
What is Salt Broker?
=====================

salt-broker is a lightweight proxy for `saltstack <https://github.com/saltstack/salt>`_


How to use it?
=====================

Install Requirements
---------------------

.. code-block:: bash

    pip install -r requirements.txt

Install salt-broker
---------------------

.. code-block:: bash

    python setup.py install

Config salt-broker
-------------------

* /etc/salt/broker

.. code-block:: yaml

    master: salt-master.example.com

Start salt-broker
-------------------

.. code-block:: bash

    salt-broker -d
