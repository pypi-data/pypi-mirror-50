# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class RateBasedRule(pulumi.CustomResource):
    metric_name: pulumi.Output[str]
    """
    The name or description for the Amazon CloudWatch metric of this rule.
    """
    name: pulumi.Output[str]
    """
    The name or description of the rule.
    """
    predicates: pulumi.Output[list]
    """
    The objects to include in a rule (documented below).
    """
    rate_key: pulumi.Output[str]
    """
    Valid value is IP.
    """
    rate_limit: pulumi.Output[float]
    """
    The maximum number of requests, which have an identical value in the field specified by the RateKey, allowed in a five-minute period. Minimum value is 2000.
    """
    def __init__(__self__, resource_name, opts=None, metric_name=None, name=None, predicates=None, rate_key=None, rate_limit=None, __name__=None, __opts__=None):
        """
        Provides a WAF Rate Based Rule Resource
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] metric_name: The name or description for the Amazon CloudWatch metric of this rule.
        :param pulumi.Input[str] name: The name or description of the rule.
        :param pulumi.Input[list] predicates: The objects to include in a rule (documented below).
        :param pulumi.Input[str] rate_key: Valid value is IP.
        :param pulumi.Input[float] rate_limit: The maximum number of requests, which have an identical value in the field specified by the RateKey, allowed in a five-minute period. Minimum value is 2000.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/wafregional_rate_based_rule.html.markdown.
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

        if metric_name is None:
            raise TypeError("Missing required property 'metric_name'")
        __props__['metric_name'] = metric_name

        __props__['name'] = name

        __props__['predicates'] = predicates

        if rate_key is None:
            raise TypeError("Missing required property 'rate_key'")
        __props__['rate_key'] = rate_key

        if rate_limit is None:
            raise TypeError("Missing required property 'rate_limit'")
        __props__['rate_limit'] = rate_limit

        super(RateBasedRule, __self__).__init__(
            'aws:wafregional/rateBasedRule:RateBasedRule',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

