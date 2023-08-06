import coeus_unity.commands as commands

DEFAULT_TIMEOUT_SECONDS = 60
DEFAULT_TRANSFORM_EXISTS = True
DEFAULT_RENDERER_VISIBLE = True
DEFAULT_SCENE_LOADED = True


def assert_transform_exists(cli, transform_ref):
    """
    Asserts that the transform exists.
    :param cli:
    :param transform_ref:
    :return:
    """
    result = commands.query_transform_exists(cli, transform_ref)
    assert result is True
    return result


def assert_scene_loaded(cli, scene_name):
    """
    Asserts that the scene is loaded.
    :param cli:
    :param scene_name:
    :return:
    """
    result = commands.query_scene_loaded(cli, scene_name)
    assert result is True
    return result


def assert_await_transform_exists(cli, transform_ref, does_exist=DEFAULT_TRANSFORM_EXISTS, timeout_seconds=DEFAULT_TIMEOUT_SECONDS):
    """
    Asserts that we successfully awaited for the transform to exist based on does_exist. If the timeout passes
    or the expression is_registered != actual state, then it will fail.
    :param cli:
    :param transform_ref:
    :param does_exist: (True | False) the state change we are waiting for.
    :param timeout_seconds: The amount of time to wait for a change before fail.
    :return:
    """
    result = commands.await_transform_exists(cli, transform_ref, does_exist, timeout_seconds)
    assert result is True
    return result


def assert_await_any_transforms_exist(cli, transform_refs, does_exist=DEFAULT_TRANSFORM_EXISTS, timeout_seconds=DEFAULT_TIMEOUT_SECONDS):
    """
    Asserts that we successfully awaited for any transforms to exist based on does_exist. If the timeout passes
    or the expression is_registered != actual state, then it will fail.
    :param cli:
    :param transform_refs:
    :param does_exist: (True | False) the state change we are waiting for.
    :param timeout_seconds: The amount of time to wait for a change before fail.
    :return:
    """
    result = commands.await_any_transforms_exist(cli, transform_refs, does_exist, timeout_seconds)
    assert result is True
    return result


def assert_await_all_transforms_exist(cli, transform_refs, does_exist=DEFAULT_TRANSFORM_EXISTS, timeout_seconds=DEFAULT_TIMEOUT_SECONDS):
    """
    Asserts that we successfully awaited for all transforms to exist based on does_exist. If the timeout passes
    or the expression is_registered != actual state, then it will fail.
    :param cli:
    :param transform_refs:
    :param does_exist: (True | False) the state change we are waiting for.
    :param timeout_seconds: The amount of time to wait for a change before fail.
    :return:
    """
    result = commands.await_all_transforms_exist(cli, transform_refs, does_exist, timeout_seconds)
    assert result is True
    return result


def assert_await_renderer_visible(cli, transform_ref, is_visible=DEFAULT_RENDERER_VISIBLE, timeout_seconds=DEFAULT_TIMEOUT_SECONDS):
    """
    Asserts that we successfully awaited for the renderer to be visible based on is_visible. If the timeout passes
    or the expression is_registered != actual state, then it will fail.
    :param cli:
    :param transform_ref:
    :param is_visible: (True | False) the state change we are waiting for.
    :param timeout_seconds: The amount of time to wait for a change before fail.
    :return:
    """
    result = commands.await_renderer_visible(cli, transform_ref, is_visible, timeout_seconds)
    assert result is True
    return result


def assert_await_scene_loaded(cli, scene_name, is_loaded=DEFAULT_SCENE_LOADED, timeout_seconds=DEFAULT_TIMEOUT_SECONDS):
    """
    Asserts that we successfully awaited for the scene to be loaded based on is_loaded. If the timeout passes
    or the expression is_registered != actual state, then it will fail.
    :param cli:
    :param scene_name:
    :param is_loaded: (True | False) the state change we are waiting for.
    :param timeout_seconds: The amount of time to wait for a change before fail.
    :return:
    """
    result = commands.await_scene_loaded(cli, scene_name, is_loaded, timeout_seconds)
    assert result is True
    return result


def assert_component_value_equals(cli, transform_ref, component_type, name, value):
    """
    Asserts that component field or property equals to the provided value
    :param cli:
    :param transform_ref:
    :param component_type: The C# type name of the component GetComponent(type)
    :param name: The field or property name.
    :param value: The value to check for equality (String | Number | Boolean)
    :return:
    """

    result = commands.fetch_component_value(cli, transform_ref, component_type, name)
    assert result == value
    return result


def assert_await_component_value_equals(cli, transform_ref, component_type, name, value, timeout_seconds=DEFAULT_TIMEOUT_SECONDS):
    """
    Asserts that we successfully awaited for the component field or property to become provided value.
    :param cli:
    :param transform_ref: Reference to the transform where the component resides
    :param component_type: The C# type name of the component GetComponent(type)
    :param name: The field or property name.
    :param value: The value to check for equality (String | Number | Boolean)
    :return:
    """

    result = commands.await_component_value_equals(cli, transform_ref, component_type, name, value, timeout_seconds)
    assert result is True
    return result
