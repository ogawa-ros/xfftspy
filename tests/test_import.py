import xfftspy

def test_version_is_valid():
    assert isinstance(xfftspy.__version__, str)
    assert xfftspy.__version__ not in ["", "0.0.0"]
