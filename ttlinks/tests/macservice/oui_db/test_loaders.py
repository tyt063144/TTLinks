from ttlinks.macservice.oui_db.loaders import LocalIabLoader, LocalMasLoader, LocalMamLoader, LocalMalLoader, LocalCidLoader


def test_local_iab_loader():
    loader = LocalIabLoader()
    loader.connect()
    loader.load()
    print(loader.data['md5'])
    assert isinstance(loader.data['md5'], str)
    assert loader.data['type'] == 'IAB'


def test_local_mas_loader():
    loader = LocalMasLoader()
    loader.connect()
    loader.load()
    print(loader.data['md5'])
    assert isinstance(loader.data['md5'], str)
    assert loader.data['type'] == 'MA_S'


def test_local_mam_loader():
    loader = LocalMamLoader()
    loader.connect()
    loader.load()
    print(loader.data['md5'])
    assert isinstance(loader.data['md5'], str)
    assert loader.data['type'] == 'MA_M'


def test_local_mal_loader():
    loader = LocalMalLoader()
    loader.connect()
    loader.load()
    print(loader.data['md5'])
    assert isinstance(loader.data['md5'], str)
    assert loader.data['type'] == 'MA_L'


def test_local_cid_loader():
    loader = LocalCidLoader()
    loader.connect()
    loader.load()
    print(loader.data['md5'])
    assert isinstance(loader.data['md5'], str)
    assert loader.data['type'] == 'CID'
