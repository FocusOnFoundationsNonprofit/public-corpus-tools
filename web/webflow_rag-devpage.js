var fileInfo = "webflow_rag-devpage.js    7-28 1628 adding diplayType";

const buttonParamsMapping = {
    'submitButton_rag-devpage_qrag': { 
        displayType: 'quoted-qa-then-ai-answer',
        ragFunction: 'qragRouting, qragLLM', 
        vector_index_name: 'deutsch-transcript-qrag', 
        route_dict_name: 'ROUTES_DICT_DEUTSCH_V3'
    },
    'submitButton_rag-devpage_vrag': { 
        displayType: 'ai-answer-only',
        ragFunction: 'vragLLM', 
        vector_index_name: 'dd-transcripts-vrag-80f-20240727'
    }
};

document.addEventListener("DOMContentLoaded", function() {
    console.log('JavaScript file loaded: ' + fileInfo);

    initializeDynamicIdAssignments();
    addClassStyles();

    document.querySelectorAll('[id^="inputText_"], [id^="submitButton_"]').forEach(element => {
        if (element.tagName.toLowerCase() === 'textarea') {
            element.addEventListener('keydown', function(event) {
                if (event.key === 'Enter' && !event.shiftKey) {
                    event.preventDefault(); // Prevent the default newline behavior
                    const trailingId = getElementIDTrailingString(element.id);
                    const buttonId = `submitButton_${trailingId}`;
                    const buttonElement = document.getElementById(buttonId);
                    if (buttonElement) {
                        console.log('Enter pressed, triggering button click for:', buttonId);
                        buttonElement.click(); // Trigger the button click associated with this textarea
                    } else {
                        console.error('Button not found for ID:', buttonId);
                    }
                }
            });
        } else if (element.tagName.toLowerCase() === 'button') {
            element.addEventListener('click', function(event) {
                console.log(`Click event on element with ID ${event.target.id}`);
                console.log(`Event currentTarget ID: ${event.currentTarget.id}`);
                try {
                    submitInputRag(event); // Pass the event directly
                } catch (error) {
                    console.error('Error in submitInputRag:', error);
                }
            });
        }
    });
});


////// DYNAMIC ELEMENT ID ASSIGNMENTS
function initializeDynamicIdAssignments() {
    const botContainers = document.querySelectorAll('.w-layout-blockcontainer.bot-container.w-container'); // Use a class that wraps your bot containers

    botContainers.forEach((botContainer) => {
        // Print the ID of each container to the console
        console.log(`Selected Container ID: ${botContainer.id}`);
        assignTextSubmissionComponentIds(botContainer);
        // Add calls to other ID assignment functions for different components here if needed
    });
}

// Adjusts the textarea height based on its content with configurable max rows and line height
function adjustTextareaHeight(textarea, maxRows, lineHeight) {
    textarea.style.height = ''; // Reset height to shrink if text is deleted
    const scrollHeight = textarea.scrollHeight;
    const maxHeight = lineHeight * maxRows;
    if (scrollHeight > maxHeight) {
        textarea.style.height = maxHeight + 'px';
        textarea.style.overflowY = 'auto'; // Enable scrolling
    } else {
        textarea.style.height = scrollHeight + 'px';
        textarea.style.overflowY = 'hidden'; // Hide scrollbar when not needed
    }
}

// Helper function to assign IDs to text submission components including the icon within the button and an error display element
function assignTextSubmissionComponentIds(botContainer) {
    const textarea = botContainer.querySelector('.botsubmit-textarea');  // access by class
    const button = botContainer.querySelector('button.primary-button.w-button');  // access by type and class because at start when initialized it is the only button
    const icon = button.querySelector('span.material-symbols-rounded');  // access by type and class
    const error = botContainer.querySelector('.botsubmit-error');  // access by class in case want other text in p elements

    const trailingIdString = getElementIDTrailingString(botContainer.id);

    if (trailingIdString) {
        textarea.id = `inputText_${trailingIdString}`;
        button.id = `submitButton_${trailingIdString}`;
        icon.id = `submitIcon_${trailingIdString}`;
        error.id = `submitError_${trailingIdString}`;

        console.log(`  - Assigned textarea ID: ${textarea.id}`);
        console.log(`  - Assigned button ID: ${button.id}`);
        console.log(`  - Assigned icon ID: ${icon.id}`);
        console.log(`  - Assigned error ID: ${error.id}`);

        // Add event listener for resizing the textarea
        textarea.addEventListener('input', function() {
            adjustTextareaHeight(textarea, 8, 20);  // call with maxRows=8 and lineHeight=20
        });

        // Validate the newly assigned button ID
        validateButtonIdInParamsMapping(button.id);
    } else {
        console.error('Failed to get trailing ID string for:', botContainer);
    }
}

