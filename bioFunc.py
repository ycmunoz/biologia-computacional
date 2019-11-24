from Bio.Seq import Seq
from Bio import SeqIO#for tree
from Bio import AlignIO
from Bio.Align.Applications import MuscleCommandline
from Bio.Align.Applications import ClustalwCommandline
from Bio.Phylo.TreeConstruction import DistanceCalculator
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor
import matplotlib
matplotlib.use('Agg')
from Bio import Phylo
import pylab
from os import path

spec_list = ["IniaGeoffrensis","VicugnaVicugna","ToromysRhipidurus","OreotrochilusMelanogaster"]

def getSeq_P(spc_id,acc_key):
	rec = SeqIO.parse("./static/seq/Proteinas/"+spec_list[spc_id-1]+".fasta", "fasta")
	count = 1
	for seq in rec:
		if count == acc_key:
			seqID = '>' +str(seq.description)
			seqSeq =  str(seq.seq)
			break
		count = count +1
	data = {'ID':seqID, 'Seq':seqSeq}
	return data

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

#Lista proteinas por nombre:
def listar_gen_proteina():
	out_key = ["1","2","3","4"]
	out_id = ["Cytochrome B","Cytochrome C Oxidase subunit 1","NADH dehydrogenase subnit 1","ATP synthase F0 subunit 6"]
	return list(zip(out_key,out_id))

def listar_especie():
	out_key = ["1","2","3","4"]
	out_id = ["Inia Geoffrensis","Vicugna Vicugna","Toromys Rhipidurus","Oreotrochilus Melanogaster"]
	return list(zip(out_key,out_id))

def importar_homologos_P(spc_id,acc_key):
	#file = "./static/seq/Homologos/Proteinas"+ file
	file = "./static/seq/Homologos/"+spec_list[spc_id-1]+str(acc_key)+".fasta" #+ file
	rec = SeqIO.parse(file,"fasta")
	out_accession = []
	out_description = []
	for r in rec:
		out_accession.append(r.id)
		out_description.append(r.description)
	return list(zip(out_accession,out_description))

def generar_arbol(especie, indice):
	tree_path = './static/img/bio/'+ especie + indice +'.png'

	if not path.exists(tree_path):
		seq_path = './static/seq/Homologos/'
		fasta_file = seq_path + especie + str(indice) + '.fasta'
		aln_file = seq_path + especie + str(indice) + '.aln'

		# Ejecuta MUSCLE para el alineamiento de secuencias homologas
		cli = MuscleCommandline(input=fasta_file, out=aln_file, clw=True)
		#cli = ClustalwCommandline(infile=fasta_file,outfile=aln_file)
		cli()

		with open(aln_file, "r") as aln:
			alineamiento = AlignIO.read(aln, "clustal")
		
		# Blosum62 para proteinas
		calculator = DistanceCalculator('blosum62')
		dm = calculator.get_distance(alineamiento)

		constructor = DistanceTreeConstructor(calculator)
		# Neighbor Joining
		nj = constructor.nj(dm)
		
		Phylo.draw(nj, label_func=get_label)
		pylab.savefig(tree_path, format='png')

def get_label(leaf):
	if "Inner" in leaf.name:
		return leaf.name
	else:
		from Bio import Entrez
		Entrez.email = "victoralegre@uni.pe"
		handle = Entrez.efetch(db="protein",id=leaf.name, rettype="gp",retmode="text")
		result=handle.read().split('\n')
		for line in result:
			if "ORGANISM" in line:
				return line.split()[1:]
		return leaf.name