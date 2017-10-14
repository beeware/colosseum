function dump_test_case(node) {
    var i, child
    var style = window.getComputedStyle(node)
    var defaultStyles = {
        // 8. Box model #######################################################
        // 8.3 Margin properties
        'margin-top': '0px',
        'margin-right': '0px',
        'margin-bottom': '0px',
        'margin-left': '0px',

        // 8.4 Padding properties
        'padding-top': '0px',
        'padding-right': '0px',
        'padding-bottom': '0px',
        'padding-left': '0px',

        // 8.5 Border properties
        // 8.5.1 Border width
        'border-top-width': '0px',
        'border-right-width': '0px',
        'border-bottom-width': '0px',
        'border-left-width': '0px',

        // 8.5.2 Border color
        'border-top-color': 'rgb(0, 0, 0)',
        'border-right-color': 'rgb(0, 0, 0)',
        'border-bottom-color': 'rgb(0, 0, 0)',
        'border-left-color': 'rgb(0, 0, 0)',

        // 8.5.3 Border style
        'border-top-style': 'none',
        'border-right-style': 'none',
        'border-bottom-style': 'none',
        'border-left-style': 'none',

        // 9. Visual formatting model #########################################
        // 9.2.4 The display property
        'display': 'inline',
        // 9.3 Positioning schemes
        'position': 'static',

        // 9.3.2 Box offsets
        'top': 'auto',
        'bottom': 'auto',
        'left': 'auto',
        'right': 'auto',

        // 9.5.1 Positioning the float
        'float': 'none',
        // 9.5.2 Controlling flow next to floats
        'clear': 'none',

        // 9.9 Layered Presentation
        'z-index': 'auto',

        // 9.10 Text Direction
        'direction': 'ltr',
        'unicode-bidi': 'normal',

        // 10. Visual formatting model details ################################
        // 10.2 Content width
        'width': 'auto',

        // 10.4 Minimum and maximum width
        'min-width': '0px',
        'max-width': 'none',

        // 10.5 Content height
        'height': 'auto',

        // 10.7 Minimum and maximum heights
        'min-height': '0px',
        'max-height': 'none',

        // 10.8 Leading and half-leading
        // line-height
        // vertical-align

        // 11. Visual effects #################################################
        // 11.1.1 Overflow
        // overflow

        // 11.1.2 Clip
        // clip

        // 11.2 Visibility
        // visibility

        // 12. Visual effects #################################################
        // 12.2 The content property
        // content

        // 12.3 Quotation marks
        // quotes

        // 12.4 Automatic counters and numbering
        // counter-reset
        // counter-increment

        // 12.5 Lists
        // list-style-type
        // list-style-image
        // list-style-position

        // 13. Paged media ####################################################
        // 13.3.1 Page break properties
        // page-break-before
        // page-break-after
        // page-break-inside

        // 13.3.2 Breaks inside elements
        // orphans
        // widows

        // 14. Colors and backgrounds #########################################
        // 14.1 Foreground color
        // color

        // 14.2.1 Background properties
        // background-color
        // background-image
        // background-repeat
        // background-attachment
        // background-position

        // 15. Fonts ##########################################################
        // 15.3 Font family
        // font-family

        // 15.4 Font Styling
        // font-style

        // 15.5 Small-caps
        // font-variant

        // 15.6 Font boldness
        // font-weight

        // 15.7 Font size
        // font-size

        // 16. Text ###########################################################
        // 16.1 Indentation
        // text-indent

        // 16.2 Alignment
        // text-align

        // 16.3 Decoration
        // text-decoration

        // 16.4 Letter and word spacing
        // letter-spacing
        // word-spacing

        // 16.5 Capitalization
        // text-transform

        // 16.6 White space
        // white-space

        // 17. Tables #########################################################
        // 17.4.1 Caption position and alignment
        // caption-side

        // 17.5.2 Table width algorithms
        // table-layout

        // 17.6 Borders
        // border-collapse
        // border-spacing
        // empty-cells

        // 18. User interface #################################################
        // 18.1 Cursors
        // cursor

        // 18.4 Dynamic outlines
        // outline-width
        // outline-style
        // outline-color

    }

    var result = {
        'tag': node.tagName,
        'style': {},
    }

    // Copy over all computed styles that have been modified
    for (var s in defaultStyles) {
        if (style.getPropertyValue(s) !== defaultStyles[s]) {
            result['style'][s.replace(/-/g, '_')] = style.getPropertyValue(s)
        }
    }

    // Inspect children as well.
    if (node.childElementCount > 0) {
        result['children'] = []
        for (i = 0; i < node.childElementCount; i++) {
            child = node.children[i];
            result['children'].push(dump_test_case(child))
        }
    }

    return result
}

function dump_reference(node) {
    var i, child
    var position = node.getBoundingClientRect()

    var result = {
        'position': [position.top, position.left],
        'size': [position.width, position.height]
    }

    if (node.childElementCount > 0) {
        result['children'] = []
        for (i = 0; i < node.childElementCount; i++) {
            child = node.children[i];
            result['children'].push(dump_reference(child))
        }
    }
    return result
}

var n, node
var result = {
    'help': [],
}

/*******************************************************
 * Mainline
 *******************************************************/

// Read the document metadata, looking for key elements:
//   <link rel='match' href="A test file that shows passing content">
//   <link ref='help' href="The URL of the relevant sections of the spec">
//   <meta name='assert' content='The description of what the test asserts'
for (n = 0; n < document.head.childElementCount; n++) {
    node = document.head.children[n]
    if (node.tagName.toLowerCase() === 'link' && node.getAttribute('rel') === 'match') {
        result.matches = node.getAttribute('href')
    } else if (node.tagName.toLowerCase() === 'link' && node.getAttribute('rel') === 'help') {
        result.help.push(node.getAttribute('href'))
    } else if (node.tagName.toLowerCase() === 'meta' && node.getAttribute('name') === 'assert') {
        result.assert = node.getAttribute('content')
    }
}

if (result.matches) {
    // If the document has a 'matches' clause, it's a test. The reference
    //    output is the linked document. It may also have an 'assert'
    //    clause, but isn't required to.
    result.test_case = dump_test_case(document.body)
} else if (result.assert) {
    // If the document has an 'assert' clause, but no 'matches' clause,
    //    it's a test that is it's own reference output.
    result.test_case = dump_test_case(document.body)
    result.reference = dump_reference(document.body)
} else {
    // There's no 'assert' *or* 'matches' clause; this is a
    // reference file.

    result.reference = dump_reference(document.body)
}

JSON.stringify(result)