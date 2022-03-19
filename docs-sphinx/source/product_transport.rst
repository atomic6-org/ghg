
.. _product-transport-api:

Product Transport
-----------------
Product Transport calculates emissions from transportation of products. There are two different tables and
therefore two different methods to calculate emissions from employee commuting. The first is for those products which
are transported over vehicle miles, the second is for those products which are transported over ton miles.

Product Transport allows for inputs of vehicle types for the calculation over vehicle miles for the following vehicle types:

.. csv-table::
    :file: ./product_transport_vehicle_miles.csv
    :header-rows: 1

Product Transport allows for inputs of vehicle types for the calculation over ton miles for the following vehicle types:

.. csv-table::
    :file: ./product_transport_ton_miles.csv
    :header-rows: 1


The fundamental calculation for each vehicle type for vehicle miles and ton miles
are their :math:`\text{CO}_2`, :math:`\text{CH}_4`, and :math:`\text{N}_2\text{O}` emissions associated
with the vehicle type and based on the vehicle miles or ton miles traveled, respectively.

The formulas are:

.. math::

   Emissions_{units,\; gas,\; vehicle\; type} = Vehicle\; Miles\; Traveled_{unit} \cdot EF_{gas,\; vehicle\; type}

This equation is derived from Equation 5 from [EPA2008OptionalEmissionsfromCommutingBusinessTravelandProductTransport]_.

where :math:`Emissions_{unit, gas, vehicle\; type}` is the mass of :math:`\text{CO}_2`, :math:`\text{CH}_4`,
or :math:`\text{N}_2\text{O}` emitted, :math:`Vehicle\; Miles\; Traveled_{units}` is the travel distance in
:math:`units` (vehicle miles or ton miles), and :math:`EF_{gas, vehicle\; type}` is the product transport
emission factor of that :math:`gas` (:math:`\text{CO}_2`, :math:`\text{CH}_4`, or :math:`\text{N}_2\text{O}`)
which is based on the :math:`vehicle\; type`.

For product transport, the :math:`\text{CO}_2\; Equivalent\; Emissions_{GHG, transport}` in metric tons is calculated.
The formula is:


.. math::

    \text{CO}_2\; Equivalent\; Emissions_{GHG, transport} = \sum_{n=1}^{\infty} Total\; Emissions_{GHG, transport} \cdot GWP_{GHG}

This equation is derived from Equation 5 from [EPA2008OptionalEmissionsfromCommutingBusinessTravelandProductTransport]_.

where :math:`Total\; Emissions_{GHG, transport}` is the sum of all the emissions for that
:math:`GHG` (:math:`\text{CO}_2\;`, :math:`\text{CH}_4`, or :math:`\text{N}_2\text{O}`) and :math:`transport`
(either vehicle miles or ton miles), and :math:`GWP_{GHG}` is the global warming potential of that :math:`GHG`.
Note that in atomic6 the final value of this calculation is divided by :math:`1000` to convert this value into
:math:`metric \; tons`.


.. [EPA2008OptionalEmissionsfromCommutingBusinessTravelandProductTransport] EPA, 2008: 2008 EPA Greenhouse Gas Inventory Protocol Core Module Guidance Optional Emissions from Commuting, Business Travel and Product Transport, pp. 10
