from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
#Vars
Theme = 'dracula'
problemQuestion =''
problemQuestionName ="rotate-array-by-n-elements/0"
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



@app.route('/')
def my_form():
	global problemQuestion
	DisplayOutput = 'none'
	if problemQuestion == '' :
		problemQuestion = Scraper(problemQuestionName)
	return render_template('index.html' , Languages = Languages , SelectedLanguage ='C' , DisplayOutput = DisplayOutput , LangHLModes = LangHLModes ,Theme = Theme , problemQuestion = problemQuestion)

@app.route('/', methods=['POST'])
def my_form_post():
	global problemQuestion
	SourceCode = request.form['code']
	CustomInput = request.form['input']
	Lang = request.form['lang']
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
	if problemQuestion == '' :
		problemQuestion = Scraper(problemQuestionName)
	#print(problemQuestion)
	return render_template('index.html' , SourceCode=SourceCode , CustomInput=CustomInput, Languages = Languages , SelectedLanguage= Lang , Output = Output , DisplayOutput = DisplayOutput , LangHLModes = LangHLModes , Theme = Theme, problemQuestion=problemQuestion)

if __name__ == "__main__" : 
	app.run(debug = True)

'''
@app.route('/home') 
def show_topics() :
	global topics
	if len(topics) == 0 : 
		topics = ScrapeTopics()
	return render_template('topics.html' , topics = topics)

@app.route('/home' , methods=['POST'])
def show_topics_form() :
	global topics
	link = request.form['Query']
	print(topics[link][0] , topics[link][1])
	return render_template('home.html')
'''
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#------------------------FUNCTIONS ---------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------

def Compile(Code , Lang , Input, Save) :
	url = 'https://ide.geeksforgeeks.org/main.php'
	data = {
	'lang' : Lang , 
	'code' : Code , 
	'input' : Input , 
	'save' : Save
	}
	response = requests.post(url,data=data)
	Output = response.json()
	res = []
	if Output['compResult']=='S' and Output['valid']=='1' :
		if Output['cmpError']!='' :
			res.append('Compilation Failed!')
			res.append('Compilation Error :'+Output['cmpError'])
			if Output['rntError']!='':
				res.append('Runtime Error :'+Output['rntError'])
		else:
			if Output['rntError']!='':
				res.append('Compilation Failed!')
				res.append('Runtime Error :'+Output['rntError'])
			else :
				res.append("Output : ")
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
		soup = BeautifulSoup(response.content , 'html5lib')
		problem = {}
		fullPageDiv = soup.find('div' , attrs={'class' : 'row fullPageDiv'})
		pPage = fullPageDiv.find('div' , attrs={'class' : 'col-sm-7 col-xs-12'})
		
		pName = pPage.find('div' , attrs={'class' : 'col-lg-12'}).strong.text.strip()
		problem['pName'] = pName

		pStats = pPage.find('div' , attrs={'class' : 'col-sm-8 col-xs-12'}).h5.find_all('a')
		pStats.append(pPage.find('div' , attrs={'class' : 'col-sm-8 col-xs-12'}).h5.find('p'))
		for i in range(len(pStats)) :
			pStats[i] = pStats[i].text
		temp = ''
		for i in range(len(pStats[0])) :
			if pStats[0][i] <='9' and pStats[0][i]>='0' :
				temp+=pStats[0][i]
		pStats[0] = temp


		pSubmissions = pStats[0]
		pAccuracy = pStats[2]
		pDifficulty = pStats[1]

		problem['pDifficulty'] = pDifficulty
		problem['pAccuracy'] = pAccuracy
		problem['pSubmissions'] = pSubmissions

		tabContent = pPage.find('div' , attrs={'class' : 'problemQuestion'}).find_all('p')
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
'''
def ScrapeTopics() :
	try :
		response = requests.get('https://practice.geeksforgeeks.org/')
		soup = BeautifulSoup(response.content , 'html5lib')
		Category = soup.find_all('div' , attrs={'class' : 'col-xs-12 col-sm-6 col-md-3 itemInnerDiv'})
		topics = []
		for i in Category :
			if(i.text.strip()=="") :
				pass
			else :
				topics.append([ str(i.text.strip()) ,  str(i.a['href'].strip()) ])
		return topics	
	except :
		print("Please Check your network connection!!")
		return []
'''


#repair scraper function to return    name : link dictionary 
#function returns name and corresponding names link is then scraped 
