import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

FEATURES = ["u", "g", "r", "i", "z"]
TARGET_CLASS = "class"
TARGET_REG = "redshift"


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"[INFO] Dataset cargado: {df.shape[0]} filas, {df.shape[1]} columnas")
    print(f"[INFO] Clases: {df[TARGET_CLASS].value_counts().to_dict()}")
    return df


def get_classification_data(df: pd.DataFrame):
    feature_cols = FEATURES + [TARGET_REG]
    X = df[feature_cols]
    le = LabelEncoder()
    y = le.fit_transform(df[TARGET_CLASS])
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    return X_train, X_test, y_train, y_test, le, scaler


def get_regression_data(df: pd.DataFrame):
    X = df[FEATURES]
    y = df[TARGET_REG]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    return X_train, X_test, y_train, y_test, scaler


def get_clustering_data(df: pd.DataFrame):
    X = df[FEATURES]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, df[TARGET_CLASS].values
