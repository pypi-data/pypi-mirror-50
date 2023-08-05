# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class GetSecurityGroupsResult:
    """
    A collection of values returned by getSecurityGroups.
    """
    def __init__(__self__, filters=None, ids=None, tags=None, vpc_ids=None, id=None):
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        __self__.filters = filters
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        __self__.ids = ids
        """
        IDs of the matches security groups.
        """
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        __self__.tags = tags
        if vpc_ids and not isinstance(vpc_ids, list):
            raise TypeError("Expected argument 'vpc_ids' to be a list")
        __self__.vpc_ids = vpc_ids
        """
        The VPC IDs of the matched security groups. The data source's tag or filter *will span VPCs*
        unless the `vpc-id` filter is also used.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """

async def get_security_groups(filters=None,tags=None,opts=None):
    """
    > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/d/security_groups.html.markdown.
    """
    __args__ = dict()

    __args__['filters'] = filters
    __args__['tags'] = tags
    __ret__ = await pulumi.runtime.invoke('aws:ec2/getSecurityGroups:getSecurityGroups', __args__, opts=opts)

    return GetSecurityGroupsResult(
        filters=__ret__.get('filters'),
        ids=__ret__.get('ids'),
        tags=__ret__.get('tags'),
        vpc_ids=__ret__.get('vpcIds'),
        id=__ret__.get('id'))
