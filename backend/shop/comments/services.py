from typing import Dict, List
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from shop.models import Comment

def load_comments(status: str) -> QuerySet:
    return Comment.objects.filter(status=status).order_by('-created_at')

def update_comment(id: int, action: str) -> bool:
    if action not in ('A', 'R'):
        return False
    item: Comment = get_object_or_404(Comment, pk=id)
    try:
        if action == "A":
            item.status = "Approved"
        elif action == "R":
            item.status = "Rejected"
        item.save()    
    except Exception as error:
        print("\n-->[ Error in modifying Comment obj ]<--\n", error)
        return False
    return True