function validateButtonIdInParamsMapping(buttonId) {
    const validButtonIds = Object.keys(buttonParamsMapping);
    // console.log(`DEBUG Validating button ID by looking for '${buttonId}' in list from mapping:`, validButtonIds);
    if (!buttonParamsMapping.hasOwnProperty(buttonId)) {
        const trailingId = getElementIDTrailingString(buttonId);
        const errorId = `submitError_${trailingId}`;
        const errorContainer = document.getElementById(errorId);
        if (errorContainer) {
            errorContainer.style.display = 'block';
            errorContainer.innerHTML = `This functionality is disabled - contact support at our domain for assistance.`;
            console.error(`Configuration Error: No parameters found for dynamically generated button ID: ${buttonId}`);
        } else {
            console.error(`Error display element not found for ID: ${errorId}`);
        }
    } else {
        const ragFunctionNames = buttonParamsMapping[buttonId].ragFunction.split(',').map(func => func.trim());
        const allFunctionsExist = ragFunctionNames.every(funcName => typeof window[funcName] === 'function');
        const allFunctionsValid = ragFunctionNames.every(funcName => funcName !== '');

        if (allFunctionsExist && allFunctionsValid) {
            console.log(`Validation of button ID passes for ${buttonId} found in buttonParamsMapping, all rag functions are valid.`);
        } else {
            console.error(`Mapping Validation Error: One or more functions specified for ${buttonId} do not exist or are empty.`);
        }
    }
}

// Utility function to get trailing string from an element ID after the first underscore
function getElementIDTrailingString(elementId) {
    const underscoreIndex = elementId.indexOf('_');
    if (underscoreIndex === -1 || underscoreIndex === elementId.length - 1) {
        console.error('Invalid element ID format:', elementId);
        return null;
    }
    return elementId.substring(underscoreIndex + 1);
}


////// CORE FUNCTIONS
function getBotContainerFromSubmitButtonId(submitButtonId) {
    // Use dynamically assigned ID to access the bot container directly
    const trailingIdString = getElementIDTrailingString(submitButtonId);
    return document.getElementById(`container_${trailingIdString}`);
}

function submitInputRag(event) {
    event.preventDefault(); // Prevent default form submission
    const submitButtonId = event.currentTarget.id; // Use currentTarget which is the button because target is the icon if that's clicked
    const trailingId = getElementIDTrailingString(submitButtonId);
    const userInputId = `inputText_${trailingId}`;
    const submitIconId = `submitIcon_${trailingId}`;

    var valueUserInput = document.getElementById(userInputId).value;
    console.log("User Input Value:", valueUserInput);
    if (!valueUserInput) {
        console.error("User input is empty or undefined.");
        return;
    }

    // Change button text and color to indicate processing
    var submitButton = document.getElementById(submitButtonId);
    var submitIcon = document.getElementById(submitIconId);
    setButtonToStopState(submitButton, submitIcon);

    // Determine which RAG function(s) to call based on the button ID
    const params = buttonParamsMapping[submitButtonId];
    const ragFunctions = params.ragFunction.split(',').map(func => func.trim());
    const numberOfRagFunctions = ragFunctions.length;
    console.log("Number of RAG Functions:", numberOfRagFunctions, "RAG Functions:", ragFunctions);

    // For VRAG (ai-answer-only), create an initial accordion item with waiting message
    if (params.displayType === 'ai-answer-only') {
        const initialJsonData = {
            content: {
                user_question: valueUserInput,
                ai_answer: "WAITING FOR AI ANSWER..."
            }
        };
        createAccordionItem(initialJsonData, submitButtonId);
    }

    // Call the first RAG function dynamically
    const firstRagFunction = ragFunctions[0];
    window[firstRagFunction](valueUserInput, params.vector_index_name, params.route_dict_name)
    .then(firstJsonData => {
        console.log("submitInputRag - Received firstRagFunction json data:", firstJsonData);
        if (params.displayType === 'quoted-qa-then-ai-answer') {
            createAccordionItem(firstJsonData, submitButtonId);
        }

        if (numberOfRagFunctions === 2) {
            const secondRagFunction = ragFunctions[1];
            return window[secondRagFunction](firstJsonData);
        } else {
            return firstJsonData; // For VRAG, we only have one function call
        }
    })
    .then(finalJsonData => {
        console.log("submitInputRag - Received final json data:", finalJsonData);
        if (params.displayType === 'ai-answer-only') {
            replaceAccordionItem(finalJsonData, submitButtonId);
        } else {
            replaceAccordionItem(finalJsonData, submitButtonId);
        }
    })
    .catch(error => {
        console.error('submitInputRag - Fetch error:', error);
    })
    .finally(() => {
        resetButtonToInitialState(submitButton, submitIcon);
        const userInputField = document.getElementById(userInputId);

        // Reset the input field and button to initial state
        userInputField.value = ''; // Clear input field after sending
        
        // Temporarily reset the textarea height to a single line
        adjustTextareaHeight(userInputField, 1, 20);

        // Ensure the textarea can expand again on user input
        userInputField.style.height = ''; // Clear any inline height style
        adjustTextareaHeight(userInputField, 8, 20); // Reapply the initial maxRows setting
    });
}

