from coeus_test.commands import verify_response
import coeus_test.message as message
from coeus_unity.transform import TransformRef

DEFAULT_TIMEOUT_SECONDS = 60
DEFAULT_RECURSIVE = True
DEFAULT_TRANSFORM_EXISTS = True
DEFAULT_RENDERER_VISIBLE = True
DEFAULT_SCENE_LOADED = True


def query_transform_exists(cli, transform_ref):
    """
    Requests status on whether a transform exists or not.
    :param cli:
    :param transform_ref:
    :return: bool
    """
    # Ensure backwards compatibility with previous versions of this command that took a transform_path string.
    transform_ref = _convert_to_transform_ref(transform_ref)

    message_payload = {
        "transform_ref": TransformRef.to_payload(transform_ref)
    }
    msg = message.Message("query.unity.transform.exists", message_payload)
    cli.send_message(msg)

    response = cli.read_message()
    verify_response(response)
    return bool(response['payload']['result'])


def await_transform_exists(cli, transform_ref, does_exist=DEFAULT_TRANSFORM_EXISTS, timeout_seconds=DEFAULT_TIMEOUT_SECONDS):
    """
    Waits for a single transform to exist based on does_exist.
    :param cli:
    :param transform_ref:
    :param does_exist: Whether or not to await for exist state (True | False)
    :param timeout_seconds: How long until this returns with failure
    :return: bool
    """
    # Ensure backwards compatibility with previous versions of this command that took a transform_path string.
    transform_ref = _convert_to_transform_ref(transform_ref)

    message_payload = {
        "transform_refs": TransformRef.list_to_payload([transform_ref]),
        "do_exist": does_exist,
        "match_mode": "All",
        "timeout": timeout_seconds
    }
    msg = message.Message("await.unity.transform.exists", message_payload)
    cli.send_message(msg)

    response = cli.read_message()
    verify_response(response)
    return bool(response['payload']['success'])


def await_any_transforms_exist(cli, transform_refs, does_exist=DEFAULT_TRANSFORM_EXISTS, timeout_seconds=DEFAULT_TIMEOUT_SECONDS):
    """
    Waits for a transform to exist based on does_exist.
    :param cli:
    :param transform_refs: An array of transform paths [...]
    :param does_exist: Whether or not to await for exist state (True | False)
    :param timeout_seconds: How long until this returns with failure
    :return: bool
    """
    # Ensure backwards compatibility with previous versions of this command that took a transform_paths string array.
    transform_refs = _convert_to_transform_refs(transform_refs)
    
    message_payload = {
        "transform_refs": TransformRef.list_to_payload(transform_refs),
        "do_exist": does_exist,
        "match_mode": "Any",
        "timeout": timeout_seconds
    }
    msg = message.Message("await.unity.transform.exists", message_payload)
    cli.send_message(msg)

    response = cli.read_message()
    verify_response(response)
    return bool(response['payload']['success'])


def await_all_transforms_exist(cli, transform_refs, does_exist=DEFAULT_TRANSFORM_EXISTS, timeout_seconds=DEFAULT_TIMEOUT_SECONDS):
    """
    Waits for all transforms specified in transform_refs to exist or not based on does_exist.
    :param cli:
    :param transform_refs: An array of transform paths [...]
    :param does_exist: Whether or not to await for exist state (True | False)
    :param timeout_seconds: How long until this returns with failure
    :return: bool
    """
    # Ensure backwards compatibility with previous versions of this command that took a transform_paths string array.
    transform_refs = _convert_to_transform_refs(transform_refs)
    
    message_payload = {
        "transform_refs": TransformRef.list_to_payload(transform_refs),
        "do_exist": does_exist,
        "match_mode": "All",
        "timeout": timeout_seconds
    }
    msg = message.Message("await.unity.transform.exists", message_payload)
    cli.send_message(msg)

    response = cli.read_message()
    verify_response(response)
    return bool(response['payload']['success'])


def fetch_transform(cli, transform_ref, recursive=DEFAULT_RECURSIVE):
    """
    Wrapper around ``fetch_transform_children`` that returns the original transform reference instead of its children.

    :param cli:
    :param transform_ref: Specifies the transform to request children for.
    :param recursive: If True, fetch children recursively; otherwise, fetch immediate children only.
    :return: The original transform reference, with its ``children`` property set as described in the documentation for
    the ``fetch_transform_children`` command.
    """
    # Ensure backwards compatibility with previous versions of this command that took a transform_path string.
    transform_ref = _convert_to_transform_ref(transform_ref)

    fetch_transform_children(cli, transform_ref, recursive)

    return transform_ref


