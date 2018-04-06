from flask_apidoc import ApiDoc
from api import api

doc = ApiDoc(app=api)


# Predefined
"""
@apiDefine GetItemsSuccess
@apiSuccess {Dict}  result  [list of dicts with items parameters].
@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
      "result": [
        {"id": 1, ... },
        {"id": 2, ... },
        ...
      ]
    }
"""
"""
@apiDefine GetItemSuccess
@apiSuccess {Dict}  result  {"dict of item's params"}
"""
"""
@apiDefine DelItemSuccess
@apiSuccess {Boolean}  result  True or False if item with id is present but couldn't be deleted (e.g. in relative DBMS).
@apiSuccessExample Success-Response false:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
      "result": false
    }
@apiSuccessExample Success-Response true:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
      "result": true
    }
"""
"""
@apiDefine PostItemSuccess
@apiSuccess {Integer}  result  The new item id.
@apiSuccessExample Success-Response true:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
      "result": 5
    }
"""
"""
@apiDefine PutItemSuccess
@apiSuccess {Dict}  result  {"dict of item's params"} - See "Get an item by id"
"""
"""
@apiDefine Error404
@apiError(Error 404){Dict}  NotFound    {"error": "Not found"}
@apiErrorExample {json} Error-Response:
    HTTP/1.0 404 NOT FOUND
    Content-Type: application/json
    {
      "error": "Not found"
    }
"""
"""
@apiDefine Error400
@apiError(Error 400){Dict}  JSONNotFound    {"error": "JSON not found"}
@apiError(Error 400){Dict}  ValidationError    {"field": "error"}
@apiErrorExample {json} Error-Response JSON:
    HTTP/1.0 400 BAD REQUEST
    Content-Type: application/json
    {
      "error": "JSON not found"
    }
@apiErrorExample {json} Error-Response validation:
    HTTP/1.0 400 BAD REQUEST
    Content-Type: application/json
    {
      "name": "field \\"name\\" is required"
    }
"""

# General (example)
"""
@api {get} /<path> Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup General
@apiExample {curl} Example usage:
    curl -i http://localhost:8001/api/v1.0/<path>/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /<path>/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup General
@apiExample {curl} Example usage:
    curl -i http://localhost:8001/api/v1.0/<path>/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
    "result": {
        "id": 1,
        "name": "some name",
        ...
        }
    }

@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /<path>/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup General
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name": "some name"}' \
         http://localhost:8001/api/v1.0/<path>/

@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /<path>/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup General
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}' \
         http://localhost:8001/api/v1.0/<path>/10

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /<path>/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup General
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/<path>/10

@apiUse DelItemSuccess
@apiUse Error404
"""


# Users
"""
@api {get} /user Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup user
@apiExample {curl} Example usage:
    curl -i http://localhost:8001/api/v1.0/user/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /user/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup user
@apiExample {curl} Example usage:
    curl -i http://localhost:8001/api/v1.0/user/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
    "result": {
        "active": true,
        "country": null,
        "id": 1,
        ...
        "created": [
          "2015-10-02",
          "15:35:40"
        ],
        "roles": [
            {
                "description": "admin",
                "id": 1,
                "name": "admin"
            },
            {
                "description": "user",
                "id": 2,
                "name": "user"
            },
        ],
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(50)}    name
@apiSuccess {String(50)}    alias
@apiSuccess {String(120)}   email
@apiSuccess {Integer}       status
@apiSuccess {String(255)}   address
@apiSuccess {String(50)}    mobile
@apiSuccess {String(255)}   website
@apiSuccess {String(255)}   country
@apiSuccess {String(255)}   photo
@apiSuccess {String}        description
@apiSuccess {Boolean}       active
@apiSuccess {Boolean}       confirmed
@apiSuccess {Datetime}      confirmed_at
@apiSuccess {Datetime}      created
@apiSuccess {Datetime}      updated
@apiSuccess {List}          roles       [list of dicts with items parameters] - see: role->get list of items
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /user/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup user
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST \
         -d '{"alias":"user", "email":"user@example.com", "password":"my_very_secure_password"}' \
         http://localhost:8001/api/v1.0/user/

@apiParam   {String(50)}    name
@apiParam   {String(50)}    alias       required
@apiParam   {String(120)}   email       required
@apiParam   {String(50)}    password    required
@apiParam   {Integer}       status
@apiParam   {String(255)}   address
@apiParam   {String(50)}    mobile
@apiParam   {String(255)}   website
@apiParam   {String(255)}   country
@apiParam   {String(255)}   photo
@apiParam   {String}        description
@apiParam   {Boolean}       active
@apiParam   {Boolean}       confirmed
@apiParam   {Datetime}      confirmed_at    format "2016-07-29 17:52:19"
@apiParam   {Datetime}      created         format "2016-07-29 17:52:19"
@apiParam   {Datetime}      updated         format "2016-07-29 17:52:19"
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /user/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup user
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"alias":"user1"}' http://localhost:8001/api/v1.0/user/10

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /user/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup user
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/user/10

@apiUse DelItemSuccess
@apiUse Error404
"""


# Equipment
"""
@api {get} /equipment Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup equipment
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/equipment/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /equipment/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup equipment
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/equipment/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {"id": 1,
                   "name": "Air Breaker",
                   "equipment_number": "123ABC456",
                   ...
                   "prev_equipment_number": "789WSX159",
                   "sibling": 1,
                   }
    }

@apiUse GetItemSuccess

@apiSuccess {Integer}         id
@apiSuccess {String(50)}      name
@apiSuccess {String(50)}      equipment_number
@apiSuccess {String(50)}      serial
@apiSuccess {Integer}         equipment_type_id
@apiSuccess {Dict}            equipment_type              see: equipment_type->get an item
@apiSuccess {Integer}         manufacturer_id
@apiSuccess {Dict}            manufacturer                see: manufacturer->get an item
@apiSuccess {Integer}         manufactured                Year manufactured, from 1900
@apiSuccess {String}          frequency                   allowed: '25', '50', '60' or 'DC'
@apiSuccess {String}          description
@apiSuccess {Integer}         location_id
@apiSuccess {Dict}            location                    see: location->get an item
@apiSuccess {Boolean}         modifier
@apiSuccess {String}          comments
@apiSuccess {Integer}         assigned_to_id              User
@apiSuccess {Dict}            assigned_to                 see: user->get an item
@apiSuccess {String}          nbr_of_tap_change_ltc       Number of tap change on LTC
@apiSuccess {Integer}         tie_status                  TieAnalysisState.
@apiSuccess {Integer}         status                      EquipmentState.
@apiSuccess {Integer}         phys_position
@apiSuccess {Float}           tension4                    Voltage4
@apiSuccess {Boolean}         validated
@apiSuccess {Boolean}         invalidation
@apiSuccess {String(50)}      prev_serial_number
@apiSuccess {String(50)}      prev_equipment_number
@apiSuccess {Integer}         sibling

@apiUse Error404
"""
"""
@api {post} /equipment Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup equipment
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST \
         -d '{"equipment_number":"987abc", "equipment_type_id":1, "location_id":4, \
              "assigned_to_id": 4, "frequency":"25", "name": "Name"}' \
          http://localhost:8001/api/v1.0/equipment/

@apiParam {String(50)}      name                        Required.
@apiParam {String(50)}      equipment_number            Required.
@apiParam {Integer}         equipment_type_id           Required.
@apiParam {Integer}         location_id                 Required.
@apiParam {Integer}         assigned_to_id              Required. User id
@apiParam {String(50)}      serial
@apiParam {Integer}         manufacturer_id
@apiParam {Integer}         manufactured                Year manufactured, from 1900
@apiParam {String}          frequency                   '25', '50', '60', 'DC'
@apiParam {String}          description
@apiParam {Boolean}         modifier
@apiParam {String}          comments
@apiParam {String}          nbr_of_tap_change_ltc       Number of tap change on LTC
@apiParam {Integer}         tie_status                  TieAnalysisState.
@apiParam {Integer}         status                      EquipmentState.
@apiParam {Integer}         phys_position
@apiParam {Float}           tension4                    Voltage4
@apiParam {Boolean}         validated
@apiParam {Boolean}         invalidation
@apiParam {String(50)}      prev_serial_number
@apiParam {String(50)}      prev_equipment_number
@apiParam {Integer}         sibling
@apiParam {Dict}            extra_fields                depending on equipment type

@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put}/{post} /equipment/:id Update an item by id. If only status field changed,
                                 send email notifications to the user who updated the
                                 equipment, the user who is assigned to the equipment
@apiVersion 1.0.0
@apiName update_equipment_handler
@apiGroup equipment
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"location_id":5}' http://localhost:8001/api/v1.0/equipment/

@apiUse PutItemSuccess
@apiUse Error404
"""
"""
@api {delete} /equipment/:id Delete an item by id
@apiVersion 1.0.0
@apiName delete_item
@apiGroup equipment
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/equipment/11

@apiUse DelItemSuccess
@apiUse Error404
"""


# Equipment_type
"""
@api {get} /equipment_type/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup equipment_type
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/equipment_type/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /equipment_type/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup equipment_type
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/equipment_type/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "code": "Y",
            "id": 15,
            "name": "Tank",
            "table_name": "tank"
        }
    }

@apiSuccess {Integer}     id
@apiSuccess {String(50)}  name
@apiSuccess {String(50)}  code
@apiSuccess {String(50)}  table_name
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /equipment_type Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup equipment_type
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST \
         -d '{"name":"Tank", "code":"Y", "table_name":"tank"}' \
         http://localhost:8001/api/v1.0/equipment_type/

@apiParam {String(50)}  name
@apiParam {String(50)}  code
@apiParam {String(50)}  table_name
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /equipment_type/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup equipment_type
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name":"My other name"}'\
    http://localhost:8001/api/v1.0/equipment_type/10

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /equipment_type/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup equipment_type
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/equipment_type/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# Contract
"""
@api {get} /contract/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup contract
@apiExample {curl} Example usage:
    curl -i http://localhost:8001/api/v1.0/contract/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /contract/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup contract
@apiExample {curl} Example usage:
    curl -i http://localhost:8001/api/v1.0/contract/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "code": "code",
            "contract_status": {
                "id": 1,
                "name": "Test contract status"
                },
            "contract_status_id": 1,
            "id": 1,
            "name": "first contract"
        }
    }

@apiSuccess {Integer}     id
@apiSuccess {String(50)}  name
@apiSuccess {String(50)}  code
@apiSuccess {String(50)}  contract_status_id
@apiSuccess {Dict}        contract_status       see: contract_status->get an item
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /contract/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup contract
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST \
         -d '{"name":"My contract", "code":"My code", "contract_status_id":1}' \
         http://localhost:8001/api/v1.0/contract/

@apiParam {String(50)}  name
@apiParam {String(50)}  code
@apiParam {String(50)}  contract_status_id
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /contract/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup contract
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name":"My other name"}'\
         http://localhost:8001/api/v1.0/contract/10

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /contract/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup contract
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/contract/10

@apiUse DelItemSuccess
@apiUse Error404
"""


# Norm
"""
@api {get} /norm/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup norm
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/norm/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /norm/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup norm
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/norm/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "Norms furan ",
            "table_name": "norm_furan"
        }
    }

@apiSuccess {Integer}     id
@apiSuccess {String(50)}  name
@apiSuccess {String(50)}  table_name
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /norm Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup norm
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST \
         -d '{"name":"Norms furan", "table_name":"norm_furan"}' \
         http://localhost:8001/api/v1.0/norm/

@apiParam {String(50)}  name
@apiParam {String(50)}  table_name
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /norm/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup norm
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name":"My other name"}'\
    http://localhost:8001/api/v1.0/norm/10

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /norm/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup norm
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/norm/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# Location
"""
@api {get} /location/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup location
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/location/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /location/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup location
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/location/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "location"
        }
    }

@apiSuccess {Integer}     id
@apiSuccess {String(50)}  name
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /location Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup location
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"My location"}' \
         http://localhost:8001/api/v1.0/location/

@apiParam {String(50)}  name
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /location/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup location
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name":"My other name"}'\
    http://localhost:8001/api/v1.0/location/10

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /location/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup location
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/location/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# Manufacturer
"""
@api {get} /manufacturer/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup manufacturer
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/manufacturer/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /manufacturer/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup manufacturer
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/manufacturer/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "description": "-",
            "id": 1,
            "location": "Enteropia",
            "markings": "AAA",
            "name": "Ardrites"
        }
    }

@apiSuccess {Integer}     id
@apiSuccess {String(50)}  name
@apiSuccess {String(50)}  table_name
@apiSuccess {String(256)} location
@apiSuccess {String}      markings
@apiSuccess {String}      description
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /manufacturer Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup manufacturer
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST \
         -d '{"name":"Ardrites", "location": "Enteropia", "markings": "AAA"}' \
         http://localhost:8001/api/v1.0/manufacturer/

@apiParam {String(50)}  name        required
@apiParam {String(50)}  table_name
@apiParam {String(256)} location
@apiParam {String}      markings
@apiParam {String}      description
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /manufacturer/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup manufacturer
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name":"My other name"}'\
    http://localhost:8001/api/v1.0/manufacturer/10

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /manufacturer/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup manufacturer
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/manufacturer/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# Electrical profile
"""
@api {get} /electrical_profile/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup electrical_profile
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/electrical_profile/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /electrical_profile/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup electrical_profile
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/electrical_profile/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "My name",
            "description": "My descripton",
            "profile_type": "electrical_profile",
            "bushing": true,
            "winding": true,
            "insulation_pf": true,
            "insulation": true,
            "visual": true,
            "resistance": true,
            "degree": true,
            "turns": true,
            "user_id": 1
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(256)}   name
@apiSuccess {String(1024)}  description
@apiSuccess {Boolean}       shared
@apiSuccess {String}        profile_type    electrical_profile
@apiSuccess {Boolean}       bushing
@apiSuccess {Boolean}       winding
@apiSuccess {Boolean}       insulation_pf
@apiSuccess {Boolean}       insulation
@apiSuccess {Boolean}       visual
@apiSuccess {Boolean}       resistance
@apiSuccess {Boolean}       degree
@apiSuccess {Boolean}       turns
@apiSuccess {Integer}       user_id
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /electrical_profile Add a new item
@apiVersion 1.0.0
@apiName create_electrical_profile_handler
@apiGroup electrical_profile
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST \
         -d '{"name":"My name", "description": "My description", "bushing": true}' \
         http://localhost:8001/api/v1.0/electrical_profile/

@apiParam {String(256)}   name
@apiParam {String(1024)}  description
@apiParam {Boolean}       shared
@apiParam {Boolean}       bushing
@apiParam {Boolean}       winding
@apiParam {Boolean}       insulation_pf
@apiParam {Boolean}       insulation
@apiParam {Boolean}       visual
@apiParam {Boolean}       resistance
@apiParam {Boolean}       degree
@apiParam {Boolean}       turns
@apiParam {Integer}       user_id
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /electrical_profile/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup electrical_profile
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name":"My other name"}'\
    http://localhost:8001/api/v1.0/electrical_profile/10

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /electrical_profile/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup electrical_profile
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/electrical_profile/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# Fluid profile
"""
@api {get} /fluid_profile/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup fluid_profile
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/fluid_profile/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /fluid_profile/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup fluid_profile
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/fluid_profile/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "My name",
            "description": "My descripton",
            "profile_type": "fluid_profile",
            ...
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(256)}   name
@apiSuccess {String(1024)}  description
@apiSuccess {Boolean}       shared
@apiSuccess {String}        profile_type  fluid_profile
@apiSuccess {Integer}       qty_ser
@apiSuccess {Integer}       sampling
@apiSuccess {Integer}       qty_jar
@apiSuccess {Integer}       sampling_jar
@apiSuccess {Integer}       qty_vial
@apiSuccess {Integer}       sampling_vial
@apiSuccess {Boolean}       gas
@apiSuccess {Boolean}       water
@apiSuccess {Boolean}       furans
@apiSuccess {Boolean}       inhibitor
@apiSuccess {Boolean}       pcb
@apiSuccess {Boolean}       dielec
@apiSuccess {Boolean}       acidity
@apiSuccess {Boolean}       density
@apiSuccess {Boolean}       pcb_jar
@apiSuccess {Boolean}       inhibitor_jar
@apiSuccess {Boolean}       point
@apiSuccess {Boolean}       dielec_2
@apiSuccess {Boolean}       color
@apiSuccess {Boolean}       pf
@apiSuccess {Boolean}       particles
@apiSuccess {Boolean}       metals
@apiSuccess {Boolean}       viscosity
@apiSuccess {Boolean}       dielec_d
@apiSuccess {Boolean}       ift
@apiSuccess {Boolean}       pf_100
@apiSuccess {Boolean}       furans_f
@apiSuccess {Boolean}       water_w
@apiSuccess {Boolean}       corr
@apiSuccess {Boolean}       dielec_i
@apiSuccess {Boolean}       visual
@apiSuccess {Boolean}       pcb_vial
@apiSuccess {Boolean}       antioxidant
@apiSuccess {Integer}       user_id
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /fluid_profile Add a new item
@apiVersion 1.0.0
@apiName create_fluid_profile_handler
@apiGroup fluid_profile
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST \
         -d '{"name":"My name", "description": "My description", "gas": true}' \
         http://localhost:8001/api/v1.0/fluid_profile/

