import streamlit as st
import time
import os
# Mark the start time
start_time = time.time()

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
from streamlit_option_menu import option_menu
import pickle
from PIL import Image
import numpy as np
import plotly.figure_factory as ff
import streamlit as st
from code.DiseaseModel import DiseaseModel
from code.helper import  prepare_symptoms_array
import seaborn as sns
import matplotlib.pyplot as plt
import joblib

# loading the models
diabetes_model = joblib.load("models/diabetes_model.sav")
heart_model = joblib.load("models/heart_disease_model.sav")
parkinson_model = joblib.load("models/parkinsons_model.sav")
# Load the lung cancer prediction model
lung_cancer_model = joblib.load('models/lung_cancer_model.sav')

# Load the pre-trained model
breast_cancer_model = joblib.load('models/breast_cancer.sav')

# Load the pre-trained model
chronic_disease_model = joblib.load('models/chronic_model.sav')

# Load the hepatitis prediction model
hepatitis_model = joblib.load('models/hepititisc_model.sav')


liver_model = joblib.load('models/liver_model.sav')# Load the lung cancer prediction model
lung_cancer_model = joblib.load('models/lung_cancer_model.sav')



# sidebar
with st.sidebar:
    selected = option_menu('Dự Đoán Đa Bệnh', [
        'Dự Đoán Bệnh',
        'Dự Đoán Tiểu Đường',
        'Dự Đoán Bệnh Tim',
        'Dự Đoán Parkinson',
        'Dự Đoán Bệnh Gan',
        'Dự Đoán Viêm Gan',
        'Dự Đoán Ung Thư Phổi',
        'Dự Đoán Bệnh Thận Mãn Tính',
        'Dự Đoán Ung Thư Vú',

    ],
        icons=['','activity', 'heart', 'person','person','person','person','bar-chart-fill'],
        default_index=0)




# Đo và hiển thị thời gian khởi động chỉ một lần duy nhất
if 'startup_measured' not in st.session_state:
    end_time = time.time()
    total_duration = end_time - start_time                                                                                                                                     
    st.sidebar.info(f"Thời gian khởi động: {total_duration:.4f} giây")
    st.session_state.startup_measured = True
    
    # Ghi thời gian vào file
    with open("startup_time.txt", "w") as file:
        file.write(str(total_duration))


 


# multiple disease prediction
if selected == 'Dự Đoán Bệnh': 
    # Create disease class and load ML model
    disease_model = DiseaseModel()
    disease_model.load_xgboost('model/xgboost_model.json')

    # Title
    st.write('# Dự Đoán Bệnh Sử Dụng Học Máy')

    symptoms = st.multiselect('Triệu chứng của bạn là gì?', options=disease_model.all_symptoms)

    X = prepare_symptoms_array(symptoms)

    # Trigger XGBoost model
    if st.button('Dự Đoán'): 
        # Run the model with the python script
        
        prediction, prob = disease_model.predict(X)
        st.write(f'## Bệnh: {prediction} với xác suất {prob*100:.2f}%')


        tab1, tab2= st.tabs(["Mô tả", "Biện pháp phòng ngừa"])

        with tab1:
            st.write(disease_model.describe_predicted_disease())

        with tab2:
            precautions = disease_model.predicted_disease_precautions()
            for i in range(4):
                st.write(f'{i+1}. {precautions[i]}')




# Diabetes prediction page
if selected == 'Dự Đoán Tiểu Đường':  # pagetitle
    st.title("Dự Đoán Bệnh Tiểu Đường")
    image = Image.open('d3.jpg')
    st.image(image, caption='Dự đoán bệnh tiểu đường')
    # columns
    # no inputs from the user
    name = st.text_input("Họ và tên:")
    col1, col2, col3 = st.columns(3)

    with col1:
        Pregnancies = st.number_input("Số lần mang thai")
    with col2:
        Glucose = st.number_input("Mức đường huyết")
    with col3:
        BloodPressure = st.number_input("Huyết áp")
    with col1:

        SkinThickness = st.number_input("Độ dày da")

    with col2:

        Insulin = st.number_input("Insulin")
    with col3:
        BMI = st.number_input("Chỉ số BMI")
    with col1:
        DiabetesPedigreefunction = st.number_input(
            "Chỉ số di truyền tiểu đường")
    with col2:

        Age = st.number_input("Tuổi")

    # code for prediction
    diabetes_dig = ''

    # button
    if st.button("Kết quả kiểm tra tiểu đường"):
        diabetes_prediction=[[]]
        diabetes_prediction = diabetes_model.predict(
            [[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreefunction, Age]])

        # after the prediction is done if the value in the list at index is 0 is 1 then the person is diabetic
        if diabetes_prediction[0] == 1:
            diabetes_dig = "Chúng tôi rất tiếc phải thông báo rằng bạn có khả năng mắc bệnh tiểu đường."
            image = Image.open('positive.jpg')
            st.image(image, caption='')
        else:
            diabetes_dig = 'Chúc mừng, bạn không mắc bệnh tiểu đường'
            image = Image.open('negative.jpg')
            st.image(image, caption='')
        st.success(name+' , ' + diabetes_dig)
        
        



