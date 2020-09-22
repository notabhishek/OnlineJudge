from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
import time
app = Flask(__name__)
#Vars
Theme = 'dracula'
problemQuestion =''
problemQuestionNames = ["rotate-array-by-n-elements/0" , "sort-and-reverse-vector/1" , "learn-to-comment/1" , "arraylist-operation/1" , "max-distance-between-same-elements/1" , "maximum-in-struct-array/1",
"addition-of-submatrix/0" , "sum-of-fai-aj-over-all-pairs-in-an-array-of-n-integers/0" , "balanced-array/0" , "counts-zeros-xor-pairs/0" , "play-with-an-array/1" , "ishaan-loves-chocolates/0" , "largest-fibonacci-subsequence/0" , "need-some-change/1"]

problemQuestionName = problemQuestionNames[0]
topics = []
Languages = {
	'C' : 'C' ,
	'Cpp' : 'C++',
	'Cpp14' :'C++14',
	'Csharp' : 'C#' , 
	'Java' : 'Java',
	'Perl' : 'Perl' , 
	'Php' : 'Php' , 
	'Python' : 'Python',
	'Python3' : 'Python 3',
	'Scala' : 'Scala' 
}
LangHLModes = {
	'C' : 'text/x-csrc' , 
	'Cpp' : 'text/x-c++src',
	'Cpp14' : 'text/x-c++src',
	'Csharp' : 'text/x-csharp' ,
	'Java' : 'text/x-java' , 
	'Perl' : 'text/x-perl',
	'Php' : 'text/x-php' ,
	'Python' : 'text/x-python' ,
	'Python3' : 'text/x-python' , 
	'Scala' : 'text/x-scala'
}
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#------------------------FUNCTIONS ---------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------

def Compile(Code , Lang , Input, Save) :
	url = 'https://ide.geeksforgeeks.org/main.php'
	urlSub = 'https://ide.geeksforgeeks.org/submissionResult.php'
	data = {
	'lang' : Lang , 
	'code' : Code , 
	'input' : Input , 
	'save' : Save
	}
	response1 = requests.post(url,data=data).json()
	print("Resrponse "  , response1)
	while(response1['status']!='SUCCESS') :
		response1 = requests.post(url,data=data).json()
	SID = response1['sid']
	# time.sleep(1)

	response = requests.post(urlSub , data= {'sid' : SID , 'requestType' : 'fetchResults'})
	Output = response.json()
	while Output['status'] != 'SUCCESS' : 
		response = requests.post(urlSub , data= {'sid' : SID , 'requestType' : 'fetchResults'})
		Output = response.json()
	# while(Output['status'] != 'SUCCESS') :
    # 	response = requests.post(urlSub , data= {'sid' : SID , 'requestType' : 'fetchResults'})
	# 	Output = response.json()
	print(Output)
	res = []
	if Output['compResult']=='S' and Output['valid']=='1' :
		if ('cmpError' in Output) and Output['cmpError']!='' :
			res.append('Compilation Failed!')
			res.append('Compilation Error :'+Output['cmpError'])
			if  ('rntError' in Output ) and Output['rntError']!='':
				res.append('Runtime Error :'+Output['rntError'])
		else:
			if ('rntError' in Output ) and Output['rntError']!='':
				res.append('Compilation Failed!')
				res.append('Runtime Error :'+Output['rntError'])
			else:
				res.append("Output : ")
				# print('Unformatted Output : \n ' , Output['output'])
				temp_op = ''
				if 'output' in Output:
    					temp_op = Output['output'].split('\n')			
				for i in range(len(temp_op)) : 
					res.append(temp_op[i].strip())
	else :
		res.append('\nCompilation Failed!')

	res.append('\nTime :'+Output['time'] + ' ')
	res.append('Memory :'+Output['memory']+'	')
	res.append('Submission Id :'+Output['id'])
	print("Output \n " , res)
	return res

