## Steps to run the demo 

### 1. Local Run Dapr in self-hosted mode without Docker (w/o containers)

##### Run components: run the following commands in separate terminals

###### 1.1 start redis-server service
`redis-server`

###### 1.2 start dapr subcscsriber service
`dapr run --app-id order-processor --components-path ../components/ --app-port 5001 -- python3 app.py`

###### 1.3 run dapr publisher service
`dapr run --app-id checkout --components-path ../components/ -- python3 app.py`


### 2. Local Installations

###### 2.1 Intialize dapr without containers (one time only)

> [How-To: Run Dapr in self-hosted mode without Docker](https://docs.dapr.io/operations/hosting/self-hosted/self-hosted-no-docker/)
The Dapr CLI provides an option to [initialize Dapr](https://docs.dapr.io/reference/cli/dapr-init/) using slim init, without the default creation of a development environment with a dependency on Docker. To initialize Dapr with slim init, after installing the Dapr CLI, use the following command:

`dapr init --slim`

###### 2.2 Install Redis without containers
> [Redis Guide](https://redis.io/docs/getting-started/) to get started with Redis. You'll learn how to install, run, and experiment with the Redis server process.
> [Dapr Redis Component Guide](https://docs.dapr.io/operations/components/setup-state-store/supported-state-stores/setup-redis/) where you can find detailed information on the Redis state store component

> [Install Redis on Mac](https://redis.io/docs/getting-started/installation/install-redis-on-mac-os/)
Use Homebrew to install and start Redis on macOS


`arch -x86_64 brew install redis`


> ##### 2.3 Install flask and cloudevents components
> Install flask and cloudevents on the system (without 
> **WARNING**: Use virtualenv instead
virtualenv):

`sudo pip3 install flask`
`sudo pip3 install cloudevents`

> ###### 2.4 Checkout App:
> build topic publisher python app

`cd pub_sub/python/sdk/checkout pip3 install -r requirements.txt`


> ###### 2.5 Order Processor App:
> build  order-processor python app

`cd pub_sub/python/sdk/order-processor pip3 install -r requirements.txt`



### 3. Kubernetes Installations

> ###### **Install Dapr on Kubernetes**

> ###### **Add stable repository**
> The stable repository is hosted on https://kubernetes-charts.storage.googleapis.com/. To add the stable repository to Helm, run the following command:

`helm repo add stable https://charts.helm.sh/stable`

> ###### 3.2. Install Redis on Kubernetes
>[How to Deploy RabbitMQ on Kubernetes](https://phoenixnap.com/kb/install-and-configure-rabbitmq-on-kubernetes): Tutorial shows you how to install a RabbitMQ instance on Kubernetes using the Helm package manager. RabbitMQ is a message broker that supports multiple messaging protocols. It is lightweight and easy to deploy on a range of platforms, including public clouds, virtual machines, and bare-metal servers. It is also highly available, scalable, and fault tolerant.

> **Create a Namespace for the RabbitMQ Deployment**
> All resources in Kubernetes are started in a namespace. Unless one is specified, the system uses the default namespace. To have better control over the deployment process use the following command to create a distinct namespace:

`kubectl create namespace rabbit`

>With Helm successfully installed and a designated namespace you are ready to start the RabbitMQ deployment process. Enter the following command to apply a default stable/rabbitmq chart from a git repository:

helm install mu-rabbit stable/rabbitmq --namespace rabbit












> ###### 3.2. Create a namespace for acr???
nerdctl build --namespace k8s.io .




helm create dapr-pub_sub-chart

helm package dapr-pub_sub-chart

helm install order-processor-release1 dapr-pub_sub-chart-0.1.0.tgz

### Testing

Postman
https://www.postman.com/downloads/