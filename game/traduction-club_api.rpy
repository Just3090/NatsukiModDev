init -100 python:
    if not hasattr(store, "submods"):
        store.submods = []

    class SubmodInfo(object):
        def __init__(self, name, version, author, coauthors, description):
            self.name = name
            self.version = version
            self.author = author
            self.coauthors = coauthors
            self.description = description

    def register_submod(name, version, author, coauthors, description):
        info = SubmodInfo(name, version, author, coauthors, description)
        store.submods.append(info)

screen submods_list_screen():
    tag menu

    use game_menu(_("Submods")):

        default tooltip = Tooltip("")

        viewport id "submods_scroll":
            scrollbars "vertical"
            mousewheel True
            draggable True

            has vbox
            style_prefix "check"
            xfill True
            xmaximum 1000

            if submods:
                for s in sorted(submods, key=lambda x: x.name):
                    vbox:
                        xfill True
                        xmaximum 1000

                        label s.name:
                            yanchor 0
                            xalign 0
                            text_text_align 0.0

                        if hasattr(s, "coauthors") and s.coauthors:
                            $ authors = "v{0}{{space=20}}por {1}, {2}".format(s.version, s.author, ", ".join(s.coauthors))
                        else:
                            $ authors = "v{0}{{space=20}}por {1}".format(s.version, s.author)

                        text "[authors]":
                            yanchor 0
                            xalign 0
                            text_align 0.0
                            layout "greedy"
                            style "main_menu_version"

                        if s.description:
                            text s.description text_align 0.0

                        null height 20
            else:
                text _("No submods are installed.")

        text tooltip.value:
            xalign 0 yalign 1.0
            xoffset 300 yoffset -10
            style "main_menu_version"

init -1 python:
    if not hasattr(store, "LATE_TOPIC_REGISTRY"):
        store.LATE_TOPIC_REGISTRY = []

init 999 python:
    for topic, topic_group in getattr(store, "LATE_TOPIC_REGISTRY", []):
        registerTopic(topic, topic_group=topic_group)
        if topic_group == TOPIC_TYPE_NORMAL:
            store.topics.TOPIC_MAP[topic.label] = topic
            store.topic_handler.ALL_TOPIC_MAP[topic.label] = topic
    store.LATE_TOPIC_REGISTRY = []








#### ====================================================== ###
#### ------------------- DOCUMENTACION -------------------- ###
#### ====================================================== ###

# It's not a good documentation I think because some metods wont work in a real submod D:



# # Documentación: Registro y extensión de eventos y holidays

# ## Introducción

# El sistema de eventos de Just Natsuki permite a submods y extensiones registrar nuevos eventos y holidays (festividades) de manera flexible. 
# Esto se logra añadiendo instancias de `Topic` al `jn_events.EVENT_MAP` para eventos, o instancias de `JNHoliday` usando el registro interno para holidays.

# Esta documentación cubre:

# - Registro de eventos personalizados
# - Registro de holidays personalizados
# - Uso de condiciones, afinidad y rangos
# - Ejemplos avanzados de integración
# - Consideraciones de persistencia y filtrado

# ---

# ## 1. Registro de eventos personalizados

# Para registrar un evento, debes crear una instancia de `Topic` y añadirla al `jn_events.EVENT_MAP` o usar la función `registerTopic`.

# ### Ejemplo básico

# ````renpy
# # En tu submod:
# init 5 python:
#     import store.jn_events as jn_events
#     from store.topics import Topic

#     jn_events.EVENT_MAP["mi_evento"] = Topic(
#         persistent._event_database,
#         label="mi_evento",
#         unlocked=True,
#         conditional="persistent.mi_variable_especial",
#         affinity_range=(jn_affinity.HAPPY, jn_affinity.LOVE)
#     )
# ````

# ### Ejemplo usando `registerTopic` y grupos (RECOMENDADO)

# ````renpy
# init 5 python:
#     registerTopic(
#         Topic(
#             persistent._event_database,
#             label="evento_avanzado",
#             unlocked=True,
#             conditional="persistent.otro_flag and jn_utils.get_total_gameplay_days() > 10",
#             affinity_range=(jn_affinity.NORMAL, None)
#         ),
#         topic_group=TOPIC_TYPE_EVENT
#     )
# ````

