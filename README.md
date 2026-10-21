# qiyas-2026-006697

Qiyas Exercises — a collection of data extraction, machine learning, and scripting exercises.

## Projects

### 📊 [Regression](./Regression)

House price / land value prediction. Trains 42 pipelines (2 encodings × 3 scalers × 7 algorithms) to predict property prices in ETB from features like room count, area, age, and location. Includes Gradio and Streamlit UIs for interactive prediction and benchmark comparison. See [`Regression/README.md`](./Regression/README.md).

### 📩 [Classification Project](./Classification%20Project)

SMS spam classifier trained on the UCI SMS Spam Collection dataset. Benchmarks 18 vectorizer/algorithm combinations (CountVectorizer & TF-IDF × 9 classifiers) and serves the best-performing pipeline (Linear SVM + CountVectorizer, F1 = 0.936) through a Streamlit UI. See [`Classification Project/README.md`](./Classification%20Project/README.md).

### 🌾 [Qiyas Hackathon — Crop Yield Forecast](./Qiyas_Hackathon_Crop_Yield_Forcast)

Ethiopian smallholder crop-yield forecasting challenge. An end-to-end reproducible regression workflow integrating plot-level agronomic inputs, regional growing-season weather data, and market prices. Evaluates multiple algorithms with feature engineering and weather ablation (final model: RMSE 0.473 t/ha, MAE 0.349 t/ha, R² 0.880, 5-fold CV 0.488 ± 0.013 t/ha). Includes interactive Streamlit and Gradio deployment apps, analytical reports, 12 visualization figures, competition presentation slides, and leaderboard submission. See [`Qiyas_Hackathon_Crop_Yield_Forcast/README.md`](./Qiyas_Hackathon_Crop_Yield_Forcast/README.md).

## Other notebooks

Practice / exercise notebooks not tied to the three projects above:

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
pip install pandas numpy scikit-learn joblib gradio streamlit plotly xgboost lightgbm matplotlib seaborn python-pptx
```
