from functools import singledispatch
import json
import pandas as pd
import time
import zmq

class Request:
    """
    Request object for creating new requests within the rendezvous architecture.
    """
    def __init__(self):
        self._msg_serialization = singledispatch(self._msg_serialization)
        self._msg_serialization.register(pd.DataFrame(), self._msg_serialization_df)
        self.request = {
            'diagnostics': [],
            'provenance': {},
            'policy': None,
            'request': None,
            'response': None
        }

    def add_provenance(self, name, content):
        """
        Whenever a request is handled a new provenance entry should be added
        :param name: the name of the provenance instance
        :param content: information regarding the current provenance instance
        """
        self.request['diagnostics'].append({'origin': name,
                                            'timestamp': int(time.time() * 1000)
                                            })
        self.request['provenance'] .update({name: content})

    def set_data(self, data):
        """
        :param data: Write data into the request. This will overwrite previous data!
        """
        self.request['request']['data'] = new_data

    def get_data(self):
        """
        :return: Returns data contained in the request.
        """
        return self.request['request']['data']

    def set_policy(self, new_policy):
        """
        :param: Writes a policy into the request. This will overwrite a previous policy!
        """
        self.request['request']['data'] = new_policy

    def get_policy(self):
        """
        :return: Returns the policy of the request.
        """
        return self.request['request']['data']

    def to_json(self):
        """
        :return: Returns request as a json object.
        """
        return json.dumps(self.request, default=self._msg_serialization)

    @classmethod
    def from_json(cls, json_request):
        """
        :param json_request: Creates a request object from a json.
        """
        v = cls()
        v.request = json.loads(json_request, object_hook=cls._obj_hook)
        return v

    @staticmethod
    def _obj_hook(dict_from_json):
        """
        :param dict_from_json: Used to translate a json back into a request message.
        """
        dict_from_json['data_df'] = pd.read_json(dict_from_json['data_df'], orient='split')
        return dict_from_json

    @staticmethod
    def _msg_serialization(message):
        """
        :param message: Used by default for serializing a message.
        """
        return json.JSONEncoder(message)

    @staticmethod
    def _msg_serialization_df(message):
        """
        :param message: Used  for serializing a message if it is an instance of pandas.DataFrame().
        """
        return message.to_json(orient='split', index=False)


class MyZeroMQ:
    """
    Sending and receiving requests via the zeroMQ messaging system.
    """
    def __init__(self):
        self.context = zmq.Context()
        self.subscriber = None
        self.publisher = None

    def subscribe_to_publisher(self, ip: str, port: int, topic: str):
        """
        Subscribes to a publisher. Multiple subscribers can subscribe to the same publisher. It is valid to start
        the publisher after the subscribers. Previously sent messages will be discarded.
        :param ip: IP address or 'localhost'
        :param port: TCP port
        :param topic: Topic which the subscribers can filter for
        """
        if isinstance(topic, str):
            topic = topic.encode()
        self.subscriber = self.context.socket(zmq.SUB)
        self.subscriber.connect("tcp://{}:{}".format(ip, port))
        self.subscriber.setsockopt(zmq.SUBSCRIBE, topic)

    def publish_to_subscriber(self, ip, port):
        """
        Publish to one subscriber. Multiple publisher can subscribe to the same subscriber. It is valid to start
        the subscriber after the publisher. Previously sent messages will be discarded.
        :param ip: IP address or 'localhost'
        :param port: TCP port
        """
        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.connect("tcp://{}:{}".format(ip, port))

    def start_publisher(self, port: int, ip: str = '*'):
        """
        Starts a new publisher. Multiple subscriber can subscribe to this publisher. It is valid to start
        the subscribers after the publisher. Previously sent messages will be discarded.
        :param port: TCP port
        :param ip: Permitted IP address for the subscribers. Default is '*', which allows all subscribers.
        """
        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.bind("tcp://{}:{}".format(ip, port))

    def start_subscriber(self, port: int, topic: str = '', ip: str = '*'):
        """
        Starts a new subscriber. Multiple publishers can send to this subscriber. It is valid to start
        the publishers after the subscriber. Previously sent messages will be discarded.
        :param port: TCP port
        :param topic: Topics which the subscribers accepts
        :param ip: Permitted IP address for the publishers. Default is '*', which allows all publishers.
        """
        if isinstance(topic, str):
            topic = topic.encode()
        self.subscriber = self.context.socket(zmq.PUB)
        self.subscriber.bind("tcp://{}:{}".format(ip, port))
        self.subscriber.setsockopt(zmq.SUBSCRIBE, topic)

    def send_request(self, topic, msg):
        """
        Sends a Request object or another serializable message.
        :param topic: Topics which the subscribers accepts
        :param msg: Message to send
        """
        if not self.publisher:
            raise Exception("Publisher hasn't be started. Use: ZeroMQ.start_publisher()")
        if isinstance(msg, Request):
            serial_msg = msg.to_json()
        else:
            serial_msg = json.dumps(msg)
        self.publisher.send_string(topic, zmq.SNDMORE)
        self.publisher.send(serial_msg)

    def receive_request(self):
        """
        Receives a Request object.
        :param topic: Topics which the subscribers accepts
        :param msg: Message to send
        """
        if not self.subscriber:
            raise Exception("Subscriber hasn't be started. Use: ZeroMQ.start_subscriber()")
        topic = self.subscriber.recv_string()
        msg = self.subscriber.recv()
        request = Request.from_json(msg)
        return topic, request


class MyKafka:
    def __init__(self):
        pass