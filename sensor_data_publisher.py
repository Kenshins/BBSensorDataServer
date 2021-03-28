#
#   Martin Kleberger 2021
#
#   Handle zero MQ publisher
#

import zmq
import logging
import struct
import chat_message_pb2 as ChatMessage

def setup_zeromq_socket(port):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    zmq_endpoint = "tcp://*:" + port
    logging.info("ZeroMQ endpoint: " + zmq_endpoint)
    socket.bind(zmq_endpoint)
    return socket

def send_on_zeromq_socket(port):
    socket = setup_zeromq_socket(port)
    m = ChatMessage.chat_message()
    m.message_content = "Ruppy Snuppy"

    logging.debug('Sending data!')
    s = m.SerializeToString()
    packed_len = struct.pack('>L', len(s))
    socket.send(packed_len)
    socket.send(s)