@apiParam {String(256)}   name
@apiParam {String(1024)}  description
@apiParam {Boolean}       shared
@apiParam {Integer}       qty_ser
@apiParam {Integer}       sampling
@apiParam {Integer}       qty_jar
@apiParam {Integer}       sampling_jar
@apiParam {Integer}       qty_vial
@apiParam {Integer}       sampling_vial
@apiParam {Boolean}       gas
@apiParam {Boolean}       water
@apiParam {Boolean}       furans
@apiParam {Boolean}       inhibitor
@apiParam {Boolean}       pcb
@apiParam {Boolean}       dielec
@apiParam {Boolean}       acidity
@apiParam {Boolean}       density
@apiParam {Boolean}       pcb_jar
@apiParam {Boolean}       inhibitor_jar
@apiParam {Boolean}       point
@apiParam {Boolean}       dielec_2
@apiParam {Boolean}       color
@apiParam {Boolean}       pf
@apiParam {Boolean}       particles
@apiParam {Boolean}       metals
@apiParam {Boolean}       viscosity
@apiParam {Boolean}       dielec_d
@apiParam {Boolean}       ift
@apiParam {Boolean}       pf_100
@apiParam {Boolean}       furans_f
@apiParam {Boolean}       water_w
@apiParam {Boolean}       corr
@apiParam {Boolean}       dielec_i
@apiParam {Boolean}       visual
@apiParam {Boolean}       pcb_vial
@apiParam {Boolean}       antioxidant
@apiParam {Integer}       user_id
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /fluid_profile/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup fluid_profile
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name":"My other name"}'\
    http://localhost:8001/api/v1.0/fluid_profile/10

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /fluid_profile/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup fluid_profile
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/fluid_profile/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# Test profile
"""
@api {get} /test_profile/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup test_profile
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/test_profile/

@apiDescription This is the united list of two list, see: fluid_profile->get items and electrical_profile->get items.
@apiUse GetItemsSuccess
@apiUse Error404
"""

# Test result
"""
@api {get} /test_result/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup test_result
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/test_result/

Can filter also by:
@apiParam {Integer}   campaign__created_by_id
@apiParam {String}    search_all    ILIKE search by id, date_analyse, analysis_number,
                                    test_reason.name, test_type.name, test_status.name,
                                    equipment.serial, equipment.equipment_number

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /test_result/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup test_result
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/test_result/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "campaign_id": 1,
            "test_reason_id": 1,
            "date_analyse": [
                "2016-07-29",
                "17:52:19"
            ],
            "test_type_id": 1,
            "sampling_point_id": 1,
            "test_status_id": 1,
        }
    }

@apiSuccess {Integer}   id
@apiSuccess {Integer}   campaign_id
@apiSuccess {Dict}      campaign            see: campaign->get an item
@apiSuccess {Integer}   test_reason_id
@apiSuccess {Dict}      test_reason         see: reason->get an item
@apiSuccess {DateTime}  date_analyse
@apiSuccess {Integer}   test_type_id
@apiSuccess {Dict}      test_type           see: test_type->get an item
@apiSuccess {Integer}   sampling_point_id
@apiSuccess {Dict}      sampling_point      see: sampling_point->get an item
@apiSuccess {Integer}   test_status_id
@apiSuccess {Dict}      test_status         see: test_status->get an item
@apiSuccess {Integer}   equipment_id
@apiSuccess {Dict}      equipment           see: equipment->get an item
@apiSuccess {Integer}   fluid_profile_id
@apiSuccess {Dict}      fluid_profile       see: fluid_profile->get an item
@apiSuccess {Integer}   electrical_profile_id
@apiSuccess {Dict}      electrical_profile  see: electrical_profile->get an item
@apiSuccess {Boolean}   percent_ratio
@apiSuccess {String}    analysis_number
@apiSuccess {Integer}   performed_by_id
@apiSuccess {Dict}      performed_by        see: performed_by->get an item
@apiSuccess {Integer}   lab_id
@apiSuccess {Dict}      lab                 see: lab->get an item
@apiSuccess {Integer}   material_id
@apiSuccess {Dict}      material            see: material->get an item
@apiSuccess {Integer}   fluid_type_id
@apiSuccess {Dict}      fluid_type          see: fluid_type->get an item
@apiSuccess {Float}     charge
@apiSuccess {String}    remark
@apiSuccess {Boolean}   modifier
@apiSuccess {Boolean}   transmission
@apiSuccess {Datetime}  repair_date
@apiSuccess {String}    repair_description
@apiSuccess {Float}     mws
@apiSuccess {Float}     temperature
@apiSuccess {Float}     containers
@apiSuccess {Integer}   lab_contract_id
@apiSuccess {Dict}      lab_contract        see: contract->get an item
@apiSuccess {String}    seringe_num
@apiSuccess {Float}     ambient_air_temperature
@apiSuccess {Boolean}   bushing
@apiSuccess {Boolean}   winding
@apiSuccess {Boolean}   insulation_pf
@apiSuccess {Boolean}   insulation
@apiSuccess {Boolean}   visual_inspection
@apiSuccess {Boolean}   resistance
@apiSuccess {Boolean}   degree
@apiSuccess {Boolean}   turns
@apiSuccess {Boolean}   gas
@apiSuccess {Boolean}   water
@apiSuccess {Boolean}   furans
@apiSuccess {Boolean}   inhibitor
@apiSuccess {Boolean}   pcb
@apiSuccess {Integer}   qty_ser
@apiSuccess {Integer}   sampling
@apiSuccess {Boolean}   dielec
@apiSuccess {Boolean}   acidity
@apiSuccess {Boolean}   density
@apiSuccess {Boolean}   pcb_jar
@apiSuccess {Boolean}   inhibitor_jar
@apiSuccess {Boolean}   point
@apiSuccess {Boolean}   dielec_2
@apiSuccess {Boolean}   color
@apiSuccess {Boolean}   pf
@apiSuccess {Boolean}   particles
@apiSuccess {Boolean}   metals
@apiSuccess {Boolean}   viscosity
@apiSuccess {Boolean}   dielec_d
@apiSuccess {Boolean}   ift
@apiSuccess {Boolean}   pf_100
@apiSuccess {Boolean}   furans_f
@apiSuccess {Boolean}   water_w
@apiSuccess {Boolean}   corr
@apiSuccess {Boolean}   dielec_i
@apiSuccess {Boolean}   visual
@apiSuccess {Integer}   qty_jar
@apiSuccess {Integer}   sampling_jar
@apiSuccess {Boolean}   pcb_vial
@apiSuccess {Boolean}   antioxidant
@apiSuccess {Integer}   qty_vial
@apiSuccess {Integer}   sampling_vial
@apiSuccess {List}      tests                see: test->get items
@apiSuccess {List}      test_sampling_cards  see: test_sampling_cards->get items
@apiSuccess {List}      test_recommendations see: test_recommendations->get items
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /test_result Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup test_result
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST \
         -d '{"campaign_id":1, "test_reason_id": 5, "test_type_id": 1, "date_analyse": "2016-07-29 17:52:19"}' \
         http://localhost:8001/api/v1.0/test_result/

@apiParam {Integer}   campaign_id       required
@apiParam {Integer}   test_reason_id
@apiParam {DateTime}  date_analyse      format "2016-07-29 17:52:19"
@apiParam {Integer}   test_type_id
@apiParam {Integer}   sampling_point_id
@apiParam {Integer}   test_status_id
@apiParam {Integer}   equipment_id
@apiParam {Integer}   fluid_profile_id
@apiParam {Integer}   electrical_profile_id
@apiParam {Boolean}   percent_ratio
@apiParam {Integer}   performed_by_id
@apiParam {Integer}   lab_id
@apiParam {Integer}   material_id
@apiParam {Integer}   fluid_type_id
@apiParam {Float}     charge
@apiParam {String}    remark
@apiParam {Boolean}   modifier
@apiParam {Boolean}   transmission
@apiParam {Datetime}  repair_date         format "2016-07-29 17:52:19"
@apiParam {String}    repair_description
@apiParam {Float}     mws
@apiParam {Float}     temperature
@apiParam {Float}     containers
@apiParam {Integer}   lab_contract_id
@apiParam {String}    seringe_num
@apiParam {Float}     ambient_air_temperature
@apiParam {Boolean}   bushing
@apiParam {Boolean}   winding
@apiParam {Boolean}   insulation_pf
@apiParam {Boolean}   insulation
@apiParam {Boolean}   visual_inspection
@apiParam {Boolean}   resistance
@apiParam {Boolean}   degree
@apiParam {Boolean}   turns
@apiParam {Boolean}   gas
@apiParam {Boolean}   water
@apiParam {Boolean}   furans
@apiParam {Boolean}   inhibitor
@apiParam {Boolean}   pcb
@apiParam {Integer}   qty_ser
@apiParam {Integer}   sampling
@apiParam {Boolean}   dielec
@apiParam {Boolean}   acidity
@apiParam {Boolean}   density
@apiParam {Boolean}   pcb_jar
@apiParam {Boolean}   inhibitor_jar
@apiParam {Boolean}   point
@apiParam {Boolean}   dielec_2
@apiParam {Boolean}   color
@apiParam {Boolean}   pf
@apiParam {Boolean}   particles
@apiParam {Boolean}   metals
@apiParam {Boolean}   viscosity
@apiParam {Boolean}   dielec_d
@apiParam {Boolean}   ift
@apiParam {Boolean}   pf_100
@apiParam {Boolean}   furans_f
@apiParam {Boolean}   water_w
@apiParam {Boolean}   corr
@apiParam {Boolean}   dielec_i
@apiParam {Boolean}   visual
@apiParam {Integer}   qty_jar
@apiParam {Integer}   sampling_jar
@apiParam {Boolean}   pcb_vial
@apiParam {Boolean}   antioxidant
@apiParam {Integer}   qty_vial
@apiParam {Integer}   sampling_vial
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {post} /test_result/equipment Add a lot of new items with equipment_id
@apiVersion 1.0.0
@apiName add_item
@apiGroup test_result
@apiExample {curl} Example with equipment_id as integer:
    curl -i -H "Content-Type: application/json" -X POST \
         -d '{"campaign_id":1,"equipment_id":5}' \
         http://localhost:8001/api/v1.0/test_result/equipment

@apiExample {curl} Example with equipment_id as list with one integer:
    curl -i -H "Content-Type: application/json" -X POST \
         -d '{"campaign_id":1,"equipment_id":[5]}' \
         http://localhost:8001/api/v1.0/test_result/equipment

@apiExample {curl} Example with equipment_id as list of integers:
    curl -i -H "Content-Type: application/json" -X POST \
         -d '{"campaign_id":1,"equipment_id":[5,6]}' \
         http://localhost:8001/api/v1.0/test_result/equipment

@apiParam {Integer}   campaign_id       required
@apiParam {Integer}   equipment_id
@apiParam {List}      equipment_id

@apiSuccess {List}  result  List of new items ids.
@apiSuccessExample Success-Response true:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
      "result": [42,43]
    }
@apiUse Error400
"""
"""
Duplicate test result and related electrical or fluid profile, if they belong
to the currently logged in user or are private.
@api {post} /test_result/:id/duplicate
@apiVersion 1.0.0
@apiName add_item
@apiGroup test_result
@apiExample {curl} Example usage:
    curl -X POST http://localhost:8001/api/v1.0/test_result/3/duplicate

@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /test_result/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup test_result
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"date_analyse": "2016-07-29 17:52:19"}'\
    http://localhost:8001/api/v1.0/test_result/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /test_result/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup test_result
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/test_result/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# Campaign
"""
@api {get} /campaign/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup campaign
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/campaign/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /campaign/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup campaign
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/campaign/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            ...
            "date_created": [
                "2016-07-29",
                "17:52:19"
            ],
            "status_id": 1,
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {Datetime}      date_created
@apiSuccess {Integer}       created_by_id
@apiSuccess {Dict}          created_by          see: user->get an item
@apiSuccess {Integer}       contract_id
@apiSuccess {Dict}          contract            see: contract->get an item
@apiSuccess {Datetime}      date_sampling
@apiSuccess {String}        description
@apiSuccess {Integer}       status_id
@apiSuccess {Dict}          status              see: campaign_status->get an item
@apiSuccess {List}          test_result         list of related test results, see: test_result->get items
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {get} /campaign/:id/finish Finish campaign setup. Send email notifications to performers,
                                person who created campaign, user who finishes the campaign
@apiVersion 1.0.0
@apiName finish_campaign_handler
@apiGroup campaign
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/campaign/1/finish

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {post} /campaign/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup campaign
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST \
         -d '{"created_by_id":1, "date_created": "2016-07-29 17:52:19", "contract_id":1}' \
         http://localhost:8001/api/v1.0/campaign/

@apiParam   {Datetime}      date_created        required format "2016-07-29 17:52:19"
@apiParam   {Integer}       created_by_id       required
@apiParam   {Integer}       contract_id         required
@apiParam   {Datetime}      date_sampling       format "2016-07-29 17:52:19"
@apiParam   {String}        description
@apiParam   {Integer}       status_id
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /campaign/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup campaign
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"date": "2016-07-29 17:52:19"}'\
    http://localhost:8001/api/v1.0/campaign/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /campaign/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup campaign
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/campaign/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# role
"""
@api {get} /role/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup role
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/role/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /role/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup role
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/role/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
            "description": "some description"
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(80)}    name
@apiSuccess {String(255)}   description
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /role/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup role
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST \
         -d '{"name":"some name", "description": "some description"}' \
         http://localhost:8001/api/v1.0/role/

@apiParam   {String(80)}    name
@apiParam   {String(255)}   description
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /role/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup role
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"description": "some other description"}'\
    http://localhost:8001/api/v1.0/role/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /role/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup role
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/role/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# lab
"""
@api {get} /lab/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup lab
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/lab/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /lab/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup lab
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/lab/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
            "analyser": "some string",
            "code": 12,
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {Integer}       code
@apiSuccess {String(256)}   name
@apiSuccess {String(256)}   analyser
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /lab/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup lab
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/lab/

@apiParam   {Integer}       code
@apiParam   {String(256)}   name
@apiParam   {String(256)}   analyser
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /lab/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup lab
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
    http://localhost:8001/api/v1.0/lab/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /lab/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup lab
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/lab/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# material
"""
@api {get} /material/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup material
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/material/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /material/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup material
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/material/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
            "code": "some code",
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(50)}    name
@apiSuccess {String(50)}    code
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /material/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup material
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/material/

@apiParam   {String(50)}    name
@apiParam   {String(50)}    code
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /material/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup material
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
    http://localhost:8001/api/v1.0/material/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /material/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup material
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/material/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# gas_sensor
"""
@api {get} /gas_sensor/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup gas_sensor
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/gas_sensor/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /gas_sensor/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup gas_sensor
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/gas_sensor/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(50)}    model
@apiSuccess {Float}         h2
@apiSuccess {Float}         ch4
@apiSuccess {Float}         c2h2
@apiSuccess {Float}         c2h4
@apiSuccess {Float}         c2h6
@apiSuccess {Float}         co
@apiSuccess {Float}         co2
@apiSuccess {Float}         o2
@apiSuccess {Float}         n2
@apiSuccess {Float}         percent_error
@apiSuccess {Integer}       ppm_error
@apiSuccess {Integer}       equipment_id
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /gas_sensor/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup gas_sensor
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST \
         -d '{"equipment_id":"1"}' \
         http://localhost:8001/api/v1.0/gas_sensor/

