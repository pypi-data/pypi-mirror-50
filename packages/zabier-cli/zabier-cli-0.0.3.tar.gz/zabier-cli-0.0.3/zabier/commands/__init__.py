from typing import Dict, IO

import yaml
import click
from dataclasses import asdict, dataclass

from dacite import from_dict
from datadiff import diff

from zabier.zabbix import get_client
from zabier.zabbix import constants
from zabier.zabbix.hostgroup import HostGroup
from zabier.zabbix.action import Action


def hostgroup(name: str, dry_run: bool):
    zabbix = get_client()
    if zabbix.host_group_exists(name):
        click.echo(f'Host group "{name}" is already exists.')
    else:
        hostgroup = HostGroup(groupid=None, name=name)
        if dry_run:
            click.echo(f'The new host group will be created.')
        else:
            groupid = zabbix.create_host_group(hostgroup)
            click.echo(f'Host group created. ID: {groupid}')


def action(name: str, file: str, dry_run: bool):
    zabbix = get_client()
    action = zabbix.get_action_by_name(name)
    action_def = _load_config_file(file)
    action_config = action_def.get('config', {})
    if 'auto_registration_config' in action_def:
        action_config = action_def['auto_registration_config']
        action_config = _refine_auto_registration_config(name, action_config)
    if action is None:
        new_action = from_dict(data_class=Action, data=action_config)
        if dry_run:
            click.echo(f'The new action will be created.')
        else:
            actionid = zabbix.create_action(new_action)
            click.echo(f'Action created. ID: {actionid}')
    else:
        remote_action = action
        local_action = from_dict(data_class=Action, data=action_config)
        diff_result = _diff_actions(local_action, remote_action)
        click.echo(diff_result)
        local_action.actionid = remote_action.actionid
        if not dry_run:
            actionid = zabbix.update_action(local_action)
            click.echo(f'Action updated. ID: {actionid}')


# def template(name: str, file: str, dry_run: bool):
#     zabbix = get_client()
#     action = zabbix.get_template_by_name(name)
#     action_def = _load_config_file(file)
#     action_config = action_def.get('config', {})
#     if 'auto_registration_config' in action_def:
#         action_config = action_def['auto_registration_config']
#         action_config = _refine_auto_registration_config(name, action_config)
#     if action is None:
#         action = from_dict(data_class=Action, data=action_config)
#         actionid = zabbix.create_action(action)
#         click.echo(f'Action created. ID: {actionid}')


def _load_config_file(file: IO) -> Dict:
    return yaml.full_load(open(file))


def _diff_actions(local: dataclass, remote: dataclass):
    local = asdict(local)
    remote = asdict(remote)
    try:
        del local['actionid']
        del remote['actionid']
        del remote['filter']['eval_formula']
        for op in remote['operations']:
            del op['actionid']
            del op['operationid']
            for key in ['optemplate', 'opgroup']:
                if key in op:
                    for op2 in op[key]:
                        del op2['operationid']
    except (KeyError, TypeError):
        pass
    return diff(remote, local)


def _refine_auto_registration_config(name: str, config: Dict) -> Dict:
    zabbix = get_client()
    try:
        hostgroup_name = config['hostgroup']
        hostgroup = zabbix.get_host_group_by_name(hostgroup_name)
        if hostgroup is None:
            raise click.UsageError(f'HostGroup "{hostgroup_name}" is not exists.')

        template_name = config['template']
        template = zabbix.get_template_by_name(template_name)
        if template is None:
            raise click.UsageError(f'Template "{template_name}" is not exists.')

        host_status_operationtype = constants.OPERATION_TYPE_ENABLE_HOST
        if config['disable_host']:
            host_status_operationtype = constants.OPERATION_TYPE_DISABLE_HOST

        refined_config = {
            'esc_period': '0',
            'eventsource': constants.EVENTSOURCE_AUTO_REGISTERED_HOST,
            'name': name,
            'status': config['status'],
            'operations': [
                {
                    'esc_period': '0',
                    'esc_step_from': '1',
                    'esc_step_to': '1',
                    'evaltype': '0',
                    'opconditions': [],
                    'operationtype': constants.OPERATION_TYPE_ADD_HOST
                },
                {
                    'esc_period': '0',
                    'esc_step_from': '1',
                    'esc_step_to': '1',
                    'evaltype': '0',
                    'opconditions': [],
                    'operationtype': constants.OPERATION_TYPE_ADD_TO_HOSTGROUP,
                    'opgroup': [
                        {'groupid': str(hostgroup.groupid)}
                    ]
                },
                {
                    'esc_period': '0',
                    'esc_step_from': '1',
                    'esc_step_to': '1',
                    'evaltype': '0',
                    'opconditions': [],
                    'operationtype': constants.OPERATION_TYPE_LINK_TO_TEMPLATE,
                    'optemplate': [
                        {'templateid': str(template.templateid)}
                    ]
                },
                {
                    'esc_period': '0',
                    'esc_step_from': '1',
                    'esc_step_to': '1',
                    'evaltype': '0',
                    'opconditions': [],
                    'operationtype': host_status_operationtype
                }
            ],
            'filter': {
                'conditions': [
                    {
                        'conditiontype': constants.CONDITION_TYPE_HOST_METADATA,
                        'value': config['hostmetadata'],
                        'operator': constants.CONDITION_OPERATOR_LIKE,
                        'formulaid': 'A'
                    }
                ],
                'evaltype': '0',
                'formula': ''
            }
        }

        return refined_config
    except KeyError as e:
        key_name = e.args[0]
        raise click.UsageError(
            f'"{key_name}" is required in "auto_registration_config".')
