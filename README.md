This small test suite has been built to test the [link
checker](http://validator.w3.org/checklink "W3C Link Checker") at W3C,
but could be used for any tool used to either check links in HTML
documents, spiders, or miscellaneous Web User-Agents by adding the proper Python module in `harness/lib`.

The test suite uses a series of hardcoded domain names for its operation, listed in the `hosts` file. They should be added to your local DNS resolution before running the crawler under test. On Unix systems, this can be obtained by appending the cost of the `hosts` file to `/etc/hosts`, or, on linux by running the command-under-test in a dedicate execution namespace, à la
```sh
 bwrap --dev-bind / / --ro-bind hosts /etc/hosts sh -c "command args"
```