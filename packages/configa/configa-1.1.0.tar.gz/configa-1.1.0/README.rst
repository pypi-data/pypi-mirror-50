#######
Configa
#######
Convert configuration items into Python objects.

*************
Prerequisites
*************
Targeting Python 3 here on a Linux platform.

Note: ``python3`` must exist in order for the project ``Makefile`` to function correctly.

***************
Getting Started
***************
Get the code::

    $ git clone https://github.com/loum/configa.git
    
Build the virtual environment and download project dependencies::

    $ cd configa
    $ make init APP_ENV=dev
    
Run the tests to make sure all is OK::

    $ source 3env/bin/activate
    (venv) $ make tests

***********************
Build the Documentation
***********************
Project documentation is self contained under the ``doc/source`` directory.  To build the documentation locally::

    $ make docs

The project comes with a simple web server that allows you to present the docs from within your own environment::

    $ cd docs/build
    $ ./http_server.py
    
Note: The web server will block your CLI and all activity will be logged to the console.  To end serving pages, just ``Ctrl-C``.
    
To view pages, open up a web browser and navigate to ``http:<your_server_IP>:8888``
