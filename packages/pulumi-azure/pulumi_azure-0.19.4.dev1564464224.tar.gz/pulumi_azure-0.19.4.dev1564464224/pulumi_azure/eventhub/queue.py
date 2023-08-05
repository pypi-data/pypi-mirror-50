# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from .. import utilities, tables

class Queue(pulumi.CustomResource):
    auto_delete_on_idle: pulumi.Output[str]
    """
    The ISO 8601 timespan duration of the idle interval after which the
    Queue is automatically deleted, minimum of 5 minutes.
    """
    dead_lettering_on_message_expiration: pulumi.Output[bool]
    """
    Boolean flag which controls whether the Queue has dead letter support when a message expires. Defaults to `false`.
    """
    default_message_ttl: pulumi.Output[str]
    """
    The ISO 8601 timespan duration of the TTL of messages sent to this
    queue. This is the default value used when TTL is not set on message itself.
    """
    duplicate_detection_history_time_window: pulumi.Output[str]
    """
    The ISO 8601 timespan duration during which
    duplicates can be detected. Default value is 10 minutes. (`PT10M`)
    """
    enable_batched_operations: pulumi.Output[bool]
    enable_express: pulumi.Output[bool]
    """
    Boolean flag which controls whether Express Entities
    are enabled. An express queue holds a message in memory temporarily before writing
    it to persistent storage. Defaults to `false` for Basic and Standard. For Premium, it MUST
    be set to `false`.
    """
    enable_partitioning: pulumi.Output[bool]
    """
    Boolean flag which controls whether to enable
    the queue to be partitioned across multiple message brokers. Changing this forces
    a new resource to be created. Defaults to `false` for Basic and Standard. For Premium, it MUST
    be set to `true`.
    """
    location: pulumi.Output[str]
    """
    Specifies the supported Azure location where the resource exists.
    Changing this forces a new resource to be created.
    """
    lock_duration: pulumi.Output[str]
    """
    The ISO 8601 timespan duration of a peek-lock; that is, the amount of time that the message is locked for other receivers. Maximum value is 5 minutes. Defaults to 1 minute. (`PT1M`)
    """
    max_delivery_count: pulumi.Output[float]
    """
    Integer value which controls when a message is automatically deadlettered. Defaults to `10`.
    """
    max_size_in_megabytes: pulumi.Output[float]
    """
    Integer value which controls the size of
    memory allocated for the queue. For supported values see the "Queue/topic size"
    section of [this document](https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-quotas).
    """
    name: pulumi.Output[str]
    """
    Specifies the name of the ServiceBus Queue resource. Changing this forces a
    new resource to be created.
    """
    namespace_name: pulumi.Output[str]
    """
    The name of the ServiceBus Namespace to create
    this queue in. Changing this forces a new resource to be created.
    """
    requires_duplicate_detection: pulumi.Output[bool]
    """
    Boolean flag which controls whether
    the Queue requires duplicate detection. Changing this forces
    a new resource to be created. Defaults to `false`.
    """
    requires_session: pulumi.Output[bool]
    """
    Boolean flag which controls whether the Queue requires sessions.
    This will allow ordered handling of unbounded sequences of related messages. With sessions enabled
    a queue can guarantee first-in-first-out delivery of messages.
    Changing this forces a new resource to be created. Defaults to `false`.
    """
    resource_group_name: pulumi.Output[str]
    """
    The name of the resource group in which to
    create the namespace. Changing this forces a new resource to be created.
    """
    support_ordering: pulumi.Output[bool]
    def __init__(__self__, resource_name, opts=None, auto_delete_on_idle=None, dead_lettering_on_message_expiration=None, default_message_ttl=None, duplicate_detection_history_time_window=None, enable_batched_operations=None, enable_express=None, enable_partitioning=None, location=None, lock_duration=None, max_delivery_count=None, max_size_in_megabytes=None, name=None, namespace_name=None, requires_duplicate_detection=None, requires_session=None, resource_group_name=None, support_ordering=None, __name__=None, __opts__=None):
        """
        Manage a ServiceBus Queue.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] auto_delete_on_idle: The ISO 8601 timespan duration of the idle interval after which the
               Queue is automatically deleted, minimum of 5 minutes.
        :param pulumi.Input[bool] dead_lettering_on_message_expiration: Boolean flag which controls whether the Queue has dead letter support when a message expires. Defaults to `false`.
        :param pulumi.Input[str] default_message_ttl: The ISO 8601 timespan duration of the TTL of messages sent to this
               queue. This is the default value used when TTL is not set on message itself.
        :param pulumi.Input[str] duplicate_detection_history_time_window: The ISO 8601 timespan duration during which
               duplicates can be detected. Default value is 10 minutes. (`PT10M`)
        :param pulumi.Input[bool] enable_express: Boolean flag which controls whether Express Entities
               are enabled. An express queue holds a message in memory temporarily before writing
               it to persistent storage. Defaults to `false` for Basic and Standard. For Premium, it MUST
               be set to `false`.
        :param pulumi.Input[bool] enable_partitioning: Boolean flag which controls whether to enable
               the queue to be partitioned across multiple message brokers. Changing this forces
               a new resource to be created. Defaults to `false` for Basic and Standard. For Premium, it MUST
               be set to `true`.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists.
               Changing this forces a new resource to be created.
        :param pulumi.Input[str] lock_duration: The ISO 8601 timespan duration of a peek-lock; that is, the amount of time that the message is locked for other receivers. Maximum value is 5 minutes. Defaults to 1 minute. (`PT1M`)
        :param pulumi.Input[float] max_delivery_count: Integer value which controls when a message is automatically deadlettered. Defaults to `10`.
        :param pulumi.Input[float] max_size_in_megabytes: Integer value which controls the size of
               memory allocated for the queue. For supported values see the "Queue/topic size"
               section of [this document](https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-quotas).
        :param pulumi.Input[str] name: Specifies the name of the ServiceBus Queue resource. Changing this forces a
               new resource to be created.
        :param pulumi.Input[str] namespace_name: The name of the ServiceBus Namespace to create
               this queue in. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] requires_duplicate_detection: Boolean flag which controls whether
               the Queue requires duplicate detection. Changing this forces
               a new resource to be created. Defaults to `false`.
        :param pulumi.Input[bool] requires_session: Boolean flag which controls whether the Queue requires sessions.
               This will allow ordered handling of unbounded sequences of related messages. With sessions enabled
               a queue can guarantee first-in-first-out delivery of messages.
               Changing this forces a new resource to be created. Defaults to `false`.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to
               create the namespace. Changing this forces a new resource to be created.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-azurerm/blob/master/website/docs/r/servicebus_queue.html.markdown.
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

        __props__['auto_delete_on_idle'] = auto_delete_on_idle

        __props__['dead_lettering_on_message_expiration'] = dead_lettering_on_message_expiration

        __props__['default_message_ttl'] = default_message_ttl

        __props__['duplicate_detection_history_time_window'] = duplicate_detection_history_time_window

        __props__['enable_batched_operations'] = enable_batched_operations

        __props__['enable_express'] = enable_express

        __props__['enable_partitioning'] = enable_partitioning

        __props__['location'] = location

        __props__['lock_duration'] = lock_duration

        __props__['max_delivery_count'] = max_delivery_count

        __props__['max_size_in_megabytes'] = max_size_in_megabytes

        __props__['name'] = name

        if namespace_name is None:
            raise TypeError("Missing required property 'namespace_name'")
        __props__['namespace_name'] = namespace_name

        __props__['requires_duplicate_detection'] = requires_duplicate_detection

        __props__['requires_session'] = requires_session

        if resource_group_name is None:
            raise TypeError("Missing required property 'resource_group_name'")
        __props__['resource_group_name'] = resource_group_name

        __props__['support_ordering'] = support_ordering

        super(Queue, __self__).__init__(
            'azure:eventhub/queue:Queue',
            resource_name,
            __props__,
            opts)


    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

