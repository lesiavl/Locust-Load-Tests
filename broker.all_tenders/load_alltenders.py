#!/usr/bin/env python
# -*- coding: utf-8 -*-

from locust import HttpLocust, TaskSet, task
from locust.clients import HttpSession
import requests
from time import sleep
import arrow
from datetime import timedelta
import logging

# http://www.accept-online.com.ua
requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.DEBUG)

headers = {'Content-Type': 'application/json'}

login_owner_json = {'login': "butov@mail.ru", 'password': "111"}
login_provider1_json = {"login": "murashkot@bigmir.net", "password": "24091980"}
login_provider2_json = {"login": "s.titarchuk@a-express.com.ua", "password": "gfhjkm"}

create_tender_json = {"id": None, "$is_plan": False,
                      "$date": "{}".format(arrow.now()),
                      "items": [{"description": "BelowThreshold_LOAD",
                                 "classification": {"scheme": "CPV","id": "03111000-2", "description": u"Насіння"},
                                 "additionalClassifications": [{"scheme": u"ДКПП", "id": "01.11.1", "description": u"Пшениця"}],
                                 "unit": {"code": "NMP", "name": u"пачок"},
                                 "quantity": 130,
                                 "deliveryAddress": {"streetAddress": u"01034, м.Київ, Шевченківський район, ВУЛИЦЯ ЯРОСЛАВІВ ВАЛ, будинок 38", "locality": u"киев", "region": u"киевская", "postalCode": "01034", "countryName": u"Україна"},
                                 "deliveryDate": {"startDate": "{}".format(arrow.now() + timedelta(days=2)), "endDate": "{}".format(arrow.now() + timedelta(days=3))},
                                 "id": "5f0d1afead1e44a8b6a45c2be35541a2"}],
                       "title": "BelowThreshold_LOAD", "description": "BelowThreshold_LOAD",
                       "procurementMethodType": "belowThreshold",
                       "value": {"amount": 10000, "currency": "UAH", "valueAddedTaxIncluded": False},
                       "minimalStep": {"amount": 50, "currency": "UAH", "valueAddedTaxIncluded": False},
                       "$status": "draft",
                       "tenderID": None,
                       "enquiryPeriod": {"startDate": "{}".format(arrow.now() + timedelta(minutes=2)),
                                         "endDate": "{}".format(arrow.now() + timedelta(minutes=4))},
                       "tenderPeriod": {"startDate": "{}".format(arrow.now() + timedelta(minutes=6)),
                                        "endDate": "{}".format(arrow.now() + timedelta(hours=1))},
                       "procuringEntity": {"kind": "general", "name": u"ТОВАРИСТВО З ОБМЕЖЕНОЮ ВІДПОВІДАЛЬНІСТЮ \"ПАУЕР ГРУП\"",
                                          "address":
                                              {"region": u"киевская", "locality": u"киев", "postalCode": "01034", "countryName": u"Україна", "streetAddress": u"01034, м.Київ, Шевченківський район, ВУЛИЦЯ ЯРОСЛАВІВ ВАЛ, будинок 38"},
                                          "name_en": u"LTD \"Pauer group\"",
                                          "identifier": {"id": "35592115", "scheme": "UA-EDR", "legalName": u"ТОВАРИСТВО З ОБМЕЖЕНОЮ ВІДПОВІДАЛЬНІСТЮ \"ПАУЕР ГРУП\"", "legalName_en": "LTD \"Pauer group\""},
                                          "contactPoint": {"url": "http://conan.com", "name": u"Конан Варвар", "email": "barbarian@conan.com", "faxNumber": "333222333", "telephone": "222333222"}},
                       "mode": "test"}

bid_json = {"value": [{"value": 10000}],
            "contact": {"name": u"гнглнглгн", "telephone": "25645652",
                        "email": "murashkot@bigmir.net", "url": "https://prozorro.shadowy.eu"},
            "features": []}

bid_json_2 = {"value": [{"value": 10000}],
              "contact": {"name": u"Сергей", "telephone": "0503580699",
                         "email": "s.titarchuk@a-express.com.ua", "url": "https://prozorro.shadowy.eu"},
              "features": []}

login_uri = '/api/v1/user/login'
draft_tender_uri = '/api/1.0/fe/tenders-draft'