# ### Opciones de configuración

# - **label**: nombre del label que ejecuta el evento.
# - **unlocked**: si el evento está desbloqueado por defecto.
# - **conditional**: string evaluado como condición para mostrar el evento.
# - **affinity_range**: tupla con el rango de afinidad requerido.

# ---

# ## 2. Registro de holidays personalizados

# Para holidays, debes crear una instancia de `JNHoliday` y registrarla usando la función interna `_m1_script0x2devents__registerHoliday`.

# ### Ejemplo básico

# ````renpy
# init 5 python in jn_events:
#     from store.jn_events import JNHoliday, JNHolidayTypes, _m1_script0x2devents__registerHoliday
#     import store.jn_affinity as jn_affinity

#     _m1_script0x2devents__registerHoliday(JNHoliday(
#         label="holiday_mi_festividad",
#         holiday_type=JNHolidayTypes.anniversary,
#         affinity_range=(jn_affinity.HAPPY, None),
#         natsuki_sprite_code="1uchgn",
#         conditional="persistent.mi_festividad_desbloqueada",
#         deco_list=["mi_decoracion"],
#         prop_list=["mi_prop"],
#         priority=50
#     ))
# ````

# ### Opciones avanzadas

# - **conditional**: permite que la festividad solo se muestre bajo ciertas condiciones.
# - **affinity_range**: restringe la afinidad necesaria.
# - **deco_list** y **prop_list**: listas de decoraciones y props a mostrar.
# - **priority**: controla el orden de aparición si hay varias festividades.

# ---

# ## 3. Combinaciones posibles

# Puedes combinar:

# - **conditional**: cualquier expresión Python válida, usando variables persistentes, funciones utilitarias, etc.
# - **affinity_range**: desde un estado mínimo hasta uno máximo, o sin límite superior/inferior.
# - **topic_group**: puedes registrar eventos en diferentes grupos (por ejemplo, eventos, interacciones, etc.).
# - **Visuales**: puedes definir props, decoraciones y música personalizada para holidays.

# ### Ejemplo: Evento solo si es un día especial y afinidad máxima

# ````renpy
# init 5 python:
#     registerTopic(
#         Topic(
#             persistent._event_database,
#             label="evento_super_especial",
#             unlocked=True,
#             conditional="jn_utils.isSpecialDay() and Natsuki.isLove()",
#             affinity_range=(jn_affinity.LOVE, jn_affinity.LOVE)
#         ),
#         topic_group=TOPIC_TYPE_EVENT
#     )
# ````

# ### Ejemplo: Holiday con props y música personalizada

# ````renpy
# init 5 python in jn_events:
#     _m1_script0x2devents__registerHoliday(JNHoliday(
#         label="holiday_fiesta_personalizada",
#         holiday_type=JNHolidayTypes.player_birthday,
#         affinity_range=(jn_affinity.AFFECTIONATE, None),
#         natsuki_sprite_code="1uchgnl",
#         bgm="mod_assets/bgm/fiesta.ogg",
#         deco_list=["globos", "guirnaldas"],
#         prop_list=["tarta_especial"],
#         priority=20
#     ))
# ````

# ---

# ## 4. Persistencia y filtrado

# El sistema guarda el estado de los holidays y eventos en el objeto `persistent`. Puedes filtrar holidays usando:

# ````renpy
# holidays = jn_events.JNHoliday.filterHolidays(
#     holiday_list=jn_events.getAllHolidays(),
#     is_seen=False,
#     affinity=store.Natsuki._getAffinityState()
# )
# ````
# NOTA: También existe el metodo para filtrar de: Topic.filter_topics(...)

# ---

# ## 5. Ejemplo completo: Submod que añade evento y holiday

# ````renpy
# init 5 python:
#     import store.jn_events as jn_events
#     from store.topics import Topic
#     import store.jn_affinity as jn_affinity

#     # Evento personalizado
#     jn_events.EVENT_MAP["evento_submod"] = Topic(
#         persistent._event_database,
#         label="evento_submod",
#         unlocked=True,
#         conditional="persistent.submod_flag",
#         affinity_range=(jn_affinity.NORMAL, jn_affinity.LOVE)
#     )

