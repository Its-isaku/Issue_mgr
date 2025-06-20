#? Import necessary modules
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.db import models
from .models import Issue, Status, Board
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import BoardForm, IssueForm\


#! |------------------------Web View------------------------| 
#? IssueListView
class IssueListView(LoginRequiredMixin, TemplateView):
    template_name = 'issues/issues_list.html'                                                         #* Template for the issues list page

    def get_context_data(self, **kwargs):                                                             #* Method to get context data for the template
        context = super().get_context_data(**kwargs)
        user_team = self.request.user.team                                                            #* Get current user's team
        
        # Filter boards: show boards created by users from the same team OR boards without a creator (legacy data)
        context['boards'] = Board.objects.filter(
            models.Q(created_by__team=user_team) | models.Q(created_by__isnull=True)
        )
        
        # Filter users to only show team members  
        context['users'] = get_user_model().objects.filter(team=user_team)                           #* Add only team users to context
        return context

#! |------------------------Web Backend logic (AJAX endpoints)------------------------| 

#? Add a new Board (AJAX)
@login_required
def add_board(request):
    if request.method == 'POST':                                                                       #* Check if the request method is POST
        form = BoardForm(request.POST)                                                                 #* Create a form instance with the POST data                                            
        if form.is_valid():                                                                            #* Validate the form                             
            board = form.save(commit=False)                                                            #* Create board instance without saving yet
            board.created_by = request.user                                                            #* Set the creator to current user
            board.save()                                                                               #* Save the board to database
            
            default_statuses = [
                {'name': 'To Do', 'description': 'Tasks to be started', 'is_fixed': True},
                {'name': 'In Progress', 'description': 'Tasks currently being worked on', 'is_fixed': True},
                {'name': 'Done', 'description': 'Completed tasks', 'is_fixed': True}
            ]
            
            for status_data in default_statuses:
                Status.objects.create(
                    name=status_data['name'],
                    description=status_data['description'],
                    board=board,
                    is_fixed=status_data['is_fixed']
                )
            
            return JsonResponse({'success': True, 'board': {'id': board.id, 'name': board.name}})      #* Return a JSON response with success status and the new board's details
        return JsonResponse({'success': False, 'errors': form.errors})                                 #* If the form is not valid, return a JSON response with errors
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)                    #* If the request method is not POST, return an error response

#? Add a new Issue (AJAX)
@login_required
def add_issue(request):
    if request.method == 'POST':                                                                       #* Check if the request method is POST
        form = IssueForm(request.POST)                                                                 #* Create a form instance with the POST data
        if form.is_valid():                                                                            #* Validate the form
            issue = form.save(commit=False)                                                            #* Create an Issue instance without saving to database yet
            issue.reporter = request.user                                                              #* Set the reporter to the current user
            
            status_id = request.POST.get('status')
            if status_id:
                new_status = get_object_or_404(Status, id=status_id)
                if new_status.board.created_by and new_status.board.created_by.team != request.user.team:
                    return JsonResponse({'success': False, 'error': 'Permission denied - invalid status'})
                issue.status = new_status
            
            issue.save()                                                                               #* Save the issue to the database
            return JsonResponse({'success': True, 'issue': {                                           #* Return a JSON response with success status and the new issue's details
                'id': issue.id,
                'title': issue.title,
                'summary': issue.summary,
                'description': issue.description,
                'assignee': issue.assignee.username if issue.assignee else '',
                'status_id': issue.status.id if issue.status else None
            }})
        return JsonResponse({'success': False, 'errors': form.errors})                                 #* If the form is not valid, return a JSON response with errors
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)                    #* If the request method is not POST, return an error response

#? Delete an Issue (AJAX)
@login_required
def delete_issue(request, issue_id):
    if request.method == 'POST':                                                                       #* Check if the request method is POST
        try:

            issue = get_object_or_404(Issue, id=issue_id)
            
            if issue.board and issue.board.created_by and issue.board.created_by.team != request.user.team:
                return JsonResponse({'success': False, 'error': 'Permission denied'})
                
            issue.delete()                                                                             #* Delete the issue
            return JsonResponse({'success': True})                                                     #* Return success response
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})                                   #* Return error response
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)                    #* If the request method is not POST, return an error response

#? Edit an Issue (AJAX)
@login_required
def edit_issue(request, issue_id):
    if request.method == 'POST':                                                                       #* Check if the request method is POST
        try:

            issue = get_object_or_404(Issue, id=issue_id)
            
            if issue.board and issue.board.created_by and issue.board.created_by.team != request.user.team:
                return JsonResponse({'success': False, 'error': 'Permission denied'})
                
            form = IssueForm(request.POST, instance=issue)                                             #* Create form with existing issue data
            if form.is_valid():                                                                        #* Validate the form
                status_id = request.POST.get('status')
                if status_id:

                    new_status = get_object_or_404(Status, id=status_id)
                    if new_status.board.created_by and new_status.board.created_by.team != request.user.team:
                        return JsonResponse({'success': False, 'error': 'Permission denied - invalid status'})
                    issue.status = new_status
                
                updated_issue = form.save()                                                            #* Save the updated issue
                return JsonResponse({'success': True, 'issue': {                                       #* Return success response with updated data
                    'id': updated_issue.id,
                    'title': updated_issue.title,
                    'summary': updated_issue.summary,
                    'description': updated_issue.description,
                    'assignee': updated_issue.assignee.username if updated_issue.assignee else '',
                    'priority': updated_issue.priority,
                    'story_points': updated_issue.story_points,
                    'status_id': updated_issue.status.id if updated_issue.status else None
                }})
            return JsonResponse({'success': False, 'errors': form.errors})                             #* Return form errors 
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})                                   #* Return error response
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)                    #* If the request method is not POST, return an error response

#? Move an Issue to a different status (AJAX - for drag and drop)
@login_required
def move_issue(request, issue_id):
    if request.method == 'POST':                                                                       #* Check if the request method is POST
        try:

            issue = get_object_or_404(Issue, id=issue_id)
            
            if issue.board and issue.board.created_by and issue.board.created_by.team != request.user.team:
                return JsonResponse({'success': False, 'error': 'Permission denied'})
            
            new_status_id = request.POST.get('status_id')                                              #* Get the new status ID from POST data
            
            if not new_status_id:
                return JsonResponse({'success': False, 'error': 'Status ID is required'})
            

            new_status = get_object_or_404(Status, id=new_status_id)
            if new_status.board.created_by and new_status.board.created_by.team != request.user.team:
                return JsonResponse({'success': False, 'error': 'Permission denied - invalid status'})
                
            old_status_id = issue.status.id if issue.status else None                                 #* Store old status for response
            
            issue.status = new_status                                                                  #* Update the issue's status
            issue.save()                                                                               #* Save the changes
            
            return JsonResponse({                                                                      #* Return success response with updated data
                'success': True, 
                'issue': {
                    'id': issue.id,
                    'title': issue.title,
                    'old_status_id': old_status_id,
                    'new_status_id': new_status.id,
                    'new_status_name': new_status.name
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})                                   #* Return error response
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)                    #* If the request method is not POST, return an error response