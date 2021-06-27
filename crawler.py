#Rueben Tiow
#6/27/2021
#Python Wikipedia WebCrawler
import wikipedia
import re
import pandas as pd

class solution:
    def __init__(self):
        """
        Default constructor that reads the Wikipedia Microsoft webpage using the Wikipedia API on 
        creation of the solution object.
        """        
        self.CONTENT = wikipedia.page(title="Microsoft").content 
        
    def configUserInput(self):
        """
        Takes in the first user input param1, for the number of words to return in the result. 
        If nothing is provided, then the default of 10 words will be returned in the result.
        Takes in the second user input param2, for the words to be excluded in the returned result.
        Returns the user input for param1 and param2. 
        :rtype: int, str
        """
        DEFAULT_OUTPUT = 10
        DEFAULT_EX = ' '
        while(True): 
            try:
                param1=int(input("Number of words to return {default 10}: ") or DEFAULT_OUTPUT)
                if param1 > 0:
                    break
            except ValueError as e:
                print(e)

        param2 = input("Words to exclude: ")
        if param2 != "":
            param2+=DEFAULT_EX
        return param1, param2
        
  
    def storeFreq(self, word, ex, freqDict):
        """
        Takes in a string word, and performs a regex pattern match to exclude words matching numbers 
        representing dates between 1 to 4 digits, any date years interval that is hyphenated, any 
        numbers that include decimals, and words that have equal signs used. If the word excludes 
        these matches, then check if it is not a word in the user's excluded word list, and stores 
        its frequency count in a dictionary. If the word is not in the dictionary, add the word as 
        the key and set its value to 1, otherwise increment the existing word's value by 1 and return 
        the dictionary.
        :type word: str
        :type ex: List[str]
        :type freqDict: Dict[str, int]
        :rtype: Dict[str, int]
        """
        if(re.match('^\d{1,4}$',word) or re.match('^\d{4}-\w+$',word) or re.match('^\d+.\d+', word) or re.match('^[=]+',word)):
            pass
        else:
            if word not in ex:
                if word not in freqDict:
                    freqDict[word] = 1
                else:
                    freqDict[word] = freqDict.get(word) + 1
        return freqDict
    
    def aggCommonWords(self, freqDict):
        """
        Takes in a dictionary freqDict, checks for miscounted common words because of capitalization, 
        or upper-case variations. Returns the dictionary freqDict with a unified sum on the frequency 
        values of these common words. The commonWords list can be extended to include more common words.
        :type freqDict: Dict[str, int]
        :rtype: Dict[str, int]        
        """
        commonWords=['the','be','to','of','and','a','in','that','have','I','for','not','on','with','he','as']
        for word in commonWords:
            val1=0
            val2=0
            val3=0
            if word.capitalize() in freqDict:
                val1=freqDict.get(word.capitalize())
                del freqDict[word.capitalize()] 
            if word.upper() in freqDict:
                val2=freqDict.get(word.upper())  
                del freqDict[word.upper()]
            if word in freqDict:
                val3=freqDict.get(word) 
                freqDict[word] = val1+val2+val3
        return(freqDict)
    
    def crawlerCode(self):
        """
        Begins by calling the configUserInput function to take the user's input to configure the settings 
        for the number of words to return, and words to exclude in the returned result. Build a word list 
        wList, by taking the Wikipedia webpage content and regex splitting on commas, white spaces, 
        periods, newline carriage, colons, and double-quotes. Loops through the word list wList, and 
        search for the History section. Continue looping through the history section and store the 
        frequency of each word in the dictionary freqDict by calling the storeFreq function. Once done, 
        call aggCommonWords on freqDict to a process common word processing for catching double counts 
        on upper case or capitalized common words. Take dictionary freqDict and store each key-value 
        pair tuple in a list, and sort in descending order. Take this data and insert it into a data 
        frame and return the data frame results.
        :rtype: DataFrame(List[(int, str)], columns=["# of occurences", "Word"])  
        """
        p1,p2 = self.configUserInput()
        ex = p2.split(' ')
        print(ex)
        wList=re.split(',| |\.|\n|:|"', self.CONTENT)
    
        index=0
        count=0
        flag=False
        freqDict={}
        
        while index<len(wList):
            if wList[index] == "History" and wList[index+1] =="==": 
                flag=True
            elif wList[index] != "History" and wList[index+1] =="==":
                if count==0: 
                    count=1
                elif count==1:
                    flag=False
                    freqDict = self.storeFreq(wList[index], ex, freqDict) #Grab final element                 
                    break
            if(flag):
                freqDict = self.storeFreq(wList[index], ex, freqDict) 
            index+=1
        
        freqDict = self.aggCommonWords(freqDict)
        freqList = [ (v,k) for k,v in freqDict.items() ]
        freqList.sort(reverse=True)
        
        df = pd.DataFrame(freqList[:p1],columns=['# of occurences','Word'])
        return(df)
    
    def runCode(self):
        """
        Loops the user input, continues running the crawlerCode function indefinitely if user 
        inputs Y or y and terminates if the user inputs N or n.
        """
        while(True):
            userIn = input("Continue? Y/N: " )
            if(userIn == "Y" or userIn == "y"):
                print(self.crawlerCode())
            elif(userIn == "N" or userIn =="n"):
                break
            else:
                print("Incorrect input")
obj = solution()
obj.runCode()                
