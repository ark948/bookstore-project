from accounts.models import CustomUser
from shop.models import Comment


def update_comment(comment_id: int, user: CustomUser, **new_values) -> bool:
    """Update a comment record."""
    obj = Comment.objects.get(pk=comment_id)
    if obj and obj.user == user:
        try:
            for field, value in new_values.items():
                if hasattr(obj, field):
                    setattr(obj, field, value)
            obj.status = Comment.STATUS_CHOICES['P']
            obj.save()
        except Exception as error:
            print(error)
            return False
        return True
    return False

