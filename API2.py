from encodings import utf_8
from flask import Flask,jsonify, request,make_response
from flask_restful import Resource, Api, reqparse
import requests
import pyodbc
import jwt
import datetime
from functools import wraps
#connecting to database
conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=10.150.72.22;'
                      'Database=ARMS;'
                      'UID=Nishant.kumar2;'
                      'PWD=$p!Ce@NSK$dbpjq;'
                      'Trusted_Connection=No;'
                    )


#application.config['SQLALCHEMY_DATABSE_URI']='sqlite:////D/VS Code python/TokenTesting/user.db'



application = Flask(__name__)
api = Api(application)

application.config['SECRET_KEY']='thisissecretkey'

token=None


# Getting the whole data of
def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        
        if 'access-token' in request.headers:
            token=request.headers['access-token']
        if not token:
            return jsonify({'message':'Token is missing'}),401
        try:
            token=request.headers['access-token']
        except:
            return jsonify({'message':'Token is invalid'}),401
        
        return f(token,*args,**kwargs)
    return decorated


# Getting the whole data of
@application.route('/Employee',methods=['GET'])
@token_required
def all_data(token):
    if token!=tokenencode:
        return jsonify({'Token Error':'Token is Mismatched/ Token is not copied correctly'}),401
    cursor = conn.cursor()
    data=cursor.execute("select TRY_CAST(EmployeeID as Varchar) as EmployeeID,TRY_CAST(StaffID as Varchar) as StaffID,CAST(EmployeeName as Varchar) as EmpName,CAST(EmployeeCategory as Varchar) as EmployeeCategory,CAST(EmployeeStatus as Varchar) as EmployeeStatus,CAST(ResignedDate as Varchar) as ResignedDate,TRY_CAST(RepositoryShortName as Varchar) as Rank from com.Employee e left join com.REPOSITORY r on CAST(e.RankID as varchar)=cast(r.RepositoryID as varchar)")
    newlist=[]
    for i in data:
        newdict={"EmployeeID":i[0],"StaffID":i[1],"EmployeeName":i[2],"EmployeeCategory":i[3],"EmployeeStatus":i[4],"ResignedDate":i[5],"Rank":i[6]}
        newlist.append(newdict)
    return jsonify(newlist)


#Not in Use
@application.route('/Employee/',methods=['GET'])
@token_required
def id_data(token):
    if token!=tokenencode:
            return jsonify({'Token Error':'Token is Mismatched/ Token is not copied correctly'})
    Id=request.args.get('Id')
        #parser.add_argument('Name', required=True)
        #parser.add_argument('userId', required=True)  # add args
        #NAME=args['Name']
    cursor = conn.cursor()
    data=cursor.execute("select TRY_CAST(EmployeeID as Varchar) as EmployeeID,TRY_CAST(StaffID as Varchar) as StaffID,CAST(EmployeeName as Varchar) as EmpName,CAST(EmployeeCategory as Varchar) as EmployeeCategory,CAST(EmployeeStatus as Varchar) as EmployeeStatus,CAST(ResignedDate as Varchar) as ResignedDate,TRY_CAST(RepositoryShortName as Varchar) as Rank from com.Employee e left join com.REPOSITORY r on CAST(e.RankID as varchar)=cast(r.RepositoryID as varchar) where e.EmployeeId=?",Id)
    newlist=[]
    for i in data:
        newdict={"EmployeeID":i[0],"StaffID":i[1],"EmployeeName":i[2],"EmployeeCategory":i[3],"EmployeeStatus":i[4],"ResignedDate":i[5],"Rank":i[6]}
        newlist.append(newdict)
    return jsonify(newlist)


@application.route('/token')
def login():
    global tokenencode
    auth=request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Please give valid username and passwords',401,{'WWW-Authenticate':'Basic realm="Login Required!"'})

    if auth.username=='Nishant':
        if auth.password=='Spice':
            tokenencode=jwt.encode({'username':auth.username, 'exp':datetime.datetime.utcnow()+datetime.timedelta(hours=24)},application.config['SECRET_KEY'])
            
            return jsonify({'token':tokenencode})

    return make_response('Could not verify the username or  password',401,{'WWW-Authenticate':'Basic realm="Login Required!"'})

    
#calling the main and runnning the whole code 
if __name__ == '__main__':
    application.run(debug=True)  # run our Flask app