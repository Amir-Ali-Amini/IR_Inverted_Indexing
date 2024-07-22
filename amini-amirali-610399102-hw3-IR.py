# %% [markdown]
# # Implementing the BSBI Algorithm for Inverted Indexing
# 
# ## AmirAli Amini - 610399102
# 
# #### HW3
# 
# 

# %% [markdown]
# # توضیحات مسئله و چالش ها و بهبود ها
# 
# بزرگ ترین چالش این مسئله مرج کردن ساب پستینگ لیست ها و تبدیل ایندکس ها به گاما کد بود.
# برای این منظور (گاما کد) تابعی نوشتم که یک عدد را به یک گاما کد تبدیل میکند و برعکس
# 
# همچنین تابعی نوشتم که یک لیست از اعداد گرفته و یک مقدار برای مقایسه، سپس لیست فاصله اولین عضو از مقدار مقایسه و سپس اختلاف هر عضو را با عوض قبل در ایندکس آن خانه قرار میدهد (از اخر لیست به سمت اول لیست این کار را انجام میدهد)
# 
# اخرین عدد(داکیومنت) دیده شده در پستینگ لیست مرج شده در هر مرحله برای هر کلمه را نیز ذخیره میکنم که به عنوان عدد مقایسه داکیومنت های بعدی قرار گیرند

# %% [markdown]
# ## کتابخانه ها 
# 
# ###  from nltk import word_tokenize :
# از این کتابخانه برای تکنایز کردن داده ها به این دلیل که توکنایز کردن دیتا سریع تر میشه استفاده کردم
# 
# ###  from nltk.corpus import stopwords :
# از این کتابخانه برای دریافت استاپینگ ورد های زبان انگلیسی استفاده کردم
# 
# ###  import string:
# از این کتابخانه برای دریافت پانچویشن های زبان انگلیسی استفاده کردم
# 
# ###  import numpy as np:
# از این کتابخانه برای جمع یک عدد با تمام اعضای یک آرایه استفاده کردم
# 
# ###  import copy:
# از این کتابخانه برای دیپ کپی کردن ارایه استفاده کردم
# 
# 
# ### import pickle 
# از ای کتابخانه برای سیو کردن دیکشنری ها در فایل استفاده میکنم (همچنین برای خواندن آنها)
# ### import shutil
# از این تابع برای حذف فولدر موجود استفاده میکنم (که بتونم دوباره بسازمش)

# %%
from nltk.tokenize import word_tokenize


from nltk.corpus import stopwords # a library to tokenize input texts

import nltk


nltk.download('punkt')
nltk.download('stopwords') # stopping word in English language

import string # using to remove punctuation

import numpy as np

import copy

import os

import pickle 
import shutil


# %%


# %% [markdown]
# ### searchEngine:
# مکان وجود یا اد شدن یک کلمه را در پستینگ لیست ورودی پیدا میکند
# 
# ### addToPostingList:
# کلمه را در پستینگ لیست ورودی اد کرده و در صورت وجود کلمه داکیومنت اندکس های آن را اپدیت میکند
# 
# ### input:
# اصلی ترین فانکشنم فک میکنم همین باشه
# 
# داخل این فانکشن داکیومن ها به ترتیب خونده میشن
# 
# هر داکیومنت که خونده میشه توکنایز میشه و چیزایی که باید ازش حذف بشن حذف میشن
# 
# برای هر پنج تا داکیومنت پشت سر هم یه پستینگ لیست ساخته میشه که بعدش پستینگ لیست پنج تایی داخل یه فایل ذخیره میشه
# 
# ### mergePostingLists:
# این تابع پستینگ لیست ها را از فایل ها مرتبط میخواند و در هنگام مرج کردن آنها با پستینگ لیست اصلی گاما کد مربوطه را نیز میسازد

# %%

