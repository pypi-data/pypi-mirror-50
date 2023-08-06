from tensorflow.core.util import event_pb2
from tensorflow.python.lib.io import tf_record
from tensorflow.python.framework import tensor_util

def my_summary_iterator(path):
    for r in tf_record.tf_record_iterator(path):
        yield event_pb2.Event.FromString(r)

from collections import namedtuple

record = namedtuple('record', 'tag step value')

def records(path:str):
    for event in my_summary_iterator(path):
        for value in event.summary.value:

            tag = value.tag
            t = tensor_util.MakeNdarray(value.tensor)
            yield record(tag, event.step, float(t))