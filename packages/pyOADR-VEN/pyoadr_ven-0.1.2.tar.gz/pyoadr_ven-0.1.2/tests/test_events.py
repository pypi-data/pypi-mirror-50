import logging
from datetime import timedelta

import pytest

from .factories import EventFactory
from pyoadr_ven import OpenADRVenAgent
from pyoadr_ven.utils import get_aware_utc_now

_LOGGER = logging.getLogger(__name__)


def event_started_opted_in():
    event = EventFactory()
    event.start_time = get_aware_utc_now() - timedelta(minutes=30)
    event.end_time = event.start_time + timedelta(hours=1)
    event.opt_type = "optIn"
    return event


def event_started_unresponded():
    event = EventFactory()
    event.start_time = get_aware_utc_now() - timedelta(minutes=30)
    event.end_time = event.start_time + timedelta(hours=1)
    return event


def event_not_started_opted_in():
    event = EventFactory()
    event.start_time = get_aware_utc_now() + timedelta(minutes=30)
    event.end_time = event.start_time + timedelta(hours=1)
    event.opt_type = "optIn"
    return event


def event_not_started_unresponded():
    event = EventFactory()
    event.start_time = get_aware_utc_now() + timedelta(minutes=30)
    event.end_time = event.start_time + timedelta(hours=1)
    return event


class TestEventStatuses:
    def setup_method(self, method):
        self.agent = OpenADRVenAgent(
            ven_id="a0af6821-10c7-02e8-7a24-02745ddd3903",
            vtn_id="ccoopvtn01",
            vtn_address="http://booma.local",
            security_level="standard",
            poll_interval_secs=15,
            log_xml=True,
            opt_in_timeout_secs=3,
            opt_in_default_decision="optIn",
            request_events_on_startup=True,
            report_parameters={},
            client_pem_bundle="/home/peter/carboncoop/hems/docker/data/carboncoop-hems-shared-data/client.pem",
            vtn_ca_cert="/home/peter/carboncoop/hems/docker/data/carboncoop-hems-shared-data/ca.crt",
        )

    def teardown_method(self, method):
        _LOGGER.info("TEARDOWN CALLED")
        self.agent = None

    def test_active_or_pending_events(self, caplog):
        caplog.set_level(logging.DEBUG)
        event1 = event_not_started_opted_in()
        event2 = event_started_opted_in()
        event3 = event_not_started_unresponded()
        event4 = event_started_unresponded()
        assert self.agent.active_or_pending_events() == []

        self.agent.add_event(event1)
        self.agent.add_event(event2)
        self.agent.add_event(event3)
        self.agent.add_event(event4)
        assert self.agent.active_or_pending_events()[0] == event1
        assert self.agent.active_or_pending_events()[1] == event2
        assert self.agent.active_or_pending_events()[2] == event3
        assert self.agent.active_or_pending_events()[3] == event4

        assert self.agent.active_or_pending_events() == [event1, event2, event3, event4]

        self.agent.process_event(event1)
        self.agent.process_event(event2)
        self.agent.process_event(event3)
        self.agent.process_event(event4)

        assert self.agent.active_or_pending_events()[0] == event2
        assert self.agent.active_or_pending_events()[1] == event1
        assert self.agent.active_or_pending_events()[2] == event3
        assert self.agent.active_or_pending_events()[3] == event4

    @pytest.mark.skip()
    def test_active_events(self, caplog):
        caplog.set_level(logging.DEBUG)

        event1 = event_not_started_opted_in()
        event2 = event_started_opted_in()
        event3 = event_not_started_unresponded()
        event4 = event_started_unresponded()
        self.agent.add_event(event1)
        self.agent.add_event(event2)
        self.agent.add_event(event3)
        self.agent.add_event(event4)
        self.agent.process_event(event1)
        self.agent.process_event(event2)
        self.agent.process_event(event3)
        self.agent.process_event(event4)
        assert len(self.agent.active_or_pending_events()) == 4
        assert self.agent.active_events() == [event2]
