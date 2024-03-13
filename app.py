from flask import Flask,render_template,request
import joblib
import numpy as np

model = joblib.load('Rmodel.joblib')
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])

def predict_Co2():
    # Get fuel type values
    EngineSizeL = float(request.form.get('Engine Size(L)'))
    Cylinders = int(request.form.get('Cylinders'))
    FuelConsumptionComb = float(request.form.get('Fuel Consumption Comb (L/100 km)'))

    selected_fuel_type = request.form.get('Fuel_Type')

    # Initialize all fuel types to zero
    Fuel_Type_E = 0
    Fuel_Type_X = 0
    Fuel_Type_Z = 0

    # Set the selected fuel type to 1, others remain 0
    if selected_fuel_type == 'E':
        Fuel_Type_E = 1
    elif selected_fuel_type == 'X':
        Fuel_Type_X = 1
    elif selected_fuel_type == 'Z':
        Fuel_Type_Z = 1
    else:
        # Handle the case when an unexpected value is received
    # You may want to add additional error handling or default behavior here
        pass
    


    # if Fuel_Type_D == 1:
        #If Diesel is selected, set other fuel type values to 0
        # Fuel_Type_E = 0
        # Fuel_Type_X = 0
        # Fuel_Type_Z = 0
    # else:
        # pass
           
# prediction
    result = model.predict(np.array([EngineSizeL,Cylinders,FuelConsumptionComb,
                                     Fuel_Type_E,Fuel_Type_X,Fuel_Type_Z]).reshape(1,6))
    

    formatted_result = f"Emitted CO2: {result[0]:.2f} g/km"  # Assuming result[0] is the emitted CO2 value

    return render_template('index.html', result=formatted_result)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)

