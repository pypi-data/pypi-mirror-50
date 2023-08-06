======================
python-designateclient
======================

python-designateclient provides python bindings and command line tools for both
Designate v1 and v2 APIs.

The :ref:`Python API bindings <bindings>` are provided by the
:program:`designateclient` module.

There are two separate command line interfaces to work with the two API
versions:

v2: the designate plugin for the :program:`openstack` command line tool.  More information can be
found on the :ref:`designate v2 command line tool page <shell-v2>`.

v1: the :program:`designate` command line tool.  More information can be found
on the :ref:`designate v1 command line tool page <shell>`.

.. warning::

    The V1 API was removed in Queens, and cannot be re-enabled.
    The :program:`designate` command line tool will no longer function on
    installs newer than Queens.


You'll need credentials for an OpenStack cloud that implements the Designate
API in order to use the client.

.. toctree::
   :maxdepth: 1

   install/index
   user/index
   cli/index
   contributor/index
   reference/index

.. rubric:: Indices and tables

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _Cloud DNS: http://www.hpcloud.com/products-services/dns
