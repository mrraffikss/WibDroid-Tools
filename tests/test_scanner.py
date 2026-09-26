import pytest
from security.scanner import scan_apk

def test_missing_apk():
    with pytest.raises(FileNotFoundError): scan_apk('missing.apk')
