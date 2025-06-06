# =================================================================
#
# Authors: Tom Kralidis <tomkralidis@gmail.com>
#          Ricardo Garcia Silva <ricardo.garcia.silva@gmail.com>
#
# Copyright (c) 2025 Tom Kralidis
# Copyright (c) 2023 Ricardo Garcia Silva
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

import json
from xml.etree import ElementTree as etree

import pytest

from pycsw.ogc.api.records import API

pytestmark = pytest.mark.functional


def test_landing_page(config_virtual_collections):
    api = API(config_virtual_collections)
    headers, status, content = api.landing_page({}, {'f': 'json'})
    content = json.loads(content)

    assert headers['Content-Type'] == 'application/json'
    assert status == 200
    assert len(content['links']) == 15

    for link in content['links']:
        assert link['href'].startswith(api.config['server']['url'])

    headers, status, content = api.landing_page({}, {'f': 'html'})
    assert status == 200
    assert headers['Content-Type'] == 'text/html'


def test_openapi(config_virtual_collections):
    api = API(config_virtual_collections)
    headers, status, content = api.openapi({}, {'f': 'json'})
    assert status == 200
    json.loads(content)
    assert headers['Content-Type'] == 'application/vnd.oai.openapi+json;version=3.0'  # noqa

    headers, status, content = api.openapi({}, {'f': 'html'})
    assert status == 200
    assert headers['Content-Type'] == 'text/html'


def test_conformance(config_virtual_collections):
    api = API(config_virtual_collections)
    content = json.loads(api.conformance({}, {})[2])

    assert len(content['conformsTo']) == 14


def test_collections(config_virtual_collections):
    api = API(config_virtual_collections)
    content = json.loads(api.collections({}, {})[2])

    assert len(content['links']) == 2
    assert len(content['collections']) == 2

    content = json.loads(api.collections({}, {})[2])['collections'][0]
    assert len(content['links']) == 4
    assert content['id'] == 'metadata:main'
    assert content['title'] == 'pycsw Geospatial Catalogue'
    assert content['description'] == 'pycsw is an OARec and OGC CSW server implementation written in Python'  # noqa
    assert content['itemType'] == 'record'


def test_queryables(config_virtual_collections):
    api = API(config_virtual_collections)
    content = json.loads(api.queryables({}, {})[2])

    assert content['type'] == 'object'
    assert content['title'] == 'pycsw Geospatial Catalogue'
    assert content['$id'] == 'http://localhost/pycsw/oarec/collections/metadata:main/queryables'  # noqa
    assert content['$schema'] == 'http://json-schema.org/draft/2019-09/schema'

    assert len(content['properties']) == 14

    assert 'geometry' in content['properties']
    assert content['properties']['geometry']['$ref'] == 'https://geojson.org/schema/Polygon.json'  # noqa

    headers, status, content = api.queryables({}, {}, 'foo')
    assert status == 400


