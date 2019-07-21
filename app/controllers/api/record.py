from flask_restful import Resource, reqparse
from app.helpers.rest import response
from app.models import model
from app.libs import utils
from app.libs import validation


class GetRecordData(Resource):
    def get(self):
        results = list()
        try:
            data_record = model.read_all("record")
        except Exception as e:
            return response(401, message=str(e))
        
        for i in data_record:
            zone_data = model.read_by_id("zone", str(i['zone']))
            ttl_data = model.read_by_id("ttl", str(i['ttl']))
            type_data = model.read_by_id("type", str(i['type']))
            
            data = {
                "key": i['key'],
                "value": i['value'],
                "created_at": i['created_at'],
                "zone": zone_data,
                "type": type_data,
                "ttl": ttl_data,
            }
            results.append(data)
        return response(200, data=results)


class GetRecordDataId(Resource):
    def get(self, key):
        try:
            data_record = model.read_by_id("record", key)
        except Exception as e:
            return response(401, message=str(e))
        else:
            zone_data = model.read_by_id("zone", str(data_record['zone']))
            ttl_data = model.read_by_id("ttl", str(data_record['ttl']))
            type_data = model.read_by_id("type", str(data_record['type']))
            data = {
                "key": data_record['key'],
                "value": data_record['value'],
                "created_at": data_record['created_at'],
                "zone": zone_data,
                "ttl": ttl_data,
                "type": type_data
            }
            return response(200, data=data)


class RecordAdd(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('record', type=str, required=True)
        parser.add_argument('serial', type=bool, required=True)
        parser.add_argument('zone', type=str, required=True)
        parser.add_argument('ttl', type=str, required=True)
        parser.add_argument('type', type=str, required=True)
        args = parser.parse_args()
        record = args["record"]
        record = record.lower()
        zone = args["zone"]
        types = args["type"]
        ttl = args["ttl"]
        serial = args['serial']

        key = utils.get_last_key("record")

        # validation
        if validation.record_validation(record):
            return response(401, message="Named Error")
        if validation.count_character(record):
            return response(401, message="Count Character Error")
        # end validation

        data = {
            "key": key,
            "value": record,
            "zone": zone,
            "serial": serial,
            "type": types,
            "ttl": ttl,
            "created_at": utils.get_datetime(),
            
        }
        try:
            model.insert_data("record", key, data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Inserted")


class RecordEdit(Resource):
    def put(self, key):
        parser = reqparse.RequestParser()
        parser.add_argument('record', type=str, required=True)
        parser.add_argument('serial', type=bool, required=True)
        parser.add_argument('zone', type=str, required=True)
        parser.add_argument('ttl', type=str, required=True)
        parser.add_argument('type', type=str, required=True)
        args = parser.parse_args()
        record = args["record"]
        record = record.lower()
        zone = args["zone"]
        types = args["type"]
        ttl = args["ttl"]
        serial = args['serial']

        # validation
        if validation.record_validation(record):
            return response(401, message="Named Error")
        if validation.count_character(record):
            return response(401, message="Count Character Error")
        # end validation

        data = {
            "key": key,
            "value": record,
            "zone": zone,
            "serial": serial,
            "type": types,
            "ttl": ttl,
            "created_at": utils.get_datetime(),
            
        }
        try:
            model.update("record", key, data)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Edited")
        

class RecordDelete(Resource):
    def delete(self, key):
        try:
            data = model.delete("record", key)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=data, message="Deleted")