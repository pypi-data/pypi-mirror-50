<img alt="sosw - Serverless Orchestrator of Serverless Workers" width="350" src="https://raw.githubusercontent.com/bimpression/sosw/docme/docs/_static/images/logo/sosw_black.png">

# Serverless Orchestrator of Serverless Workers
[![Build Status](https://travis-ci.org/bimpression/sosw.svg?branch=master)](https://travis-ci.org/bimpression/sosw)
[![Documentation Status](https://readthedocs.org/projects/sosw/badge/?version=latest)](https://docs.sosw.app/en/latest/?badge=latest)

**sosw** is a set of serverless tools for orchestrating asynchronous invocations of AWS Lambda Functions (Workers).
 ---
 Please pronounce `sosw` correctly: _/ˈsɔːsəʊ/_
 ---

## Documentation
[https://docs.sosw.app](https://docs.sosw.app/en/latest/)

## Essential Workflows
![Essential sosw Workflow Schema](https://raw.githubusercontent.com/bimpression/sosw/docme/docs/_static/images/simple-sosw.png)

## Dependencies
- Python 3.6, 3.7
- [boto3](https://github.com/boto/boto3) (AWS SDK for Python)

## Installation
See the [Installation Guidelines](https://docs.sosw.app/en/latest/installation.html) in the Documentation.

## Development
### Getting Started

Assuming you have Python 3.6 and `pipenv` installed. Create a new virtual environment: 

```bash
$ pipenv shell
```

Now install the required dependencies for development:

```bash
$ pipenv sync --dev
```

### Running Tests

Running unit tests:
```bash
$ pytest ./sosw/test/suite_3_6_unit.py
```

### Contribution Guidelines

#### Release cycle
- We follow both [Semantic Versioning](https://semver.org/) pattern
  and [PEP440](https://www.python.org/dev/peps/pep-0440/) recommendations where comply
- Master branch commits (merges) are automatically packaged and published to PyPI.
- Branches for planned staging versions follow the pattern: `X_Y_Z` (Major.Minor.Micro)
- Make your pull requests to the latest staging branch (with highest number)
- Latest documentation is compiled from branch `docme`.
  It should be up to date with latest **staging** branch, not the master.
  Make PRs with documentation change directly to `docme`.

#### Code formatting
Follow [PEP8](https://www.python.org/dev/peps/pep-0008/), but:
- both classes and functions are padded with 2 empty lines
- dictionaries are value-alligned

#### Initialization
1. Fork the repository: https://github.com/bimpression/sosw
2. Register Account in AWS: [SignUp](https://portal.aws.amazon.com/billing/signup#/start)
3. Run `pipenv sync –dev` to setup your virtual environment and download the required dependencies
4. Create DynamoDB Tables: 
    - You can find the CloudFormation template for the databases [in the example](https://raw.githubusercontent.com/bimpression/sosw/docme/docs/yaml/sosw-shared-dynamodb.yaml).
    - If you are not familiar with CloudFormation, we highly recommend at least learning the basics from [the tutorial](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/GettingStarted.Walkthrough.html).
5. Create Sandbox Lambda with Scheduler
6. Play with it.
7. Read the Documentation Convention.

#### More
See more guidelines for contribution [in the docs](https://docs.sosw.app/en/latest/contribution/index.html).

### Building the docs
Sphinx is used for building documentation. To build HTML documentation locally, use:

```bash
$ sphinx-build -ab html ./docs ./sosw-rtd
```

You can then use the built in Python web server to view the html version directly from `localhost` in your preferred browser.

```bash
$ cd sosw-rtd
$ python -m http.server
```

## Copyright

This document has been placed in the public domain.
    
    sosw - Serverless Orchestrator of Serverless Workers
    Copyright (C) 2019  sosw core contributors:
        Nikolay Grishchenko
        Sophie Fogel
        Gil Halperin
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/gpl-3.0.html>.
