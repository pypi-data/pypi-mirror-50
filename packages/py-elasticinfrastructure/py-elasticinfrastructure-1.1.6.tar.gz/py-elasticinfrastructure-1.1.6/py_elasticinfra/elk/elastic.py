import datetime as dt
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


class Indexer:
    def __init__(self, config, logger=None):
        self.config = config
        self.elk_config = config["elk"]["elastic"]
        self.index = self.elk_config["index"]
        if logger is None:
            try:
                logger = config.get_logger("elk_logger")
            except:
                raise("[ERROR] Please provide logger.")
        self.logger = logger

    def connect(self):
        try:
            self.es = Elasticsearch(self.elk_config["host"])
        except Exception as exception:
            self.logger.error("[ERROR] \t Could not connect "
                              "to elasticsearch {}".format(self.elk_config["host"]))
            raise exception
        else:
            if self.es is None:
                self.logger.error("[ERROR] \t Could not connect "
                                  "to elasticsearch {}".format(self.elk_config["host"]))
                raise "Could not connect to elasticsearch"
            else:
                self.logger.info("[INFO] \t Successfully connected "
                                 "to es")

    def index_bulk(self, metrics):
        metrics = self._prepare_index(metrics)
        try:
            bulk(self.es, metrics)
        except Exception as exception:
            self.logger.error("[ERROR] \t Could not index "
                              "bulk to elasticsearch {}".format(exception))
        else:
            self.logger.info("[INFO] \t Indexed bulk in es.")

    def _prepare_index(self, metrics):
        now = dt.datetime.now()
        # str_now = now.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        for met in metrics:
            yield{
                "_index": self.index_name,
                "_source": {
                    "timestamp": now,
                    "experiment": self.config["name"],
                    "hostname": self.config["hostname"],
                    "measurement_type": met.get_type(),
                    "measurement": met.measure()
                }
            }

    def _check_connection(self):
            # TODO: decide on other connection checks
            # e.g. es.cluster.health()
        if not self.es:
            return False

    def create_index(self, index_name=None, config=None):
        if index_name is None:
            index_name = self.index["name"]
        if config is None:
            config = self.index["config"]
        try:
            json_config = json.dumps(config, indent=4)
            current_date = dt.date.today().strftime("%d.%m.%Y")
            self.index_name = (index_name + '-' + current_date).lower()
            self.es.indices.create(index=self.index_name,
                                   body=json_config,
                                   ignore=400)
        except Exception as exception:
            self.logger.error("[ERROR] \t Could not create es "
                              " index {}".format(exception))
            raise exception
        else:
            self.logger.info("[INFO] \t Index successfully checked.")
