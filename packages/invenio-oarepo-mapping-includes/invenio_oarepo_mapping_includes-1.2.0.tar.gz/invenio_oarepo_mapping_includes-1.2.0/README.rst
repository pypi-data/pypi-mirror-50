===============================
OARepo Invenio data model
===============================

.. image:: https://img.shields.io/github/license/oarepo/oarepo-invneio.svg
        :target: https://github.com/oarepo/oarepo-invneio/blob/master/LICENSE

.. image:: https://img.shields.io/travis/oarepo/oarepo-invneio.svg
        :target: https://travis-ci.org/oarepo/oarepo-invneio

.. image:: https://img.shields.io/coveralls/oarepo/oarepo-invneio.svg
        :target: https://coveralls.io/r/oarepo/oarepo-invneio

.. image:: https://img.shields.io/pypi/v/oarepo-invneio.svg
        :target: https://pypi.org/pypi/oarepo-invneio


DC Terms data model for oarepo.


Quickstart
----------

Add this package to your dependencies. Create a directory structure containing
mappings that will be used in includes::

    <project_package>
        +- included_mappings
            +- v6
                +- multilingual-v1.0.0.json


The content of `multilingual-v1.0.0.json` is::

    {
      "MultilingualString": {
        "type": "nested",
        "properties": {
          "name": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 100
              }
            }
          },
          "lang": {
            "type": "keyword",
            "ignore_above": 3
          }
        }
      }
    }

Register the `included_mappings` directory in entry points::

    entry_points={
        'invenio_oarepo_mapping_includes': [
            '<project_package>=<project_package>.included_mappings'
        ]
    },

and do not forget to run pip install.

In ES mapping you can now include types contained in `multilingual-v1.0.0.json`::

    {
      "mappings": {
        "_doc": {
          "properties": {
            "title": {
              "type": "multilingual-v1.0.0.json#/MultilingualString"
            }
          }
        }
      }
    }

The `type` contains the file name of the json file followed by `#` and json pointer
to the definition.

If you want to include properties from multiple types in your properties, you can
use the `allOf` directive::

      {
        "mappings": {
          "_doc": {
            "allOf": [
               { "type": "invenio-v1.0.0.json#/InvenioRecord" },
               { "type": "dcterms-v1.0.0.json#/DCObject" }
            ],
            "properties": {
              "prop": {
                "type": "keyword"
              },
            }
          }
        }
      }

Doing so will include all properties from all referenced types in your mappings properties.

When `invenio index init` is run, the mapping is preprocessed, "type" is dereferenced
and the definition is replaced with the content found in the referenced type.
