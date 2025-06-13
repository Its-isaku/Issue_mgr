//? Drag and Drop Functionality for Kanban Cards
document.addEventListener('DOMContentLoaded', function() {
    let draggedCard = null;
    let draggedFromColumn = null;

    //? Add event listeners to all cards and columns
    function initializeDragAndDrop() {
        //* Remove existing event listeners first to prevent duplicates
        removeDragEventListeners();
        
        const cards = document.querySelectorAll('.card[draggable="true"]');
        const columns = document.querySelectorAll('.cards-container');

        //* Add drag events to cards
        cards.forEach(card => {
            card.addEventListener('dragstart', handleDragStart);
            card.addEventListener('dragend', handleDragEnd);
        });

        //* Add drop events to columns
        columns.forEach(column => {
            column.addEventListener('dragover', handleDragOver);
            column.addEventListener('drop', handleDrop);
            column.addEventListener('dragenter', handleDragEnter);
            column.addEventListener('dragleave', handleDragLeave);
        });
    }

    //? Remove all drag event listeners to prevent duplicates
    function removeDragEventListeners() {
        const cards = document.querySelectorAll('.card[draggable="true"]');
        const columns = document.querySelectorAll('.cards-container');

        cards.forEach(card => {
            card.removeEventListener('dragstart', handleDragStart);
            card.removeEventListener('dragend', handleDragEnd);
        });

        columns.forEach(column => {
            column.removeEventListener('dragover', handleDragOver);
            column.removeEventListener('drop', handleDrop);
            column.removeEventListener('dragenter', handleDragEnter);
            column.removeEventListener('dragleave', handleDragLeave);
        });
    }

    //? Drag Event Handlers
    function handleDragStart(e) {
        draggedCard = this;
        draggedFromColumn = this.closest('.cards-container');
        
        //* Add dragging class for visual feedback
        this.classList.add('dragging');
        
        //* Store data for the drag operation
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/html', this.outerHTML);
        e.dataTransfer.setData('text/plain', this.getAttribute('data-issue-id'));
        
        //* Reduce opacity of the dragged card with a small delay
        setTimeout(() => {
            if (draggedCard) {
                draggedCard.style.opacity = '0.5';
            }
        }, 0);
    }

    function handleDragEnd(e) {
        //* Always reset styles regardless of successful drop or not
        if (this.style) {
            this.style.opacity = '';
            this.style.transform = '';
        }
        this.classList.remove('dragging');
        
        //* Clean up all column highlights
        document.querySelectorAll('.cards-container').forEach(column => {
            column.classList.remove('drag-over');
        });
        
        //* Clear drag state
        draggedCard = null;
        draggedFromColumn = null;
        
        //* Force reflow to ensure styles are applied
        this.offsetHeight;
    }

    function handleDragOver(e) {
        if (e.preventDefault) {
            e.preventDefault(); //* Allows us to drop
        }
        
        e.dataTransfer.dropEffect = 'move';
        return false;
    }

    function handleDragEnter(e) {
        //* Add visual feedback when hovering over a drop zone
        //* Only add if we're not already over this container
        if (!this.classList.contains('drag-over')) {
            this.classList.add('drag-over');
        }
    }

    function handleDragLeave(e) {
        //* Remove visual feedback when leaving a drop zone
        //* Only remove if we're actually leaving the container, not just moving to a child
        if (!this.contains(e.relatedTarget)) {
            this.classList.remove('drag-over');
        }
    }

    function handleDrop(e) {
        if (e.stopPropagation) {
            e.stopPropagation(); //* Stops some browsers from redirecting
        }
        if (e.preventDefault) {
            e.preventDefault(); //* Prevent default browser behavior
        }

        const dropZone = this;
        
        //* Always remove drag-over class
        dropZone.classList.remove('drag-over');
        
        //* Clear all drag-over classes from other columns
        document.querySelectorAll('.cards-container').forEach(column => {
            column.classList.remove('drag-over');
        });

        //* Check if we have a valid drop (draggedCard exists and it's moving to a different column)
        if (draggedCard && draggedFromColumn !== dropZone) {
            const issueId = draggedCard.getAttribute('data-issue-id');
            const newStatusId = dropZone.getAttribute('data-status-id');
            const oldStatusId = draggedFromColumn.getAttribute('data-status-id');

            //* Ensure we have valid status IDs
            if (!issueId || !newStatusId || !oldStatusId) {
                console.error('Missing required IDs for drag and drop');
                return false;
            }

            //* Move the card visually first for immediate feedback
            const cardClone = draggedCard.cloneNode(true);
            
            //* Clean up the cloned card - remove any drag states and reset styles
            cardClone.classList.remove('dragging');
            cardClone.style.opacity = '';
            cardClone.style.transform = '';
            cardClone.setAttribute('data-status-id', newStatusId);
            
            //* Remove the original card
            draggedCard.remove();
            
            //* Add the cloned card to the new column
            dropZone.appendChild(cardClone);
            
            //* Re-initialize drag and drop for all cards (including the new one)
            initializeDragAndDrop();

            //* Update the card counts
            updateCardCounts(oldStatusId, newStatusId);

            //* Send AJAX request to update the backend
            moveIssueToStatus(issueId, newStatusId, oldStatusId, cardClone);
        }

        return false;
    } 
    //? AJAX Function to Move Issue
    function moveIssueToStatus(issueId, newStatusId, oldStatusId, cardElement) {
        //* Get CSRF token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        if (!csrfToken) {
            console.error('CSRF token not found');
            revertCardMove(cardElement, oldStatusId, newStatusId);
            return;
        }

        fetch(`/issues/move_issue/${issueId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken,
            },
            body: `status_id=${newStatusId}`
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                console.log('Issue moved successfully:', data.issue);
                
                //* Update the card's data attributes
                cardElement.setAttribute('data-status-id', newStatusId);
                
                //* Ensure the card doesn't have any stuck drag styles
                cardElement.classList.remove('dragging');
                cardElement.style.opacity = '';
                cardElement.style.transform = '';

            } else {
                console.error('Error moving issue:', data.error);
                
                //* Revert the visual change if the backend update failed
                revertCardMove(cardElement, oldStatusId, newStatusId);

            }
        })
        .catch(error => {
            console.error('Network error:', error);
            
            //* Revert the visual change if there was a network error
            revertCardMove(cardElement, oldStatusId, newStatusId);

        });
    }

    //? Helper Functions
    //? Global cleanup function to reset any stuck drag states
    function cleanupAllDragStates() {
        //* Remove dragging class from all cards
        document.querySelectorAll('.card').forEach(card => {
            card.classList.remove('dragging');
            if (card.style) {
                card.style.opacity = '';
                card.style.transform = '';
            }
        });
        
        //* Remove drag-over class from all containers
        document.querySelectorAll('.cards-container').forEach(container => {
            container.classList.remove('drag-over');
        });
        
        //* Clear global drag state
        draggedCard = null;
        draggedFromColumn = null;
    }

    function revertCardMove(cardElement, originalStatusId, failedStatusId) {
        //* Find the original column and move the card back
        const originalColumn = document.querySelector(`[data-status-id="${originalStatusId}"]`);
        if (originalColumn && cardElement) {
            originalColumn.appendChild(cardElement);
            cardElement.setAttribute('data-status-id', originalStatusId);
            
            //* Update card counts back to original state
            updateCardCounts(failedStatusId, originalStatusId);
            
            //* Re-initialize drag and drop after reverting
            initializeDragAndDrop();
        }
    }

    function updateCardCounts(fromStatusId, toStatusId) {
        //* Update the count for the column we moved from
        const fromColumn = document.querySelector(`.column[data-status-id="${fromStatusId}"]`);
        if (fromColumn) {
            const fromCountElement = fromColumn.querySelector('.task-count');
            if (fromCountElement) {
                const currentCount = parseInt(fromCountElement.textContent) || 0;
                fromCountElement.textContent = Math.max(0, currentCount - 1);
            }
        }

        //* Update the count for the column we moved to
        const toColumn = document.querySelector(`.column[data-status-id="${toStatusId}"]`);
        if (toColumn) {
            const toCountElement = toColumn.querySelector('.task-count');
            if (toCountElement) {
                const currentCount = parseInt(toCountElement.textContent) || 0;
                toCountElement.textContent = currentCount + 1;
            }
        }
    }



    //? Initialize Drag and Drop
    //? Add escape key handler to cancel drag operations
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && draggedCard) {
            cleanupAllDragStates();
        }
    });

    //? Initialize drag and drop when the page loads
    cleanupAllDragStates(); //* Clean up any previous states first
    initializeDragAndDrop();

    //? Re-initialize drag and drop when new cards are added via AJAX
    //? This function can be called from Issues_tables.js after adding new cards
    window.reinitializeDragAndDrop = function() {
        cleanupAllDragStates();
        initializeDragAndDrop();
    };
    
    //? Expose cleanup function globally for emergency cleanup
    window.cleanupDragStates = cleanupAllDragStates;
});
