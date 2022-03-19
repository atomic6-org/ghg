.. _electricity-api:

Electricity
------------
Electricity is a `Scope 2 Emission <glossary.html>`_


Usage
******
.. module:: atomic6ghg.formulas.electricity

.. autoclass:: Electricity
    :members:
    :undoc-members:
    :inherited-members:

EPA Equation Analysis
**********************

Electricity allows for inputs of purchased electricity quantities for the following eGrid subregions with units of kWh:

.. csv-table::
    :file: ./electricity.csv
    :header-rows: 1


The fundamental calculation for each eGrid subregion are their :math:`Market\; Based\; \text{CO}_2`,
:math:`Market\; Based\; \text{CH}_4`, :math:`Market\; Based\; \text{N}_2\text{O}` emissions and their
:math:`Location\; Based\; \text{CO}_2`, :math:`Location\; Based\; \text{CH}_4`,
:math:`Location\; Based\; \text{N}_2\te
xt{O}` emissions associated with the electricity purchased.
The formulas are:


.. math::

    Market\; Based\; Emissions_{electricity, eGrid\, subregion} = Electricity\; Purchased_{electricity} \cdot Market\; Based\; Emission\; Factor_{eGrid\, subregion}

.. math::

    Location\; Based\; Emissions_{electricity, eGrid\, subregion} = Electricity\; Purchased_{electricity} \cdot Location\; Based\; Emission\; Factor_{eGrid\, subregion}


This equation is derived from Equation 1 from [EPA2020IndirectEmissionsfromPurchasedElectricity]_.

where :math:`Electricity\; Purchased_{electricity}` is converted into watts, the default
:math:`Location\; Based\; Emission\; Factor_{eGrid\ subregion}` value is the emission factor for that
eGrid Subregion and fuel type if no :math:`Location\; Based\; Emission\; Factor_{eGrid\ subregion}` value is
input by the user, and the default :math:`Market\; Based\; Emission\; Factor_{eGrid\ subregion}` value is
the :math:`Location\; Based\; Emission\; Factor_{eGrid\ subregion}` if no
:math:`Market\; Based\; Emission\; Factor_{eGrid\ subregion}` value is input by the user.

For electricity, the :math:`\text{CO}_2\; Equivalent\; Emissions_{method}` in metric tons is calculated based on the
Total\; Emissions\; for\; All\; Sources_{method, GHG}. The formula is:


.. math::

    \text{CO}_2\; Equivalent\; Emissions_{method, GHG} = \sum_{n=1}^{\infty} Total\; Emissions\; for\; All\; Sources_{method, GHG} \cdot GWP_{GHG}

This equation is derived from Equation 2.2 from [EPA2020IndirectEmissionsfromPurchasedElectricity]_.

where :math:`Total\; Emissions\; for\; All\; Sources_{method, GHG}` are the sums of all the emissions for that
:math:`GHG` (:math:`\text{CO}_2\;`, :math:`\text{CH}_4`, or :math:`\text{N}_2\text{O}`) and :math:`method` (either
:math:`location\; based` or :math:`market\; based`), and :math:`GWP_{GHG}` is the global warming potential of that
:math:`GHG`.
Note that in atomic6 the final value of this calculation is divided by :math:`1000` to convert this value into
:math:`metric \; tons`.

.. [EPA2020IndirectEmissionsfromPurchasedElectricity] EPA, 2020: 2020 EPA Greenhouse Gas Inventory Guidance, Indirect Emissions from Purchased Electricity, pp. 3
