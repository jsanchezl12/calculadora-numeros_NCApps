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

**_NOTA:_** Instalar kubectl: https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/

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

# Pasos para crear el servicio con una BD en gcp
[Link Tutorial](https://misovirtual.virtual.uniandes.edu.co/codelabs/dann-tutorial-sql/index.html?index=..%2F..desarrollo-aplicaciones-nube#0)

1. Se debe hacer pull de la imagen pero con version vDatabase
```
docker build --platform linux/amd64 -t us-central1-docker.pkg.dev/gcloudprojectg14/uniandes-misw-native-calculadora-app/memory:1.1 .
docker push us-central1-docker.pkg.dev/gcloudprojectg14/uniandes-misw-native-calculadora-app/memory:1.1
docker run --platform linux/amd64 -p 4000:4000 us-central1-docker.pkg.dev/gcloudprojectg14/uniandes-misw-native-calculadora-app/memory:1.1
```
2. crear Subred para la BD

    - Purpose: Función que estará ejecutando la subred y rango de direcciones usadas.
    - Addresses: Rango de direcciones asociadas a la subred.
    - Prefix-length: La nueva longitud del prefijo de la subred. Debe ser más pequeño que el original y en el espacio de direcciones privadas 10.0.0.0/8, 172.16.0.0/12 o 192.168.0.0/16 definido en RFC 1918.
    - Network: Red creada para asociar la subred (Recuerde que si siguio el tutorial de kubernetes, puede usar la misma allí creada).
    - Project: Id del proyecto creado, puede consultarlo en el banner inicial de GCP.

```
# Crear subred
gcloud compute addresses create red-dbs-tutoriales --global --purpose=VPC_PEERING --addresses=192.168.0.0 --prefix-length=24 --network=vpn-tutoriales-misw --project=gcloudprojectg14
# Otorgar acceso a los servicios de GCP
gcloud services vpc-peerings connect --service=servicenetworking.googleapis.com --ranges=red-dbs-tutoriales --network=vpn-tutoriales-misw --project=gcloudprojectg14
# Crear Regla de Firewall
gcloud compute firewall-rules create allow-db-ingress --direction=INGRESS --priority=1000 --network=vpn-tutoriales-misw --action=ALLOW --rules=tcp:5432 --source-ranges=192.168.1.0/24 --target-tags=basesdedatos --project=gcloudprojectg14
```

3. Crear bd Relacional

    - Nombre: misw-tutorial-calculadora-db
    - Contraseña: Generada, más no olvide guardarla en un lugar de fácil acceso. La necesitará más adelante. (DreamTeam123*)
    - Versión: PostgreSQL 14
    - Región: us-central1
    - Disponibilidad zonal: Única
    - Tipo de máquina: De núcleo compartido, 1 core y 1.7 GB de RAM
    - Almacenamiento 10 GB de HDD
    - No habilitar los aumentos automáticos de almacenamiento.
    - Asignación de IP de la instancia: privada
    - Red: vpn-tutoriales-misw
    - Rango de IP asignado: red-dbs-tutoriales
    - Etiqueta: basesdedatos

4. Configurar Secrets.yaml
```
apiVersion: v1
stringData:
  uri : "postgresql+psycopg2://postgres:DREAMTEAM1234*@192.168.0.3/postgres"
kind: Secret
metadata:
  name: appsecrets
```

5. aplicamos los secretos los cuales estan referenciados en el archivo de k8s-service.yml (spec -> template -> spec -> containers -> env -> secretKeyRef -> name)

```
kubectl apply -f secrets.yaml
```

6. Cambiamos la uri de la imagen en el archivo de k8s-service.yml (spec -> template -> spec -> containers -> image)

```
us-central1-docker.pkg.dev/gcloudprojectg14/uniandes-misw-native-calculadora-app/memory:1.1
```

7. Aplicamos los cambios
```
kubectl apply -f k8s-service.yml
```

8. Hacemos un request teniendo la URL del balanceador de carga con el siguiente comando
```
curl --location --request POST 'http://34.29.74.233:80/guardar_numero' \
--header 'Content-Type: application/json' \
--data-raw '{
    "num_1": 399
}'

curl --location --request GET 'http://34.29.74.233:80/ultimo_numero' \
--header 'Content-Type: application/json' \
--data-raw '{
    "num_1": 399
}'
```

# Pasos para configurar Ingress
1. Preparar Ambiente
[Link Tutorial](https://misovirtual.virtual.uniandes.edu.co/codelabs/dann-ingress-kubernetes/index.html?index=..%2F..desarrollo-aplicaciones-nube#0)
```
kubectl delete all --all -n default
````
2. Publicar imagenes con las que se va a trabajar
```
docker build --platform linux/amd64 -t us-central1-docker.pkg.dev/gcloudprojectg14/uniandes-misw-native-calculadora-app/multiplicacion:1.2 .
docker push us-central1-docker.pkg.dev/gcloudprojectg14/uniandes-misw-native-calculadora-app/multiplicacion:1.2
```
3. Se configura el ingress teniendo en cuenta la siguiente informacion

    - Metadata: Acá se define el nombre de cómo llamaremos nuestro ingress, en este caso gateway-ingress.
    - kind: A diferencia de los anteriores fragmentos de este archivo que corresponden a kind de tipo service, en esta ocasión corresponde a un kind de tipo ingress.
    - rules: Acá se definen reglas de tráfico como los endpoints asociados a cada microservicio y el puerto que exponen para redirigir el tráfico.
    - service: Describe el contenido de cada servicio usado dentro del ingress.
    - name: Nombre único del microservicio (Este debe coincidir con el asignado en linear arriba, debe llamarse igual para que kubernetes lo reconozca)
    - pathType: El campo pathType especifica una de las tres formas en que se debe interpretar la ruta de un objeto de ingreso:
        - ImplementationSpecific: la coincidencia de prefijo de ruta se delega al controlador de ingreso (IngressClass).
        - Exact: coincide exactamente con la ruta de la URL (se distingue entre mayúsculas y minúsculas)
        - Prefix: coincidencias basadas en un prefijo de ruta de URL dividido por /. La coincidencia distingue entre mayúsculas y minúsculas y se realiza elemento por elemento de ruta. 
4. Aplicamos los cambios
```
kubectl apply -f k8s-deployments.yml
```
5. Probamos que los servicios esten funcionando
```
curl --location --request POST 'http://35.186.228.169/suma' \
--header 'Content-Type: application/json' \
--data-raw '{
    "num_1": 379,
    "num_2": 1
}'

curl --location --request POST 'http://35.186.228.169/multiplicar' \
--header 'Content-Type: application/json' \
--data-raw '{
    "num_1": 390,
    "num_2": 1
}'
```

