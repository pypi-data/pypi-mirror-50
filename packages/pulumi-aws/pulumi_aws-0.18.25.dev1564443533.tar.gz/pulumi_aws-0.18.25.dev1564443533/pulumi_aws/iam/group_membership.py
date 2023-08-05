# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class GroupMembership(pulumi.CustomResource):
    group: pulumi.Output[str]
    """
    The IAM Group name to attach the list of `users` to
    """
    name: pulumi.Output[str]
    """
    The name to identify the Group Membership
    """
    users: pulumi.Output[list]
    """
    A list of IAM User names to associate with the Group
    """
    def __init__(__self__, resource_name, opts=None, group=None, name=None, users=None, __name__=None, __opts__=None):
        """
        > **WARNING:** Multiple aws_iam_group_membership resources with the same group name will produce inconsistent behavior!
        
        Provides a top level resource to manage IAM Group membership for IAM Users. For
        more information on managing IAM Groups or IAM Users, see [IAM Groups][1] or
        [IAM Users][2]
        
        > **Note:** `aws_iam_group_membership` will conflict with itself if used more than once with the same group. To non-exclusively manage the users in a group, see the
        [`aws_iam_user_group_membership` resource][3].
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] group: The IAM Group name to attach the list of `users` to
        :param pulumi.Input[str] name: The name to identify the Group Membership
        :param pulumi.Input[list] users: A list of IAM User names to associate with the Group

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/iam_group_membership.html.markdown.
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

        if group is None:
            raise TypeError("Missing required property 'group'")
        __props__['group'] = group

        __props__['name'] = name

        if users is None:
            raise TypeError("Missing required property 'users'")
        __props__['users'] = users

        super(GroupMembership, __self__).__init__(
            'aws:iam/groupMembership:GroupMembership',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

