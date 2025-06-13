document.addEventListener('DOMContentLoaded', function() {

    //? Open card modal and set the status
    document.querySelectorAll('.add-card-btn').forEach(btn => {
        btn.onclick = function() {
            document.getElementById('issue-status-id').value = this.dataset.statusId;
        };
    });

    //? Submit add board form
    document.getElementById('form-add-board').onsubmit = function(e) {
        e.preventDefault();
        let formData = new FormData(this);
        fetch('/issues/add_board/', {
            method: 'POST',
            headers: {'X-CSRFToken': formData.get('csrfmiddlewaretoken')},
            body: formData
        })
        .then(r => r.json())
        .then(data => {
            if (data.success) location.reload();
            else alert('Error: ' + JSON.stringify(data.errors));
        });
    };

    //? Submit add card form
    document.getElementById('form-add-issue').onsubmit = function(e) {
        e.preventDefault();
        let formData = new FormData(this);
        fetch('/issues/add_issue/', {
            method: 'POST',
            headers: {'X-CSRFToken': formData.get('csrfmiddlewaretoken')},
            body: formData
        })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                location.reload();
                if (window.reinitializeDragAndDrop) {
                    window.reinitializeDragAndDrop();
                }
            }
            else alert('Error: ' + JSON.stringify(data.errors));
        });
    };

    //? Open card details modal and populate with data
    document.querySelectorAll('.DetailsBtn').forEach(btn => {
        btn.onclick = function() {
            //* Populate the edit form with current card data
            document.getElementById('edit-issue-id').value = this.dataset.issueId;
            document.getElementById('edit-issue-title').value = this.dataset.issueTitle;
            document.getElementById('edit-issue-summary').value = this.dataset.issueSummary;
            document.getElementById('edit-issue-desc').value = this.dataset.issueDescription;
            document.getElementById('edit-issue-assignee').value = this.dataset.issueAssignee;
            document.getElementById('edit-issue-priority').value = this.dataset.issuePriority;
            document.getElementById('edit-issue-story-points').value = this.dataset.issueStoryPoints;
            document.getElementById('edit-issue-status').value = this.dataset.issueStatus;
            document.getElementById('edit-issue-reporter').textContent = this.dataset.issueReporter;
            document.getElementById('edit-issue-created').textContent = this.dataset.issueCreated;
        };
    });

    //? Open delete confirmation modal
    document.querySelectorAll('.DeleteCardBtn').forEach(btn => {
        btn.onclick = function() {
            document.getElementById('delete-card-id').value = this.dataset.issueId;
            document.getElementById('delete-card-title').textContent = this.dataset.issueTitle;
        };
    });

    //? Submit edit card form
    document.getElementById('form-edit-issue').onsubmit = function(e) {
        e.preventDefault();
        let formData = new FormData(this);
        let issueId = formData.get('issue_id');
        
        fetch(`/issues/edit_issue/${issueId}/`, {
            method: 'POST',
            headers: {'X-CSRFToken': formData.get('csrfmiddlewaretoken')},
            body: formData
        })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                //* Close modal and reload page
                bootstrap.Modal.getInstance(document.getElementById('modalCardDetails')).hide();
                location.reload();
                if (window.reinitializeDragAndDrop) {
                    window.reinitializeDragAndDrop();
                }
            } else {
                alert('Error updating card: ' + JSON.stringify(data.errors || data.error));
            }
        })
        .catch(error => {
            alert('Network error: ' + error);
        });
    };

    //? Confirm delete card
    document.getElementById('confirm-delete-card').onclick = function() {
        let issueId = document.getElementById('delete-card-id').value;
        let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        fetch(`/issues/delete_issue/${issueId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            }
        })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                //* Close modal and reload page
                bootstrap.Modal.getInstance(document.getElementById('modalDeleteCard')).hide();
                location.reload();
                if (window.reinitializeDragAndDrop) {
                    window.reinitializeDragAndDrop();
                }
            } else {
                alert('Error deleting card: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(error => {
            alert('Network error: ' + error);
        });
    };
});