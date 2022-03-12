.. _sgec-factors:

Factors
-------

All physical constants and green house gas factors used in this library are pulled directly from the EPA's SGEC workbook,
specifically the sheets Unit Conversions, Heat Content and Emissions Factors, as well as some miscellaneous values
embedded in formulas and tables on other sheets.

Implementation
**************


In atom6, factors are python classes that wrap dictionaries saved in json files that are scraped from the EPA's SGEC
workbook. The Emission Factors sheet has many tables of factors, and there is a near one-to-one correspondence of each
of these tables and a factors class in atom6 as each table is used independent of each other (the exception to the
one-to-one correspondence is for mobile sources and refrigerants). The factor data are formatted in a way that is most
convenient for access for calculations in the formulas, and as such some data in the tables in the EPA SGEC workbook
are not in the factors in Atom 6 as they are superfluous with respect to the formula even though they may be
informative for a user referencing the tables. For example, the "CO2 Emissions for Road Vehicles" table on the
Emission Factors sheet is scraped and formatted into mobile_combustion_co2_emission_factors.json:

::

    {
      "gasoline": 8.78,
      "diesel": 10.21,
      "residualFuelOil": 11.27,
      "aviationGasoline": 8.31,
      "jetFuel": 9.75,
      "lpg": 5.68,
      "ethanol": 5.75,
      "biodiesel": 9.45,
      "lng": 4.5,
      "cng": 0.05444
    }

and omits the units column as the units entered for the mobile sources are assumed to be only those units. Also,
convenience refers to the ability to access the factors needed in a calculation given user input with a minimum number
of lookups. Typically this looks like factors[required_user_input_1][required_user_input_2]... -> value. For example,
on the stationary combustion page, users input the fuel type and units associated with the amount of fuel combusted.
The heat_content_factors.json (in this case for unit conversion to a common internal unit to be used for calculating
greenhouse gas emissions given another set of emission factors) look like:

