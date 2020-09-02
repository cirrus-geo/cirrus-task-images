# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [v0.2.0] - 2020-09-02

## Changed
- Output payload is written to a new file on s3 (same name as input .json file except ends with _out.json instead) rather than back to the original location

## Fixed
- Issue where subsequent batch jobs run from failure will get the output payload as the input payload because the failure happens when shutting down the docker container, but after the output payload has overwritten the input payload on s3

## [v0.1.1] - 2020-07-30

## Fixed
- Explicit response from lambda handler copied back to s3, not modified input payload

## [v0.1.0] - 2020-07-01

Initial release


[Unreleased]: https://github.com/sat-utils/sat-stac/compare/master...develop
[v0.2.0]: https://github.com/cirrus-geo/cirrus-lib/compare/v0.1.1...v0.2.0
[v0.1.1]: https://github.com/cirrus-geo/cirrus-lib/compare/v0.1.0...v0.1.1
[v0.1.0]: https://github.com/cirrus-geo/cirrus-job-images/tree/0.1.0
