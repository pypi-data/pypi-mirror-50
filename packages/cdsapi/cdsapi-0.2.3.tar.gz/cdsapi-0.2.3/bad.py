#!/usr/bin/env python

# (C) Copyright 2018 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

import cdsapi

c = cdsapi.Client(debug=True)

r = c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'variable': 'evaporation',
        'product_type': 'reanalysis',
        'date': '20170827',
        'time': '11:00',
        # 'area': [63, -82,43,-54 ],
    }, 'data.grib')
