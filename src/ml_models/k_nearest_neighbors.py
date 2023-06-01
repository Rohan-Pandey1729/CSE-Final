from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from imblearn.over_sampling import RandomOverSampler
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score


def k_nearest(filename: str):
    print("K-Nearest Neighbors:")
    df = pd.read_csv(filename)
    features = df.loc[:, df.columns != "TenYearCHD"]
    labels = df["TenYearCHD"]
    oversampler = RandomOverSampler(random_state=42)
    features_resampled, labels_resampled = oversampler.fit_resample(features,
                                                                    labels)
    (
        features_train,
        features_test,
        labels_train,
        labels_test,
    ) = train_test_split(
        features_resampled, labels_resampled, test_size=0.2, random_state=42
    )  # stratified data
    k = 3  # change value using testing
    # Perform standardization on training data
    scaler = StandardScaler()
    scaled_features_train = scaler.fit_transform(features_train)

    # Apply the same standardization to testing data
    scaled_features_test = scaler.transform(features_test)

    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(scaled_features_train, labels_train)
    labels_pred = model.predict(scaled_features_test)
    model.fit(features_train, labels_train)
    labels_train_pred = model.predict(features_train)
    return (labels_train, labels_train_pred, labels_test, labels_pred)


def grid_search(filename):
    df = pd.read_csv(filename)
    features = df.loc[:, df.columns != "TenYearCHD"]
    labels = df["TenYearCHD"]
    oversampler = RandomOverSampler(random_state=42)
    features_resampled, labels_resampled = oversampler.fit_resample(features,
                                                                    labels)
    (
        features_train,
        features_test,
        labels_train,
        labels_test,
    ) = train_test_split(
        features_resampled, labels_resampled, test_size=0.2, random_state=42
    )
    # Perform standardization on training data
    scaler = StandardScaler()
    scaled_features_train = scaler.fit_transform(features_train)

    # Apply the same standardization to testing data
    scaled_features_test = scaler.transform(features_test)
    model = KNeighborsClassifier()
    param_grid = {
        'n_neighbors': range(1, 15),  # K values
        'weights': ['uniform', 'distance'],  # Weight metrics
        'metric': ['euclidean', 'manhattan',
                   'chebyshev', 'minkowski'],  # Distance metrics
        'algorithm': ['brute', 'kd_tree', 'ball_tree']  # Algorithms
    }
    grid_search = GridSearchCV(model, param_grid, cv=5, scoring='f1')
    grid_search.fit(scaled_features_train, labels_train)
    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_
    labels_pred = best_model.predict(scaled_features_test)
    f1 = f1_score(labels_test, labels_pred)
    print("Best Hyperparameters:", best_params)
    print("F1:", f1)
