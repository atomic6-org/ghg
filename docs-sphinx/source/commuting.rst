.. _commuting-api:

Commuting
---------
Commuting calculates emissions from transportation of employees to and from work. There are two different tables and
therefore two different methods to calculate emissions from employee commuting. The first is for those employees who
commute via of personal vehicle, the second is for those employees who commute via public transportation.

Commuting allows for inputs of personal vehicle types for the following vehicle types:

.. csv-table::
    :file: ./commuting_personal_vehicle.csv
    :header-rows: 1

Commuting allows for inputs of public transportation types for the following public transport types:

.. csv-table::
    :file: ./commuting_public_transportation.csv
    :header-rows: 1


The fundamental calculation for each vehicle type or public transport type for personal vehicle and public transport
commuting are their :math:`\text{CO}_2`, :math:`\text{CH}_4`, and :math:`\text{N}_2\text{O}` emissions associated
with the vehicle type and based on the vehicle miles traveled.

The formulas are:

.. math::

   Travel\; Emissions_{travel\, mode, T} = Travel_{travel\, mode} \cdot EF_{T}

This equation is derived from Equation 1 from [EPA2008OptionalEmissionsfromCommutingBusinessTravelandProductTransport]_.

where :math:`Travel\; Emissions_{travel\, mode, T}` is the mass of :math:`\text{CO}_2`, :math:`\text{CH}_4`,
or :math:`\text{N}_2\text{O}`4` emitted, :math:`Travel_{travel\, mode}` is the travel distance in miles for a
specific travel mode, which is either vehicle miles traveled or passenger miles traveled for personal vehicle
or public transportation respectively and :math:`EF_{T}` is the travel :math:`\text{CO}_2`, :math:`\text{CH}_4`,
or :math:`\text{N}_2\text{O}` emission factor which is based on the type of personal vehicle or public transport method.

For commuting, the :math:`\text{CO}_2\; Equivalent\; Emissions_{GHG, transport}` in metric tons is calculated.
The formula is:


.. math::

    \text{CO}_2\; Equivalent\; Emissions_{GHG, transport} = \sum_{n=1}^{\infty} Total\; Emissions_{GHG, transport} \cdot GWP_{GHG}

This equation is derived from [EPA2008OptionalEmissionsfromCommutingBusinessTravelandProductTransport]_.

where :math:`Total\; Emissions_{GHG, transport}` is the sum of all the emissions for that
:math:`GHG` (:math:`\text{CO}_2\;`, :math:`\text{CH}_4`, or :math:`\text{N}_2\text{O}`) and :math:`transport`
(either personal vehicle or public transport), and :math:`GWP_{GHG}` is the
global warming potential of that :math:`GHG`.
Note that in atomic6 the final value of this calculation is divided by :math:`1000` to convert this value into
:math:`metric \; tons`.
