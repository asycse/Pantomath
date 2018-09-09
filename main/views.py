from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .utils import get_student_data
import json, os
from rest_framework.decorators import api_view
from bs4 import BeautifulSoup

PATH = os.path.dirname(os.path.abspath(__file__))

# Create your views here.
def index(request):
    response = JsonResponse({'message': 'Pantomath welcomes you!'})
    return response

def save_student_data(request):
    get_student_data()
    path = os.getcwd()+"/main/student.json"
    # with open(path, 'rb') as file:
        # file = json.load(file)
    
    # print(path)
    return JsonResponse({'message' : 'data saved successfully'}) 

def username_to_entrynum(u):
    return "20" + u[3:5] + u[:3].upper() + u[5:]

@api_view(['GET'])
def registered_courses(request):
    username = request.GET.get('username', None)
    # print()
    default = {
                'status_code' : '404', 
                'error' : True , 
                'message' : 'username is required',
                'data' : { }
               }

    if username is None:
        return JsonResponse({
                              'status_code' : '404', 
                              'error' : True , 
                              'message' : 'username is required',
                              'data' : { }
                            })
    else:
        file = open(PATH+"/student.json", 'rb')
        data = json.load(file)
        entrynum = username_to_entrynum(username)
        userdata = data.get(entrynum, None)
        if userdata is None:
            default["message"] = "username not present in database"
            return JsonResponse(default)

        default["data"] = userdata
        default["message"] = ":)"
        default["status_code"] = 200
        default["error"] = False

        return JsonResponse(default)
         



@api_view(['GET'])
def getAllDepartmentRecords(request):
    listOfUrls=[
        "http://ldap1.iitd.ernet.in/LDAP/chemical/ch114.shtml"
    ]
    code2dept = {
        "ce":"civil",
        "ch":"chemical",
        "cs":"cse",
        "bb":"dbeb",
        "ee":"ee",
        "mt":"maths",
        "me":"mech",
        "ph":"physics",
        "tt":"textile"
    }
    totalDic=[]
    Dept = ""
    ind=0

    for url in listOfUrls:
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, "html.parser")

        table_body = soup.find('table')

        rows = table_body.find_all('tr')
        print(url)
            
        for row in rows:
            cols = row.find_all('td')
            if(len(cols) > 1):
                cols = [ele.text.strip() for ele in cols]
                cols.append(Dept)
                totalDic.append([ele for ele in cols if ele]) # Get rid of empty values
                totalDic[ind][0] = kerberos_to_entry_number(totalDic[ind][0])
                ind = ind+1
            else:
                cols = [ele.text.strip() for ele in cols]
                Dept = code2dept[str(cols[0][0:2])]
    print(totalDic)
    return 4

@api_view(['GET'])
def getDepartmentStudentRecords(request):
    # print ('hey')
    # print (request.name)
    response = JsonResponse({'foo': 'bar'})
    return response
