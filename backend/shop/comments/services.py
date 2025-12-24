from typing import Dict, List
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from shop.models import Comment

def load_comments(status: int) -> QuerySet:
    return Comment.objects.filter(status=status).order_by('-created_at')


def update_comment(id: int, action: int) -> bool:
    if action not in (1, -1):
        return False
    item: Comment = get_object_or_404(Comment, pk=id)
    try:
        item.status = Comment.STATUS_CHOICES[action]
        item.save()    
    except Exception as error:
        print("\n-->[ Error in modifying Comment obj ]<--\n", error)
        return False
    return True


def approve_comment(id: int) -> bool:
    item: Comment = get_object_or_404(Comment, pk=id)
    try:
        item.status = 1
        item.save()
    except Exception as error:
        print("\n--> [ Error in approving comment ]<--\n", error)
        return False
    return True


def reject_comment(id: int) -> bool:
    item: Comment = get_object_or_404(Comment, pk=id)
    try:
        item.status = -1
        item.save()
    except Exception as error:
        print("\n--> [ Error in rejecting comment ]<--\n", error)
        return False
    return True