// returns the routing json data if api call returns success
function qragRouting(userInput, vector_index_name, route_dict_name) {
    console.log("qrag-routing - Calling Lambda function with userInput:", userInput);
    console.log("   route_dict_name:", route_dict_name, "vector_index_name:", vector_index_name);
    return fetch('https://us05oglu51.execute-api.us-west-2.amazonaws.com/api/qrag-routing', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ 
            user_question: userInput, 
            vector_index_name: vector_index_name , 
            route_dict_name: route_dict_name
        })
    })
    .then(httpResponse => {  // Clearly indicates this is the HTTP response object
        if (!httpResponse.ok) {
            throw new Error(`qrag-routing - HTTP error! status: ${httpResponse.status}`);
        }
        return httpResponse.json();  // Parse JSON from the HTTP response
    })
    .then(apiResponse => {  // This is the full API response including status and data
        console.log("qrag-routing - Received API Response:", apiResponse);
        if (!apiResponse.response) {
            throw new Error('qrag-routing - No data in API Response');
        }
        return apiResponse.response;  // return the json data in the response field of apiResponse
    });
}

// returns the complete json data if api call returns success
function qragLLM(routingJsonData) {
    console.log("qrag-llm - Calling Lambda function with routing JSON data:", routingJsonData);
    return fetch('https://sz901mb96d.execute-api.us-west-2.amazonaws.com/api/qrag-llm', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(routingJsonData)
    })
    .then(httpResponse => {
        console.log("qrag-llm - HTTP response status:", httpResponse.status); // Log HTTP response status
        if (!httpResponse.ok) {
            throw new Error(`qrag-llm - HTTP error! status: ${httpResponse.status}`);
        }
        return httpResponse.json();  // Parse JSON from the HTTP response
    })
    .then(apiResponse => {
        console.log("qrag-llm - Received API Response:", apiResponse); // Log the full API response
        if (!apiResponse.response) {
            throw new Error('qrag-llm - No data in API Response');
        }
        return apiResponse.response;  // Return the json data in the response field of apiResponse
    });
}

function vragLLM(userInput, vector_index_name) {
    console.log("vrag-llm - Calling Lambda function with userInput:", userInput, "vector_index_name:", vector_index_name);
    return fetch('https://n5yjgn8jak.execute-api.us-west-2.amazonaws.com/api/vrag-llm', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ 
            user_question: userInput,
            vector_index_name: vector_index_name 
        })
    })
    .then(httpResponse => {  // Clearly indicates this is the HTTP response object
        if (!httpResponse.ok) {
            throw new Error(`vrag-routing - HTTP error! status: ${httpResponse.status}`);
        }
        return httpResponse.json();  // Parse JSON from the HTTP response
    })
    .then(apiResponse => {  // This is the full API response including status and data
        console.log("vrag-routing - Received API Response:", apiResponse);
        if (!apiResponse.response) {
            throw new Error('vrag-routing - No data in API Response');
        }
        return apiResponse.response;  // return the json data in the response field of apiResponse
    });
}