def test_items(config_virtual_collections):
    api = API(config_virtual_collections)
    content = json.loads(api.items({}, None, {})[2])

    assert content['type'] == 'FeatureCollection'
    assert len(content['links']) == 4
    assert content['numberMatched'] == 12
    assert content['numberReturned'] == 10
    assert len(content['features']) == 10
    assert len(content['features']) == content['numberReturned']

    params = {'q': 'Lorem'}
    content = json.loads(api.items({}, None, params)[2])
    assert content['numberMatched'] == 5
    assert content['numberReturned'] == 5
    assert len(content['features']) == content['numberReturned']

    params = {'q': 'Lorem dolor'}
    content = json.loads(api.items({}, None, params)[2])
    assert content['numberMatched'] == 1
    assert content['numberReturned'] == 1
    assert len(content['features']) == content['numberReturned']

    params = {'bbox': '-50,0,50,80'}
    content = json.loads(api.items({}, None, params)[2])
    assert content['numberMatched'] == 3
    assert content['numberReturned'] == 3
    assert len(content['features']) == content['numberReturned']

    params = {'bbox': '-50,0,50,80', 'q': 'Lorem'}
    content = json.loads(api.items({}, None, params)[2])
    assert content['numberMatched'] == 1
    assert content['numberReturned'] == 1
    assert len(content['features']) == content['numberReturned']

    params = {'filter': "title LIKE '%%Lorem%%'"}
    content = json.loads(api.items({}, None, params)[2])
    assert content['numberMatched'] == 2
    assert content['numberReturned'] == 2
    assert len(content['features']) == content['numberReturned']

    params = {'filter': "title LIKE '%%Lorem%%'", 'q': 'iPsUm'}
    content = json.loads(api.items({}, None, params)[2])
    assert content['numberMatched'] == 2
    assert content['numberReturned'] == 2
    assert len(content['features']) == content['numberReturned']

    params = {'limit': 0}
    content = json.loads(api.items({}, None, params)[2])
    assert content['code'] == 'InvalidParameterValue'
    assert content['description'] == 'Limit must be a positive integer'

    params = {'limit': 4}
    content = json.loads(api.items({}, None, params)[2])
    assert content['numberMatched'] == 12
    assert content['numberReturned'] == 4
    assert len(content['features']) == content['numberReturned']

    params = {'limit': 4, 'offset': 10}
    content = json.loads(api.items({}, None, params)[2])
    assert content['numberMatched'] == 12
    assert content['numberReturned'] == 2
    assert len(content['features']) == content['numberReturned']

    params = {'sortby': 'title'}
    content = json.loads(api.items({}, None, params)[2])
    assert content['numberMatched'] == 12
    assert content['numberReturned'] == 10
    assert content['features'][5]['properties']['title'] == 'Lorem ipsum'

    params = {'sortby': '-title'}
    content = json.loads(api.items({}, None, params)[2])
    assert content['numberMatched'] == 12
    assert content['numberReturned'] == 10
    assert content['features'][5]['properties']['title'] == 'Lorem ipsum dolor sit amet'  # noqa

    cql_json = {'op': '=', 'args': [{'property': 'title'}, 'Lorem ipsum']}
    content = json.loads(api.items({}, cql_json, {})[2])
    assert content['numberMatched'] == 1
    assert content['numberReturned'] == 1
    assert len(content['features']) == content['numberReturned']

    cql_json = {'op': '=', 'args': [{'property': 'title'}, 'Lorem ipsum']}
    content = json.loads(api.items({}, cql_json, {'limit': 1})[2])
    assert content['numberMatched'] == 1
    assert content['numberReturned'] == 1
    assert len(content['features']) == content['numberReturned']

    cql_json = {'op': 'like', 'args': [{'property': 'title'}, 'lorem%']}
    content = json.loads(api.items({}, cql_json, {})[2])
    assert content['numberMatched'] == 2
    assert content['numberReturned'] == 2
    assert len(content['features']) == content['numberReturned']

    headers, status, content = api.items({}, {}, {}, 'foo')
    assert status == 400


def test_item(config_virtual_collections):
    api = API(config_virtual_collections)
    item = 'urn:uuid:19887a8a-f6b0-4a63-ae56-7fba0e17801f'
    content = json.loads(api.item({}, {}, 'metadata:main', item)[2])

    assert content['id'] == item
    assert content['type'] == 'Feature'
    assert content['properties']['title'] == 'Lorem ipsum'
    assert content['properties']['keywords'] == ['Tourism--Greece']

    item = 'urn:uuid:19887a8a-f6b0-4a63-ae56-7fba0e17801f'
    params = {'f': 'xml'}
    content = api.item({}, params, 'metadata:main', item)[2]

    e = etree.fromstring(content)

    element = e.find('{http://purl.org/dc/elements/1.1/}identifier').text
    assert element == item

    element = e.find('{http://purl.org/dc/elements/1.1/}type').text
    assert element == 'http://purl.org/dc/dcmitype/Image'

    element = e.find('{http://purl.org/dc/elements/1.1/}title').text
    assert element == 'Lorem ipsum'

    element = e.find('{http://purl.org/dc/elements/1.1/}subject').text
    assert element == 'Tourism--Greece'

    headers, status, content = api.item({}, {}, 'foo', item)
    assert status == 400
