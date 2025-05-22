#! /bin/bash
set -e

# TODO think about Dockerfiles for APPS

NAMESPACE="airlines"
MYSQL_CONFIGMAP_NAME="mysql-init-scripts"

kubectl create namespace $NAMESPACE || kubectl get namespace $NAMESPACE

print_help() {
  echo "Usage: $0 [deploy|delete] [--app <app>]"
  echo "Options:"
  echo "  deploy           Deploy app(s)"
  echo "  delete           Delete app(s) totally"
  echo "  --app <app>      Specify an APP to deploy or delete"
  echo "                   Available apps: mysql, all (default: all)"
  echo "  -h, --help       Print help"
  echo ""
  echo "Examples:"
  echo "  $0 deploy                    # Deploy all apps"
  echo "  $0 deploy --app mysql        # Deploy only MySQL"
  echo "  $0 delete --app mysql        # Delete only MySQL"
}

_mysql() {
  local action="$1"
  if [[ "$action" == "deploy" ]]; then
    echo "---------------------------------"
    echo "---      DEPLOYING MYSQL      ---"
    echo "---------------------------------"

    # Verify if .sql files are present
    if [[ ! -f "./mysql/resources/create_dst_airlines_database.sql" ]] || [[ ! -f "./mysql/resources/create_dst_airlines_users.sql" ]]; then
      echo "Error: MySQL SQL files not found in ./mysql/resources/"
      return 1
    fi

    kubectl delete configmap $MYSQL_CONFIGMAP_NAME -n $NAMESPACE --ignore-not-found
    kubectl create configmap $MYSQL_CONFIGMAP_NAME \
      -n $NAMESPACE \
      --from-file=create_dst_airlines_database.sql=./mysql/resources/create_dst_airlines_database.sql \
      --from-file=create_dst_airlines_users.sql=./mysql/resources/create_dst_airlines_users.sql

    if [[ ! -d "./mysql" ]]; then
      echo "Error: mysql directory not found"
      return 1
    fi

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

_deploy_app() {
  local app="$1"
  local action="$2"

  case $app in
    mysql)
      _mysql "$action"
      ;;
    # AUTRES APPS ICI
    *)
      echo "Error : Unknown app '$app'"
      echo "Available apps : mysql"
      return 1
      ;;
  esac
}

_complete() {
  local action="$1"

  _mysql "$action"
  # other will be added
}

OPT=$(getopt -o h -l help,app: -- "$@")
if [ $? != 0 ]; then
  echo "Error in options." >&2
  print_help
  exit 1
fi

APP=""

eval set -- "$OPT"
while true; do
  case "$1" in
    -h | --help)
      print_help
      exit 0
      ;;
    --app)
      APP="$2"
      shift 2
      ;;
    --)
      shift
      break
      ;;
    *)
      echo "Unknown option: $1"
      print_help
      exit 1
      ;;
  esac
done

ACTION="$1"
if [[ -z "$ACTION" ]]; then
  echo "Error: No action specified. Use 'deploy' or 'delete'."
  print_help
  exit 1
fi

# Valider l'action
if [[ "$ACTION" != "deploy" && "$ACTION" != "delete" ]]; then
  echo "Error: Invalid action '$ACTION'. Use 'deploy' or 'delete'."
  print_help
  exit 1
fi

echo "Registered action: $ACTION"
if [[ -n "$APP" ]]; then
  echo "App concerned: $APP"
else
  echo "All apps will be processed"
fi

# Exécuter l'action
case "$ACTION" in
  deploy)
    if [[ -z "$APP" || "$APP" == "all" ]]; then
      _complete "deploy"
    else
      _deploy_app "$APP" "deploy"
    fi
    ;;
  delete)
    if [[ -z "$APP" || "$APP" == "all" ]]; then
      _complete "delete"
    else
      _deploy_app "$APP" "delete"
    fi
    ;;
esac

echo "Operation completed."




# Post Forwarding du webserver

#kubectl port-forward svc/fastapi-service 8000:80 -n airlines
#kubectl port-forward svc/airflow-webserver 8080:8080 --namespace airlines
#kubectl port-forward svc/prometheus-server 9090:80 -n airlines 

#Avoir l'ip cluster
#kubectl get nodes -o wide

# Nécessité d'avoir une storageClass de type local-path, pour le faire sur minikube (https://minikube.sigs.k8s.io/docs/tutorials/local_path_provisioner/) :
# minikube addons enable storage-provisioner-rancher