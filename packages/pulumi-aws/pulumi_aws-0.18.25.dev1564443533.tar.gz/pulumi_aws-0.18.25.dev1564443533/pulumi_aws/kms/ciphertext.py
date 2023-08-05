# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class Ciphertext(pulumi.CustomResource):
    ciphertext_blob: pulumi.Output[str]
    """
    Base64 encoded ciphertext
    """
    context: pulumi.Output[dict]
    """
    An optional mapping that makes up the encryption context.
    """
    key_id: pulumi.Output[str]
    """
    Globally unique key ID for the customer master key.
    """
    plaintext: pulumi.Output[str]
    """
    Data to be encrypted. Note that this may show up in logs, and it will be stored in the state file.
    """
    def __init__(__self__, resource_name, opts=None, context=None, key_id=None, plaintext=None, __name__=None, __opts__=None):
        """
        The KMS ciphertext resource allows you to encrypt plaintext into ciphertext
        by using an AWS KMS customer master key. The value returned by this resource
        is stable across every apply. For a changing ciphertext value each apply, see
        the [`aws_kms_ciphertext` data source](https://www.terraform.io/docs/providers/aws/d/kms_ciphertext.html).
        
        > **Note:** All arguments including the plaintext be stored in the raw state as plain-text.
        [Read more about sensitive data in state](https://www.terraform.io/docs/state/sensitive-data.html).
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[dict] context: An optional mapping that makes up the encryption context.
        :param pulumi.Input[str] key_id: Globally unique key ID for the customer master key.
        :param pulumi.Input[str] plaintext: Data to be encrypted. Note that this may show up in logs, and it will be stored in the state file.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/kms_ciphertext.html.markdown.
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

        __props__['context'] = context

        if key_id is None:
            raise TypeError("Missing required property 'key_id'")
        __props__['key_id'] = key_id

        if plaintext is None:
            raise TypeError("Missing required property 'plaintext'")
        __props__['plaintext'] = plaintext

        __props__['ciphertext_blob'] = None

        super(Ciphertext, __self__).__init__(
            'aws:kms/ciphertext:Ciphertext',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

