import re


def analyse_comment(text, bundle):
    clean_text = " ".join(text.split())
    if not clean_text:
        return None

    clean_text = re.sub(bundle["url_pattern"], "URL", clean_text)
    clean_text = re.sub(bundle["username_pattern"], "USER", clean_text)

    pipeline = bundle["verdict_model"]
    features = pipeline[:-1].transform([clean_text])
    classifier = pipeline[-1]

    scores = classifier.predict_proba(features)[0]
    top_index = scores.argmax()
    verdict = classifier.classes_[top_index]

    guidance = "Review before posting"
    if verdict == "hate_speech":
        guidance = "Hate-speech warning"
    elif verdict == "no_hate_speech" and scores[top_index] >= bundle["reassurance_threshold"]:
        guidance = "No hate-speech concern detected"

    groups = [
        name for name, model in bundle["group_models"].items()
        if model.predict(features)[0]
    ]
    behaviors = {
        name: float(model.predict(features)[0])
        for name, model in bundle["behavior_models"].items()
    }

    return {
        "verdict": verdict,
        "posting_guidance": guidance,
        "severity": float(bundle["severity_model"].predict(features)[0]),
        "groups_referenced": groups,
        "behavior_ratings": behaviors,
    }
