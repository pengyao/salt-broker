=====================
What is Salt Broker?
=====================

salt-broker is a lightweight proxy for `saltstack <https://github.com/saltstack/salt>`_


How to use it?
=====================

Install salt-broker
-------------------

* PIP

.. code-block:: bash

    pip install salt-broker

Config salt-broker
-------------------

* /etc/salt/broker

.. code-block:: yaml

    master: salt-master.example.com

Start salt-broker
-------------------

.. code-block:: bash

    salt-broker -d
