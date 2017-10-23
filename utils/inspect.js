function dump_test_case(node) {
    var result = {
        'tag': node.tagName,
        'style': {}
    }

    if (node.tagName) {
        var styleNames = [
            // 8. Box model #######################################################
            // 8.3 Margin properties
            'margin-top',
            'margin-right',
            'margin-bottom',
            'margin-left',

            // 8.4 Padding properties
            'padding-top',
            'padding-right',
            'padding-bottom',
            'padding-left',

            // 8.5 Border properties
            // 8.5.1 Border width
            'border-top-width',
            'border-right-width',
            'border-bottom-width',
            'border-left-width',

            // 8.5.2 Border color
            'border-top-color',
            'border-right-color',
            'border-bottom-color',
            'border-left-color',

            // 8.5.3 Border style
            'border-top-style',
            'border-right-style',
            'border-bottom-style',
            'border-left-style',

            // 9. Visual formatting model #########################################
            // 9.2.4 The display property
            'display',
            // 9.3 Positioning schemes
            'position',

            // 9.3.2 Box offsets
            'top',
            'bottom',
            'left',
            'right',

            // 9.5.1 Positioning the float
            'float',
            // 9.5.2 Controlling flow next to floats
            'clear',

            // 9.9 Layered Presentation
            'z-index',

            // 9.10 Text Direction
            'direction',
            'unicode-bidi',

            // 10. Visual formatting model details ################################
            // 10.2 Content width
            'width',

            // 10.4 Minimum and maximum width
            'min-width',
            'max-width',

            // 10.5 Content height
            'height',

            // 10.7 Minimum and maximum heights
            'min-height',
            'max-height',

            // 10.8 Leading and half-leading
            'line-height',
            'vertical-align',

            // 11. Visual effects #################################################
            // 11.1.1 Overflow
            'overflow',

            // 11.1.2 Clip
            'clip',

            // 11.2 Visibility
            'visibility',

            // 12. Visual effects #################################################
            // 12.2 The content property
            'content',

            // 12.3 Quotation marks
            'quotes',

            // 12.4 Automatic counters and numbering
            'counter-reset',
            'counter-increment',

            // 12.5 Lists
            'list-style-type',
            'list-style-image',
            'list-style-position',

            // 13. Paged media ####################################################
            // 13.3.1 Page break properties
            'page-break-before',
            'page-break-after',
            'page-break-inside',

            // 13.3.2 Breaks inside elements
            'orphans',
            'widows',

            // 14. Colors and backgrounds #########################################
            // 14.1 Foreground color
            'color',

            // 14.2.1 Background properties
            'background-color',
            'background-image',
            'background-repeat',
            'background-attachment',
            'background-position',

            // 15. Fonts ##########################################################
            // 15.3 Font family
            'font-family',

            // 15.4 Font Styling
            'font-style',

            // 15.5 Small-caps
            'font-variant',

            // 15.6 Font boldness
            'font-weight',

            // 15.7 Font size
            'font-size',

            // 16. Text ###########################################################
            // 16.1 Indentation
            'text-indent',

            // 16.2 Alignment
            'text-align',

            // 16.3 Decoration
            // 'text-decoration',

            // 16.4 Letter and word spacing
            'letter-spacing',
            'word-spacing',

            // 16.5 Capitalization
            'text-transform',

            // 16.6 White space
            'white-space',

            // 17. Tables #########################################################
            // 17.4.1 Caption position and alignment
            'caption-side',

            // 17.5.2 Table width algorithms
            'table-layout',

            // 17.6 Borders
            'border-collapse',
            'border-spacing',
            'empty-cells',

            // 18. User interface #################################################
            // 18.1 Cursors
            'cursor',

            // 18.4 Dynamic outlines
            'outline-width',
            'outline-style',
            'outline-color',

            // #####################################################################
            //  Flexbox properties
            // #####################################################################
            //  5. Ordering and orientation ########################################
            //  5.1 Flex flow direction

            'flex-direction',

            // 5.2 Flex line wrapping
            'flex-wrap',

            // 5.4 Display order
            'order',

            // 7. Flexibility #####################################################
            // 7.2 Components of flexibility
            'flex-grow',
            'flex-shrink',
            'flex-basis',

            // 8. Alignment #######################################################
            // 8.2 Axis alignment
            'justify-content',

            // 8.3 Cros-axis alignment
            'align-items',
            'align-self',

            // 8.4 Packing flex lines
            'align-content',

            // #####################################################################
            //  Grid properties
            // #####################################################################
            //  7. Defining the grid ###############################################
            //  7.2 Explicit track sizing
            'grid-template-columns',
            'grid-template-rows',

            //  7.3 Named Areas
            'grid-template-areas',

            //  7.6 Implicit track sizing
            'grid-auto-columns',
            'grid-auto-rows',

            //  7.7 Automatic placement
            'grid-auto-flow',

            //  8. Placing grid items ##############################################
            //  8.3 Line-based placement
            'grid-row-start',
            'grid-column-start',
            'grid-row-end',
            'grid-column-end',

            //  10. Alignment and spacing ##########################################
            //  10.1 Gutters
            'grid-row-gap',
            'grid-column-gap'
        ]

        var defaultStyles = {
            "html, address, blockquote, body, dd, div, dl, dt, fieldset, form,\
                    frame, frameset, h1, h2, h3, h4, h5, h6, noframes, ol, p,\
                    ul, center, dir, hr, menu, pre": {
                'display': 'block',
                'unicode_bidi': 'embed'
            },
            "li": {
                'display': 'list-item'
            },
            "head": {
                'display': 'none'
            },
            "table": {
                'display': 'table'
            },
            "tr": {
                'display': 'table-row'
            },
            "thead": {
                'display': 'table-header-group'
            },
            "tbody": {
                'display': 'table-row-group'
            },
            "tfoot": {
                'display': 'table-footer-group'
            },
            "col": {
                'display': 'table-column'
            },
            "colgroup": {
                'display': 'table-column-group'
            },
            "td, th": {
                'display': 'table-cell'
            },
            "caption": {
                'display': 'table-caption'
            },
            "th": {
                'font_weight': 'bolder',
                'text_align': 'center'
            },
            "caption": {
                'text_align': 'center'
            },
            "body": {
                'margin_top': '8px',
                'margin_right': '8px',
                'margin_bottom': '8px',
                'margin_left': '8px'
            },
            "h1": {
                'font_size': '2em',
                'margin_top': '.67em',
                'margin_right': '0',
                'margin_bottom': '.67em',
                'margin_left': '0'
            },
            "h2": {
                'font_size': '1.5em',
                'margin_top': '.75em',
                'margin_right': '0',
                'margin_bottom': '.75em',
                'margin_left': '0'
            },
            "h3": {
                'font_size': '1.17em',
                'margin_top': '.83em',
                'margin_right': '0',
                'margin_bottom': '.83em',
                'margin_left': '0'
            },
            "h4, p, blockquote, ul, fieldset, form, ol, dl, dir, menu": {
                'margin_top': '1.12em',
                'margin_right': '0',
                'margin_bottom': '1.12em',
                'margin_left': '0'
            },
            "h5": {
                'font_size': '.83em',
                'margin_top': '1.5em',
                'margin_right': '0',
                'margin_bottom': '1.5em',
                'margin_left': '0'
            },
            "h6": {
                'font_size': '.75em',
                'margin_top': '1.67em',
                'margin_right': '0',
                'margin_bottom': '1.67em',
                'margin_left': '0'
            },
            "h1, h2, h3, h4, h5, h6, b, strong": {
                'font_weight': 'bolder'
            },
            "blockquote": {
                'margin_left': '40px',
                'margin_right': '40px'
            },
            "i, cite, em, var, address": {
                'font_style': 'italic'
            },
            "pre, tt, code, kbd, samp": {
               'font_family': 'monospace'
            },
            "pre": {
                'white_space': 'pre'
            },
            "button, textarea, input, select": {
                'display': 'inline-block'
            },
            "big": {
                'font_size': '1.17em'
            },
            "small, sub, sup": {
                'font_size': '.83em'
            },
            "sub": {
                'vertical_align': 'sub'
            },
            "sup": {
                'vertical_align': 'super'
            },
            "table": {
                'border_spacing': '2px'
            },
            "thead, tbody, tfoot": {
                'vertical_align': 'middle'
            },
            "td, th, tr": {
                'vertical_align': 'inherit'
            },
            "s, strike, del": {
                'text_decoration': 'line-through'
            },
            "hr": {
                'border': '1px inset'
            },
            "ol, ul, dir, menu, dd": {
                'margin_left': '40px'
            },
            "ol": {
                'list_style_type': 'decimal'
            },
            "ol ul, ul ol, ul ul, ol ol": {
                'margin_top': '0',
                'margin_bottom': '0'
            },
            "u, ins": {
                'text_decoration': 'underline'
            },
            "br:before": {
                'content': "\A",
                'white_space': 'pre-line'
            },
            "center": {
                'text_align': 'center'
            },
            ":link, :visited": {
                'text_decoration': 'underline'
            },
        }

        // Apply default stylesheet
        var selector, ss, st, rule, styles
        for (selector in defaultStyles) {
            if (node.matches(selector)) {
                for (st in defaultStyles[selector]) {
                    result['style'][st] = defaultStyles[selector][st]
                }
            }
        }

        // Apply the stylesheets to the element
        for (ss = 0; ss < document.styleSheets.length; ss++) {
            for (rule = 0; rule < document.styleSheets[ss].rules.length; rule++) {
                selector = document.styleSheets[ss].rules[rule].selectorText
                if (selector) {
                    if (selector.startsWith('@') || node.matches(selector)) {
                        styles = document.styleSheets[ss].rules[rule].style
                        for (st = 0; st < styles.length; st++) {
                            result['style'][styles[st].replace(/-/g, '_')] = styles[styles[st]]
                        }
                    }
                }
            }
        }

        // Apply all styles that have been explicitly set on the element
        for (st in styleNames) {
            if (node.style[st] !== '') {
                result['style'][st.replace(/-/g, '_')] = node.style[st]
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

try {
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

} catch (err) {
    err.message
}
