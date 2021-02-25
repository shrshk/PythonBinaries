from kubernetes import client, config
import json
import logging

SUPPORTED_METHODS = ["pod_logs", "list_pod_for_all_namespaces", "list_namespaced_event"]

def handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.debug(json.dumps(event))

    config.load_kube_config()

    api_client = client.CoreV1Api()

    for key in event:
        if key in SUPPORTED_METHODS:
            globals()[key](event[key], api_client)


def list_pod_for_all_namespaces(args, api_client):
    logger.debug("Listing pods with their IPs:")
    ret = api_client.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        logger.debug("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


def pod_logs(args, api_client):
    for pod_arg in args:
        namespace = pod_arg['namespace']
        pod_name = pod_arg['pod_name']
        pod_log = api_client.read_namespaced_pod_log(name=pod_name, namespace=namespace)
        logger.debug("logs for pod_name: " + pod_name + "in namespace: " + namespace)
        logger.debug(pod_log)

def list_namespaced_event(args, api_client):
    for pod_arg in args:
        namespace = pod_arg['namespace']
        pod_name = pod_arg['pod_name']
        namespaced_event = api_client.list_namespaced_event(name=pod_name, namespace=namespace)
        logger.debug("list event for pod_name: " + pod_name + "in namespace: " + namespace)
        logger.debug(namespaced_event)
