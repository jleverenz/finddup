:orphan:

**finddup** Recipes
===================

Delete duplicate files in ``dir1`` and ``dir2`` with rm. Note that if a pair of
duplicate files is found in both ``dir1`` and ``dir2``, those within ``dir2``
will be selected as duplicates.::

    finddup dir1/ dir2/ | xargs rm

Move duplicates in ``dupes`` directory to a target ``copies`` directory,
renumbering when there is a filename colission.::

    finddup dupes/ | xargs -I{} mv --backup=numbered {} copies/