class WebsiteTasks(TaskSet):

    @task
    def create_tender(self):
        with self.client.get('/myTender',
                             data=login_owner_json,
                             catch_response=True) as get_cookie:

            if get_cookie.status_code == 200:
                get_cookie.success()
            else:
                get_cookie.failure("Fail")

        with self.client.post(login_uri,
                              data=login_owner_json,
                              headers=headers,
                              catch_response=True) as login_response:

            if login_response.status_code == 200:
                login_response.success()
            else:
                login_response.failure("Not authorized")

        with self.client.get('/api/v1/tender/new/belowThreshold',
                             headers=headers,
                             catch_response=True) as new_tender_response:

            if new_tender_response.status_code == 200:
                new_tender_response.success()
            else:
                new_tender_response.failure("Fail")

        with open('locust_results.txt', 'a') as f:
            f.write('{} -------- STARTED\n'.format(arrow.now().format('DD.MM.YYYY HH:mm:ss')))
            f.close()

        with self.client.post('/api/v1/tender',
                              json=create_tender_json,
                              headers=headers,
                              catch_response=True) as tender_response:

            if tender_response.status_code == 200:
                tender_response.success()
            else:
                tender_response.failure("Fail")

            api_tender_id = tender_response.json()['data']['$id']

        with self.client.get('/api/v1/tender/-{}'.format(api_tender_id),
                             headers=headers,
                             catch_response=True) as get_tender_response:

            if get_tender_response.status_code == 200:
                get_tender_response.success()
            else:
                get_tender_response.failure("Fail")

        submit_tender_json = {"id": None,
                              "$id": api_tender_id,
                              "mode": "test", "$date": "{}".format(arrow.now()),
                              "items": [{"id": "5f0d1afead1e44a8b6a45c2be35541a2",
                                         "unit": {"code": "NMP", "name": u"пачок"},
                                         "quantity": 130, "description": "BelowThreshold_LOAD",
                                         "deliveryDate": {"endDate": "{}".format(arrow.now() + timedelta(days=3)),
                                                          "startDate": "{}".format(arrow.now() + timedelta(days=2))},
                                         "classification": {"scheme": "CPV", "id": "03111000-2",
                                                            "description": u"Насіння"},
                                         "additionalClassifications": [
                                             {"scheme": u"ДКПП", "id": "01.11.1", "description": u"Пшениця"}],
                                         "deliveryAddress": {
                                             "streetAddress": u"01034, м.Київ, Шевченківський район, ВУЛИЦЯ ЯРОСЛАВІВ ВАЛ, будинок 38",
                                             "locality": u"киев", "region": u"киевская", "postalCode": "01034",
                                             "countryName": u"Україна"}}],

                              "title": "BelowThreshold_LOAD",
                              "value": {"amount": 10000, "currency": "UAH", "valueAddedTaxIncluded": False},
                              "$doc_id": None, "$status": "draft", "$is_plan": False, "tenderID": None,
                              "description": "BelowThreshold_LOAD",
                              "minimalStep": {"amount": 50, "currency": "UAH", "valueAddedTaxIncluded": False},
                              "enquiryPeriod": {"endDate": "{}".format(arrow.now() + timedelta(minutes=4)),
                                                "startDate": "{}".format(arrow.now() + timedelta(minutes=2))},
                              "tenderPeriod": {"endDate": "{}".format(arrow.now() + timedelta(hours=1)),
                                               "startDate": "{}".format(arrow.now() + timedelta(minutes=6))},

                              "procuringEntity": {"kind": "general",
                                                  "name": u"ТОВАРИСТВО З ОБМЕЖЕНОЮ ВІДПОВІДАЛЬНІСТЮ \"ПАУЕР ГРУП\"",
                                                  "address": {"region": u"киевская", "locality": u"киев",
                                                              "postalCode": "01034", "countryName": u"Україна",
                                                              "streetAddress": u"01034, м.Київ, Шевченківський район, ВУЛИЦЯ ЯРОСЛАВІВ ВАЛ, будинок 38"},
                                                  "name_en": u"LTD \"Pauer group\"",
                                                  "identifier": {"id": "35592115", "scheme": "UA-EDR",
                                                                 "legalName": u"ТОВАРИСТВО З ОБМЕЖЕНОЮ ВІДПОВІДАЛЬНІСТЮ \"ПАУЕР ГРУП\"",
                                                                 "legalName_en": u"LTD \"Pauer group\""},
                                                  "contactPoint": {"url": "http://conan.com", "name": u"Конан Варвар",
                                                                   "email": "barbarian@conan.com",
                                                                   "faxNumber": "333222333", "telephone": "222333222"}},
                              "procurementMethodType": "belowThreshold"}

        with self.client.patch('/api/v1/tender/orig/{}/active.enquiries'.format(api_tender_id),
                               json=submit_tender_json,
                               headers=headers,
                               catch_response=True) as active_enquiries_response:

            if active_enquiries_response.status_code == 200:
                active_enquiries_response.success()
            else:
                active_enquiries_response.failure("Fail")

        tender_id = active_enquiries_response.json()['data']['id']
        doc_id = active_enquiries_response.json()['data']['$doc_id']
        print tender_id, doc_id

        with open('locust_results.txt', 'a') as f:
            f.write(
                '{} at {} —--------- FINISHED\n'.format(tender_id, arrow.now().format('DD.MM.YYYY HH:mm:ss')))
            f.close()

    @task
    def create_tender_make_bid(self):

        with self.client.get('/myTender',
                             data=login_owner_json,
                             catch_response=True) as get_cookie:

            if get_cookie.status_code == 200:
                get_cookie.success()
            else:
                get_cookie.failure("Fail")

        with self.client.post(login_uri,
                              data=login_owner_json,
                              headers=headers,
                              catch_response=True) as login_response:

            if login_response.status_code == 200:
                login_response.success()
            else:
                login_response.failure("Not authorized")

        with self.client.get('/api/v1/tender/new/belowThreshold',
                             headers=headers,
                             catch_response=True) as new_tender_response:

            if new_tender_response.status_code == 200:
                new_tender_response.success()
            else:
                new_tender_response.failure("Fail")

        with open('locust_results.txt', 'a') as f:
            f.write('{} -------- STARTED\n'.format(arrow.now().format('DD.MM.YYYY HH:mm:ss')))
            f.close()

        with self.client.post('/api/v1/tender',
                              json=create_tender_json,
                              headers=headers,
                              catch_response=True) as tender_response:

            if tender_response.status_code == 200:
                tender_response.success()
            else:
                tender_response.failure("Fail")

            api_tender_id = tender_response.json()['data']['$id']

        with self.client.get('/api/v1/tender/-{}'.format(api_tender_id),
                             headers=headers,
                             catch_response=True) as get_tender_response:

            if get_tender_response.status_code == 200:
                get_tender_response.success()
            else:
                get_tender_response.failure("Fail")

        submit_tender_json = {"id": None,
                              "$id": api_tender_id,
                              "mode": "test", "$date": "{}".format(arrow.now()),
                              "items": [{"id": "5f0d1afead1e44a8b6a45c2be35541a2",
                                        "unit": {"code": "NMP", "name": u"пачок"},
                                        "quantity": 130, "description":"BelowThreshold_LOAD",
                                        "deliveryDate":{"endDate": "{}".format(arrow.now() + timedelta(days=3)), "startDate": "{}".format(arrow.now() + timedelta(days=2))},
                                        "classification": {"scheme": "CPV","id": "03111000-2", "description": u"Насіння"},
                                        "additionalClassifications": [{"scheme": u"ДКПП", "id": "01.11.1", "description": u"Пшениця"}],
                                        "deliveryAddress": {"streetAddress": u"01034, м.Київ, Шевченківський район, ВУЛИЦЯ ЯРОСЛАВІВ ВАЛ, будинок 38", "locality": u"киев", "region": u"киевская", "postalCode": "01034", "countryName": u"Україна"}}],

                              "title": "BelowThreshold_LOAD", "value": {"amount": 10000, "currency": "UAH", "valueAddedTaxIncluded": False},
                              "$doc_id": None, "$status": "draft", "$is_plan": False, "tenderID": None, "description": "BelowThreshold_LOAD",
                              "minimalStep": {"amount": 50, "currency": "UAH","valueAddedTaxIncluded": False},
                              "enquiryPeriod": {"endDate": "{}".format(arrow.now() + timedelta(minutes=4)),
                                                "startDate": "{}".format(arrow.now() + timedelta(minutes=2))},
                              "tenderPeriod": {"endDate": "{}".format(arrow.now() + timedelta(hours=1)),
                                               "startDate": "{}".format(arrow.now() + timedelta(minutes=6))},

                              "procuringEntity": {"kind": "general", "name": u"ТОВАРИСТВО З ОБМЕЖЕНОЮ ВІДПОВІДАЛЬНІСТЮ \"ПАУЕР ГРУП\"",
                                                     "address": {"region": u"киевская", "locality": u"киев", "postalCode": "01034", "countryName": u"Україна",
                                                                "streetAddress": u"01034, м.Київ, Шевченківський район, ВУЛИЦЯ ЯРОСЛАВІВ ВАЛ, будинок 38"},
                                                     "name_en": u"LTD \"Pauer group\"",
                                                     "identifier": {"id": "35592115", "scheme": "UA-EDR", "legalName": u"ТОВАРИСТВО З ОБМЕЖЕНОЮ ВІДПОВІДАЛЬНІСТЮ \"ПАУЕР ГРУП\"", "legalName_en": u"LTD \"Pauer group\""},
                                                     "contactPoint": {"url": "http://conan.com", "name": u"Конан Варвар","email": "barbarian@conan.com", "faxNumber": "333222333", "telephone": "222333222"}},
                              "procurementMethodType": "belowThreshold"}

        with self.client.patch('/api/v1/tender/orig/{}/active.enquiries'.format(api_tender_id),
                               json=submit_tender_json,
                               headers=headers,
                               catch_response=True) as active_enquiries_response:

            if active_enquiries_response.status_code == 200:
                active_enquiries_response.success()
            else:
                active_enquiries_response.failure("Fail")

        tender_id = active_enquiries_response.json()['data']['id']
        doc_id = active_enquiries_response.json()['data']['$doc_id']
        print tender_id, doc_id

        with open('locust_results.txt', 'a') as f:
            f.write(
                '{} at {} —--------- FINISHED\n'.format(tender_id, arrow.now().format('DD.MM.YYYY HH:mm:ss')))
            f.close()

        get_tender_status = requests.get('https://lb.api-sandbox.openprocurement.org/api/2.3/tenders/{}'.format(tender_id))
        tender_status = get_tender_status.json()['data']['status']

        while tender_status != "active.tendering":
            sleep(20)
            r = requests.get('https://lb.api-sandbox.openprocurement.org/api/2.3/tenders/{}'.format(tender_id))
            if r.status_code == 200:
                tender_status = r.json()['data']['status']
                print tender_status

        with self.client.post(login_uri,
                              data=login_provider1_json,
                              headers=headers,
                              catch_response=True) as login_provider1_response:

            if login_provider1_response.status_code == 200:
                login_provider1_response.success()
            else:
                login_provider1_response.failure("Not authorized")

        with self.client.get('/api/v1/user/contact/default',
                             headers=headers,
                             catch_response=True) as prepare_bid_response:

            if prepare_bid_response.status_code == 200:
                prepare_bid_response.success()
            else:
                prepare_bid_response.failure("Fail")

        with self.client.post('/api/v1/tender/{}/bid'.format(doc_id),
                              json=bid_json,
                              headers=headers,
                              catch_response=True) as bid_draft_response:

            if bid_draft_response.status_code == 200:
                bid_draft_response.success()
            else:
                bid_draft_response.failure("Fail")

        api_bid_id = bid_draft_response.json()['data']['$id']

        with self.client.post('/api/v1/bid/{}/active'.format(api_bid_id),
                              headers=headers,
                              catch_response=True) as submit_bid_response:

            if submit_bid_response.status_code == 200:
                submit_bid_response.success()
            else:
                submit_bid_response.failure("Fail")

        with self.client.post(login_uri,
                              data=login_provider2_json,
                              headers=headers,
                              catch_response=True) as login_provider2_response:

            if login_provider2_response.status_code == 200:
                login_provider2_response.success()
            else:
                login_provider2_response.failure("Not authorized")

        with self.client.get('/api/v1/user/contact/default',
                             headers=headers,
                             catch_response=True) as prepare_bid2_response:

            if prepare_bid2_response.status_code == 200:
                prepare_bid2_response.success()
            else:
                prepare_bid2_response.failure("Fail")

        with self.client.post('/api/v1/tender/{}/bid'.format(doc_id),
                              json=bid_json,
                              headers=headers,
                              catch_response=True) as bid2_draft_response:

            if bid2_draft_response.status_code == 200:
                bid2_draft_response.success()
            else:
                bid2_draft_response.failure("Fail")

        api_bid_id_2 = bid_draft_response.json()['data']['$id']

        with self.client.post('/api/v1/bid/{}/active'.format(api_bid_id_2),
                              headers=headers,
                              catch_response=True) as submit_bid2_response:

            if submit_bid2_response.status_code == 200:
                submit_bid2_response.success()
            else:
                submit_bid2_response.failure("Fail")