def fetch_transform_children(cli, transform_ref, recursive=DEFAULT_RECURSIVE):
    """
    Requests children of the specified transform. Children may optionally be fetched recursively.

    Children are returned as an array of TransformRef instances. Each instance has a ``children`` property, which is
    interpreted as follows:
        * If children = None, the property wasn't fetched (recursive = False).
        * If children = [], the property was fetched (recursive = True), but the TransformRef doesn't have children.
    :param cli:
    :param transform_ref: Specifies the transform to request children for.
    :param recursive: If True, fetch children recursively; otherwise, fetch immediate children only.
    :return: Array of TransformRefs representing the immediate children of the specified transform. If children are
    fetched recursively (recursive = True), then grandchildren, etc. can be accessed via the ``children`` property of
    the returned TransformRefs.
    """
    # Ensure backwards compatibility with previous versions of this command that took a transform_path string.
    transform_ref = _convert_to_transform_ref(transform_ref)
    
    message_payload = {
        "transform_ref": TransformRef.to_payload(transform_ref),
        "recursive": recursive
    }

    msg = message.Message("fetch.unity.transform.children", message_payload)
    cli.send_message(msg)

    response = cli.read_message()
    verify_response(response)

    children = TransformRef.list_from_payload(response['payload']['children'], transform_ref)
    return children


def fetch_transform_screen_position(cli, transform_ref):
    """
    Requests screen position of a transform at path. WorldToScreenPoint is used for 3D, otherwise
    a screen-scaled center of RectTransform is used.
    :param cli:
    :param transform_ref:
    :return: [x,y]
    """
    # Ensure backwards compatibility with previous versions of this command that took a transform_path string.
    transform_ref = _convert_to_transform_ref(transform_ref)
    
    message_payload = {
        "transform_ref": TransformRef.to_payload(transform_ref)
    }
    msg = message.Message("fetch.unity.transform.screenPosition", message_payload)
    cli.send_message(msg)

    response = cli.read_message()
    verify_response(response)
    return [
            response['payload']['x'],
            response['payload']['y']
    ]


def fetch_transform_normalized_screen_position(cli, transform_ref):
    """
    Requests screen position of a transform at path. WorldToScreenPoint is used for 3D, otherwise
    a screen-scaled center of RectTransform is used.
    :param cli:
    :param transform_ref:
    :return: [x,y]
    """
    # Ensure backwards compatibility with previous versions of this command that took a transform_path string.
    transform_ref = _convert_to_transform_ref(transform_ref)
    
    message_payload = {
        "transform_ref": TransformRef.to_payload(transform_ref)
    }
    msg = message.Message("fetch.unity.transform.screenPosition", message_payload)
    cli.send_message(msg)

    response = cli.read_message()
    verify_response(response)
    return [
            response['payload']['normalized_x'],
            response['payload']['normalized_y']
    ]


def query_renderer_visible(cli, transform_ref):
    """
    Requests status on whether a renderer at transform_ref is visible.
    :param cli:
    :param transform_ref:
    :return: bool
    """
    # Ensure backwards compatibility with previous versions of this command that took a transform_path string.
    transform_ref = _convert_to_transform_ref(transform_ref)
    
    message_payload = {
        "transform_ref": TransformRef.to_payload(transform_ref)
    }
    msg = message.Message("query.unity.renderer.visible", message_payload)
    cli.send_message(msg)

    response = cli.read_message()
    verify_response(response)
    return bool(response['payload']['result'])


def await_renderer_visible(cli, transform_ref, is_visible=DEFAULT_RENDERER_VISIBLE, timeout_seconds=DEFAULT_TIMEOUT_SECONDS):
    """
    Waits for a transform renderer to become visible based on is_visible.
    :param cli:
    :param transform_ref:
    :param is_visible: Whether or not to await for visible state (True | False)
    :param timeout_seconds: How long until this returns with failure
    :return: bool
    """
    # Ensure backwards compatibility with previous versions of this command that took a transform_path string.
    transform_ref = _convert_to_transform_ref(transform_ref)
    
    message_payload = {
        "transform_ref": TransformRef.to_payload(transform_ref),
        "is_visible": is_visible,
        "timeout": timeout_seconds
    }
    msg = message.Message("await.unity.renderer.visible", message_payload)
    cli.send_message(msg)

    response = cli.read_message()
    verify_response(response)
    return bool(response['payload']['success'])


def query_scene_loaded(cli, scene_name):
    """
    Requests status on whether a scene is loaded or not.
    :param cli:
    :param scene_name:
    :return: bool
    """

    message_payload = {
        "scene_name": scene_name
    }
    msg = message.Message("query.unity.scene.loaded", message_payload)
    cli.send_message(msg)

    response = cli.read_message()
    verify_response(response)
    return bool(response['payload']['result'])


