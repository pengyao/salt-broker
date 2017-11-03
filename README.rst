=====================
What is Salt Broker?
=====================

salt-broker is a lightweight proxy for `saltstack <https://github.com/saltstack/salt>`_


How to use it?
=====================

Install salt-broker
-------------------

* RPM

.. code-block:: bash

    #for el6
    rpm -ivh salt-broker-2016.11.4-1.el6.noarch.rpm
    #for el7
    rpm -ivh salt-broker-2016.11.4-1.el7.noarch.rpm

Config salt-broker
-------------------

* /etc/salt/broker

.. code-block:: yaml

    master: salt-master.example.com

Start salt-broker
-------------------

.. code-block:: bash

    service salt-broker start
