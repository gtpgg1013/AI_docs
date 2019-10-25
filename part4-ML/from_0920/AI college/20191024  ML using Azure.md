# 20191024 : ML using Azure

- custom : 직접 만들기
- cognitive : 이미 학습된 모델 API 접근
- autoML
  - 최적 model / hyperparameter 찾기
- => 상세 내용은 pdf 참조
- azure databricks
- azure onnx : framework간의 자유로운 convert
- resources in GROUP
  - 리소스 그룹은 한국에 / 리소스는 미국에 만들 수도 있다



### Hands_On

- 리소스 그룹
- GPU 컴퓨팅 리소스는 따로 만들어서 가벼운 VM에서 스크립트 넘겨주는 방식
  - azureml.core.compute 라이브러리 사용하면 사용 가능!

- ml service 실험 탭에서 다 볼수 있게 만들어놓음!
- 