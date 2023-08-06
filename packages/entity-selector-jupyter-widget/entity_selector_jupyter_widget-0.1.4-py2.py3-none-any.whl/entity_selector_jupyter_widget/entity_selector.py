from __future__ import print_function

import ipywidgets as widgets
from traitlets import Unicode, List


@widgets.register
class EntitySelector(widgets.DOMWidget):
    _view_name = Unicode('EntitySelectorView').tag(sync=True)
    _model_name = Unicode('EntitySelectorModel').tag(sync=True)
    _view_module = Unicode('frontend_entity_selector_jupyter_widget').tag(sync=True)
    _model_module = Unicode('frontend_entity_selector_jupyter_widget').tag(sync=True)
    _view_module_version = Unicode('^0.0.1').tag(sync=True)
    _model_module_version = Unicode('^0.0.1').tag(sync=True)
    text = Unicode('').tag(sync=True)
    search = List().tag(sync=True)
    res = Unicode('').tag(sync=True)
    input_str = Unicode('')
    input_list = List()

    def __init__(self, input_str, input_list):
        super().__init__()
        # super(EntitySelector, self).__init__()
        self.search = input_str
        self.text = input_list

