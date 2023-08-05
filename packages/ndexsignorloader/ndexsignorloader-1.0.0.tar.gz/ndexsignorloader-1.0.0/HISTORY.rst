=======
History
=======

1.0.0 (2019-07-30)
-------------------

* **--edgecollapse** flag added which collapses all edges putting all attributes
  minus **direct** into lists. For **sentence** attribute each entry the
  list is now prepended with href link to citation labeled pubmed:#### In addition,
  if **--edgecollapse** flag is set then a **notes** network attribute is added to
  let user know.

* **--style** can also accept NDEx UUID for network style. Network needs to be on  same
  server set in **--profile**

0.3.0 (2019-07-29)
-------------------

* Added commandline flag **--visibility** that lets user dictate whether NEW networks are public or private (default is public)

* Signor Full Human, Signor Full Rat, and Signor Full Mouse networks have been renamed
  to Signor Complete - Human, Signor Complete - Rat, Signor Complete - Mouse

* On edges, replaced location attribute value of phenotypesList with empty string NSU-75

* Added __iconurl network attribute and renamed type network attribute to networkType

0.2.0 (2019-06-28)
------------------

* Changed prov:wasDerivedFrom network attribute to just signor website URL for full networks

* Removed author network attribute if no value is found

* Removed labels attribute for full networks 

0.1.0 (2019-06-27)
------------------

* First release on PyPI.
