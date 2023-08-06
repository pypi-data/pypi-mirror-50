import pickle



def dump(nombre_archivo, predicciones=None, algo=None, verbose = 0):

	dump_obj = {'predicciones': predicciones,'algo': algo}


	pickle.dump(dump_obj, open(nombre_archivo,'wb'),protocol=pickle.HIGHEST_PROTOCOL)

	if verbose:
		print("El objeto se ha guardado como archivo", nombre_archivo)


def cargar(nombre_archivo):


	dump_obj = pickle.load(open(nombre_archivo,'rb'))
	return dump_obj['predicciones'],dump_obj['algo']

