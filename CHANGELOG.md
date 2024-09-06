# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [0.2.0] - 2024-09-04

### Added
- External Tools section in the files (pages/external) and the nav bar - Issue https://github.com/Borealis-BioModeling/aurora-pkpd/issues/19 
- Added a drugsynergy page under pages/external and the External Tools section of the navbar. Page links out to the MuSyC web app - Issue https://github.com/Borealis-BioModeling/aurora-pkpd/issues/6

### Changed
- Moved the HT Cell Proliferation page under the External Tools section and updated the page to linkout to the Thunor web App - Issue https://github.com/Borealis-BioModeling/aurora-pkpd/issues/4
- Updated the compartmental/build page to put the descriptions/info for each step under expanders.
- Updated all the compartmental pages as well as the NCA page and Exposure-Response pages, putting the page descriptions under expanders with text printed using `st.info` to help further declutter the pages and hide extraneous info.
- Updated the home page to put each of the modeling/analysis options under expanders in an effort to help declutter the app pages and hide extraneous info.


## [0.1.2] - 2024-08-02

### Fixed
- Upload page: `pages/compartmental/upload.py`. Added in an option to specify the branch of the repository to load a model file from as a fix for Issue https://github.com/Borealis-BioModeling/aurora-pkpd/issues/17

## [0.1.1] - 2024-07-30

### Fixed
- Upload page: `pages/compartmental/upload.py`. Fixed the incorrect path to build page in the `st.switch_page` widget. Fix for Issue https://github.com/Borealis-BioModeling/aurora-pkpd/issues/13


## [Unreleased] - yyyy-mm-dd

N/A

### Added

### Changed

### Fixed