######################################
lsst-sphinx-bootstrap-theme Change log
######################################

0.2.1 (2019-08-01)
==================

Infrastructure changes
----------------------

- Updated build pipeline to use Gulp 4 and new versions of all npm dependencies.

Design changes
--------------

- ``<pre>`` elements have a small font size, 0.8 em, that helps ensure that 80-character-wide samples fit in the text column.
  As well, line wrapping is disabled in ``<pre>`` elements and if the content does overflow, the browser will show a horizontal scroll bar.
- ``<code>`` also have a slightly smaller font size, 0.95 em, which helps them match up with text inline.

0.2.0 (2018-05-23)
==================

Infrastructure changes
----------------------

- Adopted Gulp for building front-end web assets.
- Adopted Sass for generating CSS.
  The build pipeline involves gulp-sass, gulp-clean-css, gulp-sourcemaps, and autoprefixer with gulp-postcss.
  Because of the new build pipeline, we've been able to concatenate all the CSS together into a single GET.
  To make this possible, we've had to fork the basic theme's CSS file into this repo.
- Using Prettier with a precommit hook to maintain Sass code style (and eventually JavaScript too).
- Improved the PyPI deployment script so that it doesn't double-push to PyPI.
- Adopted ``setuptools_scm`` to automate the process of setting package versions for PyPI based on Git tags.

Design changes
--------------

- Switched logo to white-outlined version.
- Removed Index, Module links, and search bar in header.
  Replaced those with a LSST-global links (forum, www.lsst.org, and www.lsst.io)
- Moved the search box to the top of the side bar since another search bar isn't present in the top nav bar.
- Set up a color system based on www.lsst.org's blue, including a triad-based red, and blue tinted greys and whites.
  All elements of the page are using this colour system. H2s are blue, for example.
- Improved the appear of admonitions to tone them down just a smidge and also to integrate them with the colour system.
- Tweaked wording for page TOC
- Improved spacing in sidebar's navigation list.

0.1.2 (2018-03-08)
==================

- Switch to Source Sans and Source Code Pro from Adobe, via typekit.com.
- Larger font (16 px), narrower measure, slightly tighter leading.
- H2s now have overlines, not underlines.
- Remove outline around inline code samples; retain background hint.

0.1 (2016-12-14)
================

- Forked from  `astropy-helpers theme <https://github.com/astropy/astropy-helpers>`_ and refactored into a sphinx theme-only package.
- Added LSST branding and colors.
- Using FF Meta and Hack from typekit.com.
