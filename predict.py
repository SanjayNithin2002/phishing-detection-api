import pickle
import pandas as pd
from PhishingDetection import detect_phishing


def load_results_from_pickle(filename):
    with open(filename, 'rb') as file:
        results = pickle.load(file)
    return results

def model_predict(dicti):
    count = list(dicti.values()).count("Legitimate")
    
    if count >= 4:
        return "Legitimate"
    elif 2 <= count <= 3:
        return "Suspicious"
    else:
        return "Phishing"


def predict(url):

    label_mapping = {
        1: "Legitimate",
        0: "Suspicious",
        -1: "Phishing"
    }

    svm_model = load_results_from_pickle('models/svm_model.pkl')
    lr_model = load_results_from_pickle('models/lr_model.pkl')
    rfc_model = load_results_from_pickle('models/rfc_model.pkl')
    clf_model = load_results_from_pickle('models/clf_model.pkl')
    ensemble_model = load_results_from_pickle('models/ensemble_model.pkl')

    values_dict = detect_phishing(url)
    df = pd.DataFrame(values_dict, index=[0])

    results_dict = {
        "attribute_values": {key: label_mapping.get(value, value) for key, value in values_dict.items()},
        "model_predictions": {
            "Support Vector Machine": label_mapping[svm_model.predict(df).item()],
            "Logistic Regression": label_mapping[lr_model.predict(df).item()],
            "Random Forest Classifier": label_mapping[rfc_model.predict(df).item()],
            "AdaBoost Classifier": label_mapping[clf_model.predict(df).item()],
            "Ensemble Model": label_mapping[ensemble_model.predict(df).item()]
        }
    }

    results_dict["prediction"] = model_predict(results_dict["model_predictions"])

    return results_dict
