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


def getSeq_P(acc_id):
	accession = str(acc_id)
	Entrez.email = "X@Y.com"
	cadenaFasta = Entrez.efetch(db="protein", id=accession, rettype="fasta", retmode="text")
	S = SeqIO.parse(cadenaFasta,"fasta")
	for seq in S:
		seqID = '>' + str(seq.id)
		seqSeq =  str(seq.seq)
	data = {'ID':seqID, 'Seq':seqSeq}
	return data

def getSeq_G(acc_id):
	accession = str(acc_id)
	Entrez.email = "X@Y.com"
	cadenaFasta = Entrez.efetch(db="nucleotide", id=accession, rettype="fasta", retmode="text")
	S = SeqIO.parse(cadenaFasta,"fasta")
	for seq in S:
		seqID = '>' + str(seq.id)
		seqSeq =  str(seq.seq)
	data = {'ID':seqID, 'Seq':seqSeq}
	return data

def importar_genes():
	rec = SeqIO.parse("./static/seq/Genes/Nucleotidos.fasta", "fasta")
	i = 1
	out_key = []
	out_id = []
	for r in rec:
		out_key.append(str(i))
		out_id.append(r.id)
		i += 1
	return list(zip(out_key, out_id))

def importar_proteinas():
	rec = SeqIO.parse("./static/seq/Proteinas/Proteinas.fasta", "fasta")
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
	upgma_tree = constructor.build_tree(alineamiento)
	Phylo.draw(upgma_tree)
	#Phylo.write(upgma_tree, 'arbolito.xml','phyloxml')
	path = './static/img/bio/arbol_filogenetico'+ indice +'.png'
	pylab.savefig(path, format='png')