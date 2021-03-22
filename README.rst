*****************************************
Power-to-Heat in district heating systems
*****************************************

An optimization model of a district heating network with investment in large-scale heatpumps,
thermal storage and resistive heaters.


How to run the model
~~~~~~~~~~~~~~~~~~~~

To run the model, make sure that the timeseries data

* demand_heat_2017.csv
* price_electricity_spot_2017.csv

are provided in model/00_raw. Then, run the model:

.. code-block::

    python main.py


License
=======

Copyright (C) 2017 Beuth Hochschule für Technik Berlin and Reiner Lemoine Institut gGmbH

This program is free software: you can redistribute it and/or modify it under the terms of the GNU
General Public License as  published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not,
see http://www.gnu.org/licenses/.