@apiParam   {String(50)}    model
@apiParam   {Float}         h2
@apiParam   {Float}         ch4
@apiParam   {Float}         c2h2
@apiParam   {Float}         c2h4
@apiParam   {Float}         c2h6
@apiParam   {Float}         co
@apiParam   {Float}         co2
@apiParam   {Float}         o2
@apiParam   {Float}         n2
@apiParam   {Float}         percent_error
@apiParam   {Integer}       ppm_error
@apiParam   {Integer}       equipment_id required
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /gas_sensor/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup gas_sensor
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"h2": 5}'\
    http://localhost:8001/api/v1.0/gas_sensor/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /gas_sensor/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup gas_sensor
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/gas_sensor/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# transformer
"""
@api {get} /transformer/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup transformer
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/transformer/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /transformer/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup transformer
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/transformer/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            ...
        }
    }

@apiSuccess {Integer}     id
@apiSuccess {Integer}     fluid_type_id
@apiSuccess {Dict}        fluid_type        see: fluid_type->get an item
@apiSuccess {Integer}     gassensor_id
@apiSuccess {Dict}        gassensor     see: gassensor->get an item
@apiSuccess {Integer}     equipment_id
@apiSuccess {Float}       fluid_volume
@apiSuccess {Boolean}     sealed
@apiSuccess {Boolean}     welded_cover
@apiSuccess {Integer}     windings
@apiSuccess {Integer}     cooling_rating
@apiSuccess {Boolean}     autotransformer
@apiSuccess {Boolean}     threephase
@apiSuccess {Integer}     fluid_level_id
@apiSuccess {Dict}        fluid_level    see: fluid_level->get an item
@apiSuccess {String}      phase_number   allowed: '1', '3' or '6'
@apiSuccess {String}      frequency      allowed: '25', '50', '60' or 'DC'
@apiSuccess {Float}       primary_tension
@apiSuccess {Float}       secondary_tension
@apiSuccess {Float}       tertiary_tension
@apiSuccess {Float}       based_transformer_power
@apiSuccess {Float}       first_cooling_stage_power
@apiSuccess {Float}       second_cooling_stage_power
@apiSuccess {String}      primary_winding_connection
@apiSuccess {String}      secondary_winding_connection
@apiSuccess {String}      tertiary_winding_connection
@apiSuccess {String}      quaternary_winding_connection
@apiSuccess {Integer}     winding_metal1
@apiSuccess {Float}       bil1
@apiSuccess {Float}       bil2
@apiSuccess {Float}       bil3
@apiSuccess {Boolean}     static_shield1
@apiSuccess {Boolean}     static_shield2
@apiSuccess {Boolean}     static_shield3
@apiSuccess {Float}       bushing_neutral1
@apiSuccess {Float}       bushing_neutral2
@apiSuccess {Float}       bushing_neutral3
@apiSuccess {Float}       bushing_neutral4
@apiSuccess {Float}       ltc1
@apiSuccess {Float}       ltc2
@apiSuccess {Float}       ltc3
@apiSuccess {Integer}     temperature_rise
@apiSuccess {Float}       impedance1
@apiSuccess {Float}       imp_base1
@apiSuccess {Float}       impedance2
@apiSuccess {Float}       imp_base2
@apiSuccess {Float}       mvaforced11
@apiSuccess {Float}       mvaforced12
@apiSuccess {Float}       mvaforced13
@apiSuccess {Float}       mvaforced14
@apiSuccess {Float}       mvaforced21
@apiSuccess {Float}       mvaforced22
@apiSuccess {Float}       mvaforced23
@apiSuccess {Float}       mvaforced24
@apiSuccess {Float}       impedance3
@apiSuccess {Float}       impbasedmva3
@apiSuccess {Integer}     formula_ratio2
@apiSuccess {Integer}     formula_ratio
@apiSuccess {String(20)}  ratio_tag1
@apiSuccess {String(20)}  ratio_tag2
@apiSuccess {String(20)}  ratio_tag3
@apiSuccess {String(20)}  ratio_tag4
@apiSuccess {String(20)}  ratio_tag5
@apiSuccess {String(20)}  ratio_tag6
@apiSuccess {Integer}     bushing_serial1_id
@apiSuccess {Dict}        bushing_serial1       see: bushing->get an item
@apiSuccess {Integer}     bushing_serial2_id
@apiSuccess {Dict}        bushing_serial2       see: bushing->get an item
@apiSuccess {Integer}     bushing_serial3_id
@apiSuccess {Dict}        bushing_serial3       see: bushing->get an item
@apiSuccess {Integer}     bushing_serial4_id
@apiSuccess {Dict}        bushing_serial4       see: bushing->get an item
@apiSuccess {Integer}     bushing_serial5_id
@apiSuccess {Dict}        bushing_serial5       see: bushing->get an item
@apiSuccess {Integer}     bushing_serial6_id
@apiSuccess {Dict}        bushing_serial6       see: bushing->get an item
@apiSuccess {Integer}     bushing_serial7_id
@apiSuccess {Dict}        bushing_serial7       see: bushing->get an item
@apiSuccess {Integer}     bushing_serial8_id
@apiSuccess {Dict}        bushing_serial8       see: bushing->get an item
@apiSuccess {Integer}     bushing_serial9_id
@apiSuccess {Dict}        bushing_serial9       see: bushing->get an item
@apiSuccess {Integer}     bushing_serial10_id
@apiSuccess {Dict}        bushing_serial10      see: bushing->get an item
@apiSuccess {Integer}     bushing_serial11_id
@apiSuccess {Dict}        bushing_serial11      see: bushing->get an item
@apiSuccess {Integer}     bushing_serial12_id
@apiSuccess {Dict}        bushing_serial12      see: bushing->get an item
@apiSuccess {Float}       mvaactual
@apiSuccess {Float}       mvaractual
@apiSuccess {Float}       mwreserve
@apiSuccess {Float}       mvarreserve
@apiSuccess {Float}       mwultime
@apiSuccess {Float}       mvarultime
@apiSuccess {Float}       third_cooling_stage_power
@apiSuccess {Float}       quaternary_winding_connection
@apiSuccess {Float}       bil4
@apiSuccess {Float}       static_shield4
@apiSuccess {Float}       ratio_tag7
@apiSuccess {Float}       ratio_tag8
@apiSuccess {Float}       formula_ratio3
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /transformer/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup transformer
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST \
         -d '{"fluid_type_id": 1, "gassensor_id": 1, "equipment_id": 1}' \
         http://localhost:8001/api/v1.0/transformer/

@apiParam   {Integer}     fluid_type_id    required
@apiParam   {Integer}     gassensor_id required
@apiParam   {Integer}     equipment_id required
@apiParam   {Float}       fluid_volume
@apiParam   {Boolean}     sealed
@apiParam   {Boolean}     welded_cover
@apiParam   {Integer}     windings
@apiParam   {Integer}     cooling_rating
@apiParam   {Boolean}     autotransformer
@apiParam   {Boolean}     threephase
@apiParam   {Integer}     fluid_level_id
@apiParam   {String}      phase_number   allowed: '1', '3' or '6'
@apiParam   {String}      frequency      allowed: '25', '50', '60' or 'DC'
@apiParam   {Float}       primary_tension
@apiParam   {Float}       secondary_tension
@apiParam   {Float}       tertiary_tension
@apiParam   {Float}       based_transformer_power
@apiParam   {Float}       first_cooling_stage_power
@apiParam   {Float}       second_cooling_stage_power
@apiParam   {String}     primary_winding_connection
@apiParam   {String}     secondary_winding_connection
@apiParam   {String}     tertiary_winding_connection
@apiParam   {String}     quaternary_winding_connection
@apiParam   {Integer}     winding_metal1
@apiParam   {Float}       bil1
@apiParam   {Float}       bil2
@apiParam   {Float}       bil3
@apiParam   {Boolean}     static_shield1
@apiParam   {Boolean}     static_shield2
@apiParam   {Boolean}     static_shield3
@apiParam   {Float}       bushing_neutral1
@apiParam   {Float}       bushing_neutral2
@apiParam   {Float}       bushing_neutral3
@apiParam   {Float}       bushing_neutral4
@apiParam   {Float}       ltc1
@apiParam   {Float}       ltc2
@apiParam   {Float}       ltc3
@apiParam   {Integer}     temperature_rise
@apiParam   {Float}       impedance1
@apiParam   {Float}       imp_base1
@apiParam   {Float}       impedance2
@apiParam   {Float}       imp_base2
@apiParam   {Float}       mvaforced11
@apiParam   {Float}       mvaforced12
@apiParam   {Float}       mvaforced13
@apiParam   {Float}       mvaforced14
@apiParam   {Float}       mvaforced21
@apiParam   {Float}       mvaforced22
@apiParam   {Float}       mvaforced23
@apiParam   {Float}       mvaforced24
@apiParam   {Float}       impedance3
@apiParam   {Float}       impbasedmva3
@apiParam   {Integer}     formula_ratio2
@apiParam   {Integer}     formula_ratio
@apiParam   {String(20)}  ratio_tag1
@apiParam   {String(20)}  ratio_tag2
@apiParam   {String(20)}  ratio_tag3
@apiParam   {String(20)}  ratio_tag4
@apiParam   {String(20)}  ratio_tag5
@apiParam   {String(20)}  ratio_tag6
@apiParam   {Integer}     bushing_serial1_id
@apiParam   {Integer}     bushing_serial2_id
@apiParam   {Integer}     bushing_serial3_id
@apiParam   {Integer}     bushing_serial4_id
@apiParam   {Integer}     bushing_serial5_id
@apiParam   {Integer}     bushing_serial6_id
@apiParam   {Integer}     bushing_serial7_id
@apiParam   {Integer}     bushing_serial8_id
@apiParam   {Integer}     bushing_serial9_id
@apiParam   {Integer}     bushing_serial10_id
@apiParam   {Integer}     bushing_serial11_id
@apiParam   {Integer}     bushing_serial12_id
@apiParam   {Float}       mvaactual
@apiParam   {Float}       mvaractual
@apiParam   {Float}       mwreserve
@apiParam   {Float}       mvarreserve
@apiParam   {Float}       mwultime
@apiParam   {Float}       mvarultime
@apiParam   {Float}       third_cooling_stage_power
@apiParam   {Float}       quaternary_winding_connection
@apiParam   {Float}       bil4
@apiParam   {Float}       static_shield4
@apiParam   {Float}       ratio_tag7
@apiParam   {Float}       ratio_tag8
@apiParam   {Float}       formula_ratio3
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /transformer/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup transformer
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"fluid_volume": 2}'\
    http://localhost:8001/api/v1.0/transformer/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /transformer/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup transformer
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/transformer/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# breaker
"""
@api {get} /breaker/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup breaker
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/breaker/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /breaker/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup breaker
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/breaker/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            ...
        }
    }

@apiSuccess {Integer}   id
@apiSuccess {Integer}   current_rating
@apiSuccess {Integer}   equipment_id
@apiSuccess {Boolean}   open
@apiSuccess {Integer}   fluid_type_id
@apiSuccess {Dict}      fluid_type      see: fluid_type->get an item
@apiSuccess {Integer}   fluid_level_id
@apiSuccess {Dict}      fluid_level     see: fluid_level->get an item
@apiSuccess {Integer}   interrupting_medium_id
@apiSuccess {Dict}      interrupting_medium     see: interrupting_medium->get an item
@apiSuccess {Integer}   breaker_mechanism_id
@apiSuccess {Dict}      breaker_mechanism       see: breaker_mechanism->get an item
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /breaker/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup breaker
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST \
         -d '{"equipment_id": 1, "current_rating": 1}' \
         http://localhost:8001/api/v1.0/breaker/

@apiParam   {Integer}     equipment_id required
@apiParam   {Integer(6)}  current_rating
@apiParam   {Boolean}     open
@apiParam   {Integer}     fluid_type_id
@apiParam   {Integer}     fluid_level_id
@apiParam   {Integer}     interrupting_medium_id
@apiParam   {Integer}     breaker_mechanism_id
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /breaker/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup breaker
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"current_rating": 2}'\
    http://localhost:8001/api/v1.0/breaker/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /breaker/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup breaker
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/breaker/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# tap_changer
"""
@api {get} /tap_changer/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup tap_changer
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/tap_changer/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /tap_changer/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup tap_changer
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/tap_changer/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            ...
        }
    }

@apiSuccess {Integer}   id
@apiSuccess {String}    model
@apiSuccess {String}    filter
@apiSuccess {Integer}   counter
@apiSuccess {Integer}   number_of_taps
@apiSuccess {Integer}   tap_set
@apiSuccess {Integer}   fluid_type_id
@apiSuccess {Dict}      fluid_type                 see: fluid_type->get an item
@apiSuccess {Integer}   fluid_level_id
@apiSuccess {Dict}      fluid_level                see: fluid_level->get an item
@apiSuccess {Integer}   interrupting_medium_id
@apiSuccess {Dict}      interrupting_medium        see: interrupting_medium->get an item
@apiSuccess {Integer}   equipment_id
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /tap_changer/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup tap_changer
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST \
         -d '{"equipment_id": 1}' \
         http://localhost:8001/api/v1.0/tap_changer/

@apiParam   {String(50)}    model
@apiParam   {String(30)}    filter
@apiParam   {Integer}       counter
@apiParam   {Integer}       number_of_taps
@apiParam   {Integer}       tap_set
@apiParam   {Integer}       fluid_type_id
@apiParam   {Integer}       fluid_level_id
@apiParam   {Integer}       interrupting_medium_id
@apiParam   {Integer}       equipment_id required
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /tap_changer/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup tap_changer
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"model": "some other model"}'\
    http://localhost:8001/api/v1.0/tap_changer/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /tap_changer/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup tap_changer
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/tap_changer/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# bushing
"""
@api {get} /bushing/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup bushing
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/bushing/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /bushing/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup bushing
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/bushing/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
        }
    }

@apiSuccess {Integer}   id
@apiSuccess {String}    model
@apiSuccess {String}    type    'phase' or 'Neutral'
@apiSuccess {Float}     kv
@apiSuccess {Boolean}   sealed
@apiSuccess {Integer}   current_rating
@apiSuccess {Float}     fluid_volume
@apiSuccess {Integer}   bil
@apiSuccess {Float}     c1
@apiSuccess {Float}     c1pf
@apiSuccess {Float}     c2
@apiSuccess {Float}     c2pf
@apiSuccess {Integer}   fluid_type_id
@apiSuccess {Dict}      fluid_type      see: fluid_type->get an item
@apiSuccess {Integer}   equipment_id
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /bushing/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup bushing
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST \
         -d '{"equipment_id": 1, "model": "some model"}' \
         http://localhost:8001/api/v1.0/bushing/

@apiParam   {String(50)}    model
@apiParam   {String}        type      allowed: 'phase' or 'Neutral'
@apiParam   {Float}         kv
@apiParam   {Boolean}       sealed
@apiParam   {Integer}       current_rating
@apiParam   {Float}         fluid_volume
@apiParam   {Integer(8)}    bil
@apiParam   {Float}         c1
@apiParam   {Float}         c1pf
@apiParam   {Float}         c2
@apiParam   {Float}         c2pf
@apiParam   {Integer}       fluid_type_id
@apiParam   {Integer}       equipment_id required
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /bushing/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup bushing
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"model": "some other model"}'\
    http://localhost:8001/api/v1.0/bushing/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /bushing/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup bushing
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/bushing/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# resistance
"""
@api {get} /resistance/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup resistance
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/resistance/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /resistance/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup resistance
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/resistance/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
        }
    }

@apiSuccess {Integer}   id
@apiSuccess {Float}     neutral_resistance
@apiSuccess {Float}     neutral_resistance1
@apiSuccess {Boolean}   neutral_resistance0
@apiSuccess {Float}     neutral_resistance2
@apiSuccess {Float}     neutral_resistance3
@apiSuccess {Boolean}   neutral_resistance_open1
@apiSuccess {Boolean}   neutral_resistance_open2
@apiSuccess {Float}     neutral_resistance_open3
@apiSuccess {Float}     kv
@apiSuccess {Integer}   bil
@apiSuccess {Boolean}   open
@apiSuccess {Integer}   equipment_id
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /resistance/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup resistance
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST \
         -d '{"equipment_id": 1, "neutral_resistance": 5}' \
         http://localhost:8001/api/v1.0/resistance/

@apiParam   {Integer}       equipment_id required
@apiParam   {Float}         neutral_resistance
@apiParam   {Float}         neutral_resistance1
@apiParam   {Boolean}       neutral_resistance0
@apiParam   {Float}         neutral_resistance2
@apiParam   {Float}         neutral_resistance3
@apiParam   {Boolean}       neutral_resistance_open1
@apiParam   {Boolean}       neutral_resistance_open2
@apiParam   {Float}         neutral_resistance_open3
@apiParam   {Float}         kv
@apiParam   {Integer(8)}    bil
@apiParam   {Boolean}       open
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /resistance/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup resistance
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"neutral_resistance": 6}'\
    http://localhost:8001/api/v1.0/resistance/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /resistance/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup resistance
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/resistance/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# air_breaker
"""
@api {get} /air_breaker/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup air_breaker
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/air_breaker/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /air_breaker/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup air_breaker
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/air_breaker/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
        }
    }

@apiSuccess {Integer}   id
@apiSuccess {Integer}   current_rating
@apiSuccess {Integer}   equipment_id
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /air_breaker/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup air_breaker
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST \
         -d '{"equipment_id": 1, "current_rating": 1}' \
         http://localhost:8001/api/v1.0/air_breaker/

@apiParam   {Integer(6)}    current_rating
@apiParam   {Integer}       equipment_id required
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /air_breaker/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup air_breaker
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"current_rating": 2}'\
    http://localhost:8001/api/v1.0/air_breaker/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /air_breaker/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup air_breaker
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/air_breaker/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# capacitor
"""
@api {get} /capacitor/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup capacitor
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/capacitor/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /capacitor/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup capacitor
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/capacitor/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            ...
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {Float}         kv
@apiSuccess {Float}         kvar
@apiSuccess {Integer(8)}    bil
@apiSuccess {Integer}       equipment_id
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /capacitor/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup capacitor
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST \
         -d '{"equipment_id": 1, "kv": 10}' \
         http://localhost:8001/api/v1.0/capacitor/

@apiParam   {Float}         kv
@apiParam   {Float}         kvar
@apiParam   {Integer(8)}    bil
@apiParam   {Integer}       equipment_id required
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /capacitor/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup capacitor
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"kv": 11}'\
    http://localhost:8001/api/v1.0/capacitor/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /capacitor/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup capacitor
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/capacitor/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# powersource
"""
@api {get} /powersource/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup powersource
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/powersource/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /powersource/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup powersource
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/powersource/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            ...
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {Float}         kv
@apiSuccess {Boolean}       threephase
@apiSuccess {Integer}       equipment_id
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /powersource/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup powersource
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST \
         -d '{"equipment_id": 1, "kv": 10}' \
         http://localhost:8001/api/v1.0/powersource/

