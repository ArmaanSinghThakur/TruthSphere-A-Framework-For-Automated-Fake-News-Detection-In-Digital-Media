import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
import re
import string
import pickle







data_fake= pd.read_csv("Fake.csv")
data_real= pd.read_csv("True.csv")
def wordopt(text):
    text= text.lower()
    text= re.sub('\[.*?\]', '', text)
    text= re.sub("\\W", " ", text)
    text= re.sub("https?://\S+|www\.\S+", "", text)
    text= re.sub('<.*?>+', '' , text)
    text=re.sub('[%s]' %re.escape(string.punctuation), '', text)
    text= re.sub('\n', '', text)
    text= re.sub('\w*\d\w*', '', text)
    return text


data_merge= pd.concat([data_real,data_fake])
data= data_merge.sample(frac=1)

data["text"]= data["text"].apply(wordopt)

x= data['text']
y= data['class']
x_train, x_test, y_train, y_test= train_test_split(x,y, test_size=0.25)

vectorization= TfidfVectorizer()
xv_train= vectorization.fit_transform(x_train)
xv_test= vectorization.transform(x_test)
LR= LogisticRegression()
DT= DecisionTreeClassifier()
GB= GradientBoostingClassifier(random_state=0)
RF= RandomForestClassifier(random_state=0)

LR.fit(xv_train, y_train)
DT.fit(xv_train, y_train)
GB.fit(xv_train, y_train)
RF.fit(xv_train, y_train)

def output_label(n):
    if n == 0:
        return "Fake News"
    elif n == 1:
        return "Real News"

def manual_testing(news):
    testing_news = {"text": [news]}
    new_def_test = pd.DataFrame(testing_news)
    new_def_test["text"] = new_def_test["text"].apply(wordopt)
    new_x_test = new_def_test["text"]
    new_xv_test = vectorization.transform(new_x_test)
    pred_LR = LR.predict(new_xv_test)
    pred_DT = DT.predict(new_xv_test)
    pred_GBC = GB.predict(new_xv_test)
    pred_RFC = RF.predict(new_xv_test)

    LR_main = output_label(pred_LR[0])
    DT_main = output_label(pred_DT[0])
    RFC_main = output_label(pred_RFC[0])

    if LR_main == DT_main == RFC_main:
        return LR_main
    elif LR_main == DT_main or LR_main == RFC_main:
        return LR_main
    elif DT_main == LR_main or DT_main == RFC_main:
        return DT_main



