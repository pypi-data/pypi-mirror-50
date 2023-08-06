import os


def test_tox_addoption():
    assert os.environ.get('LOCAL_PLUGIN_ADDOPTION') == 'local_addoption'

def test_tox_configure():
    assert os.environ.get('LOCAL_PLUGIN_CONFIGURE') == 'local_configure'

def test_tox_get_python_executable():
    assert os.environ.get('LOCAL_PLUGIN_GET_PYTHON_EXECUTABLE') == 'local_get_python_executable'

def test_tox_runenvreport():
    assert os.environ.get('LOCAL_PLUGIN_RUNENVREPORT') == 'local_runenvreport'
