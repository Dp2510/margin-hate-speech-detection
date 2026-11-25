# Margin · Hate Speech Detection

Margin is a local dashboard that gives posting guidance for draft English social-media comments. Fine-tuned DistilBERT predicts one of three classes: no hate speech, hate speech, or ambiguous. Separate text models estimate severity, possible groups referenced, and behavior ratings. This project was developed for CS913 Natural Language Processing at IIIT Surat.

## Repository contents

| Path | Purpose |
| --- | --- |
| `hateSpeech.ipynb` | Dataset preparation, model experiments, and evaluation |
| `comment_web.py` | Local HTTP server |
| `comment_analysis.py` | Prediction and dashboard guidance logic |
| `templates/comment_review.html` | Dashboard interface |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Excludes local environments, data, and generated model artifacts |

## Set up on Windows

From the repository folder in PowerShell, use Python 3.12:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

For notebook work in VS Code, open `hateSpeech.ipynb` and select the project's `.venv` as the notebook kernel. DistilBERT training in the notebook checks for a CUDA GPU. Install a compatible [CUDA build of PyTorch](https://pytorch.org/get-started/locally/) before running those cells.

## Run the dashboard

Place a trusted copy of `hate_speech_models.joblib` and the full `distilbert_berkeley_epoch2/` directory beside `comment_web.py`. Use the same scikit-learn version used to save the joblib bundle. Use the final DistilBERT version of `comment_analysis.py` from your working dashboard.

```powershell
.\.venv\Scripts\python.exe comment_web.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000). For a local demo, use prepared checkpoints so you can start the dashboard directly.

## Reproduce the experiments

Download the [UC Berkeley Measuring Hate Speech Parquet file](https://huggingface.co/datasets/ucberkeley-dlab/measuring-hate-speech/blob/main/measuring-hate-speech.parquet) and save it in the repository root as `measuring_hate_speech.parquet`. The notebook aggregates votes and ratings by comment ID, cleans the text, assigns grouped train/validation/test splits, and generates `berkeley_hate_speech_processed.parquet`. It also exports the auxiliary model bundle and the DistilBERT checkpoints. The earlier notebook interface exports a TF-IDF version of `comment_analysis.py`; keep a copy of the final dashboard module when rerunning that cell.

The dataset contains offensive language. Credit the [UC Berkeley D-Lab dataset](https://huggingface.co/datasets/ucberkeley-dlab/measuring-hate-speech) and follow its terms when sharing data.

## Results

The selected DistilBERT checkpoint (epoch 2) achieved **67.5% accuracy**, **0.583 macro F1**, and **70.3% hate-speech recall** on 3,957 held-out test comments. The dashboard shows “No hate-speech concern detected” when no hate speech is the highest-scoring class and its score is at least 0.90. Lower-scoring no-hate predictions and ambiguous predictions prompt review.
