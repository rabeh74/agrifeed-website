/**
 * Arabic Number Input Handler
 * Automatically converts Arabic numerals (٠-٩) to English numerals (0-9)
 */

(function() {
    'use strict';

    // Arabic to English number mapping
    const arabicToEnglish = {
        '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4',
        '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9'
    };

    // Convert Arabic numbers to English
    function convertArabicToEnglish(text) {
        if (!text) return text;
        return text.split('').map(char => arabicToEnglish[char] || char).join('');
    }

    // Handle input on number fields and text fields that expect numbers
    function handleNumberInput(event) {
        const input = event.target;
        const originalValue = input.value;
        const convertedValue = convertArabicToEnglish(originalValue);
        
        if (originalValue !== convertedValue) {
            // Store cursor position
            const cursorPos = input.selectionStart;
            
            // Update value
            input.value = convertedValue;
            
            // Restore cursor position
            input.setSelectionRange(cursorPos, cursorPos);
            
            // Trigger change event if needed
            input.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }

    // Initialize on DOM ready
    function initialize() {
        // Target ALL number and text inputs that might contain numbers
        const numberInputs = document.querySelectorAll(
            'input[type="number"], input[type="tel"], input[type="text"]'
        );

        numberInputs.forEach(input => {
            // Add event listeners
            input.addEventListener('input', handleNumberInput);
            input.addEventListener('keyup', handleNumberInput);
            input.addEventListener('paste', function(e) {
                setTimeout(() => handleNumberInput(e), 10);
            });
            
            // Mark as initialized to avoid duplicate listeners
            input.dataset.arabicConverterInitialized = 'true';
        });

        console.log(`Arabic number converter initialized for ${numberInputs.length} inputs`);
    }

    // Run on page load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initialize);
    } else {
        initialize();
    }

    // Re-initialize for dynamically added inputs
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            mutation.addedNodes.forEach(function(node) {
                if (node.nodeType === 1) { // Element node
                    // Check if the node itself is an input
                    if (node.tagName === 'INPUT' && 
                        (node.type === 'number' || node.type === 'tel' || node.type === 'text') &&
                        !node.dataset.arabicConverterInitialized) {
                        node.addEventListener('input', handleNumberInput);
                        node.addEventListener('keyup', handleNumberInput);
                        node.addEventListener('paste', function(e) {
                            setTimeout(() => handleNumberInput(e), 10);
                        });
                        node.dataset.arabicConverterInitialized = 'true';
                    }
                    
                    // Check for inputs within the added node
                    const inputs = node.querySelectorAll 
                        ? node.querySelectorAll('input[type="number"], input[type="tel"], input[type="text"]')
                        : [];
                    
                    inputs.forEach(input => {
                        if (!input.dataset.arabicConverterInitialized) {
                            input.addEventListener('input', handleNumberInput);
                            input.addEventListener('keyup', handleNumberInput);
                            input.addEventListener('paste', function(e) {
                                setTimeout(() => handleNumberInput(e), 10);
                            });
                            input.dataset.arabicConverterInitialized = 'true';
                        }
                    });
                }
            });
        });
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });

})();

