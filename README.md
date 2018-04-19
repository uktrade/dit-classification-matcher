# DIT CPV, HS & Taric Mapping Service

This service does one thing and this is to provide HS & TARIC codes from a CPV input. Input data used is *HS2017* and *CPV2008*.

![Pass the butter](https://vignette.wikia.nocookie.net/rickandmorty/images/6/67/Butter_Robot_Picture.png/revision/latest?cb=20171106225602 "Butter Robot")

We aim to follow [GDS service standards](https://www.gov.uk/service-manual/service-standard) and [GDS design principles](https://www.gov.uk/design-principles).

## Installation

```pip install flask```
```chmod a+x app.py```
```./app.py```

## Running tests

TBA

## Style checking

Run style checks with pep8. There is a custom, minimal pep8 configuration file.

## Concepts

### Endpoints

There is a single usable endpoint at the moment, /api/v1/cpv/<CPVID>.

A sample request at _http://localhost:5000/api/v1/cpv/03141000_ will return:

{
  "cpv": {
    "description": "Bulls' semen", 
    "id": 3141000, 
    "uri": "http://localhost:5000/api/v1/cpv/3141000"
  }, 
  "hs": {
    "description": "051110 - Animal products; bovine semen", 
    "id": "051110"
  }
}

There is also an endpoint listing all the CPV entries, /api/v1/cpvs.

### License

MIT licensed. See the bundled LICENSE file for more details.
  
## Deployment
  
TBA

## Contribution

You are welcome to contribute, please get in touch with [Alex Giamas](mailto:alexandros.giamas@digital.trade.gov.uk) or [Mateusz Lapsa Malawski](mailto:mateusz.lapsa-malawski@digital.trade.gov.uk).


