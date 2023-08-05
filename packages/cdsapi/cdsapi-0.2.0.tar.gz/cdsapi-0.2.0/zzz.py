#!/usr/bin/env python

# (C) Copyright 2018 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.

import cdsapi

c = cdsapi.Client()

r  = c.retrieve("reanalysis-era5-pressure-levels",
           {
               "variable": "temperature",
               "pressure_level": "250",
               "product_type": "reanalysis",
               "date": "2017-12-01/2017-12-31",
               "time": "00:00",
               "format": "netcdf"
           })

r.download("dowload.grib")

