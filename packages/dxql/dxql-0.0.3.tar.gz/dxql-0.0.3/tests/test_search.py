import unittest
import os
import json
from pathlib import Path
from dxql import search


# DATA_DIR = Path(os.path.dirname(__file__)) / 'data'

TEST_DATA = [
    {'event': 1, 'k': 'v', 'ip': 7, 'index': 'geoip'},
    {'event': 2, 'k': 'v', 'ip': 10, 'index': 'geoip'},
    {'event': 3, 'k': 'v', 'ip': 15, 'index': 'geoip'},
    {'ip': 7, 'handle': 'handle1', 'index': 'ip_rdap'},
    {'ip': 10, 'handle': 'handle2', 'index': 'ip_rdap'},
    {'ip': 15, 'handle': 'handle3', 'index': 'ip_rdap'},
    {'ip': 19, 'handle': 'handle3', 'index': 'ip_rdap'},
    {'ip': 21, 'handle': 'handle3', 'index': 'ip_rdap'},
    {'event': 4, 'k': 'v1', 'handle': 'handle1', 'index': 'rdap'},
    {'event': 5, 'k': 'v2', 'handle': 'handle2', 'index': 'rdap'},
    {'event': 6, 'k': 'v3', 'handle': 'handle3', 'index': 'rdap'}
]


if __name__ == '__main__':
    unittest.main()


