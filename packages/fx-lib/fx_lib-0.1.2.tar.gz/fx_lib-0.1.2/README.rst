======
fx-lib
======


Frank Xu(FX)'s personal FX common lib in Python



Install
--------

    pip install git+https://github.com/frankyxhl/py_fx_lib

    or

    pip install fx_lib



Log Module
----------

    import logging
    from fx_lib.log import setup_logging


    setup_logging(".sync.logging.yaml", default_level=logging.DEBUG)
    log = logging.getLogger("frank")


    # log.info("Hello, World")


Example
**********************
Please check here `Config example file <docs/log_config_example.yaml>`_
