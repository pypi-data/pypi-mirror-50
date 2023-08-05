import logging
import os

from polytropos.ontology.task import Task

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

data: str = os.path.join("/Users/dbborens/dmz/output/anr_test_data")
conf = os.path.join("/Users/dbborens/dmz/github/analysis/etl5")
task = Task.build(conf, data, "do_debug")
task.run()