# Heart prediction page
if selected == 'Dự Đoán Bệnh Tim':
    st.title("Dự đoán bệnh tim")
    image = Image.open('heart2.jpg')
    st.image(image, caption='Suy tim')
    # age	sex	cp	trestbps	chol	fbs	restecg	thalach	exang	oldpeak	slope	ca	thal	target
    # columns
    # no inputs from the user
    name = st.text_input("Họ và tên:")
    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input("Tuổi")
    with col2:
        sex=0
        display = ("Nam", "Nữ")
        options = list(range(len(display)))
        value = st.selectbox("Giới tính", options, format_func=lambda x: display[x])
        if value == 0:
            sex = 1
        elif value == 1:
            sex = 0
    with col3:
        cp=0
        display = ("Đau thắt ngực điển hình","Đau thắt ngực không điển hình","Đau không phải đau thắt ngực","Không có triệu chứng")
        options = list(range(len(display)))
        value = st.selectbox("Loại đau ngực", options, format_func=lambda x: display[x])
        if value == 0:
            cp = 0
        elif value == 1:
            cp = 1
        elif value == 2:
            cp = 2
        elif value == 3:
            cp = 3
    with col1:
        trestbps = st.number_input("Huyết áp khi nghỉ ngơi")

    with col2:

        chol = st.number_input("Cholesterol huyết thanh")
    
    with col3:
        restecg=0
        display = ("Bình thường","Có bất thường sóng ST-T","Phì đại thất trái")
        options = list(range(len(display)))
        value = st.selectbox("Điện tâm đồ khi nghỉ ngơi", options, format_func=lambda x: display[x])
        if value == 0:
            restecg = 0
        elif value == 1:
            restecg = 1
        elif value == 2:
            restecg = 2

    with col1:
        exang=0
        thalach = st.number_input("Nhịp tim tối đa đạt được")
   
    with col2:
        oldpeak = st.number_input("Chênh lệch ST do tập thể dục")
    with col3:
        slope=0
        display = ("Đi lên","Phẳng","Đi xuống")
        options = list(range(len(display)))
        value = st.selectbox("Độ dốc đoạn ST khi tập", options, format_func=lambda x: display[x])
        if value == 0:
            slope = 0
        elif value == 1:
            slope = 1
        elif value == 2:
            slope = 2
    with col1:
        ca = st.number_input("Số lượng mạch máu chính (0–3) được hiển thị bằng huỳnh quang")
    with col2:
        thal=0
        display = ("Bình thường","Khiếm khuyết cố định","Khiếm khuyết có thể đảo ngược")
        options = list(range(len(display)))
        value = st.selectbox("Thalassemia", options, format_func=lambda x: display[x])
        if value == 0:
            thal = 0
        elif value == 1:
            thal = 1
        elif value == 2:
            thal = 2
    with col3:
        agree = st.checkbox('Đau thắt ngực do tập thể dục')
        if agree:
            exang = 1
        else:
            exang=0
    with col1:
        agree1 = st.checkbox('Đường huyết lúc đói > 120mg/dl')
        if agree1:
            fbs = 1
        else:
            fbs=0
    # code for prediction
    heart_dig = ''
    

    # button
    if st.button("Kết quả kiểm tra tim"):
        heart_prediction=[[]]
        # change the parameters according to the model
        
        # b=np.array(a, dtype=float)
        heart_prediction = heart_model.predict([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])

        if heart_prediction[0] == 1:
            heart_dig = 'Chúng tôi rất tiếc phải thông báo rằng bạn có khả năng mắc bệnh tim.'
            image = Image.open('positive.jpg')
            st.image(image, caption='')
            
        else:
            heart_dig = "Chúc mừng, bạn không mắc bệnh tim."
            image = Image.open('negative.jpg')
            st.image(image, caption='')
        st.success(name +' , ' + heart_dig)









