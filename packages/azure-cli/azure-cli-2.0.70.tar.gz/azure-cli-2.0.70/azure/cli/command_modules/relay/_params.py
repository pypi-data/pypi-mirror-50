# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=line-too-long
# pylint: disable=too-many-statements

from azure.cli.core.commands.parameters import tags_type, get_enum_type, resource_group_name_type, name_type, get_location_type, get_resource_name_completion_list, get_three_state_flag
from azure.cli.core.commands.validators import get_default_location_from_resource_group


def load_arguments_sb(self, _):
    from azure.cli.command_modules.relay._completers import get_wcfrelay_command_completion_list, \
        get_hyco_command_completion_list

    from knack.arguments import CLIArgumentType
    from azure.mgmt.relay.models import SkuTier, AccessRights, KeyType
    rights_arg_type = CLIArgumentType(options_list=['--rights'], nargs='+', arg_type=get_enum_type(AccessRights), help='Space-separated list of Authorization rule rights')
    key_arg_type = CLIArgumentType(options_list=['--key'], arg_type=get_enum_type(KeyType), help='specifies Primary or Secondary key needs to be reset')
    keyvalue_arg_type = CLIArgumentType(options_list=['--key-value'], help='Optional, if the key value provided, is set for KeyType or autogenerated Key value set for keyType.')

    with self.argument_context('relay') as c:
        c.argument('resource_group_name', arg_type=resource_group_name_type)
        c.argument('namespace_name', options_list=['--namespace-name'], id_part='name', help='Name of Namespace')

    with self.argument_context('relay namespace') as c:
        c.argument('namespace_name', id_part='name', arg_type=name_type, completer=get_resource_name_completion_list('Microsoft.relay/namespaces'), help='Name of Namespace')

    with self.argument_context('relay namespace exists') as c:
        c.argument('name', arg_type=name_type, help='Namespace name. Name can contain only letters, numbers, and hyphens. The namespace must start with a letter, and it must end with a letter or number.')

    for scope in ['relay namespace create', 'relay namespace update']:
        with self.argument_context(scope) as c:
            c.argument('tags', arg_type=tags_type)
            c.argument('sku', arg_type=get_enum_type(SkuTier))

    with self.argument_context('relay namespace create') as c:
        c.argument('location', arg_type=get_location_type(self.cli_ctx), validator=get_default_location_from_resource_group)

    # region Namespace Authorization Rule
    with self.argument_context('relay namespace authorization-rule list') as c:
        c.argument('namespace_name', options_list=['--namespace-name'], id_part=None, help='Name of the Namespace')

    with self.argument_context('relay namespace authorization-rule') as c:
        c.argument('authorization_rule_name', arg_type=name_type, id_part='child_name_1', help='Name of Namespace Authorization Rule')
        c.argument('namespace_name', id_part='name', options_list=['--namespace-name'], help='Name of Namespace')

    for scope in ['relay namespace authorization-rule create', 'relay namespace authorization-rule update', 'relay wcfrelay authorization-rule create', 'relay wcfrelay authorization-rule update', 'relay hyco authorization-rule create', 'relay hyco authorization-rule update']:
        with self.argument_context(scope) as c:
            c.argument('rights', arg_type=rights_arg_type)

    with self.argument_context('relay namespace authorization-rule keys renew') as c:
        c.argument('key_type', arg_type=key_arg_type)
        c.argument('key', arg_type=keyvalue_arg_type)

    with self.argument_context('relay namespace authorization-rule keys list') as c:
        c.argument('authorization_rule_name', arg_type=name_type, id_part=None, help='Name of Namespace Authorization Rule')
        c.argument('namespace_name', id_part=None, options_list=['--namespace-name'], help='Name of Namespace')

    # region WCF Relay
    with self.argument_context('relay wcfrelay') as c:
        c.argument('relay_name', arg_type=name_type, id_part='child_name_1', completer=get_wcfrelay_command_completion_list, help='Name of WCF Relay')

    for scope in ['relay wcfrelay create', 'relay wcfrelay update']:
        with self.argument_context(scope) as c:
            c.argument('status', arg_type=get_enum_type(['Active', 'Disabled', 'SendDisabled', 'ReceiveDisabled']), help='Enumerates the possible values for the status of a messaging entity.')
            c.argument('relay_type', arg_type=get_enum_type(['Http', 'NetTcp']), default='NetTcp', help='Relay type')
            c.argument('user_metadata', help='Endpoint metadata')

    with self.argument_context('relay wcfrelay create') as c:
        c.argument('requires_client_authorization', arg_type=get_three_state_flag(), help='Indicates whether client authorization is required')
        c.argument('requires_transport_security', arg_type=get_three_state_flag(), help='Indicates whether transport security is required')

    with self.argument_context('relay wcfrelay list') as c:
        c.argument('namespace_name', id_part=None, options_list=['--namespace-name'], help='Name of Namespace')

    # region WCF Relay Authorization Rule
    with self.argument_context('relay wcfrelay authorization-rule') as c:
        c.argument('authorization_rule_name', arg_type=name_type, id_part='child_name_2', help='Name of WCF Relay Authorization Rule')
        c.argument('relay_name', id_part='child_name_1', options_list=['--relay-name'], help='Name of WCF Relay')

    with self.argument_context('relay wcfrelay authorization-rule list') as c:
        c.argument('namespace_name', id_part=None, options_list=['--namespace-name'], help='Name of Namespace')
        c.argument('relay_name', id_part=None, options_list=['--relay-name'], help='Name of WCF Relay')

    with self.argument_context('relay wcfrelay authorization-rule keys renew') as c:
        c.argument('key_type', arg_type=key_arg_type)
        c.argument('key', arg_type=keyvalue_arg_type)

    with self.argument_context('relay wcfrelay authorization-rule keys list') as c:
        c.argument('authorization_rule_name', arg_type=name_type, id_part=None, help='Name of WCF Relay Authorization Rule')
        c.argument('relay_name', id_part=None, options_list=['--relay-name'], help='Name of WCF Relay')
        c.argument('namespace_name', id_part=None, options_list=['--namespace-name'], help='Name of Namespace')

    # region - Hybrid Connection
    for scope in ['relay hyco show', 'relay hyco delete']:
        with self.argument_context(scope) as c:
            c.argument('hybrid_connection_name', arg_type=name_type, id_part='child_name_1', completer=get_hyco_command_completion_list, help='Name of Hybrid Connection')

    # region - Hybrid Connection Create
    with self.argument_context('relay hyco create') as c:
        c.argument('hybrid_connection_name', arg_type=name_type, id_part='child_name_1', completer=get_hyco_command_completion_list, help='Name of Hybrid Connection')
        c.argument('status', arg_type=get_enum_type(['Active', 'Disabled', 'SendDisabled', 'ReceiveDisabled']), help='Enumerates the possible values for the status of a messaging entity.')
        c.argument('requires_client_authorization', arg_type=get_three_state_flag(), help='Indicates whether client authorization is required')
        c.argument('user_metadata', help='Endpoint metadata')

    # region - Hybrid Connection Update
    with self.argument_context('relay hyco update') as c:
        c.argument('hybrid_connection_name', arg_type=name_type, id_part='child_name_1', completer=get_hyco_command_completion_list, help='Name of Hybrid Connection')
        c.argument('status', arg_type=get_enum_type(['Active', 'Disabled', 'SendDisabled', 'ReceiveDisabled']), help='Enumerates the possible values for the status of a messaging entity.')
        c.argument('requires_client_authorization', arg_type=get_three_state_flag(), help='Indicates whether client authorization is required')
        c.argument('user_metadata', help='Endpoint metadata')

    with self.argument_context('relay hyco list') as c:
        c.argument('namespace_name', id_part=None, options_list=['--namespace-name'], help='Name of Namespace')

    # region Hybrid Connection Authorization Rule
    with self.argument_context('relay hyco authorization-rule') as c:
        c.argument('authorization_rule_name', arg_type=name_type, id_part='child_name_2', help='name of Hybrid Connection Authorization Rule')
        c.argument('hybrid_connection_name', options_list=['--hybrid-connection-name'], id_part='child_name_1', help='name of Hybrid Connection')

    with self.argument_context('relay hyco authorization-rule list') as c:
        c.argument('namespace_name', id_part=None, options_list=['--namespace-name'], help='Name of Namespace')
        c.argument('hybrid_connection_name', options_list=['--hybrid-connection-name'], id_part=None, help='name of Hybrid Connection')

    with self.argument_context('relay hyco authorization-rule keys list') as c:
        c.argument('authorization_rule_name', arg_type=name_type, id_part=None, help='Name of Hybrid Connection Authorization Rule')
        c.argument('hybrid_connection_name', id_part=None, options_list=['--hybrid-connection-name'], help='Name of Hybrid Connection')
        c.argument('namespace_name', id_part=None, options_list=['--namespace-name'], help='Name of Namespace')

    with self.argument_context('relay hyco authorization-rule keys renew') as c:
        c.argument('key_type', arg_type=key_arg_type)
        c.argument('key', arg_type=keyvalue_arg_type)
