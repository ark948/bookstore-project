from typing import Dict, List

from shop.models import Comment

def load_comments(status: str):
    return Comment.objects.filter(status=status).order_by('-created_at')