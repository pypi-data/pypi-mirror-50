import logging
import pytest
from datetime import timedelta
from pyoadr_ven import OpenADRVenAgent
from pyoadr_ven import models
from pyoadr_ven.utils import get_aware_utc_now

from .factories import EventNotStartedYetFactory
from .factories import EventStartingNowFactory


class TestEventStatuses:
    def setup_class(cls):
        cls.agent = OpenADRVenAgent(
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

    def test_active_or_pending_events(self, caplog):
        caplog.set_level(logging.DEBUG)
        event1 = EventStartingNowFactory()
        event2 = EventStartingNowFactory()
        event3 = EventNotStartedYetFactory()
        self.agent.add_event(event1)
        self.agent.add_event(event2)
        self.agent.add_event(event3)

        self.agent.process_event(event1)
        self.agent.process_event(event2)
        self.agent.process_event(event3)
        assert self.agent.active_or_pending_events() == [event1, event2, event3]

    @pytest.mark.skip()
    def test_active_events(self, caplog):
        event1 = EventStartingNowFactory()
        event2 = EventStartingNowFactory()
        event1.opt_type = "optIn"
        self.agent.add_event(event1)
        self.agent.add_event(event2)
        self.agent.process_event(event1)
        self.agent.process_event(event2)

        assert self.agent.active_events() == [event1]
