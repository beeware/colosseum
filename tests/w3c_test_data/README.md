# Introduction

W3C CSS tests:
- source: https://github.com/w3c/csswg-test
- view tests: http://test.csswg.org/harness/

W3C tests are defined as:
- Test (CSS, some HTML elements)
- Reference (a simpler/alternative CSS and some HTML elements)
- Results are verified usually visually by a human, recorded in a timestamped db

# Strategy

__Do this regularly__:

0. Install `selenium`.
1. Run `tests/get_w3c_test_data.py TEST_DIR`, where `TEST_DIR` is the path to a checkout of `https://github.com/w3c/csswg-test`. This will:
    1. Use `Selenium` to launch a browser to interpret CSS and render:
        1. Pull attribute/value pairs as test inputs
        2. Pull width/height/x/y as test outputs
        3. TODO: loop over a number of browsers
    2. Store inputs/outputs to disk, this is list a definitions corresponding to w3c tests
2. Commit list of definitions to `pybee/colosseum` repo


__Do this every time the test suite is run__:

1. Loop over list of definitions:
    1. Dynamically create a unit test for each definition
    2. Construct dicts for inputs and expected outputs from definition

# Definitions Schema

The definitions are stored as JSON files on disk. Each file is in essence a
dict with the following keys:

| field | description |
| :---- | :---------- |
| capabilities | Selenium output, obtain from `driver.capabilities` |
| node_data | test definition, see sub-items |
| node_data.style | key-value pairs of the CSS style to be applied to the node |
| node_data.position | key-value pairs with keys for 'width', 'height', 'top', 'left' |
| node_data.children | a list of nodes with the same specification as `node_data`. For nodes without children, use an empty list. |
| stored_time | linux timestamp |
| w3c_path | path of the W3C CSS test file relative to the root of the `csswg-test` repo |
| w3c_sha | Commit SHA of the `csswg-test` repo at the time of definitions generation |

# Example Definition

See `example.json`, which implements `test_layout.LayoutEngineTest.test_should_layout_node_with_children`
in the schema defined above.
