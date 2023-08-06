Introduction
============

What is InChI
~~~~~~~~~~~~~

   * The IUPAC International Chemical Identifier.
   * Textual identifier for chemical substances, designed to provide a standard way 
     to encode molecular information and to facilitate the search for such 
     information in databases and on the web.


Who develops InChI
~~~~~~~~~~~~~~~~~~

   * The not-for-profit *InChI Trust* (part of IUPAC) develops and supports the standard.
   * Prior to 1.04, the software was freely available under the open source LGPL license,
     but it now uses a custom license called IUPAC-InChI Trust License.


Basic structure of InChI
~~~~~~~~~~~~~~~~~~~~~~~~

   * The identifiers describe chemical substances in terms of layers of information:

      * atoms and their bond connectivity
      * tautomeric information
      * isotope information
      * stereochemistry
      * electronic charge information


InChI layers
~~~~~~~~~~~~

1. Main layer
   
   * Chemical formula (no prefix). This is the only sublayer that must occur in every InChI.
   * Atom connections (prefix: "c"). The atoms in the chemical formula (except for hydrogens) are numbered in sequence; 
     this sublayer describes which atoms are connected by bonds to which other ones.
   * Hydrogen atoms (prefix: "h"). Describes how many hydrogen atoms are connected to each of the other atoms.

2. Charge layer

   * proton sublayer (prefix: "p" for "protons")
   * charge sublayer (prefix: "q")

3. Stereochemical layer
   
   * double bonds and cumulenes (prefix: "b")
   * tetrahedral stereochemistry of atoms and allenes (prefixes: "t", "m")
   * type of stereochemistry information (prefix: "s")

4. Isotopic layer (prefixes: "i", "h", as well as "b", "t", "m", "s" for isotopic stereochemistry)
5. Fixed-H layer (prefix: "f"); contains some or all of the above types of layers except atom connections; 
   may end with "o" sublayer; never included in standard InChI
6. Reconnected layer (prefix: "r"); contains the whole InChI of a structure with 
   reconnected metal atoms; never included in standard InChI


Examples
~~~~~~~~

   .. image:: _static/ethanol.png

   * InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3

   .. image:: _static/vitaminC.png 

   * InChI=1S/C6H8O6/c7-1-2(8)5-3(9)4(10)6(11)12-5/h2,5,7-8,10-11H,1H2/t2-,5+/m0/s1
