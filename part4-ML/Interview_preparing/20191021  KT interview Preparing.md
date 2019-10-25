# 2019/10/21 : KT interview Preparing

### 1. 자소서 기반 준비

- data에 대한 나의 태도
- 끊임없는 공부 - spark study에서 얻은 것 / 배운 것 / 느낀 것



- 최고 목표의 지향 : 자소서 상에서는 tensorflow를 사용한 CNN 모델 정확도를 상승시킨 방법 설명
  
  - inceptionNet / ResNet을 텐서플로에서 직접 구현 => keras에서 더 쉽게 layer들을 구현도 가능
  
  - 여기서 얻은 지식들을 실제로 사용하고 싶어, PPT라는 프로젝트를 계획, 실행함.
  
    - PPT : personal presentation trainer의 약자
    - 혼자서 발표연습을 가능케 하고, 이에 대한 피드백을 주는 서비스!
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
      - Feature Preprocessing / EDA / Validation / Data Leak / Metrics Optimization
      - Feature Engineering / Hyperparameter Optimization / Ensemble
      - Kaggle study는 5주간 Coursera 강의를 듣고 서로 피드백하며 기초를 쌓음
      - 그 이후에 스터디 내부에서 팀을 이뤄 competiton에 참여할 예정
      - 최근 elice에서 주최한 data challenge에 참여하여 10위 수상



- '서울 테마카페 맵' : MVC pattern으로 JAVA 를 활용하여 웹 서비스 구축
  - DAO / VO class를 만들고 드라이버를 활용한 커넥션 구축
  - R을 이용한 데이터 선 처리 분석 후 데이터를 보여주는 사이트 구축



- '공동의 목표 달성을 위한 협업' : 에 대한 경험 => '서울 테마카페 앱'이 꽤나 예전 경험이다!
  - 가장 최근에 했던 경험 => 은 PPT!
  - 아이디어 제안 : 발표가 중요해지는 현대 사회, 그러나 현대인의 삶은 더 바빠지기 때문에 혼자서도 나의 발표를 간단하게 평가하고 피드백 받을 수 있으면 좋겠다!
  - 기본 로직 제안
    - 동영상을 일정 텀을 두고 스냅샷을 찍은 다음, 각 스냅샷에 대해 Pose Estimation과 Face Emotion Recognition을 한다.
    - 각 snapshot에 대해 feedback을 제공한다
    - **전체 snapshot의 데이터들을 통계적으로 분석하여 피드백을 제공**
      - 각 랜드마크의 이동 분포가 너무 작다 : 각 부위의 움직임이 너무 적다 : 적극적인 제스처 제안
      - eye detection 횟수 / snapshot 수 : 얼마나 정면을 발표자가 바라보며 하였는가 등
  - GCP에 개발 환경을 마련하여(GPU가 부착된 VM을 할당), 딥 러닝 알고리즘을 수행할 수 있는 환경을 구축하였음 (CUDA, cuDNN)
  - Django 웹 서버와 연동하기 위해 venv를 활용한 가상 환경 구성 : keras / tensorflow inferrencing / Django Framework 개발 환경과의 conflict 방지
  - OpenCV, OpenPose를 활용한 Human Pose Estimation landmark 좌표값 얻음
  - Pose 데이터(좌표)를 자체 알고리즘을 활용하여 자세가 올바른 presentation과 적합하지 않다면 각 지표에 대해 조언을 주게 설계
    - 너무 눈을 스크린 쪽만 바라보고 있다 : 청중을 덜 응시하고 있다
    - 허리가 너무 굽어있다
    - 손을 주머니에 꽂고 발표하고 있다
  - Kaggle Face Emotion Data를 활용하여 얼굴 표정을 분류하는 모델 학습
    - ResNet51 아키텍쳐로 학습, val acc 기준 55% 달성
    - positive / negative / neutral 3가지 분류로 나누어서 통계적으로 분석, 피드백 제공



### 2. 지원 동기

- 데이터 사이언티스트 업무를 수행하며, 데이터 분석과 모델링을 하며 고객에게 가치 있는 일을 하며, 한편으로는 기술적으로 성장하는 것이 제 목표입니다. 이같은 높은 성취를 위해서 데이터 분석 직무 담당자에게 가장 중요한 요소는 '데이터를 계속 씹어 먹을 수 있는 끈기'입니다.

- 최근 AI의 트렌드가 딥러닝 분야로 넘어가면서, 많은 사람들이 딥러닝 모델들이 세상의 모든 문제들을 간단히 해결시켜 줄 일종의 마법 상자로 생각합니다.

