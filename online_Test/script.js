// Apply formatting (bold, italic)
function formatText(command) {
    document.execCommand(command, false, null);
    updateMarkup();
}

// Change font family
function changeFont(font) {
    document.execCommand('fontName', false, font);
    updateMarkup();
}

// Change text color
function changeTextColor(color) {
    document.execCommand('foreColor', false, color);
    updateMarkup();
}

// Change text highlight color
function changeHighlightColor(color) {
    document.execCommand('hiliteColor', false, color);
    updateMarkup();
}

// Align text (left, center, right, justify)
function alignText(alignment) {
    document.execCommand('justify' + alignment, false, null);
    updateMarkup();
}

// Update markup view
function updateMarkup() {
    const editorContent = document.getElementById('editor').innerHTML;
    document.getElementById('markupText').textContent = editorContent;
}








// // Apply formatting (bold, italic)
// function formatText(command) {
//     document.execCommand(command, false, null);
// }

// // Change font family
// function changeFont(font) {
//     document.execCommand('fontName', false, font);
// }

// // Change text color
// function changeTextColor(color) {
//     document.execCommand('foreColor', false, color);
// }

// // Change text highlight color
// function changeHighlightColor(color) {
//     document.execCommand('hiliteColor', false, color);
// }

// // Align text (left, center, right, justify)
// function alignText(alignment) {
//     document.execCommand('justify' + alignment, false, null);
// }

// // Toggle annotations
// function toggleAnnotation() {
//     const annotationToggle = document.getElementById('annotationToggle');
//     const annotationStatus = document.getElementById('annotationStatus');
//     if (annotationToggle.checked) {
//         annotationStatus.textContent = "Annotations are on.";
//     } else {
//         annotationStatus.textContent = "Annotations are off.";
//     }
// }







// // Apply formatting (bold, italic)
// function formatText(command) {
//     document.execCommand(command, false, null);
// }

// // Change font family
// function changeFont(font) {
//     document.execCommand('fontName', false, font);
// }

// // Change text color
// function changeTextColor(color) {
//     document.execCommand('foreColor', false, color);
// }

// // Change text highlight color
// function changeHighlightColor(color) {
//     document.execCommand('hiliteColor', false, color);
// }







// // Save the text to a file
// function saveText() {
//     const text = document.getElementById('editor').value;
//     const blob = new Blob([text], { type: 'text/plain' });
//     const link = document.createElement('a');
//     link.href = URL.createObjectURL(blob);
//     link.download = 'text-editor-content.txt';
//     link.click();
// }

// // Clear the text area
// function clearText() {
//     document.getElementById('editor').value = '';
// }