==============
Stakion Logger
==============

`Stakion <https://stakion.io>`__ monitors ML models in realtime by just logging the input and output features.

Using stakion-logger, you can easily send JSON logs to Stakion for analysis.

Requirements
------------

- Python 2.7 or 3.4+
- ``requests_futures``
- ``socketio``

Installation
------------
The easiest way to install the stakion logger is with pip:
```
$ pip install stakion-logger
```

Quickstart
----------
Stakion has been developed to integrate as a logging library and is therefore
very simple to use.

The first step is to initialise the logger:

.. code:: python
    
    from stakion import logger
    
    sender = logger.StakionSender(
        project_id=#Your project ID,
        api_key=#Your api key
    )


You can then send log messages asynchronously using:

.. code:: python
    
    sender.publish(
        correlation_id=correlation_id,
        event_type=event_type,
        model=model_name,
        data=log_message
    )

Usage
-----
In order for Stakion to compute monitoring metrics, the log message need to follow a certain format:

correlation_id
    The correlation ID is used to identify one single prediction. This is
    useful to group input and output features together for example. It is also
    used when searching through the logs

event_type
    Stakion supports 5 events types:
    
    - prediction_requested
       Used to compute the total number of predictions made in a
       certain period. Can be omited if the number of predictions
       corresponds to the number of unique correlation ID in the
       input_features and output_features events.
    
    - input_features
       The input features for a prediction.
    
    - output_features
       The input features for a prediction.
    
    - crash_logger
       Used internally when a message can't be validated.
       
    - error
       Used to track the number of errors.

data
    For Stakion to compute accurate metrics, the data object must be correctly
    formated based on the event_type:
    
    - prediction_requested
        Data should be ``None``
    
    - input_features
        Should be a dictionary where each key is a feature. Example:
        
        .. code:: python
        
            data = {
                "feature_1": feature_1,
                "feature_2": feature_2
            }
    
    - output_features
        Should be a dictionary where each key is a feature. Example:
        
        .. code:: python
        
            data = {
                "outcome": outcome
            }
    
    - error
        Should be a dictionary with the keys:
        
        .. code:: python
        
            data = {
                "level': "CRITICAL",
                "message': "Can't output to log",
                "traceback": traceback.format_exc()
            }