- 그것은 큰 오산입니다. 데이터에 대한 직접적인 이해와 한 발자국 더 나아가 도메인 지식을 활용한 깊이 있는 분석이 이루어지지 않는다면, 예측을 위한 모델은 제대로 작동하지 않을 것입니다. 심지어 작동하더라도 데이터를 실제적으로 통찰하지 못했기 때문에 또 다른 문제가 발생할 것입니다.

- 이를 위해서 데이터 분석은 끊임없이 이루어져야 합니다. 말 그대로 데이터를 계속하여 분석하고, 시각화하여 납득할 수 있는 결과를 가져와야 할 것입니다.

- 그러나 이 과정은 그리 유쾌하지만은 않습니다. 지루한 반복의 연속일 때가 많습니다.

- 하지만, 반복적이고 때로는 쉽지 않은 분석을 거쳐 나온 하나의 통찰은 그 값어치를 합니다. 그리고 그 짜릿함이 저를 데이터 분석에서 빠져나오지 못하게 합니다. 이러한 반복을 즐길 줄 아는 것, 그러한 데이터 과학자로 회사에 기여하고 성장하고 싶습니다.

  

### 3. 내가 이 곳에서 공헌할 수 있는 부분

- 다양한 프레임워크, 언어 사용

  - Django, Flask, MVC pattern의 웹 서비스 개발

  - Python, Java

    

- 다양한 AI 분야의 경험으로 실제 프로젝트에 언제든 뛰어 들 준비가 되어 있음

  - 이미지 : OpenPose / OpenCV / Conv Network 설계 경험

    - PPT
    - python Tkinter GUI를 사용한 직접 영상처리 프로그램 제작
    - Image classification kaggle competition 참여
    - 심화 :  explainable AI에 관심이 생겨 AI college의 XAI 과정을 신청하여 현재 참여 중

  - Sequential Data(Text) : 

    - 자연어 처리의 기본 개념 및 구성요소를 익혔으며, 알고리즘을 구현하였습니다.
      - BOW / Ngram을 활용한 Naive Baysian spam filter
      - Word2Vec를 활용한 워드 임베딩
    - kears, TF를 이용한 sequential data processing에 관심이 생겨 기초 모델부터 최신 논문 base 모델까지 구현중입니다.
    - LSTM 모델을 활용한 기계번역
    - Seq2Seq (with Attention)  : 문체를 따라하는 모델 훈련 (현대어 => 성경)
    - Transformer

  - 정형 데이터 : 

    - Kaggle competition tutorial
      - titanic, house prising, cat & dpg classification
    - Alice data challenge competition 참여 : 10위
      - 데이터 전처리 / 분석 / 머신 러닝 알고리즘 사용
    - 현재 Kaggle study를 수강하며 체계적으로 개념부터 다시 정리중

  - 강화학습

    - OpenAI gym을 설치하여 frozenlake 실습

    - Q-learning 개념을 이해하고 이를 DQN으로 발전시켜 학습시켜 보았음

    - 깊게는 아니지만, 강화학습의 기본 개념을 이해함 => DP

      

- 다양한 스터디, 외부활동, 교육으로 운신의 폭을 넓힘

  - slowpaper
    - 매주 토요일마다 모여 한 편의 딥러닝 논문을 같이 읽는 스터디입니다. 남이 해석해 놓은 논문 내용이 아니라 직접 3시간 동안 논문을 낑낑대며 읽어보며, 제 힘으로 논문을 읽는 법을 깨달았습니다.
  - Apache Spark를 통한 대용량 데이터 처리와 스파크 내부 이해
    - 대용량 데이터 처리를 위한 프레임워크인 Spark를 공부했습니다. 이전까지는 Spark가 단순히 빅 데이터를 처리하는 블랙박스 같은 DB 느낌이었다면, 현재는 원리를 조금 더 생각하여 데이터 분석 파이프라인 최적화를 위해 어떤 쿼리를 사용할 지 고민하는 습관을 얻게 되었습니다.
  - Kaggle
    - Coursera 강의를 듣고, 팀을 구성해 Kaggle Competition에 도전하는 스터디입니다.
  - Deeplab 논문반
    - 매 주 월요일 두개의 논문을 세미나 형식으로 발표합니다. 최신 트렌드의 논문에 대한 정보를 얻을 수 있는 시간입니다.



- [sw/가지] [오후 6:15] 문제 풀이가 2개고
  [sw/가지] [오후 6:15] 하나는 대기중에 문제지로 푸는 4문제
  [sw/가지] [오후 6:15] 하나는 개인pt로 5문제
  [sw/가지] [오후 6:15] 개인pt끝나고 자소서질문
  [sw/가지] [오후 6:15] 이거 아닌가요?