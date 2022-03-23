hdf5-reader-service
===========================

|code_ci| |docs_ci| |coverage| |pypi_version| |license|

Microservice for reading HDF5 data and serving it via REST, aimed at performance and concurrency

============== ==============================================================
PyPI           ``pip install hdf5-reader-service``
Source code    https://github.com/DiamondLightSource/python-hdf5-reader-service
Documentation  https://DiamondLightSource.github.io/hdf5-reader-service
Releases       https://github.com/DiamondLightSource/python-hdf5-reader-service/releases
============== ==============================================================


To run a basic server::

    uvicorn hdf5_reader_service.main:app

.. |code_ci| image:: https://github.com/DiamondLightSource/python-hdf5-reader-service/workflows/Code%20CI/badge.svg?branch=master
    :target: https://github.com/DiamondLightSource/python-hdf5-reader-service/actions?query=workflow%3A%22Code+CI%22
    :alt: Code CI

.. |docs_ci| image:: https://github.com/DiamondLightSource/python-hdf5-reader-service/workflows/Docs%20CI/badge.svg?branch=master
    :target: https://github.com/DiamondLightSource/python-hdf5-reader-service/actions?query=workflow%3A%22Docs+CI%22
    :alt: Docs CI

.. |coverage| image:: https://codecov.io/gh/DiamondLightSource/hdf5-reader-service/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/DiamondLightSource/hdf5-reader-service
    :alt: Test Coverage

.. |pypi_version| image:: https://img.shields.io/pypi/v/hdf5-reader-service.svg
    :target: https://pypi.org/project/hdf5-reader-service
    :alt: Latest PyPI version

.. |license| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0
    :alt: Apache License

..
    Anything below this line is used when viewing README.rst and will be replaced
    when included in index.rst

See https://DiamondLightSource.github.io/hdf5-reader-service for more detailed documentation.