function generateDropdownContent(jsonData, displayType) {
    let dropdownContent = '';
    if (displayType === 'ai-answer-only') {
        if (jsonData.content.ai_answer === "WAITING FOR AI ANSWER...") {
            dropdownContent += `<div class="accordion-dropdown-text" style="color: red; font-style: italic;">WAITING FOR AI ANSWER...</div>`;
        } else {
            dropdownContent += `<div class="accordion-dropdown-text" style="color: red;">AI ANSWER:<br>${simpleMarkdownToHtml(jsonData.content.ai_answer)}</div>`;
        }
    } else if (displayType === 'quoted-qa-then-ai-answer') {
        if (jsonData.content.route_preamble) {
            dropdownContent += `<div class="accordion-dropdown-text">${simpleMarkdownToHtml(jsonData.content.route_preamble)}</div>`;
        }
        if (jsonData.content.quoted_qa) {
            dropdownContent += `<div class="accordion-dropdown-text">${simpleMarkdownToHtml(jsonData.content.quoted_qa)}</div>`;
        }
        if (jsonData.content.ai_answer && jsonData.content.ai_answer !== "WAITING FOR AI ANSWER...") {
            dropdownContent += `<div class="accordion-dropdown-text" style="color: red;">AI ANSWER:<br>${simpleMarkdownToHtml(jsonData.content.ai_answer)}</div>`;
        } else {
            dropdownContent += `<div class="accordion-dropdown-text" style="color: red; font-style: italic;">WAITING FOR AI ANSWER...</div>`;
        }
    }
    return dropdownContent;
}

function createAccordionItem(jsonData, submitButtonId) {
    // Check for necessary elements exist and if not throw error
    if (!checkBotElementsExist(submitButtonId)) {
        throw new Error("createAccordionItem - Required elements not found.");
    }

    const botContainer = getBotContainerFromSubmitButtonId(submitButtonId);
    
    // Check if the hidden-div already exists in the botContainer, if not, create the Hidden Div and Share Elements
    if (!botContainer.querySelector('.hidden-div')) {
        createHiddenDivAndShareElements(botContainer);
    }
    
    const accordionCard = botContainer.querySelector('.accordion-card');

    // Create the accordion item container
    var accordionItem = document.createElement('div');
    accordionItem.className = 'accordion-item w-dropdown';

    // Create the accordion toggle
    var accordionToggle = document.createElement('div');
    accordionToggle.className = 'accordion-toggle w-dropdown-toggle';

    // Set the title text using 'user_question' from jsonData and apply text clamping
    const user_question = jsonData.content.user_question.replace(/\n/g, '<br>');
    accordionToggle.innerHTML = `
        <div class="accordion-icon w-icon-dropdown-toggle"></div>
        <div class="accordion-title-text">${user_question}</div>
    `;
    
    const params = buttonParamsMapping[submitButtonId];
    const displayType = params.displayType;

    var dropdownList = document.createElement('nav');
    dropdownList.className = 'accordion-dropdown-list w-dropdown-list';
    dropdownList.style.display = 'block'; // Start visible

    dropdownList.innerHTML = generateDropdownContent(jsonData, displayType);

    // Convert JSON response to Markdown and append to the top of the hidden div with deleteTopHeadingFlag set to false
    writeMarkdownToHiddenDiv(jsonData, botContainer, false);

    // Add toggle event
    accordionToggle.addEventListener('click', function () {
        var isCollapsed = dropdownList.style.display === 'none';
        dropdownList.style.display = isCollapsed ? 'block' : 'none';

        // Toggle icon rotation
        var icon = accordionToggle.querySelector('.accordion-icon');
        icon.style.transform = isCollapsed ? 'rotate(0deg)' : 'rotate(-90deg)';
    });

    // Append the toggle and dropdown to the accordion item
    accordionItem.appendChild(accordionToggle);
    accordionItem.appendChild(dropdownList);

    accordionCard.insertBefore(accordionItem, accordionCard.firstChild);
}

function replaceAccordionItem(jsonData, submitButtonId) {
    // Check for necessary elements exist and if not throw error
    if (!checkBotElementsExist(submitButtonId)) {
        throw new Error("replaceAccordionItem - Required elements not found.");
    }

    const botContainer = getBotContainerFromSubmitButtonId(submitButtonId);

    let accordionCard = botContainer.querySelector('.accordion-card');
    if (!accordionCard) {
        console.error("replaceAccordionItem - Accordion card not found.");
        return;
    }

    // Find the first accordion item to update - this method will always return the topmost one in the DOM
    let accordionItem = accordionCard.querySelector('.accordion-item');
    if (!accordionItem) {
        console.error("replaceAccordionItem - Accordion item not found.");
        return;
    }

    const accordionTitleText = accordionItem.querySelector('.accordion-title-text');
    const user_question = jsonData.content.user_question.replace(/\n/g, '<br>');
    accordionTitleText.innerHTML = user_question;

    const params = buttonParamsMapping[submitButtonId];
    const displayType = params.displayType;

    const dropdownList = accordionItem.querySelector('.accordion-dropdown-list');
    dropdownList.innerHTML = generateDropdownContent(jsonData, displayType);

    // Convert JSON response to Markdown and append to the hidden div with deletion of the top heading
    writeMarkdownToHiddenDiv(jsonData, botContainer, true);
}

