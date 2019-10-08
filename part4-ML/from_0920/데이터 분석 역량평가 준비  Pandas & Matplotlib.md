## 데이터 분석 역량평가 준비 : Pandas & Matplotlib

### 함수

- groupby
  - unstack : 멀티인덱싱 펴기
  - size : 그룹별 숫자세기
- argsort(axis) : 숫자 큰 순서로 index return
- pivot_table(target, index, columns, aggfunc) : 정리하는 피봇 테이블 만들어줌
- concat(list_df, ignore_index, axis) : list_df : df들 담고있는 list, axis = 0 이면 밑으로, 1이면 옆으로
- reset_index() : index => column
- 

### 토픽



### 팁

- df.groupby() 객체는 iterable하다
  - for year_sex, group in names.groupby(['year','sex']):
        print(year_sex)
  - 이처럼 groupby의 기준이 되는 두 값(year,sex) / 그에 따라 그룹화된 데이터프레임(group)

- 더이상 f, ax = plt.subplots 에 대한 문서를 찾지 말자
  - f, ax = plt.subplots(num_row, num_col, figsize=(10,12))
  - f.tight_layout()
    - for i, name in enumerate(subset.columns):
          sns.lineplot(data=subset, x=subset.index, y=name, ax=ax[i]) #기본
    - for i, name in enumerate(subset.columns):
          subset[name].plot(kind='line', ax=ax[i]) # 이런식으로도 가능 : 종류는 다양하게!
    - np.linspace(0, 1.2, 13) 
    - yticks=np.linspace(0, 1.2, 13), xticks=range(1880, 2020, 10) : 설정 가능