@apiParam   {Integer}       equipment_id required
@apiParam   {Float}         kv
@apiParam   {Boolean}       threephase
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /powersource/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup powersource
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"kv": 11}'\
    http://localhost:8001/api/v1.0/powersource/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /powersource/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup powersource
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/powersource/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# switchgear
"""
@api {get} /switchgear/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup switchgear
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/switchgear/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /switchgear/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup switchgear
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/switchgear/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            ...
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {Integer(6)}    current_rating
@apiSuccess {Integer}       insulation_id
@apiSuccess {Dict}          insulation      see: insulation->get an item
@apiSuccess {Integer}       equipment_id
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /switchgear/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup switchgear
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST \
    -d '{"equipment_id": 1, "current_rating": 1}' \
         http://localhost:8001/api/v1.0/switchgear/

@apiParam   {Integer(6)}    current_rating
@apiParam   {Integer}       insulation_id
@apiParam   {Integer}       equipment_id required
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /switchgear/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup switchgear
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT \
         -d '{"current_rating": 2}'\
    http://localhost:8001/api/v1.0/switchgear/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /switchgear/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup switchgear
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/switchgear/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# induction_machine
"""
@api {get} /induction_machine/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup induction_machine
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/induction_machine/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /induction_machine/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup induction_machine
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/induction_machine/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            ...
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {Integer(6)}    current_rating
@apiSuccess {String(50)}    hp
@apiSuccess {String(50)}    kva
@apiSuccess {String(50)}    pf
@apiSuccess {Integer}       equipment_id
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /induction_machine/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup induction_machine
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST \
         -d '{"equipment_id": 1, "current_rating":1}' \
         http://localhost:8001/api/v1.0/induction_machine/

@apiParam   {Integer}       equipment_id required
@apiParam   {Integer(6)}    current_rating
@apiParam   {String(50)}    hp
@apiParam   {String(50)}    kva
@apiParam   {String(50)}    pf
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /induction_machine/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup induction_machine
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT \
         -d '{"current_rating": 2}'\
    http://localhost:8001/api/v1.0/induction_machine/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /induction_machine/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup induction_machine
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/induction_machine/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# synchronous_machine
"""
@api {get} /synchronous_machine/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup synchronous_machine
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/synchronous_machine/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /synchronous_machine/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup synchronous_machine
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/synchronous_machine/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            ...
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {Integer(6)}    current_rating
@apiSuccess {String(50)}    hp
@apiSuccess {String(50)}    kw
@apiSuccess {Integer}       equipment_id
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /synchronous_machine/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup synchronous_machine
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST \
         -d '{"equipment_id": 1, "current_rating": 1}' \
         http://localhost:8001/api/v1.0/synchronous_machine/

@apiParam   {Integer}       equipment_id required
@apiParam   {Integer(6)}    current_rating
@apiParam   {String(50)}    hp
@apiParam   {String(50)}    kw
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /synchronous_machine/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup synchronous_machine
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT \
         -d '{"current_rating": 2}'\
    http://localhost:8001/api/v1.0/synchronous_machine/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /synchronous_machine/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup synchronous_machine
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/synchronous_machine/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# rectifier
"""
@api {get} /rectifier/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup rectifier
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/rectifier/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /rectifier/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup rectifier
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/rectifier/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            ...
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {Float}         fluid_volume
@apiSuccess {Boolean}       sealed
@apiSuccess {Integer}       windings
@apiSuccess {Boolean}       welded_cover
@apiSuccess {Integer}       cooling_rating
@apiSuccess {Integer}       fluid_type_id
@apiSuccess {Dict}          fluid_type      see: fluid_type->get an item
@apiSuccess {Integer}       fluid_level_id
@apiSuccess {Dict}          fluid_level     see: fluid_level->get an item
@apiSuccess {Integer}       gas_sensor_id
@apiSuccess {Dict}          gas_sensor      see: gas_sensor->get an item
@apiSuccess {Integer}       equipment_id
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /rectifier/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup rectifier
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST \
         -d '{"equipment_id": 1, "fluid_volume": 10}' \
         http://localhost:8001/api/v1.0/rectifier/

@apiParam   {Integer}       equipment_id required
@apiParam   {Float}         fluid_volume
@apiParam   {Boolean}       sealed
@apiParam   {Integer}       windings
@apiParam   {Boolean}       welded_cover
@apiParam   {Integer}       cooling_rating
@apiParam   {Integer}       fluid_type_id
@apiParam   {Integer}       fluid_level_id
@apiParam   {Integer}       gas_sensor_id
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /rectifier/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup rectifier
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT \
         -d '{"fluid_volume": 11}'\
    http://localhost:8001/api/v1.0/rectifier/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /rectifier/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup rectifier
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/rectifier/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# inductance
"""
@api {get} /inductance/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup inductance
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/inductance/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /inductance/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup inductance
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/inductance/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            ...
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {Float}         fluid_volume
@apiSuccess {Boolean}       sealed
@apiSuccess {Boolean}       welded_cover
@apiSuccess {Integer}       cooling_rating
@apiSuccess {Integer}       fluid_type_id
@apiSuccess {Dict}          fluid_type      see: fluid_type->get an item
@apiSuccess {Integer}       fluid_level_id
@apiSuccess {Dict}          fluid_level     see: fluid_level->get an item
@apiSuccess {Integer}       gas_sensor_id
@apiSuccess {Dict}          gas_sensor      see: gas_sensor->get an item
@apiSuccess {Integer}       equipment_id
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /inductance/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup inductance
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST \
         -d '{"equipment_id": 1, "fluid_volume": 10}' \
         http://localhost:8001/api/v1.0/inductance/

@apiParam   {Integer}       equipment_id required
@apiParam   {Float}         fluid_volume
@apiParam   {Boolean}       sealed
@apiParam   {Boolean}       welded_cover
@apiParam   {Integer}       cooling_rating
@apiParam   {Integer}       fluid_type_id
@apiParam   {Integer}       fluid_level_id
@apiParam   {Integer}       gas_sensor_id
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /inductance/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup inductance
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT \
         -d '{"fluid_volume": 11}'\
    http://localhost:8001/api/v1.0/inductance/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /inductance/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup inductance
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/inductance/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# tank
"""
@api {get} /tank/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup tank
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/tank/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /tank/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup tank
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/tank/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            ...
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {Boolean}       welded_cover
@apiSuccess {Integer}       fluid_type_id
@apiSuccess {Dict}          fluid_type      see: fluid_type->get an item
@apiSuccess {Integer}       fluid_level_id
@apiSuccess {Dict}          fluid_level     see: fluid_level->get an item
@apiSuccess {Integer}       equipment_id
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /tank/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup tank
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST \
         -d '{"equipment_id": 1, "welded_cover": true}' \
         http://localhost:8001/api/v1.0/tank/

@apiParam   {Integer}       equipment_id required
@apiParam   {Boolean}       welded_cover
@apiParam   {Integer}       fluid_type_id
@apiParam   {Integer}       fluid_level_id
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /tank/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup tank
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT \
         -d '{"welded_cover": false}'\
    http://localhost:8001/api/v1.0/tank/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /tank/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup tank
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/tank/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# switch
"""
@api {get} /switch/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup switch
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/switch/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /switch/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup switch
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/switch/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            ...
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {Integer(6)}    current_rating
@apiSuccess {Boolean}       threephase
@apiSuccess {Boolean}       open
@apiSuccess {Integer}       interrupting_medium_id
@apiSuccess {Dict}          interrupting_medium     see: interrupting_medium->get an item
@apiSuccess {Integer}       equipment_id
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /switch/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup switch
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST \
         -d '{"equipment_id": 1, "current_rating": 10}' \
         http://localhost:8001/api/v1.0/switch/

@apiParam   {Integer}       equipment_id required
@apiParam   {Integer(6)}    current_rating
@apiParam   {Boolean}       threephase
@apiParam   {Boolean}       open
@apiParam   {Integer}       interrupting_medium_id
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /switch/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup switch
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT \
         -d '{"current_rating": 11}'\
    http://localhost:8001/api/v1.0/switch/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /switch/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup switch
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/switch/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# cable
"""
@api {get} /cable/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup cable
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/cable/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /cable/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup cable
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/cable/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            ...
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {Integer}       equipment_id
@apiSuccess {String(50)}    model
@apiSuccess {Boolean}       sealed
@apiSuccess {Boolean}       threephase
@apiSuccess {Integer}       insulation_id
@apiSuccess {Dict}          insulation     see: insulation->get an item
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /cable/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup cable
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST \
         -d '{"equipment_id": 1, "model" : "some model"}' \
         http://localhost:8001/api/v1.0/cable/

@apiParam   {Integer}       equipment_id    required
@apiParam   {String(50)}    model
@apiParam   {Boolean}       sealed
@apiParam   {Boolean}       threephase
@apiParam   {Integer}       insulation_id
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /cable/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup cable
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT \
         -d '{"model": "some other model"}'\
    http://localhost:8001/api/v1.0/cable/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /cable/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup cable
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/cable/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# recommendation
"""
@api {get} /recommendation/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup recommendation
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/recommendation/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /recommendation/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup recommendation
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/recommendation/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
            ...
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(50)}    name
@apiSuccess {String(50)}    code
@apiSuccess {String}        description
@apiSuccess {Integer}       test_type_id
@apiSuccess {Dict}          test_type       see: test_type->get an item
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /recommendation/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup recommendation
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/recommendation/

@apiParam   {String(50)}    name
@apiParam   {String(50)}    code
@apiParam   {String}        description
@apiParam   {Integer}       test_type_id
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /recommendation/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup recommendation
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
    http://localhost:8001/api/v1.0/recommendation/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /recommendation/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup recommendation
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/recommendation/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# Test recommendation
"""
@api {get} /test_recommendation/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup test_recommendation
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/test_recommendation/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /test_recommendation/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup test_recommendation
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/test_recommendation/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "recommendation_id": 1,
            ...
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {Integer}       recommendation_id
@apiSuccess {Dict}          recommendation      see: recommendation->get an item
@apiSuccess {String}        recommendation_notes
@apiSuccess {Integer}       user_id
@apiSuccess {Dict}          user                see: user->get an item
@apiSuccess {String}        date_created
@apiSuccess {String}        date_updated
@apiSuccess {Integer}       test_type_id
@apiSuccess {Dict}          test_type           see: test_type->get an item
@apiSuccess {Integer}       test_result_id
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /test_recommendation/ Add a new item
@apiVersion 1.0.0
@apiName create_test_recommendation_handler
@apiGroup test_recommendation
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"recommendation_id":1}' \
         http://localhost:8001/api/v1.0/test_recommendation/

@apiParam   {Integer}       recommendation_id
@apiParam   {String}        recommendation_notes
@apiParam   {Integer}       user_id
@apiParam   {String}        date_created     format "2016-07-29 17:52:19"
@apiParam   {String}        date_updated     format "2016-07-29 17:52:19"
@apiParam   {Integer}       test_type_id
@apiParam   {Integer}       test_result_id
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /test_recommendation/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup test_recommendation
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"recommendation_id":2}'\
    http://localhost:8001/api/v1.0/test_recommendation/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /test_recommendation/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup test_recommendation
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/test_recommendation/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# syringe
"""
@api {get} /syringe/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup syringe
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/syringe/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /syringe/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup syringe
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/syringe/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "serial": "some serial",
            ...
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(50)}    serial
@apiSuccess {Integer}       lab_id
@apiSuccess {Dict}          lab     see: lab->get an item
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /syringe/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup syringe
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"serial": "some serial"}' \
         http://localhost:8001/api/v1.0/syringe/

@apiParam   {String(50)}    serial            required
@apiParam   {Integer}    lab_id
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /syringe/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup syringe
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"serial": "some serial"}'\
    http://localhost:8001/api/v1.0/syringe/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /syringe/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup syringe
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/syringe/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# test_status
"""
@api {get} /test_status/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup test_status
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/test_status/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /test_status/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup test_status
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/test_status/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
            ...
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(50)}    code
@apiSuccess {String(50)}    name
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /test_status/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup test_status
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/test_status/

@apiParam   {String(50)}    code
@apiParam   {String(50)}    name
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /test_status/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup test_status
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
    http://localhost:8001/api/v1.0/test_status/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /test_status/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup test_status
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/test_status/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# campaign_status
"""
@api {get} /campaign_status/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup campaign_status
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/campaign_status/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /campaign_status/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup campaign_status
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/campaign_status/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
            ...
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(50)}    code
@apiSuccess {String(50)}    name
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /campaign_status/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup campaign_status
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/campaign_status/

@apiParam   {String(50)}    code
@apiParam   {String(50)}    name
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /campaign_status/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup campaign_status
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
    http://localhost:8001/api/v1.0/campaign_status/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /campaign_status/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup campaign_status
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/campaign_status/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# test_type
"""
@api {get} /test_type/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup test_type
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/test_type/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /test_type/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup test_type
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/test_type/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
            ...
        }
    }

@apiSuccess {Integer}  id
@apiSuccess {String}   name
@apiSuccess {Integer}  group_id
@apiSuccess {Boolean}  is_group
@apiSuccess {String}   test_table_name
@apiSuccess {String}   checkbox_name
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /test_type/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup test_type
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name", "is_group": false}' \
         http://localhost:8001/api/v1.0/test_type/

