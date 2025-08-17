# Importar las vistas principales para exponerlas en el espacio de nombres del paquete
from .profile_views import show_profile
from .search_views import show_search_people, search_and_select_person
from .add_views import show_add_person_form
from .edit_views import show_edit_person_form

__all__ = [
    'show_profile',
    'show_search_people',
    'search_and_select_person',
    'show_add_person_form',
    'show_edit_person_form'
]
