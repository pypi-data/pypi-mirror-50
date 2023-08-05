# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class ZoneAssociation(pulumi.CustomResource):
    vpc_id: pulumi.Output[str]
    """
    The VPC to associate with the private hosted zone.
    """
    vpc_region: pulumi.Output[str]
    """
    The VPC's region. Defaults to the region of the AWS provider.
    """
    zone_id: pulumi.Output[str]
    """
    The private hosted zone to associate.
    """
    def __init__(__self__, resource_name, opts=None, vpc_id=None, vpc_region=None, zone_id=None, __name__=None, __opts__=None):
        """
        Create a ZoneAssociation resource with the given unique name, props, and options.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] vpc_id: The VPC to associate with the private hosted zone.
        :param pulumi.Input[str] vpc_region: The VPC's region. Defaults to the region of the AWS provider.
        :param pulumi.Input[str] zone_id: The private hosted zone to associate.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/route53_zone_association.html.markdown.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if not resource_name:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(resource_name, str):
            raise TypeError('Expected resource name to be a string')
        if opts and not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if vpc_id is None:
            raise TypeError("Missing required property 'vpc_id'")
        __props__['vpc_id'] = vpc_id

        __props__['vpc_region'] = vpc_region

        if zone_id is None:
            raise TypeError("Missing required property 'zone_id'")
        __props__['zone_id'] = zone_id

        super(ZoneAssociation, __self__).__init__(
            'aws:route53/zoneAssociation:ZoneAssociation',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

