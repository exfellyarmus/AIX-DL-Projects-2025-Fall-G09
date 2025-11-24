# 기상 데이터 기반의 자전거 수요 예측
이서현, 한양인터칼리지학부(서울), jiyeahna19@hanyang.ac.kr
정시형, 한양인터칼리지학부(서울),
하준호, 한양인터칼리지학부(서울),

I. Proposal
Motivation
본 프로젝트는 기상 요인이 도시 내 자전거 수요에 미치는 영향을 정량적으로 분석하고, 이를 기반으로 일별 대여량을 예측하는 모델을 구현하는 데 목적이 있다.
특히 Bike Sharing Dataset은 계절성·기상 변화·사용 패턴이 모두 반영되어 있어, 기계학습 모델이 환경적 요인을 어떻게 활용하는지 검증하기에 적합하다. 본 연구는 Python 기반 분석 환경에서 일관된 예측 절차를 구축하여, 기상 변수만으로도 수요 예측이 가능한지를 평가한다.

What do you want to see at the end?
본 프로젝트는 다음의 결과물을 목표로 한다:
(1) 기상 변수와 대여량 간의 통계적·시각적 관계 파악,
(2) RandomForest 회귀 모델의 예측 성능 산출,
(3) 변수 중요도 분석을 통한 영향 요인 규명,
(4) 예측값과 실제값의 비교를 통한 모델의 적합성 평가.

II. Datasets

분석에는 UCI Machine Learning Repository의 Bike Sharing Dataset 중 “day.csv”를 사용하였다. 데이터는 2011–2012년 기간의 일별 기록을 포함하며, 총 731개의 관측치로 구성된다.
주요 변수
temp: 정규화된 실온
atemp: 체감온도
hum: 상대습도
windspeed: 풍속
cnt: 총 자전거 대여량(예측 목표 변수)
본 데이터는 기상 조건 변화가 자전거 이용 패턴에 어떻게 반영되는지 분석하기에 충분한 분산과 계절적 변화를 포함하고 있다.

III. Methodology
Algorithm Selection
Codex를 통해 생성된 분석 스크립트는 RandomForestRegressor를 기반으로 하며, 이는 다음과 같은 이유로 적절한 선택이다:
비선형적 관계를 포착하는 데 유리하며,
다수의 결정 트리를 결합하여 예측 안정성을 확보하고,
변수 중요도(feature importance)를 명확히 제시할 수 있다.
따라서 기상 변수의 상대적 영향력 평가와 예측 정확도 확보에 모두 적합하다.

Feature Selection
모델 입력 피처로는 다음 네 가지를 선택하였다.
temp
atemp
hum
windspeed
이는 기상 정보 중 대여량 변화에 실질적 영향력을 가진 항목으로 간주되는 변수들이다.
목표 변수는 cnt로 설정하였다.

Data Split
전체 데이터를 80:20 비율로 훈련·검증 세트로 분리하고, random_state=42를 사용하여 분석의 재현성을 확보하였다.

IV. Evaluation & Analysis
Exploratory Data Analysis (EDA)
데이터 기초 통계, 상위 5개 행, 상관행렬 등을 검토한 결과,
**온도(temp, atemp)**는 대여량과 강한 양의 상관관계를 보였으며,
**습도(hum)**는 일정 수준의 음의 상관을,
**풍속(windspeed)**은 비교적 약한 관계를 나타냈다.
이러한 상관 구조는 기상 변화가 수요 변동에 직접적 영향을 준다는 점을 시사한다.

Model Evaluation
RandomForestRegressor 학습 후 다음 두 지표로 성능을 평가하였다:
MAE: 예측 오차의 평균 절대값
R² score: 종속변수에 대한 설명력
예측값과 실제값의 비교를 통해, 모델이 전반적으로 일별 수요 패턴을 안정적으로 재현함을 확인하였다.

Plots
Temperature vs Rental Count
산점도 분석에서 온도 상승과 대여량 증가 간의 일관된 패턴이 시각적으로 관찰되었다.
Actual vs Predicted
두 값은 전반적으로 y=x 선 주변에 분포하여 모델 적합도를 확인하는 데 유용하였다.

Feature Importance
랜덤포레스트 중요도 분석 결과,
temp, atemp가 가장 높은 기여도를 보였으며,
hum과 windspeed는 상대적으로 낮은 영향을 보였다.
이는 온도 관련 요인이 일별 자전거 수요를 결정하는 핵심 변수임을 강조한다.

V. Related Work

본 연구는 다음 문헌 및 자료를 참고하여 수행되었다:
UCI Machine Learning Repository: Dataset Documentation
Scikit-learn User Guide: RandomForestRegressor 및 평가 지표
Pandas Documentation: 데이터 처리 및 기술 통계
Matplotlib Tutorials: 산점도 및 기타 시각화 기법
이 자료들은 모델 선택·평가 방법론·시각화 접근법을 정립하는 데 참고하였다.

VI. Conclusion: Discussion

본 프로젝트는 기상 요인을 활용하여 자전거 대여량을 예측하는 회귀 모델을 구축하고, 그 성능을 정량적·시각적으로 검증하였다.
RandomForest 기반 분석을 통해 온도 계열 변수의 지배적 영향력, 습도 및 풍속의 보조적 역할, 그리고 예측 가능성의 구조적 특성이 확인되었다.
결과적으로 본 연구는 기상 데이터만을 기반으로 한 수요 예측 모델이 일정 수준의 설명력과 안정성을 확보할 수 있음을 보여준다. 또한 변수 중요도 분석을 통해 수요 결정 요인의 상대적 비중을 명확하게 파악할 수 있었으며, 이는 도시 교통 계획 및 운영 전략 수립 시 참고 자료로 활용될 수 있다.
