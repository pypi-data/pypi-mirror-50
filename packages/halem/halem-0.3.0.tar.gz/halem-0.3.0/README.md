[ ![Documentation](https://img.shields.io/badge/sphinx-documentation-informational.svg)](https://halem.readthedocs.io)
[ ![License: MIT](https://img.shields.io/badge/License-MIT-informational.svg)](https://github.com/TUDelft-CITG/HALEM/blob/master/LICENSE.txt)
[ ![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3251545.svg)](https://doi.org/10.5281/zenodo.3251545)

[![CircleCI](https://circleci.com/gh/TUDelft-CITG/HALEM.svg?style=svg&circle-token=64796bff34a56507bad599a6cec980b7b8be0bb9)](https://circleci.com/gh/TUDelft-CITG/HALEM)


Route optimization in dynamic flow fields
====================================

## Features
This package contains route optimization for given currents. The following features are taken into account in this version:
* Spatial varying currents
* Temporal changing currents
* Variable shipping velocity
* minimal water depth
* Squad

Does not take into account:
* Inertial behavior of the ship

Different routes that can be optimized are:
* Shortest route (halem.HALEM_time)
* Fastest route (halem.HALEM_space)
* Cheapest route route (halem.HALEM_cost)
* Cleanest route (halem.HALEM_co2)

## Implementation
This package is built for implementation into the Open CL-Sim package (see https://github.com/TUDelft-CITG/OpenCLSim). 


## Installation
The Package can be installed using pip. Type following code in the python command prompt:

``` bash
pip install halem
```
