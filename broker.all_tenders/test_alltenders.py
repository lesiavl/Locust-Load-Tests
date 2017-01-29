#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import requests
import arrow
from datetime import timedelta
from time import sleep

requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.DEBUG)

base_url = 'https://prozorro.shadowy.eu'
login_uri = '/api/v1/user/login'

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


session = requests.session()

session.get(base_url + '/myTender')

login_response = session.post(
        base_url + login_uri,
        json=login_owner_json,
        headers=headers
    )

new_tender_response = session.get(base_url + '/api/v1/tender/new/belowThreshold', headers=headers)
print new_tender_response.status_code


tender_response = session.post(base_url + '/api/v1/tender',
                               json=create_tender_json,
                               headers=headers
                               )
print tender_response.status_code

api_tender_id = tender_response.json()['data']['$id']

get_tender_response = session.get(base_url + '/api/v1/tender/-{}'.format(api_tender_id),
                                  headers=headers
                                  )
print get_tender_response.status_code

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

active_enquiries_response = session.patch(base_url + '/api/v1/tender/orig/{}/active.enquiries'.format(api_tender_id),
                                          json=submit_tender_json,
                                          headers=headers
                                          )
print active_enquiries_response.status_code, active_enquiries_response.content

tender_id = active_enquiries_response.json()['data']['id']
doc_id = active_enquiries_response.json()['data']['$doc_id']
print tender_id, doc_id

get_tender_status = session.get(
    'https://lb.api-sandbox.openprocurement.org/api/2.3/tenders/{}'.format(tender_id)
)

tender_status = get_tender_status.json()['data']['status']

while tender_status != "active.tendering":
    sleep(20)
    r = requests.get('https://lb.api-sandbox.openprocurement.org/api/2.3/tenders/{}'.format(tender_id))
    if r.status_code == 200:
        tender_status = r.json()['data']['status']
        print tender_status

login_provider1_response = session.post(
        base_url + login_uri,
        json=login_provider1_json,
        headers=headers
    )
print login_provider1_response.status_code

prepare_bid_response = session.get(base_url + '/api/v1/user/contact/default',
                                   headers=headers
                                   )
print prepare_bid_response.status_code, prepare_bid_response.content

bid_json = {"value": [{"value": 10000}],
            "contact": {"name": u"гнглнглгн", "telephone": "25645652",
                        "email": "murashkot@bigmir.net", "url": "https://prozorro.shadowy.eu"},
            "features": []}

bid_draft_response = session.post(base_url + '/api/v1/tender/{}/bid'.format(doc_id),
                                  json=bid_json,
                                  headers=headers
                                  )
api_bid_id = bid_draft_response.json()['data']['$id']
print bid_draft_response.status_code, bid_draft_response.content

submit_bid_response = session.post(base_url + '/api/v1/bid/{}/active'.format(api_bid_id),
                                   headers=headers)
print submit_bid_response.status_code, submit_bid_response.content

login_provider2_response = session.post(
        base_url + login_uri,
        json=login_provider2_json,
        headers=headers
    )
print login_provider2_response.status_code, login_provider2_response.content

prepare_bid_response = session.get(base_url + '/api/v1/user/contact/default',
                                   headers=headers
                                   )
print prepare_bid_response.status_code, prepare_bid_response.content

bid_json_2 = {"value": [{"value": 10000}],
              "contact": {"name": u"Сергей", "telephone": "0503580699",
                         "email": "s.titarchuk@a-express.com.ua", "url": "https://prozorro.shadowy.eu"},
              "features": []}

bid_draft_response = session.post(base_url + '/api/v1/tender/{}/bid'.format(doc_id),
                                  json=bid_json_2,
                                  headers=headers
                                  )
print bid_draft_response.status_code, bid_draft_response.content

api_bid_id_2 = bid_draft_response.json()['data']['$id']

submit_bid_response = session.post(base_url + '/api/v1/bid/{}/active'.format(api_bid_id_2),
                                   headers=headers)
print submit_bid_response.status_code