function createHiddenDivAndShareElements(botContainer) {
    console.log('Creating hidden div and download button');
    
    // Get the bot title text and process it
    let botTitleTextElement = botContainer.querySelector('.bot-title-text');
    let botTitleText = botTitleTextElement.textContent;
    // Strip the last character if it's a colon
    if (botTitleText.endsWith(':')) {
        botTitleText = botTitleText.slice(0, -1);
    }

    // Create a hidden div
    let hiddenDiv = document.createElement('div');
    hiddenDiv.className = 'hidden-div';
    hiddenDiv.style.display = 'none';
    hiddenDiv.textContent = `${botTitleText}\nby Randy True of focusonfoundations.org`;

    // Create download and email buttons
    let downloadButton = createIconButton('download', 'material-symbols-rounded', () => downloadMarkdown(botContainer));
    let emailButton = createIconButton('mail', 'material-symbols-rounded', () => toggleEmailInputAndCheckboxVisibility(emailButton));
    
    console.log('createHiddenDivAndShareElements - Hidden div, download button, and email button created and event listener added');
    // Create an input text block for email address
    let emailInput = createInput('email', 'Enter your email address here', 'email-input-address');
    emailInput.style.display = 'none';
    emailInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent the default action to stop form submission
            sendEmail(event); // Call the sendEmail function
        }
    });

    // Create a checkbox for "add me to the email list for updates to this project"
    let emailCheckboxContainer = createCheckboxWithLabel('Add me to the email list for updates to this project.');

    // Create a block for download, email button, email input, and checkbox with label
    let shareDiv = document.createElement('div');
    shareDiv.className = 'share-div';
    shareDiv.appendChild(downloadButton);
    shareDiv.appendChild(emailButton);
    shareDiv.appendChild(emailInput);
    shareDiv.appendChild(emailCheckboxContainer);

    // Find the accordion container and insert the hiddenDiv and shareDiv above it
    let accordionContainer = botContainer.querySelector('.accordion-container');
    botContainer.insertBefore(hiddenDiv, accordionContainer);
    botContainer.insertBefore(shareDiv, accordionContainer);
}
 
  
////// CHILD FUNCTIONS FOR createHiddenDivAndShareElements 
function createIconButton(iconText, iconClass, eventListener) {
    let button = document.createElement('button');
    let icon = document.createElement('span');
    icon.className = iconClass;
    icon.textContent = iconText;
    button.appendChild(icon);
    button.className = 'primary-button w-button';
    styleButton(button, {marginTop: '10px', marginLeft: '20px', padding: '4px 8px', fontSize: '12px', borderRadius: '14px', cursor: 'pointer'});
    button.addEventListener('click', eventListener);
    return button;
}
  
function styleButton(button, styles) {
    Object.assign(button.style, styles);
}

function addClassStyles() {
    const style = document.createElement('style');
    document.head.appendChild(style);
    // Style for the shareDiv to use flexbox
    style.sheet.insertRule(`
        .share-div {
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: left;
        }
    `, style.sheet.cssRules.length);
    // Consolidated style for hiding elements initially
    style.sheet.insertRule(`
        .email-input-address {
            display: none;
            margin-left: 20px;
            width: 300px;
            height: 30px;
            transform: translateY(30%);
        }
    `, style.sheet.cssRules.length);
    style.sheet.insertRule(`
        .email-checkbox-container {
            display: none;
            margin-left: 20px;
            transform: translateY(60%);
    `, style.sheet.cssRules.length);
    style.sheet.insertRule(`
        .email-checkbox {
            display: inline-block;
            width: 20px;
            height: 20px;
        }
    `, style.sheet.cssRules.length);
    style.sheet.insertRule(`
        .email-checkbox-label {
            display: inline-block;
            font-size: 12px;
            margin-left: 5px;
        }
    `, style.sheet.cssRules.length);
}

function createInput(type, placeholder, className) {
    let input = document.createElement('input');
    input.type = type;
    input.placeholder = placeholder;
    input.className = className; // Assign the class name
    return input;
}
  
