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
                  key='1:1c2ab50b-2208-4d84-b59d-87154cae4441'
                  )


# r = c.service('cds.services.echo', 42)
# print(r)


# r = c.service('map.plot', 42)
# print(r)

# r = c.service("catalogue.retrieve",
#     'reanalysis-era5-single-levels',
#     {"variable": "2t",
#         "product_type": "reanalysis",
#         "date": "2012-12-01",
#         "time": "14:00"})

# r = c.service('map.plot', r)

# r.download("test.png")

code = """
import cdstoolbox as ct


@ct.application(title='Hello World!')
@ct.output.figure()
def application():

    data = ct.catalogue.retrieve(
        'seasonal-monthly-single-levels',
        {
            'originating_centre': 'ecmwf',
            'variable': '2m_temperature',
            'product_type': 'ensemble_mean',
            'year': '2018',
            'month': ['02'],
            'leadtime_month': ['1'],
            'format': 'grib'
        }
    )
    print(data)
    # dataset_mean = ct.cube.average(data, ['time', 'realization'])

    fig = ct.cdsplot.figure(subplot_kw={'projection': ct.cdsplot.crs.Robinson()})
    ct.cdsplot.geomap(
        data, pcolormesh_kwargs={'cmap': 'RdBu_r'}, fig=fig,
        title='Mean {long_name}'
    )

    return fig, data
"""


r = c.workflow(code)
print(r)
paths = c.download(r)

print(paths)
