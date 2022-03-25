.. _steam-api:

Steam
------
Steam is a `Scope 2 Emission <glossary.html>`_ that accounts for emissions from purchased steam.

Usage
*****
.. module:: atomic6ghg.formulas.steam

.. autoclass:: Steam
    :members:
    :undoc-members:
    :inherited-members:

Example Usage
******************
Python example code usage:

.. code-block:: python

    from atomic6ghg.formulas import Steam
    steam_input: dict = {
      "version": "steam.1.0.0",
      "emissionFactorDataForSteamPurchased": [
        {
          "sourceId": "BLR-012",
          "sourceDescription": "Steam Generator",
          "sourceArea": 15000,
          "fuelType": "coalCoke",
          "boilerEfficiency": 80,
          "steamPurchased": 10000,
          "locationBasedEmissionFactorsCO2Factor": 0,
          "locationBasedEmissionFactorsCH4Factor": 0,
          "locationBasedEmissionFactorsN2OFactor": 0,
          "marketBasedEmissionFactorsCO2Factor": 0,
          "marketBasedEmissionFactorsCH4Factor": 0,
          "marketBasedEmissionFactorsN2OFactor": 0
        }
      ]
    }
    engine = Steam(steam_input)
    outputs: dict = engine.to_dict()
    print(outputs.get('CO2EquivalentEmissionsLocationBasedElectricityEmissions'))


EPA Equation Analysis
*********************
Steam allows for inputs of purchased steam quantities for the following fuel types with units of MMBtu:

.. csv-table::
    :file: ./steam.csv
    :header-rows: 1


The fundamental calculation for each fuel type are their :math:`Location\; Based\; \text{CO}_2`,
:math:`Location\; Based\; \text{CH}_4`, :math:`Location\; Based\; \text{N}_2\text{O}` emissions and their
:math:`Market\; Based\; \text{CO}_2`, :math:`Market\; Based\; \text{CH}_4`, :math:`Market\; Based\; \text{N}_2\text{O}`
emissions associated with the steam purchased and based on boiler efficiency.
The formulas are:

.. math::

   Location\; Based\; Emissions_{GHG,\, fuel} = \frac{Steam\; Purchased_{fuel} \cdot Location\; Based\; Emission\; Factor_{GHG,\, fuel}}{Boiler\; Efficiency}

.. math::

    Market\; Based\; Emissions_{GHG,\, fuel} = \frac{Steam\; Purchased_{fuel} \cdot Market\; Based\; Emission\; Factor_{GHG,\, fuel}}{Boiler\; Efficiency}


This equation is derived from Equation 2.1 from [IPCC2006_V2CH2]_ (see Stationary Combustion), with accounting for :math:`Boiler\; Efficiency`.

where the default :math:`Boiler\; Efficiency` value is 80% if no :math:`Boiler\; Efficiency` value is input by the user,
the default :math:`Location\; Based\; Emission\; Factor_{GHG,\, fuel}` value is the emission factor for that fuel
type if no :math:`Location\; Based\; Emission\; Factor_{GHG,\, fuel}` value is input by the user,
and the default :math:`Market\; Based\; Emission\; Factor_{GHG,\, fuel}` value is the
:math:`Location\; Based\; Emission\; Factor_{GHG,\, fuel}` if no :math:`Market\; Based\; Emission\; Factor_{GHG,\, fuel}`
value is input by the user.

For steam, the :math:`\text{CO}_2\; Equivalent\; Emissions_{method}` in metric tons is calculated based on the
Total\; Emissions\; for\; All\; Sources_{method, GHG}. The formula is:


.. math::

    \text{CO}_2\; Equivalent\; Emissions_{method, GHG} = \sum_{n=1}^{\infty} Total\; Emissions\; for\; All\; Sources_{method, GHG} \cdot GWP_{GHG}

This equation is derived from Equation 2.2 from [IPCC2006_V2CH2]_.

where :math:`Total\; Emissions\; for\; All\; Sources_{method, GHG}` are the sums of all the emissions for that
:math:`GHG` (:math:`\text{CO}_2\;`, :math:`\text{CH}_4`, or :math:`\text{N}_2\text{O}`) and :math:`method` (either
:math:`location\; based` or :math:`market\; based`), and :math:`GWP_{GHG}` is the global warming potential of that
:math:`GHG`.
Note that in atomic6 the final value of this calculation is divided by :math:`1000` to convert this value into
:math:`metric \; tons`.

.. [IPCC2006_V2CH2] `IPCC, 2006: 2006 IPCC Guidelines for National Greenhouse Gas Inventories, Volume 2: Energy, Chapter 2: Stationary Combustion <https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_2_Ch2_Stationary_Combustion.pdf>`_
