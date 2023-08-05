# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class Namespace(pulumi.CustomResource):
    enabled: pulumi.Output[bool]
    """
    Is this Notification Hub Namespace enabled? Defaults to `true`.
    """
    location: pulumi.Output[str]
    """
    The Azure Region in which this Notification Hub Namespace should be created.
    """
    name: pulumi.Output[str]
    """
    The name to use for this Notification Hub Namespace. Changing this forces a new resource to be created.
    """
    namespace_type: pulumi.Output[str]
    """
    The Type of Namespace - possible values are `Messaging` or `NotificationHub`. Changing this forces a new resource to be created.
    """
    resource_group_name: pulumi.Output[str]
    """
    The name of the Resource Group in which the Notification Hub Namespace should exist. Changing this forces a new resource to be created.
    """
    servicebus_endpoint: pulumi.Output[str]
    """
    The ServiceBus Endpoint for this Notification Hub Namespace.
    """
    sku: pulumi.Output[dict]
    """
    ) A `sku` block as described below.
    """
    sku_name: pulumi.Output[str]
    """
    The name of the SKU to use for this Notification Hub Namespace. Possible values are `Free`, `Basic` or `Standard`. Changing this forces a new resource to be created.
    """
    def __init__(__self__, resource_name, opts=None, enabled=None, location=None, name=None, namespace_type=None, resource_group_name=None, sku=None, sku_name=None, __name__=None, __opts__=None):
        """
        Manages a Notification Hub Namespace.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] enabled: Is this Notification Hub Namespace enabled? Defaults to `true`.
        :param pulumi.Input[str] location: The Azure Region in which this Notification Hub Namespace should be created.
        :param pulumi.Input[str] name: The name to use for this Notification Hub Namespace. Changing this forces a new resource to be created.
        :param pulumi.Input[str] namespace_type: The Type of Namespace - possible values are `Messaging` or `NotificationHub`. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which the Notification Hub Namespace should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[dict] sku: ) A `sku` block as described below.
        :param pulumi.Input[str] sku_name: The name of the SKU to use for this Notification Hub Namespace. Possible values are `Free`, `Basic` or `Standard`. Changing this forces a new resource to be created.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-azurerm/blob/master/website/docs/r/notification_hub_namespace.html.markdown.
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

        __props__['enabled'] = enabled

        __props__['location'] = location

        __props__['name'] = name

        if namespace_type is None:
            raise TypeError("Missing required property 'namespace_type'")
        __props__['namespace_type'] = namespace_type

        if resource_group_name is None:
            raise TypeError("Missing required property 'resource_group_name'")
        __props__['resource_group_name'] = resource_group_name

        __props__['sku'] = sku

        __props__['sku_name'] = sku_name

        __props__['servicebus_endpoint'] = None

        super(Namespace, __self__).__init__(
            'azure:notificationhub/namespace:Namespace',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