def Scraper( ProblemCode ) :
	BASE_URL = "https://practice.geeksforgeeks.org/problems/"
	URL = BASE_URL + ProblemCode
	try:
		response = requests.get(URL)
		soup = BeautifulSoup(response.content ,'html5lib')
		#print(soup)
		problem = {}
		fullPageDiv = soup.find('div' , attrs={'class' : 'row problem-container'})
		# print("full Page Div \n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n" , fullPageDiv)
		pPage = fullPageDiv #fullPageDiv.find('div' , attrs={'class' : 'col-sm-7 col-xs-12'})
		pName = pPage.find('span' , attrs={'class' : 'problem-tab__name'}).text.strip()
		# print("\n\n\n\n\n\n\n\n\nProblem " , pName)
		problem['pName'] = pName

		pStats = pPage.find_all('span' , attrs={'class' : 'problem-tab__value'})
		
		# pStats.append(pPage.find('div' , attrs={'class' : 'col-sm-8 col-xs-12'}).h5.find('p'))
		for i in range(len(pStats)) :
			pStats[i] = pStats[i].text
		# print("\n\n\n\n\n", pStats)
		temp = ''
		# for i in range(len(pStats[0])) :
		# 	if (pStats[0][i] <='9' and pStats[0][i]>='0') or (pStats[0][i]=='.') :
		# 		temp+=pStats[0][i]
		# pStats[0] = temp

		pSubmissions = pStats[1]
		pAccuracy = pStats[0]
		pDifficulty = pStats[2]

		problem['pDifficulty'] = pDifficulty
		problem['pAccuracy'] = pAccuracy
		problem['pSubmissions'] = pSubmissions
		print("\n\n\n\n\n\n" , problem)
		tabContent = pPage.find('div' , attrs={'class' : 'problem-statement'}).find_all('p')
		pDesc = []
		for i in range(len(tabContent)) :
			tabContent[i] = tabContent[i].text
			pDesc.append(tabContent[i].strip().split('\n'))
		problem['pDesc'] = pDesc
		#print(pDesc)
		problem['pValid'] = '1'
		return problem	
	except ConnectionError:
		print("Couldn't connect to Internet! Please check your connection & Try again.")
	problem = {'pValid' : '0'}
	return problem


@app.route('/')
def my_form():
	global problemQuestion
	global problemQuestionIndex
	global problemQuestionNames
	global problemQuestionName
	DisplayOutput = 'none'
	if problemQuestion == '' :
		problemQuestionIndex = 0
		problemQuestionName = problemQuestionNames[1]
		problemQuestion = Scraper(problemQuestionName)
		print(problemQuestion)
	return render_template('index.html' , Languages = Languages , SelectedLanguage ='Python3' , DisplayOutput = DisplayOutput , LangHLModes = LangHLModes ,Theme = Theme , problemQuestion = problemQuestion , problemQuestionNames = problemQuestionNames,selectedProblem = problemQuestionName)

@app.route('/', methods=['POST'])
def my_form_post():
	global problemQuestion
	global problemQuestionIndex
	global problemQuestionNames
	global problemQuestionName
	SourceCode = request.form['code']
	CustomInput = request.form['input']
	Lang = request.form['lang']
	problemQuestionName = request.form['selectedProblem']
	#problemQuestionName = problemQuestionNames[0]
	print("Form : " , request.form)
	Save = 'true'
	Output = ''
	DisplayOutput='none'
	
	if request.form['Query']=='submit' :
		Output = Compile(SourceCode , Lang , CustomInput , Save)
		DisplayOutput = 'block'
	elif request.form['Query']=='hide_output' :
		DisplayOutput = 'none'
	elif request.form['Query']=='show_output' :
		DisplayOutput = 'block'
	elif request.form['Query']=='change_problem' :
		problemQuestionName = request.form['selectedProblem']
		problemQuestion = Scraper(problemQuestionName)

	if problemQuestion == '' :
		problemQuestion = Scraper(problemQuestionName)
	#print(problemQuestion)
	return render_template('index.html' , SourceCode=SourceCode , CustomInput=CustomInput, Languages = Languages , SelectedLanguage= Lang , Output = Output , DisplayOutput = DisplayOutput , LangHLModes = LangHLModes , Theme = Theme,problemQuestion = problemQuestion, problemQuestionNames=problemQuestionNames, selectedProblem = problemQuestionName)

if __name__ == "__main__" : 
	app.run(debug = True)




