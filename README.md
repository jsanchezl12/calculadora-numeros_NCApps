# Calculadora de números

Para levantar el proyecto en su repositorio local, ejecute los siguientes pasos:

### 1. Instalar ambiente virtual:

En su terminal ejecute:
```
pip install virtualenv
```
Cuando la descarga finalize cree el ambiente virtual mediante:
```
virtualenv vnv
```
Esto creara en la carpeta local, archivos necesarios para aislar un ambiente de dependencias en Python, activelo mediante:
```
source vnv/bin/activate
```
Posteriormente baje las dependencias mediante:
```
pip install -r requirements.txt
```
### 2. Levantar la API:
En su terminal ejecute:
```
python3 -m flask run
``` 
### 3. Curl para sumar el dos números:
```
curl --location --request POST 'http://localhost:4000/suma' \
--header 'Content-Type: application/json' \
--data-raw '{    
    "num_1" : 2,
    "num_2": 3
}'

```
us-central1-docker.pkg.dev/gcloudprojectg14/uniandes-misw-native-calculadora-app/suma:1.0
# Pasos para inicializar gcloud
1. Instalar gcloud en mac o  descargar carpeta google-cloud-sdk
https://cloud.google.com/sdk/docs/install?hl=es-419

```./google-cloud-sdk/install.sh```

2. Iniciar sesión en gcloud

```./google-cloud-sdk/bin/gcloud init```

3. Verificar proyect id: gcloudprojectg14

```gcloud config get-value project```

4. Verificar autenticación para subir imagenes de docker con su zona de gcp

```gcloud auth configure-docker us-central1-docker.pkg.dev```


# Pasos para crear la imagen de docker

1. Crear el archivo Dockerfile
2. Construir la imagen con el siguiente comando teniendo en cuenta el nombre del grupo en gcp (gcloudprojectg14)
```
## Para otras plataformas
docker build -t us-central1-docker.pkg.dev/gcloudprojectg14/uniandes-misw-native-calculadora-app/suma:1.1 .
## Para mac m1
docker build --platform linux/amd64 -t us-central1-docker.pkg.dev/gcloudprojectg14/uniandes-misw-native-calculadora-app/suma:1.1 .
## Inspeccionar imagen para revisar Arquitetura
docker inspect us-central1-docker.pkg.dev/gcloudprojectg14/uniandes-misw-native-calculadora-app/suma:1.1 
```
3. Subir la imagen a gcp (Artifact Registry)
```
docker push us-central1-docker.pkg.dev/gcloudprojectg14/uniandes-misw-native-calculadora-app/suma:1.1
```
4. Corremos la imagen localmente
```
## Para otras plataformas
docker run -p 4000:4000 us-central1-docker.pkg.dev/gcloudprojectg14/uniandes-misw-native-calculadora-app/suma:1.1
## Para mac m1
docker run --platform linux/amd64 -p 4000:4000 us-central1-docker.pkg.dev/gcloudprojectg14/uniandes-misw-native-calculadora-app/suma:1.1
```

5. Probamos la imagen
```
curl --location --request POST 'http://localhost:4000/suma' \
--header 'Content-Type: application/json' \
--data-raw '{
    "num_1" : 12,
    "num_2": 3
}'
```
# Pasos para crear el cluster de kubernetes en gcp
1. Creamos una red virtual en gcp
```
gcloud compute networks create vpn-tutoriales-misw --project=gcloudprojectg14 --subnet-mode=custom --mtu=1460 --bgp-routing-mode=regional
```
2. Creamos una subred en gcp
```
gcloud compute networks subnets create red-k8s-tutoriales --range=192.168.32.0/19 --network=vpn-tutoriales-misw --region=us-central1 --project=gcloudprojectg14
```
3. Crear cluster de kubernetes en gcp ---> Autopilot
```
    Nombre: uniandes-misw-cloud-native-k8s
    Region: us-central1
    Red: vpn-tutoriales-misw
    Subred del nodo: red-k8s-tutoriales
    Rango de direcciones del pod: 192.168.64.0/21
    Rango de direcciones del servicio: 192.168.72.0/21
```
4. Conexion a Cluster
```
gcloud container clusters get-credentials uniandes-misw-cloud-native-k8s --region us-central1 --project gcloudprojectg14
```
5. Modificamos el archivo de K8s-service.yml para que apunte a la imagen de docker en gcp (spec -> template -> spec -> containers -> image)

6. Modificamos el servicio en k8s
    - Creacion: ```kubectl create -f K8s-service.yml```
    - Remplazamos: ```kubectl replace -f K8s-service.yml```
    - Eliminacion: ```kubectl delete -f K8s-service.yml```
    - Actualizacion: ```kubectl apply -f K8s-service.yml```

7. revisamos pods

```kubectl get pods```

8. revisamos servicios

```kubectl get services```

9. revisamos deployment

```kubectl get deployment```

10. Revisar pods con los comandos

```
kubectl describe pod <nombre del pod>
kubectl logs <nombre del pod> --all-containers=true
kubectl logs -f <nombre del pod> 
kubectl get events
```

11. Probar servicio

```
curl --location --request POST 'http://34.69.180.86:80/suma' \
--header 'Content-Type: application/json' \
--data-raw '{
    "num_1": 399,
    "num_2": 1
}'
```

