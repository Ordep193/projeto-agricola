def is_coordenador_or_superuser(user):
    return user.is_superuser or hasattr(user, 'coordenador')