if selected == 'Dự Đoán Parkinson':
    st.title("Dự đoán bệnh Parkinson")
    image = Image.open('p1.jpg')
    st.image(image, caption='Bệnh Parkinson')
  # parameters
#    name	MDVP:Fo(Hz)	MDVP:Fhi(Hz)	MDVP:Flo(Hz)	MDVP:Jitter(%)	MDVP:Jitter(Abs)	MDVP:RAP	MDVP:PPQ	Jitter:DDP	MDVP:Shimmer	MDVP:Shimmer(dB)	Shimmer:APQ3	Shimmer:APQ5	MDVP:APQ	Shimmer:DDA	NHR	HNR	status	RPDE	DFA	spread1	spread2	D2	PPE
   # change the variables according to the dataset used in the model
    name = st.text_input("Họ và tên:")
    col1, col2, col3 = st.columns(3)
    with col1:
        MDVP = st.number_input("MDVP:Fo(Hz)")
    with col2:
        MDVPFIZ = st.number_input("MDVP:Fhi(Hz)")
    with col3:
        MDVPFLO = st.number_input("MDVP:Flo(Hz)")
    with col1:
        MDVPJITTER = st.number_input("MDVP:Jitter(%)")
    with col2:
        MDVPJitterAbs = st.number_input("MDVP:Jitter(Abs)")
    with col3:
        MDVPRAP = st.number_input("MDVP:RAP")

    with col2:

        MDVPPPQ = st.number_input("MDVP:PPQ ")
    with col3:
        JitterDDP = st.number_input("Jitter:DDP")
    with col1:
        MDVPShimmer = st.number_input("MDVP:Shimmer")
    with col2:
        MDVPShimmer_dB = st.number_input("MDVP:Shimmer(dB)")
    with col3:
        Shimmer_APQ3 = st.number_input("Shimmer:APQ3")
    with col1:
        ShimmerAPQ5 = st.number_input("Shimmer:APQ5")
    with col2:
        MDVP_APQ = st.number_input("MDVP:APQ")
    with col3:
        ShimmerDDA = st.number_input("Shimmer:DDA")
    with col1:
        NHR = st.number_input("NHR")
    with col2:
        HNR = st.number_input("HNR")
  
    with col2:
        RPDE = st.number_input("RPDE")
    with col3:
        DFA = st.number_input("DFA")
    with col1:
        spread1 = st.number_input("spread1")
    with col1:
        spread2 = st.number_input("spread2")
    with col3:
        D2 = st.number_input("D2")
    with col1:
        PPE = st.number_input("PPE")

    # code for prediction
    parkinson_dig = ''
    
    # button
    if st.button("Kết quả kiểm tra Parkinson"):
        parkinson_prediction=[[]]
        # change the parameters according to the model
        parkinson_prediction = parkinson_model.predict([[MDVP, MDVPFIZ, MDVPFLO, MDVPJITTER, MDVPJitterAbs, MDVPRAP, MDVPPPQ, JitterDDP, MDVPShimmer,MDVPShimmer_dB, Shimmer_APQ3, ShimmerAPQ5, MDVP_APQ, ShimmerDDA, NHR, HNR,  RPDE, DFA, spread1, spread2, D2, PPE]])

        if parkinson_prediction[0] == 1:
            parkinson_dig = 'Chúng tôi rất tiếc phải thông báo rằng bạn có khả năng mắc bệnh Parkinson'
            image = Image.open('positive.jpg')
            st.image(image, caption='')
        else:
            parkinson_dig = "Chúc mừng, bạn không mắc bệnh Parkinson"
            image = Image.open('negative.jpg')
            st.image(image, caption='')
        st.success(name+' , ' + parkinson_dig)



# Load the dataset
lung_cancer_data = pd.read_csv('data/lung_cancer.csv')

# Convert 'M' to 0 and 'F' to 1 in the 'GENDER' column
lung_cancer_data['GENDER'] = lung_cancer_data['GENDER'].map({'M': 'Nam', 'F': 'Nữ'})

