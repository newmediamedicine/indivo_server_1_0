Important note about cloning this repository
=====================================================================

For the Python import paths to work, you must do the following: 

When cloning this repo, clone into indivo_server.

* git clone https://github.com/fyoung/indivo_server_1_0.git indivo_server

Please note when following the instructions for installing that for
this repository you should ignore the steps involving submodules
namely "git submodule init" and "git submodule update" because they
are not supported.

Also there is no need to "checkout" a specific tag. What you retrieve
from this repository is the latest stable version.


Welcome to Indivo
=================

Indivo is the original personally controlled health record (PCHR) system. 
A PCHR enables an individual to own and manage a complete, secure, digital 
copy of her health and wellness information. Indivo integrates health 
information across sites of care and over time. Indivo is free and 
open-source, uses open, unencumbered standards, and is actively deployed 
in diverse settings.

See indivohealth.org for more information about the project.

See docs.indivohealth.org for technical documentation.

Required Setup
--------------

* cron jobs should be scheduled to run::
  
  python manage.py cleanup_old_tokens

See http://wiki.chip.org/indivo/index.php/HOWTO:_install_Indivo_X for 
full installation instructions.


Licensing
---------

Copyright (C) 2012  Children's Hospital Boston. All rights reserved.

This program is free software: you can redistribute it and/or modify it 
under the terms of the GNU General Public License as published by the 
Free Software Foundation, either version 3 of the License, or (at your 
option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

A copy of the GNU General Public License is located in the LICENSE.txt
file in this repository, and at http://www.gnu.org/licenses/.
