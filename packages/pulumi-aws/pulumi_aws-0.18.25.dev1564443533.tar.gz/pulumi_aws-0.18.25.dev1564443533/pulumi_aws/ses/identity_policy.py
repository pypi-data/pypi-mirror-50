# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class IdentityPolicy(pulumi.CustomResource):
    identity: pulumi.Output[str]
    """
    Name or Amazon Resource Name (ARN) of the SES Identity.
    """
    name: pulumi.Output[str]
    """
    Name of the policy.
    """
    policy: pulumi.Output[str]
    def __init__(__self__, resource_name, opts=None, identity=None, name=None, policy=None, __name__=None, __opts__=None):
        """
        Manages a SES Identity Policy. More information about SES Sending Authorization Policies can be found in the [SES Developer Guide](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/sending-authorization-policies.html).
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] identity: Name or Amazon Resource Name (ARN) of the SES Identity.
        :param pulumi.Input[str] name: Name of the policy.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/ses_identity_policy.html.markdown.
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

        if identity is None:
            raise TypeError("Missing required property 'identity'")
        __props__['identity'] = identity

        __props__['name'] = name

        if policy is None:
            raise TypeError("Missing required property 'policy'")
        __props__['policy'] = policy

        super(IdentityPolicy, __self__).__init__(
            'aws:ses/identityPolicy:IdentityPolicy',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

