from eppzy.util import parse_datetime


def test_parse_datetime():
    # ISO datetime
    parse_datetime('2019-08-01T10:52:03.423Z')
    # nominet datetime
    parse_datetime('2019-08-01T10:52:03')
