#
# Copyright (c) 2013-2019 Quarkslab.
# This file is part of IRMA project.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the top-level directory
# of this distribution and at:
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# No part of the project, including this file, may be copied,
# modified, propagated, or distributed except according to the
# terms contained in the LICENSE file.

from marshmallow import fields, Schema, post_load
from ..csts import ProbeType


class ProbeSchema(Schema):
    name = fields.String()
    display_name = fields.String()
    category = fields.Function(
        serialize=lambda obj: (
            obj.category.value if isinstance(obj.category, ProbeType)
            else obj.category
        ),
        deserialize=lambda obj: obj
    )

    @post_load
    def make_object(self, data):
        return Probe(**data)


class Probe:

    def __init__(self, *, name, display_name, category):
        self.name = name
        self.display_name = display_name
        self.category = ProbeType(category)

    @property
    def id(self):
        # TODO: edit when real probe objects are implemented
        raise NotImplementedError("Not a real Probe object")

    def __repr__(self):
        # TODO: edit when real probe objects are implemented
        return self.__class__.__name__ + "." + self.name

    def __str__(self):
        # TODO: edit when real probe objects are implemented
        ret = "Probe{"
        ret += "name: {}; ".format(self.name)
        ret += "display_name: {}; ".format(self.display_name)
        ret += "category: {}; ".format(self.category.value)
        ret += "}"
        return ret

    def __eq__(self, other):
        # TODO: edit when real probe objects are implemented
        return isinstance(other, Probe) and self.name == other.name

    def __ne__(self, other):
        return not (self == other)
