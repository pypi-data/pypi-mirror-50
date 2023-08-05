# Notarius

Notarius submits a macOS application package to Apple to be notarized.

## Requirements

+ Python3
+ Xcode 10+

## Installation

`pip install notarius`

## Usage

~~~
$ notarius -h
Usage: notarius [options]

Options:
  -h, --help      show this help message and exit
  -f FILENAME     DMG to use (required for all actions)
  --mock          Use mock answers

  Notarize app:
    --notarize
    -b BUNDLE_ID  App's bundle ID
    -p PASSWORD   Apple developer account's password
    -u USERNAME   Apple developer account

  Validate app after notarization:
    --validate
~~~
