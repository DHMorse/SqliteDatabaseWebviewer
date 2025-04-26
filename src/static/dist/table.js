"use strict";
/**
 * table.ts - TypeScript functions for database table operations
 * For use with Flask application
 */
/**
 * Copies the given text to the clipboard
 * @param text - The text to copy to clipboard
 */
function copyToClipboard(text) {
    // Try to use the clipboard API
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text)
            .then(() => {
            // Show a temporary tooltip or notification
            showCopyNotification(text);
        })
            .catch(err => {
            console.error('Failed to copy: ', err);
            alert('Unable to copy to clipboard. Your browser may not support this feature.');
        });
    }
    else {
        // Fallback for browsers that don't support clipboard API
        fallbackCopyToClipboard(text);
    }
}
/**
 * Copies all data from a specific row
 * @param rowIndex - The index of the row to copy
 */
function copyRowData(rowIndex) {
    if (!tableData || !tableData.rows || rowIndex >= tableData.rows.length) {
        console.error('Invalid row index or missing data');
        return;
    }
    const rowData = tableData.rows[rowIndex];
    const columns = tableData.columns;
    // Format as key-value pairs
    let formattedData = '';
    for (let i = 0; i < columns.length; i++) {
        formattedData += `${columns[i]}: ${rowData[i]}\n`;
    }
    copyToClipboard(formattedData);
    showCopyNotification('Row data copied');
}
/**
 * Copies row data as comma-separated values
 * @param rowIndex - The index of the row to copy
 */
function copyRowDataAsCSV(rowIndex) {
    if (!tableData || !tableData.rows || rowIndex >= tableData.rows.length) {
        console.error('Invalid row index or missing data');
        return;
    }
    const rowData = tableData.rows[rowIndex];
    // Join values with comma and space
    const csvText = rowData.join(', ');
    copyToClipboard(csvText);
    showCopyNotification('Row copied as CSV format');
}
/**
 * Copies all table data to clipboard
 */
function copyAllData() {
    if (!tableData || !tableData.rows || !tableData.columns) {
        console.error('Missing table data');
        return;
    }
    // Create CSV-like format
    let csvContent = tableData.columns.join(',') + '\n';
    // Add each row
    tableData.rows.forEach(row => {
        // Handle values that might contain commas by quoting them
        const formattedRow = row.map(value => {
            // Convert to string and check if it needs quotes
            const strValue = String(value);
            return strValue.includes(',') || strValue.includes('"') ?
                `"${strValue.replace(/"/g, '""')}"` : strValue;
        });
        csvContent += formattedRow.join(',') + '\n';
    });
    copyToClipboard(csvContent);
    showCopyNotification('All table data copied as CSV');
}
/**
 * Shows a temporary notification that text was copied
 * @param text - The text that was copied
 */
function showCopyNotification(text) {
    // Create a temporary notification element
    const notification = document.createElement('div');
    // Truncate very long text for the notification
    const displayText = text.length > 50 ? text.substring(0, 47) + '...' : text;
    notification.textContent = `Copied: ${displayText}`;
    notification.style.position = 'fixed';
    notification.style.bottom = '20px';
    notification.style.left = '50%';
    notification.style.transform = 'translateX(-50%)';
    notification.style.backgroundColor = '#bb86fc';
    notification.style.color = '#000';
    notification.style.padding = '10px 20px';
    notification.style.borderRadius = '4px';
    notification.style.zIndex = '1000';
    notification.style.maxWidth = '80%';
    notification.style.overflow = 'hidden';
    notification.style.textOverflow = 'ellipsis';
    notification.style.whiteSpace = 'nowrap';
    // Add to document
    document.body.appendChild(notification);
    // Remove after 2 seconds
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transition = 'opacity 0.5s';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 500);
    }, 2000);
}
/**
 * Fallback method for copying to clipboard using document.execCommand
 * @param text - The text to copy
 */
function fallbackCopyToClipboard(text) {
    try {
        // Create a temporary textarea element
        const textarea = document.createElement('textarea');
        textarea.value = text;
        // Make the textarea out of viewport
        textarea.style.position = 'fixed';
        textarea.style.left = '-999999px';
        textarea.style.top = '-999999px';
        document.body.appendChild(textarea);
        // Select and copy
        textarea.focus();
        textarea.select();
        const successful = document.execCommand('copy');
        // Clean up
        document.body.removeChild(textarea);
        if (successful) {
            showCopyNotification(text);
        }
        else {
            alert('Unable to copy to clipboard');
        }
    }
    catch (err) {
        console.error('Fallback: Oops, unable to copy', err);
        alert('Unable to copy to clipboard');
    }
}
