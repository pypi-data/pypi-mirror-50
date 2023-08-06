from ayarami import Settings, DEFAULT_SETTINGS_NAME
import pytest

TEST_SETTINGS_NAME = "_test"


@pytest.fixture
def reset_instances():
    for instance in [key for key in Settings._instances.keys() if key != DEFAULT_SETTINGS_NAME]:
        Settings.del_instance(instance)
    Settings.get_instance(DEFAULT_SETTINGS_NAME).clear()


# noinspection PyProtectedMember
def test_default_creation():
    assert len(Settings._instances)
    assert DEFAULT_SETTINGS_NAME in Settings._instances


def test_get_instance(reset_instances):
    with pytest.raises(KeyError):
        Settings.get_instance(TEST_SETTINGS_NAME)
    assert Settings.get_instance(DEFAULT_SETTINGS_NAME)


def test_del_instance(reset_instances):
    Settings(TEST_SETTINGS_NAME)
    assert Settings.get_instance(TEST_SETTINGS_NAME)

    Settings.del_instance(TEST_SETTINGS_NAME)
    with pytest.raises(KeyError):
        Settings.get_instance(TEST_SETTINGS_NAME)

    with pytest.raises(ValueError):
        Settings.del_instance(DEFAULT_SETTINGS_NAME)


def test_set_instance(reset_instances):
    # noinspection PyMissingConstructor
    class _Throwaway(Settings):
        def __init__(self, name):
            self._name = name
            self._registry = {}

    with pytest.raises(ValueError):
        Settings.set_instance(_Throwaway(DEFAULT_SETTINGS_NAME))

    Settings.set_instance(_Throwaway(TEST_SETTINGS_NAME))
    with pytest.raises(ValueError):
        Settings.set_instance(_Throwaway(TEST_SETTINGS_NAME))


def test_init(reset_instances):
    instance = Settings(TEST_SETTINGS_NAME)
    assert instance._name == TEST_SETTINGS_NAME
    assert instance._registry == {}
    assert TEST_SETTINGS_NAME in Settings._instances
    Settings.del_instance(TEST_SETTINGS_NAME)


def test_configure_and_getattr_str(reset_instances):
    instance = Settings.get_instance(DEFAULT_SETTINGS_NAME)
    instance.configure("tests.confs.a_config_file")
    assert instance.A == 10
    with pytest.raises(KeyError):
        _ = instance._B
    assert instance.C_ == 30


def test_configure_and_getattr_module(reset_instances):
    instance = Settings.get_instance(DEFAULT_SETTINGS_NAME)
    import tests.confs.another_config_file
    # noinspection PyTypeChecker
    instance.configure(tests.confs.another_config_file)
    assert instance.A == 101
    with pytest.raises(KeyError):
        _ = instance._B
    assert instance.C_ == 303


def test_configure_and_getattr_etc(reset_instances):
    instance = Settings.get_instance(DEFAULT_SETTINGS_NAME)

    class _Throwaway:
        A = 10
        C_ = 30
        NAME = "_Throwaway"

    with pytest.raises(ValueError):
        # noinspection PyTypeChecker
        instance.configure(_Throwaway)


def test_configure_and_getattr(reset_instances):
    instance = Settings.get_instance(DEFAULT_SETTINGS_NAME)

    with pytest.raises(ValueError):
        _ = instance.SOMETHING

    instance.configure("tests.confs.a_config_file")
    instance.configure("tests.confs.another_config_file")
    assert instance.A == 101
    assert instance.C_ == 303
    assert instance.NAME == "a_config_file"
    assert instance.NAME2 == "another_config_file"
