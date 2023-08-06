Development version with additional functionality
=================================================

1. Utilization of metabolomics BMRB entries

    * Goal

       * Use metabolite entries provided by BMRB that contain 
         transition peaks and assigned peaks for C13 and H1 
         to generate isotopically resolved InChI identifiers 
         for transition peaks that we have that will be used
         for NMR studies.  

    * Problem  

       * Transition peaks in metabolomics entries provided by
         BMRB are not assigned.

    * Development

       * Use ``nmrstarlib`` to pull necessary loops from metabolomics entries.
       * Pull the coupling constants matrix from ``xml`` entry. 
       * Use coupling constants matrix to generate transition peaks and assign them.
       * Identify hydrogen couplings from coupling constant matrix and identify which 
         neighbot hydrogens caused splitting of peaks.
       * Use assigned C13 peaks to assign C13 transition peaks 
         (easy to do because there are normally 1-to-1 mapping between thos peaks).
       * Finally generate isotopically resloved InChI

       .. code:: bash

          $ tree

          bmse
          ├── bmse.py
          ├── ccm.py
          ├── __init__.py
          ├── namebmse.py

       * Some cases are hard to calculate those transition peaks from coupling constants matrix.
       * There are only 500 entries out of 1500 entries have coupling constants matrix provided.

2. Use 1D-1H J3 couplings (scalar couplings of hydrogens separated by 3 single bonds) to generate
   InChI and then use those to assign experimental transition peaks.   
