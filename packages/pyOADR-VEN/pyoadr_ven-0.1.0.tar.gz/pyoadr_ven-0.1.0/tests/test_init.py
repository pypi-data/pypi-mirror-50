# import responses
# import requests

# from pyoadr_ven import OpenADRVenAgent
# from pyoadr_ven import models
# from pyoadr_ven.utils import get_aware_utc_now

# from .factories import EventNotStartedYetFactory
# from .factories import EventStartingNowFactory

# VTN_ADDRESS = "https://openadr-staging.carbon.coop"
# ENDPOINT_BASE = "/OpenADR2/Simple/2.0b/"
# ENDPOINT = VTN_ADDRESS + ENDPOINT_BASE
# EIEVENT = ENDPOINT + "EiEvent"
# EIREPORT = ENDPOINT + "EiReport"
# EIREGISTERPARTY = ENDPOINT + "EiRegisterParty"
# POLL = ENDPOINT + "OadrPoll"


# class TestOnstartMethod:
#     # @classmethod
#     def setup_method(cls):
#         cls.agent = OpenADRVenAgent(
#             ven_id="a0af6821-10c7-02e8-7a24-02745ddd3903",
#             vtn_id="ccoopvtn01",
#             vtn_address=VTN_ADDRESS,
#             security_level="standard",
#             poll_interval_secs=15,
#             log_xml=True,
#             opt_in_timeout_secs=3,
#             opt_in_default_decision="optIn",
#             request_events_on_startup=True,
#             report_parameters={},
#             client_pem_bundle="/home/peter/carboncoop/hems/docker/data/carboncoop-hems-shared-data/client.pem",
#             vtn_ca_cert="/home/peter/carboncoop/hems/docker/data/carboncoop-hems-shared-data/ca.crt",
#         )

#     @responses.activate
#     def test_onstart_method_calls_events_endpoint(self):
#         # responses.add(responses.POST, POLL, body="<xml></xml>")
#         # responses.add(responses.POST, EIEVENT, body="<xml></xml>")
#         # responses.add(responses.POST, EIREPORT, body="<xml></xml>")
#         self.agent.onstart_method()
#         assert responses.calls[0].request.url == EIEVENT

#     @responses.activate
#     def test_onstart_method_calls_reports_endpoint(self):
#         # responses.add(responses.POST, POLL, body="<xml></xml>")
#         # responses.add(responses.POST, EIEVENT, body="<xml></xml>")
#         # responses.add(responses.POST, EIREPORT, body="<xml></xml>")
#         self.agent.onstart_method()
#         assert responses.calls[1].request.url == EIREPORT

#     @responses.activate
#     def test_onstart_method_calls_poll_endpoint(self):
#         # responses.add(responses.POST, POLL, body="<xml></xml>")
#         # responses.add(responses.POST, EIEVENT, body="<xml></xml>")
#         # responses.add(responses.POST, EIREPORT, body="<xml></xml>")
#         self.agent.onstart_method()
#         assert responses.calls[2].request.url == POLL
#         assert False


# class TestRunMainProcesses:
#     def setup_class(cls):
#         cls.agent = OpenADRVenAgent(
#             ven_id="a0af6821-10c7-02e8-7a24-02745ddd3903",
#             vtn_id="ccoopvtn01",
#             vtn_address=VTN_ADDRESS,
#             security_level="standard",
#             poll_interval_secs=15,
#             log_xml=True,
#             opt_in_timeout_secs=3,
#             opt_in_default_decision="optIn",
#             request_events_on_startup=True,
#             report_parameters={},
#             client_pem_bundle="/home/peter/carboncoop/hems/docker/data/carboncoop-hems-shared-data/client.pem",
#             vtn_ca_cert="/home/peter/carboncoop/hems/docker/data/carboncoop-hems-shared-data/ca.crt",
#         )
#         cls.agent.onstart_method()

#     @responses.activate
#     def test_run_main_processes_method(self):
#         self.agent.run_main_processes()
#         assert responses.calls[2].request.url == POLL
