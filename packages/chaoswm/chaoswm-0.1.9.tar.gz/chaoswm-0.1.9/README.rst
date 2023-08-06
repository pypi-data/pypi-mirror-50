=====================
chaostoolkit-wiremock
=====================




.. image:: https://img.shields.io/pypi/v/chaoswm.svg
        :target: https://pypi.python.org/pypi/chaoswm

.. image:: https://img.shields.io/travis/grubert65/chaostoolkit-wiremock.svg
        :target: https://travis-ci.org/grubert65/chaostoolkit_wiremock

.. image:: https://readthedocs.org/projects/chaostoolkit-wiremock/badge/?version=latest
        :target: https://chaostoolkit-wiremock.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




ChaosToolkit driver for wiremock

Installation from Pypi
----------------------

You need to have a python 3.5+ interpreter::
    
    pip install chaoswm


Installation from source
------------------------
In order to use it, you need python 3.5+ in your environment

Steps::

    python3 -mvenv ~/virtualenvs/chaostoolkit-wiremock
    surce  ~/virtualenvs/chaostoolkit-wiremock/bin/activate
    git clone git@github.com:sky-uk/chaostoolkit-wiremock.git
    cd chaostoolkit-wiremock
    pip install -r requirements_dev.txt
    make clean && make test && make install

To run in production, first install the requirements::

    pip install -r requirements.txt


Supported actions
-----------------

-	**add_mappings**: adds a list of mappings to wiremock
-	**populate_from_dir**: adds all mappings found in a directory
-	**delete_mappings**: deletes a list of mappings
-	**global_fixed_delay**: adds a fixed delay to all mappings 
-	**global_random_delay**: adds a random delay to all mappings 
-	**fixed_delay**: adds a fixed delay to a list of mappings
-	**random_delay**: adds a random delay to a list of mapppings
-	**chunked_dribble_delay**: adds a chunked dribble delay to a list of mappings
-	**down**: sets a list of services down
-	**up**: deletes all delays connected with a list of mappings
-	**reset**: resets the wiremock server: deletes all mappings!


Supported probes
----------------

-   **server_running**: returns 1 if the configured Wiremock server can be contacted
-   **mappings**: returns the list of mappings found on the server


Configuration
-------------

The following keys can be configured in the experiment global configuration
section, under the "wiremock" key:

-   **host**: the wiremock server host
-   **port**: the wiremock server port
-   **contextPath**:  the contextPath for your wiremock server (optional)
-   **timeout**: accepted timeout (defaults to 1 sec)
-   **down**: the delayDistribution section used by the ``down`` action

Configuration example::

    {
        "configuration": {
            "wiremock": {
                "host": "localhost",
                "port": 8080,
                "contextPath": "/wiremock",
                "timeout": 10,
                "down": {
                    "type": "lognormal",
                    "median": 3000,
                    "sigma": 0.2
                }
            }
        }
    }



Exported Actions
----------------

Note: the experiments directory contains json snippets for each of them for
you to play with.

Adding a list of mappings::

    {
      "method": [
        {
          "type": "action",
          "name": "adding a mapping",
          "provider": {
            "type": "python",
            "module": "chaoswm.actions",
            "func": "add_mappings",
            "arguments": {
              "mappings": [{
                "request": {
                   "method": "GET",
                   "url": "/hello"
                },
                "response": {
                   "status": 200,
                   "body": "Hello world!",
                   "headers": {
                       "Content-Type": "text/plain"
                   }
                } 
              }]
            }
          }
        }
      ]
    }

Adding all mappings found in a directory (see experiment file populate_from_dir.json)::

    {
      "type": "action",
      "name": "populate_from_dir",
      "provider": {
        "type": "python",
        "module": "chaoswm.actions",
        "func": "populate_from_dir",
        "arguments": {
          "dir": "experiments/mappings"
        }
      }
    }

