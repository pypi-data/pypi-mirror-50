# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class ColorPickerBox(Component):
    """A ColorPickerBox component.
A box for color picker.

Keyword arguments:
- id (string; optional): The ID used to identify the color picker in Dash callbacks
- value (optional): Color value of the picker. value has the following type: dict containing keys 'hex', 'rbg'.
Those keys have the following types:
  - hex (string; optional): Hex string
  - rbg (optional): RGB/RGBA object. rbg has the following type: dict containing keys 'r', 'g', 'b', 'a'.
Those keys have the following types:
  - r (number; optional)
  - g (number; optional)
  - b (number; optional)
  - a (number; optional)
- disabled (boolean; optional): If true, disable color picking
- className (string; optional): Class to apply to the root component element
- style (dict; optional): Style to apply to the root component element
- label (string; optional): Label on top of the component"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, value=Component.UNDEFINED, disabled=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, label=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'value', 'disabled', 'className', 'style', 'label']
        self._type = 'ColorPickerBox'
        self._namespace = 'colorpicker_box'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'value', 'disabled', 'className', 'style', 'label']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(ColorPickerBox, self).__init__(**args)