# Lung Cancer prediction page
if selected == 'Dự Đoán Ung Thư Phổi':
    st.title("Dự Đoán Ung Thư Phổi")
    image = Image.open('h.png')
    st.image(image, caption='Dự Đoán Ung Thư Phổi')

    # Columns
    # No inputs from the user
    name = st.text_input("Họ và tên:")
    col1, col2, col3 = st.columns(3)

    with col1:
        gender = st.selectbox("Giới tính:", lung_cancer_data['GENDER'].unique())
    with col2:
        age = st.number_input("Tuổi")
    with col3:
        smoking = st.selectbox("Hút thuốc:", ['KHÔNG', 'CÓ'])
    with col1:
        yellow_fingers = st.selectbox("Ngón tay vàng:", ['KHÔNG', 'CÓ'])

    with col2:
        anxiety = st.selectbox("Lo âu:", ['KHÔNG', 'CÓ'])
    with col3:
        peer_pressure = st.selectbox("Áp lực từ bạn bè:", ['KHÔNG', 'CÓ'])
    with col1:
        chronic_disease = st.selectbox("Bệnh mãn tính:", ['KHÔNG', 'CÓ'])

    with col2:
        fatigue = st.selectbox("Mệt mỏi:", ['KHÔNG', 'CÓ'])
    with col3:
        allergy = st.selectbox("Dị ứng:", ['KHÔNG', 'CÓ'])
    with col1:
        wheezing = st.selectbox("Thở khò khè:", ['KHÔNG', 'CÓ'])

    with col2:
        alcohol_consuming = st.selectbox("Uống rượu:", ['KHÔNG', 'CÓ'])
    with col3:
        coughing = st.selectbox("Ho:", ['KHÔNG', 'CÓ'])
    with col1:
        shortness_of_breath = st.selectbox("Khó thở:", ['KHÔNG', 'CÓ'])

    with col2:
        swallowing_difficulty = st.selectbox("Khó nuốt:", ['KHÔNG', 'CÓ'])
    with col3:
        chest_pain = st.selectbox("Đau ngực:", ['KHÔNG', 'CÓ'])

    # Code for prediction
    cancer_result = ''

    # Button
    if st.button("Dự đoán ung thư phổi"):
        # Create a DataFrame with user inputs
        user_data = pd.DataFrame({
            'GENDER': [gender],
            'AGE': [age],
            'SMOKING': [smoking],
            'YELLOW_FINGERS': [yellow_fingers],
            'ANXIETY': [anxiety],
            'PEER_PRESSURE': [peer_pressure],
            'CHRONICDISEASE': [chronic_disease],
            'FATIGUE': [fatigue],
            'ALLERGY': [allergy],
            'WHEEZING': [wheezing],
            'ALCOHOLCONSUMING': [alcohol_consuming],
            'COUGHING': [coughing],
            'SHORTNESSOFBREATH': [shortness_of_breath],
            'SWALLOWINGDIFFICULTY': [swallowing_difficulty],
            'CHESTPAIN': [chest_pain]
        })

        # Map string values to numeric
        user_data.replace({'KHÔNG': 1, 'CÓ': 2}, inplace=True)

        # Strip leading and trailing whitespaces from column names
        user_data.columns = user_data.columns.str.strip()

        # Convert columns to numeric where necessary
        numeric_columns = ['AGE', 'FATIGUE', 'ALLERGY', 'ALCOHOLCONSUMING', 'COUGHING', 'SHORTNESSOFBREATH']
        user_data[numeric_columns] = user_data[numeric_columns].apply(pd.to_numeric, errors='coerce')

        # Perform prediction
        cancer_prediction = lung_cancer_model.predict(user_data)

        # Display result
        if cancer_prediction[0] == 'YES':
            cancer_result = "Mô hình dự đoán rằng có nguy cơ mắc ung thư phổi."
            image = Image.open('positive.jpg')
            st.image(image, caption='')
        else:
            cancer_result = "Mô hình dự đoán không có nguy cơ đáng kể mắc ung thư phổi."
            image = Image.open('negative.jpg')
            st.image(image, caption='')

        st.success(name + ', ' + cancer_result)




# Liver prediction page
if selected == 'Dự Đoán Bệnh Gan':  # pagetitle
    st.title("Dự đoán bệnh gan")
    image = Image.open('liver.jpg')
    st.image(image, caption='Dự đoán bệnh gan.')
    # columns
    # no inputs from the user
