import os
for dirName, subDirList, fnames in os.walk('C:/images'): #이 밑에 폴더들 싹다 긁어서 가져옴 (딕셔너리 형식?)
    for fname in fnames:
        if os.path.splitext(fname)[1].upper() == '.GIF': # 확장자 긁어낼 때 : splitext / 디렉터리 네임이랑 파일네임 구분하려면 : 그냥 split
            print(os.path.join(dirName,fname))
            print(fname)