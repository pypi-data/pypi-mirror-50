#!/usr/bin/env python

# (C) Copyright 2018 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

import cdsapi

c = cdsapi.Client(full_stack=True,
                  debug=True,
                  url='https://cds-test.climate.copernicus.eu/api/v2',
                  key='1:1c2ab50b-2208-4d84-b59d-87154cae4441')


# r = c.service('cds.services.echo', 42)
# print(r)


# r = c.service('map.plot', 42)
# print(r)

r = c.service("catalogue.retrieve",
    'reanalysis-era5-single-levels',
    {"variable": "2t",
        "product_type": "reanalysis",
        "date": "2012-12-01",
        "time": "14:00"})

r = c.service('map.plot', r)

r.download("test.png")


