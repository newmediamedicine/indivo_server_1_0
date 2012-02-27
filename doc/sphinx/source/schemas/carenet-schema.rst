Indivo Carenet Schema
=====================

A list of carenets is returned when a user/app wants to know how a document is shared. However, this same 
list of carenets might be used in a different setting. Thus, the "mode" attribute is optional. It indicates 
whether sharing in this carenet was done explicitly, or via some implicit auto-share rule.

Schema:

.. include:: /../../../schemas/metadata_schemas/carenet.xsd
   :literal:

Example:

.. include:: /../../../schemas/metadata_schemas/carenet.xml
   :literal:
