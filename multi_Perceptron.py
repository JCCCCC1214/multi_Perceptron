import tkinter as tk
import math
import random
import numpy as np
import matplotlib.pyplot as plt
import easygui
flag = False
lists = []
trainlist = []
count = 0
trainnumber = 0
testnumber = 0
tempcount = 0
degree = 0
colordot = ['cyan','gray','green','hotpink','blue',
'chocolate','gold']
window = tk.Tk()
var1 = tk.DoubleVar() #訓練正確率
var2 = tk.DoubleVar() #測是正確率
var3 = tk.StringVar() #顯示檔案路徑
var4 = tk.StringVar() #最後鍵結值
var5 = tk.StringVar()
var6 = tk.StringVar()
var7 = tk.DoubleVar()
var3.set("尚未選擇檔案") 
# 設定視窗標題、大小和背景顏色
window.title('多層感知機')
window.geometry('600x500')
window.configure(background='white')


l1 = tk.Label(window, text = "請輸入學習率",font=('Arial', 10),bg = "gray", width = 12, height = 2 )
l1.place(x=10,y=20)
l2 = tk.Label(window, text = "請輸入學習次數",font=('Arial', 10),bg = "gray", width = 12, height = 2 )
l2.place(x=10,y=80)
l3 = tk.Label(window, text = "訓練正確率",font=('Arial', 10),bg = "gray", width = 12, height = 2 )
l3.place(x=10,y=210)
l4 = tk.Label(window, text = "測試正確率",font=('Arial', 10),bg = "gray", width = 12, height = 2 )
l4.place(x=10,y=250)
l5 = tk.Label(window, textvariable=var1,font=('Arial', 10),bg = "yellow", width = 12, height = 2 )
l5.place(x=130,y=210)
l6 = tk.Label(window, textvariable=var2,font=('Arial', 10),bg = "yellow", width = 12, height = 2 )
l6.place(x=130,y=250)
l7 = tk.Label(window, textvariable=var3,font=('Arial', 10),fg = "red",bg = "white",  height = 2 )
l7.place(x=150,y=130)
l8 = tk.Label(window, text = "隱藏層第一個鍵結值",font=('Arial', 10),bg = "gray", width = 20, height = 2 )
l8.place(x=10,y=290)
l9 = tk.Label(window, textvariable=var4,font=('Arial', 10), height = 2 )
l9.place(x=200,y=290)


l12 = tk.Label(window, text = "隱藏層第二個鍵結值",font=('Arial', 10),bg = "gray", width = 20, height = 2 )
l12.place(x=10,y=330)
l10 = tk.Label(window, textvariable=var5,font=('Arial', 10), height = 2 )
l10.place(x=200,y=330)

l13 = tk.Label(window, text = "輸出層鍵結值",font=('Arial', 10),bg = "gray", width = 12, height = 2 )
l13.place(x=10,y=370)
l11 = tk.Label(window, textvariable=var6,font=('Arial', 10), height = 2 )
l11.place(x=130,y=370)

l14 = tk.Label(window, text = "均方根誤差",font=('Arial', 10),bg = "gray", width = 12, height = 2 )
l14.place(x=10,y=410)
l15 = tk.Label(window, textvariable=var7,font=('Arial', 10), height = 2 )
l15.place(x=130,y=410)



e1 = tk.Entry(window, show=None,width = 10)   
e2 = tk.Entry(window, show=None,width = 10)  # 顯示成明文形式

e1.place(x=130,y=30)
e2.place(x=130,y=90)

