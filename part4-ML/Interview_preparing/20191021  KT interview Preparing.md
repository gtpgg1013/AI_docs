# 2019/10/21 : KT interview Preparing

### 1. 자소서 기반 준비

- data에 대한 나의 태도
- 끊임없는 공부 - spark study에서 얻은 것 / 배운 것 / 느낀 것



- 최고 목표의 지향 : 자소서 상에서는 tensorflow를 사용한 CNN 모델 정확도를 상승시킨 방법 설명
  
  - inceptionNet / ResNet을 텐서플로에서 직접 구현 => keras에서 더 쉽게 layer들을 구현도 가능
  
  - 여기서 얻은 지식들을 실제로 사용하고 싶어, PPT라는 프로젝트를 계획, 실행함.
  
    - PPT : personal presentation trainer의 약자로, 발표가 점점더 중요해지는 가운데, 만약 나의 발표를 봐 줄 사람이 없다면 피드백을 받기가 어렵다!
    - OpenPose라는 opensource를 사용하여, 사람의 pose를 estimation함 => 사람의 포즈의 landmark의 좌표들을 이용하여 자체 알고리즘으로 평가, 피드백
    - ResNet을 사용하여 Kaggle Data를 이용하여 Facial Emotion Estimator model을 학습시킴
    - Django를 이용하여 GCP 상에서 Deploy함 : deep learning algorithm inferencing을 빠르게 하기 위해, CUDA, cuDNN 프레임워크를 빌드하여 사용함
  
  - 또한 현재 AI college에서 Explainable AI 과정에 참여 => 현재 최신 논문들을 읽으면서 '해석 가능한 모델을 만드는 법'을 더 깊게 공부중
  
    - 해석 가능한 모델 : 어떤 부분을 보고 모델이 이러한 결과를 내 놓았는가?
  
    - 안전성 확보와 모델 해석력 상승 (이게 없다면 그저 trial-error의 연속이 될 수밖에 없다!)
  
      

- 위 문서를 작성한 시기 / 프로젝트를 수행한 시기는 조금 예전이었다

  - 최근에는 sequential data에 관심이 많아져서 sequential model / transformer 모델 구현을 공부중이다.
  - 아직 완벽하고 자유롭게 개념을 구현할 정도는 아니기 때문에, 최신 논문들과 오픈소스 코드들을 보며 공부중임
    - Bert와 ko-Bert 등을 잘 이용하면 더 좋은 모델을 만들어 낼 수 있을것이라 생각함
  - 그 가장 첫번째 도전으로 attention mechanism을 사용한 seq2seq model을 기반으로 '성경의 문체를 따라하는 모델'을 학습시킴
    - 자연어 처리 관련 모델을 사용함에 있어서 전처리가 얼마나 중요한지 다시 한번 깨닫게 되었음
    - 성능이 그렇게 나쁘지는 않았으나, 결국 더 잘 하기 위해서는 '문맥'을 더 잘 파악할 수 있는 self-attention 개념을 사용한 transformer model의 구현이 필연적이라고 생각함

  

- 최고 어려웠던 도전 : 빅 콘테스트
  - 챔피언 리그 : 리니지 게임 데이터를 이용해 이탈 유저와 평균 결제액을 예측하는 프로젝트를 진행
  - EDA 및 Feature Engineering
    - 전투 / 지출 / 혈맹 / 거래 / 활동 등으로 나누어져 있는 테이블을 하나로 합침
    - Null data는 implementation 함 id별 average / group별 average 등 기준
    - EDA를 하던 도중 : 40000명의 data 중 오직 0.065%의 사람이 매출의 11%를 차지하고 있음!
      - 모델을 구축할 때 타겟 레이블의 편향이 매우 큼을 인지함
    - knn, kmeans 머신러닝 혹은 평균, 중간값 등으로 NaN을 보간함
    - 데이터의 feature를 하나하나 시각화하여 특성을 분석하려고 노력함
    - 모델링 (LSTM)에 너무 집중하여 실제 더 중요한 데이터를 더 등한시했다
    - 정형 데이터 컴페티션에는 사실 부스팅 계열의 머신러닝 알고리즘이 더 강력한 경우가 많다
  - 이 대회에서 체계적인 지식이 부족함을 느낌
    - 그러나 이 대회에서의 경험을 바탕으로 elice 데이터 챌린지에서 10위를 달성
      - 4가지의 머신러닝 문제를 푸는 대회였음 : 정형 데이터 
    - 앞으로 정형 데이터에 더욱 분석을 더욱 완벽하게 하고 싶어서 Kaggle study에 참여중!
      - Kaggle study는 5주간 Coursera 강의를 듣고 서로 피드백하며 기초를 쌓음
      - 그 이후에 스터디 내부에서 팀을 이뤄 competiton에 참여할 예정
      - 최근 elice에서 주최한 data challenge에 참여하여 10위 수상



- 



### 2. 지원 동기



### 3. 내가 이 곳에서 공헌할 수 있는 부분