# st.write(info.astype(int).info())
    name = st.text_input("Họ và tên:")
    col1, col2, col3 = st.columns(3)

    with col1:
        Sex=0
        display = ("Nam", "Nữ")
        options = list(range(len(display)))
        value = st.selectbox("Giới tính", options, format_func=lambda x: display[x])
        if value == 0:
            Sex = 0
        elif value == 1:
            Sex = 1
    with col2:
        age = st.number_input("Nhập tuổi của bạn") # 2 
    with col3:
        Total_Bilirubin = st.number_input("Nhập chỉ số Bilirubin tổng") # 3
    with col1:
        Direct_Bilirubin = st.number_input("Nhập chỉ số Bilirubin trực tiếp")# 4

    with col2:
        Alkaline_Phosphotase = st.number_input("Nhập chỉ số Alkaline Phosphotase") # 5
    with col3:
        Alamine_Aminotransferase = st.number_input("Nhập chỉ số Alamine Aminotransferase") # 6
    with col1:
        Aspartate_Aminotransferase = st.number_input("Nhập chỉ số Aspartate Aminotransferase") # 7
    with col2:
        Total_Protiens = st.number_input("Nhập chỉ số Protein tổng")# 8
    with col3:
        Albumin = st.number_input("Nhập chỉ số Albumin") # 9
    with col1:
        Albumin_and_Globulin_Ratio = st.number_input("Nhập tỷ lệ Albumin và Globulin") # 10 
    # code for prediction
    liver_dig = ''

    # button
    if st.button("Kết quả kiểm tra gan"):
        liver_prediction=[[]]
        liver_prediction = liver_model.predict([[Sex,age,Total_Bilirubin,Direct_Bilirubin,Alkaline_Phosphotase,Alamine_Aminotransferase,Aspartate_Aminotransferase,Total_Protiens,Albumin,Albumin_and_Globulin_Ratio]])

        # after the prediction is done if the value in the list at index is 0 is 1 then the person is diabetic
        if liver_prediction[0] == 1:
            image = Image.open('positive.jpg')
            st.image(image, caption='')
            liver_dig = "Chúng tôi rất tiếc phải thông báo rằng bạn có khả năng mắc bệnh gan."
        else:
            image = Image.open('negative.jpg')
            st.image(image, caption='')
            liver_dig = "Chúc mừng, bạn không mắc bệnh gan."
        st.success(name+' , ' + liver_dig)






# Hepatitis prediction page
if selected == 'Dự Đoán Viêm Gan':
    st.title("Dự Đoán Viêm Gan")
    image = Image.open('h.png')
    st.image(image, caption='Dự Đoán Viêm Gan')

    # Columns
    # No inputs from the user
    name = st.text_input("Họ và tên:")
    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input("Nhập tuổi của bạn")  # 2
    with col2:
        sex = st.selectbox("Giới tính", ["Nam", "Nữ"])
        sex = 1 if sex == "Nam" else 2
    with col3:
        total_bilirubin = st.number_input("Nhập chỉ số Bilirubin tổng")  # 3

    with col1:
        direct_bilirubin = st.number_input("Nhập chỉ số Bilirubin trực tiếp")  # 4
    with col2:
        alkaline_phosphatase = st.number_input("Nhập chỉ số Alkaline Phosphatase")  # 5
    with col3:
        alamine_aminotransferase = st.number_input("Nhập chỉ số Alamine Aminotransferase")  # 6

    with col1:
        aspartate_aminotransferase = st.number_input("Nhập chỉ số Aspartate Aminotransferase")  # 7
    with col2:
        total_proteins = st.number_input("Nhập chỉ số Protein tổng")  # 8
    with col3:
        albumin = st.number_input("Nhập chỉ số Albumin")  # 9

    with col1:
        albumin_and_globulin_ratio = st.number_input("Nhập tỷ lệ Albumin và Globulin")  # 10

    with col2:
        your_ggt_value = st.number_input("Nhập giá trị GGT của bạn")  # Add this line
    with col3:
        your_prot_value = st.number_input("Nhập giá trị PROT của bạn")  # Add this line

    # Code for prediction
    hepatitis_result = ''

    # Button
    if st.button("Dự đoán viêm gan"):
        # Create a DataFrame with user inputs
        user_data = pd.DataFrame({
            'Age': [age],
            'Sex': [sex],
            'ALB': [total_bilirubin],  # Correct the feature name
            'ALP': [direct_bilirubin],  # Correct the feature name
            'ALT': [alkaline_phosphatase],  # Correct the feature name
            'AST': [alamine_aminotransferase],
            'BIL': [aspartate_aminotransferase],  # Correct the feature name
            'CHE': [total_proteins],  # Correct the feature name
            'CHOL': [albumin],  # Correct the feature name
            'CREA': [albumin_and_globulin_ratio],  # Correct the feature name
            'GGT': [your_ggt_value],  # Replace 'your_ggt_value' with the actual value
            'PROT': [your_prot_value]  # Replace 'your_prot_value' with the actual value
        })

        # Perform prediction
        hepatitis_prediction = hepatitis_model.predict(user_data)
        # Display result
        if hepatitis_prediction[0] == 1:
            hepatitis_result = "Chúng tôi rất tiếc phải thông báo rằng bạn có khả năng mắc bệnh viêm gan."
            image = Image.open('positive.jpg')
            st.image(image, caption='')
        else:
            hepatitis_result = 'Chúc mừng, bạn không mắc bệnh viêm gan.'
            image = Image.open('negative.jpg')
            st.image(image, caption='')

        st.success(name + ', ' + hepatitis_result)