@apiParam   {String(50)}  name              required
@apiParam   {Integer}     group_id
@apiParam   {Boolean}     is_group          required
@apiParam   {String(100)} test_table_name
@apiParam   {String(100)} checkbox_name
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /test_type/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup test_type
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
    http://localhost:8001/api/v1.0/test_type/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /test_type/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup test_type
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/test_type/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# bushing_test
"""
@api {get} /bushing_test/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup bushing_test
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/bushing_test/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /bushing_test/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup bushing_test
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/bushing_test/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "test_result_id": 1,
            ...
        }
    }

@apiSuccess {Integer}  id
@apiSuccess {Integer}  test_result_id
@apiSuccess {Float}    h1
@apiSuccess {Float}    h2
@apiSuccess {Float}    h3
@apiSuccess {Float}    hn
@apiSuccess {Float}    h1c1
@apiSuccess {Float}    h2c1
@apiSuccess {Float}    h3c1
@apiSuccess {Float}    hnc1
@apiSuccess {Float}    h1c2
@apiSuccess {Float}    h2c2
@apiSuccess {Float}    h3c2
@apiSuccess {Float}    hnc2
@apiSuccess {Float}    x1
@apiSuccess {Float}    x2
@apiSuccess {Float}    x3
@apiSuccess {Float}    xn
@apiSuccess {Float}    x1c1
@apiSuccess {Float}    x2c1
@apiSuccess {Float}    x3c1
@apiSuccess {Float}    xnc1
@apiSuccess {Float}    x1c2
@apiSuccess {Float}    x2c2
@apiSuccess {Float}    x3c2
@apiSuccess {Float}    xnc2
@apiSuccess {Float}    t1
@apiSuccess {Float}    t2
@apiSuccess {Float}    t3
@apiSuccess {Float}    tn
@apiSuccess {Float}    t1c1
@apiSuccess {Float}    t2c1
@apiSuccess {Float}    t3c1
@apiSuccess {Float}    tnc1
@apiSuccess {Float}    t1c2
@apiSuccess {Float}    t2c2
@apiSuccess {Float}    t3c2
@apiSuccess {Float}    tnc2
@apiSuccess {Float}    temperature
@apiSuccess {Float}    facteur
@apiSuccess {Float}    facteur1
@apiSuccess {Float}    facteur2
@apiSuccess {Float}    q1
@apiSuccess {Float}    q2
@apiSuccess {Float}    q3
@apiSuccess {Float}    qn
@apiSuccess {Float}    q1c1
@apiSuccess {Float}    q2c1
@apiSuccess {Float}    q3c1
@apiSuccess {Float}    qnc1
@apiSuccess {Float}    q1c2
@apiSuccess {Float}    q2c2
@apiSuccess {Float}    q3c2
@apiSuccess {Float}    qnc2
@apiSuccess {Float}    facteur3
@apiSuccess {Float}    humidity
@apiSuccess {Float}    test_kv_h1
@apiSuccess {Float}    test_kv_h2
@apiSuccess {Float}    test_kv_h3
@apiSuccess {Float}    test_kv_hn
@apiSuccess {Float}    test_kv_x1
@apiSuccess {Float}    test_kv_x2
@apiSuccess {Float}    test_kv_x3
@apiSuccess {Float}    test_kv_xn
@apiSuccess {Float}    test_kv_t1
@apiSuccess {Float}    test_kv_t2
@apiSuccess {Float}    test_kv_t3
@apiSuccess {Float}    test_kv_tn
@apiSuccess {Float}    test_kv_q1
@apiSuccess {Float}    test_kv_q2
@apiSuccess {Float}    test_kv_q3
@apiSuccess {Float}    test_kv_qn
@apiSuccess {Float}    test_pfc2_h1
@apiSuccess {Float}    test_pfc2_h2
@apiSuccess {Float}    test_pfc2_h3
@apiSuccess {Float}    test_pfc2_hn
@apiSuccess {Float}    test_pfc2_x1
@apiSuccess {Float}    test_pfc2_x2
@apiSuccess {Float}    test_pfc2_x3
@apiSuccess {Float}    test_pfc2_xn
@apiSuccess {Float}    test_pfc2_t1
@apiSuccess {Float}    test_pfc2_t2
@apiSuccess {Float}    test_pfc2_t3
@apiSuccess {Float}    test_pfc2_tn
@apiSuccess {Float}    test_pfc2_q1
@apiSuccess {Float}    test_pfc2_q2
@apiSuccess {Float}    test_pfc2_q3
@apiSuccess {Float}    test_pfc2_qn
@apiSuccess {Float}    facteurn
@apiSuccess {Float}    facteurn1
@apiSuccess {Float}    facteurn2
@apiSuccess {Float}    facteurn3
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /bushing_test/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup bushing_test
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"test_result_id":2, "h1": 13}' \
         http://localhost:8001/api/v1.0/bushing_test/

@apiParam   {Integer}    test_result_id
@apiParam   {Float}    h1
@apiParam   {Float}    h2
@apiParam   {Float}    h3
@apiParam   {Float}    hn
@apiParam   {Float}    h1c1
@apiParam   {Float}    h2c1
@apiParam   {Float}    h3c1
@apiParam   {Float}    hnc1
@apiParam   {Float}    h1c2
@apiParam   {Float}    h2c2
@apiParam   {Float}    h3c2
@apiParam   {Float}    hnc2
@apiParam   {Float}    x1
@apiParam   {Float}    x2
@apiParam   {Float}    x3
@apiParam   {Float}    xn
@apiParam   {Float}    x1c1
@apiParam   {Float}    x2c1
@apiParam   {Float}    x3c1
@apiParam   {Float}    xnc1
@apiParam   {Float}    x1c2
@apiParam   {Float}    x2c2
@apiParam   {Float}    x3c2
@apiParam   {Float}    xnc2
@apiParam   {Float}    t1
@apiParam   {Float}    t2
@apiParam   {Float}    t3
@apiParam   {Float}    tn
@apiParam   {Float}    t1c1
@apiParam   {Float}    t2c1
@apiParam   {Float}    t3c1
@apiParam   {Float}    tnc1
@apiParam   {Float}    t1c2
@apiParam   {Float}    t2c2
@apiParam   {Float}    t3c2
@apiParam   {Float}    tnc2
@apiParam   {Float}    temperature
@apiParam   {Float}    facteur
@apiParam   {Float}    facteur1
@apiParam   {Float}    facteur2
@apiParam   {Float}    q1
@apiParam   {Float}    q2
@apiParam   {Float}    q3
@apiParam   {Float}    qn
@apiParam   {Float}    q1c1
@apiParam   {Float}    q2c1
@apiParam   {Float}    q3c1
@apiParam   {Float}    qnc1
@apiParam   {Float}    q1c2
@apiParam   {Float}    q2c2
@apiParam   {Float}    q3c2
@apiParam   {Float}    qnc2
@apiParam   {Float}    facteur3
@apiParam   {Float}    humidity
@apiParam   {Float}    test_kv_h1
@apiParam   {Float}    test_kv_h2
@apiParam   {Float}    test_kv_h3
@apiParam   {Float}    test_kv_hn
@apiParam   {Float}    test_kv_x1
@apiParam   {Float}    test_kv_x2
@apiParam   {Float}    test_kv_x3
@apiParam   {Float}    test_kv_xn
@apiParam   {Float}    test_kv_t1
@apiParam   {Float}    test_kv_t2
@apiParam   {Float}    test_kv_t3
@apiParam   {Float}    test_kv_tn
@apiParam   {Float}    test_kv_q1
@apiParam   {Float}    test_kv_q2
@apiParam   {Float}    test_kv_q3
@apiParam   {Float}    test_kv_qn
@apiParam   {Float}    test_pfc2_h1
@apiParam   {Float}    test_pfc2_h2
@apiParam   {Float}    test_pfc2_h3
@apiParam   {Float}    test_pfc2_hn
@apiParam   {Float}    test_pfc2_x1
@apiParam   {Float}    test_pfc2_x2
@apiParam   {Float}    test_pfc2_x3
@apiParam   {Float}    test_pfc2_xn
@apiParam   {Float}    test_pfc2_t1
@apiParam   {Float}    test_pfc2_t2
@apiParam   {Float}    test_pfc2_t3
@apiParam   {Float}    test_pfc2_tn
@apiParam   {Float}    test_pfc2_q1
@apiParam   {Float}    test_pfc2_q2
@apiParam   {Float}    test_pfc2_q3
@apiParam   {Float}    test_pfc2_qn
@apiParam   {Float}    facteurn
@apiParam   {Float}    facteurn1
@apiParam   {Float}    facteurn2
@apiParam   {Float}    facteurn3
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /bushing_test/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup bushing_test
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"test_result_id": 2}'\
    http://localhost:8001/api/v1.0/bushing_test/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /bushing_test/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup bushing_test
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/bushing_test/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# winding_test
"""
@api {get} /winding_test/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup winding_test
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/winding_test/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /winding_test/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup winding_test
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/winding_test/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "test_result_id": 2,
            ...
        }
    }

@apiSuccess {Integer}        id
@apiSuccess {Integer}    test_result_id
@apiSuccess {Float}    test_kv1
@apiSuccess {Float}    test_kv2
@apiSuccess {Float}    test_kv3
@apiSuccess {Float}    test_kv4
@apiSuccess {Float}    test_kv5
@apiSuccess {Float}    test_kv6
@apiSuccess {Float}    test_kv7
@apiSuccess {Float}    test_kv8
@apiSuccess {Float}    test_kv9
@apiSuccess {Float}    test_kv10
@apiSuccess {Float}    m_meter1
@apiSuccess {Float}    m_meter2
@apiSuccess {Float}    m_meter3
@apiSuccess {Float}    m_meter4
@apiSuccess {Float}    m_meter5
@apiSuccess {Float}    m_meter6
@apiSuccess {Float}    m_meter7
@apiSuccess {Float}    m_meter8
@apiSuccess {Float}    m_meter9
@apiSuccess {Float}    m_meter10
@apiSuccess {Float}    m_multiplier1
@apiSuccess {Float}    m_multiplier2
@apiSuccess {Float}    m_multiplier3
@apiSuccess {Float}    m_multiplier4
@apiSuccess {Float}    m_multiplier5
@apiSuccess {Float}    m_multiplier6
@apiSuccess {Float}    m_multiplier7
@apiSuccess {Float}    m_multiplier8
@apiSuccess {Float}    m_multiplier9
@apiSuccess {Float}    m_multiplier10
@apiSuccess {Float}    w_meter1
@apiSuccess {Float}    w_meter2
@apiSuccess {Float}    w_meter3
@apiSuccess {Float}    w_meter4
@apiSuccess {Float}    w_meter5
@apiSuccess {Float}    w_meter6
@apiSuccess {Float}    w_meter7
@apiSuccess {Float}    w_meter8
@apiSuccess {Float}    w_meter9
@apiSuccess {Float}    w_meter10
@apiSuccess {Float}    w_multiplier1
@apiSuccess {Float}    w_multiplier2
@apiSuccess {Float}    w_multiplier3
@apiSuccess {Float}    w_multiplier4
@apiSuccess {Float}    w_multiplier5
@apiSuccess {Float}    w_multiplier6
@apiSuccess {Float}    w_multiplier7
@apiSuccess {Float}    w_multiplier8
@apiSuccess {Float}    w_multiplier9
@apiSuccess {Float}    w_multiplier10
@apiSuccess {Boolean}    type_doble
@apiSuccess {Float}    humidity
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /winding_test/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup winding_test
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"test_result_id":2, "type_doble": true}' \
         http://localhost:8001/api/v1.0/winding_test/

@apiParam   {Integer}    test_result_id
@apiParam   {Float}    test_kv1
@apiParam   {Float}    test_kv2
@apiParam   {Float}    test_kv3
@apiParam   {Float}    test_kv4
@apiParam   {Float}    test_kv5
@apiParam   {Float}    test_kv6
@apiParam   {Float}    test_kv7
@apiParam   {Float}    test_kv8
@apiParam   {Float}    test_kv9
@apiParam   {Float}    test_kv10
@apiParam   {Float}    m_meter1
@apiParam   {Float}    m_meter2
@apiParam   {Float}    m_meter3
@apiParam   {Float}    m_meter4
@apiParam   {Float}    m_meter5
@apiParam   {Float}    m_meter6
@apiParam   {Float}    m_meter7
@apiParam   {Float}    m_meter8
@apiParam   {Float}    m_meter9
@apiParam   {Float}    m_meter10
@apiParam   {Float}    m_multiplier1
@apiParam   {Float}    m_multiplier2
@apiParam   {Float}    m_multiplier3
@apiParam   {Float}    m_multiplier4
@apiParam   {Float}    m_multiplier5
@apiParam   {Float}    m_multiplier6
@apiParam   {Float}    m_multiplier7
@apiParam   {Float}    m_multiplier8
@apiParam   {Float}    m_multiplier9
@apiParam   {Float}    m_multiplier10
@apiParam   {Float}    w_meter1
@apiParam   {Float}    w_meter2
@apiParam   {Float}    w_meter3
@apiParam   {Float}    w_meter4
@apiParam   {Float}    w_meter5
@apiParam   {Float}    w_meter6
@apiParam   {Float}    w_meter7
@apiParam   {Float}    w_meter8
@apiParam   {Float}    w_meter9
@apiParam   {Float}    w_meter10
@apiParam   {Float}    w_multiplier1
@apiParam   {Float}    w_multiplier2
@apiParam   {Float}    w_multiplier3
@apiParam   {Float}    w_multiplier4
@apiParam   {Float}    w_multiplier5
@apiParam   {Float}    w_multiplier6
@apiParam   {Float}    w_multiplier7
@apiParam   {Float}    w_multiplier8
@apiParam   {Float}    w_multiplier9
@apiParam   {Float}    w_multiplier10
@apiParam   {Boolean}    type_doble
@apiParam   {Float}    humidity
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /winding_test/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup winding_test
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"type_doble": false}'\
    http://localhost:8001/api/v1.0/winding_test/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /winding_test/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup winding_test
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/winding_test/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# visual_inspection_test
"""
@api {get} /visual_inspection_test/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup visual_inspection_test
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/visual_inspection_test/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /visual_inspection_test/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup visual_inspection_test
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/visual_inspection_test/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "test_result_id": 2,
            ...
        }
    }

@apiSuccess {Integer}        id
@apiSuccess {Integer}      test_result_id
@apiSuccess {String(1000)} notes
@apiSuccess {Integer}    tank_cover_gasket_id
@apiSuccess {Integer}    tank_manhole_gasket_id
@apiSuccess {Integer}    tank_gas_relay_id
@apiSuccess {Integer}    tank_oil_level_id
@apiSuccess {Float}    tank_winding_temp_max
@apiSuccess {Float}    tank_winding_temp_actual
@apiSuccess {Float}    tank_oil_temp_max
@apiSuccess {Float}    tank_oil_temp_actual
@apiSuccess {Boolean}    tank_winding_flag
@apiSuccess {Boolean}    tank_oil_flag
@apiSuccess {Integer}    tank_pressure_unit_id
@apiSuccess {Float}    tank_pressure
@apiSuccess {Integer}    tank_overpressure_valve_id
@apiSuccess {Integer}    tank_ampling_valve_id
@apiSuccess {Integer}    tank_oil_pump_id
@apiSuccess {Float}     tank_gas_analyser
@apiSuccess {Integer}    tank_overall_condition_id
@apiSuccess {Integer}    exp_tank_pipe_gasket_id
@apiSuccess {Integer}    exp_tank_oil_level_id
@apiSuccess {Integer}    exp_tank_paint_id
@apiSuccess {Integer}    exp_tank_overall_condition_id
@apiSuccess {Integer}    bushing_gasket_id
@apiSuccess {Integer}    bushing_oil_level_id
@apiSuccess {Integer}    bushing_overall_condition_id
@apiSuccess {Integer}    tap_changer_gasket_id
@apiSuccess {Integer}    tap_changer_oil_level_id
@apiSuccess {Float}      tap_changer_temp_max
@apiSuccess {Float}      tap_changer_temp_actual
@apiSuccess {Float}      tap_changer_pressure_max
@apiSuccess {Float}      tap_changer_pressure_actual
@apiSuccess {Integer}    tap_changer_pressure_unit_id
@apiSuccess {Float}      tap_changer_tap_position
@apiSuccess {Integer}    tap_changer_overpressure_valve_id
@apiSuccess {Integer}    tap_changer_sampling_valve_id
@apiSuccess {Integer}    tap_changer_operation_counter
@apiSuccess {Integer}    tap_changer_counter_id
@apiSuccess {Integer}    tap_changer_filter_id
@apiSuccess {Integer}    tap_changer_overall_condition_id
@apiSuccess {Integer}    radiator_fan_id
@apiSuccess {Integer}    radiator_gasket_id
@apiSuccess {Integer}    radiator_overall_condition_id
@apiSuccess {Integer}    control_cab_connection_id
@apiSuccess {Integer}    control_cab_heating_id
@apiSuccess {Integer}    control_cab_overall_condition_id
@apiSuccess {Float}      grounding_value
@apiSuccess {Integer}    grounding_connection_id
@apiSuccess {Integer}    misc_foundation_id
@apiSuccess {Float}    misc_temp_ambiant
@apiSuccess {Float}    misc_load
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /visual_inspection_test/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup visual_inspection_test
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"test_result_id":2}' \
         http://localhost:8001/api/v1.0/visual_inspection_test/

@apiParam   {Integer}      test_result_id
@apiParam   {String(1000)} notes
@apiParam   {Integer}    tank_cover_gasket_id
@apiParam   {Integer}    tank_manhole_gasket_id
@apiParam   {Integer}    tank_gas_relay_id
@apiParam   {Integer}    tank_oil_level_id
@apiParam   {Float}    tank_winding_temp_max
@apiParam   {Float}    tank_winding_temp_actual
@apiParam   {Float}    tank_oil_temp_max
@apiParam   {Float}    tank_oil_temp_actual
@apiParam   {Boolean}    tank_winding_flag
@apiParam   {Boolean}    tank_oil_flag
@apiParam   {Integer}    tank_pressure_unit_id
@apiParam   {Float}    tank_pressure
@apiParam   {Integer}    tank_overpressure_valve_id
@apiParam   {Integer}    tank_ampling_valve_id
@apiParam   {Integer}    tank_oil_pump_id
@apiParam   {Float}    tank_gas_analyser
@apiParam   {Integer}    tank_overall_condition_id
@apiParam   {Integer}    exp_tank_pipe_gasket_id
@apiParam   {Integer}    exp_tank_oil_level_id
@apiParam   {Integer}    exp_tank_paint_id
@apiParam   {Integer}    exp_tank_overall_condition_id
@apiParam   {Integer}    bushing_gasket_id
@apiParam   {Integer}    bushing_oil_level_id
@apiParam   {Integer}    bushing_overall_condition_id
@apiParam   {Integer}    tap_changer_gasket_id
@apiParam   {Integer}    tap_changer_oil_level_id
@apiParam   {Float}    tap_changer_temp_max
@apiParam   {Float}    tap_changer_temp_actual
@apiParam   {Float}    tap_changer_pressure_max
@apiParam   {Float}    tap_changer_pressure_actual
@apiParam   {Integer}    tap_changer_pressure_unit_id
@apiParam   {Float}    tap_changer_tap_position
@apiParam   {Integer}    tap_changer_overpressure_valve_id
@apiParam   {Integer}    tap_changer_sampling_valve_id
@apiParam   {Integer}    tap_changer_operation_counter
@apiParam   {Integer}    tap_changer_counter_id
@apiParam   {Integer}    tap_changer_filter_id
@apiParam   {Integer}    tap_changer_overall_condition_id
@apiParam   {Integer}    radiator_fan_id
@apiParam   {Integer}    radiator_gasket_id
@apiParam   {Integer}    radiator_overall_condition_id
@apiParam   {Integer}    control_cab_connection_id
@apiParam   {Integer}    control_cab_heating_id
@apiParam   {Integer}    control_cab_overall_condition_id
@apiParam   {Float}    grounding_value
@apiParam   {Integer}    grounding_connection_id
@apiParam   {Integer}    misc_foundation_id
@apiParam   {Float}    misc_temp_ambiant
@apiParam   {Float}    misc_load
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /visual_inspection_test/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup visual_inspection_test
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"test_result_id":3}'\
    http://localhost:8001/api/v1.0/visual_inspection_test/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /visual_inspection_test/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup visual_inspection_test
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/visual_inspection_test/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# insulation_resistance_test
"""
@api {get} /insulation_resistance_test/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup insulation_resistance_test
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/insulation_resistance_test/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /insulation_resistance_test/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup insulation_resistance_test
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/insulation_resistance_test/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "test_result_id": 2,
            ...
        }
    }

@apiSuccess {Integer}        id
@apiSuccess {Integer}    test_result_id
@apiSuccess {Float}    test_kv1
@apiSuccess {Float}    resistance1
@apiSuccess {Float}    multiplier1
@apiSuccess {Float}    test_kv2
@apiSuccess {Float}    resistance2
@apiSuccess {Float}    multiplier2
@apiSuccess {Float}    test_kv3
@apiSuccess {Float}    resistance3
@apiSuccess {Float}    multiplier3
@apiSuccess {Float}    test_kv4
@apiSuccess {Float}    resistance4
@apiSuccess {Float}    multiplier4
@apiSuccess {Float}    test_kv5
@apiSuccess {Float}    resistance5
@apiSuccess {Float}    multiplier5
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /insulation_resistance_test/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup insulation_resistance_test
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"test_result_id":2}' \
         http://localhost:8001/api/v1.0/insulation_resistance_test/