var = tk.StringVar()
def select_file():

    path = easygui.fileopenbox()
    file = open(path, mode="r")
    var3.set(path)
    global lists,trainlist,count,trainnumber,testnumber,tempcount,flag,degree,colordot
    flag = True
    lists = []
    trainlist = []
    for line in file:
        list = line.split()
        list = ['-1'] + list 
        lists.append(list)
    minn = 10
    maxx = 0
    for i in range(len(lists)):
        if(int(lists[i][3])<minn):
            minn = int(lists[i][3])
        elif(int(lists[i][3])>maxx):
            maxx = int(lists[i][3])
    for i in range(len(lists)):
        lists[i][3] = str((int(lists[i][3])-minn)/(maxx-minn))
    degree = len(lists[0]) - 2
    count = len(lists)
    trainnumber = math.ceil(count * 2 / 3)
    testnumber = count - trainnumber
    tempcount = count-1
    for i in range(0,trainnumber):
        r = random.randint(0,tempcount)
        tempcount -= 1
        trainlist.append(lists[r])
        lists[r:r+1] = []
    
def gogo():
    global lists,trainlist,count,trainnumber,testnumber,tempcount,var1,var2,degree
    weight = [[],[],[]]
    ans = []
    midd = [0,0,0]
    Q = [0,0,0]
    cnt = 0
    correctrate = 0
    correctnumber = 0
    for i in range(3):
        tweight = []
        for j in range(degree+1):
            tweight+=[random.uniform(-1,1)]
        weight[i]+=tweight
    learnrate = float(e1.get())
    times = int(e2.get())
    for i in range(3):
        ans+=[weight[i]]
    Eav = 10
    while times>0:
        index = cnt % trainnumber
        for i in range(2):
            sum = 0
            for j in range(0,degree+1):
                sum += weight[i][j]*float(trainlist[index][j])
            midd[i] = 1/(1+math.exp(-1*sum))
        sum = -1 * weight[2][0]
        for j in range(0,degree):
            sum += weight[2][j+1]*midd[j]
        midd[2] = 1/(1+math.exp(-1*sum))
        Q[2] = (float(trainlist[index][3]) - midd[2]) * midd[2] * (1 - midd[2])
        Q[0] = (midd[0] * (1 - midd[0]) * Q[2] * weight[2][1])
        Q[1] = (midd[1] * (1 - midd[1]) * Q[2] * weight[2][2])
        
        for i in range(2):
            for j in range(3):
                weight[i][j] += learnrate * Q[i] * float(trainlist[index][j])
        for j in range(3):
            if j==0:
                weight[2][j] += learnrate * Q[2] * -1
            else:
                weight[2][j] += learnrate * Q[2] * midd[j-1]
        correctnumber = 0
        E = 0
        for i in range(trainnumber):
            tempa = 0
            tempb = 0
            tempc = 0
            for l in range(3):
                tempa += weight[0][l] * float(trainlist[i][l])
            tempa = 1/(1+math.exp(-1*tempa))
            for l in range(3):
                tempb += weight[1][l] * float(trainlist[i][l])
            tempb = 1/(1+math.exp(-1*tempb))
            tempc = -1 * weight[2][0] + tempa * weight[2][1] + tempb * weight[2][2]
            tempc = 1/(1+math.exp(-1*tempc))
            tempE = 1/2 * (tempc - float(trainlist[i][3])) * (tempc - float(trainlist[i][3]))
            E = E + tempE
            if(float(trainlist[i][3]) == 0 and tempc<0.5):
                correctnumber += 1
            elif(float(trainlist[i][3]) == 1 and tempc>0.5):
                correctnumber += 1
        if(correctnumber/trainnumber > correctrate):
            correctrate = correctnumber/trainnumber
            Eav = E/trainnumber
            for i in range(3):
                ans[i] = weight[i]
        times-=1
        cnt+=1


    plt.subplot(2, 2, 1)
    for i in range(0,trainnumber):
        if(float(trainlist[i][degree+1]) == 1):
            plt.scatter(float(trainlist[i][1]),float(trainlist[i][2]),s=5,color = colordot[int(float(trainlist[i][degree+1]))])
        elif(float(trainlist[i][degree+1]) == 0):
            plt.scatter(float(trainlist[i][1]),float(trainlist[i][2]),s=5,color = colordot[int(float(trainlist[i][degree+1]))])
        else:
            plt.scatter(float(trainlist[i][1]),float(trainlist[i][2]),s=5,color = colordot[int(float(trainlist[i][degree+1]))])
    plt.title("beforetrain")

    plt.subplot(2, 2, 2)
    for i in range(0,trainnumber):
        tempa = 0
        tempb = 0
        tempc = 0
        for l in range(3):
            tempa += ans[0][l] * float(trainlist[i][l])
        tempa = 1/(1+math.exp(-1*tempa))
        for l in range(3):
            tempb += ans[1][l] * float(trainlist[i][l])
        tempb = 1/(1+math.exp(-1*tempb))
        tempc = -1 * ans[2][0] + tempa * ans[2][1] + tempb * ans[2][2]
        tempc = 1/(1+math.exp(-1*tempc))
        if(tempc>0.5):
            plt.scatter(float(trainlist[i][1]),float(trainlist[i][2]),s=5,color = colordot[1])
        elif(tempc<0.5):
            plt.scatter(float(trainlist[i][1]),float(trainlist[i][2]),s=5,color = colordot[0])
    plt.title("latertrain")

    plt.subplot(2, 2, 3)
    for i in range(0,testnumber):
        if(float(lists[i][degree+1]) == 1):
            plt.scatter(float(lists[i][1]),float(lists[i][2]),s=5,color = colordot[int(float(lists[i][degree+1]))])
        elif(float(lists[i][degree+1]) == 0):
            plt.scatter(float(lists[i][1]),float(lists[i][2]),s=5,color = colordot[int(float(lists[i][degree+1]))])
        else:
            plt.scatter(float(lists[i][1]),float(lists[i][2]),s=5,color = colordot[int(float(lists[i][degree+1]))])
    plt.title("beforetest")

    testcorrectnumber = 0
    testcorrectrate = 0
    plt.subplot(2, 2, 4)
    for i in range(0,testnumber):
        tempa = 0
        tempb = 0
        tempc = 0
        for l in range(3):
            tempa += ans[0][l] * float(lists[i][l])
        tempa = 1/(1+math.exp(-1*tempa))
        for l in range(3):
            tempb += ans[1][l] * float(lists[i][l])
        tempb = 1/(1+math.exp(-1*tempb))
        tempc = -1 * ans[2][0] + tempa * ans[2][1] + tempb * ans[2][2]
        tempc = 1/(1+math.exp(-1*tempc))
        if(float(lists[i][3]) == 0 and tempc<0.5):
                testcorrectnumber += 1
        elif(float(lists[i][3]) == 1 and tempc>0.5):
                testcorrectnumber += 1
        if(tempc>0.5):
            plt.scatter(float(lists[i][1]),float(lists[i][2]),s=5,color = colordot[1])
        elif(tempc<0.5):
            plt.scatter(float(lists[i][1]),float(lists[i][2]),s=5,color = colordot[0])
    testcorrectrate = testcorrectnumber/testnumber
    plt.title("latertest")
    var1.set(round(correctrate,5))
    var2.set(round(testcorrectrate,5))
    var7.set(round(Eav,5))
    w = '['
    for i in range(degree+1):
        w += str(round(ans[0][i],5))
        if(i!=degree):
            w+= " , "
    w +="]"
    var4.set(w)
    w = '['
    for i in range(degree+1):
        w += str(round(ans[1][i],5))
        if(i!=degree):
            w+= " , "
    w +="]"
    var5.set(w)
    w = '['
    for i in range(degree+1):
        w += str(round(ans[2][i],5))
        if(i!=degree):
            w+= " , "
    w +="]"
    var6.set(w)
    plt.show()
    

b1 = tk.Button(window, text='請選擇檔案', font=('Arial', 12), width=10, height=1,command=select_file)
b1.place(x=10,y=130)
b2 = tk.Button(window, text='開始訓練', font=('Arial', 12), width=10, height=1,command=gogo)
b2.place(x=80,y=170)



window.mainloop()