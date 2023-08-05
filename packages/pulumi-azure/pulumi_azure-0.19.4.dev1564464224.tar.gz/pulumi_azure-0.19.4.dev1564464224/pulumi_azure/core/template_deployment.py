# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class TemplateDeployment(pulumi.CustomResource):
    deployment_mode: pulumi.Output[str]
    name: pulumi.Output[str]
    """
    Specifies the name of the template deployment. Changing this forces a
    new resource to be created.
    """
    outputs: pulumi.Output[dict]
    """
    A map of supported scalar output types returned from the deployment (currently, Azure Template Deployment outputs of type String, Int and Bool are supported, and are converted to strings - others will be ignored) and can be accessed using `.outputs["name"]`.
    """
    parameters: pulumi.Output[dict]
    """
    Specifies the name and value pairs that define the deployment parameters for the template.
    """
    parameters_body: pulumi.Output[str]
    """
    Specifies a valid Azure JSON parameters file that define the deployment parameters. It can contain KeyVault references
    """
    resource_group_name: pulumi.Output[str]
    """
    The name of the resource group in which to
    create the template deployment.
    """
    template_body: pulumi.Output[str]
    """
    Specifies the JSON definition for the template.
    """
    def __init__(__self__, resource_name, opts=None, deployment_mode=None, name=None, parameters=None, parameters_body=None, resource_group_name=None, template_body=None, __name__=None, __opts__=None):
        """
        Create a TemplateDeployment resource with the given unique name, props, and options.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: Specifies the name of the template deployment. Changing this forces a
               new resource to be created.
        :param pulumi.Input[dict] parameters: Specifies the name and value pairs that define the deployment parameters for the template.
        :param pulumi.Input[str] parameters_body: Specifies a valid Azure JSON parameters file that define the deployment parameters. It can contain KeyVault references
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to
               create the template deployment.
        :param pulumi.Input[str] template_body: Specifies the JSON definition for the template.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-azurerm/blob/master/website/docs/r/template_deployment.html.markdown.
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

        if deployment_mode is None:
            raise TypeError("Missing required property 'deployment_mode'")
        __props__['deployment_mode'] = deployment_mode

        __props__['name'] = name

        __props__['parameters'] = parameters

        __props__['parameters_body'] = parameters_body

        if resource_group_name is None:
            raise TypeError("Missing required property 'resource_group_name'")
        __props__['resource_group_name'] = resource_group_name

        __props__['template_body'] = template_body

        __props__['outputs'] = None

        super(TemplateDeployment, __self__).__init__(
            'azure:core/templateDeployment:TemplateDeployment',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

