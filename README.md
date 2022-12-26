# Dapr Pub/Sub Demo

## Steps to run the demo 

#### 1. Local Run Dapr in self-hosted mode without Docker (w/o containers)

##### Run components: run the following commands in separate terminals

###### 1.1 start redis-server service
`redis-server`

###### 1.2 start dapr subcscsriber service
`cd dapr-pub_sub/order-processor`
`dapr run --app-id order-processor --components-path ../components/ --app-port 5001 -- python3 app.py`

###### 1.3 run dapr publisher service
`cd dapr-pub_sub/checkout`
`dapr run --app-id checkout --components-path ../components/ --app-port 5002 -- python3 app.py`

###### 1.4 fire checkout event
http://localhost:5002/checkout?counter=100


##### Run in local kubernetes cluster (w/ containers)

###### 1.0 deploy dapr pubsub chart
`helm -n default upgrade -i dapr-pubsub-release1 dapr-pub_sub-chart --set customResources.enabled=false --debug`




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


### 3. AKS Dapr extensions

> ###### 3.1. Install Dapr on AKS
> [Quickstart: Connect an existing Kubernetes cluster to Azure Arc](https://learn.microsoft.com/en-us/azure/azure-arc/kubernetes/quickstart-connect-cluster?tabs=azure-cli)
> [Troubleshoot Dapr extension installation errors](https://learn.microsoft.com/en-us/troubleshoot/azure/azure-kubernetes/troubleshoot-dapr-extension-installation-errors)

`az login`

`az k8s-extension create --cluster-type managedClusters \`
`--cluster-name cluster1 \`
`--resource-group azure-kubernetes-service \`
`--name dapr \`
`--extension-type Microsoft.Dapr`

`az k8s-extension create --name dapr --extension-type Microsoft.Dapr --config enableTraining=True enableInference=True inferenceRouterServiceType=LoadBalancer allowInsecureConnections=True inferenceLoadBalancerHA=False --cluster-type managedClusters --cluster-name cluster1 --resource-group azure-kubernetes-service --scope cluster`

### 4. Kubernetes Installations

> ###### **Install Dapr on Kubernetes**

> ###### **Add stable repository**
> The stable repository is hosted on https://kubernetes-charts.storage.googleapis.com/. To add the stable repository to Helm, run the following command:

`helm repo add stable https://charts.helm.sh/stable`

> ###### 4.1. Install Redis on Kubernetes
>[How to Deploy RabbitMQ on Kubernetes](https://phoenixnap.com/kb/install-and-configure-rabbitmq-on-kubernetes): Tutorial shows you how to install a RabbitMQ instance on Kubernetes using the Helm package manager. RabbitMQ is a message broker that supports multiple messaging protocols. It is lightweight and easy to deploy on a range of platforms, including public clouds, virtual machines, and bare-metal servers. It is also highly available, scalable, and fault tolerant.

> **Create a Namespace for the RabbitMQ Deployment**
> All resources in Kubernetes are started in a namespace. Unless one is specified, the system uses the default namespace. To have better control over the deployment process use the following command to create a distinct namespace:

`kubectl create namespace rabbit`

>With Helm successfully installed and a designated namespace you are ready to start the RabbitMQ deployment process. Enter the following command to apply a default stable/rabbitmq chart from a git repository:

helm install mu-rabbit stable/rabbitmq --namespace rabbit

> ###### 4.2. Connect to Azure Container Registry

> [Create a Secret by providing credentials on the command line](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/#create-a-secret-by-providing-credentials-on-the-command-line)
> Create this Secret, naming it acrcred:

`kubectl create secret docker-registry acrcred --docker-server=<your-registry-server> --docker-username=<your-name> --docker-password=<your-pword> --docker-email=<your-email>`

where:

* __your-registry-server__ is your Private Docker Registry FQDN. Use https://index.docker.io/v1/ for DockerHub.
* __your-name__ is your Docker username.
* __your-pword__ is your Docker password.
* __your-email__ is your Docker email.
You have successfully set your Docker credentials in the cluster as a Secret called __acrcred__.



> ###### 4.3. Working with local container registry
> [Working with local container registry](https://docs.rancherdesktop.io/tutorials/working-with-containers/)

`nerdctl build --namespace k8s.io .`


### 5. Helm package and deploy

> ###### 5.1. Create a helm chart

`helm create dapr-pub_sub-chart`

> ###### 5.2. Test the helm chart - dry-run

`helm -n default upgrade -i dapr-pubsub-release1 dapr-pub_sub-chart --set customResources.enabled=false --debug --dry-run`

> ###### 5.3. Deploy the helm chart w/o --debug
`helm -n default upgrade -i dapr-pubsub-release1 dapr-pub_sub-chart --set customResources.enabled=false [--debug]`


### 6. Testing

Postman
https://www.postman.com/downloads/


# Dapr pub/sub

In this quickstart, you'll create a publisher microservice and a subscriber microservice to demonstrate how Dapr enables a publish-subcribe pattern. The publisher will generate messages of a specific topic, while subscribers will listen for messages of specific topics. See [Why Pub-Sub](#why-pub-sub) to understand when this pattern might be a good choice for your software architecture.

Visit [this](https://docs.dapr.io/developing-applications/building-blocks/pubsub/) link for more information about Dapr and Pub-Sub.

> **Note:** This example leverages the Dapr client SDK.  If you are looking for the example using only HTTP `requests` [click here](../http).

This quickstart includes one publisher:

- Python client message generator `checkout` 

And one subscriber: 
 
- Python subscriber `order-processor`

### Run Python message subscriber with Dapr

<!-- STEP
name: run
-->

```bash
cd ./order-processor
pip3 install -r requirements.txt 
```

<!-- END_STEP -->

2. Run the Python subscriber app with Dapr: 

<!-- STEP
name: Run python subscriber
expected_stdout_lines:
  - '== APP == Subscriber received : 4'
  - "Exited App successfully"
expected_stderr_lines:
output_match_mode: substring
working_dir: ./order-processor
background: true
sleep: 10
-->

```bash
dapr run --app-id order-processor --components-path ../../../components/ --app-port 5001 -- uvicorn app:app --port 5001
```

<!-- END_STEP -->

### Run Python message publisher with Dapr

1. Install dependencies: 

<!-- STEP
name: Install python dependencies
-->

```bash
cd ./checkout
pip3 install -r requirements.txt 
```
<!-- END_STEP -->

3. Run the Python publisher app with Dapr: 

<!-- STEP
name: Run python publisher
expected_stdout_lines:
  - '== APP == INFO:root:Published data: {"orderId": 1}'
  - '== APP == INFO:root:Published data: {"orderId": 2}'
  - "Exited App successfully"
expected_stderr_lines:
output_match_mode: substring
working_dir: ./checkout
background: true
sleep: 10
-->

```bash
dapr run --app-id checkout --components-path ../../../components/ -- python3 app.py
```

<!-- END_STEP -->

```bash
dapr stop --app-id checkout
dapr stop --app-id order-processor
```
