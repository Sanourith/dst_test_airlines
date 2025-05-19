#! /bin/bash
set -e

# TODO think about Dockerfiles for APPS

NAMESPACE="airlines"
MYSQL_CONFIGMAP_NAME="mysql-init-scripts"

echo "Deploying all mysql suite..."

kubectl create namespace $NAMESPACE || kubectl get namespace $NAMESPACE
kubectl delete configmap $MYSQL_CONFIGMAP_NAME -n $NAMESPACE --ignore-not-found
kubectl create configmap $MYSQL_CONFIGMAP_NAME \
  -n $NAMESPACE \
  --from-file=create_dst_airlines_database.sql=./mysql/resources/create_dst_airlines_database.sql \
  --from-file=create_dst_airlines_users.sql=./mysql/resources/create_dst_airlines_users.sql

kubectl apply -f mysql/ -n $NAMESPACE

# # POUR TOUT CASSER, commente au dessus et décommente ou utilise les commandes :
# kubectl delete namespace airlines
# kubectl delete pv mysql-pv

# Tu peux aussi test avec k9s !
# tape ": namespace"
# "ctrl + D" sur le namespace
# tape ": pv"
# "ctrl + D" sur le pv
# HOP


print_help() {
  echo "Usage: $0 [deploy|delete] [--app <app>]"
  echo "Options:"
  echo "deploy           Deploy app"
  echo "delete           Delete an app totally"
  echo "  --app <app>    Specify an APP to deploy or delete"
  echo "                 (eg mysql)"
  echo "  -h, --help     Print help"
}

_mysql() {
  local action="$1"
  if [[ "$action" == "deploy" ]]; then
    echo "---------------------------------"
    echo "---      DEPLOYING MYSQL      ---"
    echo "---------------------------------"

    kubectl delete configmap $MYSQL_CONFIGMAP_NAME -n $NAMESPACE --ignore-not-found
    kubectl create configmap $MYSQL_CONFIGMAP_NAME \
      -n $NAMESPACE \
      --from-file=create_dst_airlines_database.sql=./mysql/resources/create_dst_airlines_database.sql \
      --from-file=create_dst_airlines_users.sql=./mysql/resources/create_dst_airlines_users.sql

    kubectl apply -f mysql/ -n $NAMESPACE
    echo "MySQL deployment completed"

  elif [[ "$action" == "delete" ]]; then 
    echo "--------------------------------"
    echo "---      DELETING MYSQL      ---"
    echo "--------------------------------"

    kubectl delete -f mysql/ -n $NAMESPACE --ignore-not-found
    kubectl delete configmap $MYSQL_CONFIGMAP_NAME -n $NAMESPACE --ignore-not-found
    
    echo "MySQL deletion completed"
  fi
}

# TODO

_complete() {
  local action="$1"

  _mysql "$action"
  # other will be added
}

# OPT=$(getopt -o h -l help -l app: -l deploy -l delete -- "$@")
# if [ $? != 0 ]; then
#   echo "Error in options." >&2
#   exit 1
# fi

# APP=""

# eval set -- "$OPT"
# while true; do
#   case "$1" in
#     -h | --help)
#       print_help
#       exit 0
#       ;;
#     --app)
#       APP="$2"
#       shift 2
#       ;;
#     --)
#       shift
#       break
#       ;;
#     *)
#       echo "Unknown option : $1"
#       exit 1
#       ;;

# ACTION="$1"
# if [[ -z "$ACTION" ]]; then
#   echo "Unknown command, use 'deploy' or 'delete'."
#   print_help
#   exit 1
# fi

# echo "Registered action : $ACTION"
# if [[ -n "$APP" ]]; then
#   echo "App concerned : $APP"
# else
#   echo "All apps will be concerned"
# fi

# TODO 
# case $ACTION init
#   deploy)
#     if [[ -z "$APP" ]]; then
#       _complete "deploy"
#     else
#       deploy $APP
#     fi
#   delete)
#     echo ""
#     ;;





# Post Forwarding du webserver

#kubectl port-forward svc/fastapi-service 8000:80 -n airlines
#kubectl port-forward svc/airflow-webserver 8080:8080 --namespace airlines
#kubectl port-forward svc/prometheus-server 9090:80 -n airlines 

#Avoir l'ip cluster
#kubectl get nodes -o wide

# Nécessité d'avoir une storageClass de type local-path, pour le faire sur minikube (https://minikube.sigs.k8s.io/docs/tutorials/local_path_provisioner/) :
# minikube addons enable storage-provisioner-rancher