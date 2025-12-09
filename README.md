# 기상 데이터 기반의 자전거 수요 예측
이서현, 한양인터칼리지학부(서울), jiyeahna19@hanyang.ac.kr
<br>정시형, 한양인터칼리지학부(서울), non2021115@hanyang.ac.kr
<br>하준호, 한양인터칼리지학부(서울), haho0802@hanyang.ac.kr

<br>[I. Proposal](#section1)
<br>[II. Datasets](#section2)
<br>[III. Methodology](#section3)
<br>[IV. Evaluation and Analysis](#section4)
<br>[V. Related Work](#section5)
<br>[VI. Conclusion](#section6)

## I. Proposal<a id="section1"></a>
<br>**Motivation**
<br>본 프로젝트는 일별 기상 데이터가 자전거 대여 수요에 미치는 영향을 정량적으로 분석하고, 이를 기반으로 일일 대여량을 예측하는 모델을 구축하는 것을 목적으로 한다.
UCI Bike Sharing Dataset의 day.csv는 온도, 체감온도, 습도, 풍속 등 기상 요인과 실제 대여량이 함께 기록되어 있어 기계학습 회귀 모델의 적용 가능성을 평가하기에 적합한 구조를 갖고 있다.
따라서 본 연구는 기상 기반 예측 모델이 도심형 자전거 서비스 수요 변동을 어느 정도 설명할 수 있는지 분석적 근거를 제공하고자 한다.

<br>**What do you want to see at the end?**
<br>본 프로젝트는 다음의 결과물을 목표로 한다:
<br>-기상 변수와 대여량 간의 통계적·시각적 관계 분석
<br>-RandomForestRegressor 기반 예측 모델 구현
<br>-예측 성능(MAE, R²)의 정량적 평가
<br>-Feature Importance 분석을 통한 주요 영향 요인 규명
<br>-시각화 기반의 해석 제공 (온도-대여량, 실제값-예측값)

## II. Datasets <a id="section2"></a>
<br>본 분석은 UCI Machine Learning Repository에서 제공하는 Bike Sharing Dataset 중 “day.csv” 파일을 사용하였다.
<br>
```python
data_path = "day.csv" #파일 디렉토리
bike_data = pd.read_csv(data_path) #파일 저장
# Basic EDA: preview data, summary statistics, and correlations
print("First 5 rows of the dataset:")
print(bike_data.head())

print("\nBasic statistics:")
print(bike_data.describe())

print("\nCorrelation matrix:")
print(bike_data.corr(numeric_only=True))
```
<br> 데이터 로딩과 데이터 미리보기

<br>해당 데이터는 2011–2012년 기간의 일별 관측치(총 731개)로 구성되며, 기상 조건과 대여량이 함께 기록되어 있다.
본 연구에서는 모델 입력 변수로 다음 네 가지 기상 요인을 채택하였다:
<br>temp: 정규화된 온도
<br>atemp: 정규화된 체감온도
<br>hum: 상대습도
<br>windspeed: 풍속
```python
feature_columns = ["temp", "atemp", "hum", "windspeed"]
target_column = "cnt"
X = bike_data[feature_columns]
y = bike_data[target_column]
```
<br>종속변수는 cnt(하루 총 대여량)으로 설정하였다.
<br>이 네 변수는 실제 이용자의 활동성과 날씨 민감도를 반영하는 요인으로, 예측 모델의 입력 피처로 타당하다.

## III. Methodology <a id="section3"></a>
<br>Exploratory Data Analysis (EDA)
<br>데이터의 기초 통계, 상위 5개 행, 그리고 사용 변수(temp, atemp, hum, windspeed, cnt) 중심으로 상관행렬을 확인하였다.
EDA 결과, temp–cnt, atemp–cnt는 높은 양의 상관관계를 보였고, hum–cnt, windspeed–cnt는 비교적 낮거나 약한 음의 상관관계를 보였다.
이는 기상 요인이 자전거 이용 패턴에 의미 있게 작용함을 시사한다.

<br>Model Selection: RandomForestRegressor
<br>본 프로젝트는 RandomForestRegressor를 사용하여 예측 모델을 구성하였다.
랜덤포레스트는 비선형 관계 탐지, 다중 트리 결합을 통한 높은 안정성, 변수 중요도 산출 가능성 등의 장점으로 인해 본 연구 목적에 적합하다.

<br>Model Parameters
<br>분석의 안정성을 강화하기 위해 n_estimators=200을 사용하여 트리 개수를 기본값(100)보다 증가시켰다.
이는 개별 트리의 변동성을 평균화하여 보다 일관된 회귀 성능을 얻기 위한 설정이다.
```python
model = RandomForestRegressor(n_estimators=200, random_state=42)
```
<br> RandomForestRegressor 모델 정의

<br>Train–Test Split
<br>전체 데이터를 80:20 비율로 훈련·테스트 세트로 분리하였고, random_state=42를 사용하여 재현성을 확보하였다.
```python
# Split the data into training and testing sets (80:20 split)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```
<br> 학습 데이터와 테스트 데이터 분류

## IV. Evaluation and Analysis <a id="section4"></a>
<br>Model Performance
<br>모델 학습 후, 테스트 세트에 대해 다음 평가 지표를 산출하였다.
```python
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
```
<br>Mean Absolute Error (MAE): 1210.97
<br>R² Score: 0.4499
<br>R² = 0.4499는 모델이 기상 변수만으로 전체 수요 변동성의 약 45%를 설명함을 의미한다.
이는 자전거 이용량이 날씨 외에도 요일, 사회적 패턴, 이벤트 등 다양한 요인에 의해 영향을 받는다는 점을 반영하며, 기상 변수 중심 모델로서는 타당한 수준의 설명력을 제공한다.

<br>Scatter Plots
<br>(a) Temperature vs Bike Count
<br><img width="517" height="470" alt="image" src="https://github.com/user-attachments/assets/d88dc4a1-26c4-4ae3-ae97-00b3546dc5b4" />
<br>온도 상승과 대여량 증가 간의 일관된 양의 관계가 관찰되었다.
<br>이는 온도가 자전거 이용 활동성의 핵심 결정 요인임을 시각적으로 확인시키는 결과이다.

<br>(b) Actual vs Predicted Bike Counts
<br><img width="348" height="470" alt="image" src="https://github.com/user-attachments/assets/d6adfdea-960f-42cd-86f0-08e833973ec3" />
<br>실제값과 예측값은 대체로 y=x 이상적인 예측선 주변에 분포하며, 모델이 수요 패턴을 일정 수준으로 재현하고 있음을 보여준다.
<br>특정 구간에서 예측 편차가 발생하나 이는 입력 피처가 네 가지 기상 요인으로 제한되어 있다는 점에서 구조적으로 자연스러운 결과이다.



<br>Feature Importance
<br>RandomForestRegressor가 산출한 변수 중요도는 다음과 같다:
<br>temp: 0.4284
<br>atemp: 0.2441
<br>hum: 0.1990
<br>windspeed: 0.1286
<br>온도 관련 변수(temp, atemp)가 가장 높은 중요도를 보이는데,
이는 두 변수가 높은 상관관계(>0.98)를 가지며 온도 정보를 공통적으로 반영하기 때문이다.
이 두 변수의 높은 중요도는 온도 변화가 자전거 대여량 예측에서 핵심적 역할을 한다는 점을 재확인한다.
습도와 풍속은 보조적 영향 요인으로 해석할 수 있다.

## V. Related Work <a id="section5"></a>
<br>본 프로젝트는 다음 자료를 기반으로 분석을 수행하였다:
<br>UCI Machine Learning Repository: Bike Sharing Dataset 문서
<br>Scikit-learn Documentation: RandomForestRegressor, train_test_split, 평가 지표
<br>Pandas Documentation: 데이터 처리 및 기술 통계
<br>Matplotlib Tutorials: 시각화 방법

## VI. Conclusion <a id="section6"></a>
<br>본 프로젝트는 기상 데이터를 활용하여 일별 자전거 대여량을 예측하는 회귀 모델을 구축하고, 그 성능과 해석 결과를 체계적으로 검증하였다.
온도 변수의 지배적 영향력, 습도·풍속의 제한적 역할, 실제값-예측값 비교 결과 등을 종합적으로 고려할 때, 기상 요인 중심의 예측 모델은 수요 패턴의 상당 부분을 설명할 수 있음을 확인하였다.
본 분석은 도시형 공유 자전거 서비스의 운영 정책, 수요 예측, 기상 기반 리소스 배분 전략을 구축하는 데 참고 자료로 활용될 수 있다.
