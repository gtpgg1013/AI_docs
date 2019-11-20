# Setting VM for DL in GCP

- nvidia-docker 환경 설치 :  https://deepmi.me/linux/18791/ 
- 
- locale 설정
  - sudo apt-get install language-pack-ko
    sudo locale-gen ko_KR.UTF-8
  - pip
    - sudo apt-get update
      sudo apt-get install python3-pip -y



- Making VM with VGA
- install CUDA : including nvidia driver while installing
- https://cloud.google.com/compute/docs/gpus/add-gpus?hl=ko#install-driver-script
- following above script : ubuntu 18.04 LTS with CUDA 10.0



- password change : sudo passwd [username]



- Install ubuntu-desktop : GUI for RDP networking
- https://evols-atirev.tistory.com/27
- following above script



- Install cuDNN : Follow below link
- install files through web browser : https://developer.nvidia.com/rdp/cudnn-download

- https://red-pulse.tistory.com/226 : follow commands

- finish to install cuDNN



- Python library install
- [https://jeinalog.tistory.com/entry/GCP-%EB%94%A5%EB%9F%AC%EB%8B%9D%EC%9D%84-%EC%9C%84%ED%95%9C-VM-%EC%9D%B8%EC%8A%A4%ED%84%B4%EC%8A%A4-%EA%B5%AC%EC%84%B1-feat-GPU](https://jeinalog.tistory.com/entry/GCP-딥러닝을-위한-VM-인스턴스-구성-feat-GPU)



- Openpose
  - https://github.com/CMU-Perceptual-Computing-Lab/openpose/tree/master : main git
  - https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation.md#prerequisites : read installation : install prerequisites
  - 현재 cmake 버전 업그레이드 후 컴파일 하려 했더니 제대로 되지 않음
  - 다음에 하자



- Install Dlib library : https://www.pyimagesearch.com/2018/01/22/install-dlib-easy-complete-guide/

