from django.shortcuts import get_object_or_404
from shop.models import Vote, Comment

def check_vote_exists(comment_id: int, user):
    comment_obj = Comment.objects.get(pk=comment_id)
    if comment_obj:
        item = Vote.objects.filter(
            comment=comment_obj,
            user=user
        ).first()
        if item.exists():
            return True
        else:
            return False
    return None