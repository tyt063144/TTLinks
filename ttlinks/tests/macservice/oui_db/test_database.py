import pytest

from ttlinks.macservice.oui_db.database import LocalOUIDatabase
from ttlinks.macservice.oui_utils import OUIUnit


@pytest.fixture
def db():
    return LocalOUIDatabase()

def test_search(db):
    mac = "08-BF-B8"
    result = db.search(mac)
    assert result.record.get('organization') == 'ASUSTek COMPUTER INC.'

def test_bulk_search(db):
    macs = ["08-BF-B8", "00:09:0F:FE:0A:9B", 'aa-bb-cc-dd-ee-ff']
    results = db.bulk_search(macs)
    assert isinstance(results['08-BF-B8'], OUIUnit)
    assert isinstance(results['00:09:0F:FE:0A:9B'], OUIUnit)
    assert results['aa-bb-cc-dd-ee-ff'] is None

def test_bulk_search_empty(db):
    macs = []
    results = db.bulk_search(macs)
    assert results == {}

def test_search_invalid_mac(db):
    mac = "invalid_mac"
    result = db.search(mac)
    assert result is None

def test_bulk_search_with_invalid_mac(db):
    macs = ["invalid_mac"]
    results = db.bulk_search(macs)
    assert results['invalid_mac'] is None