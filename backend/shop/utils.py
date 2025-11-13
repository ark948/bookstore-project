from accounts.models import CustomUser


def has_custom_permission(user: CustomUser) -> bool:
    return user.is_authenticated

def custom_print(*args) -> None:
    for i in args:
        print("->", i, "\n")