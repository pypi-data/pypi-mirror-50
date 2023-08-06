from __future__ import print_function, absolute_import

from .entity_selector import EntitySelector
from ipywidgets import Button, jslink, VBox, Widget, Output


class widget:
    txt = Button(
        # button_style='info',
        description='Done',
        icon='check'
    )

    res = ''

    def __init__(self, str_1, str_2, func):
        super().__init__()
        self.es = EntitySelector(str_1, str_2)
        self.link = jslink((self.es, 'res'), (self.txt, 'tooltip'))
        self.txt._click_handlers.callbacks = []
        self.txt.on_click(func, remove=True)
        self.txt.on_click(func)

    def __repr__(self):
        display(VBox((self.es, self.txt)))
        return ''

    # def display(self):
    #     display(VBox((self.es, self.txt)))
    #     while self.res == '':
    #         pass
    #     return self.res
    #
    # def hook(self, btn):
    #     self.res = self.es.res
    #     print(self.es.res)
    #     print(btn.description)
    #     return self.es.res