@apiParam   {Integer}    test_result_id
@apiParam   {Float}    test_kv1
@apiParam   {Float}    resistance1
@apiParam   {Float}    multiplier1
@apiParam   {Float}    test_kv2
@apiParam   {Float}    resistance2
@apiParam   {Float}    multiplier2
@apiParam   {Float}    test_kv3
@apiParam   {Float}    resistance3
@apiParam   {Float}    multiplier3
@apiParam   {Float}    test_kv4
@apiParam   {Float}    resistance4
@apiParam   {Float}    multiplier4
@apiParam   {Float}    test_kv5
@apiParam   {Float}    resistance5
@apiParam   {Float}    multiplier5
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /insulation_resistance_test/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup insulation_resistance_test
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"test_result_id": 3}'\
    http://localhost:8001/api/v1.0/insulation_resistance_test/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /insulation_resistance_test/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup insulation_resistance_test
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/insulation_resistance_test/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# polymerisation_degree_test
"""
@api {get} /polymerisation_degree_test/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup polymerisation_degree_test
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/polymerisation_degree_test/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /polymerisation_degree_test/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup polymerisation_degree_test
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/polymerisation_degree_test/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "test_result_id": 2,
            ...
        }
    }

@apiSuccess {Integer}      id
@apiSuccess {Integer}      test_result_id
@apiSuccess {Float}        phase_a1
@apiSuccess {Float}        phase_a2
@apiSuccess {Float}        phase_a3
@apiSuccess {Float}        phase_b1
@apiSuccess {Float}        phase_b2
@apiSuccess {Float}        phase_b3
@apiSuccess {Float}        phase_c1
@apiSuccess {Float}        phase_c2
@apiSuccess {Float}        phase_c3
@apiSuccess {Integer(4)}   lead_a
@apiSuccess {Integer(4)}   lead_b
@apiSuccess {Integer(4)}   lead_c
@apiSuccess {Integer(4)}   lead_n
@apiSuccess {Integer(4)}   winding
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /polymerisation_degree_test/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup polymerisation_degree_test
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"test_result_id":2}' \
         http://localhost:8001/api/v1.0/polymerisation_degree_test/

@apiParam   {Integer}    test_result_id
@apiParam   {Float}    phase_a1
@apiParam   {Float}    phase_a2
@apiParam   {Float}    phase_a3
@apiParam   {Float}    phase_b1
@apiParam   {Float}    phase_b2
@apiParam   {Float}    phase_b3
@apiParam   {Float}    phase_c1
@apiParam   {Float}    phase_c2
@apiParam   {Float}    phase_c3
@apiParam   {Integer(4)}   lead_a
@apiParam   {Integer(4)}   lead_b
@apiParam   {Integer(4)}   lead_c
@apiParam   {Integer(4)}   lead_n
@apiParam   {Integer(4)}   winding
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /polymerisation_degree_test/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup polymerisation_degree_test
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"test_result_id": 3}'\
    http://localhost:8001/api/v1.0/polymerisation_degree_test/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /polymerisation_degree_test/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup polymerisation_degree_test
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/polymerisation_degree_test/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# transformer_turn_ratio_test
"""
@api {get} /transformer_turn_ratio_test/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup transformer_turn_ratio_test
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/transformer_turn_ratio_test/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /transformer_turn_ratio_test/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup transformer_turn_ratio_test
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/transformer_turn_ratio_test/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "test_result_id": 2,
            ...
        }
    }

@apiSuccess {Integer}   id
@apiSuccess {Integer}   test_result_id
@apiSuccess {Integer}   winding          required
@apiSuccess {Integer}   tap_position
@apiSuccess {Float}     measured_current1
@apiSuccess {Float}     measured_current2
@apiSuccess {Float}     measured_current3
@apiSuccess {Float}     calculated_current1
@apiSuccess {Float}     calculated_current2
@apiSuccess {Float}     calculated_current3
@apiSuccess {Float}     error1
@apiSuccess {Float}     error2
@apiSuccess {Float}     error3
@apiSuccess {Float}     ratio
@apiSuccess {Boolean}   select
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /transformer_turn_ratio_test/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup transformer_turn_ratio_test
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"test_result_id":2, "winding":5}' \
         http://localhost:8001/api/v1.0/transformer_turn_ratio_test/

@apiParam   {Integer}   test_result_id
@apiParam   {Integer}   winding          required
@apiParam   {Integer}   tap_position
@apiParam   {Float}     measured_current1
@apiParam   {Float}     measured_current2
@apiParam   {Float}     measured_current3
@apiParam   {Float}     calculated_current1
@apiParam   {Float}     calculated_current2
@apiParam   {Float}     calculated_current3
@apiParam   {Float}     error1
@apiParam   {Float}     error2
@apiParam   {Float}     error3
@apiParam   {Float}     ratio
@apiParam   {Boolean}   select
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /transformer_turn_ratio_test/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup transformer_turn_ratio_test
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"test_result_id":3}'\
    http://localhost:8001/api/v1.0/transformer_turn_ratio_test/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /transformer_turn_ratio_test/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup transformer_turn_ratio_test
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/transformer_turn_ratio_test/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# winding_resistance_test
"""
@api {get} /winding_resistance_test/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup winding_resistance_test
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/winding_resistance_test/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /winding_resistance_test/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup winding_resistance_test
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/winding_resistance_test/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "test_result_id": 2,
            ...
        }
    }

@apiSuccess {Integer}        id
@apiSuccess {Integer}   test_result_id
@apiSuccess {Integer}   winding          required
@apiSuccess {Integer}   tap_position
@apiSuccess {Float}     mesure1
@apiSuccess {Float}     temp1
@apiSuccess {Float}     corr1
@apiSuccess {Float}     mesure2
@apiSuccess {Float}     temp2
@apiSuccess {Float}     corr2
@apiSuccess {Float}     mesure3
@apiSuccess {Float}     temp3
@apiSuccess {Float}     corr3
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /winding_resistance_test/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup winding_resistance_test
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"test_result_id":2, "winding": 5}' \
         http://localhost:8001/api/v1.0/winding_resistance_test/

@apiParam   {Integer}   test_result_id
@apiParam   {Integer}   winding          required
@apiParam   {Integer}   tap_position
@apiParam   {Float}     mesure1
@apiParam   {Float}     temp1
@apiParam   {Float}     corr1
@apiParam   {Float}     mesure2
@apiParam   {Float}     temp2
@apiParam   {Float}     corr2
@apiParam   {Float}     mesure3
@apiParam   {Float}     temp3
@apiParam   {Float}     corr3
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /winding_resistance_test/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup winding_resistance_test
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"test_result_id":3}'\
    http://localhost:8001/api/v1.0/winding_resistance_test/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /winding_resistance_test/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup winding_resistance_test
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/winding_resistance_test/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# dissolved_gas_test
"""
@api {get} /dissolved_gas_test/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup dissolved_gas_test
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/dissolved_gas_test/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /dissolved_gas_test/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup dissolved_gas_test
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/dissolved_gas_test/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "test_result_id": 2,
            ...
        }
    }

@apiSuccess {Integer}        id
@apiSuccess {Integer}   test_result_id
@apiSuccess {Float}     h2
@apiSuccess {Float}     o2
@apiSuccess {Float}     n2
@apiSuccess {Float}     co
@apiSuccess {Float}     ch4
@apiSuccess {Float}     co2
@apiSuccess {Float}     c2h2
@apiSuccess {Float}     c2h4
@apiSuccess {Float}     c2h6
@apiSuccess {Boolean}   h2_flag
@apiSuccess {Boolean}   o2_flag
@apiSuccess {Boolean}   n2_flag
@apiSuccess {Boolean}   co_flag
@apiSuccess {Boolean}   ch4_flag
@apiSuccess {Boolean}   co2_flag
@apiSuccess {Boolean}   c2h2_flag
@apiSuccess {Boolean}   c2h4_flag
@apiSuccess {Boolean}   c2h6_flag
@apiSuccess {Float}     cap_gaz
@apiSuccess {Float}     content_gaz
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /dissolved_gas_test/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup dissolved_gas_test
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"test_result_id":2}' \
         http://localhost:8001/api/v1.0/dissolved_gas_test/

@apiParam   {Integer}   test_result_id
@apiParam   {Float}     h2
@apiParam   {Float}     o2
@apiParam   {Float}     n2
@apiParam   {Float}     co
@apiParam   {Float}     ch4
@apiParam   {Float}     co2
@apiParam   {Float}     c2h2
@apiParam   {Float}     c2h4
@apiParam   {Float}     c2h6
@apiParam   {Boolean}   h2_flag
@apiParam   {Boolean}   o2_flag
@apiParam   {Boolean}   n2_flag
@apiParam   {Boolean}   co_flag
@apiParam   {Boolean}   ch4_flag
@apiParam   {Boolean}   co2_flag
@apiParam   {Boolean}   c2h2_flag
@apiParam   {Boolean}   c2h4_flag
@apiParam   {Boolean}   c2h6_flag
@apiParam   {Float}     cap_gaz
@apiParam   {Float}     content_gaz
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /dissolved_gas_test/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup dissolved_gas_test
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"test_result_id":3}'\
    http://localhost:8001/api/v1.0/dissolved_gas_test/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /dissolved_gas_test/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup dissolved_gas_test
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/dissolved_gas_test/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# water_test
"""
@api {get} /water_test/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup water_test
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/water_test/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /water_test/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup water_test
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/water_test/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "test_result_id": 2,
            ...
        }
    }

@apiSuccess {Integer}    id
@apiSuccess {Integer}    test_result_id
@apiSuccess {Boolean}    water_flag
@apiSuccess {Float}      water
@apiSuccess {String(80)} remark
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /water_test/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup water_test
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"test_result_id":2}' \
         http://localhost:8001/api/v1.0/water_test/

@apiParam   {Integer}    test_result_id
@apiParam   {Boolean}    water_flag
@apiParam   {Float}      water
@apiParam   {String(80)} remark
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /water_test/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup water_test
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"test_result_id":3}'\
    http://localhost:8001/api/v1.0/water_test/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /water_test/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup water_test
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/water_test/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# furan_test
"""
@api {get} /furan_test/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup furan_test
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/furan_test/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /furan_test/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup furan_test
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/furan_test/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "test_result_id": 2,
            ...
        }
    }

@apiSuccess {Integer}   id
@apiSuccess {Integer}   test_result_id
@apiSuccess {Float}     hmf
@apiSuccess {Float}     fol
@apiSuccess {Float}     fal
@apiSuccess {Float}     acf
@apiSuccess {Float}     mef
@apiSuccess {Boolean}   hmf_flag
@apiSuccess {Boolean}   fol_flag
@apiSuccess {Boolean}   fal_flag
@apiSuccess {Boolean}   acf_flag
@apiSuccess {Boolean}   mef_flag
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /furan_test/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup furan_test
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"test_result_id":2}' \
         http://localhost:8001/api/v1.0/furan_test/

@apiParam   {Integer}   test_result_id
@apiParam   {Float}     hmf
@apiParam   {Float}     fol
@apiParam   {Float}     fal
@apiParam   {Float}     acf
@apiParam   {Float}     mef
@apiParam   {Boolean}   hmf_flag
@apiParam   {Boolean}   fol_flag
@apiParam   {Boolean}   fal_flag
@apiParam   {Boolean}   acf_flag
@apiParam   {Boolean}   mef_flag
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /furan_test/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup furan_test
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"test_result_id":3}'\
    http://localhost:8001/api/v1.0/furan_test/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /furan_test/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup furan_test
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/furan_test/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# inhibitor_test
"""
@api {get} /inhibitor_test/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup inhibitor_test
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/inhibitor_test/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /inhibitor_test/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup inhibitor_test
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/inhibitor_test/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "test_result_id": 2,
            ...
        }
    }

@apiSuccess {Integer}    id
@apiSuccess {Integer}    test_result_id
@apiSuccess {Integer}    inhibitor_type_id
@apiSuccess {Float}      inhibitor
@apiSuccess {String(80)} remark
@apiSuccess {Boolean}    inhibitor_flag
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /inhibitor_test/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup inhibitor_test
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"test_result_id":2}' \
         http://localhost:8001/api/v1.0/inhibitor_test/

@apiParam   {Integer}    test_result_id
@apiParam   {Integer}    inhibitor_type_id
@apiParam   {Float}      inhibitor
@apiParam   {String(80)} remark
@apiParam   {Boolean}    inhibitor_flag
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /inhibitor_test/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup inhibitor_test
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"test_result_id":3}'\
    http://localhost:8001/api/v1.0/inhibitor_test/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /inhibitor_test/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup inhibitor_test
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/inhibitor_test/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# inhibitor_type
"""
@api {get} /inhibitor_type/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup inhibitor_type
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/inhibitor_type/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /inhibitor_type/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup inhibitor_type
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/inhibitor_type/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
            ...
        }
    }

@apiSuccess {Integer}        id
@apiSuccess {String(10)}    name
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /inhibitor_type/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup inhibitor_type
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/inhibitor_type/

@apiParam   {String(10)}    name
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /inhibitor_type/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup inhibitor_type
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "other name"}'\
    http://localhost:8001/api/v1.0/inhibitor_type/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /inhibitor_type/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup inhibitor_type
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/inhibitor_type/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# pcb_test
"""
@api {get} /pcb_test/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup pcb_test
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/pcb_test/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /pcb_test/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup pcb_test
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/pcb_test/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "test_result_id": 2,
            ...
        }
    }

@apiSuccess {Integer}   id
@apiSuccess {Integer}   test_result_id
@apiSuccess {Float}     aroclor_1242
@apiSuccess {Float}     aroclor_1254
@apiSuccess {Float}     aroclor_1260
@apiSuccess {Boolean}   aroclor_1242_flag
@apiSuccess {Boolean}   aroclor_1254_flag
@apiSuccess {Boolean}   aroclor_1260_flag
@apiSuccess {Float}     pcb_total
@apiSuccess {Boolean}   total_flag
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /pcb_test/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup pcb_test
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"test_result_id":2}' \
         http://localhost:8001/api/v1.0/pcb_test/

@apiParam   {Integer}   test_result_id
@apiParam   {Float}     aroclor_1242
@apiParam   {Float}     aroclor_1254
@apiParam   {Float}     aroclor_1260
@apiParam   {Boolean}   aroclor_1242_flag
@apiParam   {Boolean}   aroclor_1254_flag
@apiParam   {Boolean}   aroclor_1260_flag
@apiParam   {Float}     pcb_total
@apiParam   {Boolean}   total_flag
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /pcb_test/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup pcb_test
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"test_result_id":3}'\
    http://localhost:8001/api/v1.0/pcb_test/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /pcb_test/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup pcb_test
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/pcb_test/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# particle_test
"""
@api {get} /particle_test/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup particle_test
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/particle_test/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /particle_test/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup particle_test
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/particle_test/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "test_result_id": 2,
            ...
        }
    }

@apiSuccess {Integer}        id
@apiSuccess {Integer}   test_result_id
@apiSuccess {Float}     _2um
@apiSuccess {Float}     _5um
@apiSuccess {Float}     _10um
@apiSuccess {Float}     _15um
@apiSuccess {Float}     _25um
@apiSuccess {Float}     _50um
@apiSuccess {Float}     _100um
@apiSuccess {Float}     nas1638
@apiSuccess {Float}     iso4406_1
@apiSuccess {Float}     iso4406_2
@apiSuccess {Float}     iso4406_3
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /particle_test/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup particle_test
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"test_result_id":2}' \
         http://localhost:8001/api/v1.0/particle_test/

