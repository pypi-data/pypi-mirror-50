from datetime import timedelta

import factory
from pyoadr_ven import models
from pyoadr_ven.utils import get_aware_utc_now


class EventStartingNowFactory(factory.Factory):
    class Meta:
        model = models.EiEvent
        model.start_time = get_aware_utc_now()
        model.end_time = model.start_time + timedelta(hours=1)
        # model.opt_type = "optIn"

    request_id = factory.Sequence(lambda n: "request_%d" % n)
    event_id = factory.Sequence(lambda n: "event_%d" % n)


class EventNotStartedYetFactory(factory.Factory):
    class Meta:
        model = models.EiEvent
        model.start_time = get_aware_utc_now() + timedelta(hours=1)
        model.end_time = model.start_time + timedelta(hours=1)
        # model.opt_type = "optIn"

    request_id = factory.Sequence(lambda n: "request_%d" % n)
    event_id = factory.Sequence(lambda n: "event_%d" % n)
    # start_time = get_aware_utc_now()
    # end_time = start_time + timedelta(hours=1)
    # opt_type = "optIn"
