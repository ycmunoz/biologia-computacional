#for Flask
from flask import Flask
from flask import render_template, flash, redirect, request
import os
import formsFunc as ff
import bioFunc as bf
import webbrowser as wb
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_key'
bootstrap = Bootstrap(app)

# //////////////////////////////// INICIO ////////////////////////////////
@app.route('/')
def objetivos():
	return render_template('index_objetivos.html', title='Inicio')

# //////////////////////////////// ANALISIS ////////////////////////////////
@app.route('/Analisis/', methods=('GET', 'POST'))
@app.route('/Analisis/Proteina', methods=('GET', 'POST'))
def proteina():
	form_p = ff.protein_form()
	#lista = bf.importar_proteinas("IniaGeoffrensis")
	especies = bf.listar_especie()
	lista = bf.listar_gen_proteina()
	lista_homologos = []
	form_p.specie_list.choices = especies
	form_p.protein_list.choices = lista
	if form_p.validate_on_submit():
		flash('Proteina escogida = %s' % (form_p.protein_list.data))
		spc_indice = int(form_p.specie_list.data)
		indice = int(form_p.protein_list.data)
		lista_homologos = bf.importar_homologos_P(spc_indice,indice)
		info = bf.getSeq_P(spc_indice,indice)
		return render_template('analisis_proteina.html', title='Proteina', form = form_p, lista=lista_homologos, info=info)
	return render_template('analisis_proteina.html', title='Proteina', form = form_p)

@app.route('/Analisis/Arbol' , methods=('GET', 'POST'))
def arbol():
	form_t = ff.tree_form()
	especie_lista = bf.listar_especie()
	lista = bf.listar_gen_proteina()
	form_t.specie_list.choices = especie_lista
	form_t.tree_list.choices = lista
	if form_t.validate_on_submit():
		flash('ID: %s' %(form_t.tree_list.data))
		espc_indice = int(form_t.specie_list.data)
		indice = form_t.tree_list.data
		# Se genera el arbol en .png
		bf.generar_arbol(bf.spec_list[espc_indice-1], indice)
		info = list(open('./static/seq/Informacion/'+indice+'.txt','r'))[1]	
		return render_template('analisis_filogenetica.html', title='Arbol', form = form_t, especie = bf.spec_list[espc_indice-1], indice = indice, info=info)
	return render_template('analisis_filogenetica.html', title='Arbol', form = form_t)

# //////////////////////////////// PROYECTO ////////////////////////////////
@app.route('/Proyecto/')
@app.route('/Proyecto/Integrantes')
def integrantes():
	return render_template('proyecto_integrantes.html', title='Integrantes')