# jaundice prediction page
if selected == 'Dự Đoán Bệnh Vàng Da':  # pagetitle
    st.title("Dự đoán bệnh vàng da")
    image = Image.open('j.jpg')
    st.image(image, caption='Dự đoán bệnh vàng da')
    # columns
    # no inputs from the user
# st.write(info.astype(int).info())
    name = st.text_input("Họ và tên:")
    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input("Nhập tuổi của bạn   ") # 2 
    with col2:
        Sex=0
        display = ("Nam", "Nữ")
        options = list(range(len(display)))
        value = st.selectbox("Giới tính", options, format_func=lambda x: display[x])
        if value == "Nam":
            Sex = 0
        elif value == "Nữ":
            Sex = 1
    with col3:
        Total_Bilirubin = st.number_input("Entre your Total_Bilirubin") # 3
    with col1:
        Direct_Bilirubin = st.number_input("Entre your Direct_Bilirubin")# 4

    with col2:
        Alkaline_Phosphotase = st.number_input("Entre your Alkaline_Phosphotase") # 5
    with col3:
        Alamine_Aminotransferase = st.number_input("Entre your Alamine_Aminotransferase") # 6
    with col1:
        Total_Protiens = st.number_input("Entre your Total_Protiens")# 8
    with col2:
        Albumin = st.number_input("Entre your Albumin") # 9 
    # code for prediction
    jaundice_dig = ''

    # button
    if st.button("Jaundice test result"):
        jaundice_prediction=[[]]
        jaundice_prediction = jaundice_model.predict([[age,Sex,Total_Bilirubin,Direct_Bilirubin,Alkaline_Phosphotase,Alamine_Aminotransferase,Total_Protiens,Albumin]])

        # after the prediction is done if the value in the list at index is 0 is 1 then the person is diabetic
        if jaundice_prediction[0] == 1:
            image = Image.open('positive.jpg')
            st.image(image, caption='')
            jaundice_dig = "we are really sorry to say but it seems like you have Jaundice."
        else:
            image = Image.open('negative.jpg')
            st.image(image, caption='')
            jaundice_dig = "Congratulation , You don't have Jaundice."
        st.success(name+' , ' + jaundice_dig)












from sklearn.preprocessing import LabelEncoder
import joblib


