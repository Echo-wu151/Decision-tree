import treePlotter
import trees
fr=open('car traning2.txt')
#lenses=[inst.strip().split('\t') for inst in fr.readline()]     #此处不能使用readline，否则返回的数据只有一行且分割为单个字母
car=[inst.strip().split(',') for inst in fr.readlines()]
#print(car)
carLabels=['buying','maint','doors','persons','lug_boot','safety']
carLabels1=['buying','maint','doors','persons','lug_boot','safety']
carTree=trees.createTree(car,carLabels)                    #必须要带上tree才不会报错
#print(carTree)
#treePlotter.createPlot(carTree)

def classify(inputTree,featLabels,testVec):
    classLabel=''                          #此处如果不加这段代码时就会报以下错误
                                            # UnboundLocalError: local variable 'classLabel' referenced before assignment
    #global classLabel                      #如果加上这个代码会报以下错误SyntaxError: name 'classLabel' is assigned to before global declaration
                                            #另外如果将此代码运行，classLabel=''代码屏蔽，则会出现不正确的运行结果或者出现classLael没有定义
    firstStr=list(inputTree.keys())[0]
    #print('this is the firstStr:',inputTree.keys())
    secondDict=inputTree[firstStr]
    #print('this is the seconddict:',secondDict)
    featIndex=featLabels.index(firstStr)
    #print('this is the featindex:',featIndex)
    for key in secondDict.keys():
        if testVec[featIndex]==key:
            if type(secondDict[key]).__name__=='dict':
                classLabel=classify(secondDict[key],featLabels,testVec)
            else:
                classLabel=secondDict[key]
                #print('this is the classLabel:',classLabel)
    return classLabel




def testacuccy(inputTree,featLabel,testdataset):
    testdatasetnum=len(testdataset)
    print(testdatasetnum)
    rightnum=0
    for i in range(testdatasetnum):
        testdatasetvec=testdataset[i][:-1]
        testresult=classify(inputTree,featLabel,testdatasetvec)
        if testresult==testdataset[i][-1]:
            rightnum+=1
    print(rightnum)
    accuracy=float(rightnum/testdatasetnum)
    return accuracy


frtest=open('car2.txt')                                         #数据一定要保证标点符号符合规范，且最后不能有空行，否则会出现空列表导致运行出错
#lenses=[inst.strip().split('\t') for inst in fr.readline()]     #此处不能使用readline，否则返回的数据只有一行且分割为单个字母
cartest=[inst.strip().split(',') for inst in frtest.readlines()]   #正确率只有22%，初步分析结果应该是训练数据不全导致决策树不够全面，因此如何分析数据
                                                                    #选择恰当的数据进行训练尤为重要，将训练数据换成car traning2后准确率提升到了57%
                                                                    #将训练数据增加到93个后发现准确率较第二次反而降低了差不多一个百分点

fineltestresult=testacuccy(carTree,carLabels1,cartest)
print(fineltestresult)