# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
import os

from knack.util import CLIError

from azure.cli.command_modules.ams._sdk_utils import (get_sdk_model_class, get_stand_alone_presets)

from azure.mgmt.media.models import (StandardEncoderPreset, TransformOutput,
                                     BuiltInStandardEncoderPreset, EncoderNamedPreset)


def create_transform(client, account_name, resource_group_name, transform_name, preset,
                     insights_to_extract=None, audio_language=None, on_error=None,
                     relative_priority=None, description=None):

    outputs = [build_transform_output(preset, insights_to_extract, audio_language,
                                      on_error, relative_priority)]

    return client.create_or_update(resource_group_name, account_name, transform_name,
                                   outputs, description)


def add_transform_output(client, account_name, resource_group_name, transform_name, preset,
                         insights_to_extract=None, audio_language=None, on_error=None,
                         relative_priority=None):

    transform = client.get(resource_group_name, account_name, transform_name)

    if not transform:
        raise CLIError('The transform resource was not found.')

    transform.outputs.append(build_transform_output(preset, insights_to_extract, audio_language,
                                                    on_error, relative_priority))

    return client.create_or_update(resource_group_name, account_name, transform_name, transform.outputs)


def build_transform_output(preset, insights_to_extract, audio_language, on_error,
                           relative_priority):
    from azure.mgmt.media.models import (OnErrorType, Priority)

    validate_arguments(preset, insights_to_extract, audio_language)
    transform_output = get_transform_output(preset)

    if preset == 'VideoAnalyzer':
        transform_output.preset.audio_language = audio_language
        transform_output.preset.insights_to_extract = insights_to_extract
    elif preset == 'AudioAnalyzer':
        transform_output.preset.audio_language = audio_language

    if on_error is not None:
        transform_output.on_error = OnErrorType(on_error)

    if relative_priority is not None:
        transform_output.relative_priority = Priority(relative_priority)

    return transform_output


def validate_arguments(preset, insights_to_extract, audio_language):

    if insights_to_extract and preset != 'VideoAnalyzer':
        raise CLIError("insights-to-extract argument only works with VideoAnalyzer preset type.")

    if audio_language and preset not in get_stand_alone_presets():
        raise CLIError("audio-language argument only works with VideoAnalyzer or AudioAnalyzer preset types.")


def remove_transform_output(client, account_name, resource_group_name, transform_name, output_index):
    transform = client.get(resource_group_name, account_name, transform_name)

    try:
        transform.outputs.pop(output_index)
    except IndexError:
        raise CLIError("index {} doesn't exist on outputs".format(output_index))

    return client.create_or_update(resource_group_name, account_name, transform_name, transform.outputs)


def transform_update_setter(client, resource_group_name,
                            account_name, transform_name, parameters):
    return client.create_or_update(resource_group_name, account_name, transform_name,
                                   parameters.outputs, parameters.description)


def update_transform(instance, description=None):
    if not instance:
        raise CLIError('The transform resource was not found.')

    if description is not None:
        instance.description = description

    return instance


def get_transform_output(preset):
    transform_preset = None

    try:
        if os.path.exists(preset):
            transform_preset = parse_standard_encoder_preset(preset)
        else:
            if preset in get_stand_alone_presets():
                transform_preset = get_sdk_model_class("{}Preset".format(preset))()
            else:
                if preset not in [e.value for e in EncoderNamedPreset]:
                    raise CLIError("Couldn't create a preset from '{}'".format(preset))
                transform_preset = BuiltInStandardEncoderPreset(preset_name=preset)
    except:
        raise CLIError("Couldn't create a preset from '{}'".format(preset))

    transform_output = TransformOutput(preset=transform_preset)
    return transform_output


def parse_standard_encoder_preset(custom_preset_path):
    try:
        with open(custom_preset_path) as custom_preset_json_stream:
            custom_preset_json = json.load(custom_preset_json_stream)
            custom_preset = StandardEncoderPreset(**custom_preset_json)
            return custom_preset
    except:
        raise CLIError("Couldn't find a valid custom preset JSON definition in '{}'. Check the schema is correct."
                       .format(custom_preset_path))
