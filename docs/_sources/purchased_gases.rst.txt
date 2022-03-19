.. _purchased-gases-api:

Purchased Gases
---------------
Purchased gases calculates the carbon content (or emission factor) for some complex purchased gas streams. These complex gas streams include:

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