::

    {
      "anthraciteCoal": {
        "mmbtu": 0.03985651654045436,
        "shortTon": 1.0
      },
      "bituminousCoal": {
        "mmbtu": 0.04011231448054553,
        "shortTon": 1.0
      },

so the access of the value is heat_content_factors[fuel_type][units].

Why wrap the factors jsons in python classes? For mobile sources it was required as handling the year of a vehicle
required logic that should not exist in the formula, as the formula scripts should be able to hand off user input to
factors and get values with no overhead. The remaining factors classes are trivial wrappers for now, however in the
future as the SGEC tool expands to other non-US markets these classes may have to do unit conversions or implement
other logic as the user input for these markets will differ given their record keeping of emissions sources.

The factors are located in atom6-ghg/atom6ghg/factors and the scraped json files are located in
atom6-ghg/atom6ghg/factors/source_data.

Factors Data
************


Unit Conversion Factors
~~~~~~~~~~~~~~~~~~~~~~~

Unit conversion factors allow for conversions of limited sets of units for volume, energy, mass weight, and distance.
These factors are also overloaded, as they contain some metric unit prefixes and their multiplicative factors (e.g.,
"Kilo": 1000) as well as the molecular weights of C and CO2.

The syntax for unit conversion factors is unit_conversion_factors[unit_converting_from][unit_converting_to]. For each unit the
identity conversion is there as well.

Example:
::

    "pounds": {
      "gram": 453.6,
      "pounds": 1.0,
      "kilogram": 0.4536,
      "metricTon": 0.0004536,
      "shortTon": 0.0005
    },

All of the unit conversion factors were scraped from the Unit Conversions sheet in the EPA's SGEC workbook.

Heat Content Factors
~~~~~~~~~~~~~~~~~~~~~~~

Heat content factors generally allow for conversion of heat energy into volumes or masses, for different stationary
combustion fuel sources.

The syntax for heat content factors is heat_content_factors[fuel_type][unit_converting_from].

Example:
::

    {
      "anthraciteCoal": {
        "mmbtu": 0.03985651654045436,
        "shortTon": 1.0
      },

All of the heat content factors were scraped from the Heat Content sheet in the EPA's SGEC workbook.

Stationary Combustion Emission Factors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Stationary combustion emission factors have CO2, CH4 and N2O factors for stationary combustion fuel sources.

The syntax for stationary combustion emission factors is
stationary_combustion_emission_factors[fuel_type][emission_gas_conversion_key]. The emission_gas_conversion_key
contains information about the greenhouse gas as well as the units associated with the factor (see below example).
These keys will likely change (see :ref:`refactoring`)

Example:
::

    "naturalGas": {
      "CO2 Factor (kg / mmBtu)": 53.06,
      "CH4 Factor (g / mmBtu)": 1.0,
      "N2O Factor (g / mmBtu)": 0.1,
      "CO2 Factor (kg / Unit)": 0.05444,
      "CH4 Factor (g / unit)": 0.00103,
      "N2O Factor (g / unit)": 0.0001,
      "Unit": "scf"
    },

All of the stationary combustion emission factors were scraped from the Stationary Combustion Emission Factors (Used for Steam and
Stationary Combustion) table on the Emission Factors sheet in the EPA's SGEC workbook.

Mobile Combustion CO2 Emission Factors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Mobile combustion CO2 emission factors have CO2 emission factors for mobile combustion fuel sources.

The syntax for mobile combustion CO2 emission factors is mobile_combustion_co2_emission_factors[fuel_type]. The factors
are in units of kg / unit, where unit is the internal unit associated with the mobile combustion fuel source (which is
gallons for all except scf for compressed natural gas (CNG)).

Example:
::

  "gasoline": 8.78,

All of the mobile combustion CO2 emission factors were scraped from the CO2 Emissions for Road Vehicles table on the
Emission Factors sheet in the EPA's SGEC workbook.

Mobile Combustion CH4 and N2O Emission Factors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Mobile combustion CH4 and N2O emission factors have CH4 and N2O emission factors for vehicle type, mobile combustion
fuel source and year combinations.

The syntax for mobile combustion CH4 and N2O emission factors is
mobile_combustion_ch4_and_n2o_emission_factors[vehicle_type][fuel_type][year][key], where key is either "ch4_factor",
"n2o_factor", or "year_display". "ch4_factor" and "n2o_factor" yield the CH4 and N2O emission factors for the
vehicle_type/fuel_type/year combination in units of g / unit, where unit is the internal unit associated with the mobile
combustion fuel source (which is gallons for all except scf for compressed natural gas (CNG)).

"year_display" yields the year or range of years (as "begin-end") associated with an input year. Ranges of years occur
when the emission factors were constant for that range. Many vehicle_type/fuel_type combinations' CH4 and N2O emission
factors do not depend on time. In those cases the year associated with the emission factors is "default" and the value
for their "year_display" is "".

The python class that wraps mobile combustion CH4 and N2O emission factors contains logic that handles year inputs for
all vehicle_type/fuel_type combinations (essentially ignoring the year input if the combination's emission factors do
not depend on year).

Example, year dependent emission factors:
::

    {
      "heavyDutyVehicles": {
        "gasoline": {
          "1985": {
            "ch4_factor": 0.409,
            "n2o_factor": 0.0515,
            "year_display": "1985-1986"
          },
          "1986": {
            "ch4_factor": 0.409,
            "n2o_factor": 0.0515,
            "year_display": "1985-1986"
          },
          "1987": {
            "ch4_factor": 0.3675,
            "n2o_factor": 0.0849,
            "year_display": "1987"
          },

Example, year independent emission factors:

::

  "loggingEquipment": {
    "gasoline2Stroke": {
      "default": {
        "ch4_factor": 12.03,
        "n2o_factor": 0.08,
        "year_display": ""
      }
    },

All of the mobile combustion CH4 and N2O emission factors were scraped from the CH4 and N2O Emissions for Highway
Vehicles, and CH4 and N2O Emissions for Non-Road Vehicles tables on the Emission Factors sheet in the EPA's SGEC
workbook.

Refrigerants GWP Factors
~~~~~~~~~~~~~~~~~~~~~~~~~

Refrigerants GWP factors have global warming potentials (GWPs) for greenhouse gases and blended refrigerants, relative
to CO2.

The syntax for refrigerants GWP factors is refrigerants_gwp_factors[gas].

Example:
::

    {
      "co2": 1,
      "ch4": 25,
      "n2o": 298,
      "hfc23": 14800,
      "hfc32": 675,

All of the refrigerants GWP factors were scraped from the Refrigerants and Global Warming
Potentials (GWPs) tables (one for gas and the one below for blended refrigerants) on the Emission Factors sheet in the
EPA's SGEC workbook.

.. _refrigeration-equipment-factors:

Refrigeration and AC Equipment Emission Factors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Refrigeration and AC equipment emission factors have emission factors for refrigeration and AC systems, specifically
for charging, annual loss, recovery efficiency and remaining refrigerant (at end-of-life). These factors are used for
Refrigeration and AC emissions in the Screening Method (the other accounting methods in Refrigeration and AC emissions
do not use equipment level data).

The syntax for refrigeration and AC equipment emission factors is
refrigeration_and_ac_equipment_emission_factors[equipment_type][factor_key], where factor_key is one of the following
in the example below.

Example:
::

  "carAcUnits": {
    "installationEmissionFactor": 0.005,
    "operatingEmissionFactor": 0.2,
    "refrigerantRemainingAtDisposal": 0.5,
    "recoveryEfficiency": 0.5
  },

All of the refrigeration and AC equipment emission factors were manually acquired from equations in the Formula
Selection for Type of Equipment table on the Refrigeration and AC sheet in the EPA's SGEC workbook. All of these
factors are originally sourced from [IPCC2019V3CH7]_.

.. [IPCC2019V3CH7] IPCC, 2019: 2019 Refinement to the 2006 IPCC Guidelines for National Greenhouse Gas Inventories,
    Volume 3: Industrial Processes and Product Use, Chapter 7: Emissions of Fluorinated Substitutes for Ozone Depleting
    Substances, pp. 32, TABLE 7.9 (UPDATED) DEFAULT ESTIMATES FOR CHARGE, LIFETIME AND EMISSION FACTORS FOR
    REFRIGERATION AND AIR-CONDITIONING SYSTEMS

Fire Suppression Leak Rates Factors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fire suppression leak rates factors have leak rates for fixed and portable fire suppression systems.

The entirety of the factors is below:
::

    {
      "fixed": 0.035,
      "portable": 0.025
    }

These factors were scraped from the Fire Suppressant Leak Rates table on the Emission Factors sheet in the
EPA's SGEC workbook. Note, these factors differ from another set used in the EPA's SGEC workbook. See
:ref:`certification-note`.

Molecular Weights Factors
~~~~~~~~~~~~~~~~~~~~~~~~~~

Molecular weights factors have molecular weights, and fractions of carbon for a set of hydrocarbons, specifically the
set of gases used in the Waste Gases formula.

The syntax for molecular weights factors is molecular_weights_factors[gas][key], where key is one of "molecularWeight",
"percentCarbon", or "chemicalFormula".

Example:
::

  "Carbon Monoxide": {
    "molecularWeight": 28.010399999999997,
    "percentCarbon": 0.42880501528003884,
    "chemicalFormula": "co"
  },

All of the molecular weights factors were scraped from the Determining Emission Factor for Gas Waste Stream table on the
Waste Gases sheet in the EPA's SGEC workbook.

Electricity Emission Factors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Electricity emission factors have CO2, CH4, and N2O emissions factors for eGRID subregions of the U.S.

The syntax for electricity emission factors is electricity_emission_factors[subregion][gas], where gas is one of the big
3 greenhouse gases "co2", "ch4", or "n2o".

Example:
::

  "akgd": {
    "co2": 1114.4,
    "ch4": 0.098,
    "n2o": 0.013
  },

All of the electricity emission factors were scraped from the Electricity Emission Factors (System Average) table on the
Emission Factors sheet in the EPA's SGEC workbook.

Business Travel Factors
~~~~~~~~~~~~~~~~~~~~~~~~

Business travel factors have CO2, CH4, and N2O emissions factors for vehicles.

The syntax for business travel factors is business_travel_factors[vehicle_type][key], where key is one of the big
3 greenhouse gases "co2", "ch4", or "n2o" as well as "units". The factors are in units of kg / mile for CO2 emissions
and g / mile for CH4 and N2O emissions.

Example:
::

  "passengerCars": {
    "co2": 0.341,
    "ch4": 0.009,
    "n2o": 0.008,
    "units": "vehicle-mile"
  },

All of the business travel factors were scraped from the Business Travel and Employee Commuting Emission Factors table
on the Emission Factors sheet in the EPA's SGEC workbook.

Product Transport Factors
~~~~~~~~~~~~~~~~~~~~~~~~~~

Product transport factors have CO2, CH4, and N2O emissions factors for vehicles.

The syntax for product transport factors is product_transport_factors[vehicle_type][units][gas], where "units" is the
unit associated with the transport method, either "vehicle-mile", or "ton-mile". Some vehicles only allow for one of the
two units. The gas one of the big 3 greenhouse gases "co2", "ch4", or "n2o". The factors are in units of kg / unit for
CO2 emissions and g / unit for CH4 and N2O emissions.

Example:
::

  "mediumAndHeavyDutyTruck": {
    "vehicle-mile": {
      "co2": 1.407,
      "ch4": 0.013,
      "n2o": 0.033
    },
    "ton-mile": {
      "co2": 0.211,
      "ch4": 0.002,
      "n2o": 0.0049
    }
  },

All of the product transport factors were scraped from the Product Transport Emission Factors table
on the Emission Factors sheet in the EPA's SGEC workbook.

Waste Emission Factors
~~~~~~~~~~~~~~~~~~~~~~~~

Waste emission factors have CO2 emissions factors for different waste material and disposal method combinations.

The syntax for waste emission factors is waste_emission_factors[waste_type][disposal_method], where disposal_method is
one of either "recycled", "landfilled", or "combusted". The factors are in units of metric tons CO2 / short ton.

Example:
::

  "aluminumCans": {
    "recycled": 0.06,
    "landfilled": 0.02,
    "combusted": 0.01
  },

All of the waste emission factors were scraped from the Waste Emission Factors table on the Emission Factors sheet in
the EPA's SGEC workbook.

Use in Formulas
***************

Here is the relationship between factors and what formulas they are used in:

===============================================  ===================================================================================================================================================================
Factor                                           Formulas
===============================================  ===================================================================================================================================================================
Unit Conversion Factors                          Refrigeration and AC, Fire Suppression, Purchased Gases, Waste Gases, Electricity, Waste
Heat Content Factors                             Stationary Combustion
Stationary Combustion Emission Factors           Stationary Combustion, Steam
Mobile Combustion CO2 Emission Factors           Mobile Sources
Mobile Combustion CH4 and N2O Emission Factors   Mobile Sources
Refrigerants GWP Factors                         Stationary Combustion, Mobile Sources, Refrigeration and AC, Fire Suppression, Purchased Gases, Electricity, Steam, Business Travel, Commuting, Product Transport
Refrigeration and AC Equipment Emission Factors  Refrigeration and AC
Fire Suppression Leak Rates Factors              Fire Suppression
Molecular Weights Factors                        Waste Gases
Electricity Emission Factors                     Electricity
Business Travel Factors                          Business Travel, Commuting
Product Transport Factors                        Product Transport
Waste Emission Factors                           Waste
===============================================  ===================================================================================================================================================================
