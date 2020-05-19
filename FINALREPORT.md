# Project Report - Pelican
Pelican is a static site generator written in Python.
Unit testing was performed on this repository.

### Unit Testing with Sufficient Coverage
Work was initially intended to test Pelican's linter. However,
due to the complexity of the linting system within Pelican, I decided to 
write test suites to test Pelican's utility functionality.

Code coverage was conducted with `coverage.py` (https://coverage.readthedocs.io/en/coverage-5.1/#).
However, I was not able to get the coverage report for the specific files I've
altered due to the internal workings of Pelican and the vast number
of dependencies involved which constantly led to errors with running `coverage.py`.

### Automated Testing
Automated testing was not used for this project.

##### Link to Repository
https://github.com/csun-comp587-s20/pelican/pelican/tests/test_functionality.py
on the `master` branch of `csun-comp-587-s20` organization.

### Lessons Learned
* The Pelican project was found to be slightly too complicated for me  to write tests for as 
the project already involved meticulously tested code by its developers/contributors.

* Being able to write and execute efficient test suites requires deep understanding of the project
and it's internal workings.

* With my current knowledge of utilizing verification testing techniques with technologies 
alike Dafny, a verification testing approach could have been performed on this project.

* Introducing property-based testing could also prove to be useful to test this framework.


