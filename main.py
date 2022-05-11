#import Print as Print
from flask import Flask, Response, request
import pymongo
import json
from bson.objectid import ObjectId
app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(host = 'localhost',port =27017,serverSelectionTimeoutMS = 1000)
    db = mongo.company
    mongo.server_info() #trigger exception if cannot connect to db

except:
    print("ERROR: Could not connect to database")
##################################################DELETE
@app.route("/users/<id>", methods=["DELETE"])
def delete(id):
    try:
        dbResponse = db.users.delete_one({"_id":ObjectId(id)})
        if dbResponse.deleted_count == 1:

        #for attr in dir(dbResponse):
         #   print(f"***{attr}***")
            return Response(
                response=json.dumps({"message": "User Successfully Deleted","id":f"{id}"}),
                status=200,
                mimetype="application/json"

                )
        else:
            return Response(
                response=json.dumps({"message": "User Not found","id":f"{id}"}),
                status=200,
                mimetype="application/json"

                )



    except Exception as  ex:
        print("******")
        print(ex)
        print("******")
        return Response(
            response=json.dumps({"message": "Sorry Can Not Delete User"}),
            status=500,
            mimetype="application/json"

            )


##################################################Update
@app.route("/users/<id>", methods =["PATCH"])
def update_user(id):
    try:
        dbResponse = db.users.update_one(
            {"_id": ObjectId(id)},
            {"$set":{"name": request.form["name"]}}
        )
        #for attr in dir(dbResponse):
            #print(f"*****{attr}*****")
        if dbResponse.modified_count == 1:
            return Response(
                response=json.dumps({"message": "User Updated"}),
                status=200,
                mimetype="application/json"

                )
        else:
            return Response(
                response=json.dumps({"message": "Nothing to Updated"}),
                status=200,
                mimetype="application/json"

                )

    except Exception as  ex:
        print("*********")
        print(ex)
        print("********")
        return Response(
            response=json.dumps({"message": "Sorry Can Not Update User"}),
            status=500,
            mimetype="application/json"

        )



#################################################READ
@app.route("/users", methods=["GET"])
def get_some_users():
    try:
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])
        return Response(
            response=json.dumps(data),
            status=500,
            mimetype="application/json"

        )


    except Exception as  ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "Can not read Users"}),
            status=500,
            mimetype="application/json"

        )

#############################################CREATE
@app.route("/users", methods=["POST"])
def create_user():
    try:
        user = {"name":request.form["name"], "lastName":request.form["lastName"]}
        dbResponse = db.users.insert_one(user)
        print(dbResponse.inserted_id)
        #for attr in dir(dbResponse):
           # print(attr)
        return Response(
            response = json.dumps({"message":"User Created", "id":f"{dbResponse.inserted_id}"}),
            status=200,
            mimetype="application/json"

        )
    except Exception as ex:
        print("********")
        print(ex)
        print("********")
############################
if __name__ == "__main__":
    app.run(port=80, debug=True)
