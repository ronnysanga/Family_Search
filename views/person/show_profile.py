from typing import Optional
from utils.console_utils import show_header, show_message, get_input, clear_screen
from services.person import get_person_by_id, get_person_by_user_id


def show_profile(user_id: int, person_id: Optional[int] = None) -> None:
    """
    Muestra el perfil de una persona y permite (si corresponde) editarlo.

    Reglas:
    - Si no se pasa person_id, se busca la persona vinculada al user_id (id_usuario_creador).
    - Solo el creador del perfil (id_usuario_creador == user_id) puede editar.
    """

    if person_id is None:
        person = get_person_by_user_id(user_id)
        if not person:
            show_message("No hay una persona vinculada a este usuario.", "error")
            return
        person_id = person.get("id_persona")
    else:
        person = get_person_by_id(person_id)
        if not person:
            show_message("Persona no encontrada.", "error")
            return

    puede_editar = str(person.get("id_usuario_creador")) == str(user_id)

    while True:
        clear_screen()
        show_header(f"Perfil de {person.get('nombres', '')} {person.get('apellidos', '')}")

        print("\n" + "=" * 50)
        print(f"Nombres: {person.get('nombres', '')}")
        print(f"Apellidos: {person.get('apellidos', '')}")

        fnac = person.get("fecha_nac_formateada") or person.get("fecha_nacimiento")
        if fnac:
            print(f"Fecha de Nacimiento: {fnac}")

        fdef = person.get("fecha_def_formateada") or person.get("fecha_defuncion")
        if fdef:
            print(f"Fecha de Defunción: {fdef}")

        if person.get("sexo"):
            sexo_val = str(person["sexo"]).lower()
            if sexo_val in ("masculino", "m"):
                print("Sexo: Masculino")
            elif sexo_val in ("femenino", "f"):
                print("Sexo: Femenino")
            else:
                print(f"Sexo: {person['sexo']}")

        if person.get("lugar_nacimiento"):
            print(f"Lugar de Nacimiento: {person['lugar_nacimiento']}")

        if person.get("biografia"):
            print("\nBiografía:")
            print("-" * 50)
            print(person["biografia"])

        print("\n" + "=" * 50)

        print("\nOpciones:")
        if puede_editar:
            print("1. Editar perfil")
        print("2. Volver al menú principal")

        choice = get_input("\nSeleccione una opción: ").strip()

        if choice == "1" and puede_editar:
            from .edit_views import show_edit_person_form
            show_edit_person_form(person, user_id)
            person = get_person_by_id(person_id) or person
            puede_editar = str(person.get("id_usuario_creador")) == str(user_id)

        elif choice == "2":
            input("\nPresione ENTER para volver al menú principal...")
            return

        else:
            show_message("Opción no válida. Intente nuevamente.", "error")
            input("Presione ENTER para continuar...")
