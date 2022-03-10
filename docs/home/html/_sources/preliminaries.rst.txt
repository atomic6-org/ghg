Things to do next:
==================

Other Applications
------------------

    * Additional scope 1 emissions
        * EPA SGEC does not have explicit emissions calculators for the following industries that have emissions
          methodologies developed by the IPCC in Volume 3, Industrial Processes Product Use:
            * Mineral Industry https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/3_Volume3/V3_2_Ch2_Mineral_Industry.pdf
            * Chemical Industry https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/3_Volume3/V3_3_Ch3_Chemical_Industry.pdf
            * Metal Industry https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/3_Volume3/V3_4_Ch4_Metal_Industry.pdf
            * Electronics Industry https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/3_Volume3/V3_6_Ch6_Electronics_Industry.pdf
        * There are also additional chapters in Volume 3 associated with other sources of emissions in industry.

    * are there international/metric variations we can support?
        * EPA SGEC seems to be using the global warming potential (GWP) values from AR4 (IPCC's Fourth Assessment Report)
          from 2007. The GHG Protocol calculator tool gives the option for using the AR4 or AR5 (IPCC's Fifth Assessment
          Report) from 2014. AR6 (IPCC's Sixth Assessment Report) came out in 2021
          (https://www.ipcc.ch/report/ar6/wg1/#FullReport) and has the most up to date GWP factors for greenhouse
          gases/refrigerants in the chapter 7 supplementary material:
          https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter_07_Supplementary_Material.pdf
          Incorporating these values would put the library at the forefront of current climate science and may
          make the library more attractive to businesses involved in markets with mandatory reporting (as the regulatory
          agencies may demand more up to date emissions estimates).
          Note: the GWP factors used in computing CO2 equivalent emissions are the 100 year values (column header GWP
          100). This is true in both EPA's SGEC and GHG Protocol's GHG Emissions Calculation Tool.

        * There may be a caveat to the above change to factors. It may be the case that factors and/or equations to be
          used for carbon accounting are enshrined in law for different countries. For example, see: https://www.ecfr.gov/current/title-40/part-98/subpart-C

        * The EU (including UK) seem to have different emissions standards for vehicles. In the EU, vehicles are classified
          into Stages depending on the motor power and other variables. The stages were introduced over time and set
          upper limits to CO2, NO_x, and HC (hydrocarbons) emissions per quantity fuel combusted. Note NO2 is contained in
          NO_x and CH4 is contained in HC. See https://en.wikipedia.org/wiki/European_emission_standards. It is unclear if
          the UK will change emissions standards after Brexit.

    * How are Scope 2 emissions handled in non-US markets (GHG is US electricity market only)?
        * Both Canada and Australia have regional market based emissions factors. Values can be found in the Greenhouse
          Gas Protocol's emissions calculator tool: https://ghgprotocol.org/sites/default/files/GHG%20Emissions%20Calculation%20Tool_0.xlsx
          under the Emissions Factor sheet, along with China.
          This document has values and sources for emissions factors beyond what is in the GHG Protocol's tool:
          https://www.carbonfootprint.com/docs/2020_07_emissions_factors_sources_for_2020_electricity_v1_3.pdf
          This document does not have CH4 and N2O emissions factors, only CO2.

    * make a list of US specific calculations that must be replaced in other countries
        * I do not believe there are US specific calculations. Accounting methodologies and their associated formulas
          are outlined by the IPCC. What changes are the emissions factors by market.

        * what are the sector specific calculations?

    * enable flexibility in identifying units of input values and returned values

    * review GHG with Greenville SME reconcile with an actual report
        * is there somewhere else in GE where scopes 2 and 3 are featured more significantly? Also, data for mobile
          sources and gas/refrigerant scope 1? (Greenville SME only provided data for stationary combustion)

.. _refactoring:

Refactoring
-----------

    * As a general principle, we should take as much pre-computing out of the hands of the user as possible. (Should the
      library support a "turbotax" like app for carbon accounting?)
        * In mobile sources, if the fuel usage associated with a vehicle is not known, but the mileage is then the EPA's
          SGEC directs the user to calculate the fuel usage based on a reference chart of approximate fuel efficiencies
          per vehicle. This can be done by the library. (I'm not sure if the simplified material balance is doing this
          already, but the language used to discuss the inputs across the two tables is different).
        * On the Refrigeration and AC page the material balance method gives instructions on how to calculate input
          fields to the table. Those could be the inputs to a more granular method, which then leverages the current
          method for calculation.

    * Change stationary_combustion_emission_factors to only take greenhouse gas as key and eliminate dual internal unit
      dependence. Currently, the stationary combustion page and the steam page both use
      stationary_combustion_emission_factors, and calculate emissions for nearly the same set of fuel types. However,
      the internal units that each convert to are different for each fuel type. E.g., anthraciteCoal has an internal
      unit of short tons on the stationary combustion page and mmBtu on the steam page. However, the user may enter in
      anthraciteCoal fuel combusted in units of mmbtu on the stationary combustion page (which are converted to short
      tons using heat content factors), and then uses the "CO2 Factor (kg / Unit)" key to get CO2 emissions for the
      short ton converted value. The steam page only allows for steam purchased in mmbtu, and then the CO2 emissions
      factors are retrieved using the "CO2 Factor (kg / mmBtu)" key in stationary_combustion_emission_factors. This is
      flawed design - there should only be one internal unit that the greenhouse gas factors are associated with
      (e.g., mmbtu ) for each fuel type and all input values' units should be converted to that one internal unit before
      calculating GHG emissions instead of maintaining multiple sets of GHG factors.

    * GWP factors for blended refrigerants are not accurate. If the blended refrigerant contains any HFC gas that has
      been phased out in the US due to EPA regulation, then that gas' GWP contribution to the blend is set to 0.
      Therefore every blended refrigerant with this property has a GWP which is less (sometimes absurdly so) than its
      actual value. E.g., R-409A is a blend of 60% HCFC-22, 25% HCFC-124, and 15% HCFC-142b, all three of which have
      been phased out in the US, yet its GWP is 0. This seems highly problematic, especially for markets outside the US
      where these refrigerants may still be in use.

    * Make references to CO2, CH4, and N2O keys in factors consistent across all. Some factors have lowercase while
      others have upper, e.g., "co2" vs "CO2".

    * make_molecular_weights in create_conversion_constants.py could be refactored as it opens one page multiple times
      (may not be necessary as this is likely an approximately one time use function)

    * Standardize emissions calculations for CO2, CH4 and N2O in formulas (staticmethods) into one equation that takes
      the gas as an argument (which then will be passed on to the factors to get the corresponding emission factor for
      the gas) for those formulae that calculate CH4 and N2O in addition to CO2.

Doc
---
  * Sphinx/RestructuredText API docs. Build in the lib repo. Dev audience
  * Concept doc. Build as a volume in ECM docs. Data Science/SME audience.
  * Should we unify notation for equations throughout the documentation? Notation for equations varies between the IPCC
    and the EPA as well as internally for each. Or should we source formulas with the exact same notation as what is in
    the reference document?

OSS Prep
--------
  * GE licensing friction
  * Move to public Github, PyPi, readthedocs.io


