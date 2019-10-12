## 데이터 분석 역량평가 준비 : Pandas & Matplotlib

### 함수

- groupby
  - unstack : 멀티인덱싱 펴기
  - size : 그룹별 숫자세기
- argsort(axis) : 숫자 큰 순서로 index return
- pivot_table(target, index, columns, aggfunc) : 정리하는 피봇 테이블 만들어줌
- concat(list_df, ignore_index, axis) : list_df : df들 담고있는 list, axis = 0 이면 밑으로, 1이면 옆으로
- reset_index() : index => column
- mean, sum, count 등 기술통계값 => skipNa=True가 기본
- merge(df1, df2, on, how, left_on, right_on,suffixes,left_index,right_index) : default is inner join
- concat([list of dfs], axis) => axis=0 : row별 연산 / axis=1 :  column별 연산 
- DF, series만들 때 index=pd.date_range('1/1/2000', periods=1000) : 날짜가 index로 들어간 자료생성

### 토픽

- map VS apply VS applymap

  - map

    Series에만 사용할 수 있는 함수 : 컬럼의 데이터를 하나씩 꺼내서 특정 function을 반복 적용할 때 사용 

  - apply

    커스텀 함수를 사용하기 위해 DF에서 복수개의 컬럼이 필요할 때 사용

    axis = 0 : row를 merge / axis = 1 : column을 merge

  - applymap : 그냥 elementwise하게 함수를 적용시 사용

  - index값을 apply에 쓰고싶을 때 : apply에 쓸 때는 df.name을 불러와서 사용해야 함



### 팁

- DataFrame의 정의 자체 : 사실은 공통 인덱스를 가지는 열 시리즈(Column Series)를 딕셔너리로 묶어놓은 것일 뿐이다. 

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

- axis = 0 : row를 따라 / axis = 1 : col을 따라