class searchEngine:
    def __init__(self , debug = False,tempDirectory="postingList") -> None: # constructor of class
        self.debug = debug
        # self.subPostingLists=[
        self.codedPostingLit=[] # gama coding posting list
        self.tempDirectory=tempDirectory
        self.stop = set(stopwords.words('english') + list(string.punctuation)) # all extra expression which should ignore

        # structure of codedPostingLit : list of {word : nameOfWord , docs :gamaCode of including docs}


    # Binary search to find a word in the posting list.

    #     Parameters:
    #     - word: The word to search for.
    #     - postingList: The posting list to search in.

    #     Returns:
    #     - Index of the word in the posting list.
    def searchPostingList(self, word,postingList): # this function changed to search on input posting list
        s= 0 
        e = len(postingList)
        if e <=0 :
            return 0
        e-=1
        while (1):
            if (e-s < 2):
                if (postingList[e]["word"] < word):
                    return e+1
                if (postingList[e]["word"] == word):
                    return e
                if (postingList[s]["word"] >= word):
                    return s

                return e
            mid = (s+e)/2
            mid = int(mid)
            if (word<postingList[mid]["word"]):
                e=mid
            elif (word> postingList[mid]["word"]):
                s = mid
            else :
                return mid
            
        # {word:str, indexes:list(int)}
    # binary search to find a word in each dictionary

    #---------------------------------------------------------------------------------------------------------------------

    # Add tokenized words to the posting list.

    #     Parameters:
    #     - tokenizedText: List of tokenized words.
    #     - docIndex: Index of the document.
    #     - postingList: The posting list to add the words to.
    # this function changed to add on input subPosting list
    def addToPostingList(self, tokenizedText: list[str],docIndex:int,postingList=[]): # add tokenized word in posting list 
        for i in range(len(tokenizedText)):
            word = tokenizedText[i]
            index = self.searchPostingList(word,postingList=postingList) # find index of word in posting list
            if (len(postingList)>index): # check if index is not larger than posting list (if word is bigger that all words, search function returns len(postingList)+1)
                if (postingList[index]["word"] == word): # check if index is the index of the word
                    if (postingList[index]["docs"][-1]["doc"] == docIndex): # if we have already added the document index 
                        postingList[index]["docs"][-1]["indexes"].append(i) # as we read tokens in order of their index, we need to add token in end of the list

                    else:
                        postingList[index]["docs"].append({"doc":docIndex,"indexes":[i] }) # if we have not already added the document and dou to the fact that they are read in order of their index, we can easily add append new one in end of the list 

                else :
                    postingList[index:index]= [({"word":word , "docs":[{"doc":docIndex , "indexes":[i]}]})] # word is bigger that all other words => we can append it to end of the list

            else :
                postingList.append({"word":word , "docs":[{"doc":docIndex , "indexes":[i]}]}) # we have not already added the word and dou to the fact that they are read in order of their index, we can easily add append new one in end of the list




    #---------------------------------------------------------------------------------------------------------------------


    # Process input files, tokenize text, and create posting lists.

    #     Parameters:
    #     - filePath: List of file paths.

    # this function changed to save make subPosting lists and save then on file
    def input (self, filePath: list[str]): # input paths of inputs
        tempPostingList=[]
        if(os.path.exists(self.tempDirectory)):
            shutil.rmtree(self.tempDirectory)
        os.mkdir(self.tempDirectory)
        saved=False
        for i in range(len(filePath)): # for files in input
            
            if i%5==0:
                if (i>0):
                    # self.subPostingLists.append(copy.deepcopy(tempPostingList))
                    # print(tempPostingList)
                    saved=True
                    with open(f'{self.tempDirectory}/saved_postingList{int(i/5)-1}.pkl', 'wb') as f: # save subPostingList on a file
                        pickle.dump(tempPostingList, f)
                tempPostingList=[]
            saved = False
            file = open(filePath[i],'r',encoding='cp1252') # open the file
            text = file.read() # read the file
            file.close()  # close the file
            # tokenize text and ignore stopping words using nltk library 
            tokenizedText = [word for word in word_tokenize(text.lower(),preserve_line=False) if word not in self.stop] 
            print (f'document {i+1} : {filePath[i]}')
            # print(tokenizedText)
            self.addToPostingList(tokenizedText , i+1 ,tempPostingList) # i indicates to index of document we are reading
        if (not saved):
            # self.subPostingLists.append(copy.deepcopy(tempPostingList))
            with open(f'{self.tempDirectory}/saved_postingList{int((len(filePath)-1)/5)}.pkl', 'wb') as f:
                pickle.dump(tempPostingList, f)
            tempPostingList=[]
        
    #---------------------------------------------------------------------------------------------------------------------

    # Convert a number to Gamma code.

    #     Parameters:
    #     - n: The number to convert.

    #     Returns:
    #     - Gamma code representation of the number.


    # in this function I make gamma code of a number
    def numberToGamaCode(self, n):  # new function for homework 3
        binaryNumber = bin(n)[2:]
        ans = ""
        for _ in range (len(binaryNumber)):
            ans+="1"
        ans+="0"+binaryNumber[1:]
        return ans
    

    #---------------------------------------------------------------------------------------------------------------------

    # Convert a list to Gamma code based on the distance of elements.

    #     Parameters:
    #     - ls: The list to convert.
    #     - startingIndex: Starting index for creating a suitable gamma code .

    #     Returns:
    #     - Gamma code representation of the list.

    # in this function I make gamma code of a list base of the distance of elements
    # startingIndex is used to make a posting list that can be merged with last one in a token(it is used to merge subPosting lists)
    def listToGamaCode(self, ls , startingIndex = 0):  # new function for homework 3
        temp = ""
        s = startingIndex
        for item in ls:
            temp+=self.numberToGamaCode(item-s)
            s = item
        return temp
    



    #---------------------------------------------------------------------------------------------------------------------


    # Convert Gamma code to a number.

    #     Parameters:
    #     - gamaCode: The Gamma code to convert.

    #     Returns:
    #     - The decoded number.
    
    # in this function I make number of a gamma code
    def gamaCodeToNumber(self,gamaCode):
        oneCounter=0
        for i in gamaCode:
            if i == '1':
                oneCounter+=1
            else: break
        if oneCounter==1:return 1
        return int("1"+gamaCode[oneCounter+1:],2)
        
    #---------------------------------------------------------------------------------------------------------------------


    # Convert Gamma code to a list of elements.

    #     Parameters:
    #     - gamaCode: The Gamma code to convert.

    #     Returns:
    #     - The decoded list.
    # in this function I returned the list of elements that makes input gamma code
    def gamaCodeToList(self,gamaCode):
        temp = []
        s=0
        e=0
        while(s!=len(gamaCode)):
            if gamaCode[e] =="1":
                e+=1
            else :
                e=(e-s)*2+s
                temp.append(gamaCode[s:e])
                s=e
        
        ls =  list(map(self.gamaCodeToNumber,temp))
        for i in range(1,len(ls)):
            ls[i]+=ls[i-1]
        return ls



    #---------------------------------------------------------------------------------------------------------------------


    # Merge subPosting lists into the main posting list.

    # in this function I merge posting lists after reding them from their files (then names of files are sorted base on sequence of their posting lists)
    def mergePostingLists (self): # new function for homework 3
        codedPostingList = self.codedPostingLit
        ls = sorted(os.listdir(self.tempDirectory))

        for file in ls:
            with open(f'{self.tempDirectory}/{file}', 'rb') as f:
                subPostingList=pickle.load( f)
            for item in subPostingList:
                word = item["word"]
                index = self.searchPostingList(word,codedPostingList) # find index of word in posting list
                if (len(codedPostingList)>index): # check if index is not larger than posting list (if word is bigger that all words, search function returns len(postingList)+1)
                    if (codedPostingList[index]["word"] == word): # check if index is the index of the word
                        codedPostingList[index]["docs"]+=self.listToGamaCode([document["doc"] for document in item["docs"] ],codedPostingList[index]["lastSeenIndex"]) # first make gamma code of lists of document indexes for this token base of last seen index and then merge with last gamma code 
                        codedPostingList["lastSeenIndex"]:item["docs"][-1]["doc"] # update last seen document index

                    else :
                        codedPostingList[index:index]=[{"word":item["word"],"docs": self.listToGamaCode([document["doc"] for document in item["docs"] ]) , "lastSeenIndex":item["docs"][-1]["doc"]}] # merge a token in middle of main posting list when it's the first time it is seen (base on its value )

                else :
                    codedPostingList.append({"word":item["word"],"docs": self.listToGamaCode([document["doc"] for document in item["docs"] ]) , "lastSeenIndex":item["docs"][-1]["doc"]}) # merge a token in end of main posting list when it's the first time it is seen (base on its value )
            # print("gama is :")
            # print(self.codedPostingLit)

    #---------------------------------------------------------------------------------------------------------------------


    # Find a word in the posting list.

    #     Parameters:
    #     - word: The word to search for.

    #     Returns:
    #     - Index of the word in the posting list or -1 if not found.

    # I changed this function to first transform gamma code to list on index and then return the results
    def findWord(self, word): # this function use our binary search function to find word in posting list and if the word is not included in the list, returns -1
        index = self.searchPostingList(word,self.codedPostingLit)
        if (index< len(self.codedPostingLit)):
            if (self.codedPostingLit[index]["word"] == word):
                return index # real index of the word
        return -1 # word is not in the posting list


    def find(self , query:str): # split the query and find the result 
        splitQuery = query.lower().split()
        if (len(splitQuery)==1): # query is only one word
            index = self.findWord(splitQuery[0])
            if (index>-1):
                print("word appears in :  ", self.codedPostingLit[index]["docs"])
                return [ i for i in self.gamaCodeToList(self.codedPostingLit[index]["docs"])]
            return []

        else: 
            index1 = self.findWord(splitQuery[0])
            index2 = self.findWord(splitQuery[2])
            if splitQuery[1] in ["and" ,"or", "AND", "OR"]: # boolean condition
                
                if (splitQuery[1] in ["and","AND"]): # and condition
                    if(index1!=-1 and index2!=-1): # check if there are result for both of words
                        print("first word is in :  ", self.codedPostingLit[index1]["docs"])
                        print("second word is in :  ", self.codedPostingLit[index2]["docs"])

                        docs1 =  set([ i for i in self.gamaCodeToList(self.codedPostingLit[index1]["docs"])]) # find document of word one 
                        docs2 =  set([ i for i in self.gamaCodeToList(self.codedPostingLit[index2]["docs"])]) # find document of word two 
                        # print(self.codedPostingLit[index1]["docs"] , self.codedPostingLit[index2]["docs"])
                        return list(docs1.intersection(docs2)) # make intersection of two results
                    return []
                    
                if (splitQuery[1] in ["or","OR"]): # or condition
                    if(index1!=-1 and index2!=-1): # check if there are result for both of words
                        print("first word is in :  ", self.codedPostingLit[index1]["docs"])
                        print("second word is in :  ", self.codedPostingLit[index2]["docs"])
                        docs1 =  set([ i for i in self.gamaCodeToList(self.codedPostingLit[index1]["docs"])])
                        docs2 =  set([ i for i in self.gamaCodeToList(self.codedPostingLit[index2]["docs"])])
                        # print(self.codedPostingLit[index1]["docs"] , self.codedPostingLit[index2]["docs"])
                        return list(docs1.union(docs2))
                    print("first word is in :  ", self.codedPostingLit[index1]["docs"])
                    print("second word is in :  ", self.codedPostingLit[index2]["docs"])
                    if(index1!=-1): return [ i for i in self.gamaCodeToList(self.codedPostingLit[index1]["docs"])] # check if there is result for first word
                    return [ i for i in self.gamaCodeToList(self.codedPostingLit[index2]["docs"])] # check if there is result for second word

            # else : # near condition
            #     nearNumber = int(splitQuery[1].split('/')[1]) # find near 
            #     if(index1!=-1 and index2!=-1): # check if there are result for both of words
            #         docs1 =   {i["doc"]:i["indexes"] for i in self.postingList[index1]["docs"]} # find document of word one and make dictionary for result
            #         docs2 =   {i["doc"]:i["indexes"] for i in self.postingList[index2]["docs"]} # find document of word two and make dictionary for result

            #         result = [] 
            #         keysOfDocs2 = docs2.keys()
            #         for key, value in docs1.items():
            #             if (key in keysOfDocs2):
            #                 d1 = np.array(value) # indexes of word in first document
            #                 d2 = np.array(copy.deepcopy(docs2[key])) # indexes of word in second document
            #                 distanceMatrix = np.array([[abs(i - j )for i in d1] for j in d2]) # distance matrix
            #                 if (distanceMatrix.min() <= nearNumber): # check validation
            #                     result.append(key)


            #                 # example of distanceMatrix
            #                 # 
            #                 # [[ 0  1  2 10 11]
            #                 # [ 1  0  1  9 10]
            #                 # [ 2  1  0  8  9]
            #                 # [10  9  8  0  1]
            #                 # [11 10  9  1  0]]


                    return result
            return []
            


    def prnt(self):
        for i in self.postingList:
            print(i)

    def printGamaCodePostingList(self):
        print("gama code posting list is : ")
        for i in self.codedPostingLit:
            print(i)

    def printPostingListsFiles(self):
        ls = sorted(os.listdir(self.tempDirectory))
        print(ls)
        for file in ls:
            with open(f'{self.tempDirectory}/{file}', 'rb') as f:
                print(pickle.load( f))




# %% [markdown]
# # Test cases:

# %%
import os
directory_input = ['docs/'+path for path in os.listdir('docs') if path[-3:] == 'txt']
print(directory_input)

# %%
test_directory = searchEngine(tempDirectory="test_directory_postingLists")
test_directory.input(directory_input)
test_directory.mergePostingLists()

# %%
test = searchEngine(tempDirectory="test_postingLists")

test.input(['document1.txt','document2.txt','document3.txt'])
test.mergePostingLists()


# %%
test.printGamaCodePostingList()

# %%
test_directory.printGamaCodePostingList()

# %%
test.printPostingListsFiles()

# %%
test_directory.printPostingListsFiles()

# %% [markdown]
# # Test Query:

# %%
test.find("contains")

# %%
test_directory.find("several")

# %%
test_directory.find("several and 10")


# %%
test_directory.find("several or 10")



