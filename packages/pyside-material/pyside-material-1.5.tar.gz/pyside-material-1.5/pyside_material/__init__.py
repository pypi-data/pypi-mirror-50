import os
import logging

import jinja2
# from jinja2 import Template

from xml.etree import ElementTree


# from . import resource_rc

# with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resource_rc.py'), 'r') as file:
    # content = file.read()
    # # content = content.replace("#0000ff", theme['primaryColor'])
    # # content = content.replace("#ffff00", theme['secondaryColor'])
    # exec(content)


template = 'material.css.template'
resource = os.path.join('resources', 'resource_rc.py')


# ----------------------------------------------------------------------
def build_stylesheet(theme='', light_secondary=False):
    """"""
    default_theme = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'themes', 'dark_teal.xml')

    if not os.path.exists(theme):

        theme = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'themes', theme)
        if not os.path.exists(theme):

            if theme:
                logging.warning(f"{theme} not exist, using {default_theme} by default.")

            theme = default_theme

    tree = ElementTree.parse(theme)
    theme = {child.attrib['name']: child.text for child in tree.getroot()}

    for k in theme:
        os.environ[str(k)] = theme[k]

    if light_secondary:
        theme['secondaryColor'], theme['secondaryLightColor'], theme['secondaryDarkColor'] = theme['secondaryColor'], theme['secondaryDarkColor'], theme['secondaryLightColor']
        # 'secondaryColor': '#fafafa', 'secondaryLightColor': '#ffffff', 'secondaryDarkColor': '#c7c7c7'

    set_icons_theme(theme)

    loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(os.path.abspath(__file__))))
    env = jinja2.Environment(autoescape=True, loader=loader)

    theme['icon'] = None

    env.filters['opacity'] = opacity
    # env.filters['load'] = load

    stylesheet = env.get_template(template)

    return stylesheet.render(**theme)


# ----------------------------------------------------------------------
def apply_stylesheet(app, theme='', save_as=None, light_secondary=False):
    """"""
    app.setStyle("Fusion")
    stylesheet = build_stylesheet(theme, light_secondary)

    if save_as:
        with open(save_as, 'w') as file:
            file.writelines(stylesheet)

    return app.setStyleSheet(stylesheet)


# ----------------------------------------------------------------------
def opacity(theme, value=0.5):
    """"""
    r, g, b = theme[1:][0:2], theme[1:][2:4], theme[1:][4:]
    r, g, b = int(r, 16), int(g, 16), int(b, 16)

    return f'rgba({r}, {g}, {b}, {value})'


# ----------------------------------------------------------------------
def set_icons_theme(theme):
    """"""
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), resource), 'r') as file:
        content = file.read()

        replaces = (

            ["#0000ff", 'primaryColor'],
            ["#ff0000", 'secondaryLightColor'],

        )

        for color, replace in replaces:
            colors = [color] + [''.join(list(color)[:i] + ['\\\n'] + list(color)[i:]) for i in range(1, 7)]
            for c in colors:
                content = content.replace(c, theme[replace])

        exec(content, globals())


# ----------------------------------------------------------------------
def list_themes():
    """"""
    themes = os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'themes'))
    themes = filter(lambda a: a.endswith('xml'), themes)
    return list(themes)
