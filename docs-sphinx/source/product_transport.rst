
.. _product-transport-api:

Product Transport
-----------------
Product Transport is a `Scope 3 Emission <glossary.html>`_ that accounts for emissions from the transportation of
products. This can be transportation via `vehicle miles <glossary.html>`_ or via `ton-miles <glossary.html>`_.

Class Documentation
************************
.. module:: atomic6ghg.formulas.product_transport

.. autoclass:: ProductTransport
    :members:
    :undoc-members:
    :inherited-members:

Example Usage
******************

Python example code usage:

.. code-block:: python

    from atomic6ghg.formulas import ProductTransport
    product_transport_input: dict = {
        "version": "product-transport.1.0.0",
        "productTransportByVehicleMiles": [
            {"vehicleType": "passengerCars", "vehicleMiles": 250}
        ]
    }
    engine = ProductTransport(product_transport_input)
    outputs: dict = engine.to_dict()
    print(outputs.get('totalCO2EquivalentEmissions'))

EPA Equation Analysis
**********************
There are two different tables and therefore two different methods to calculate emissions from employee commuting. The
first is for those products which are transported over vehicle miles, the second is for those products which are
transported over ton miles.

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
with the vehicle type and based on the vehicle miles or ton miles traveled.

The formulas are:

.. math::

   Emissions_{transport, GHG,\; vehicle\; type} = Miles\; Traveled_{transport} \cdot EF_{GHG,\; vehicle\; type}

This equation is derived from Equation 5 from [EPA2008_p10]_.

where :math:`Emissions_{transport, GHG, vehicle\; type}` is the mass of the :math:`GHG` (either :math:`\text{CO}_2`,
:math:`\text{CH}_4`, or :math:`\text{N}_2\text{O}`) emitted, :math:`Miles\; Traveled_{transport}` is the travel
distance over the :math:`transport` (either vehicle miles or ton-miles), and :math:`EF_{gas, vehicle\; type}` is the product transport emission factor of that :math:`GHG`
(:math:`\text{CO}_2`, :math:`\text{CH}_4`, or :math:`\text{N}_2\text{O}`) which is based on the :math:`vehicle\; type`.

For product transport, the :math:`\text{CO}_2\; Equivalent\; Emissions_{GHG, transport}` in metric tons is calculated.
The formula is:

.. math::

    \text{CO}_2\; Equivalent\; Emissions_{GHG, transport} = \sum_{n=1}^{\infty} Total\; Emissions_{GHG, transport} \cdot GWP_{GHG}

This equation is derived from Equation 5 from [EPA2008_p10]_.

where :math:`Total\; Emissions_{GHG, transport}` is the sum of all the emissions for that
:math:`GHG` (:math:`\text{CO}_2\;`, :math:`\text{CH}_4`, or :math:`\text{N}_2\text{O}`) and :math:`transport`
(either vehicle miles or ton miles), and :math:`GWP_{GHG}` is the global warming potential of that :math:`GHG`.
Note that in atomic6 the final value of this calculation is converted to :math:`metric \; tons`.


.. [EPA2008_p10] `EPA, 2008: 2008 EPA Greenhouse Gas Inventory Protocol Core Module Guidance Optional Emissions from Commuting, Business Travel and Product Transport, pp. 10 <https://nepis.epa.gov/Exe/ZyNET.exe/P1001177.txt?ZyActionD=ZyDocument&Client=EPA&Index=2006%20Thru%202010&Docs=&Query=&Time=&EndTime=&SearchMethod=1&TocRestrict=n&Toc=&TocEntry=&QField=&QFieldYear=&QFieldMonth=&QFieldDay=&UseQField=&IntQFieldOp=0&ExtQFieldOp=0&XmlQuery=&File=D%3A%5CZYFILES%5CINDEX%20DATA%5C06THRU10%5CTXT%5C00000003%5CP1001177.txt&User=ANONYMOUS&Password=anonymous&SortMethod=h%7C-&MaximumDocuments=1&FuzzyDegree=0&ImageQuality=r75g8/r75g8/x150y150g16/i425&Display=hpfr&DefSeekPage=x&SearchBack=ZyActionL&Back=ZyActionS&BackDesc=Results%20page&MaximumPages=1&ZyEntry=13&slide>`_
