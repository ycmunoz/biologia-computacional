#for Flask
from flask import Flask
from flask import render_template, flash, redirect, request
import os
import formsFunc as ff
import bioFunc as bf
#import dbDef
from flask_sqlalchemy import SQLAlchemy
import webbrowser as wb
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_key'
bootstrap = Bootstrap(app)

dbdir = 'sqlite:///'+os.path.abspath(os.getcwd()) + '/static/osos.db'
app.config['SQLALCHEMY_DATABASE_URI'] = dbdir
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#https://www.tutorialspoint.com/flask/flask_sqlalchemy.htm
class Osos(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    commonName = db.Column(db.String(100))
    scientificName = db.Column(db.String(100))  
    redList = db.Column(db.String(10))
    link = db.Column(db.String(20))

    def __init__(self, name, city, addr,pin):
        self.commonName = commonName
        self.scientificName = scientificName
        self.redList = redList
        self.link = link

def setdb():
	import pandas as pd
	data = pd.read_csv('static/data/Osos.csv')
	for row in data.shape[0]:
		scientificName = data['ScientificName'].iloc[row]
		commonName = data['CommonName'].iloc[row]
		redList = data['IUCNRedListCategory'].iloc[row]
		link = data['Hyperlink'].iloc[row]
		data['commonName = commonName, scientificName = scientificName, redList = redList, link = link']
		osos = Osos( commonName = commonName, scientificName = scientificName, redList = redList, link = link)
		db.session.add(osos)
		db.session.commit()

# //////////////////////////////// INICIO ////////////////////////////////
@app.route('/')
@app.route('/Inicio/Objetivos')
def objetivos():
	db.create_all()
	return render_template('index_objetivos.html', title='Inicio')

# //////////////////////////////// ANALISIS ////////////////////////////////
@app.route('/Analisis/', methods=('GET', 'POST'))
@app.route('/Analisis/Gen', methods=('GET', 'POST'))
def gen():
	form_g = ff.gen_form()
	lista = bf.importar_genes()
	lista_homologos = []
	form_g.gen_list.choices = lista
	if form_g.validate_on_submit():
		flash('Gen escogido = %s' % (form_g.gen_list.data))
		indice = int(form_g.gen_list.data)
		file_homologo = form_g.gen_list.data
		file_homologo += '.fasta'
		lista_homologos = bf.importar_homologos_G(file_homologo)
		info = bf.getSeq_G(lista[indice-1][1])
		return render_template('analisis_gen.html', title='Gen', form = form_g, lista=lista_homologos, info=info)
	return render_template('analisis_gen.html', title='Gen', form = form_g)

@app.route('/Analisis/Proteina', methods=('GET', 'POST'))
def proteina():
	form_p = ff.protein_form()
	lista = bf.importar_proteinas()
	lista_homologos = []
	form_p.protein_list.choices = lista
	if form_p.validate_on_submit():
		flash('Proteina escogida = %s' % (form_p.protein_list.data))
		indice = int(form_p.protein_list.data)
		file_homologo = form_p.protein_list.data
		file_homologo += '.fasta'
		lista_homologos = bf.importar_homologos_P(file_homologo)
		info = bf.getSeq_P(lista[indice-1][1])
		return render_template('analisis_proteina.html', title='Proteina', form = form_p, lista=lista_homologos, info=info)
	return render_template('analisis_proteina.html', title='Proteina', form = form_p)

@app.route('/Analisis/Arbol' , methods=('GET', 'POST'))
def arbol():
	form_t = ff.tree_form()
	lista = bf.importar_genes()
	form_t.tree_list.choices = lista
	if form_t.validate_on_submit():
		flash('ID: %s' %(form_t.tree_list.data))
		indice = form_t.tree_list.data
		path_arbol_num = './static/seq/Homologos/Nucleotidos'+form_t.tree_list.data
		comando = 'clustalw '+ path_arbol_num  + '.fasta'
		os.system(comando)
		bf.generar_arbol(path_arbol_num + '.aln', indice)
		info = list(open('./static/seq/Informacion/'+indice+'.txt','r'))[1]	
		return render_template('analisis_filogenetica.html', title='Arbol', form = form_t, indice = indice, info=info)
	return render_template('analisis_filogenetica.html', title='Arbol', form = form_t)

# ////////////////////////////////Otras especies////////////////////////////

@app.route('/Analisis/Especies', methods=('GET', 'POST'))
def especie():
    setdb()
	#http://datazone.bearlife.org/species/factsheet/ + ?
	#return render_template('analisis_especies.html', title='Especies')
	#, osos = Osos.query.all())

@app.route('/new', methods = ['GET', 'POST'])
def new():
	if request.method == 'POST':
		if not request.form['commonName'] or not request.form['scientificName']:
			flash('Please enter all the fields', 'error')
		else:
			osos = osos(request.form['commonName'], request.form['scientificName'],
				request.form['redList'], request.form['link'])
         
			db.session.add(osos)
			db.session.commit()
         
			flash('Record was successfully added')
			return redirect('/Analisis/Especies')
	return render_template('new.html')

# //////////////////////////////// PROYECTO ////////////////////////////////
@app.route('/Proyecto/')
@app.route('/Proyecto/Integrantes')
def integrantes():
	return render_template('proyecto_integrantes.html', title='Integrantes')

#if __name__ == '__main__':
#	wb.open('http://127.0.0.1:5000')
#	app.run(debug=True)
