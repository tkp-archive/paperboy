import json
from six import string_types
from traitlets import List, Unicode, Bool, TraitType

_DOM_IMPLEMENTED = ('text', 'select', 'label', 'button', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span')
_FORM_IMPLEMENTED = ('file', 'text', 'select', 'label', 'submit', 'datetime', 'autocomplete', 'checkbox', 'textarea')


class DOMElement(TraitType):
    default_value = 'text'
    info_text = 'an dom element'

    def validate(self, obj, value):
        if not isinstance(value, string_types):
            self.error(obj, value)
        if value not in _DOM_IMPLEMENTED:
            self.error(obj, value)
        return value


class FormElement(TraitType):
    default_value = 'text'
    info_text = 'an dom element'

    def validate(self, obj, value):
        if not isinstance(value, string_types):
            self.error(obj, value)
        if value not in _FORM_IMPLEMENTED:
            self.error(obj, value)
        return value


class FormEntry(TraitType):
    name = Unicode(allow_none=False)
    type = FormElement()
    value = Unicode(default_value='')
    label = Unicode(allow_none=True)
    placeholder = Unicode(allow_none=True)
    options = List(default_value=[])
    required = Bool(default_value=False)
    readonly = Bool(default_value=False)

    def to_json(self, string=False):
        ret = {}
        ret['name'] = self.name
        ret['type'] = self.type
        if self.value:
            ret['value'] = self.value
        if self.label:
            ret['label'] = self.label
        if self.placeholder:
            ret['placeholder'] = self.placeholder
        if self.options:
            ret['options'] = self.options
        if self.required:
            ret['required'] = self.required
        if self.readonly:
            ret['readonly'] = self.readonly
        if string:
            return json.dumps(ret)
        return ret


class DOMEntry(TraitType):
    name = Unicode(allow_none=False)
    type = DOMElement()
    value = Unicode(default_value='')
    label = Unicode(allow_none=True)
    placeholder = Unicode(allow_none=True)
    options = List(default_value=[])
    required = Bool(default_value=False)
    readonly = Bool(default_value=False)

    def to_json(self, string=False):
        ret = {}
        ret['name'] = self.type
        ret['type'] = self.type
        if self.value:
            ret['value'] = self.value
        if self.label:
            ret['label'] = self.label
        if self.placeholder:
            ret['placeholder'] = self.placeholder
        if self.options:
            ret['options'] = self.options
        if self.required:
            ret['required'] = self.required
        if self.readonly:
            ret['readonly'] = self.readonly
        ret = {}
        ret[self.name] = ret

        if string:
            return json.dumps(ret)
        return ret


class Form(TraitType):
    entries = List(trait=FormEntry)

    def to_json(self, string=False):
        ret = {}
        for entry in self.entries:
            ret.update(entry.to_json())
        if string:
            return json.dumps(ret)
        return ret


class Response(TraitType):
    entries = List(trait=DOMEntry)

    def to_json(self, string=False):
        ret = {}
        for entry in self.entries:
            ret.update(entry.to_json())
        if string:
            return json.dumps(ret)
        return ret
