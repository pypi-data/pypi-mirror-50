# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class MailFrom(pulumi.CustomResource):
    behavior_on_mx_failure: pulumi.Output[str]
    """
    The action that you want Amazon SES to take if it cannot successfully read the required MX record when you send an email. Defaults to `UseDefaultValue`. See the [SES API documentation](https://docs.aws.amazon.com/ses/latest/APIReference/API_SetIdentityMailFromDomain.html) for more information.
    """
    domain: pulumi.Output[str]
    """
    Verified domain name to generate DKIM tokens for.
    """
    mail_from_domain: pulumi.Output[str]
    """
    Subdomain (of above domain) which is to be used as MAIL FROM address (Required for DMARC validation)
    """
    def __init__(__self__, resource_name, opts=None, behavior_on_mx_failure=None, domain=None, mail_from_domain=None, __name__=None, __opts__=None):
        """
        Provides an SES domain MAIL FROM resource.
        
        > **NOTE:** For the MAIL FROM domain to be fully usable, this resource should be paired with the [aws_ses_domain_identity resource](https://www.terraform.io/docs/providers/aws/r/ses_domain_identity.html). To validate the MAIL FROM domain, a DNS MX record is required. To pass SPF checks, a DNS TXT record may also be required. See the [Amazon SES MAIL FROM documentation](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/mail-from-set.html) for more information.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] behavior_on_mx_failure: The action that you want Amazon SES to take if it cannot successfully read the required MX record when you send an email. Defaults to `UseDefaultValue`. See the [SES API documentation](https://docs.aws.amazon.com/ses/latest/APIReference/API_SetIdentityMailFromDomain.html) for more information.
        :param pulumi.Input[str] domain: Verified domain name to generate DKIM tokens for.
        :param pulumi.Input[str] mail_from_domain: Subdomain (of above domain) which is to be used as MAIL FROM address (Required for DMARC validation)

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/ses_domain_mail_from.html.markdown.
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

        __props__['behavior_on_mx_failure'] = behavior_on_mx_failure

        if domain is None:
            raise TypeError("Missing required property 'domain'")
        __props__['domain'] = domain

        if mail_from_domain is None:
            raise TypeError("Missing required property 'mail_from_domain'")
        __props__['mail_from_domain'] = mail_from_domain

        super(MailFrom, __self__).__init__(
            'aws:ses/mailFrom:MailFrom',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

