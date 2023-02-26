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

# Pasos para crear la imagen de docker

1. Crear el archivo Dockerfile
2. Construir la imagen con el siguiente comando teniendo en cuenta el nombre del grupo en gcp (gcloudprojectg14)
docker build -t us-central1-docker.pkg.dev/gcloudprojectg14/uniandes-misw-native-calculadora-app/suma:1.1 .
3. Subir la imagen a gcp
docker push us-central1-docker.pkg.dev/gcloudprojectg14/uniandes-misw-native-calculadora-app/suma:1.1
4. Corremos la imagen localmente
docker run -p 4000:4000 us-central1-docker.pkg.dev/gcloudprojectg14/uniandes-misw-native-calculadora-app/suma:1.1
5. Probamos la imagen
```
curl --location --request POST 'http://localhost:4000/suma' \
--header 'Content-Type: application/json' \
--data-raw '{
    "num_1" : 12,
    "num_2": 3
}'
```

6. Creamos una red virtual en gcp
gcloud compute networks create vpn-tutoriales-misw --project=gcloudprojectg14 --subnet-mode=custom --mtu=1460 --bgp-routing-mode=regional
7. Creamos una subred en gcp
gcloud compute networks subnets create red-k8s-tutoriales --range=192.168.32.0/19 --network=vpn-tutoriales-misw --region=us-central1 --project=gcloudprojectg14
8. Crear cluster de kubernetes en gcp ---> Autopilot
    Nombre: uniandes-misw-cloud-native-k8s
    Region: us-central1
    Red: vpn-tutoriales-misw
    Subred del nodo: red-k8s-tutoriales
    Rango de direcciones del pod: 192.168.64.0/21
    Rango de direcciones del servicio: 192.168.72.0/21

9. Conexion a Cluster
gcloud container clusters get-credentials uniandes-misw-cloud-native-k8s --region us-central1 --project gcloudprojectg14

