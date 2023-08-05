# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class GetReportDefinitionResult:
    """
    A collection of values returned by getReportDefinition.
    """
    def __init__(__self__, additional_artifacts=None, additional_schema_elements=None, compression=None, format=None, report_name=None, s3_bucket=None, s3_prefix=None, s3_region=None, time_unit=None, id=None):
        if additional_artifacts and not isinstance(additional_artifacts, list):
            raise TypeError("Expected argument 'additional_artifacts' to be a list")
        __self__.additional_artifacts = additional_artifacts
        """
        A list of additional artifacts.
        """
        if additional_schema_elements and not isinstance(additional_schema_elements, list):
            raise TypeError("Expected argument 'additional_schema_elements' to be a list")
        __self__.additional_schema_elements = additional_schema_elements
        """
        A list of schema elements.
        """
        if compression and not isinstance(compression, str):
            raise TypeError("Expected argument 'compression' to be a str")
        __self__.compression = compression
        """
        Preferred format for report.
        """
        if format and not isinstance(format, str):
            raise TypeError("Expected argument 'format' to be a str")
        __self__.format = format
        """
        Preferred compression format for report.
        """
        if report_name and not isinstance(report_name, str):
            raise TypeError("Expected argument 'report_name' to be a str")
        __self__.report_name = report_name
        if s3_bucket and not isinstance(s3_bucket, str):
            raise TypeError("Expected argument 's3_bucket' to be a str")
        __self__.s3_bucket = s3_bucket
        """
        Name of customer S3 bucket.
        """
        if s3_prefix and not isinstance(s3_prefix, str):
            raise TypeError("Expected argument 's3_prefix' to be a str")
        __self__.s3_prefix = s3_prefix
        """
        Preferred report path prefix.
        """
        if s3_region and not isinstance(s3_region, str):
            raise TypeError("Expected argument 's3_region' to be a str")
        __self__.s3_region = s3_region
        """
        Region of customer S3 bucket.
        """
        if time_unit and not isinstance(time_unit, str):
            raise TypeError("Expected argument 'time_unit' to be a str")
        __self__.time_unit = time_unit
        """
        The frequency on which report data are measured and displayed.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """

async def get_report_definition(report_name=None,opts=None):
    """
    Use this data source to get information on an AWS Cost and Usage Report Definition.
    
    > *NOTE:* The AWS Cost and Usage Report service is only available in `us-east-1` currently.
    
    > *NOTE:* If AWS Organizations is enabled, only the master account can use this resource.

    > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/d/cur_report_definition.html.markdown.
    """
    __args__ = dict()

    __args__['reportName'] = report_name
    __ret__ = await pulumi.runtime.invoke('aws:cur/getReportDefinition:getReportDefinition', __args__, opts=opts)

    return GetReportDefinitionResult(
        additional_artifacts=__ret__.get('additionalArtifacts'),
        additional_schema_elements=__ret__.get('additionalSchemaElements'),
        compression=__ret__.get('compression'),
        format=__ret__.get('format'),
        report_name=__ret__.get('reportName'),
        s3_bucket=__ret__.get('s3Bucket'),
        s3_prefix=__ret__.get('s3Prefix'),
        s3_region=__ret__.get('s3Region'),
        time_unit=__ret__.get('timeUnit'),
        id=__ret__.get('id'))
