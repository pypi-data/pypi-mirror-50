import factory

from pyoadr_ven import models


class EventFactory(factory.Factory):
    class Meta:
        model = models.EiEvent

    request_id = factory.Sequence(lambda n: "request_%d" % n)
    event_id = factory.Sequence(lambda n: "event_%d" % n)
