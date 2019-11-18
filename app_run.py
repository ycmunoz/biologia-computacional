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
@app.route('/Analisis/Gen', methods=('GET', 'POST'))
def gen():
	form_g = ff.gen_form()
	lista = bf.importar_genes("IniaGeoffrensis")
	lista_homologos = []
	form_g.gen_list.choices = lista
	if form_g.validate_on_submit():
		flash('Gen escogido = %s' % (form_g.gen_list.data))
		indice = int(form_g.gen_list.data)
		file_homologo = form_g.gen_list.data
		file_homologo += '.fasta'
		lista_homologos = bf.importar_homologos_G(file_homologo)
		info = bf.getSeq_G("IniaGeoffrensis",lista[indice-1][1])
		return render_template('analisis_gen.html', title='Gen', form = form_g, lista=lista_homologos, info=info)
	return render_template('analisis_gen.html', title='Gen', form = form_g)

@app.route('/Analisis/Proteina', methods=('GET', 'POST'))
def proteina():
	form_p = ff.protein_form()
	lista = bf.importar_proteinas("IniaGeoffrensis")
	lista_homologos = []
	form_p.protein_list.choices = lista
	if form_p.validate_on_submit():
		flash('Proteina escogida = %s' % (form_p.protein_list.data))
		indice = int(form_p.protein_list.data)
		file_homologo = form_p.protein_list.data
		file_homologo += '.fasta'
		lista_homologos = bf.importar_homologos_P(file_homologo)
		info = bf.getSeq_P("IniaGeoffrensis",lista[indice-1][1])
		return render_template('analisis_proteina.html', title='Proteina', form = form_p, lista=lista_homologos, info=info)
	return render_template('analisis_proteina.html', title='Proteina', form = form_p)

@app.route('/Analisis/Arbol' , methods=('GET', 'POST'))
def arbol():
	form_t = ff.tree_form()
	lista = bf.importar_genes("IniaGeoffrensis")
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

# //////////////////////////////// PROYECTO ////////////////////////////////
@app.route('/Proyecto/')
@app.route('/Proyecto/Integrantes')
def integrantes():
	return render_template('proyecto_integrantes.html', title='Integrantes')

#if __name__ == '__main__':
#	wb.open('http://127.0.0.1:5000')
#	app.run(debug=True)
