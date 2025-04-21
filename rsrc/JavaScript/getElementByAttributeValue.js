// !! code snippet made by hamzaaitbrik @ GitHub !!



(() => {

    const matchedElements = [];

    function traverse(node) {

        // Check if the node is an element node and has the specified href
        if (node.nodeType === Node.ELEMENT_NODE && node.tagName === 'TAGNAME') {

            if (node.getAttribute('ATTRIBUTE') === 'VALUE') {

                matchedElements.push(node);

            }

        }

        // If the node is a shadow host, traverse its shadow root
        if (node.shadowRoot) {

            traverse(node.shadowRoot);

        }

        // Recursively traverse child nodes
        node.childNodes.forEach(child => traverse(child));

    }

    // Start traversing from the document body
    traverse(document.body);

    const targetElement = matchedElements[0];

    return targetElement;

})();