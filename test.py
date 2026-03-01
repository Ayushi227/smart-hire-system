import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression

age = 22
gender = 'female'
val1 = 1
val2 = 1
val3=10
val4 =2
val5 =1
 # model prediction
df = pd.read_csv(r'static\trainDataset.csv')
le = LabelEncoder()
df['Gender'] = le.fit_transform(df['Gender'])
x_train = df.iloc[:, :-1].to_numpy()
y_train = df.iloc[:, -1].to_numpy(dtype = str)
lreg = LogisticRegression(multi_class='multinomial', solver='newton-cg',max_iter =1000)
lreg.fit(x_train, y_train)

if gender == 'male':
    gender = 1
elif gender == 'female': 
    gender = 0
input =  [gender, age, val1, val2, val3, val4, val5]

pred = str(lreg.predict([input])[0]).capitalize()
print(pred)