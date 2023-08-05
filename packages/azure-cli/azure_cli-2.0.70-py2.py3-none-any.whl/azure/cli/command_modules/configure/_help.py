# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.help_files import helps


helps['configure'] = """
    type: command
    short-summary: Manage Azure CLI configuration. This command is interactive.
    parameters:
        - name: --defaults -d
          short-summary: >
            Space-separated 'name=value' pairs for common argument defaults.
    examples:
        - name: Set default resource group, webapp and VM names.
          text: az configure --defaults group=myRG web=myweb vm=myvm
        - name: Clear default webapp and VM names.
          text: az configure --defaults vm='' web=''
"""

helps['cache'] = """
    type: group
    short-summary: Commands to manage CLI objects cached using the `--defer` argument.
"""

helps['cache list'] = """
    type: command
    short-summary: List the contents of the object cache.
"""

helps['cache show'] = """
    type: command
    short-summary: Show the contents of a specific object in the cache.
"""

helps['cache delete'] = """
    type: command
    short-summary: Delete an object from the cache.
"""

helps['cache purge'] = """
    type: command
    short-summary: Clear the entire CLI object cache.
"""
