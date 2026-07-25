# 📩 Classification Project — SMS Spam Classifier

Classifies SMS messages as spam or ham (not spam), trained on the [UCI SMS Spam Collection](https://archive.ics.uci.edu/dataset/228/sms+spam+collection) dataset (5,574 messages). Benchmarks 18 vectorizer/algorithm combinations and serves the best one through a Streamlit UI.

## How it works

1. **`train_classifiers.py`** trains every combination of:
   - **Vectorizer:** CountVectorizer (Bag of Words), TF-IDF
   - **Algorithm:** Perceptron, Logistic Regression, Linear SVM, KNN, Decision Tree, Random Forest, XGBoost, LightGBM, Neural Network (MLP)

   That's 18 trained pipelines, each scored on accuracy, F1, precision, and recall (F1 is used to rank them, since spam is a minority class ~13% of the data). Two files are saved:
   - `classification_bundle.pkl` — all 18 trained pipelines + results table (large)
   - `best_model.pkl` — just the winning pipeline, lightweight, deployment-ready

2. **`streamlit_classifier_app.py`** loads `best_model.pkl` and classifies whatever message you type in — no model picker, it always uses the best-performing pipeline found during training.

## Results

| Rank | Pipeline                               | Accuracy | F1    |
| ---- | -------------------------------------- | -------- | ----- |
| 1    | Linear SVM + CountVectorizer           | 98.39%   | 0.936 |
| 2    | Linear SVM + TF-IDF                    | 98.12%   | 0.925 |
| 3    | Neural Network (MLP) + CountVectorizer | 98.12%   | 0.924 |
| 4    | Neural Network (MLP) + TF-IDF          | 98.03%   | 0.923 |
| 5    | Perceptron + TF-IDF                    | 97.94%   | 0.921 |

**Linear SVM + CountVectorizer** wins — highest F1, and trains in ~0.02s.

## Setup

From within this folder:

```bash
pip install pandas numpy scikit-learn joblib xgboost lightgbm streamlit
```

You'll also need the `SMSSpamCollection` file in this folder (tab-separated, `label` + `message` columns, no header) — [download from UCI](https://archive.ics.uci.edu/dataset/228/sms+spam+collection).

## Usage

```bash
# 1. Train all 18 pipelines and save the model files
python train_classifiers.py

# 2. Run the Streamlit UI
streamlit run streamlit_classifier_app.py
```

## Folder structure

```
Classification Project/
├── train_classifiers.py           # Trains all 18 pipelines, saves model files
├── streamlit_classifier_app.py    # Streamlit UI (uses best_model.pkl only)
├── SMSSpamCollection               # Dataset (download from UCI, not included)
├── classification_bundle.pkl       # Generated: all 18 models + results
├── best_model.pkl                  # Generated: winning pipeline only
└── results_summary.csv             # Generated: metrics table for all 18 pipelines
```

## Notes

- CountVectorizer and TF-IDF are both explicitly cast to `float64` — LightGBM rejects the integer sparse output CountVectorizer produces by default.
- Linear SVM has no `predict_proba`, so the app falls back to `decision_function` for a confidence signal (a signed distance from the decision boundary, not a probability).
- To retrain on new/updated data, just rerun `train_classifiers.py` — it regenerates all three output files.
- `classification_bundle.pkl` is ~35MB — consider adding it to `.gitignore` since `best_model.pkl` is all the deployed app actually needs.
