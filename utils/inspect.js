function dump_test_case(node) {
    var result = {
        'tag': node.tagName,
        'style': {}
    }

    if (node.tagName) {
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
            // 'background-color': 'rgb(0, 0, 0, 0)',
            // 'background-image': 'none',
            // 'background-repeat': 'repeat',
            // 'background-attachment': 'scroll',
            // 'background-position': '0% 0%',

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

        // Copy over all computed styles that have been modified
        for (var s in defaultStyles) {
            if (style.getPropertyValue(s) !== defaultStyles[s]) {
                result['style'][s.replace(/-/g, '_')] = style.getPropertyValue(s)
            }
        }

        // Inspect children as well.
        if (node.childNodes.length > 0) {
            result['children'] = []
            for (var i = 0; i < node.childNodes.length; i++) {
                child = dump_test_case(node.childNodes[i])
                if (child) {
                    result['children'].push(child)
                }
            }
        }
    } else {
        var text = node.textContent.trim()
        if (text) {
            result['text'] = text
        } else {
            return null
        }
    }
    return result
}

function dump_reference(node, tagName) {
    var style = node.style && window.getComputedStyle(node)
    if (style && style.display === 'none') {
        return null
    } else if (tagName) {
        var position = node.getBoundingClientRect()
        var result = {
            'content': {
                'position': [
                    position.left + parseInt(style.borderLeftWidth) + parseInt(style.paddingLeft),
                    position.top + parseInt(style.borderTopWidth) + parseInt(style.paddingTop)
                ],
                'size': [
                    position.width
                        - parseInt(style.borderLeftWidth) - parseInt(style.borderRightWidth)
                        - parseInt(style.paddingLeft) - parseInt(style.paddingRight),
                    position.height
                        - parseInt(style.borderTopWidth) - parseInt(style.borderBottomWidth)
                        - parseInt(style.paddingTop) - parseInt(style.paddingBottom)
                ]
            },
            'padding': [
                parseInt(style.paddingTop),
                parseInt(style.paddingRight),
                parseInt(style.paddingBottom),
                parseInt(style.paddingRight)
            ],
            'padding_box': {
                'position': [
                    position.left + parseInt(style.borderLeftWidth),
                    position.top + parseInt(style.borderTopWidth)
                ],
                'size': [
                    position.width - parseInt(style.borderLeftWidth) - parseInt(style.borderRightWidth),
                    position.height - parseInt(style.borderTopWidth) - parseInt(style.borderBottomWidth)
                ]
            },
            'border': [
                parseInt(style.borderTopWidth),
                parseInt(style.borderRightWidth),
                parseInt(style.borderBottomWidth),
                parseInt(style.borderRightWidth)
            ],
            'border_box': {
                'position': [position.left, position.top],
                'size': [position.width, position.height]
            },
            // 'margin': [
            //     parseInt(style.marginTop),
            //     parseInt(style.marginRight),
            //     parseInt(style.marginBottom),
            //     parseInt(style.marginRight)
            // ],
            // 'margin_box': {
            //     'position': [
            //         position.left - parseInt(style.marginLeft),
            //         position.top - parseInt(style.marginTop)
            //     ],
            //     'size': [
            //         position.width + parseInt(style.marginLeft) + parseInt(style.marginRight),
            //         position.height + parseInt(style.marginTop) + parseInt(style.marginBottom)
            //     ]
            // },
            'tag': node.tagName.toLowerCase(),
            'id': node.id
        }
        // If this is a node that has a single (non-ignorable) text child,
        // include the text for debugging purposes.
        if (node.childNodes.length == 1 && !node.childNodes[0].tagName) {
            var textContent = node.childNodes[0].textContent.trim()
            if (textContent !== '') {
                result['text'] = textContent
            }
        }

        if (node.childNodes.length > 0) {
            result['children'] = []
            var prevChild = null
            var parent, child, content, reference
            for (var i = 0; i < node.childNodes.length; i++) {
                child = node.childNodes[i]
                parent = child.parentNode
                // If the child has a tagName, it's a Node;
                // process it as normal.
                // Otherwise, it's a text element. If it's the only
                // child of the parent, or if the content is ignorable,
                // do nothing; otherwise, wrap the text in a span
                // to evaluate it's size.
                if (child.tagName) {
                    reference = dump_reference(child, child.tagName)
                } else if (parent.childNodes.length > 1
                            && child.textContent.trim() !== '') {
                    content = document.createElement('span')
                    // Make sure the style on the temporary
                    // span element is reset
                    content.style.margin = 0
                    content.style.border = 0
                    content.style.padding = 0
                    content.style.display = 'inline'
                    content.style.position = 'static'

                    // Add the text node to the child
                    content.append(child)

                    // Add the temporary element back into the document
                    if (prevChild) {
                        prevChild.after(content)
                    } else {
                        parent.prepend(content)
                    }

                    reference = dump_reference(content)
                } else {
                    reference = null
                }

                if (reference) {
                    result['children'].push(reference)
                }
                prevChild = child
            }
        }
    } else {
        var position = node.getBoundingClientRect()
        result = {
            'text': node.textContent,
            'size': [position.width, position.height]
        }
    }
    return result
}

/*******************************************************
 * Mainline
 *******************************************************/

// Evaluating the reference will modify the document, so
// evaluate the test case first.
var test_case = dump_test_case(document.body)
var reference = dump_reference(document.body, document.body.tagName)

var result = {
    'help': [],
    'test_case': test_case,
    'reference': reference
}

// Read the document metadata, looking for key elements:
//   <link rel='match' href="A test file that shows passing content">
//   <link ref='help' href="The URL of the relevant sections of the spec">
//   <meta name='assert' content='The description of what the test asserts'
for (var n = 0; n < document.head.childElementCount; n++) {
    var node = document.head.children[n]
    if (node.tagName.toLowerCase() === 'link' && node.getAttribute('rel') === 'match') {
        result.matches = node.getAttribute('href')
    } else if (node.tagName.toLowerCase() === 'link' && node.getAttribute('rel') === 'help') {
        result.help.push(node.getAttribute('href'))
    } else if (node.tagName.toLowerCase() === 'meta' && node.getAttribute('name') === 'assert') {
        result.assert = node.getAttribute('content')
    }
}

JSON.stringify(result)