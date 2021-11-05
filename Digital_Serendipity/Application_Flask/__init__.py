from flask import *
import Application_Flask.templates.community as community
import Application_Flask.templates.Building_Calculation as building
import Application_Flask.templates.Finding_User as user
import pandas as pd
import csv

#Flask Starting
app = Flask(__name__)
app.debug = True

#First screen
@app.route('/')
def student():
    return render_template('index.html')

@app.route('/phase1',methods = ['POST', 'GET'])
def user_decision():
    result = []
    #Getting variables related to users
    if request.method == "POST":
        Name = request.form['Name']
        S_Building = request.form['S_Building']
        Building = request.form['Building']
        Time = request.form['Time']
        user_list = [Name, S_Building, Building,Time]
 
        if request.form.get('service_need'):       
            #add user list
            f = open('user_list.csv','a', newline='',encoding='utf-8-sig')
            wr = csv.writer(f)
            wr.writerow(user_list)
            #select service contents
            result = community.group_select(Name,Building)

            return render_template('result1.html',result=result)
  
        else:
            #add list of service provider
            f = open('user_list_provider.csv','a', newline='',encoding='utf-8-sig')
            wr = csv.writer(f)
            wr.writerow(user_list)
            #save User_building_list
            building_list = user.Building_list_maker(S_Building,Building)
            building.Building_List_Appender(Name,Time,building_list)

            return render_template('provider_result.html')
            
@app.route('/phase2',methods = ['POST', 'GET'])
def user_finding():
    if request.method == "POST":

        #Getting new user
        new_data = user.New_User_Invitation()
        name = new_data[0]
        start = new_data[1]
        end = new_data[2]
        time = new_data[3]

        #Building_list calculation
        building_list = user.Building_list_maker(start,end)

        #same building sorting
        user.Building_List_Comparison(building_list)

        #fina list with checking time
        result_user = user.Time_Comparison(time)
        user_result_sentence = "Your good friend is" + str(result_user)

        return render_template('result2.html', result3=result_user,
                               score3=user_result_sentence)

@app.route('/phase3',methods = ['POST', 'GET'])
def complete():                           
    
    return "<h1>연결 완료 되었습니다!</h1>"

if __name__ == '__main__':
       app.run(debug = True)   