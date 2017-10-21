// Remove any assistance text in the test case itself.
// Assistance text is content that:
// * is in the first element of the body,
// * when the element is a <p>
// * where the text content contains certain magic words.
// * and the document contains elements other than the <p>
if (document.body.childElementCount > 1) {
    if (document.body.children[0].tagName
            && document.body.children[0].tagName.toUpperCase() === 'P') {
        condition = document.body.children[0].textContent
        if (condition && condition.indexOf('passes') != -1
            || condition.indexOf('should') != -1
            || condition.indexOf('must') != -1
        ) {
            document.body.children[0].remove()
        }
    }
}