# init 5 python in jn_events:
#     # Holiday personalizado
#     _m1_script0x2devents__registerHoliday(JNHoliday(
#         label="holiday_submod",
#         holiday_type=JNHolidayTypes.anniversary,
#         affinity_range=(jn_affinity.HAPPY, None),
#         natsuki_sprite_code="1uchgn",
#         conditional="persistent.submod_flag",
#         deco_list=["deco_submod"],
#         prop_list=["prop_submod"],
#         priority=30
#     ))
# ````


# ## 6. Consideraciones

# - Los holidays solo pueden ejecutarse una vez por año, a menos que se reinicien.
# - Puedes usar cualquier variable persistente o función utilitaria en las condiciones.


# ## Referencias

# - `jn_events.EVENT_MAP`
# - `JNHoliday`
# - `Topic`
# - script-events.rpy





#### ====================================================== ###
#### ------------------- DOCUMENTACION -------------------- ###
#### ====================================================== ###

# Al registrar un tópico usando "registerTopic(Topic(...), topic_group=...)", puedes definir las siguientes variables/argumentos:

# - persistent_db
# Referencia al diccionario persistente donde se guardan los datos del tópico (ej: persistent._topic_database).
# NOTA: para eventos va persistent._event_database y para tópicos normales persistent._topic_database

# - label
# (str)
# Nombre único del label Ren'Py que ejecuta el tópico.

# - prompt
# (str, opcional)
# Texto que se muestra en los menús para este tópico.

# - conditional
# (str, opcional)
# Expresión Python (como string) que debe evaluarse como verdadera para que el tópico esté disponible.

# - category
# (list[str], opcional)
# Lista de categorías para agrupar el tópico en menús.

# - unlocked
# (bool, opcional, default: False)
# Si el tópico está desbloqueado por defecto.

# - nat_says
# (bool, opcional)
# Si Natsuki puede iniciar este tópico.

# - player_says
# (bool, opcional)
# Si el jugador puede iniciar este tópico.

# - affinity_range
# (tuple, opcional)
# Rango de afinidad necesario para que el tópico esté disponible.

# - trust_range
# (tuple, opcional)
# Rango de confianza necesario para que el tópico esté disponible.

# - location
# (str, opcional)
# Ubicación asociada al tópico (ej: "classroom").

# - additional_properties
# (dict, opcional)
# Diccionario de propiedades extra personalizadas para el tópico.
# Es útil para extensiones visuales, custom flags, iconos, etc.

#  ## Propiedades persistentes (se actualizan en runtime)
# - shown_count
# (int)
# Veces que el usuario ha visto este tópico.

# - last_seen
# (datetime)
# Última vez que se mostró el tópico.

# - unlocked_on
# (datetime)
# Fecha/hora en que se desbloqueó el tópico.

# ## - Ejemplo de registro de un tópico

# ```
# init 5 python:
#     registerTopic(
#         Topic(
#             persistent._topic_database,
#             label="mi_topic_ejemplo",
#             prompt="¿Te gusta el helado?",
#             unlocked=True,
#             conditional="persistent.tiene_helado",
#             category=["Comida", "Favoritos"],
#             nat_says=True,
#             player_says=True,
#             affinity_range=(jn_affinity.NORMAL, jn_affinity.LOVE),
#             trust_range=None,
#             location="cafeteria",
#             additional_properties={"icon": "icecream.png"}
#         ),
#         topic_group=TOPIC_TYPE_NORMAL
#     )
# ```

# -- Puedes omitir cualquier argumento opcional si no lo necesitas.
# -- Usa additional_properties para cualquier dato personalizado que tu submod requiera.
# -- Los tópicos se pueden filtrar por afinidad, ubicación, categorías, etc., usando las funciones del sistema base.

# Referencias:
# Clase 'Topic'
# Función 'registerTopic'
# 'topic-handler.rpy'


#### ====================================================== ###
#### ------------------- DOCUMENTACION -------------------- ###
#### ====================================================== ###

# ## Registro de submods

# Para registrar tu submod y que aparezca en el menú de submods:

# ```python
# register_submod(
#     name=_("Mi Submod"),
#     version="1.0",
#     author="Autor",
#     coauthors=["Colaborador1", "Colaborador2"],
#     description=_("Descripción breve del submod.")
# )
# ```