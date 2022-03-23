.. _purchased-gases-api:

Purchased Gases
---------------
Purchased Gases is a `scope 1 emission <glossary.html>`_ that accounts for `purchased gas stream <glossary.html>`_.
Industrial gases are sometimes used in processes such as manufacturing, testing, or laboratory uses.  For example, CO2
gas is often used in welding operations.  These gases are typically released to the atmosphere after use.  Any releases
of the seven major greenhouse gases (CO2, CH4, N2O, PFCs, HFCs, SF6, and NF3) must be included in the GHG inventory.
Ozone depleting substances, such as CFCs and HCFCs, are regulated internationally and are typically excluded from a GHG
inventory or reported as a memo item.

Usage
**********
.. module:: atomic6ghg.formulas.purchased_gases

.. autoclass:: PurchasedGases
   :members:
   :undoc-members:
   :inherited-members:

.. code-block:: python

    from atomic6ghg.formulas import PurchasedGases

    input_data = json.load(
    """
    {
      "version": "purchased-gases.1.0.0",
      "purchasedGases": [
        {
          "gas": "ch4",
          "gasGWP": 25,
          "purchasedAmount": 300,
          "co2EquivalentEmissions": 7500
        },
        {
          "gas": "ch4",
          "gasGWP": 25,
          "purchasedAmount": 400,
          "co2EquivalentEmissions": 10000
        },
        {
          "gas": "nf3",
          "gasGWP": 17200,
          "purchasedAmount": 30,
          "co2EquivalentEmissions": 516000
        },
        {
          "gas": "hfc134a",
          "gasGWP": 1430,
          "purchasedAmount": 50,
          "co2EquivalentEmissions": 71500
        },
        {
          "gas": "c2f6",
          "gasGWP": 12200,
          "purchasedAmount": 70,
          "co2EquivalentEmissions": 854000
        },
        {
          "gas": "c6f14",
          "gasGWP": 9300,
          "purchasedAmount": 1123,
          "co2EquivalentEmissions": 10443900
        },
        {
          "gas": "r422a",
          "gasGWP": 3143,
          "purchasedAmount": 595,
          "co2EquivalentEmissions": 1870085
        },
        {
          "gas": "hfc125",
          "gasGWP": 3500,
          "purchasedAmount": 582,
          "co2EquivalentEmissions": 2037000
        },
        {
          "gas": "r502",
          "gasGWP": 0,
          "purchasedAmount": 182,
          "co2EquivalentEmissions": 0
        },
        {
          "gas": "r401b",
          "gasGWP": 14,
          "purchasedAmount": 56,
          "co2EquivalentEmissions": 784
        },
        {
          "gas": "r422d",
          "gasGWP": 2729,
          "purchasedAmount": 19,
          "co2EquivalentEmissions": 51851
        }
      ],
      "totalCo2EquivalentEmissions": 7195.284432
    }
    """
    )

    calculated_data = PurchasedGases.to_dict(input_data)

    calculated_data['totalCo2EquivalentEmissions']

**Parameters:**
    * **input_data** - (dict) input data that follows the JSON schema

EPA Equation Analysis
**************************************************
Purchased gases calculates the carbon content (or emission factor) for some complex purchased gas streams.


These complex gas streams include:

.. csv-table::
    :file: ./purchased_gases.csv
    :header-rows: 1

The fundamental calculations for each purchased gas Component are their

.. math::
   \text{CO}_2\; Equivalent\; Emissions_{gas} = GWP_{gas} * Purchased Amount_{gas}

These equations are derived from Equation 4 from [EPA2016DirectEmissionsfromStationaryCombustionSources]_.

where :math:`\text{CO}_2\; Equivalent\; Emissions_{gas}` is the total CO2 equivalent in merit unit pounds, :math:`GWP_{gas}`
is the global warming potential for that gas.


For purchased gases, the :math:`\text{CO}_2\; Equivalent\; Emissions_{gas}` in metric tons is calculated.
The formula is:


.. math::

    \text{CO}_2\; Equivalent\; Emissions_{gas} = \sum_{n=1}^{\infty} \text{CO}_2\; Equivalent\; Emissions_{gas}

This equation is derived from [EPA2016DirectEmissionsfromStationaryCombustionSources]_.

where :math:`gas` is the purchased gas.
Note that in atomic6 the final value of this calculation is multiplied by :math:`kilogram\; per\; pound` to convert this
value from :math:`lbs` to :math:`kilograms` then divided by :math:`1000` to convert this value into
:math:`metric \; tons`.


.. [EPA2016DirectEmissionsfromStationaryCombustionSources] EPA, 2016: 2016 EPA Greenhouse Gas Inventory Guidance, Direct Emissions from Stationary Combustion Sources, pp. 11

