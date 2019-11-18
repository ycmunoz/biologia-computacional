#for BioPython
from Bio.Blast import NCBIWWW
from Bio.Seq import Seq
from Bio import SeqIO
from Bio.Alphabet import generic_dna, generic_protein, generic_rna
from Bio import Entrez
from Bio import SeqIO
#for tree
from Bio import AlignIO
from Bio.Phylo.TreeConstruction import DistanceCalculator
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor
import matplotlib
matplotlib.use('Agg') #para resolver lo de la imagen
from Bio import Phylo
import pylab


def getSeq_P(especie,acc_id):
	rec = SeqIO.parse("./static/seq/Proteinas/"+especie+".fasta", "fasta")
	for seq in rec:
		if seq.id == acc_id:
			seqID = '>' +str(seq.description)
			seqSeq =  str(seq.seq)
			break
	data = {'ID':seqID, 'Seq':seqSeq}
	return data

def getSeq_G(especie,acc_id):
	rec = SeqIO.parse("./static/seq/Genes/"+especie+".fasta", "fasta")
	for seq in rec:
		if seq.id == acc_id:
			seqID = '>' +str(seq.description)
			seqSeq =  str(seq.seq)
			break
	data = {'ID':seqID, 'Seq':seqSeq}
	return data

def importar_genes(especie):
	rec = SeqIO.parse("./static/seq/Genes/"+especie+".fasta", "fasta")
	i = 1
	out_key = []
	out_id = []
	for r in rec:
		out_key.append(str(i))
		out_id.append(r.id)
		i += 1
	return list(zip(out_key, out_id))

def importar_proteinas(especie):
	rec = SeqIO.parse("./static/seq/Proteinas/"+especie+".fasta", "fasta")
	i = 1
	out_key = []
	out_id = []
	for r in rec:
		out_key.append(str(i))
		out_id.append(r.id)
		i += 1
	return list(zip(out_key, out_id))

def importar_homologos_G(file):
	file = "./static/seq/Homologos/Nucleotidos"+ file
	rec = SeqIO.parse(file,"fasta")
	out_accession = []
	out_description = []
	for r in rec:
		out_accession.append(r.id)
		out_description.append(r.description)
	return list(zip(out_accession,out_description))

def importar_homologos_P(file):
	file = "./static/seq/Homologos/Proteinas"+ file
	rec = SeqIO.parse(file,"fasta")
	out_accession = []
	out_description = []
	for r in rec:
		out_accession.append(r.id)
		out_description.append(r.description)
	return list(zip(out_accession,out_description))

def generar_arbol(file, indice):
	with open(file, "r") as aln:
		alineamiento = AlignIO.read(aln, "clustal")

	calculator = DistanceCalculator('identity')
	dm = calculator.get_distance(alineamiento)

	constructor = DistanceTreeConstructor(calculator)
	nj = constructor.nj(dm)	# Neighbor Joining
	Phylo.draw(nj)
	path = './static/img/bio/arbol_filogenetico'+ indice +'.png'
	pylab.savefig(path, format='png')