Deleting a list of mappings::

    {
      "method": [
        {
          "type": "action",
          "name": "deleting a mapping",
          "provider": {
            "type": "python",
            "module": "chaoswm.actions",
            "func": "delete_mappings",
            "arguments": {
              "filter": [{
                "method": "GET",
                "url": "/some/thing"
              }]
            }
          }
        }
      ]
    }


Adding a global fixed delay::

    {
      "method": [
        {
          "type": "action",
          "name": "Adding a global fixed delay",
          "provider": {
            "type": "python",
            "module": "chaoswm.actions",
            "func": "global_fixed_delay"
            "arguments": {
                "fixedDelay": 10
            }
          }
        }
      ]
    }


Adding a global random delay::

    {
      "method": [
        {
          "type": "action",
          "name": "Adding a global random delay",
          "provider": {
            "type": "python",
            "module": "chaoswm.actions",
            "func": "global_random_delay"
            "arguments": {
              "delayDistribution": {
                "type": "lognormal",
                "median": 20,
                "sigma": 0.1
              }
            }
          }
        }
      ]
    }


Adding a fixed delay to a list of mappings::

    {
      "method": [
        {
          "type": "action",
          "name": "Adding a fixed delay to a mapping",
          "provider": {
            "type": "python",
            "module": "chaoswm.actions",
            "func": "fixed_delay"
            "arguments": {
              "filter": [{
                "method": "GET",
                "url": "/some/thing"
              }],
              "fixedDelayMilliseconds": 100
            }
          }
        }
      ]
    }


Adding a random delay to a list of mappings::

    {
      "method": [
        {
          "type": "action",
          "name": "Adding a random delay to a mapping",
          "provider": {
              "type": "python",
              "module": "chaoswm.actions",
              "func": "random_delay"
              "arguments": {
                "filter": [{
                  "method": "GET",
                  "url": "/some/thing",
                }],
                "delayDistribution": {
                  "type": "lognormal",
                  "median": 80,
                  "sigma": 0.4
                }
              }
          }
        }
      ]
    }

Adding a ChunkedDribbleDelay to a list of mappings::

    {
      "method": [
        {
          "type": "action",
          "name": "Adding a ChunkedDribbleDelay to a mapping",
          "provider": {
            "type": "python",
            "module": "chaoswm.actions",
            "func": "chunked_dribble_delay"
            "arguments": {
              "filter": [{
                "method": "GET",
                "url": "/some/thing",
              }],
              "chunkedDribbleDelay": {
                "numberOfChunks": 5,
                "totalDuration": 1000
              }
            }
          }
        }
      ]
    }


Taking a list of mappings down (heavy distribution delay)
This action will use the parameters specified in the "down" key of
the configuration section::

    {
      "method": [
        {
          "type": "action",
          "name": "Taking a mapping down",
          "provider": {
            "type": "python",
            "module": "chaoswm.actions",
            "func": "down"
            "arguments": {
              "filter": [{
                "method": "GET",
                "url": "/some/thing",
              }]
            }
          }
        }
      ]
    }


Taking a list of mappings up back again::

    {
      "method": [
        {
          "type": "action",
          "name": "Taking a mapping down",
          "provider": {
            "type": "python",
            "module": "chaoswm.actions",
            "func": "up"
            "arguments": {
              "filter": [{
                "method": "GET",
                "url": "/some/thing",
              }]
            }
          }
        }
      ]
    }


Resetting the wiremock server (deleting all mappings)::

    {
      "method": [
        {
          "type": "action",
          "name": "Taking a mapping down",
          "provider": {
              "type": "python",
              "module": "chaoswm.actions",
              "func": "reset"
          }
        }
      ]
    }


Discovery
=========

You may use the Chaos Toolkit to discover the capabilities of this extension::

    $ chaos discover chaostoolkit-wiremock  --no-install


Experiments
===========

The experiments directory contains experiments to play against a default WM
server (maybe the easiest way is to start a wiremock docker container exposing 
default port 8080).




Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
