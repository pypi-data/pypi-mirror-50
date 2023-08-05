# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class Listener(pulumi.CustomResource):
    arn: pulumi.Output[str]
    """
    The ARN of the listener (matches `id`)
    """
    certificate_arn: pulumi.Output[str]
    """
    The ARN of the default SSL server certificate. Exactly one certificate is required if the protocol is HTTPS. For adding additional SSL certificates, see the [`aws_lb_listener_certificate` resource](https://www.terraform.io/docs/providers/aws/r/lb_listener_certificate.html).
    """
    default_actions: pulumi.Output[list]
    """
    An Action block. Action blocks are documented below.
    """
    load_balancer_arn: pulumi.Output[str]
    """
    The ARN of the load balancer.
    """
    port: pulumi.Output[float]
    """
    The port. Specify a value from `1` to `65535` or `#{port}`. Defaults to `#{port}`.
    """
    protocol: pulumi.Output[str]
    """
    The protocol. Valid values are `HTTP`, `HTTPS`, or `#{protocol}`. Defaults to `#{protocol}`.
    """
    ssl_policy: pulumi.Output[str]
    """
    The name of the SSL Policy for the listener. Required if `protocol` is `HTTPS` or `TLS`.
    """
    def __init__(__self__, resource_name, opts=None, certificate_arn=None, default_actions=None, load_balancer_arn=None, port=None, protocol=None, ssl_policy=None, __name__=None, __opts__=None):
        """
        Provides a Load Balancer Listener resource.
        
        > **Note:** `aws_alb_listener` is known as `aws_lb_listener`. The functionality is identical.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] certificate_arn: The ARN of the default SSL server certificate. Exactly one certificate is required if the protocol is HTTPS. For adding additional SSL certificates, see the [`aws_lb_listener_certificate` resource](https://www.terraform.io/docs/providers/aws/r/lb_listener_certificate.html).
        :param pulumi.Input[list] default_actions: An Action block. Action blocks are documented below.
        :param pulumi.Input[str] load_balancer_arn: The ARN of the load balancer.
        :param pulumi.Input[float] port: The port. Specify a value from `1` to `65535` or `#{port}`. Defaults to `#{port}`.
        :param pulumi.Input[str] protocol: The protocol. Valid values are `HTTP`, `HTTPS`, or `#{protocol}`. Defaults to `#{protocol}`.
        :param pulumi.Input[str] ssl_policy: The name of the SSL Policy for the listener. Required if `protocol` is `HTTPS` or `TLS`.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/lb_listener.html.markdown.
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

        __props__['certificate_arn'] = certificate_arn

        if default_actions is None:
            raise TypeError("Missing required property 'default_actions'")
        __props__['default_actions'] = default_actions

        if load_balancer_arn is None:
            raise TypeError("Missing required property 'load_balancer_arn'")
        __props__['load_balancer_arn'] = load_balancer_arn

        if port is None:
            raise TypeError("Missing required property 'port'")
        __props__['port'] = port

        __props__['protocol'] = protocol

        __props__['ssl_policy'] = ssl_policy

        __props__['arn'] = None

        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="aws:elasticloadbalancingv2/listener:Listener")])
        opts = alias_opts if opts is None else opts.merge(alias_opts)
        super(Listener, __self__).__init__(
            'aws:lb/listener:Listener',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

