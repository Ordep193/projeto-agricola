def is_coordenador_or_superuser(user, produtor):
    return user.is_superuser or getattr(user, 'coordenador', None) == produtor.coordenador
