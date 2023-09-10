from flask import Flask, jsonify
from flask_cors import CORS
import grpc, json
from google.protobuf.json_format import MessageToJson
import examples_pb2
import examples_pb2_grpc
import time
import memcache
from pymemcache.client import base

# Creating connection with mnemcached
mc = memcache.Client(['memcached:11211'], debug=0)

# Setting a value
mc.set('France', 'Paris', time=60)

print(mc.get('France'))

valor = mc.get('France')

if valor is None:
    print("No hay valor")
else:
    print(valor)

app = Flask(__name__)
CORS(app)

class DataClient(object):
    def __init__(self):
        
        self.host = 'server'
        self.server_port = '50051'
        self.channel = grpc.insecure_channel('{}:{}'.format(self.host, self.server_port))
        self.stub = examples_pb2_grpc.DataStub(self.channel)

    def GetTemperature(self):
        request = examples_pb2.Empty()
        return self.stub.GetWeatherData(request)
    
    def GetCoins(self):
        request = examples_pb2.Empty()
        return self.stub.GetCoinsData(request)


# ROUTES
@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Hello world"})

@app.route('/temperature', methods=['GET'])
def getTemperatura():
    client = DataClient()
    response = client.GetTemperature()
    response = MessageToJson(response)
    response = json.loads(response)
    print(response)
    return jsonify(response)


@app.route('/cash', methods=['GET'])
def getCoins():
    client = DataClient()
    response = client.GetCoins()
    response = MessageToJson(response)
    # insert the json response into memcached
    mc.set('coins', response, time=60)
    # get the json response from memcached
    response = mc.get('coins')
    print("Response from memcached: ",response)
    # make a response with this tring concate in the response "Response from memcached: "
    response = json.loads(response)
    # in jsonify includes the next parameter "Response from memcached: " 
    
    return jsonify("Response from memcached: ",response)   

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)