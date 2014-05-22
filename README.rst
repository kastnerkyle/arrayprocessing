arrayprocessing
===============

Array processing algorithms and simulation for RF array design, 
direction of arrival (DOA) / direction finding (DF), and geolocation.

Current Element Types
---------------------

* Monopole

Current Geometry Types
----------------------

* Linear

* Random 

Current Array Types
-------------------

* Uniformly Weighted

* Classical Beamformer

To Do
=====

* Circular geometry

* Planar geometry

* Y geometry

* MVDR Beamformer

* Null Steered

* Combination Beamformer (combinations of above types i.e. MVDR + null steered)

* Implement DF algorithms (MVDR, MPDR, MUSIC, ESPIRIT, others?)

* Tools for DF error

* Array type for arbitrary geometry passed as [N, 3] numpy array

* Doublet elements

* Give elements a plot_response() function

* Read arrays and geometries from CSV

* Add data simulation and dataset support

* Add tests

* Integrate with empy and work towards arbitrary EM/RF simulation
