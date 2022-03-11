Schemas
=======

Each of the 13 workbook sheets has an associated schema in the atom6 library. The schema for a page is a json document
which defines the structure of the data that the library receives as well as the structure of the data that the
library returns for that page, and corresponds with the structure of the page in the EPA's SGEC workbook. Under the top
level key "properties" are keys that correspond to different sections of the page. For example, the schema for the
Offsets page:

::

    {
      "$schema": "http://json-schema.org/schema#",
      "title": "purchasedOffsets",
      "description": "Document schema of Offsets workbook page in SGEC",
      "type": "object",
      "properties": {
        "version": {
          "type": "string",
          "pattern": "^purchased-offsets.1.0.0"
        },
        "h1Title": {
          "type": "string",
          "title": "Purchased Offsets"
        },
        "instruction": {
          "type": "string",
          "title": "Enter quantity of offsets purchased for each offset project in terms of CO2 equivalent. Enter offsets purchased for the inventory reporting period."
        },
        "purchasedOffsets": {
          "type": "array",
          "title": "Table 1. Total Amount of Purchased Offsets",
          "items": {
            "type": "object",
            "properties": {
              "projectId": {
                "title": "ID",
                "description": "Global warming potential of selected gas",
                "format": "s",
                "formula": "None",
                "type": "string"
              },
              "projectDescription": {
                "title": "Project Description",
                "description": "",
                "format": "s",
                "formula": "None",
                "type": "string"
              },
              "purchasedOffset": {
                "title": "Offsets Purchased (Metric Tons CO2e)",
                "description": "",
                "format": ",",
                "formula": "None",
                "type": [
                  "number",
                  "null"
                ]
              }
            },
            "required": [
              "purchasedOffset"
            ]
          }
        },
        "totalPurchasedOffsets,": {
          "title": "Total CO2 Equivalent Emission Reductions (metric tons) - Offsets",
          "formula": "atom6ghg.formulas.purchased_offsets.make_co2_equivalent_emissions",
          "type": ["number", "null"]
        },
        "footNote": {}
      },
      "required": [
        "version",
        "purchasedOffsets"
      ]
    }

which corresponds with the Offsets page in the EPA's SGEC workbook:

.. image:: ../../Images/atom6-schema-spec-example-full-page.jpg

The keys "h1Title", "instruction", "purchasedOffsets", "totalPurchasedOffsets" and "footnote" correspond with the page
title, page guidance, Total Amount Of Purchased Offsets user data entry table, Total CO2
Equivalent Emission Reductions (metric tons) - Offsets value and footnote, respectively.

The keys under the top level key "properties" that correspond with tables are of type "array", where each element of
the array corresponds with a row of the table. Under "items" -> "properties" are keys which correspond to the columns
of the table. In the example above, the keys "projectId", "projectDescription", and "purchasedOffset" correspond to the
columns "ID", "Project Description", and "Offsets Purchased (Metric Tons CO2e)", respectively. Note that the "title"
key under each of the column level keys is the title used for each column in the EPA's SGEC workbook.

If the table is one that has user input then the "required" key (parallel to "items" for the table) is an array of all
columns necessary for a calculation to occur and must be present in the data retunred form the UI for a given row, even
if they are null valued. Also, if a particular column of the table has a restricted set of values (indicated in the
EPA's SGEC workbook by a dropdown list), then the column level key has an "enum" key with an array of allowed values
for that column. For example, the "stationarySourceFuelConsumption" table's "fuelCombusted" column has a restricted set
of stationary fuel types that the formula code can compute for, and are enumerated in the schema:

::

    "fuelCombusted": {
      "title": "Fuel Combusted",
      "description": "Dropdown selection of type of fuel combusted",
      "format": "s",
      "formula": "None",
      "type": "string",
      "enum": ["", "anthraciteCoal", "bituminousCoal", "subBituminousCoal", "ligniteCoal", "naturalGas", "distillateFuelOilNo2", "residualFuelOilNo6", "kerosene", "liquefiedPetroleumGases", "woodAndWoodResiduals", "landfillGas"]

which corresponds with:

.. image:: ../../Images/atom6-schema-spec-example-enum.png

Note that the values are tokenized into camel case from the original values found in the EPA's SGEC workbook, and
this tokenization lookup from the original is in atom6-ghg/tools/__init__.py.

The only variation in the schema pattern described above exists for the Mobile Sources page's schema. The calculated
tables: "totalOrganizationWideOnRoadGasolineMobileSourceMileageAndEmissions",
"totalOrganizationWideOnRoadNonGasolineMobileSourceMileageAndEmissions" and
"totalOrganizationWideNonRoadMobileSourceFuelUsageAndEmissions" have one-to-many relations ships between the first or
first and second columns and the remainder of the columns in the table. Each of these tables has a column-level key
which does not correspond to a column explicitly, but instead contains all of the "many" columns under its own
"properties" key. For example, in "totalOrganizationWideOnRoadGasolineMobileSourceMileageAndEmissions":

::

    "totalOrganizationWideOnRoadGasolineMobileSourceMileageAndEmissions": {
        "type": "array",
        "title": "Total Organization-Wide On-Road Gasoline Mobile Source Mileage and CH4/N2O Emissions",
        "items": {
            "vehicleType": {
                "title": "Vehicle Type",
                "type": "object",
                "description": "Type of Vehicle",
                "format": "s",
                "formula": "atom6ghg.formulas.mobiles_sources.total_organization_wide_on_road_mileage_ch4_n2o_emissions"
            },
            "emissionByYear": {
                "type": "object",
                "properties": {
                    "vehicleYear": {
                        "title": "Vehicle Year",
                        "description": "Make year of the Vehicle",
                        "format": "s",
                        "formula": "None",
                        "type": "number"
                    },
                    "mileage": {
                        "title": "Mileage (miles)",
                        "description": "Calculated total mileage of the vehicle",
                        "format": ",",
                        "formula": "atom6ghg.formulas.mobile_sources.total_organization_wide_on_road_mileage",
                        "type": ["number", "null"]
                    },
                    "CH4": {
                        "title": "CH4 (g)",
                        "description": "Calculated quantity of CH4 combusted for given fuel type measured in grams",
                        "format": ":.1f",
                        "formula": "atom6ghg.formulas.mobile_sources.total_organization_wide_on_road_ch4",
                        "type": ["number", "null"]
                    },
                    "N2O": {
                        "title": "N2O (g)",
                        "description": "Calculated quantity of N2O combusted for given fuel type measured in grams",
                        "format": ":.1f",
                        "formula": "atom6ghg.formulas.mobile_sources.total_organization_wide_on_road_n2o",
                        "type": ["number", "null"]
                    }

the "emissionByYear" key does not explicitly correspond with a column in the UI, but corresponds with all the "many"
columns "vehicleYear", "mileage", "CH4", and "N2O".

This corresponds with the table structure in the EPA's SGEC workbook:

.. image:: ../../Images/atom6-schema-spec-example-one-to-many.jpg

The naming convention for schemas is <page>.json, where <page> is the page's name in snake case. All page schemas are
found in atom6-ghg/atom6ghg/schemas.

