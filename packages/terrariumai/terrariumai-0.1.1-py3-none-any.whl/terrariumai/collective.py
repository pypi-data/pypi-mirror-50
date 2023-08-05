import threading
import grpc
import sys
import time
from queue import Queue
from .collective_pb2 import *
from .collective_pb2_grpc import *


PROD_SERVER_ADDR = "34.67.243.23:9090" # TODO

def defaultModelFunc(obsv):
  raise Exception('You need to pass in a model function.')
  
def connectRemoteModel(secret, modelFunc, addr=PROD_SERVER_ADDR):
  # Create the stub
  channel = grpc.insecure_channel(addr)
  stub = collective_pb2_grpc.CollectiveStub(channel)
  metadata = [('model-secret', secret)]
  # Create the iterator
  request_queue = Queue()
  request_iter = iter(request_queue.get, object())
  # Connect
  responses = stub.ConnectRemoteModel(request_iter, metadata=metadata)
  # Try/catch cleanup for Notebook
  try:
      for response in responses:
        # Create the request
        actions = []
        for obsv in response.observations:
          actions.append(modelFunc(obsv))
        actionPacket = collective_pb2.ActionPacket(actions=actions)
        # Set the request to the iterator
        request_queue.put(actionPacket)
  except KeyboardInterrupt:
    # Send cancel to the server
    responses.cancel()

def createAction(id, action, direction):
  return collective_pb2.Action(id=id, action=action, direction=direction)