function createCheckboxWithLabel(labelText) {
    let container = document.createElement('div');
    container.className = 'email-checkbox-container';
    container.style.display = 'none';

    let checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.className = 'email-checkbox';

    let label = document.createElement('label');
    label.className = 'email-checkbox-label';
    label.textContent = labelText;

    container.appendChild(checkbox);
    container.appendChild(label);

    return container;
}
  
function toggleEmailInputAndCheckboxVisibility(emailButton) {
    let emailInput = emailButton.parentElement.querySelector('.email-input-address');
    let emailCheckboxContainer = emailButton.parentElement.querySelector('.email-checkbox-container');
    let displayStyle = emailInput.style.display === 'none' ? 'inline-block' : 'none';
    
    emailInput.style.display = displayStyle;
    emailCheckboxContainer.style.display = displayStyle;
}

function writeMarkdownToHiddenDiv(jsonData, botContainer, deleteTopHeadingFlag) {
    const MARKDOWN_HEADING_LEVEL = '##'; // Set the Markdown heading level to be removed if needed

    if (!botContainer) {
        console.error('writeMarkdownToHiddenDiv - Error: botContainer is null.');
        return;
    }
    var markdownContent = processJsonToMarkdown(jsonData);
    var hiddenDiv = botContainer.querySelector('.hidden-div'); // Accessing the element with class='hidden-div' using the passed botContainer
    if (!hiddenDiv) {
        console.error('writeMarkdownToHiddenDiv - Error: hiddenDiv not found within the botContainer.');
        return;
    }
    let initialText = hiddenDiv.textContent;

    // Optionally remove the top Markdown heading and content below it until the next heading of the same level
    if (deleteTopHeadingFlag) {
        const firstHeadingIndex = initialText.indexOf('\n' + MARKDOWN_HEADING_LEVEL + ' ');
        console.log('DEBUG - Next heading index:', firstHeadingIndex, 'text:', initialText.substring(firstHeadingIndex, firstHeadingIndex + 10));
            if (firstHeadingIndex !== -1) {
            let nextHeadingIndex = initialText.indexOf('\n' + MARKDOWN_HEADING_LEVEL + ' ', firstHeadingIndex + 1);
            let preHeadingText = initialText.substring(0, firstHeadingIndex); // Preserve text before the first heading
            console.log('DEBUG - Next heading index:', nextHeadingIndex, 'text:', initialText.substring(nextHeadingIndex, nextHeadingIndex + 10));
            console.log('DEBUG - Pre-heading text:', preHeadingText);
            if (nextHeadingIndex === -1) { // No next heading found, delete to the end
                initialText = preHeadingText; // Assign initialText to just the preHeadingText
            } else {
                let postHeadingText = initialText.substring(nextHeadingIndex); // Preserve text after the next heading
                console.log('DEBUG - Post-heading text:', postHeadingText);
                initialText = preHeadingText + postHeadingText; // Combine the preserved parts
            }
        }
    }
    hiddenDiv.textContent = initialText; // Update the text content of hiddenDiv
    console.log('DEBUG After deletion - Current total content of hiddenDiv:', {
        content: hiddenDiv.textContent
    });

    // Insert the new markdown content
    const firstMarkdownHeaderIndex = initialText.search(/##\s/);
    let insertionPoint;
    if (firstMarkdownHeaderIndex !== -1) {
        insertionPoint = initialText.substring(0, firstMarkdownHeaderIndex).search(/\S\s*$/) + 1;
    } else {
        insertionPoint = initialText.search(/\S\s*$/) + 1;
    }
    hiddenDiv.textContent = initialText.substring(0, insertionPoint) + markdownContent + initialText.substring(insertionPoint);
    console.log('writeMarkdownToHiddenDiv - Markdown content updated in the hidden div');
    console.log('DEBUG After insertion - Current total content of hiddenDiv:', {
        content: hiddenDiv.textContent
    });
}

function appendMarkdownToHiddenDiv(jsonData, botContainer) {
    if (!botContainer) {
        console.error('appendMarkdownToHiddenDiv - Error: botContainer is null.');
        return;
    }
    var markdownContent = processJsonToMarkdown(jsonData);
    var hiddenDiv = botContainer.querySelector('.hidden-div'); // Accessing the element with class='hidden-div' using the passed botContainer
    if (!hiddenDiv) {
        console.error('appendMarkdownToHiddenDiv - Error: hiddenDiv not found within the botContainer.');
        return;
    }
    const initialText = hiddenDiv.textContent;
    const firstMarkdownHeaderIndex = initialText.search(/##\s/);
    let insertionPoint;
    if (firstMarkdownHeaderIndex !== -1) {
        insertionPoint = initialText.substring(0, firstMarkdownHeaderIndex).search(/\S\s*$/) + 1;
    } else {
        insertionPoint = initialText.search(/\S\s*$/) + 1;
    }
    hiddenDiv.textContent = initialText.substring(0, insertionPoint) + markdownContent + initialText.substring(insertionPoint);
    console.log('appendMarkdownToHiddenDiv - Markdown content inserted at the correct position in the hidden div');
}

////// SHARE FUNCTIONS
function downloadMarkdown(botContainer) {
    // Get the markdown content from the hidden div within the specified bot container
    let hiddenDiv = botContainer.querySelector('.hidden-div');
    let markdownContent = hiddenDiv.textContent;

    // Create a Blob from the markdown content with proper encoding
    let blob = new Blob([markdownContent], { type: 'text/markdown;charset=utf-8' });

    // Create a link element
    let link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'questions_and_answers.md';

    // Programmatically click the link to trigger the download
    link.click();
}

function sendEmail(event) {
    event.preventDefault(); // Prevent default form submission
    const displayDuration = 5000;

    // Access the email input field relative to the event target (email button)
    var emailButton = event.currentTarget;
    var emailInputAddress = emailButton.parentNode.querySelector('input[type="email"]');
    var emailInputAddressValue = emailInputAddress.value;

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailInputAddressValue || !emailRegex.test(emailInputAddressValue)) {
        console.error("Invalid or empty email address.");
        displayTempMessage('Invalid email address.', 'error', displayDuration, emailButton);
        return;
    }

    // Access the hidden div to get the Markdown content
    var hiddenDiv = emailButton.closest('.bot-container').querySelector('.hidden-div');
    var hiddenDivMarkdown = hiddenDiv.textContent;

    // Convert Markdown content to HTML and plain text
    var emailContent = processMarkdownToTextAndHtml(hiddenDivMarkdown);

    // Prepare the email body prelude
    var emailPrelude = 'Below is the requested content. If you did not request this content, please reply to this email stating that, and let us know if you would like to prevent this email address from receiving any further messages.';
    var emailBodyPlain = `${emailPrelude}\n\n${emailContent.plainText}`;
    var emailBodyHtml = `<p>${emailPrelude.replace(/\n/g, '<br>')}</p><br>${emailContent.html}`;

    // Prepare the request payload
    var payload = {
        to_address: emailInputAddressValue,
        email_subject: "Your Deutsch QRAG Demo Questions and Answers - from focusonfoundations.org",
        from_address: "randy@floodlamp.bio",
        email_body_plain: emailBodyPlain,
        email_body_html: emailBodyHtml
    };

    // Send the email via the Lambda function
    fetch('https://kllsn7lnqa.execute-api.us-west-2.amazonaws.com/api/send-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
        .then(response => {
            console.log("Fetch response status:", response.status); // Log response status
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Received data:", data); // Log the response data
            displayTempMessage('Email sent successfully!', 'success', displayDuration, emailButton);
        })
        .catch(error => {
            console.error('Fetch error:', error); // Log any errors in the catch block
            displayTempMessage('Failed to send email.', 'error', displayDuration, emailButton);
        })
        .finally(() => {
            emailInputAddress.value = ''; // Clear the email input field
        });
}

function displayTempMessage(message, type, displayDuration, element) {
    console.log(`Display message: ${message}, Duration: ${displayDuration}ms`);

    const messageElement = document.createElement('div');
    messageElement.textContent = message;
    messageElement.style.color = type === 'error' ? 'red' : 'green';
    messageElement.style.textAlign = 'left';
    messageElement.style.marginLeft = '200px';
    messageElement.style.marginTop = '10px';

    const container = element.closest('.bot-container');
    const shareDiv = container.querySelector('.share-div');

    // Insert the message element right after the shareDiv
    if (shareDiv.nextSibling) {
        container.insertBefore(messageElement, shareDiv.nextSibling);
    } else {
        container.appendChild(messageElement); // Fallback if no next sibling
    }

    setTimeout(() => {
        container.removeChild(messageElement);
    }, displayDuration);
}


////// HELPER
function checkBotElementsExist(submitButtonId) {
    const submitButton = document.getElementById(submitButtonId);
    if (!submitButton) {
        console.error("checkBotElementsExist - Submit button not found.");
        return false;
    }

    let botContainer = submitButton.closest('.bot-container');
    if (!botContainer) {
        console.error("checkBotElementsExist - Bot container not found.");
        return false;
    }

    let accordionContainer = botContainer.querySelector('.accordion-container');
    if (!accordionContainer) {
        console.error("checkBotElementsExist - Accordion container not found.");
        return false;
    }

    let accordionCard = accordionContainer.querySelector('.accordion-card');
    if (!accordionCard) {
        console.error("checkBotElementsExist - Accordion card not found.");
        return false;
    }

    return true;
}


////// TEXT PROCESSING
function processJsonToMarkdown(jsonData) {
    const metadata = jsonData.metadata;
    const content = jsonData.content;
    const userQuestion = content.user_question;
    const routePreamble = content.route_preamble;
    const aiAnswer = content.ai_answer;

    let markdownString = `\n\n\n## ${userQuestion}\n`;  // add markdown heading level 2
    markdownString += `${routePreamble}\n\n`;

    if (content.quoted_qa) {
        const quotedQaLines = content.quoted_qa.split('\n');
        let formattedQa = '';

        quotedQaLines.forEach(line => {
            if (line.trim().startsWith('QUOTED QUESTION') && !line.trim().startsWith('QUOTED QUESTION SIMILARITY SCORE')) {
                formattedQa += `### ${line.trim()}\n`;
            } else {
                formattedQa += `${line}\n`;
            }
        });

        markdownString += formattedQa;
    }

    markdownString += `### AI ANSWER:\n${aiAnswer}`;

    return markdownString;
}

function simpleMarkdownToHtml(markdownString) {
    // Convert headings
    let htmlContent = markdownString
        .replace(/^###### (.*$)/gim, '<span style="font-size: 0.67em;">$1</span>')
        .replace(/^##### (.*$)/gim, '<span style="font-size: 0.83em;">$1</span>')
        .replace(/^#### (.*$)/gim, '<span style="font-size: 1em;">$1</span>')
        .replace(/^### (.*$)/gim, '<span style="font-size: 1.17em;"><strong>$1</strong></span>')
        .replace(/^## (.*$)/gim, '<span style="font-size: 1.5em;"><strong>$1</strong></span>')
        .replace(/^# (.*$)/gim, '<span style="font-size: 2em;"><strong>$1</strong></span>');

    // Convert bold and italic
    htmlContent = htmlContent
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')  // Convert double asterisks to bold
        .replace(/__(.*?)__/g, '<strong>$1</strong>')      // Convert double underscores to bold
        .replace(/\*(.*?)\*/g, '<em>$1</em>');      // Convert single asterisk to italic
 
    htmlContent = htmlContent
        .split('\n')
        .map(line => line.startsWith('QUOTED SOURCE') ? line : line.replace(/_(.*?)_/g, '<em>$1</em>'))
        .join('\n');  // Convert single underscore to italic, exempting lines that start with "QUOTED SOURCE"
    
    // Convert links to open in new tab
    htmlContent = htmlContent.replace(/\[(.*?)\]\((.*?)\)/gim, '<a href="$2" target="_blank">$1</a>');

    // Convert newlines to <br> tags
    htmlContent = htmlContent.replace(/\n/g, '<br>');

    return htmlContent.trim();
}

// Returns HTML and plain text for an email
function processMarkdownToTextAndHtml(markdownString) {
    // Convert Markdown to HTML using the simple conversion function
    const htmlContent = simpleMarkdownToHtml(markdownString);
    
    // Extract the first line and make it a title tag
    const firstLine = htmlContent.split('<br>')[0];
    const titleTag = `<span style="font-size: 2em; font-weight: bold;">${firstLine}</span>`;
    const modHtmlContent = htmlContent.replace(firstLine, titleTag);
    
    // Remove Markdown syntax to get plain text
    const plainTextContent = markdownString
    .replace(/[*_]/g, '')  // Remove asterisks and underscores used for bold and italic
    .replace(/#/g, '')     // Remove hash symbols used for headings
    .replace(/\n/g, ' ');  // Replace newlines with spaces

    return {
        plainText: plainTextContent,
        html: modHtmlContent
    };
}


////// STYLING
function setButtonToStopState(button, icon) {
    button.style.backgroundColor = '#f0ad4e'; // Change to a processing color, e.g., orange
    icon.textContent = 'stop_circle'; // Change to stop circle icon
    icon.style.fontSize = '24px';
    icon.style.transform = 'translateY(10%)'; // Adjust position
}

function resetButtonToInitialState(button, icon) {
    button.style.backgroundColor = '#3898ec'; // Reset to initial color
    icon.textContent = 'arrow_upward'; // Change back to arrow upward icon
    icon.style.fontSize = '20px';
}

