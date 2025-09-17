from accounts.models import CustomUser


def has_custom_permission(user: CustomUser) -> bool:
    return user.is_authenticated