# Chronic Kidney Disease Prediction Page
if selected == 'Dự Đoán Bệnh Thận Mãn Tính':
    st.title("Dự Đoán Bệnh Thận Mãn Tính")
    # Add the image for Chronic Kidney Disease prediction if needed
    name = st.text_input("Họ và tên:")
    # Columns
    # No inputs from the user
    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.slider("Nhập tuổi của bạn", 1, 100, 25)  # 2
    with col2:
        bp = st.slider("Nhập huyết áp của bạn", 50, 200, 120)  # Add your own ranges
    with col3:
        sg = st.slider("Nhập trọng lượng riêng", 1.0, 1.05, 1.02)  # Add your own ranges

    with col1:
        al = st.slider("Nhập chỉ số Albumin", 0, 5, 0)  # Add your own ranges
    with col2:
        su = st.slider("Nhập chỉ số đường", 0, 5, 0)  # Add your own ranges
    with col3:
        rbc = st.selectbox("Hồng cầu", ["Bình thường", "Bất thường"])
        rbc = 1 if rbc == "Bình thường" else 0

    with col1:
        pc = st.selectbox("Tế bào mủ", ["Bình thường", "Bất thường"])
        pc = 1 if pc == "Bình thường" else 0
    with col2:
        pcc = st.selectbox("Cụm tế bào mủ", ["Có", "Không"])
        pcc = 1 if pcc == "Có" else 0
    with col3:
        ba = st.selectbox("Vi khuẩn", ["Có", "Không"])
        ba = 1 if ba == "Có" else 0

    with col1:
        bgr = st.slider("Nhập đường huyết ngẫu nhiên", 50, 200, 120)  # Add your own ranges
    with col2:
        bu = st.slider("Nhập urê máu", 10, 200, 60)  # Add your own ranges
    with col3:
        sc = st.slider("Nhập creatinine huyết thanh", 0, 10, 3)  # Add your own ranges

    with col1:
        sod = st.slider("Nhập chỉ số Natri", 100, 200, 140)  # Add your own ranges
    with col2:
        pot = st.slider("Nhập chỉ số Kali", 2, 7, 4)  # Add your own ranges
    with col3:
        hemo = st.slider("Nhập chỉ số Hemoglobin", 3, 17, 12)  # Add your own ranges

    with col1:
        pcv = st.slider("Nhập thể tích khối hồng cầu", 20, 60, 40)  # Add your own ranges
    with col2:
        wc = st.slider("Nhập số lượng bạch cầu", 2000, 20000, 10000)  # Add your own ranges
    with col3:
        rc = st.slider("Nhập số lượng hồng cầu", 2, 8, 4)  # Add your own ranges

    with col1:
        htn = st.selectbox("Tăng huyết áp", ["Có", "Không"])
        htn = 1 if htn == "Có" else 0
    with col2:
        dm = st.selectbox("Đái tháo đường", ["Có", "Không"])
        dm = 1 if dm == "Có" else 0
    with col3:
        cad = st.selectbox("Bệnh động mạch vành", ["Có", "Không"])
        cad = 1 if cad == "Có" else 0

    with col1:
        appet = st.selectbox("Cảm giác thèm ăn", ["Tốt", "Kém"])
        appet = 1 if appet == "Tốt" else 0
    with col2:
        pe = st.selectbox("Phù chân", ["Có", "Không"])
        pe = 1 if pe == "Có" else 0
    with col3:
        ane = st.selectbox("Thiếu máu", ["Có", "Không"])
        ane = 1 if ane == "Có" else 0

    # Code for prediction
    kidney_result = ''

    # Button
    if st.button("Dự đoán bệnh thận mãn tính"):
        # Create a DataFrame with user inputs
        user_input = pd.DataFrame({
            'age': [age],
            'bp': [bp],
            'sg': [sg],
            'al': [al],
            'su': [su],
            'rbc': [rbc],
            'pc': [pc],
            'pcc': [pcc],
            'ba': [ba],
            'bgr': [bgr],
            'bu': [bu],
            'sc': [sc],
            'sod': [sod],
            'pot': [pot],
            'hemo': [hemo],
            'pcv': [pcv],
            'wc': [wc],
            'rc': [rc],
            'htn': [htn],
            'dm': [dm],
            'cad': [cad],
            'appet': [appet],
            'pe': [pe],
            'ane': [ane]
        })

        # Perform prediction
        kidney_prediction = chronic_disease_model.predict(user_input)
        # Display result
        if kidney_prediction[0] == 1:
            image = Image.open('positive.jpg')
            st.image(image, caption='')
            kidney_prediction_dig = "Chúng tôi rất tiếc phải thông báo rằng bạn có khả năng mắc bệnh thận."
        else:
            image = Image.open('negative.jpg')
            st.image(image, caption='')
            kidney_prediction_dig = "Chúc mừng, bạn không mắc bệnh thận."
        st.success(name+' , ' + kidney_prediction_dig)



