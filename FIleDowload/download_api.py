from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import requests
import random
from timecalculation import file_size, download_time
import pyspeedtest
from dbconnection import get_database
from bson.json_util import dumps
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(__name__)
api = Api(app)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)


class DownloadFile(Resource):

    @limiter.limit("200 per day")  # API limits
    def post(self):
        try:
            if request.args.get('url'):
                total_length = int(requests.head(request.args.get('url'), stream=True).headers.get('content-length'))
                size,name=file_size(total_length)
                st = pyspeedtest.SpeedTest()
                #bandwith_size,type=file_size(st.download())
                estimated=download_time(size,name,1,'MB')  # 1 MB will be the bandwidth of network.
                id = random.randrange(10000, 50000, 5)
                file_name=request.args.get('url').split('/')[-1]
                collection = get_database()
                collection.insert_one(
                    {'_id': id,
                     'Total_file_size': str(size)+' '+name,
                     'Estimated_time_to_complete': estimated,
                     'Status': 'Downloading',
                     'FilE_name': file_name
                     }
                )
                my_file = requests.get(request.args.get('url'), stream=True)
                open('/home/shravan/Downloads/'+file_name, 'wb').write(my_file.content)  # Put download path
                collection = get_database()
                my_query = {"_id": id}
                new_values = {"$set": {"Status": 'Completed'}}
                collection.update_one(my_query,new_values)
                return id
            else:
                return "No URL found."
        except Exception as message:
                return message


class GetStatus(Resource):
    @limiter.limit("200 per day")
    def get(self):
        id = request.args.get('id')
        collection = get_database()
        return jsonify(dumps(collection.find_one(({"_id": int(id)}))))


api.add_resource(DownloadFile, '/download')
api.add_resource(GetStatus, '/status')

if __name__=='__main__':
    app.run(debug=True, threaded=True)  # multi threaded


