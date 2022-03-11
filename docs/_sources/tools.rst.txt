Tools
=====

Atom6 contains a directory ``tools`` that is not part of the library distribution but was instrumental in its creation
and testing. The directory contains python scripts for scraping values from the EPA's SGEC workbook for each of the
emissions pages as well as for the factors, and a set of dictionaries for tokenizing the string values from these pages
for the API. It also maintains a separate requirements.txt for packages used in it but not for the atom6 dist. The main
package used for scraping the workbook is pandas.

Tokenization
------------

``__init__.py`` contains a set of dictionaries that are used for tokenizing strings into approximate camelcase values
for atom6. This was done to eliminate spaces, dashes, etc. in values as well as standardize variable references to the
same value.

Example:
::

    tokenization_map_units = {
        'Dth (Decatherm)': 'decatherm',
        'Mcf': 'mcf',
        'Mlb (1,000 pounds)': 'mlb',
        'ccf': 'ccf',
        'cubic meter': 'cubicMeter',
        'kWh': 'kWh',
        'lb': 'lb',
        'mmBtu': 'mmbtu',
        'short ton': 'shortTon',
        'therm': 'therm',
        'Short ton': 'shortTon',
        'short tons': 'shortTon',
        'gallon': 'gallons',
        'gallons': 'gallons',
        'scf': 'scf',
        'Gallons': 'gallons',

Factors Scraper
---------------

``create_conversion_constants.py`` is the single script that scrapes, formats all factors from their tables in the
EPA's SGEC workbook and saves them in atom6-ghg/atom6ghg/factors/source_data. For each set of factors there is a
``make_...`` function, though that function may open more than one table at a time for condensing into one set. E.g.,
``make_mobile_combustion_ch4_and_n2o_emission_factors`` scrapes the three tables: CH4 and N2O Emissions for Highway
Vehicles, and CH4 and N2O Emissions for Non-Road Vehicles, and arranges their data into one set of factors. Further, the
data was tokenized as well as arranged into a form for ease of use in the formulas given the API. E.g., for Mobile
Sources, users have the option to enter year for vehicles which may or may not be necessary depending on the vehicle
type and fuel type combination. The factors for CH4 and N2O emissions

The only factors that were hand crafted and were not created as part of this script were \
``refrigeration_and_ac_equipment_emission_factors.json`` (see :ref:`refrigeration-equipment-factors` for further
information).