class TestEverything(unittest.TestCase):
    def setUp(self):
        self.query = ''
        self.expected = []

    def do_it(self):
        pipeline = search.Pipeline.create_pipeline(self.query, True)
        actual = list(pipeline.execute(TEST_DATA))
        self.assertEqual(self.expected, actual)

    def test_search_no_expressions(self):
        self.expected = TEST_DATA
        self.query = 'search'

        self.do_it()

    def test_search_one_expression(self):
        self.expected = [
            {'event': 1, 'k': 'v', 'ip': 7, 'index': 'geoip'},
            {'event': 2, 'k': 'v', 'ip': 10, 'index': 'geoip'},
            {'event': 3, 'k': 'v', 'ip': 15, 'index': 'geoip'}
        ]

        self.query = 'search index=geoip'

        self.do_it()

    def test_search_conjunction(self):
        self.expected = [
            {'event': 2, 'k': 'v', 'ip': 10, 'index': 'geoip'}
        ]

        self.query = 'search index=geoip ip=10'

        self.do_it()

    def test_search_ne_expression(self):
        self.expected = [
            {'event': 2, 'k': 'v', 'ip': 10, 'index': 'geoip'},
            {'event': 3, 'k': 'v', 'ip': 15, 'index': 'geoip'}
        ]

        self.query = 'search index=geoip ip!=7'

        self.do_it()

    def test_search_lt_expression(self):
        self.expected = [
            {'event': 1, 'k': 'v', 'ip': 7, 'index': 'geoip'}
        ]

        self.query = 'search index=geoip ip<10'

        self.do_it()

    def test_search_le_expression(self):
        self.expected = [
            {'event': 1, 'k': 'v', 'ip': 7, 'index': 'geoip'},
            {'event': 2, 'k': 'v', 'ip': 10, 'index': 'geoip'}
        ]

        self.query = 'search index=geoip ip<=10'

        self.do_it()

    def test_search_gt_expression(self):
        self.expected = [
            {'event': 3, 'k': 'v', 'ip': 15, 'index': 'geoip'}
        ]

        self.query = 'search index=geoip ip>10'

        self.do_it()

    def test_search_ge_expression(self):
        self.expected = [
            {'event': 2, 'k': 'v', 'ip': 10, 'index': 'geoip'},
            {'event': 3, 'k': 'v', 'ip': 15, 'index': 'geoip'}
        ]

        self.query = 'search index=geoip ip>=10'

        self.do_it()

    def test_search_field_dne(self):
        self.expected = []

        self.query = 'search index=geoip derp=herp'

        self.do_it()

    def test_search_no_matches(self):
        self.expected = []

        self.query = 'search index=geoip ip=2'

        self.do_it()

    def test_search_asterisk(self):
        self.expected = [
            {'event': 1, 'k': 'v', 'ip': 7, 'index': 'geoip'},
            {'event': 2, 'k': 'v', 'ip': 10, 'index': 'geoip'},
            {'event': 3, 'k': 'v', 'ip': 15, 'index': 'geoip'}
        ]

        self.query = 'search index=geoip ip=*'

        self.do_it()

    def test_search_disjunction(self):
        self.expected = [
            {'event': 2, 'k': 'v', 'ip': 10, 'index': 'geoip'},
            {'event': 3, 'k': 'v', 'ip': 15, 'index': 'geoip'}
        ]

        self.query = 'search index=geoip ip=10 or ip=15'

        self.do_it()

    def test_search_not(self):
        self.expected = [
            {'event': 1, 'k': 'v', 'ip': 7, 'index': 'geoip'},
            {'event': 3, 'k': 'v', 'ip': 15, 'index': 'geoip'}
        ]

        self.query = 'search index=geoip not ip=10'

        self.do_it()

    def test_search_disjunction_not(self):
        self.expected = [
            {'event': 1, 'k': 'v', 'ip': 7, 'index': 'geoip'},
            {'event': 2, 'k': 'v', 'ip': 10, 'index': 'geoip'},
            {'event': 3, 'k': 'v', 'ip': 15, 'index': 'geoip'}
        ]

        self.query = 'search index=geoip not ip=10 or event=2'

        self.do_it()

    def test_search_fields(self):
        self.expected = [
            {'ip': 7},
            {'ip': 10},
            {'ip': 15}
        ]

        self.query = 'search index=geoip | fields ip'

        self.do_it()

    def test_search_fields_multiple(self):
        self.expected = [
            {'event': 1, 'ip': 7},
            {'event': 2, 'ip': 10},
            {'event': 3, 'ip': 15}
        ]

        self.query = 'search index=geoip | fields event ip'

        self.do_it()

    def test_search_fields_join(self):
        self.expected = [
            {'handle': 'handle1', 'index': ['ip_rdap', 'rdap'], 'event': 4, 'ip': 7},
            {'handle': 'handle2', 'index': ['ip_rdap', 'rdap'], 'event': 5, 'ip': 10},
            {'handle': 'handle3', 'index': ['ip_rdap', 'rdap'], 'event': 6, 'ip': [15, 19, 21]}
        ]

        self.query = 'search index=ip_rdap or index=rdap or index=geoip | fields index ip handle event | join handle'

        self.do_it()

    def test_search_fields_join_prettyprint_json(self):
        self.expected = [
            '{\n'
            '    "index": [\n'
            '        "ip_rdap",\n'
            '        "rdap"\n'
            '    ],\n'
            '    "ip": 7,\n'
            '    "handle": "handle1",\n'
            '    "event": 4\n'
            '}',
            '{\n'
            '    "index": [\n'
            '        "ip_rdap",\n'
            '        "rdap"\n'
            '    ],\n'
            '    "ip": 10,\n'
            '    "handle": "handle2",\n'
            '    "event": 5\n'
            '}',
            '{\n'
            '    "index": [\n'
            '        "ip_rdap",\n'
            '        "rdap"\n'
            '    ],\n'
            '    "ip": [\n'
            '        15,\n'
            '        19,\n'
            '        21\n'
            '    ],\n'
            '    "handle": "handle3",\n'
            '    "event": 6\n'
            '}'
        ]

        self.query = 'search index=ip_rdap or index=rdap | fields index ip handle event | join handle | prettyprint format=json'

        self.do_it()

    def test_search_fields_join_prettyprint_table(self):
        self.expected = [
            'index                ip            handle   event  ',
            "['ip_rdap', 'rdap']  7             handle1  4      ",
            "['ip_rdap', 'rdap']  10            handle2  5      ",
            "['ip_rdap', 'rdap']  [15, 19, 21]  handle3  6      "
        ]

        self.query = 'search index=ip_rdap or index=rdap | fields index ip handle event | join handle | prettyprint format=table'

        self.do_it()


class TestPipelineToJson(unittest.TestCase):
    def test(self):
        pipeline = search.Pipeline.create_pipeline('search index=geoip not ip=10 or event>=2 | fields index ip handle event | join handle | prettyprint format=table')

        expected = [
            {
                'type': 'search',
                'expressions': [
                    {
                        'type': 'comparison',
                        'field': 'index',
                        'val': 'geoip',
                        'op': 'eq'
                    },
                    {
                        'type': 'disjunction',
                        'parts': [
                            {
                                'type': 'not',
                                'item': {
                                    'type': 'comparison',
                                    'field': 'ip',
                                    'val': '10',
                                    'op': 'eq'
                                }
                            },
                            {
                                'type': 'comparison',
                                'field': 'event',
                                'val': '2',
                                'op': 'ge'
                            }
                        ]
                    }
                ]
            },
            {
                'type': 'fields',
                'fields': ['index', 'ip', 'handle', 'event']
            },
            {
                'type': 'join',
                'by_field': 'handle',
                'args': {},
                'where': []
            },
            {
                'type': 'prettyprint',
                'format': 'table'
            }
        ]

        actual = pipeline.to_json()

        self.assertEqual(expected, actual)
