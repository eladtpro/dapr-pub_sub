from flask import Flask, request, jsonify
from cloudevents.http import from_http
import json
from os import getenv

app = Flask(__name__)


# dapr run --app-id order-processor --components-path ../components/ --app-port 5001 -- python3 app.py
# Register Dapr pub/sub subscriptions
@app.route('/dapr/subscribe', methods=['GET'])
def subscribe():
    subscriptions = [{
        'pubsubname': 'orderpubsub',
        'topic': 'orders',
        'route': 'orders'
    }]
    print('Dapr pub/sub is subscribed to: ' + json.dumps(subscriptions))
    return jsonify(subscriptions)


# Dapr subscription in /dapr/subscribe sets up this route
@app.route('/orders', methods=['POST'])
def orders_subscriber():
    event = from_http(request.headers, request.get_data())
    print('Subscriber received : %s' % event.data['orderId'], flush=True)
    return json.dumps({'success': True}), 200, {
        'ContentType': 'application/json'}

portNumber = getenv('PORT', 5001)
print('Starting app on port: ' + str(portNumber), flush=True)
app.run(port=int(portNumber), debug=True)
