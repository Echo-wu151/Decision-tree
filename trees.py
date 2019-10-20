from math import log
import treePlotter
def calcShannonEnt(dataSet):
    numEntries=len(dataSet)   #获取数据集的长度
    #print(numEntries)
    labelCounts={}            #定义一个空字典
    for featVec in dataSet:
        currentLabel=featVec[-1]  #取出数据集中每一个列表的最后一个元素：‘no’or‘yes’
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel]=0   #对字典进行操作，如果数据标签没有出现在labelcounts中就加进去，如果已出现了就值加1
            #print(labelCounts)
        labelCounts[currentLabel]+=1        #这段的功能是统计每个‘no’和‘yes’在数据集中出现的次数
        #print(labelCounts)
    shannonEnt=0.0
    for key in labelCounts:                 #计算香农熵
        prob=float(labelCounts[key])/numEntries
        shannonEnt-=prob*log(prob,2)
        #print(prob)

    return shannonEnt




def creatDataSet():
    dataSet=[[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]
    labels=['no surfacing','flippers']
    return dataSet,labels

def splitDataSet(dataSet,axis,value):
    retDataSet=[]                       #python传递的是列表的引用，因此要创建一个新的列表
    for featVec in dataSet:
        if featVec[axis]==value:                    #将数据集中与给定特征相匹配的数据抽取出来放在retdataset中
            reduceFeatVec=featVec[:axis]
            reduceFeatVec.extend(featVec[axis+1:])      #这两行代码巧妙的将符合特征值的特征向量结合到一起
            retDataSet.append(reduceFeatVec)            #（以鱼的数据举例：[1,1,'yes']是数据集中的一个数据，
    return retDataSet                                   #前两个元素是特征，如果第一个元素匹配上了，则resetdataset中会出现[1,'yes'],除去了第一个元素

def chooseBestFeatureToSplit(dataSet):                      #计算信息增益，根据信息增益最大的特征值来划分数据集
    numFeatures=len(dataSet[0])-1                           #计算特征数量，最后一项是类别特征所以要减1
    baseEntropy=calcShannonEnt(dataSet)                     #计算数据集的信息熵
    bestInfoGain=0.0
    bestFeature=-1                                          #为避免特征的干扰，设为负数
    for i in range(numFeatures):                            #对每一个特征进行提取（看每个特征包含哪些取值，此处只有0/1两种取值
        featList=[example[i] for example in dataSet]
        #print(featList)
        uniqueVals=set(featList)                            #去掉字典中重复的key，此时只有key
        #print(uniqueVals)
        newEntropy=0.0
        for value in uniqueVals:                            #计算信息增益
            subDataSet=splitDataSet(dataSet,i,value)
            #print(subDataSet)
            prob=len(subDataSet)/float(len(dataSet))
            newEntropy+=prob*calcShannonEnt(subDataSet)
        infoGain=baseEntropy-newEntropy
        if(infoGain>bestInfoGain):                          #找出信息增益最大的特征
            bestInfoGain=infoGain
            bestFeature=i
    return bestFeature

def majorityCnt(classList):                     #投票表决，选出数据集中列别最多的标签
    classCount={}
    for vote in classList:
        if vote not in classCount.key():
            classCount[vote] = 0
        classCount[vote]+=1
    sortedClassCount=sorted(classCount.items(),key=operator.itemgetter(1),reverse=Ture)
    return sortedClassCount[0][0]

def createTree(dataSet,labels):                             #构建递归树，为画递归树做准备
    classList=[example[-1] for example in dataSet]
    if classList.count(classList[0])==len(classList):
        #print(classList[0])
        return classList[0]                             #如果运行到此，则返回一个值不必运行下面的程序
    if len(dataSet[0])==1:
        return majorityCnt(classList)           #这一句的用途是？如果还没划分完，就将其划分为标签数最多的那一类
    bestFeat=chooseBestFeatureToSplit(dataSet)
    bestFeatLabel=labels[bestFeat]
    myTree={bestFeatLabel:{}}                   #下面的mytree如何跟这里的mytree结合起来？最后一次递归会成为上一次递归的值
    #print('this is mytree:',myTree)
    del(labels[bestFeat])
    #print('this is labels:',labels)
    #print('if the dataSet changes:',dataSet)
    featValues=[example[bestFeat] for example in dataSet]
    uniqueVals=set(featValues)
    for value in uniqueVals:
        subLabels=labels[:]
       # print('this is the bestFeat:',bestFeat)
        #print(value)
        #print('this is sublabels:',subLabels)
        #print(splitDataSet(dataSet, bestFeat, value))
        #print('if this is the samw:',dataSet)
        myTree[bestFeatLabel][value]=createTree(splitDataSet(dataSet,bestFeat,value),subLabels) #递归的myTree为啥没有传递到下次递归中？因为函数还没有返回mytree
        #print('this is a new mytree:',myTree)
    return myTree

def classify(inputTree,featLabels,testVec):
    firstStr=list(inputTree.keys())[0]
    secondDict=inputTree[firstStr]
    featIndex=featLabels.index(firstStr)
    for key in secondDict.keys():
        if testVec[featIndex]==key:
            if type(secondDict[key]).__name__=='dict':
                classLabel=classify(secondDict[key],featLabels,testVec)
            else:
                classLabel=secondDict[key]
    return classLabel


def storeTree(inputTree,filename):
    import pickle
    fw=open(filename,'wb')
    pickle.dump(inputTree,fw)
    fw.close()


def grabTree(filename):
    import pickle
    fr=open(filename,'rb')
    return pickle.load(fr)

myDat,labels=creatDataSet()
#print(labels)
#myDat[0][-1]='maybe'
#print(myDat)
#print(calcShannonEnt(myDat))
#print(splitDataSet(myDat,1,1))
#print(splitDataSet(myDat,0,0))
#print(chooseBestFeatureToSplit(myDat))
#myTree=treePlotter.retrieveTree(0)
#print(myTree)
#print(classify(myTree,labels,[1,1]))

#storeTree(myTree,'classifierStoreage.txt')
#print(grabTree('classifierStoreage.txt'))
print(createTree(myDat,labels))