.. _steam-api:

Steam
------
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


This equation is derived from Equation 2.1 from [IPCC2006V2CH2]_ (see Stationary Combustion), with accounting for :math:`Boiler\; Efficiency`.

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

This equation is derived from Equation 2.2 from [IPCC2006V2CH2]_.

where :math:`Total\; Emissions\; for\; All\; Sources_{method, GHG}` are the sums of all the emissions for that
:math:`GHG` (:math:`\text{CO}_2\;`, :math:`\text{CH}_4`, or :math:`\text{N}_2\text{O}`) and :math:`method` (either
:math:`location\; based` or :math:`market\; based`), and :math:`GWP_{GHG}` is the global warming potential of that
:math:`GHG`.
Note that in atomic6 the final value of this calculation is divided by :math:`1000` to convert this value into
:math:`metric \; tons`.
