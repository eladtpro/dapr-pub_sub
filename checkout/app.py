from flask import Flask, request, jsonify
from dapr.clients import DaprClient
import time
import json
import logging
from os import getenv

app = Flask(__name__)

# dapr run --app-id checkout --components-path ../components/ -- python3 app.py
logging.basicConfig(level=logging.INFO)

@app.route('/')
@app.route('/health')
def health_check():
    return 'OK', 204

# Dapr subscription in /dapr/subscribe sets up this route
@app.route('/checkout', methods=['GET'])
def fire_orders():
    counter = request.args.get('counter', default = 1, type = int)
    for i in range(counter, counter+10):
        order = {'orderId': i}

        with DaprClient() as client:
            # Publish an event/message using Dapr PubSub
            result = client.publish_event(
                pubsub_name='orderpubsub',
                topic_name='orders',
                data=json.dumps(order),
                data_content_type='application/json',
            )
        dump = 'Published data: ' + json.dumps(order)
        logging.info(dump)
        print(dump, flush=True)
        time.sleep(1)
    return json.dumps({'success': True}), 200, {
        'ContentType': 'application/json'}

portNumber = getenv('PORT', 5002)
print('Starting app on port: ' + str(portNumber), flush=True)
app.run(port=int(portNumber), debug=True)




