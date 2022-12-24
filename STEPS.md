## Steps to run the demo 

### Local Run Dapr in self-hosted mode without Docker (w/o containers)

##### Run agents


###### start redis server
`redis-server`

###### start dapr subcscsriber service
`dapr run --app-id order-processor --components-path ../components/ --app-port 5001 -- python3 app.py`

###### run dapr publisher service
`dapr run --app-id checkout --components-path ../components/ -- python3 app.py`



### Installations

###### Intialize dapr without containers (one time only)

> [How-To: Run Dapr in self-hosted mode without Docker](https://docs.dapr.io/operations/hosting/self-hosted/self-hosted-no-docker/)
The Dapr CLI provides an option to [initialize Dapr](https://docs.dapr.io/reference/cli/dapr-init/) using slim init, without the default creation of a development environment with a dependency on Docker. To initialize Dapr with slim init, after installing the Dapr CLI, use the following command:

`dapr init --slim`

###### Install Redis without containers
>[Redis Guide](https://redis.io/docs/getting-started/) to get started with Redis. You'll learn how to install, run, and experiment with the Redis server process.

> [Dapr Redis Component Guide](https://docs.dapr.io/operations/components/setup-state-store/supported-state-stores/setup-redis/) where you can find detailed information on the Redis state store component


> [Install Redis on Mac](https://redis.io/docs/getting-started/installation/install-redis-on-mac-os/)
Use Homebrew to install and start Redis on macOS


`arch -x86_64 brew install redis`


> ##### Install flask and cloudevents components
> Install flask and cloudevents on the system (without 
> **WARNING**: Use virtualenv instead
virtualenv):

`sudo pip3 install flask`
`sudo pip3 install cloudevents`

> ###### Checkout App:
> build topic publisher python app

`cd pub_sub/python/sdk/checkout pip3 install -r requirements.txt`


> ###### Order Processor App:
> build  order-processor python app

`cd pub_sub/python/sdk/order-processor pip3 install -r requirements.txt`






### Kubernetes

> ###### create a namespace for acr???
nerdctl build --namespace k8s.io .


helm create order-processor-chart

helm package order-processor-chart

helm install order-processor-release1 order-processor-chart-0.1.0.tgz

### Testing

Postman
https://www.postman.com/downloads/