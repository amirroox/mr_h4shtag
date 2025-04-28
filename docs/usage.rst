Usage
=====

Installation
------------

Install the tool using pip:

.. code-block:: bash

    pip install -r requirements.txt

Running the Tool
----------------

Start the tool via the command-line interface:

.. code-block:: bash

    python main.py --help

Example: Scan a target for XSS vulnerabilities:

.. code-block:: bash

    python main.py --target http://example.com --scan xss

API Server
----------

Run the REST API server:

.. code-block:: bash

    python main.py --ai api

Access the dashboard at ``http://localhost:8000/dashboard``.