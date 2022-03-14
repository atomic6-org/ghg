.. _sgec-certification:

Certification
-------------

To certify all calculations, values were entered directly into the EPA's SGEC workbook covering
as wide an input space as possible. These input values together with the aggregated totals and emissions values
calculated by the EPA's SGEC workbook are referred to as canonical values in our documentation.
Python scripts were written leveraging the Pandas library to scrape the canonical values from each of the 13 sheets
listed above. The scraped user input canonical values were then used as inputs to the calculator scripts for each
page, and all atom6 calculated values were compared for equality (within floating point error) to all canonical
calculated values, from intermediate emissions values on up through the total CO2 equivalent.

All scope 1,2 and 3 scrapers are located in atom6-ghg/tools. The scraper for all factors is also located in
atom6-ghg/tools.

The tests certifying each calculator page in atom6 are located in atom6-ghg/tests, and all have the suffix ``_formula``,
e.g., the test certifying the stationary combustion page is named ``test_stationary_combustion_formula.py``.

.. _certification-note:

Note
****

In the Source Level Fire Suppression Gas CO2 Equivalent Emissions - Screening Method table on the Fire Suppression page
in the the EPA's SGEC workbook, there iss an inconsistency in the way that CO2 Equivalent Emissions (kg) is calculated.
The example row and the first row of the table have formulas for CO2 Equivalent Emissions that use factors from the
Fire Suppressant Leak Rates table on the Emission Factors sheet, while the remaining rows' formulas have hard coded
factors that do not agree with the factors in the table. We could not find these hard coded values in reference
literature, while the factors in the Fire Suppressant Leak Rates table were pulled from EPA (2020) Inventory of U.S.
Greenhouse Gas Emissions and Sinks: 1990-2018. Page A-285. We decided to change the remaining cells to match the formula
from the first two, and reference the factors that were backed by the literature.
