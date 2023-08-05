# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class LogStream(pulumi.CustomResource):
    arn: pulumi.Output[str]
    """
    The Amazon Resource Name (ARN) specifying the log stream.
    """
    log_group_name: pulumi.Output[str]
    """
    The name of the log group under which the log stream is to be created.
    """
    name: pulumi.Output[str]
    """
    The name of the log stream. Must not be longer than 512 characters and must not contain `:`
    """
    def __init__(__self__, resource_name, opts=None, log_group_name=None, name=None, __name__=None, __opts__=None):
        """
        Provides a CloudWatch Log Stream resource.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] log_group_name: The name of the log group under which the log stream is to be created.
        :param pulumi.Input[str] name: The name of the log stream. Must not be longer than 512 characters and must not contain `:`

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/cloudwatch_log_stream.html.markdown.
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

        if log_group_name is None:
            raise TypeError("Missing required property 'log_group_name'")
        __props__['log_group_name'] = log_group_name

        __props__['name'] = name

        __props__['arn'] = None

        super(LogStream, __self__).__init__(
            'aws:cloudwatch/logStream:LogStream',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

