from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
import datetime
import openpyxl

import pandas as pd

import matplotlib.pyplot as plt


from sklearn.ensemble import VotingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score

# Create your views here.
from Remote_User.models import ClientRegister_Model,energy_demand_prediction,detection_ratio,detection_accuracy

def login(request):


    if request.method == "POST" and 'submit1' in request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            enter = ClientRegister_Model.objects.get(username=username,password=password)
            request.session["userid"] = enter.id

            return redirect('ViewYourProfile')
        except:
            pass

    return render(request,'RUser/login.html')

def Register1(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneno = request.POST.get('phoneno')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        ClientRegister_Model.objects.create(username=username, email=email, password=password, phoneno=phoneno,
                                            country=country, state=state, city=city, address=address, gender=gender)
        obj = "Registered Successfully"
        return render(request, 'RUser/Register1.html', {'object': obj})
    else:
        return render(request,'RUser/Register1.html')

def ViewYourProfile(request):
    userid = request.session['userid']
    obj = ClientRegister_Model.objects.get(id= userid)
    return render(request,'RUser/ViewYourProfile.html',{'object':obj})


def predict_energy_demand_prediction_type(request):
    if request.method == "POST":

        Fid= request.POST.get('Fid')
        Station_Name= request.POST.get('Station_Name')
        Start_Date= request.POST.get('Start_Date')
        End_Date= request.POST.get('End_Date')
        Total_Duration_hh_mm_ss= request.POST.get('Total_Duration_hh_mm_ss')
        Charging_Time_hh_mm_ss= request.POST.get('Charging_Time_hh_mm_ss')
        Energy_kWh= request.POST.get('Energy_kWh')
        Port_Number= request.POST.get('Port_Number')
        Plug_Type= request.POST.get('Plug_Type')
        Address1= request.POST.get('Address1')
        City= request.POST.get('City')
        State_Province= request.POST.get('State_Province')
        Country= request.POST.get('Country')
        Latitude= request.POST.get('Latitude')
        Longitude= request.POST.get('Longitude')
        Fee_USD= request.POST.get('Fee_USD')
        Ended_By= request.POST.get('Ended_By')
        Make= request.POST.get('Make')
        Model= request.POST.get('Model')
        Vehicle_Type= request.POST.get('Vehicle_Type')


        df = pd.read_csv('Datasets.csv', encoding='latin-1')
        df
        df.columns

        def apply_results(results):
            if (results == 0):
                return 0
            elif (results == 1):
                return 1

        df['Results'] = df['Label'].apply(apply_results)

        X = df['Fid'].apply(str)
        y = df['Results']

        X.shape, y.shape

        print("FID")
        print(X)
        print("Label")
        print(y)


        cv = CountVectorizer()
        X = cv.fit_transform(X)

        models = []
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
        X_train.shape, X_test.shape, y_train.shape

        print("KNeighborsClassifier")
        from sklearn.neighbors import KNeighborsClassifier
        kn = KNeighborsClassifier()
        kn.fit(X_train, y_train)
        knpredict = kn.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, knpredict) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, knpredict))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, knpredict))
        models.append(('KNeighborsClassifier', kn))


        print("Decision Tree Classifier")
        dtc = DecisionTreeClassifier()
        dtc.fit(X_train, y_train)
        dtcpredict = dtc.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, dtcpredict) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, dtcpredict))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, dtcpredict))
        models.append(('DecisionTreeClassifier', dtc))

        # SVM Model
        print("SVM")
        from sklearn import svm
        lin_clf = svm.LinearSVC()
        lin_clf.fit(X_train, y_train)
        predict_svm = lin_clf.predict(X_test)
        svm_acc = accuracy_score(y_test, predict_svm) * 100
        print(svm_acc)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, predict_svm))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, predict_svm))
        models.append(('svm', lin_clf))

        # Enable below 2 Models if u want

        """print("Artificial Neural Network (ANN)")

        from sklearn.neural_network import MLPClassifier
        mlpc = MLPClassifier().fit(X_train, y_train)
        y_pred = mlpc.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, y_pred) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, y_pred))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, y_pred))
        models.append(('MLPClassifier', mlpc))"""


        """print("Random Forest Classifier")
        from sklearn.ensemble import RandomForestClassifier
        rf_clf = RandomForestClassifier()
        rf_clf.fit(X_train, y_train)
        rfpredict = rf_clf.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, rfpredict) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, rfpredict))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, rfpredict))
        models.append(('RandomForestClassifier', rf_clf)) """


        classifier = VotingClassifier(models)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)

        Fid1 = [Fid]
        vector1 = cv.transform(Fid1).toarray()
        predict_text = classifier.predict(vector1)

        pred = str(predict_text).replace("[", "")
        pred1 = pred.replace("]", "")

        prediction = int(pred1)

        if prediction == 0:
            val = 'Low'
        elif prediction == 1:
            val = 'High'



        print(val)
        print(pred1)

        energy_demand_prediction.objects.create(
        Fid=Fid,
        Station_Name=Station_Name,
        Start_Date=Start_Date,
        End_Date=End_Date,
        Total_Duration_hh_mm_ss=Total_Duration_hh_mm_ss,
        Charging_Time_hh_mm_ss=Charging_Time_hh_mm_ss,
        Energy_kWh=Energy_kWh,
        Port_Number=Port_Number,
        Plug_Type=Plug_Type,
        Address1=Address1,
        City=City,
        State_Province=State_Province,
        Country=Country,
        Latitude=Latitude,
        Longitude=Longitude,
        Fee_USD=Fee_USD,
        Ended_By=Ended_By,
        Make=Make,
        Model=Model,
        Vehicle_Type=Vehicle_Type,
        Prediction=val)

        return render(request, 'RUser/predict_energy_demand_prediction_type.html',{'objs': val})
    return render(request, 'RUser/predict_energy_demand_prediction_type.html')