@apiParam   {Integer}   test_result_id
@apiParam   {Float}     _2um
@apiParam   {Float}     _5um
@apiParam   {Float}     _10um
@apiParam   {Float}     _15um
@apiParam   {Float}     _25um
@apiParam   {Float}     _50um
@apiParam   {Float}     _100um
@apiParam   {Float}     nas1638
@apiParam   {Float}     iso4406_1
@apiParam   {Float}     iso4406_2
@apiParam   {Float}     iso4406_3
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /particle_test/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup particle_test
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"test_result_id":3}'\
    http://localhost:8001/api/v1.0/particle_test/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /particle_test/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup particle_test
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/particle_test/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# metals_in_oil_test
"""
@api {get} /metals_in_oil_test/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup metals_in_oil_test
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/metals_in_oil_test/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /metals_in_oil_test/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup metals_in_oil_test
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/metals_in_oil_test/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "test_result_id": 2,
            ...
        }
    }

@apiSuccess {Integer}        id
@apiSuccess {Integer}   test_result_id
@apiSuccess {Float}     iron
@apiSuccess {Float}     nickel
@apiSuccess {Float}     aluminium
@apiSuccess {Float}     copper
@apiSuccess {Float}     tin
@apiSuccess {Float}     silver
@apiSuccess {Float}     lead
@apiSuccess {Float}     zinc
@apiSuccess {Float}     arsenic
@apiSuccess {Float}     cadmium
@apiSuccess {Float}     chrome
@apiSuccess {Boolean}   iron_flag
@apiSuccess {Boolean}   nickel_flag
@apiSuccess {Boolean}   aluminium_flag
@apiSuccess {Boolean}   copper_flag
@apiSuccess {Boolean}   tin_flag
@apiSuccess {Boolean}   silver_flag
@apiSuccess {Boolean}   lead_flag
@apiSuccess {Boolean}   zinc_flag
@apiSuccess {Boolean}   arsenic_flag
@apiSuccess {Boolean}   cadmium_flag
@apiSuccess {Boolean}   chrome_flag
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /metals_in_oil_test/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup metals_in_oil_test
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"test_result_id":2}' \
         http://localhost:8001/api/v1.0/metals_in_oil_test/

@apiParam   {Integer}   test_result_id
@apiParam   {Float}     iron
@apiParam   {Float}     nickel
@apiParam   {Float}     aluminium
@apiParam   {Float}     copper
@apiParam   {Float}     tin
@apiParam   {Float}     silver
@apiParam   {Float}     lead
@apiParam   {Float}     zinc
@apiParam   {Float}     arsenic
@apiParam   {Float}     cadmium
@apiParam   {Float}     chrome
@apiParam   {Boolean}   iron_flag
@apiParam   {Boolean}   nickel_flag
@apiParam   {Boolean}   aluminium_flag
@apiParam   {Boolean}   copper_flag
@apiParam   {Boolean}   tin_flag
@apiParam   {Boolean}   silver_flag
@apiParam   {Boolean}   lead_flag
@apiParam   {Boolean}   zinc_flag
@apiParam   {Boolean}   arsenic_flag
@apiParam   {Boolean}   cadmium_flag
@apiParam   {Boolean}   chrome_flag
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /metals_in_oil_test/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup metals_in_oil_test
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"test_result_id":3}'\
    http://localhost:8001/api/v1.0/metals_in_oil_test/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /metals_in_oil_test/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup metals_in_oil_test
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/metals_in_oil_test/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# fluid_test
"""
@api {get} /fluid_test/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup fluid_test
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/fluid_test/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /fluid_test/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup fluid_test
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/fluid_test/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "test_result_id": 2,
            ...
        }
    }

@apiSuccess {Integer}    id
@apiSuccess {Integer}    test_result_id
@apiSuccess {Float}      dielectric_1816
@apiSuccess {Float}      dielectric_1816_2
@apiSuccess {Float}      dielectric_877
@apiSuccess {Float}      dielectric_iec_156
@apiSuccess {Float}      acidity
@apiSuccess {Float}      color
@apiSuccess {Float}      ift
@apiSuccess {String(25)} visual
@apiSuccess {Float}      density
@apiSuccess {Float}      pf20c
@apiSuccess {Float}      pf100c
@apiSuccess {Float}      sludge
@apiSuccess {Float}      aniline_point
@apiSuccess {String(25)} corrosive_sulfur
@apiSuccess {Float}      viscosity
@apiSuccess {Float}      flash_point
@apiSuccess {Float}      pour_point
@apiSuccess {Boolean}    dielectric_1816_flag
@apiSuccess {Boolean}    dielectric_1816_2_flag
@apiSuccess {Boolean}    dielectric_877_flag
@apiSuccess {Boolean}    dielectric_iec_156_flag
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /fluid_test/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup fluid_test
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"test_result_id":2}' \
         http://localhost:8001/api/v1.0/fluid_test/

@apiParam   {Integer}    test_result_id
@apiParam   {Float}      dielectric_1816
@apiParam   {Float}      dielectric_1816_2
@apiParam   {Float}      dielectric_877
@apiParam   {Float}      dielectric_iec_156
@apiParam   {Float}      acidity
@apiParam   {Float}      color
@apiParam   {Float}      ift
@apiParam   {String(25)} visual
@apiParam   {Float}      density
@apiParam   {Float}      pf20c
@apiParam   {Float}      pf100c
@apiParam   {Float}      sludge
@apiParam   {Float}      aniline_point
@apiParam   {String(25)} corrosive_sulfur
@apiParam   {Float}      viscosity
@apiParam   {Float}      flash_point
@apiParam   {Float}      pour_point
@apiParam   {Boolean}    dielectric_1816_flag
@apiParam   {Boolean}    dielectric_1816_2_flag
@apiParam   {Boolean}    dielectric_877_flag
@apiParam   {Boolean}    dielectric_iec_156_flag
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /fluid_test/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup fluid_test
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"test_result_id":3}'\
    http://localhost:8001/api/v1.0/fluid_test/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /fluid_test/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup fluid_test
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/fluid_test/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# norm_physic
"""
@api {get} /norm_physic/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup norm_physic
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/norm_physic/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /norm_physic/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup norm_physic
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/norm_physic/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
            ...
        }
    }

@apiSuccess {Integer}     id
@apiSuccess {String(20)}  name
@apiSuccess {Integer}     equipment_id
@apiSuccess {Float}       acid_min
@apiSuccess {Float}       acid_max
@apiSuccess {Float}       ift_min
@apiSuccess {Float}       ift_max
@apiSuccess {Float}       d1816_min
@apiSuccess {Float}       d1816_max
@apiSuccess {Float}       d877_min
@apiSuccess {Float}       d877_max
@apiSuccess {Float}       color_min
@apiSuccess {Float}       color_max
@apiSuccess {Float}       density_min
@apiSuccess {Float}       density_max
@apiSuccess {Float}       pf20_min
@apiSuccess {Float}       pf20_max
@apiSuccess {Float}       water_min
@apiSuccess {Float}       water_max
@apiSuccess {Float}       flashpoint_min
@apiSuccess {Float}       flashpoint_max
@apiSuccess {Float}       pourpoint_min
@apiSuccess {Float}       pourpoint_max
@apiSuccess {Float}       viscosity_min
@apiSuccess {Float}       viscosity_max
@apiSuccess {Float}       d1816_2_min
@apiSuccess {Float}       d1816_2_max
@apiSuccess {Float}       p100_min
@apiSuccess {Float}       p100_max
@apiSuccess {Integer}     fluid_type_id
@apiSuccess {Integer}     cei156_min
@apiSuccess {Integer}     cei156_max
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /norm_physic/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup norm_physic
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name", "equipment_id":2}' \
         http://localhost:8001/api/v1.0/norm_physic/

@apiParam   {String(20)}  name            required
@apiParam   {Integer}     equipment_id    required
@apiParam   {Float}       acid_min
@apiParam   {Float}       acid_max
@apiParam   {Float}       ift_min
@apiParam   {Float}       ift_max
@apiParam   {Float}       d1816_min
@apiParam   {Float}       d1816_max
@apiParam   {Float}       d877_min
@apiParam   {Float}       d877_max
@apiParam   {Float}       color_min
@apiParam   {Float}       color_max
@apiParam   {Float}       density_min
@apiParam   {Float}       density_max
@apiParam   {Float}       pf20_min
@apiParam   {Float}       pf20_max
@apiParam   {Float}       water_min
@apiParam   {Float}       water_max
@apiParam   {Float}       flashpoint_min
@apiParam   {Float}       flashpoint_max
@apiParam   {Float}       pourpoint_min
@apiParam   {Float}       pourpoint_max
@apiParam   {Float}       viscosity_min
@apiParam   {Float}       viscosity_max
@apiParam   {Float}       d1816_2_min
@apiParam   {Float}       d1816_2_max
@apiParam   {Float}       p100_min
@apiParam   {Float}       p100_max
@apiParam   {Integer}     fluid_type_id
@apiParam   {Integer}     cei156_min
@apiParam   {Integer}     cei156_max
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /norm_physic/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup norm_physic
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
    http://localhost:8001/api/v1.0/norm_physic/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /norm_physic/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup norm_physic
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/norm_physic/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# norm_gas
"""
@api {get} /norm_gas/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup norm_gas
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/norm_gas/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /norm_gas/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup norm_gas
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/norm_gas/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
            ...
        }
    }

@apiSuccess {Integer}    id
@apiSuccess {String(50)} name
@apiSuccess {Integer}    condition
@apiSuccess {Float}      h2
@apiSuccess {Float}      ch4
@apiSuccess {Float}      c2h2
@apiSuccess {Float}      c2h4
@apiSuccess {Float}      c2h6
@apiSuccess {Float}      co
@apiSuccess {Float}      co2
@apiSuccess {Float}      tdcg
@apiSuccess {Integer}    fluid_level
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /norm_gas/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup norm_gas
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/norm_gas/

@apiParam   {String(50)} name
@apiParam   {Integer}    condition
@apiParam   {Float}      h2
@apiParam   {Float}      ch4
@apiParam   {Float}      c2h2
@apiParam   {Float}      c2h4
@apiParam   {Float}      c2h6
@apiParam   {Float}      co
@apiParam   {Float}      co2
@apiParam   {Float}      tdcg
@apiParam   {Integer}    fluid_level
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /norm_gas/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup norm_gas
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
    http://localhost:8001/api/v1.0/norm_gas/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /norm_gas/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup norm_gas
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/norm_gas/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# particles
"""
@api {get} /particles/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup particles
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/particles/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /particles/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup particles
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/particles/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "equipment_id": 2,
            ...
        }
    }

@apiSuccess {Integer}   id
@apiSuccess {Integer}   equipment_id
@apiSuccess {Float}     _2um
@apiSuccess {Float}     _5um
@apiSuccess {Float}     _10um
@apiSuccess {Float}     _15um
@apiSuccess {Float}     _25um
@apiSuccess {Float}     _50um
@apiSuccess {Float}     _100um
@apiSuccess {Float}     nas1638
@apiSuccess {Float}     iso4406_1
@apiSuccess {Float}     iso4406_2
@apiSuccess {Float}     iso4406_3
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /particles/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup particles
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"equipment_id": 2}' \
         http://localhost:8001/api/v1.0/particles/

@apiParam   {Integer}   equipment_id
@apiParam   {Float}     _2um
@apiParam   {Float}     _5um
@apiParam   {Float}     _10um
@apiParam   {Float}     _15um
@apiParam   {Float}     _25um
@apiParam   {Float}     _50um
@apiParam   {Float}     _100um
@apiParam   {Float}     nas1638
@apiParam   {Float}     iso4406_1
@apiParam   {Float}     iso4406_2
@apiParam   {Float}     iso4406_3
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /particles/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup particles
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"equipment_id": 3}'\
    http://localhost:8001/api/v1.0/particles/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /particles/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup particles
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/particles/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# norm_isolation
"""
@api {get} /norm_isolation/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup norm_isolation
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/norm_isolation/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /norm_isolation/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup norm_isolation
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/norm_isolation/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "c": 2.23,
            ...
        }
    }

@apiSuccess {Integer}   id
@apiSuccess {Float}     c
@apiSuccess {Float}     f
@apiSuccess {Float}     notseal
@apiSuccess {Float}     seal
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /norm_isolation/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup norm_isolation
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"c": 2.23}' \
         http://localhost:8001/api/v1.0/norm_isolation/

@apiParam   {Float}     c
@apiParam   {Float}     f
@apiParam   {Float}     notseal
@apiParam   {Float}     seal
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /norm_isolation/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup norm_isolation
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"c": 2.24}'\
    http://localhost:8001/api/v1.0/norm_isolation/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /norm_isolation/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup norm_isolation
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/norm_isolation/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# norm_furan
"""
@api {get} /norm_furan/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup norm_furan
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/norm_furan/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /norm_furan/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup norm_furan
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/norm_furan/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
            ...
        }
    }

@apiSuccess {Integer}        id
@apiSuccess {String(50)} name
@apiSuccess {Float}      c1
@apiSuccess {Float}      c2
@apiSuccess {Float}      c3
@apiSuccess {Float}      c4
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /norm_furan/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup norm_furan
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/norm_furan/

@apiParam   {String(50)} name
@apiParam   {Float}      c1
@apiParam   {Float}      c2
@apiParam   {Float}      c3
@apiParam   {Float}      c4
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /norm_furan/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup norm_furan
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
    http://localhost:8001/api/v1.0/norm_furan/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /norm_furan/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup norm_furan
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/norm_furan/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# fluid_type
"""
@api {get} /fluid_type/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup fluid_type
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/fluid_type/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /fluid_type/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup fluid_type
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/fluid_type/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(50)}    name
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /fluid_type/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup fluid_type
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/fluid_type/

@apiParam   {String(50)}    name
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /fluid_type/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup fluid_type
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
         http://localhost:8001/api/v1.0/fluid_type/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /fluid_type/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup fluid_type
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/fluid_type/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# sampling_point
"""
@api {get} /sampling_point/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup sampling_point
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/sampling_point/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /sampling_point/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup sampling_point
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/sampling_point/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(50)}    name
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /sampling_point/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup sampling_point
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/sampling_point/

@apiParam   {String(50)}    name
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /sampling_point/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup sampling_point
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
         http://localhost:8001/api/v1.0/sampling_point/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /sampling_point/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup sampling_point
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/sampling_point/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# contract_status
"""
@api {get} /contract_status/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup contract_status
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/contract_status/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /contract_status/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup contract_status
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/contract_status/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(50)}    name
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /contract_status/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup contract_status
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/contract_status/

@apiParam   {String(50)}    name
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /contract_status/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup contract_status
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
         http://localhost:8001/api/v1.0/contract_status/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /contract_status/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup contract_status
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/contract_status/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# interrupting_medium
"""
@api {get} /interrupting_medium/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup interrupting_medium
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/interrupting_medium/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /interrupting_medium/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup interrupting_medium
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/interrupting_medium/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(50)}    name
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /interrupting_medium/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup interrupting_medium
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/interrupting_medium/

@apiParam   {String(50)}    name
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /interrupting_medium/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup interrupting_medium
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
         http://localhost:8001/api/v1.0/interrupting_medium/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /interrupting_medium/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup interrupting_medium
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/interrupting_medium/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# gas_level
"""
@api {get} /gas_level/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup gas_level
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/gas_level/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /gas_level/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup gas_level
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/gas_level/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(50)}    name
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /gas_level/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup gas_level
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/gas_level/

@apiParam   {String(50)}    name
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /gas_level/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup gas_level
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
         http://localhost:8001/api/v1.0/gas_level/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /gas_level/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup gas_level
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/gas_level/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# equipment_connection
"""
@api {get} /equipment_connection/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup equipment_connection
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/equipment_connection/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /equipment_connection/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup equipment_connection
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/equipment_connection/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "equipment_id": 2,
            "parent_id": 3,
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {Integer}       equipment_id
@apiSuccess {Integer}       parent_id
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /equipment_connection/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup equipment_connection
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"equipment_id": 2, "parent_id": 3}' \
         http://localhost:8001/api/v1.0/equipment_connection/

@apiParam   {Integer}       equipment_id
@apiParam   {Integer}       parent_id
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /equipment_connection/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup equipment_connection
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"parent_id": 4}'\
         http://localhost:8001/api/v1.0/equipment_connection/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /equipment_connection/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup equipment_connection
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/equipment_connection/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# sibling
"""
@api {get} /sibling/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup sibling
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/sibling/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /sibling/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup sibling
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/sibling/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "equipment_id": 2,
            "sibling_id": 3,
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {Integer}       equipment_id
@apiSuccess {Integer}       sibling_id
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /sibling/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup sibling
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"equipment_id": 2, "sibling_id": 3}' \
         http://localhost:8001/api/v1.0/sibling/

@apiParam   {Integer}       equipment_id
@apiParam   {Integer}       sibling_id
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /sibling/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup sibling
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"sibling_id": 4}'\
         http://localhost:8001/api/v1.0/sibling/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /sibling/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup sibling
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/sibling/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# sampling_card
"""
@api {get} /sampling_card/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup sampling_card
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/sampling_card/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /sampling_card/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup sampling_card
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/sampling_card/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "card_gathered": 5,
            "card_print": true,
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {Integer}       card_gathered
@apiSuccess {Boolean}       card_print
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /sampling_card/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup sampling_card
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"card_print": true}' \
         http://localhost:8001/api/v1.0/sampling_card/

@apiParam   {Integer}       card_gathered
@apiParam   {Boolean}       card_print
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /sampling_card/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup sampling_card
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"card_print": false}'\
         http://localhost:8001/api/v1.0/sampling_card/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /sampling_card/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup sampling_card
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/sampling_card/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# breaker_mechanism
"""
@api {get} /breaker_mechanism/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup breaker_mechanism
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/breaker_mechanism/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /breaker_mechanism/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup breaker_mechanism
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/breaker_mechanism/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(50)}    name
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /breaker_mechanism/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup breaker_mechanism
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/breaker_mechanism/

@apiParam   {String(50)}    name
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /breaker_mechanism/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup breaker_mechanism
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
         http://localhost:8001/api/v1.0/breaker_mechanism/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /breaker_mechanism/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup breaker_mechanism
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/breaker_mechanism/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# insulation
"""
@api {get} /insulation/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup insulation
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/insulation/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /insulation/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup insulation
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/insulation/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(50)}    name
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /insulation/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup insulation
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/insulation/

@apiParam   {String(50)}    name
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /insulation/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup insulation
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
         http://localhost:8001/api/v1.0/insulation/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /insulation/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup insulation
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/insulation/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# test_reason
"""
@api {get} /test_reason/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup test_reason
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/test_reason/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /test_reason/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup test_reason
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/test_reason/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(50)}    name
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /test_reason/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup test_reason
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/test_reason/