def await_scene_loaded(cli, scene_name, is_loaded=DEFAULT_SCENE_LOADED, timeout_seconds=DEFAULT_TIMEOUT_SECONDS):
    """
    Waits for a scene to be loaded based on is_loaded.
    :param cli:
    :param scene_name:
    :param is_loaded: Whether or not to await for loaded state (True | False)
    :param timeout_seconds: How long until this returns with failure
    :return: bool
    """
    message_payload = {
        "scene_name": scene_name,
        "is_loaded": is_loaded,
        "timeout": timeout_seconds
    }
    msg = message.Message("await.unity.scene.loaded", message_payload)
    cli.send_message(msg)

    response = cli.read_message()
    verify_response(response)
    return bool(response['payload']['success'])


def fetch_component_value(cli, transform_ref, component_type, name):
    """
    Requests value from a component field or property
    :param cli:
    :param transform_ref: The path of the transform where the component resides
    :param component_type: The C# type name of the component GetComponent(type)
    :param name: The field or property name.
    :return: Component value
    """
    # Ensure backwards compatibility with previous versions of this command that took a transform_path string.
    transform_ref = _convert_to_transform_ref(transform_ref)
    
    message_payload = {
        "transform_ref": TransformRef.to_payload(transform_ref),
        "component_type": component_type,
        "name": name
    }
    msg = message.Message("fetch.unity.component.value", message_payload)
    cli.send_message(msg)

    response = cli.read_message()
    verify_response(response)
    return response['payload']['result']


def assign_component_value(cli, transform_ref, component_type, name, value):
    """
    Assigns a value to a component
    :param cli:
    :param transform_ref: The path of the transform where the component resides
    :param component_type: The C# type name of the component GetComponent(type)
    :param name: The field or property name.
    :param value: The value to assign (String | Number | Boolean)
    :return: bool
    """
    # Ensure backwards compatibility with previous versions of this command that took a transform_path string.
    transform_ref = _convert_to_transform_ref(transform_ref)
    
    message_payload = {
        "transform_ref": TransformRef.to_payload(transform_ref),
        "component_type": component_type,
        "name": name,
        "value": value
    }
    msg = message.Message("assign.unity.component.value", message_payload)
    cli.send_message(msg)

    response = cli.read_message()
    verify_response(response)


def await_component_value_equals(cli, transform_ref, component_type, name, value, timeout_seconds=DEFAULT_TIMEOUT_SECONDS):
    """
    Waits for component field or property to become provided value
    :param cli:
    :param transform_ref: The path of the transform where the component resides
    :param component_type: The C# type name of the component GetComponent(type)
    :param name: The field or property name.
    :param value: The value to check for equality (String | Number | Boolean)
    :param timeout_seconds: How long until this returns with failure
    :return bool(response['payload']['success'])
    """
    # Ensure backwards compatibility with previous versions of this command that took a transform_path string.
    transform_ref = _convert_to_transform_ref(transform_ref)
    
    message_payload = {
        "transform_ref": TransformRef.to_payload(transform_ref),
        "component_type": component_type,
        "name": name,
        "value": value,
        "timeout": timeout_seconds
    }
    msg = message.Message("await.unity.component.value.equals", message_payload)
    cli.send_message(msg)

    response = cli.read_message()
    verify_response(response)
    return bool(response['payload']['success'])


def _convert_to_transform_ref(transform_ref):
    """
    Converts the input to a TransformRef. If the input is already a TransformRef, no conversion is performed.

    Conversion is performed to ensure backwards compatibility with commands that previously took a transform_path,
    which now take a transform_ref to distinguish between multiple transforms with the same path.
    :param transform_ref: an instance of TransformRef, or a string representing a transform path.
    :return: If the input is already a TransformRef, no conversion is performed; otherwise, returns a new instance of
    TransformRef containing the specified transform path.
    """
    if not isinstance(transform_ref, TransformRef):
        transform_ref = TransformRef(transform_ref)
    return transform_ref


def _convert_to_transform_refs(transform_refs):
    """
    Converts the input to an array of TransformRef. If the input is already an array of TransformRef, no conversion is
    performed.

    Conversion is performed to ensure backwards compatibility with commands that previously took a transform_path,
    which now take a transform_ref to distinguish between multiple transforms with the same path.
    :param transform_refs: an array of TransformRef, or an array of strings representing transform paths.
    :return: If the input is already an array of TransformRef, no conversion is performed; otherwise, returns an array
    of TransformRefs containing the specified transform paths.
    """
    for i in range(len(transform_refs)):
        transform_refs[i] = _convert_to_transform_ref(transform_refs[i])
    return transform_refs
