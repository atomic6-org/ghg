.. _business-travel-api:

Business Travel
---------------
Business Travel is a `Scope 3 Emission <glossary.html>`_ that accounts for employee business travel including personal
vehicle travel, rail or bus travel, and air travel. The Business Travel category includes emissions from the
transportation of employees for business related activities in vehicles owned or operated by third parties, such as
aircraft, trains, buses, and passenger cars.


Class Documentation
************************
.. module:: atomic6ghg.formulas.business_travel

.. autoclass:: BusinessTravel
    :members:
    :undoc-members:
    :inherited-members:

Example Usage
******************

Python example code usage:

.. code-block:: python

    from atomic6ghg.formulas import BusinessTravel
    business_travel_input: dict = {
        "version": "business-travel.1.0.0",
        "personalVehicleRentalCarOrTaxiBusinessTravel": [
            {"vehicleType": "passengerCars", "vehicleMiles": 250}
        ]
    }
    engine = BusinessTravel(business_travel_input)
    outputs: dict = engine.to_dict()
    print(outputs.get('totalCO2EquivalentEmissions'))

EPA Equation Analysis
**********************
Business Travel calculates emissions from business travel of employees. There are three different tables and
therefore three different methods to calculate emissions from employee business travel. The first is for those employees
traveling by car, the second is for those employees traveling by rail or bus, and third one is for those employee
traveling by air.

Business Travel allows for inputs of personal vehicle types for the following vehicle types:

.. csv-table::
    :file: ./commuting_personal_vehicle.csv
    :header-rows: 1

Business Travel allows for inputs of public transportation types for the following public transport types:

.. csv-table::
    :file: ./commuting_public_transportation.csv
    :header-rows: 1

Business Travel allows for input of flight length types for the following flight length types:

.. csv-table::
    :file: ./business_travel_air.csv
    :header-rows: 1

The fundamental calculation for each vehicle type, public transport type, flight length for personal vehicle,
public transport, and flight length business travel are their :math:`\text{CO}_2`, :math:`\text{CH}_4`, and
:math:`\text{N}_2\text{O}` emissions associated with the vehicle type or flight length and based on the miles
traveled.

The formulas are:

.. math::

   Travel\; Emissions_{travel\ mode, \, T} = Travel_{travel\, mode} \cdot EF_{T}

This equation is derived from Equation 1 from [EPA2008_p4]_.

where :math:`Travel\; Emissions_{travel\ mode, \, T}` is the mass of :math:`\text{CO}_2`, :math:`\text{CH}_4`,
or :math:`\text{N}_2\text{O}`4` emitted, :math:`Travel_{travel\, mode}` is the travel distance in miles for a
specific travel mode, which can be vehicle miles traveled, passenger miles traveled or flight length for personal
vehicle, public transportation or flight respectively and :math:`EF_{T}` is the travel :math:`\text{CO}_2`,
:math:`\text{CH}_4`, or :math:`\text{N}_2\text{O}` emission factor which is based on the type of personal vehicle,
public transport or air travel.

For business travel, the :math:`\text{CO}_2\; Equivalent\; Emissions_{GHG, transport}` in metric tons is calculated.
The formula is:


.. math::

    \text{CO}_2\; Equivalent\; Emissions_{GHG, transport} = \sum_{n=1}^{\infty} Total\; Emissions_{GHG, transport} \cdot GWP_{GHG}

This equation is derived from [EPA2008_p4-7]_.

where :math:`Total\; Emissions_{GHG, transport}` is the sum of all the emissions for that
:math:`GHG` (:math:`\text{CO}_2\;`, :math:`\text{CH}_4`, or :math:`\text{N}_2\text{O}`) and :math:`transport`
(either personal vehicle, public transportation, or air travel), and :math:`GWP_{GHG}` is the
global warming potential of that :math:`GHG`.
Note that in atomic6 the final value of this calculation is converted into :math:`metric \; tons`.

.. [EPA2008_p4] `EPA, 2008: 2008 EPA Greenhouse Gas Inventory Protocol Core Module Guidance Optional Emissions from Commuting, Business Travel and Product Transport, pp. 4 <https://nepis.epa.gov/Exe/ZyNET.exe/P1001177.txt?ZyActionD=ZyDocument&Client=EPA&Index=2006%20Thru%202010&Docs=&Query=&Time=&EndTime=&SearchMethod=1&TocRestrict=n&Toc=&TocEntry=&QField=&QFieldYear=&QFieldMonth=&QFieldDay=&UseQField=&IntQFieldOp=0&ExtQFieldOp=0&XmlQuery=&File=D%3A%5CZYFILES%5CINDEX%20DATA%5C06THRU10%5CTXT%5C00000003%5CP1001177.txt&User=ANONYMOUS&Password=anonymous&SortMethod=h%7C-&MaximumDocuments=1&FuzzyDegree=0&ImageQuality=r75g8/r75g8/x150y150g16/i425&Display=hpfr&DefSeekPage=x&SearchBack=ZyActionL&Back=ZyActionS&BackDesc=Results%20page&MaximumPages=1&ZyEntry=7&slide>`_

.. [EPA2008_p4-7] `EPA, 2008: 2008 EPA Greenhouse Gas Inventory Protocol Core Module Guidance Optional Emissions from Commuting, Business Travel and Product Transport, pp. 4-7 <https://nepis.epa.gov/Exe/ZyNET.exe/P1001177.txt?ZyActionD=ZyDocument&Client=EPA&Index=2006%20Thru%202010&Docs=&Query=&Time=&EndTime=&SearchMethod=1&TocRestrict=n&Toc=&TocEntry=&QField=&QFieldYear=&QFieldMonth=&QFieldDay=&UseQField=&IntQFieldOp=0&ExtQFieldOp=0&XmlQuery=&File=D%3A%5CZYFILES%5CINDEX%20DATA%5C06THRU10%5CTXT%5C00000003%5CP1001177.txt&User=ANONYMOUS&Password=anonymous&SortMethod=h%7C-&MaximumDocuments=1&FuzzyDegree=0&ImageQuality=r75g8/r75g8/x150y150g16/i425&Display=hpfr&DefSeekPage=x&SearchBack=ZyActionL&Back=ZyActionS&BackDesc=Results%20page&MaximumPages=1&ZyEntry=7&slide>`_
