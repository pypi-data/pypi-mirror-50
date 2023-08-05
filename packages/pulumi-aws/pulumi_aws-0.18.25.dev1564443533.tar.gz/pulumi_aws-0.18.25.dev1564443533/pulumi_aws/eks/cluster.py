# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class Cluster(pulumi.CustomResource):
    arn: pulumi.Output[str]
    """
    The Amazon Resource Name (ARN) of the cluster.
    """
    certificate_authority: pulumi.Output[dict]
    """
    Nested attribute containing `certificate-authority-data` for your cluster.
    """
    created_at: pulumi.Output[str]
    enabled_cluster_log_types: pulumi.Output[list]
    """
    A list of the desired control plane logging to enable. For more information, see [Amazon EKS Control Plane Logging](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html)
    """
    endpoint: pulumi.Output[str]
    """
    The endpoint for your Kubernetes API server.
    """
    name: pulumi.Output[str]
    """
    Name of the cluster.
    """
    platform_version: pulumi.Output[str]
    """
    The platform version for the cluster.
    """
    role_arn: pulumi.Output[str]
    """
    The Amazon Resource Name (ARN) of the IAM role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf.
    """
    version: pulumi.Output[str]
    """
    Desired Kubernetes master version. If you do not specify a value, the latest available version at resource creation is used and no upgrades will occur except those automatically triggered by EKS. The value must be configured and increased to upgrade the version when desired. Downgrades are not supported by EKS.
    """
    vpc_config: pulumi.Output[dict]
    """
    Nested argument for the VPC associated with your cluster. Amazon EKS VPC resources have specific requirements to work properly with Kubernetes. For more information, see [Cluster VPC Considerations](https://docs.aws.amazon.com/eks/latest/userguide/network_reqs.html) and [Cluster Security Group Considerations](https://docs.aws.amazon.com/eks/latest/userguide/sec-group-reqs.html) in the Amazon EKS User Guide. Configuration detailed below.
    """
    def __init__(__self__, resource_name, opts=None, enabled_cluster_log_types=None, name=None, role_arn=None, version=None, vpc_config=None, __name__=None, __opts__=None):
        """
        Manages an EKS Cluster.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] enabled_cluster_log_types: A list of the desired control plane logging to enable. For more information, see [Amazon EKS Control Plane Logging](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html)
        :param pulumi.Input[str] name: Name of the cluster.
        :param pulumi.Input[str] role_arn: The Amazon Resource Name (ARN) of the IAM role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf.
        :param pulumi.Input[str] version: Desired Kubernetes master version. If you do not specify a value, the latest available version at resource creation is used and no upgrades will occur except those automatically triggered by EKS. The value must be configured and increased to upgrade the version when desired. Downgrades are not supported by EKS.
        :param pulumi.Input[dict] vpc_config: Nested argument for the VPC associated with your cluster. Amazon EKS VPC resources have specific requirements to work properly with Kubernetes. For more information, see [Cluster VPC Considerations](https://docs.aws.amazon.com/eks/latest/userguide/network_reqs.html) and [Cluster Security Group Considerations](https://docs.aws.amazon.com/eks/latest/userguide/sec-group-reqs.html) in the Amazon EKS User Guide. Configuration detailed below.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/eks_cluster.html.markdown.
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

        __props__['enabled_cluster_log_types'] = enabled_cluster_log_types

        __props__['name'] = name

        if role_arn is None:
            raise TypeError("Missing required property 'role_arn'")
        __props__['role_arn'] = role_arn

        __props__['version'] = version

        if vpc_config is None:
            raise TypeError("Missing required property 'vpc_config'")
        __props__['vpc_config'] = vpc_config

        __props__['arn'] = None
        __props__['certificate_authority'] = None
        __props__['created_at'] = None
        __props__['endpoint'] = None
        __props__['platform_version'] = None

        super(Cluster, __self__).__init__(
            'aws:eks/cluster:Cluster',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

