# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.help_files import helps  # pylint: disable=unused-import


helps['container'] = """
    type: group
    short-summary: Manage Azure Container Instances.
"""

helps['container create'] = """
    type: command
    short-summary: Create a container group.
    examples:
        - name: Create a container in a container group with 1 core and 1Gb of memory.
          text: az container create -g MyResourceGroup --name myapp --image myimage:latest --cpu 1 --memory 1
        - name: Create a container in a container group that runs Windows, with 2 cores and 3.5Gb of memory.
          text: az container create -g MyResourceGroup --name mywinapp --image winappimage:latest --os-type Windows --cpu 2 --memory 3.5
        - name: Create a container in a container group with public IP address, ports and DNS name label.
          text: az container create -g MyResourceGroup --name myapp --image myimage:latest --ports 80 443 --dns-name-label contoso
        - name: Create a container in a container group that invokes a script upon start.
          text: az container create -g MyResourceGroup --name myapp --image myimage:latest --command-line "/bin/sh -c '/path to/myscript.sh'"
        - name: Create a container in a container group that runs a command and stop the container afterwards.
          text: az container create -g MyResourceGroup --name myapp --image myimage:latest --command-line "echo hello" --restart-policy Never
        - name: Create a container in a container group with environment variables.
          text: az container create -g MyResourceGroup --name myapp --image myimage:latest --environment-variables key1=value1 key2=value2
        - name: Create a container in a container group using container image from Azure Container Registry.
          text: az container create -g MyResourceGroup --name myapp --image myAcrRegistry.azurecr.io/myimage:latest --registry-password password
        - name: Create a container in a container group that mounts an Azure File share as volume.
          text: az container create -g MyResourceGroup --name myapp --image myimage:latest --command-line "cat /mnt/azfile/myfile" --azure-file-volume-share-name myshare --azure-file-volume-account-name mystorageaccount --azure-file-volume-account-key mystoragekey --azure-file-volume-mount-path /mnt/azfile
        - name: Create a container in a container group that mounts a git repo as volume.
          text: az container create -g MyResourceGroup --name myapp --image myimage:latest --command-line "cat /mnt/gitrepo" --gitrepo-url https://github.com/user/myrepo.git --gitrepo-dir ./dir1 --gitrepo-mount-path /mnt/gitrepo
        - name: Create a container in a container group using a yaml file.
          text: az container create -g MyResourceGroup -f containerGroup.yaml
        - name: Create a container group using Log Analytics from a workspace name.
          text: az container create -g MyResourceGroup --name myapp --log-analytics-workspace myworkspace
        - name: Create a container group with a system assigned identity.
          text: az container create -g MyResourceGroup --name myapp --image myimage:latest --assign-identity
        - name: Create a container group with a system assigned identity. The group will have a 'Contributor' role with access to a storage account.
          text: az container create -g MyResourceGroup --name myapp --image myimage:latest --assign-identity --scope /subscriptions/99999999-1bf0-4dda-aec3-cb9272f09590/MyResourceGroup/myRG/providers/Microsoft.Storage/storageAccounts/storage1
        - name: Create a container group with a user assigned identity.
          text: az container create -g MyResourceGroup --name myapp --image myimage:latest --assign-identity  /subscriptions/mySubscrpitionId/resourcegroups/myRG/providers/Microsoft.ManagedIdentity/userAssignedIdentities/myID
        - name: Create a container group with both system and user assigned identity.
          text: az container create -g MyResourceGroup --name myapp --image myimage:latest --assign-identity [system] /subscriptions/mySubscrpitionId/resourcegroups/myRG/providers/Microsoft.ManagedIdentity/userAssignedIdentities/myID
          supported-profiles: latest
"""

helps['container delete'] = """
    type: command
    short-summary: Delete a container group.
"""

helps['container list'] = """
    type: command
    short-summary: List container groups.
"""

helps['container show'] = """
    type: command
    short-summary: Get the details of a container group.
"""

helps['container logs'] = """
    type: command
    short-summary: Examine the logs for a container in a container group.
"""

helps['container export'] = """
    type: command
    short-summary: Export a container group in yaml format.
    examples:
        - name: Export a container group in yaml.
          text: az container export -g MyResourceGroup --name mynginx -f output.yaml
"""

helps['container exec'] = """
    type: command
    short-summary: Execute a command from within a running container of a container group.
    long-summary: The most common use case is to open an interactive bash shell. See examples below. This command is currently not supported for Windows machines.
    examples:
        - name: Stream a shell from within an nginx container.
          text: az container exec -g MyResourceGroup --name mynginx --container-name nginx --exec-command "/bin/bash"
"""

helps['container attach'] = """
    type: command
    short-summary: Attach local standard output and error streams to a container in a container group.
"""
