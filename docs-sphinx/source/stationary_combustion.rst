
.. _stationary-combustion-api:

Stationary Combustion
---------------------
Stationary Combustion is a `Scope 1 Emission <glossary.html>`_ that includes, but is not limited to,
`boilers <glossary.html>`_, `simple and combined-cycle combustion turbines <glossary.html>`_,
`engines <glossary.html>`_, `incinerators <glossary.html>`_, and `process heaters <glossary.html>`_. Stationary fuel
combustion sources are devices that combust solid, liquid, or gaseous fuel, generally for the purposes of producing
energy, generating steam, providing useful heat or energy for industrial, commercial or institutional use, or reducing
the volume of waste by removing combustible matter.

Usage
**********
.. module:: atomic6ghg.formulas.stationary_combustion

.. autoclass:: StationaryCombustion
    :members:
    :undoc-members:
    :inherited-members:

.. code-block:: python

    from atomic6ghg.formulas import StationaryCombustion

    input_data = {
      "version": "stationary-combustion.1.0.0",
      "stationarySourceFuelConsumption": [
        {
          "sourceId": "BLR-014",
          "sourceDescription": "West Power Plant",
          "sourceArea": 10517,
          "fuelCombusted": "anthraciteCoal",
          "quantityCombusted": 100,
          "units": "mmbtu"
        }
      ]
    }

    calculated_data = StationaryCombustion(input_data).to_dict()

    print(calculated_data['totalCo2EquivalentEmissions'])
    print(calculated_data['totalBiomassEquivalentEmissions'])


EPA Equation Analysis
**************************************************
Stationary combustion allows for inputs of combusted quantities for the following sources with units, which are
converted into an internal atomic6 unit:

.. csv-table::
   :file: ./stationary_combustion.csv
   :header-rows: 1

The fundamental calculation for each source are their :math:`\text{CO}_2`, :math:`\text{CH}_4`, and
:math:`\text{N}_2\text{O}` emissions associated with the quantity combusted. The formula is:

.. math::

   Emissions_{GHG,\, fuel} = Fuel\; Consumption_{fuel} \cdot Emission\; Factor_{GHG,\, fuel}

This is Equation 2.1 from [IPCC2006V2CH2]_. Note, in atomic6, the :math:`Fuel\; Consumption_{fuel}` is actually composed
of two terms:

.. math::

   Fuel\; Consumption_{fuel} = User\; Input\; Fuel\; Consumption_{fuel,\, fuel\: units} \cdot Unit\; Conversion\; Factor_{fuel\: units}

where :math:`Unit\; Conversion\; Factor_{fuel\; units}` converts the :math:`fuel\; units` into the standardized
internal atomic6 unit for :math:`Fuel\; Consumption_{fuel}`, which varies depending on the stationary combustion source
(see above table). This is necessary, since :math:`Emission\; Factor_{GHG,\; fuel}` is only available in limited sets
of units, but we want to allow for a wide range of input units for :math:`fuel\; units` to minimize unit conversion
being done by the user from the system they use for record keeping.

For stationary combustion, the :math:`Total \text{CO}_2\; Equivalent\; Emissions_{GHG,\, fuel}` and
:math:`Total\; Biomass\; \text{CO}_2\; Equivalent\; Emissions_{GHG}` in metric tons are calculated. The formulas are:

.. math::

    Total\; \text{CO}_2\; Equivalent\; Emissions_{GHG,\, fuel} = \sum_{n=1}^{\infty} Emissions_{GHG,\, fuel, n} \cdot EF_{GHG}


where :math:`Total\; \text{CO}_2\; Equivalent\; Emissions_{GHG, fuel}` is the sum of all :math:`GHG` emissions by
each source (fossil fuel or non fossil fuel), :math:`Emissions_{GHG,\, fuel}` are emissions of any :math:`GHG`
(fossil fuel or non fossil fuel :math:`\text{CO}_2`, :math:`\text{CH}_4`, and :math:`\text{N}_2\text{O}`),
and :math:`EF_{GHG}` is the emission factor for that :math:`GHG` to convert it into :math:`\text{CO}_2\;`.
Note that in atomic6, those emissions with units of grams are converted into kilograms, then the final value of this
calculation is divided by :math:`1000` to convert this value into :math:`metric \; tons`.

.. math::

    Total\; Biomass\; \text{CO}_2\; Equivalent\; Emissions_{fuel} = \sum_{n=1}^{\infty} Non\; Fossil\; Fuel\; \text{CO}_2\; Emissions_{fuel, n}

These equations are outlined in Equation 2.2 from [IPCC2006V2CH2]_.

where :math:`Total\; Biomass\; \text{CO}_2\; Equivalent\; Emissions_{fuel}` is the sum of
:math:`Non\; Fossil\; Fuel\; \text{CO}_2\; Emissions_{fuel, n}`, which only accounts for the GHG :math:`\text{CO}_2`.
Note that in atomic6 the final value of this calculation is converted into :math:`metric \; tons`.

.. [IPCC2006V2CH2] `IPCC, 2006: 2006 IPCC Guidelines for National Greenhouse Gas Inventories, Volume 2, Energy, Chapter 2, Stationary Combustion, pp. 11 <https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/2_Volume2/V2_2_Ch2_Stationary_Combustion.pdf>`_
