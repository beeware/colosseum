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

1. Loop over tests defined in `w3c/csswg-test`
    1. Use `Selenium` to launch a browser to interpret CSS and render:
        1. Pull attribute/value pairs as test inputs
        2. Pull width/height/x/y as test outputs
        3. TODO: loop over a number of browsers
    2. Store inputs/outputs to disk, this is list a definitions corresponding to w3c tests
2. Commit list of definitions to `pybee/colosseum` repo


__Do this on every test__:

1. Loop over list of definitions:
    1. Construct `nested_dict` for inputs and expected outputs from definition
    2. Run as unit test

# Definitions Schema

The definitions is stored as a JSON on disk. It is in essence a list of dict where each dict has the following specification:

| field | description |
| :---- | :---------- |
| capabilities | Selenium output, obtain from `driver.capabilities` |
| node_data | test descriptions, a tree of nodes where each node contains three keys, `children` is a list of children nodes, `position` is a dict with keys `height`, `left`, `top` and `width`, and `style` is a list of key-value pairs of allowed style keywords. |
| stored_time | linux timestamp |
| w3c_path | path of the W3C CSS test file relative to the root of the `csswg-test` repo |
| w3c_sha | Commit SHA of the `csswg-test` repo at the time of definitions generation |

# Example Definition

```
[
    {
        "capabilities": {},
        "node_data": {
            "children": [
                {
                    "children": [],
                    "position": {
                        "height": 500,
                        "left": 0,
                        "top": 0,
                        "width": 500
                    },
                    "style": {
                        "height": 500,
                        "width": 500
                    }
                },
                {
                    "children": [],
                    "position": {
                        "height": 250,
                        "left": 0,
                        "top": 500,
                        "width": 250
                    },
                    "style": {
                        "height": 250,
                        "width": 250
                    }
                },
                {
                    "children": [],
                    "position": {
                        "height": 125,
                        "left": 0,
                        "top": 750,
                        "width": 125
                    },
                    "style": {
                        "height": 125,
                        "width": 125
                    }
                }
            ],
            "position": {
                "height": 1000,
                "left": 0,
                "top": 0,
                "width": 1000
            },
            "style": {
                "height": 1000,
                "width": 1000
            }
        },
        "stored_time": 1471228060,
        "w3c_path": "css-flexbox-1/align-content-001.htm",
        "w3c_sha": "7be59dd2ba04892c68f9978bd601935a23375473"
    },
    ...
]
```
