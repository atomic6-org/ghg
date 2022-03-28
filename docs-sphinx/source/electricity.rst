.. _electricity-api:

Electricity
------------
Electricity is a `Scope 2 Emission <glossary.html>`_ that includes the generation, transmission, and distribution of
electricity. Carbon dioxide and smaller amounts of methane and nitrous oxide are released during the combustion of fossil
fuels, such as coal, oil, and natural gas, to produce electricity.


Usage
******
.. module:: atomic6ghg.formulas.electricity

.. autoclass:: Electricity
    :members:
    :undoc-members:
    :inherited-members:

Python example code usage:

.. code-block:: python

    from atomic6ghg.formulas import Electricity
    electricity_input: dict = {
        "version": "electricity.1.0.0",
        "totalElectricityPurchased": [
            {"eGridSubregion": "akgd", "electricityPurchased": 250,
            "marketBasedEmissionFactorsCO2Emissions": 8.7,
            "marketBasedEmissionFactorsCH4Emissions": 8.7,
            "marketBasedEmissionFactorsN2OEmissions": 8.7}
        ]
    }
    engine = Electricity(electricity_input)
    outputs: dict = engine.to_dict()
    print(outputs.get('CO2EquivalentEmissionsLocationBasedElectricityEmissions'))
    print(outputs.get('CO2EquivalentEmissionsMarketBasedElectricityEmissions'))

EPA Equation Analysis
**********************

Electricity allows for inputs of purchased electricity quantities for the following eGrid subregions with units of kWh:

.. csv-table::
    :file: ./electricity.csv
    :header-rows: 1


The fundamental calculation for each eGrid subregion are their :math:`Market\; Based\; \text{CO}_2`,
:math:`Market\; Based\; \text{CH}_4`, :math:`Market\; Based\; \text{N}_2\text{O}` emissions and their
:math:`Location\; Based\; \text{CO}_2`, :math:`Location\; Based\; \text{CH}_4`,
:math:`Location\; Based\; \text{N}_2\text{O}` emissions associated with the electricity purchased.
The formulas are:


.. math::

    Market\; Based\; Emissions_{eGrid\, subregion,\, GHG} = Electricity\; Purchased_{eGrid\, subregion} \cdot Market\; Based\; Emission\; Factor_{eGrid\, subregion,\, GHG}

.. math::

    Location\; Based\; Emissions_{eGrid\, subregion,\, GHG} = Electricity\; Purchased_{eGrid\, subregion} \cdot Location\; Based\; Emission\; Factor_{eGrid\, subregion,\, GHG}


This equation is derived from Equation 1 from [EPA2020_p3]_.

where :math:`Electricity\; Purchased_{eGrid\, subregion}` is converted into watts, the default
:math:`Location\; Based\; Emission\; Factor_{eGrid\ subregion,\, GHG}` value is the emission factor for that
:math:`eGrid Subregion` and :math:`GHG` if no :math:`Location\; Based\; Emission\; Factor_{eGrid\ subregion,\, GHG}`
value is input by the user, and the default :math:`Market\; Based\; Emission\; Factor_{eGrid\ subregion,\, GHG}` value
is the :math:`Location\; Based\; Emission\; Factor_{eGrid\ subregion, GHG}` if no
:math:`Market\; Based\; Emission\; Factor_{eGrid\ subregion, GHG}` value is input by the user.

For electricity, the :math:`\text{CO}_2\; Equivalent\; Emissions_{method,\, GHG}` in metric tons is calculated based on the
:math:`Total\; Emissions\; for\; All\; Sources_{method, GHG}`. The formula is:


.. math::

    \text{CO}_2\; Equivalent\; Emissions_{method, GHG} = \sum_{n=1}^{\infty} Total\; Emissions\; for\; All\; Sources_{method, GHG} \cdot GWP_{GHG}

This equation is derived from Equation 1 from [EPA2020_p3]_.

where :math:`Total\; Emissions\; for\; All\; Sources_{method, GHG}` are the sums of all the emissions for that
:math:`GHG` (:math:`\text{CO}_2\;`, :math:`\text{CH}_4`, or :math:`\text{N}_2\text{O}`) and :math:`method` (either
:math:`location\; based` or :math:`market\; based`), and :math:`GWP_{GHG}` is the global warming potential of that
:math:`GHG`.
Note that in atomic6 the final value of this calculation is converted into :math:`metric \; tons`.

.. [EPA2020_p3] `EPA, 2020: 2020 EPA Greenhouse Gas Inventory Guidance, Indirect Emissions from Purchased Electricity, pp. 3 <https://www.epa.gov/sites/default/files/2020-12/documents/electricityemissions.pdf#page=6>`_
