# PiXL Maths App Farm

This project requires at least Python 3.6 (can probably use lower versions but not tested).
The tool is designed to work with [PiXL's Maths App](https://mathsapp.pixl.org.uk/PMA2.html).
It was created by reverse engineering the flash file and took a huge amount of time so any
support is appreciated.

## Setup
1. Install [Python](https://www.python.org/downloads/)
2. Run `pip install -U pma` in your terminal/command prompt. This is the same command to update

There are also [docker images](https://hub.docker.com/r/orangutan/pma).

## CLI Usage
* `pma farm --help`
* `python -m pma farm --help`
* `python -m pma farm --goal 100 SCHOOL_ID USERNAME PASSWORD`
* `python -m pma farm --yes SCHOOL_ID USERNAME PASSWORD`
* `python -m pma farm --goal 100 --yes SCHOOL_ID USERNAME PASSWORD`
* `python -m pma farm SCHOOL_ID USERNAME PASSWORD`
