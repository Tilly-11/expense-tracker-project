import numpy as np
from django.db.models import Sum
from .sentence_classifier import SimpleCategoryModel
from sklearn.ensemble import IsolationForest
from joblib import load
from ..models import Expense

def detect_anomalies_for_user(user, months=6):
    """
    Simple approach: aggregate user's expenses per category over last `months`.
    Fit IsolationForest on amounts or use z-score per category.
    Returns list of anomalous expense dicts.
    """
    qs = Expense.objects.filter(user=user)  # you can filter by date range
    if qs.count() < 10:
        return []  # not enough data

    # build numeric feature: [amount, month_of_year] optionally category encoding
    data = []
    ids = []
    for e in qs:
        data.append([float(e.amount)])
        ids.append(e.id)
    import numpy as np
    X = np.array(data)
    iso = IsolationForest(n_estimators=100, contamination=0.02, random_state=42)
    iso.fit(X)
    preds = iso.predict(X)  # -1 is anomaly
    anomalous = []
    for i, p in enumerate(preds):
        if p == -1:
            e = qs[i]
            anomalous.append({
                'id': e.id,
                'amount': float(e.amount),
                'description': e.description,
                'date': e.date.isoformat(),
            })
    return anomalous