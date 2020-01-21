from flask import Flask, request, render_template
import requests

app = Flask(__name__)

#Vars
Theme = 'dracula'
DisplayOutput = 'none'
Languages = {
	'C' : 'C' ,
	'Cpp' : 'C++' ,
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
	res = "\nSubmission Results :"
	if Output['compResult']=='S' and Output['valid']=='1' :
		if Output['cmpError']!='' :
			res+='Compilation Failed!'
			res+=('\nCompilation Error :\n'+Output['cmpError'])
			if Output['rntError']!='':
				res+=('\nRuntime Error :\n'+Output['rntError'])
		else:
			if Output['rntError']!='':
				res+='Compilation Failed!'
				res+=('\nRuntime Error :\n'+Output['rntError'])
			else :
				res+='Accepted!!\n'
				res+=(('\nOutput :\n'+Output['output']).strip())
	else :
		res+='\nCompilation Failed!'
	res+=('\nTime :'+Output['time'] + ' ')
	res+=('Memory :'+Output['memory']+'	')
	res+=('Submission Id :'+Output['id'])
	return res
@app.route('/')
def my_form():
	DisplayOutput = 'none'
	return render_template('index.html' , Languages = Languages , SelectedLanguage ='C' , DisplayOutput = DisplayOutput , LangHLModes = LangHLModes ,Theme = Theme)

@app.route('/', methods=['POST'])
def my_form_post():
    SourceCode = request.form['code']
    CustomInput = request.form['input']
    Lang = request.form['lang']
    print("Language = " , Lang)
    Save = 'true'
    Output = Compile(SourceCode , Lang , CustomInput , Save)
    print('Output' ,  Output)
    DisplayOutput = 'block'
    return render_template('index.html' , SourceCode=SourceCode , CustomInput=CustomInput, Languages = Languages , SelectedLanguage= Lang , Output = Output , DisplayOutput = DisplayOutput , LangHLModes = LangHLModes , Theme = Theme)

if __name__ == "__main__" : 
	app.run(debug = True)