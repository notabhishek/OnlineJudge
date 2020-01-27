from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)
#Vars
Theme = 'dracula'
problemQuestion =''
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
	res = ["\nSubmission Results :"]
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
				res.append('Accepted!!')
				res.append(('Output :\n'+Output['output']).strip())
	else :
		res.append('\nCompilation Failed!')
	res.append('\nTime :'+Output['time'] + ' ')
	res.append('Memory :'+Output['memory']+'	')
	res.append('Submission Id :'+Output['id'])
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
		print(pDesc)
		problem['pValid'] = '1'
		return problem	
	except ConnectionError:
		print("Couldn't connect to Internet! Please check your connection & Try again.")
	problem = {'pValid' : '0'}
	return problem


@app.route('/')
def my_form():
	global problemQuestion
	DisplayOutput = 'none'
	if problemQuestion == '' :
		problemQuestion = Scraper("kth-smallest-element/0")
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
	if request.form['LangChanged']=='false' :
		Output = Compile(SourceCode , Lang , CustomInput , Save)
		DisplayOutput = 'block'
	if problemQuestion == '' :
		problemQuestion = Scraper("kth-smallest-element/0")
	return render_template('index.html' , SourceCode=SourceCode , CustomInput=CustomInput, Languages = Languages , SelectedLanguage= Lang , Output = Output , DisplayOutput = DisplayOutput , LangHLModes = LangHLModes , Theme = Theme , problemQuestion = problemQuestion)

if __name__ == "__main__" : 
	app.run(debug = True)