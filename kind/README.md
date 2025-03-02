```shell
kind create cluster --name=kindle --config kind-config-cluster.yml 
docker build -t systemdevformations/kindle-modi .
docker tag  kindle-mobi systemdevformations/kindle-modi
docker login
docker push systemdevformations/kindle-mobi
```


```shell
kind create cluster --name kindle --config kind-config-cluster.yml

kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/kind/deploy.yaml

curl -skSL https://raw.githubusercontent.com/kubernetes-csi/csi-driver-nfs/v4.9.0/deploy/install-driver.sh | bash -s v4.9.0 --
```