# -*- coding: utf-8 -*-

"""Module deleting all aws EKS cluster resources."""

import logging
import time

import boto3

from botocore.exceptions import ClientError, EndpointConnectionError


def nuke_all_eks(older_than_seconds):
    """EKS cluster deleting function.

    Deleting all EKS clusters with a timestamp greater
    than older_than_seconds.

    :param int older_than_seconds:
        The timestamp in seconds used from which the aws
        resource will be deleted
    """
    # Convert date in seconds
    time_delete = time.time() - older_than_seconds

    # Define connection
    eks = boto3.client("eks")

    try:
        eks.list_clusters()
    except EndpointConnectionError:
        print("eks resource is not available in this aws region")
        return

    # List all eks cluster
    eks_cluster_list = eks_list_clusters(time_delete)

    # Nuke all eks cluster
    for cluster in eks_cluster_list:

        # Delete eks cluster
        try:
            eks.delete_cluster(name=cluster)
            print("Nuke EKS Cluster{0}".format(cluster))
        except ClientError as e:
            logging.error("Unexpected error: %s", e)


def eks_list_clusters(time_delete):
    """EKS cluster list function.

    List the names of all EKS clusters with
    a timestamp lower than time_delete.

    :param int time_delete:
        Timestamp in seconds used for filter EKS clusters
    :returns:
        List of EKS cluster names
    :rtype:
        [str]
    """
    # Define the connection
    eks = boto3.client("eks")
    response = eks.list_clusters()

    # Initialize eks cluster list
    eks_cluster_list = []

    # Retrieve all eks cluster
    for kube in response["clusters"]:
        k8s = eks.describe_cluster(name=kube)
        if k8s["cluster"]["createdAt"].timestamp() < time_delete:

            eks_cluster = kube
            eks_cluster_list.insert(0, eks_cluster)

    return eks_cluster_list
