# -*- coding: utf-8 -*-

"""Module deleting all network acl."""

from typing import Iterator

import boto3

from botocore.exceptions import ClientError

from nuke.exceptions import nuke_exceptions


class NukeNetworkAcl:
    """Abstract network acl nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize endpoint nuke."""
        if region_name:
            self.ec2 = boto3.client("ec2", region_name=region_name)
        else:
            self.ec2 = boto3.client("ec2")

    def nuke(self) -> None:
        """Network acl delete function."""
        for net_acl in self.list_network_acls():
            try:
                self.ec2.delete_network_acl(NetworkAclId=net_acl)
                print("Nuke ec2 network acl {0}".format(net_acl))
            except ClientError as exc:
                nuke_exceptions("network acl", net_acl, exc)

    def list_network_acls(self) -> Iterator[str]:
        """Network acl list function.

        :yield Iterator[str]:
            Network acl Id
        """
        response = self.ec2.describe_network_acls()

        for network_acl in response["NetworkAcls"]:
            yield network_acl["NetworkAclId"]
