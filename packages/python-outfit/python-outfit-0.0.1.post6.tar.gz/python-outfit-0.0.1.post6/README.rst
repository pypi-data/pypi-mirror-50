=============
python-outfit
=============

:Info: utilities for distributed environment
:Repository: https://github.com/situkangsayur/python-outfit
:Author: Hendri Karisma (http://github.com/situkangsayur)
:Maintainer: Hendri Karisma (http://github.com/situkangsayur)

.. image:: https://travis-ci.org/situkangsayur/python-outfit.svg?branch=master
  :target: https://travis-ci.org/situkangsayur/python-outfit

.. image:: https://coveralls.io/repos/github/situkangsayur/python-outfit/badge.svg?branch=master
  :target: https://coveralls.io/github/situkangsayur/python-outfit?branch=master

Python Outfit is set of dependencies across a range of python standard package for software development. 

Features for 0.0.1 version:

1. Load config using yaml.
2. Integrated to Consul.
#. Load config file from a path in KV Consul.
#. Integrated to Vault.
#. Load Secret KV from Vault.
#. add some db status to py-healtchecker.
#. simple Logger.
#. Load Logger configurations from consul, yaml, json, and dictionary logging var in python file.

How to install **Outfit**
=========================
You can use pip for installing python-outfit.

::

    pip install python-outfit

pypi link : `link to outfit <https://pypi.org/project/python-outfit/>`_

Quick Start
===========

Just add outfit packe then import the Class that you need. First to load configuration import Outfit class. Then call *Oufit.setup('config_path')* call setup static method and pass the path of the configuration file to *Oufit.setup()*

.. code:: python

    from outfit import Outfit

    if __name__ == '__main__':
        Outfit.setup('conf/configuration.yaml')

Then you can import **ConsulCon** for Consul Connection or **VaulCon** for Vault Connection, or you can use **Logger** to do some logging text for debug, info, error, or critical mode.

.. code:: python

    from outfit import Outfit
    from outfit import ConsulCon, VaultCon
    from outfit import Logger

    if __name__ == '__main__':
        Outfit.setup('conf/configuration.yaml')
        con_consul = ConsulCon()

        Logger.debug('get the information such as config file from consul kv then will be returned as python dictionary')
        config_dict = con_consul.get_kv()

        con_vault = VaultCon()

        Logger.info('get the secret information in vault secret kv then will be returned as python dictionary')
        secret_dict = con_vault.get_secret_kv()


The consul and vault connection will get the configs information from yaml file, including the Logger config source.

This is the example of the .yaml file for **outfit** configurations:

.. code:: yaml

    vault:
        host: localhost
        port: 9500
        scheme: http
        token: token123jhk123
        path: sample/app
    consul:
        host: localhost
        port: 9500
        scheme: http
        token: token123jhk123
        path: sample/app
    logconfig:
        mode: development
        source_type: yaml_file
        source_location: ./tests/assets/logging.yaml

We can see that the logconfig will provide the log configuration information, it contains mode, source_type, and source_location:

- **mode** of log it depends on the logger profile that you write in log config.
- **source_type**, it can be **yaml_file**, **json_file**, **consul_kv**, and **dictionary** type from python file.
- **source_location**, it will provide the location of the files or consul kv directory.


Sample for log config using *source_type* consul kv:

.. code:: yaml

    vault:
        host: localhost
        port: 9500
        scheme: http
        token: token123jhk123
        path: sample/app
    consul:
        host: localhost
        port: 9500
        scheme: http
        token: token123jhk123
        path: sample/app
    logconfig:
        mode: development
        source_type: consulkv  
        source_location: assets/logging.yaml


And for logging yaml file or the structures :

.. code:: yaml

    ---
    version: 1
    disable_existing_loggers: False
    formatters:
        simple:
          format: "%(asctime)s, %(levelname)s:%(filename)s(%(lineno)d)> %(message)s"
     
    handlers:
        debug_console:
            class: logging.StreamHandler
            level: DEBUG
            formatter: simple
            stream: ext://sys.stdout

        production_console:
            class: logging.StreamHandler
            level: INFO
            formatter: simple
            stream: ext://sys.stdout

        
        debug_file_handler:
            class: logging.handlers.RotatingFileHandler
            level: DEBUG
            formatter: simple
            filename: tests/logs/debug.log
            maxBytes: 10485760 # 10MB
            backupCount: 20
            encoding: utf8
     
        info_file_handler:
            class: logging.handlers.RotatingFileHandler
            level: INFO
            formatter: simple
            filename: tests/logs/info.log
            maxBytes: 10485760 # 10MB
            backupCount: 20
            encoding: utf8
     
        error_file_handler:
            class: logging.handlers.RotatingFileHandler
            level: ERROR
            formatter: simple
            filename: tests/logs/errors.log
            maxBytes: 10485760 # 10MB
            backupCount: 20
            encoding: utf8

        critical_file_handler:
            class: logging.handlers.RotatingFileHandler
            level: CRITICAL
            formatter: simple
            filename: tests/logs/critical.log
            maxBytes: 10485760 # 10MB
            backupCount: 20
            encoding: utf8
     
    loggers:
        development:
            level: DEBUG
            handlers: [debug_console, debug_file_handler, info_file_handler, error_file_handler, critical_file_handler]
            propagate: True

        production:
            level: INFO
            handlers: [production_console, info_file_handler, error_file_handler, critical_file_handler]
            propagate: True
    ...

you can get more detail about log config in yaml from `this link <https://docs.python.org/3/howto/logging.html>`_
