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
<br>- 기상 변수와 대여량 간의 통계적·시각적 관계 분석
<br>- RandomForestRegressor 기반 예측 모델 구현
<br>- 예측 성능(MAE, R²)의 정량적 평가
<br>- Feature Importance 분석을 통한 주요 영향 요인 규명
<br>- 시각화 기반의 해석 제공 (온도-대여량, 실제값-예측값)

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
<br>**Exploratory Data Analysis (EDA)**
<br>데이터의 기초 통계, 상위 5개 행, 그리고 사용 변수(temp, atemp, hum, windspeed, cnt) 중심으로 상관행렬을 확인하였다.
E화
