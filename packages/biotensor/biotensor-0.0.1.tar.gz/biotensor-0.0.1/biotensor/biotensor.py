#数据读取
##需求：
##   读取用户的输入
from __future__ import unicode_literals, print_function, division
from io import open
import glob
import os
def findFiles(path): return glob.glob(path)
def readLines(filename):
    lines = open(filename).read().strip().split('\n')
    return [line.upper() for line in lines]

n_flag = 1
for filename in findFiles('*.bed'):
    cmd = "bedtools getfasta -fi hg19.fa -bed " + filename + " > " + str(n_flag) + ".fa "
    os.system(cmd)
    cmd = "mv "+ str(n_flag) + ".fa "+ str(n_flag) +".input"
    os.system(cmd)
    n_flag = n_flag + 1

category_lines = {}#每个标签内部的序列
all_categories = []
for filename in findFiles('*.input'):
    category = os.path.splitext(os.path.basename(filename))[0]
    all_categories.append(category)
    lines = readLines(filename)
    category_lines[category] = lines
n_categories = len(all_categories)

#数据编码
##需求： 
## 实现输入序列，输出张量
import torch
all_letters="ATCGN"##生物编码由A，T，C，G四个碱基组成，有时不确定是atcg中的哪个，就用N表示
n_letters = 5##总共有几种碱基，等于len(all_letters)

def letterToIndex(letter):
    return all_letters.find(letter)

def letterToTensor(letter):
    tensor = torch.zeros(1, n_letters)
    tensor[0][letterToIndex(letter)] = 1
    return tensor

def lineToTensor(line):
    #turn a sequcence to a tensor
    #size [seq_length,1,base(include N)]
    tensor = torch.zeros(len(line), 1, n_letters)
    for li, letter in enumerate(line):
        tensor[li][0][letterToIndex(letter)] = 1
    return tensor
##编码示例
print(lineToTensor("ATCGATCCGAC"))

#数据集合划分
##需求: 
#1. 划分训练集和测试集
#3. 设定每次训练输入的样本量
import random

random_k = 0
random_k = input("请输入划分比例（0～100）：")
while (int(random_k) < 0 or int(random_k) > 100):
    print ("非法输入！")
    random_k = input("请输入划分比例（0～100）：")
    
def randomChoice(l):
    return l[random.randint(0, len(l) - 1)]

def randomTrainingExample():
    category = randomChoice(all_categories)
    line = randomChoice(category_lines[category])
    category_tensor = torch.tensor([all_categories.index(category)], dtype=torch.long)
    line_tensor = lineToTensor(line)
    return category, line, category_tensor, line_tensor

for i in range(10):
    category, line, category_tensor, line_tensor = randomTrainingExample()
    #print('category =', category, '/ line =', line)