@apiParam   {String(50)}    name
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /test_reason/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup test_reason
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
         http://localhost:8001/api/v1.0/test_reason/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /test_reason/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup test_reason
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/test_reason/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# location
"""
@api {get} /location/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup location
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/location/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /location/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup location
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/location/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(50)}    name
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /location/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup location
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/location/

@apiParam   {String(50)}    name
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /location/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup location
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
         http://localhost:8001/api/v1.0/location/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /location/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup location
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/location/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# gasket_condition
"""
@api {get} /gasket_condition/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup gasket_condition
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/gasket_condition/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /gasket_condition/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup gasket_condition
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/gasket_condition/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(25)}    name
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /gasket_condition/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup gasket_condition
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/gasket_condition/

@apiParam   {String(25)}    name
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /gasket_condition/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup gasket_condition
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
         http://localhost:8001/api/v1.0/gasket_condition/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /gasket_condition/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup gasket_condition
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/gasket_condition/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# gas_relay
"""
@api {get} /gas_relay/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup gas_relay
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/gas_relay/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /gas_relay/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup gas_relay
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/gas_relay/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(25)}    name
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /gas_relay/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup gas_relay
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/gas_relay/

@apiParam   {String(25)}    name
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /gas_relay/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup gas_relay
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
         http://localhost:8001/api/v1.0/gas_relay/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /gas_relay/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup gas_relay
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/gas_relay/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# fluid_level
"""
@api {get} /fluid_level/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup fluid_level
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/fluid_level/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /fluid_level/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup fluid_level
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/fluid_level/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(25)}    name
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /fluid_level/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup fluid_level
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/fluid_level/

@apiParam   {String(25)}    name
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /fluid_level/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup fluid_level
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
         http://localhost:8001/api/v1.0/fluid_level/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /fluid_level/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup fluid_level
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/fluid_level/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# pressure_unit
"""
@api {get} /pressure_unit/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup pressure_unit
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/pressure_unit/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /pressure_unit/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup pressure_unit
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/pressure_unit/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(25)}    name
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /pressure_unit/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup pressure_unit
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/pressure_unit/

@apiParam   {String(25)}    name
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /pressure_unit/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup pressure_unit
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
         http://localhost:8001/api/v1.0/pressure_unit/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /pressure_unit/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup pressure_unit
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/pressure_unit/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# valve_condition
"""
@api {get} /valve_condition/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup valve_condition
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/valve_condition/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /valve_condition/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup valve_condition
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/valve_condition/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(25)}    name
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /valve_condition/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup valve_condition
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/valve_condition/

@apiParam   {String(25)}    name
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /valve_condition/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup valve_condition
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
         http://localhost:8001/api/v1.0/valve_condition/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /valve_condition/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup valve_condition
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/valve_condition/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# pump_condition
"""
@api {get} /pump_condition/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup pump_condition
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/pump_condition/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /pump_condition/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup pump_condition
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/pump_condition/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(25)}    name
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /pump_condition/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup pump_condition
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/pump_condition/

@apiParam   {String(25)}    name
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /pump_condition/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup pump_condition
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
         http://localhost:8001/api/v1.0/pump_condition/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /pump_condition/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup pump_condition
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/pump_condition/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# overall_condition
"""
@api {get} /overall_condition/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup overall_condition
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/overall_condition/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /overall_condition/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup overall_condition
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/overall_condition/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(25)}    name
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /overall_condition/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup overall_condition
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/overall_condition/

@apiParam   {String(25)}    name
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /overall_condition/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup overall_condition
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
         http://localhost:8001/api/v1.0/overall_condition/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /overall_condition/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup overall_condition
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/overall_condition/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# paint_types
"""
@api {get} /paint_types/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup paint_types
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/paint_types/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /paint_types/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup paint_types
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/paint_types/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(25)}    name
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /paint_types/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup paint_types
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/paint_types/

@apiParam   {String(25)}    name
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /paint_types/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup paint_types
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
         http://localhost:8001/api/v1.0/paint_types/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /paint_types/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup paint_types
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/paint_types/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# tap_counter_status
"""
@api {get} /tap_counter_status/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup tap_counter_status
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/tap_counter_status/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /tap_counter_status/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup tap_counter_status
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/tap_counter_status/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(25)}    name
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /tap_counter_status/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup tap_counter_status
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/tap_counter_status/

@apiParam   {String(25)}    name
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /tap_counter_status/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup tap_counter_status
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
         http://localhost:8001/api/v1.0/tap_counter_status/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /tap_counter_status/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup tap_counter_status
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/tap_counter_status/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# tap_filter_condition
"""
@api {get} /tap_filter_condition/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup tap_filter_condition
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/tap_filter_condition/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /tap_filter_condition/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup tap_filter_condition
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/tap_filter_condition/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(25)}    name
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /tap_filter_condition/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup tap_filter_condition
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/tap_filter_condition/

@apiParam   {String(25)}    name
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /tap_filter_condition/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup tap_filter_condition
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
         http://localhost:8001/api/v1.0/tap_filter_condition/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /tap_filter_condition/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup tap_filter_condition
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/tap_filter_condition/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# fan_condition
"""
@api {get} /fan_condition/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup fan_condition
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/fan_condition/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /fan_condition/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup fan_condition
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/fan_condition/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(25)}    name
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /fan_condition/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup fan_condition
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/fan_condition/

@apiParam   {String(25)}    name
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /fan_condition/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup fan_condition
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
         http://localhost:8001/api/v1.0/fan_condition/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /fan_condition/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup fan_condition
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/fan_condition/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# connection_condition
"""
@api {get} /connection_condition/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup connection_condition
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/connection_condition/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /connection_condition/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup connection_condition
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/connection_condition/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(25)}    name
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /connection_condition/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup connection_condition
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/connection_condition/

@apiParam   {String(25)}    name
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /connection_condition/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup connection_condition
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
         http://localhost:8001/api/v1.0/connection_condition/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /connection_condition/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup connection_condition
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/connection_condition/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# foundation_condition
"""
@api {get} /foundation_condition/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup foundation_condition
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/foundation_condition/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /foundation_condition/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup foundation_condition
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/foundation_condition/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(25)}    name
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /foundation_condition/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup foundation_condition
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/foundation_condition/

@apiParam   {String(25)}    name
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /foundation_condition/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup foundation_condition
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
         http://localhost:8001/api/v1.0/foundation_condition/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /foundation_condition/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup foundation_condition
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/foundation_condition/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# heating_condition
"""
@api {get} /heating_condition/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup heating_condition
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/heating_condition/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /heating_condition/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup heating_condition
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/heating_condition/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(25)}    name
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /heating_condition/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup heating_condition
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/heating_condition/

@apiParam   {String(25)}    name
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /heating_condition/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup heating_condition
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
         http://localhost:8001/api/v1.0/heating_condition/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /heating_condition/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup heating_condition
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/heating_condition/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# test_sampling_card
"""
@api {get} /test_sampling_card/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup test_sampling_card
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/test_sampling_card/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /test_sampling_card/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup test_sampling_card
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/test_sampling_card/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "test_result_id": 1,
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {Integer}       test_result_id
@apiSuccess {Integer}       date_created
@apiSuccess {Integer}       printed
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /test_sampling_card/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup test_sampling_card
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"test_result_id":1}' \
         http://localhost:8001/api/v1.0/test_sampling_card/

@apiParam   {Integer}       test_result_id
@apiParam   {Integer}       date_created
@apiParam   {Integer}       printed
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /test_sampling_card/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup test_sampling_card
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"test_result_id":1}'\
         http://localhost:8001/api/v1.0/test_sampling_card/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /test_sampling_card/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup test_sampling_card
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/test_sampling_card/3

@apiUse DelItemSuccess
@apiUse Error404
"""

# country
"""
@api {get} /country/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup country
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/country/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /country/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup country
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/country/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "Afghanistan",
            "iso_name": "AF",
        }
    }

@apiSuccess {Integer}   id
@apiSuccess {String}    name
@apiSuccess {String}    iso_name
@apiUse GetItemSuccess
@apiUse Error404
"""


# schedule
"""
@apiIgnore
@api {get} /schedule/ Get a list of items. Return all items if user is admin,
                      otherwise return the ones which belong to the user
@apiVersion 1.0.0
@apiName read_tasks_handler
@apiGroup schedule
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/schedule/

@apiUse GetItemsSuccess # TODO
@apiUse Error404
"""
"""
@apiIgnore
@api {get} /schedule/:id Get an item by id. Return any item if user is admin,
                         otherwise return the item only if it belongs to the user
@apiVersion 1.0.0
@apiName read_task_handler
@apiGroup schedule
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/schedule/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id":
            "parent_id": 1,
            ...
        }
    }

@apiSuccess {Integer}    id
@apiSuccess {Datetime}   date_start
@apiSuccess {Integer}    period_years
@apiSuccess {Integer}    period_months
@apiSuccess {Integer}    period_days
@apiSuccess {Integer}    assigned_to_id
@apiSuccess {Dict}       assigned_to                see: user->get an item
@apiSuccess {Boolean}    recurring
@apiSuccess {Integer}    notify_before_in_days
@apiSuccess {String}     description
@apiSuccess {Integer}    test_recommendation_id
@apiSuccess {Dict}       test_recommendation        see: test_recommendation->get an item
@apiSuccess {Integer}    priority
@apiSuccess {Integer}    order
@apiSuccess {Datetime}   date_updated
@apiSuccess {Datetime}   date_created
@apiSuccess {Integer}    status_id
@apiSuccess {Dict}       status                     see: task_status->get an item
@apiSuccess {Integer}    parent_id
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /schedule/ Add a new item. Allow any user to create a new item.
                       Send email notifications to the user who created the
                       new task and to the user who is assigned to the task
@apiVersion 1.0.0
@apiName create_task_handler
@apiGroup schedule
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" \
         -X POST -d '{"test_recommendation_id":2, "start_date":"2016-07-29 17:52:19", "assigned_to_id":3, "priority":5}' \
         http://localhost:8001/api/v1.0/schedule/

@apiParam {Integer}    id
@apiParam {Datetime}   date_start                       required        format "2016-07-29 17:52:19"
@apiParam {Integer}    period_years
@apiParam {Integer}    period_months
@apiParam {Integer}    period_days
@apiParam {Integer}    assigned_to_id                   required
@apiParam {Boolean}    recurring
@apiParam {Integer}    notify_before_in_days
@apiParam {String}     description
@apiParam {Integer}    test_recommendation_id           required
@apiParam {Integer}    priority                         required
@apiParam {Integer}    order
@apiParam {Datetime}   date_updated                                     format "2016-07-29 17:52:19"
@apiParam {Datetime}   date_created                                     format "2016-07-29 17:52:19"
@apiParam {Integer}    status_id
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@apiIgnore
@api {put}/{post} /schedule/:id Update an item. Allow to update any item if user is admin,
                                or only if the item belongs to the user.
                                Send email notifications to the user who updated the task,
                                the user who has been previously assigned to the task and
                                the user who is assigned to the task after update
@apiVersion 1.0.0
@apiName update_task_handler
@apiGroup schedule
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"test_recommendation_id": 3}'\
    http://localhost:8001/api/v1.0/schedule/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@apiIgnore
@api {delete} /schedule/:id Delete an item. Allow to delete any item if user is admin,
                            or only if the item belongs to the user
@apiVersion 1.0.0
@apiName delete_task_handler
@apiGroup schedule
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/schedule/3

@apiUse DelItemSuccess
@apiUse Error404
"""


# diagnosis
"""
@api {get} /diagnosis/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup diagnosis
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/diagnosis/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /diagnosis/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup diagnosis
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/diagnosis/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "some name",
            ...
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(50)}    name
@apiSuccess {String(50)}    code
@apiSuccess {String}        description
@apiSuccess {Integer}       test_type_id
@apiSuccess {Dict}          test_type       see: test_type->get an item
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /diagnosis/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup diagnosis
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"some name"}' \
         http://localhost:8001/api/v1.0/diagnosis/

@apiParam   {String(50)}    name
@apiParam   {String(50)}    code
@apiParam   {String}        description
@apiParam   {Integer}       test_type_id
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /diagnosis/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup diagnosis
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "some other name"}'\
    http://localhost:8001/api/v1.0/diagnosis/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /diagnosis/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup diagnosis
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/diagnosis/3

@apiUse DelItemSuccess
@apiUse Error404
"""

# Test diagnosis
"""
@api {get} /test_diagnosis/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup test_diagnosis
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/test_diagnosis/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /test_diagnosis/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup test_diagnosis
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/test_diagnosis/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "diagnosis_id": 1,
            ...
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {Integer}       diagnosis_id
@apiSuccess {Dict}          diagnosis           see: diagnosis->get an item
@apiSuccess {String}        diagnosis_notes
@apiSuccess {Integer}       user_id
@apiSuccess {Dict}          user                see: user->get an item
@apiSuccess {String}        date_created
@apiSuccess {String}        date_updated
@apiSuccess {Integer}       test_type_id
@apiSuccess {Dict}          test_type           see: test_type->get an item
@apiSuccess {Integer}       test_result_id
@apiSuccess {Dict}          test_result         see: test_result->get an item
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /test_diagnosis/ Add a new item
@apiVersion 1.0.0
@apiName create_test_diagnosis_handler
@apiGroup test_diagnosis
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"diagnosis_id":1}' \
         http://localhost:8001/api/v1.0/test_diagnosis/

@apiParam {Integer}       diagnosis_id
@apiParam {String}        diagnosis_notes
@apiParam {Integer}       user_id
@apiParam {String}        date_created      format "2016-07-29 17:52:19"
@apiParam {String}        date_updated      format "2016-07-29 17:52:19"
@apiParam {Integer}       test_type_id
@apiParam {Integer}       test_result_id
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /test_diagnosis/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup test_diagnosis
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"diagnosis_id":2}'\
    http://localhost:8001/api/v1.0/test_diagnosis/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /test_diagnosis/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup test_diagnosis
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/test_diagnosis/3

@apiUse DelItemSuccess
@apiUse Error404
"""

# Test repair note
"""
@api {get} /test_repair_note/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup test_repair_note
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/test_repair_note/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /test_repair_note/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup test_repair_note
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/test_repair_note/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "description": "description",
            ...
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String}        description
@apiSuccess {String}        remark
@apiSuccess {String}        sample
@apiSuccess {Integer}       user_id
@apiSuccess {Dict}          user                see: user->get an item
@apiSuccess {String}        date_created
@apiSuccess {Integer}       test_result_id
@apiSuccess {Dict}          test_result         see: test_result->get an item
@apiSuccess {Integer}       test_type_id
@apiSuccess {Dict}          test_type           see: test_type->get an item
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /test_repair_note/ Add a new item
@apiVersion 1.0.0
@apiName create_test_repair_note_handler
@apiGroup test_repair_note
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"test_result_id":1, "test_type_id": 1}' \
         http://localhost:8001/api/v1.0/test_repair_note/

@apiParam {Integer}       id
@apiParam {String}        description
@apiParam {String}        remark
@apiParam {String}        sample
@apiParam {Integer}       user_id
@apiParam {String}        date_created        format "2016-07-29 17:52:19"
@apiParam {Integer}       test_result_id
@apiParam {Integer}       test_type_id
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /test_repair_note/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup test_repair_note
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"description": "description updated"}'\
    http://localhost:8001/api/v1.0/test_repair_note/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /test_repair_note/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup test_repair_note
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/test_repair_note/3

@apiUse DelItemSuccess
@apiUse Error404
"""

# Task status
"""
@api {get} /task_status/ Get a list of items
@apiVersion 1.0.0
@apiName get_items
@apiGroup task_status
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/task_status/

@apiUse GetItemsSuccess
@apiUse Error404
"""
"""
@api {get} /task_status/:id Get an item by id
@apiVersion 1.0.0
@apiName get_item
@apiGroup task_status
@apiExample {curl} Example usage:
      curl -i http://localhost:8001/api/v1.0/task_status/1

@apiSuccessExample Success-Response:
    HTTP/1.0 200 OK
    Content-Type: application/json
    {
        "result": {
            "id": 1,
            "name": "New"
        }
    }

@apiSuccess {Integer}       id
@apiSuccess {String(20)}    name
@apiUse GetItemSuccess
@apiUse Error404
"""
"""
@api {post} /task_status/ Add a new item
@apiVersion 1.0.0
@apiName add_item
@apiGroup task_status
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X POST -d '{"name": "Ready for deploy"}' \
         http://localhost:8001/api/v1.0/task_status/

@apiParam {Integer}       id
@apiParam {String(50)}    name
@apiUse PostItemSuccess
@apiUse Error400
"""
"""
@api {put} /task_status/:id Update an item
@apiVersion 1.0.0
@apiName update_item
@apiGroup task_status
@apiExample {curl} Example usage:
    curl -i -H "Content-Type: application/json" -X PUT -d '{"name": "Ready for testing"}'\
    http://localhost:8001/api/v1.0/task_status/1

@apiUse PutItemSuccess
@apiUse Error400
"""
"""
@api {delete} /task_status/:id Delete an item
@apiVersion 1.0.0
@apiName delete_item
@apiGroup task_status
@apiExample {curl} Example usage:
    curl -X DELETE http://localhost:8001/api/v1.0/task_status/3

@apiUse DelItemSuccess
@apiUse Error404
"""
