import matplotlib.pyplot as plt
decisionNode=dict(boxstyle="sawtooth",fc="0.8")
leafNode=dict(boxstyle="round4",fc="0.8")
arrow_args=dict(arrowstyle="<-")
def plotNode(nodeTxt,centerPt,parentPt,nodeType):
    createPlot.ax1.annotate(nodeTxt,xy=parentPt,xycoords='axes fraction',xytext=centerPt,textcoords='axes fraction',va="center",ha="center",bbox=nodeType,arrowprops=arrow_args)


def getNumLeafs(myTree):                        #计算叶子节点的个数
    numLeafs=0
    #firstStr=myTree.keys()[0]
    firstStr = list(myTree.keys())[0]            #要强制换成list类型，否则无法索引
    secondDict=myTree[firstStr]                     #由第一个键值得到其对应的值，从此值引入递归得到叶子节点的个数
    for key in secondDict.keys():                   #这一段是整个函数的关键点，判断是否为字典类型，并由此决定是否调用递归
        if type(secondDict[key]).__name__=='dict':
            numLeafs+=getNumLeafs(secondDict[key])
        else:
            numLeafs+=1
    return numLeafs

def getTreeDepth(myTree):                           #计算判断节点的个数，即节点的深度，与叶子节点个数计算函数不同，此处要有两个变量
    maxDepth=0
    #firstStr=myTree.keys()[0]
    firstStr = list(myTree.keys())[0]
    secondDict=myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            thisDepth=1+getTreeDepth(secondDict[key])
        else:
            thisDepth=1                     #此处赋值并不会改变上一次递归时的值
        if thisDepth>maxDepth:
            maxDepth=thisDepth
    return maxDepth                         #maxdpth返回后，下次再递归调用时不会再执行maxdepth这条命令

def retrieveTree(i):
    listOfTree=[{'no surfacing':{0:'no',1:{'flippers':{0:'no',1:'yes'}}}},{'no surfaing':{0:'no',1:{'flippers':{0:{'head':{0:'no',1:'yes'}},1:'no'}}}}]
    return listOfTree[i]

def plotMidText(cntrPt,parentPt,txtString):
    xMid=(parentPt[0]-cntrPt[0])/2.0+cntrPt[0]
    yMid=(parentPt[1]-cntrPt[1])/2.0+cntrPt[1]
    createPlot.ax1.text(xMid,yMid,txtString)

def plotTree(myTree,parentPt,nodeTxt):              #parentPt为指向文本的点，nodeTxt为要显示的文本
    numLeafs=getNumLeafs(myTree)
    depth=getTreeDepth(myTree)
    firstStr=list(myTree.keys())[0]
    cntrPt=(plotTree.xOff+(1.0+float(numLeafs))/2.0/plotTree.totalW,plotTree.yOff)    #cntrPt为文本的中心点
    plotMidText(cntrPt,parentPt,nodeTxt)
    plotNode(firstStr,cntrPt,parentPt,decisionNode)
    secondDict=myTree[firstStr]
    plotTree.yOff=plotTree.yOff-1.0/plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            plotTree(secondDict[key],cntrPt,str(key))
        else:
            plotTree.xOff=plotTree.xOff+1.0/plotTree.totalW
            plotNode(secondDict[key],(plotTree.xOff,plotTree.yOff),cntrPt,leafNode)
            plotMidText((plotTree.xOff,plotTree.yOff),cntrPt,str(key))
    plotTree.yOff=plotTree.yOff+1.0/plotTree.totalD


def createPlot(inTree):
    fig=plt.figure(1,facecolor='white')
    fig.clf()
    #x=range(0,10,1)
    #y=range(0,10,1)
    axprops=dict(xticks=(),yticks=())
    createPlot.ax1=plt.subplot(111,frameon=False,**axprops)
    plotTree.totalW=float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff=-0.5/plotTree.totalW
    plotTree.yOff=1.0
    plotTree(inTree,(0.5,1.0),'')
    #plotNode(U'decisionnode',(0.5,0.1),(0.1,0.5),decisionNode)
    #plotNode(U'leafnode',(0.8,0.1),(0.3,0.8),leafNode)
    plt.show()



#print(createPlot())
#print(retrieveTree(1))
#print(retrieveTree(0))
#print(getTreeDepth(retrieveTree(0)))
#print(getTreeDepth(retrieveTree(1)))
#print(getNumLeafs(retrieveTree(0)))
#print(getNumLeafs(retrieveTree(1)))

myTree=retrieveTree(0)
myTree['no surfacing'][3]='maybe'

print(createPlot(myTree))