# Breast Cancer Prediction Page
if selected == 'Dự Đoán Ung Thư Vú':
    st.title("Dự Đoán Ung Thư Vú")
    name = st.text_input("Họ và tên:")
    # Columns
    # No inputs from the user
    col1, col2, col3 = st.columns(3)

    with col1:
        radius_mean = st.slider("Nhập bán kính trung bình", 6.0, 30.0, 15.0)
        texture_mean = st.slider("Nhập kết cấu trung bình", 9.0, 40.0, 20.0)
        perimeter_mean = st.slider("Nhập chu vi trung bình", 43.0, 190.0, 90.0)

    with col2:
        area_mean = st.slider("Nhập diện tích trung bình", 143.0, 2501.0, 750.0)
        smoothness_mean = st.slider("Nhập độ mịn trung bình", 0.05, 0.25, 0.1)
        compactness_mean = st.slider("Nhập độ chặt trung bình", 0.02, 0.3, 0.15)

    with col3:
        concavity_mean = st.slider("Nhập độ lõm trung bình", 0.0, 0.5, 0.2)
        concave_points_mean = st.slider("Nhập điểm lõm trung bình", 0.0, 0.2, 0.1)
        symmetry_mean = st.slider("Nhập độ đối xứng trung bình", 0.1, 1.0, 0.5)

    with col1:
        fractal_dimension_mean = st.slider("Nhập kích thước fractal trung bình", 0.01, 0.1, 0.05)
        radius_se = st.slider("Nhập sai số chuẩn bán kính", 0.1, 3.0, 1.0)
        texture_se = st.slider("Nhập sai số chuẩn kết cấu", 0.2, 2.0, 1.0)

    with col2:
        perimeter_se = st.slider("Nhập sai số chuẩn chu vi", 1.0, 30.0, 10.0)
        area_se = st.slider("Nhập sai số chuẩn diện tích", 6.0, 500.0, 150.0)
        smoothness_se = st.slider("Nhập sai số chuẩn độ mịn", 0.001, 0.03, 0.01)

    with col3:
        compactness_se = st.slider("Nhập sai số chuẩn độ chặt", 0.002, 0.2, 0.1)
        concavity_se = st.slider("Nhập sai số chuẩn độ lõm", 0.0, 0.05, 0.02)
        concave_points_se = st.slider("Nhập sai số chuẩn điểm lõm", 0.0, 0.03, 0.01)

    with col1:
        symmetry_se = st.slider("Nhập sai số chuẩn độ đối xứng", 0.1, 1.0, 0.5)
        fractal_dimension_se = st.slider("Nhập sai số chuẩn kích thước fractal", 0.01, 0.1, 0.05)

    with col2:
        radius_worst = st.slider("Nhập bán kính xấu nhất", 7.0, 40.0, 20.0)
        texture_worst = st.slider("Nhập kết cấu xấu nhất", 12.0, 50.0, 25.0)
        perimeter_worst = st.slider("Nhập chu vi xấu nhất", 50.0, 250.0, 120.0)

    with col3:
        area_worst = st.slider("Nhập diện tích xấu nhất", 185.0, 4250.0, 1500.0)
        smoothness_worst = st.slider("Nhập độ mịn xấu nhất", 0.07, 0.3, 0.15)
        compactness_worst = st.slider("Nhập độ chặt xấu nhất", 0.03, 0.6, 0.3)

    with col1:
        concavity_worst = st.slider("Nhập độ lõm xấu nhất", 0.0, 0.8, 0.4)
        concave_points_worst = st.slider("Nhập điểm lõm xấu nhất", 0.0, 0.2, 0.1)
        symmetry_worst = st.slider("Nhập độ đối xứng xấu nhất", 0.1, 1.0, 0.5)

    with col2:
        fractal_dimension_worst = st.slider("Nhập kích thước fractal xấu nhất", 0.01, 0.2, 0.1)

        # Code for prediction
    breast_cancer_result = ''

    # Button
    if st.button("Dự đoán ung thư vú"):
        # Create a DataFrame with user inputs
        user_input = pd.DataFrame({
            'radius_mean': [radius_mean],
            'texture_mean': [texture_mean],
            'perimeter_mean': [perimeter_mean],
            'area_mean': [area_mean],
            'smoothness_mean': [smoothness_mean],
            'compactness_mean': [compactness_mean],
            'concavity_mean': [concavity_mean],
            'concave points_mean': [concave_points_mean],  # Update this line
            'symmetry_mean': [symmetry_mean],
            'fractal_dimension_mean': [fractal_dimension_mean],
            'radius_se': [radius_se],
            'texture_se': [texture_se],
            'perimeter_se': [perimeter_se],
            'area_se': [area_se],
            'smoothness_se': [smoothness_se],
            'compactness_se': [compactness_se],
            'concavity_se': [concavity_se],
            'concave points_se': [concave_points_se],  # Update this line
            'symmetry_se': [symmetry_se],
            'fractal_dimension_se': [fractal_dimension_se],
            'radius_worst': [radius_worst],
            'texture_worst': [texture_worst],
            'perimeter_worst': [perimeter_worst],
            'area_worst': [area_worst],
            'smoothness_worst': [smoothness_worst],
            'compactness_worst': [compactness_worst],
            'concavity_worst': [concavity_worst],
            'concave points_worst': [concave_points_worst],  # Update this line
            'symmetry_worst': [symmetry_worst],
            'fractal_dimension_worst': [fractal_dimension_worst],
        })

        # Perform prediction
        breast_cancer_prediction = breast_cancer_model.predict(user_input)
        # Display result
        if breast_cancer_prediction[0] == 1:
            image = Image.open('positive.jpg')
            st.image(image, caption='')
            breast_cancer_result = "Chúng tôi rất tiếc phải thông báo rằng bạn có khả năng mắc ung thư vú."
        else:
            image = Image.open('negative.jpg')
            st.image(image, caption='')
            breast_cancer_result = "Chúc mừng, bạn không mắc ung thư vú."

        st.success(name + ', ' + breast_cancer_result)
