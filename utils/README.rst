W3C testing strategy
====================

W3C CSS tests:
- source: https://github.com/w3c/csswg-test
- view tests: http://test.csswg.org/harness/

W3C tests are defined as:

- Test (CSS, some HTML elements)

- Reference (a simpler/alternative CSS and some HTML elements)

- Results are verified usually visually by a human, recorded in a timestamped db

Testing strategy
----------------

Manually verifying tests in a subjective fashion is a surefire way to make sure
they never get run. So, Colosseum converts the official W3C tests into unit tests
that can be run objectively.

The W3C tests are published in sections. To add a new section to the test suite,
run::

    python -m utils.get_w3c_test_data <test_dir> <test_section>

where `<test_dir>` is the path to a checkout of `https://github.com/w3c/csswg-test`,
and `<test_section>` is the name of the top-level test section. This will convert
the section into a series of unit tests.

The W3C will occasionally update the test suite. To merge these changes into
Colosseum, run::

    python -m utils.get_w3c_test_data <test_dir>`
