"""
Bike rental demand prediction using UCI Bike Sharing Dataset (day.csv).
The script performs EDA, trains a RandomForestRegressor, evaluates it,
prints feature importances, and generates diagnostic plots.
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score


def main() -> None:
    """Execute the data analysis, model training, evaluation, and visualization."""
    # Load the dataset from the current directory
    data_path = "day.csv"
    bike_data = pd.read_csv(data_path)

    # Basic EDA: preview data, summary statistics, and correlations
    print("First 5 rows of the dataset:")
    print(bike_data.head())

    print("\nBasic statistics:")
    print(bike_data.describe())

    print("\nCorrelation matrix:")
    print(bike_data.corr(numeric_only=True))

    # Select features and target variable
    feature_columns = ["temp", "atemp", "hum", "windspeed"]
    target_column = "cnt"
    X = bike_data[feature_columns]
    y = bike_data[target_column]

    # Split the data into training and testing sets (80:20 split)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Initialize and train the RandomForestRegressor model
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    # Predict on the test set
    y_pred = model.predict(X_test)

    # Evaluate the model using MAE and R^2 score
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"\nMean Absolute Error (MAE): {mae:.2f}")
    print(f"R^2 Score: {r2:.4f}")

    # Display feature importances
    feature_importances = pd.Series(
        model.feature_importances_, index=feature_columns
    ).sort_values(ascending=False)

    print("\nFeature Importances:")
    for feature, importance in feature_importances.items():
        print(f"{feature}: {importance:.4f}")

    # Plot temperature vs. total bike count
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.scatter(bike_data["temp"], bike_data["cnt"], alpha=0.6)
    plt.title("Temperature vs Bike Count")
    plt.xlabel("Normalized Temperature")
    plt.ylabel("Total Bike Count")

    # Plot actual vs. predicted counts with reference line
    plt.subplot(1, 2, 2)
    plt.scatter(y_test, y_pred, alpha=0.6, label="Predictions")
    plt.title("Actual vs Predicted Bike Counts")
    plt.xlabel("Actual Counts")
    plt.ylabel("Predicted Counts")
    diagonal_start = min(y_test.min(), y_pred.min())
    diagonal_end = max(y_test.max(), y_pred.max())
    plt.plot(
        [diagonal_start, diagonal_end],
        [diagonal_start, diagonal_end],
        color="red",
        linestyle="--",
        label="Ideal Fit",
    )
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
