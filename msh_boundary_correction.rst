Magnetosheath Boundary Correction
==================================

As it is not unusual that modelled magnetopause/bow shock (currently
`Shue et al. (1998) <https://agupubs.onlinelibrary.wiley.com/doi/epdf/10.1029/98JA01103>`_
magnetopause model and `Jelinek et al. (2012) <https://agupubs.onlinelibrary.wiley.com/doi/epdf/10.1029/2011JA017252>`_
bow shock model, respectively) does not match with observed magnetosheath
boundaries, we added manual boundary adjust function.

As described in `Usage`, mpoff and bsoff parameters adjust MP/BS location in
radial direction (positive is Sun-side, negative is Earth-side) in Earth radii
at each input point.
