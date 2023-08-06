from keynote_parser.unicode_utils import \
    fix_unicode, to_py3_compatible, to_py2_compatible


def test_non_surrogate_pair():
    assert fix_unicode('\u2716\uFE0F') == '\u2716\uFE0F'
    assert to_py2_compatible('\u2716\uFE0F') == '\u2716\uFE0F'
    assert to_py3_compatible('\u2716\uFE0F') == '\u2716\uFE0F'


def test_surrogate_pair():
    assert to_py2_compatible(r'\U0001F1E8\U0001F1E6') \
        == r'\ud83c\udde8\ud83c\udde6'
    assert to_py3_compatible(r'\ud83c\udde8\ud83c\udde6') \
        == r'\U0001f1e8\U0001f1e6'


def test_basic_multilingual_plane():
    srpska = r'\u0441\u0440\u043f\u0441\u043a\u0430'
    assert to_py2_compatible(srpska) == srpska
    assert to_py3_compatible(srpska) == srpska
