import pytest, os

from ttlinks.macservice.oui_file_parsers import OuiFileParser

base_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_resources/')


def test_iab_txt_parser():
    result = OuiFileParser.parse_oui_file(os.path.join(base_folder, 'test_iab.txt'))
    assert result['md5'] is not None
    assert result['type'].name == 'IAB'
    assert len(result['oui_units']) != 0


def test_iab_csv_parser():
    result = OuiFileParser.parse_oui_file(os.path.join(base_folder, 'test_iab.csv'))
    assert result['md5'] is not None
    assert result['type'].name == 'IAB'
    assert len(result['oui_units']) != 0


def test_mas_txt_parser():
    result = OuiFileParser.parse_oui_file(os.path.join(base_folder, 'test_mas.txt'))
    assert result['md5'] is not None
    assert result['type'].name == 'MA_S'
    assert len(result['oui_units']) != 0


def test_mas_csv_parser():
    result = OuiFileParser.parse_oui_file(os.path.join(base_folder, 'test_mas.csv'))
    assert result['md5'] is not None
    assert result['type'].name == 'MA_S'
    assert len(result['oui_units']) != 0


def test_mam_txt_parser():
    result = OuiFileParser.parse_oui_file(os.path.join(base_folder, 'test_mam.txt'))
    assert result['md5'] is not None
    assert result['type'].name == 'MA_M'
    assert len(result['oui_units']) != 0


def test_mam_csv_parser():
    result = OuiFileParser.parse_oui_file(os.path.join(base_folder, 'test_mam.csv'))
    assert result['md5'] is not None
    assert result['type'].name == 'MA_M'
    assert len(result['oui_units']) != 0


def test_mal_txt_parser():
    result = OuiFileParser.parse_oui_file(os.path.join(base_folder, 'test_mal.txt'))
    assert result['md5'] is not None
    assert result['type'].name == 'MA_L'
    assert len(result['oui_units']) != 0


def test_mal_csv_parser():
    result = OuiFileParser.parse_oui_file(os.path.join(base_folder, 'test_mal.csv'))
    assert result['md5'] is not None
    assert result['type'].name == 'MA_L'
    assert len(result['oui_units']) != 0


def test_cid_txt_parser():
    result = OuiFileParser.parse_oui_file(os.path.join(base_folder, 'test_cid.txt'))
    assert result['md5'] is not None
    assert result['type'].name == 'CID'
    assert len(result['oui_units']) != 0


def test_cid_csv_parser():
    result = OuiFileParser.parse_oui_file(os.path.join(base_folder, 'test_cid.csv'))
    assert result['md5'] is not None
    assert result['type'].name == 'CID'
    assert len(result['oui_units']) != 0
