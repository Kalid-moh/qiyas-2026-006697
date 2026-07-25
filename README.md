# qiyas-2026-006697

Qiyas Exercises — a collection of data extraction, machine learning, and scripting exercises.

## Projects

### 📊 [Regression](./Regression)

House price / land value prediction. Trains 42 pipelines (2 encodings × 3 scalers × 7 algorithms) to predict property prices in ETB from features like room count, area, age, and location. Includes Gradio and Streamlit UIs for interactive prediction and benchmark comparison. See [`Regression/README.md`](./Regression/README.md).

### 📩 [Classification Project](./Classification%20Project)

SMS spam classifier trained on the UCI SMS Spam Collection dataset. Benchmarks 18 vectorizer/algorithm combinations (CountVectorizer & TF-IDF × 9 classifiers) and serves the best-performing pipeline (Linear SVM + CountVectorizer, F1 = 0.936) through a Streamlit UI. See [`Classification Project/README.md`](./Classification%20Project/README.md).

## Other notebooks

Practice / exercise notebooks not tied to the two projects above:

| File                     | Description                 |
| ------------------------ | --------------------------- |
| `Numpy.ipynb`            | NumPy exercises             |
| `class 15 ML task.ipynb` | ML class exercise           |
| `data extraction.ipynb`  | Data extraction practice    |
| `file_writing.ipynb`     | File I/O practice           |
| `table scraping.ipynb`   | Web table scraping practice |
| `test/`                  | Test/scratch files          |

## Setup

Each project folder has its own README with specific setup instructions and dependencies. General requirements across the repo:

```bash
pip install pandas numpy scikit-learn joblib gradio streamlit plotly xgboost lightgbm
```
