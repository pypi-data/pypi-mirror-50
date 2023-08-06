# py-elasticinfrastructure
This small utilty indexes infrastructure metrics to elasticsearch.


It was created to gather infrastructure data from machine learning experiments, with a focus on GPU utilization and CPU temperature.
The inspiration comes from metricbeats by Elastic. However, this module is written in Python and it is easier to customize (I found some community beats for Elastic outdated and impossible to run on newer machines).

## Install

```
$ pip install py-elasticinfrastructure 
```

## Run

There are two ways of running the project: (1) as an standalone program, see [example.py](https://github.com/NullConvergence/py_metrics/blob/master/example.py) or (2) on a separate thread, part of a bigger project, see [example_multithread.py](https://github.com/NullConvergence/py_metrics/blob/master/example_multithread.py).

#### 1. Run standalone
In order to run the project in the first case, you have to add a configuration JSON file (see [configs](https://github.com/NullConvergence/py_metrics/tree/master/configs)) and run:

```
$ python example.py --config=configs/<config-file>.json
```
An example config file is provided as [default](https://github.com/NullConvergence/py_metrics/blob/master/configs/default.json). 
Make sure you edit the elasticsearch host data before you run the project.


#### 2. Run in a project
In order to run in a separate project, the library will spawn a new thread and run the indexing loop.
After instalation, you can import and configure the runner as follows:
```
import time
from py_elasticinfra.elk.elastic import Indexer
from py_elasticinfra.runner import Runner
from py_elasticinfra.utils.parse_config import ConfigParser

## confgure elasticsearch indexer
# config can be a json or a file path

es = Indexer(config)
es.connect()
es.create_index()

# configure and run 
runner = Runner(config, es)
runner.run_background()

# stop runner after 5 seconds
time.sleep(5)
runner.stop_background()
```

An example is configured in [example_multithread.py](https://github.com/NullConvergence/py-elasticinfrastructure/blob/master/example_multithread.py) and can be ran:
```
$ python example_multithread.py --config/<config>.json
```

An example config file is provided as [default](https://github.com/NullConvergence/py_metrics/blob/master/configs/default.json). 
Make sure you edit the elasticsearch host data before you run the project.

## Extend

You can add new metrics by adding a new file in the ```py_metrics/metrics``` folder and subclassing the BaseMetric.
Afterwards, you can add it to the ```__init__.py``` file and to the config.

## ELK Docker

In order to run the ELK stack in docker, see [docker-elk](https://github.com/deviantony/docker-elk).
The indexed data can be mined using Kibana.
