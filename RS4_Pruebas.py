
def promedio_facultades(info: dict, contando_externos : bool = True ) -> tuple:


    facultades = extraer_facultades(info)
    try : 
        facultades_notas = extraer_notas_facultad(facultades, info, contando_externos )
    except: 
        return "Error numérico."
  
    promedios_fac = calcular_promedio_facultades(facultades_notas)
    conjunto_estudiantes=set()
    
    for facultad in facultades_notas:
        for estudiante in facultades_notas[facultad]: 
            conjunto_estudiantes.add(estudiante)
    lista_estudiantes= [ estudiante for  estudiante in conjunto_estudiantes]
   

    
    alumnos_correo = []
    for key in lista_estudiantes:
        estudiante = info[key]
        correo = armar_correos(estudiante)
        alumnos_correo.append(correo)
    
    promedios_estudiantes = (promedios_fac, sorted(alumnos_correo))
    return promedios_estudiantes         
  
    #return alumnos
    

def calcular_promedio_facultades(facultades_notas):
    promedios_fac = {}
    
    for facultad in facultades_notas: 
        lista_notas = facultades_notas[facultad]
        suma_notas_facultad = 0
        suma_creditos_facultad = 0
        for estudiante in lista_notas:
            suma_notas_facultad += lista_notas[estudiante][0]
            suma_creditos_facultad += lista_notas[estudiante][1]
        promedio_notas_facultad = round(suma_notas_facultad/suma_creditos_facultad,2)
        promedios_fac[facultad]= promedio_notas_facultad
        sorted_promedios_fac = sorted(promedios_fac.keys())
        promedios_fac_organizados = {}
        for valor in sorted_promedios_fac:
            promedios_fac_organizados[valor]= promedios_fac[valor]
    return promedios_fac_organizados

def extraer_notas_facultad(facultades:set, info:dict, contando_externos:bool ):
    facultades_notas = {}
    for facultad in facultades:
       
        notas_facultad = {}      
        for estudiante in info:

            materias_estudiante = info[estudiante]["materias"]
            suma_notas= 0
            suma_creditos = 0
            numero_notas_validas = 0
            
            for materia in materias_estudiante:

               
                if materia["retirada"].lower() == "no" and materia["creditos"] >= 1 and materia["facultad"] == facultad :
                    if contando_externos == True:
                        suma_notas += materia["nota"]*materia["creditos"]
                        suma_creditos += materia["creditos"]
                        numero_notas_validas += 1
                    else:
                        if info[estudiante]["programa"] == materia["codigo"][0:4] and str(estudiante)[4:6] !="05":
                            suma_notas += materia["nota"]*materia["creditos"]
                            suma_creditos += materia["creditos"]
                            numero_notas_validas += 1


            if numero_notas_validas > 0:
                promedio =suma_notas/suma_creditos
                notas_facultad[estudiante] = (suma_notas,suma_creditos)
    
        facultades_notas[facultad] = notas_facultad
    return facultades_notas    


def extraer_facultades (info:dict):
    facultades = set()
    for estudiante in info: 
        materias_estudiante = info[estudiante]["materias"]  
        for materia in materias_estudiante:
            facultades.add(materia["facultad"])           
    return facultades
    
        
def calcular_nombres (nombre_completo: str)->int:
    #nombre completo dividir por espacios y guardarlo en una tupla
    #calcular la longitud de la lista
    
    #retornar la longitud
    numerar_nombres= nombre_completo.split()
    cantidad_nombres = len(numerar_nombres)
    return cantidad_nombres, numerar_nombres

def armar_correos (estudiante: dict):
    nombre = estudiante["nombres"]
    apellido = estudiante["apellidos"]
    
    
    documento = str(estudiante["documento"])
    
    fin = len(documento)
    ini = len(documento)-2
            
    subdocumento_correo= documento[ini:fin]
    
    subnombre= calcular_nombres(nombre)
    cantidad_nombres= subnombre[0]
    nombres_separados = subnombre[1]
    primeraLetraPN= nombres_separados[0]
    
    apellidos_separados = calcular_nombres(apellido)[1]
    primerApellido= apellidos_separados[1]
    SegundoApellido= apellidos_separados[0]
    # si tiene dos nombres iniciales= {primera letra del primer nombre}{primera letra del segundo nombre}.{e
    # primer apellido y dos ultimos numero del documento
   
   
    if cantidad_nombres >1:
        primeraLetraSN= nombres_separados[1]
        correo= primeraLetraPN[0] +  primeraLetraSN[0]+'.' + primerApellido + subdocumento_correo
    else:
        # si tiene un nombre = inicial del primer nombre y primera letra primer apellido
        # segundo apellido y dos ultimos numeros del documento
        correo= primeraLetraPN[0] + primerApellido[0] +'.'+ SegundoApellido + subdocumento_correo
        
    correo = correo.lower()    
    correo = correo.replace(",","").replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u").replace("ñ","n")
    
    return correo



'''
CONSIDERACIONES IMPORTANTES PARA LOS CORREOS ELECTRÓNICOS:
* No debe tener duplicados
* Debe estar completamente en minúsculas
* No debe tener acentos

EL PROMEDIO DE LA FACULTAD: 
* Debe reportarse redondeado a dos decimales
* No debe considerar las materias retiradas
* Si contando_externos es False, no debe considerar materias electivas ni vacacionales
'''

# Prueba 1:
print(promedio_facultades({
					20170136837:{
								"nombres" : "Jorge Juan",
								"apellidos" : "Moreno, López",
								"documento" : 88481595,
								"programa" : "ARQU",
								"materias" : [
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-8218",
												"nota" : 4.49,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-2113",
												"nota" : 2.97,
												"creditos" : 2,
												"retirada" : "Si",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-5048",
												"nota" : 4.26,
												"creditos" : 0,
												"retirada" : "No",
												},
											]
								},
					20130225137:{
								"nombres" : "Sara Carolina",
								"apellidos" : "Gómez, Fernández",
								"documento" : 58770043,
								"programa" : "ARQD",
								"materias" : [
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-7738",
												"nota" : 3.36,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-9115",
												"nota" : 2.62,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-7698",
												"nota" : 1.59,
												"creditos" : 4,
												"retirada" : "Si",
												},
											]
								},
					20110274333:{
								"nombres" : "Carolina Paula",
								"apellidos" : "Ochoa, López",
								"documento" : 82364435,
								"programa" : "DIMD",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-7972",
												"nota" : 3.15,
												"creditos" : 1,
												"retirada" : "No",
												},
											]
								},
					20200116062:{
								"nombres" : "Sara Camila",
								"apellidos" : "Martínez, Gómez",
								"documento" : 40079000,
								"programa" : "DIGR",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-9331",
												"nota" : 4.0,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-3530",
												"nota" : 3.4,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-8548",
												"nota" : 3.1,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-9771",
												"nota" : 3.91,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20100379147:{
								"nombres" : "Jorge Juan",
								"apellidos" : "Romero, López",
								"documento" : 39344921,
								"programa" : "DIGR",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-9511",
												"nota" : 2.38,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-6043",
												"nota" : 3.71,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-1720",
												"nota" : 2.5,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20200126220:{
								"nombres" : "Sofia",
								"apellidos" : "Cordoba, Romero",
								"documento" : 90333325,
								"programa" : "IQUI",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "IQUI-4982",
												"nota" : 4.57,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IQUI-4982",
												"nota" : 2.8,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IQUI-6947",
												"nota" : 2.47,
												"creditos" : 3,
												"retirada" : "Si",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IQUI-2248",
												"nota" : 3.43,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20130271126:{
								"nombres" : "Gabriela",
								"apellidos" : "Alvarez, García",
								"documento" : 72857337,
								"programa" : "ARQU",
								"materias" : [
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-4963",
												"nota" : 3.15,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-2113",
												"nota" : 3.9,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-1221",
												"nota" : 4.37,
												"creditos" : 4,
												"retirada" : "No",
												},
											]
								},
					20160219974:{
								"nombres" : "Daniela Sara",
								"apellidos" : "Cuellar, Guitiérrez",
								"documento" : 80398132,
								"programa" : "IIND",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "IIND-3557",
												"nota" : 3.91,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IIND-5158",
												"nota" : 3.83,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IIND-7543",
												"nota" : 3.41,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20190264705:{
								"nombres" : "Julio Nicolas",
								"apellidos" : "Fernández, Ramírez",
								"documento" : 42697671,
								"programa" : "DIIN",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-7888",
												"nota" : 4.68,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20150222512:{
								"nombres" : "Mateo Gabriel",
								"apellidos" : "Niño, Romero",
								"documento" : 12964051,
								"programa" : "DIMD",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-3683",
												"nota" : 3.6,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-4014",
												"nota" : 3.15,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-1670",
												"nota" : 4.75,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					}))
# Expected return:
# ({'Arquitectura': 3.81, 'Diseño': 3.58, 'Ingenieria': 3.63, 'Medicina': 3.08}, ['cp.lopez35', 'ds.guitierrez32', 'gg.alvarez37', 'jj.lopez21', 'jj.lopez95', 'jn.ramirez71', 'mg.romero51', 'sc.fernandez43', 'sc.gomez00', 'sr.cordoba25'])

# Prueba 2:
print(promedio_facultades({
					20170116008:{
								"nombres" : "Sofia Natalia",
								"apellidos" : "Martinez, Alvarez",
								"documento" : 86056697,
								"programa" : "HAMO",
								"materias" : [
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-3145",
												"nota" : 3.79,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-1882",
												"nota" : 3.02,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-4916",
												"nota" : 3.99,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-9576",
												"nota" : 3.2,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IIND-7401",
												"nota" : 4.08,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20180181912:{
								"nombres" : "Julian Andres",
								"apellidos" : "Fernández, Gómez",
								"documento" : 38203099,
								"programa" : "ARQD",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-4822",
												"nota" : 3.99,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-6559",
												"nota" : 3.09,
												"creditos" : 1,
												"retirada" : "No",
												},
											]
								},
					20170131506:{
								"nombres" : "Laura Camila",
								"apellidos" : "Cuellar, Pérez",
								"documento" : 15755411,
								"programa" : "MENF",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-7857",
												"nota" : 3.19,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-1857",
												"nota" : 2.62,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-1415",
												"nota" : 2.83,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-1720",
												"nota" : 2.58,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20100240601:{
								"nombres" : "Andres Julian",
								"apellidos" : "Ochoa, Romero",
								"documento" : 81959788,
								"programa" : "IBIO",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-7472",
												"nota" : 3.6,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-5465",
												"nota" : 2.58,
												"creditos" : 2,
												"retirada" : "Si",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-8357",
												"nota" : 4.69,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-9511",
												"nota" : 2.51,
												"creditos" : 3,
												"retirada" : "Si",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-3379",
												"nota" : 4.31,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20160386484:{
								"nombres" : "Julio",
								"apellidos" : "Sánchez, Fernández",
								"documento" : 95423746,
								"programa" : "HART",
								"materias" : [
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-3008",
												"nota" : 2.83,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-3008",
												"nota" : 2.53,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-2620",
												"nota" : 4.06,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20190365550:{
								"nombres" : "Catalina Valentina",
								"apellidos" : "García, López",
								"documento" : 88933669,
								"programa" : "MENF",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-5278",
												"nota" : 3.45,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-1857",
												"nota" : 4.56,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-9835",
												"nota" : 3.93,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-9442",
												"nota" : 4.46,
												"creditos" : 0,
												"retirada" : "No",
												},
											]
								},
					20150173830:{
								"nombres" : "Catalina Valentina",
								"apellidos" : "Fernández, Guitiérrez",
								"documento" : 36216549,
								"programa" : "DISE",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-3520",
												"nota" : 2.71,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-5596",
												"nota" : 4.7,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-6981",
												"nota" : 2.79,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-5596",
												"nota" : 2.51,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-5161",
												"nota" : 2.36,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20100383099:{
								"nombres" : "Juan Pablo",
								"apellidos" : "Moreno, Cordoba",
								"documento" : 17911136,
								"programa" : "ARQD",
								"materias" : [
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-9115",
												"nota" : 4.18,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-6074",
												"nota" : 3.73,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20090198116:{
								"nombres" : "Sofia Gabriela",
								"apellidos" : "Diaz, Moreno",
								"documento" : 62587112,
								"programa" : "ICIV",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-1157",
												"nota" : 2.45,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-7915",
												"nota" : 4.17,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-5962",
												"nota" : 4.49,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20190262931:{
								"nombres" : "Paula Natalia",
								"apellidos" : "Torres, Jiménez",
								"documento" : 18534577,
								"programa" : "HART",
								"materias" : [
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-2081",
												"nota" : 4.43,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-8458",
												"nota" : 4.77,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-1258",
												"nota" : 3.15,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20190299456:{
								"nombres" : "Natalia Paula",
								"apellidos" : "Moreno, Alvarez",
								"documento" : 89771722,
								"programa" : "DIMD",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-7322",
												"nota" : 4.27,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-5808",
												"nota" : 3.19,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-4470",
												"nota" : 2.26,
												"creditos" : 4,
												"retirada" : "Si",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-7972",
												"nota" : 3.66,
												"creditos" : 1,
												"retirada" : "No",
												},
											]
								},
					20150172603:{
								"nombres" : "Catalina Paula",
								"apellidos" : "Pérez, Diaz",
								"documento" : 59641117,
								"programa" : "IBIO",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-8636",
												"nota" : 4.65,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-1999",
												"nota" : 2.52,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-3063",
												"nota" : 2.95,
												"creditos" : 4,
												"retirada" : "No",
												},
											]
								},
					20160197253:{
								"nombres" : "Julian Mateo",
								"apellidos" : "Jiménez, Fernández",
								"documento" : 41016120,
								"programa" : "MEDI",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-9348",
												"nota" : 4.55,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-9306",
												"nota" : 2.77,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-1836",
												"nota" : 3.66,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20160174103:{
								"nombres" : "Mateo Julio",
								"apellidos" : "Diaz, López",
								"documento" : 88132707,
								"programa" : "IBIO",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-2104",
												"nota" : 4.55,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-3425",
												"nota" : 3.98,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-4686",
												"nota" : 4.97,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-9455",
												"nota" : 2.43,
												"creditos" : 0,
												"retirada" : "Si",
												},
											]
								},
					20150384070:{
								"nombres" : "Carolina Natalia",
								"apellidos" : "López, Gómez",
								"documento" : 33424549,
								"programa" : "DIMD",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-7322",
												"nota" : 2.49,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-4101",
												"nota" : 3.14,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-8021",
												"nota" : 2.97,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-7470",
												"nota" : 4.77,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					}, False ))
# Expected return:
# ({'Arquitectura': 3.84, 'Diseño': 3.37, 'Historia del Arte': 3.66, 'Ingenieria': 3.88, 'Medicina': 3.45}, ['aj.romero88', 'cn.gomez49', 'cp.diaz17', 'cv.guitierrez49', 'cv.lopez69', 'jf.sanchez46', 'jm.fernandez20', 'jp.cordoba36', 'lc.perez11', 'mj.lopez07', 'np.alvarez22', 'pn.jimenez77', 'sg.moreno12', 'sn.alvarez97'])

# Prueba 3:
print(promedio_facultades({
					20180258748:{
								"nombres" : "Laura Carolina",
								"apellidos" : "Cuellar, Martínez",
								"documento" : 56903142,
								"programa" : "IIND",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "IIND-7343",
												"nota" : 3.42,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IIND-9484",
												"nota" : 4.06,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IIND-7543",
												"nota" : 3.55,
												"creditos" : 3,
												"retirada" : "Si",
												},
											]
								},
					20200161520:{
								"nombres" : "Gabriela Maria",
								"apellidos" : "Torres, Torres",
								"documento" : 33383264,
								"programa" : "HART",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "IIND-5406",
												"nota" : 3.38,
												"creditos" : 3,
												"retirada" : "Si",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-8321",
												"nota" : 4.5,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-8634",
												"nota" : 2.43,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20180275516:{
								"nombres" : "Camila Maria",
								"apellidos" : "Pardo, Moreno",
								"documento" : 16460416,
								"programa" : "MEDI",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-8291",
												"nota" : 3.63,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-6474",
												"nota" : 3.91,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-6559",
												"nota" : 4.87,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-6400",
												"nota" : 3.98,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20130237460:{
								"nombres" : "Sara Daniela",
								"apellidos" : "Fernández, Pérez",
								"documento" : 50851757,
								"programa" : "DIGR",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-9511",
												"nota" : 2.88,
												"creditos" : 3,
												"retirada" : "Si",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-7820",
												"nota" : 4.5,
												"creditos" : 0,
												"retirada" : "No",
												},
											]
								},
					20150225965:{
								"nombres" : "Catalina Sara",
								"apellidos" : "Pérez, Fernández",
								"documento" : 56904845,
								"programa" : "DIGR",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-7820",
												"nota" : 2.6,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-9590",
												"nota" : 3.45,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-1863",
												"nota" : 3.73,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-7837",
												"nota" : 2.42,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-2013",
												"nota" : 2.77,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20150220803:{
								"nombres" : "Laura Gabriela",
								"apellidos" : "Moreno, Álvarez",
								"documento" : 23932358,
								"programa" : "ICIV",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-5962",
												"nota" : 2.56,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-6796",
												"nota" : 3.71,
												"creditos" : 2,
												"retirada" : "Si",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-7476",
												"nota" : 4.82,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20150137119:{
								"nombres" : "Camilo Oscar",
								"apellidos" : "Pérez, Álvarez",
								"documento" : 70531411,
								"programa" : "HART",
								"materias" : [
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-2388",
												"nota" : 4.1,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-8458",
												"nota" : 2.52,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-4558",
												"nota" : 2.15,
												"creditos" : 2,
												"retirada" : "Si",
												},
											]
								},
					20200255611:{
								"nombres" : "Mateo",
								"apellidos" : "Ochoa, Gómez",
								"documento" : 88455293,
								"programa" : "ICIV",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-4627",
												"nota" : 2.4,
												"creditos" : 3,
												"retirada" : "Si",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-5019",
												"nota" : 3.97,
												"creditos" : 4,
												"retirada" : "No",
												},
											]
								},
					20180243721:{
								"nombres" : "Julio Julián",
								"apellidos" : "Guitiérrez, Gómez",
								"documento" : 82734307,
								"programa" : "DIIN",
								"materias" : [
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-8894",
												"nota" : 4.73,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-4822",
												"nota" : 2.56,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-2252",
												"nota" : 2.83,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20170128822:{
								"nombres" : "Catalina Camila",
								"apellidos" : "Cuellar, Suárez",
								"documento" : 50244386,
								"programa" : "DIMD",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-4014",
												"nota" : 4.46,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-7470",
												"nota" : 3.05,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-2531",
												"nota" : 2.42,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-5945",
												"nota" : 4.99,
												"creditos" : 4,
												"retirada" : "No",
												},
											]
								},
					20170250887:{
								"nombres" : "Andres Gabriel",
								"apellidos" : "Romero, Fernández",
								"documento" : 59716178,
								"programa" : "HAMO",
								"materias" : [
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-1258",
												"nota" : 4.19,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-1938",
												"nota" : 3.69,
												"creditos" : 2,
												"retirada" : "Si",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-3145",
												"nota" : 4.8,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-3743",
												"nota" : 4.2,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-2432",
												"nota" : 3.07,
												"creditos" : 1,
												"retirada" : "No",
												},
											]
								},
					20110264007:{
								"nombres" : "Julián Daniel",
								"apellidos" : "López, Niño",
								"documento" : 32543959,
								"programa" : "ARQU",
								"materias" : [
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-8743",
												"nota" : 2.53,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-5122",
												"nota" : 2.39,
												"creditos" : 3,
												"retirada" : "Si",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-1033",
												"nota" : 3.82,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-7824",
												"nota" : 2.37,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20150132819:{
								"nombres" : "Camila Gabriela",
								"apellidos" : "Romero, Hernández",
								"documento" : 27075752,
								"programa" : "IBIO",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "IIND-9454",
												"nota" : 2.73,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-8357",
												"nota" : '4,54',
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-3425",
												"nota" : 4.69,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IIND-9454",
												"nota" : 3.04,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20180354205:{
								"nombres" : "Nicolas Andres",
								"apellidos" : "Jiménez, López",
								"documento" : 36852757,
								"programa" : "DIMD",
								"materias" : [
											]
								},
					20150144454:{
								"nombres" : "Daniel Andres",
								"apellidos" : "Ramírez, Álvarez",
								"documento" : 18621326,
								"programa" : "IIND",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "IIND-3557",
												"nota" : 2.65,
												"creditos" : 1,
												"retirada" : "No",
												},
											]
								},
					20200161348:{
								"nombres" : "Camila Paula",
								"apellidos" : "Jiménez, Jiménez",
								"documento" : 95052431,
								"programa" : "MEDI",
								"materias" : [
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-8607",
												"nota" : 2.78,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-4689",
												"nota" : 2.68,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20170313423:{
								"nombres" : "Mateo Andres",
								"apellidos" : "Córdoba, Pérez",
								"documento" : 34429692,
								"programa" : "DIMD",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-4470",
												"nota" : 2.77,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-7107",
												"nota" : 3.17,
												"creditos" : 4,
												"retirada" : "No",
												},
											]
								},
					20170326003:{
								"nombres" : "Camila Laura",
								"apellidos" : "Moreno, Fernández",
								"documento" : 68731744,
								"programa" : "IIND",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "IIND-5406",
												"nota" : 2.59,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-5433",
												"nota" : 3.18,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IIND-5055",
												"nota" : 3.96,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-3008",
												"nota" : 3.76,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20170365049:{
								"nombres" : "Camila Andrea",
								"apellidos" : "Jiménez, López",
								"documento" : 58154488,
								"programa" : "DISE",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-6981",
												"nota" : 3.82,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-6515",
												"nota" : 2.98,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-5596",
												"nota" : 3.07,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-5596",
												"nota" : 2.75,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20180341955:{
								"nombres" : "Sara Maria",
								"apellidos" : "Guitiérrez, Moreno",
								"documento" : 74599213,
								"programa" : "IIND",
								"materias" : [
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-2619",
												"nota" : 3.9,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IIND-9208",
												"nota" : 2.34,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IIND-1447",
												"nota" : 3.14,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20180158352:{
								"nombres" : "Mateo Nicolas",
								"apellidos" : "Sánchez, Hernández",
								"documento" : 48956920,
								"programa" : "HART",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-1893",
												"nota" : 4.12,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-4540",
												"nota" : 2.71,
												"creditos" : 4,
												"retirada" : "No",
												},
											]
								},
					20130175938:{
								"nombres" : "Julián Oscar",
								"apellidos" : "Torres, Ramírez",
								"documento" : 79099097,
								"programa" : "HART",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-4328",
												"nota" : 2.96,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-4558",
												"nota" : 2.41,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-7452",
												"nota" : 3.74,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-5285",
												"nota" : 1.72,
												"creditos" : 0,
												"retirada" : "Si",
												},
											]
								},
					20170125563:{
								"nombres" : "Laura Maria",
								"apellidos" : "López, Ramírez",
								"documento" : 90235907,
								"programa" : "DIIN",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-4067",
												"nota" : 2.91,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-6616",
												"nota" : 2.51,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-4773",
												"nota" : 4.85,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-2390",
												"nota" : 2.69,
												"creditos" : 0,
												"retirada" : "No",
												},
											]
								},
					20190134014:{
								"nombres" : "Jorge Mateo",
								"apellidos" : "Fernández, García",
								"documento" : 92067080,
								"programa" : "ARQD",
								"materias" : [
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-5194",
												"nota" : 3.54,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-8904",
												"nota" : 4.51,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-9114",
												"nota" : 3.07,
												"creditos" : 3,
												"retirada" : "Si",
												},
											]
								},
					20170273043:{
								"nombres" : "Camila Maria",
								"apellidos" : "Álvarez, Díaz",
								"documento" : 48481864,
								"programa" : "DIIN",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-1173",
												"nota" : 4.4,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-6748",
												"nota" : 3.15,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-9865",
												"nota" : 4.79,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-5441",
												"nota" : 4.76,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-3583",
												"nota" : 3.71,
												"creditos" : 4,
												"retirada" : "No",
												},
											]
								},
					20170272657:{
								"nombres" : "Laura Camila",
								"apellidos" : "Fernández, Gómez",
								"documento" : 38458203,
								"programa" : "HAMO",
								"materias" : [
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-7286",
												"nota" : 4.45,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-7667",
												"nota" : 3.54,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20140240515:{
								"nombres" : "Camila Catalina",
								"apellidos" : "Niño, López",
								"documento" : 72978501,
								"programa" : "DIMD",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-7666",
												"nota" : 2.89,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-6337",
												"nota" : 4.36,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-4067",
												"nota" : 4.6,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20110361896:{
								"nombres" : "Nicolas Gabriel",
								"apellidos" : "Jiménez, Martínez",
								"documento" : 24390101,
								"programa" : "ARQD",
								"materias" : [
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-2553",
												"nota" : 2.88,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-3843",
												"nota" : 2.81,
												"creditos" : 0,
												"retirada" : "Si",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-1864",
												"nota" : 2.61,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-5405",
												"nota" : 4.29,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20140530242:{
								"nombres" : "Daniela Sofia",
								"apellidos" : "García, Ramírez",
								"documento" : 51195781,
								"programa" : "IIND",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "IIND-5821",
												"nota" : 3.83,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IIND-4333",
												"nota" : 3.59,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20190357498:{
								"nombres" : "Valentina Catalina",
								"apellidos" : "Suárez, Niño",
								"documento" : 12006504,
								"programa" : "ISIS",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-4305",
												"nota" : 2.55,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-6565",
												"nota" : 2.75,
												"creditos" : 3,
												"retirada" : "Si",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-7601",
												"nota" : 4.31,
												"creditos" : 0,
												"retirada" : "No",
												},
											]
								},
					20160234611:{
								"nombres" : "Andrea Sofia",
								"apellidos" : "Niño, Ramírez",
								"documento" : 99066142,
								"programa" : "DISE",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-6026",
												"nota" : 4.02,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-9206",
												"nota" : 4.13,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-5161",
												"nota" : 3.63,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-1821",
												"nota" : 2.8,
												"creditos" : 4,
												"retirada" : "No",
												},
											]
								},
					20180231918:{
								"nombres" : "Camila",
								"apellidos" : "Cuellar, Díaz",
								"documento" : 76315685,
								"programa" : "MENF",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-4810",
												"nota" : 3.25,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-4702",
												"nota" : 3.02,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-9442",
												"nota" : 2.83,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-2072",
												"nota" : 3.2,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-8291",
												"nota" : 4.37,
												"creditos" : 1,
												"retirada" : "No",
												},
											]
								},
					20100134260:{
								"nombres" : "Andres Mateo",
								"apellidos" : "Martínez, Álvarez",
								"documento" : 14991799,
								"programa" : "DIIN",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-7926",
												"nota" : 3.73,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-9865",
												"nota" : 3.52,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20200245086:{
								"nombres" : "Maria Catalina",
								"apellidos" : "Ramírez, Sánchez",
								"documento" : 93214275,
								"programa" : "DIIN",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-9838",
												"nota" : 3.51,
												"creditos" : '2',
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IQUI-5835",
												"nota" : 3.53,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-1652",
												"nota" : 3.67,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-5158",
												"nota" : 4.7,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-7888",
												"nota" : 2.47,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20190536642:{
								"nombres" : "Mateo Pablo",
								"apellidos" : "Ramírez, Pérez",
								"documento" : 51730947,
								"programa" : "DISE",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-9838",
												"nota" : 3.98,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-6777",
												"nota" : 4.84,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-8797",
												"nota" : 2.62,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20090357760:{
								"nombres" : "Jose Pablo",
								"apellidos" : "Álvarez, Romero",
								"documento" : 93191384,
								"programa" : "HAMO",
								"materias" : [
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-5327",
												"nota" : 3.4,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-9435",
												"nota" : 2.66,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-7355",
												"nota" : 3.88,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-6328",
												"nota" : 4.69,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-1069",
												"nota" : 4.22,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20200383664:{
								"nombres" : "Catalina Andrea",
								"apellidos" : "Moreno, Cuellar",
								"documento" : 51313239,
								"programa" : "MEDI",
								"materias" : [
											]
								},
					20090116467:{
								"nombres" : "Nicolas Gabriel",
								"apellidos" : "García, Fernández",
								"documento" : 52393411,
								"programa" : "HAMO",
								"materias" : [
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-7665",
												"nota" : 4.26,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-8607",
												"nota" : 3.18,
												"creditos" : 0,
												"retirada" : "Si",
												},
											]
								},
					20120243135:{
								"nombres" : "Oscar Andres",
								"apellidos" : "Guitiérrez, Ochoa",
								"documento" : 29004076,
								"programa" : "IBIO",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-8942",
												"nota" : 3.15,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-5266",
												"nota" : 2.79,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20200295005:{
								"nombres" : "Camila Sara",
								"apellidos" : "Fernández, Cuellar",
								"documento" : 72005742,
								"programa" : "MENF",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-5889",
												"nota" : 4.28,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-9442",
												"nota" : 2.56,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-6067",
												"nota" : 3.6,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-1415",
												"nota" : 2.73,
												"creditos" : 3,
												"retirada" : "Si",
												},
											]
								},
					20170186478:{
								"nombres" : "Jose",
								"apellidos" : "López, Moreno",
								"documento" : 11640390,
								"programa" : "DIIN",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-7915",
												"nota" : 4.92,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-3136",
												"nota" : 4.38,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-7888",
												"nota" : 1.81,
												"creditos" : 2,
												"retirada" : "Si",
												},
											]
								},
					20200133687:{
								"nombres" : "Laura Daniela",
								"apellidos" : "Ramírez, Fernández",
								"documento" : 79751620,
								"programa" : "ARQD",
								"materias" : [
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-6822",
												"nota" : 3.75,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-6074",
												"nota" : 3.33,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20120175303:{
								"nombres" : "Natalia Catalina",
								"apellidos" : "Cuellar, Córdoba",
								"documento" : 95268184,
								"programa" : "MEDI",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-6559",
												"nota" : 3.3,
												"creditos" : 1,
												"retirada" : "Si",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-2339",
												"nota" : 4.69,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20110158990:{
								"nombres" : "Maria Carolina",
								"apellidos" : "Romero, García",
								"documento" : 93538878,
								"programa" : "IBIO",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-1999",
												"nota" : 3.52,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IIND-2514",
												"nota" : 2.65,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-4686",
												"nota" : 3.28,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20140139618:{
								"nombres" : "Oscar Mateo",
								"apellidos" : "Martínez, Hernández",
								"documento" : 68038752,
								"programa" : "IBIO",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-8544",
												"nota" : 3.02,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IIND-8074",
												"nota" : 3.08,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IIND-8672",
												"nota" : 3.59,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-4502",
												"nota" : 3.73,
												"creditos" : 3,
												"retirada" : "Si",
												},
											]
								},
					} ))
# Expected return:
# 'Error numérico.'

# Prueba 4
print(promedio_facultades({
					20200389418:{
								"nombres" : "Carolina Camila",
								"apellidos" : "Martínez, Jiménez",
								"documento" : 28762912,
								"programa" : "ARQU",
								"materias" : [
											]
								},
					20180218013:{
								"nombres" : "Julio Nicolas",
								"apellidos" : "Pardo, Ramírez",
								"documento" : 77780207,
								"programa" : "ISIS",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-2485",
												"nota" : 4.49,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-6565",
												"nota" : 2.44,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-2485",
												"nota" : 4.17,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-6565",
												"nota" : 1.93,
												"creditos" : 3,
												"retirada" : "Si",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-6565",
												"nota" : 3.29,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20120153166:{
								"nombres" : "Maria Camila",
								"apellidos" : "Gómez, Suárez",
								"documento" : 13060098,
								"programa" : "MEDI",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-6474",
												"nota" : 4.48,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-1652",
												"nota" : 3.63,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-9490",
												"nota" : 3.61,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-8458",
												"nota" : 3.0,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20180294370:{
								"nombres" : "Andres Oscar",
								"apellidos" : "Martínez, Guitiérrez",
								"documento" : 38221530,
								"programa" : "DISE",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-5161",
												"nota" : 3.18,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-4199",
												"nota" : 3.31,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-2553",
												"nota" : 2.67,
												"creditos" : 4,
												"retirada" : "No",
												},
											]
								},
					20180174629:{
								"nombres" : "Oscar Juan",
								"apellidos" : "Martínez, Gómez",
								"documento" : 34690377,
								"programa" : "ARQU",
								"materias" : [
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-1033",
												"nota" : 4.32,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-8159",
												"nota" : 3.06,
												"creditos" : 3,
												"retirada" : "Si",
												},
											]
								},
					20170370686:{
								"nombres" : "Natalia Camila",
								"apellidos" : "Torres, Sánchez",
								"documento" : 25039805,
								"programa" : "HAMO",
								"materias" : [
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-5327",
												"nota" : 3.65,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-7667",
												"nota" : 3.46,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20120156530:{
								"nombres" : "Camilo Gabriel",
								"apellidos" : "Moreno, Ochoa",
								"documento" : 54472182,
								"programa" : "MENF",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-9442",
												"nota" : 2.79,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-9962",
												"nota" : 3.09,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-1163",
												"nota" : 4.22,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-5889",
												"nota" : 3.93,
												"creditos" : 0,
												"retirada" : "No",
												},
											]
								},
					20110118150:{
								"nombres" : "Sara Natalia",
								"apellidos" : "Jiménez, Niño",
								"documento" : 59028529,
								"programa" : "ARQD",
								"materias" : [
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-4773",
												"nota" : 2.87,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20130160334:{
								"nombres" : "Pablo Oscar",
								"apellidos" : "García, Cuellar",
								"documento" : 45422646,
								"programa" : "MEDI",
								"materias" : [
											]
								},
					20190127090:{
								"nombres" : "Natalia Andrea",
								"apellidos" : "Romero, Álvarez",
								"documento" : 14645452,
								"programa" : "HAMO",
								"materias" : [
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-6565",
												"nota" : 3.63,
												"creditos" : 4,
												"retirada" : "No",
												},
											]
								},
					20170399947:{
								"nombres" : "Nicolas Oscar",
								"apellidos" : "Hernández, Sánchez",
								"documento" : 91484557,
								"programa" : "HART",
								"materias" : [
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-1069",
												"nota" : 4.96,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-5285",
												"nota" : 3.81,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-9958",
												"nota" : 3.48,
												"creditos" : 4,
												"retirada" : "No",
												},
											]
								},
					20100179298:{
								"nombres" : "Camila Gabriela",
								"apellidos" : "Cuellar, Torres",
								"documento" : 96827835,
								"programa" : "DIGR",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-7820",
												"nota" : 3.52,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-1771",
												"nota" : 2.98,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-3496",
												"nota" : 4.97,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20190365476:{
								"nombres" : "Daniela Laura",
								"apellidos" : "Ramírez, Ramírez",
								"documento" : 61089799,
								"programa" : "HAMO",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-4547",
												"nota" : 3.52,
												"creditos" : 0,
												"retirada" : "Si",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-9958",
												"nota" : 3.09,
												"creditos" : 4,
												"retirada" : "Si",
												},
											]
								},
					20090262678:{
								"nombres" : "Daniela Gabriela",
								"apellidos" : "Martínez, Pérez",
								"documento" : 96124452,
								"programa" : "DISE",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-6229",
												"nota" : 3.94,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-1893",
												"nota" : 4.49,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-9206",
												"nota" : 2.9,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20100171092:{
								"nombres" : "Nicolas",
								"apellidos" : "Córdoba, Martínez",
								"documento" : 72480454,
								"programa" : "DIMD",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-5808",
												"nota" : 3.39,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-6433",
												"nota" : 3.79,
												"creditos" : 3,
												"retirada" : "Si",
												},
											]
								},
					20190289451:{
								"nombres" : "Oscar Nicolas",
								"apellidos" : "Pérez, Pérez",
								"documento" : 59881117,
								"programa" : "ARQD",
								"materias" : [
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-1864",
												"nota" : 3.98,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-5433",
												"nota" : 4.66,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-6074",
												"nota" : 4.73,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20140165504:{
								"nombres" : "Jose Andres",
								"apellidos" : "López, Cuellar",
								"documento" : 15055406,
								"programa" : "DIIN",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-3496",
												"nota" : 4.64,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-4482",
												"nota" : 2.82,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-9838",
												"nota" : 2.59,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-5808",
												"nota" : 3.82,
												"creditos" : 0,
												"retirada" : "No",
												},
											]
								},
					20190292166:{
								"nombres" : "Julio Pablo",
								"apellidos" : "Pérez, Martínez",
								"documento" : 26413662,
								"programa" : "DIMD",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-9962",
												"nota" : 1.71,
												"creditos" : 3,
												"retirada" : "Si",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-5273",
												"nota" : 3.31,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IQUI-6551",
												"nota" : 4.8,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-6433",
												"nota" : 3.68,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-8021",
												"nota" : 3.16,
												"creditos" : 4,
												"retirada" : "No",
												},
											]
								},
					20180161244:{
								"nombres" : "Sara Catalina",
								"apellidos" : "Martínez, Guitiérrez",
								"documento" : 98676583,
								"programa" : "ISIS",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-3123",
												"nota" : 3.85,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-3123",
												"nota" : 2.46,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-1419",
												"nota" : 1.95,
												"creditos" : 3,
												"retirada" : "Si",
												},
											]
								},
					20200183107:{
								"nombres" : "Valentina Natalia",
								"apellidos" : "Ramírez, Hernández",
								"documento" : 80930550,
								"programa" : "IBIO",
								"materias" : [
											]
								},
					20160227193:{
								"nombres" : "Camilo Oscar",
								"apellidos" : "López, Ochoa",
								"documento" : 74195269,
								"programa" : "HART",
								"materias" : [
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-2432",
												"nota" : 1.61,
												"creditos" : 1,
												"retirada" : "Si",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-3743",
												"nota" : 3.61,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-9576",
												"nota" : 3.85,
												"creditos" : 1,
												"retirada" : "No",
												},
											]
								},
					20190160404:{
								"nombres" : "Daniela Sofia",
								"apellidos" : "Díaz, Sánchez",
								"documento" : 74241179,
								"programa" : "MENF",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-4060",
												"nota" : 3.51,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-9962",
												"nota" : 2.59,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-5644",
												"nota" : 3.85,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20160125451:{
								"nombres" : "Sofia Paula",
								"apellidos" : "Niño, Niño",
								"documento" : 74237274,
								"programa" : "DIMD",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-3018",
												"nota" : 3.81,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-6433",
												"nota" : 4.29,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-5431",
												"nota" : 3.35,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-7666",
												"nota" : 2.94,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20200250665:{
								"nombres" : "Camila Sofia",
								"apellidos" : "Niño, Suárez",
								"documento" : 91866051,
								"programa" : "HART",
								"materias" : [
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-5285",
												"nota" : 2.7,
												"creditos" : 0,
												"retirada" : "Si",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-1258",
												"nota" : 2.46,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-4996",
												"nota" : 2.98,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-2169",
												"nota" : 1.71,
												"creditos" : 3,
												"retirada" : "Si",
												},
											]
								},
					20130162157:{
								"nombres" : "Julián Nicolas",
								"apellidos" : "López, García",
								"documento" : 16922275,
								"programa" : "DISE",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-6613",
												"nota" : 4.73,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-9978",
												"nota" : 4.36,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-6981",
												"nota" : 2.75,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-6229",
												"nota" : 2.41,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-1869",
												"nota" : 4.93,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20180118534:{
								"nombres" : "Laura Daniela",
								"apellidos" : "Niño, Córdoba",
								"documento" : 37558115,
								"programa" : "ARQU",
								"materias" : [
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-8218",
												"nota" : 2.94,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-6624",
												"nota" : 3.76,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-5122",
												"nota" : 3.5,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-4199",
												"nota" : 3.91,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20190267586:{
								"nombres" : "Camila Daniela",
								"apellidos" : "Álvarez, Álvarez",
								"documento" : 50614954,
								"programa" : "ISIS",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-8212",
												"nota" : 4.76,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-4155",
												"nota" : 3.1,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-3123",
												"nota" : 4.07,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20180116791:{
								"nombres" : "Laura Gabriela",
								"apellidos" : "Guitiérrez, Martínez",
								"documento" : 67795888,
								"programa" : "MENF",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-7325",
												"nota" : 2.99,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-9306",
												"nota" : 4.25,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-9241",
												"nota" : 3.84,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-4060",
												"nota" : 4.74,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20180213265:{
								"nombres" : "Sara Camila",
								"apellidos" : "Moreno, Torres",
								"documento" : 21130593,
								"programa" : "MENF",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-1720",
												"nota" : 3.03,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-1857",
												"nota" : 4.31,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-6822",
												"nota" : 4.25,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20130340473:{
								"nombres" : "Daniela Laura",
								"apellidos" : "Fernández, Álvarez",
								"documento" : 76404118,
								"programa" : "ARQD",
								"materias" : [
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-7589",
												"nota" : 3.57,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-1269",
												"nota" : 3.87,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-8768",
												"nota" : 3.64,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20160352144:{
								"nombres" : "Andrea Paula",
								"apellidos" : "López, Pardo",
								"documento" : 79485645,
								"programa" : "HART",
								"materias" : [
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-1938",
												"nota" : 3.44,
												"creditos" : 2,
												"retirada" : "Si",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-4567",
												"nota" : 4.87,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-4567",
												"nota" : 2.61,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-7530",
												"nota" : 2.57,
												"creditos" : 0,
												"retirada" : "Si",
												},
											]
								},
					20130171737:{
								"nombres" : "Daniela Carolina",
								"apellidos" : "Pérez, Ochoa",
								"documento" : 67301690,
								"programa" : "DIGR",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-4067",
												"nota" : 4.08,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-8825",
												"nota" : 3.98,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-3496",
												"nota" : 2.87,
												"creditos" : 3,
												"retirada" : "Si",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-7239",
												"nota" : 2.62,
												"creditos" : 3,
												"retirada" : "Si",
												},
											]
								},
					20180257403:{
								"nombres" : "Paula Natalia",
								"apellidos" : "Gómez, Álvarez",
								"documento" : 73674960,
								"programa" : "DISE",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-1893",
												"nota" : 2.4,
												"creditos" : 3,
												"retirada" : "Si",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-8201",
												"nota" : 3.56,
												"creditos" : 3,
												"retirada" : "Si",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-4446",
												"nota" : 2.6,
												"creditos" : 0,
												"retirada" : "No",
												},
											]
								},
					20100172903:{
								"nombres" : "Oscar Julián",
								"apellidos" : "Martínez, García",
								"documento" : 47005459,
								"programa" : "HAMO",
								"materias" : [
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-6375",
												"nota" : 1.55,
												"creditos" : 2,
												"retirada" : "Si",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-3008",
												"nota" : 3.08,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-7667",
												"nota" : 2.61,
												"creditos" : 2,
												"retirada" : "Si",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-1069",
												"nota" : 2.3,
												"creditos" : 3,
												"retirada" : "Si",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-1069",
												"nota" : 3.17,
												"creditos" : 3,
												"retirada" : "Si",
												},
											]
								},
					20170297929:{
								"nombres" : "Paula Maria",
								"apellidos" : "Jiménez, Suárez",
								"documento" : 63745099,
								"programa" : "ARQD",
								"materias" : [
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-6822",
												"nota" : 4.36,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-2553",
												"nota" : 3.88,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-7738",
												"nota" : 4.75,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-1670",
												"nota" : 3.29,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20160156628:{
								"nombres" : "Juan",
								"apellidos" : "López, Guitiérrez",
								"documento" : 55128400,
								"programa" : "ARQD",
								"materias" : [
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-6195",
												"nota" : 3.57,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-7530",
												"nota" : 3.96,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-1269",
												"nota" : 3.45,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20130266471:{
								"nombres" : "Sara Daniela",
								"apellidos" : "Martínez, Hernández",
								"documento" : 61250000,
								"programa" : "HART",
								"materias" : [
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-6298",
												"nota" : 2.93,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-4540",
												"nota" : 3.55,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-5327",
												"nota" : 3.93,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20140227848:{
								"nombres" : "Jose Nicolas",
								"apellidos" : "Díaz, Romero",
								"documento" : 21403906,
								"programa" : "IQUI",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "IQUI-3859",
												"nota" : 3.94,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IQUI-9815",
												"nota" : 3.68,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IQUI-9702",
												"nota" : 2.7,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IQUI-2859",
												"nota" : 4.05,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20170115295:{
								"nombres" : "Maria Paula",
								"apellidos" : "Córdoba, Ramírez",
								"documento" : 43182695,
								"programa" : "ICIV",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-8615",
												"nota" : 4.43,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-1020",
												"nota" : 3.12,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-1020",
												"nota" : 3.18,
												"creditos" : 4,
												"retirada" : "No",
												},
											]
								},
					20140186272:{
								"nombres" : "Gabriel Nicolas",
								"apellidos" : "Cuellar, López",
								"documento" : 55100972,
								"programa" : "DIMD",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-5413",
												"nota" : 3.69,
												"creditos" : 0,
												"retirada" : "Si",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-8304",
												"nota" : 4.98,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-7666",
												"nota" : 3.23,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-3018",
												"nota" : 3.67,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					} ))
# Expected return:
# ({'Arquitectura': 3.77, 'Diseño': 3.81, 'Historia del Arte': 3.54, 'Ingenieria': 3.58, 'Medicina': 3.71}, ['ao.guitierrez30', 'ap.pardo45', 'cd.alvarez54', 'cg.ochoa82', 'cg.torres35', 'co.ochoa69', 'cs.suarez51', 'dc.ochoa90', 'dg.perez52', 'dl.alvarez18', 'ds.sanchez79', 'gn.lopez72', 'ja.cuellar06', 'jg.lopez00', 'jn.garcia75', 'jn.ramirez07', 'jn.romero06', 'jp.martinez62', 'ld.cordoba15', 'lg.martinez88', 'mc.suarez98', 'mp.ramirez95', 'na.alvarez52', 'nc.sanchez05', 'no.sanchez57', 'oj.garcia59', 'oj.gomez77', 'on.perez17', 'pm.suarez99', 'sc.guitierrez83', 'sc.torres93', 'sd.hernandez00', 'sn.nino29', 'sp.nino74'])

#Prueba 5:
print(promedio_facultades({
					20180234491:{
								"nombres" : "Julio Juan",
								"apellidos" : "López, Cuellar",
								"documento" : 89783030,
								"programa" : "ICIV",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-2983",
												"nota" : 3.65,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-4627",
												"nota" : 3.34,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-6267",
												"nota" : 3.29,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-7182",
												"nota" : 2.83,
												"creditos" : 2,
												"retirada" : "Si",
												},
											]
								},
					20180111599:{
								"nombres" : "Camilo Julián",
								"apellidos" : "Cuellar, Sánchez",
								"documento" : 25501871,
								"programa" : "HART",
								"materias" : [
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-1258",
												"nota" : 3.77,
												"creditos" : 3,
												"retirada" : "Si",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-4066",
												"nota" : 2.76,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-5285",
												"nota" : 3.74,
												"creditos" : 0,
												"retirada" : "Si",
												},
											]
								},
					20130111233:{
								"nombres" : "Camilo Jorge",
								"apellidos" : "Pérez, Díaz",
								"documento" : 68407479,
								"programa" : "MEDI",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-7278",
												"nota" : 2.48,
												"creditos" : 1,
												"retirada" : "Si",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-2625",
												"nota" : 3.52,
												"creditos" : 4,
												"retirada" : "Si",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-2553",
												"nota" : 2.24,
												"creditos" : 3,
												"retirada" : "Si",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-9490",
												"nota" : 4.64,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20180270894:{
								"nombres" : "Camila",
								"apellidos" : "Guitiérrez, Pardo",
								"documento" : 88027774,
								"programa" : "DIIN",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-1626",
												"nota" : 3.99,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-4277",
												"nota" : 4.29,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-2430",
												"nota" : 2.77,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20180221472:{
								"nombres" : "Nicolas Oscar",
								"apellidos" : "Niño, Ramírez",
								"documento" : 83313299,
								"programa" : "ISIS",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-6515",
												"nota" : 2.34,
												"creditos" : 4,
												"retirada" : "Si",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-3961",
												"nota" : 3.19,
												"creditos" : 4,
												"retirada" : "No",
												},
											]
								},
					20170229508:{
								"nombres" : "Daniel Nicolas",
								"apellidos" : "Guitiérrez, Álvarez",
								"documento" : 50548066,
								"programa" : "DIIN",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-6043",
												"nota" : 3.25,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-1173",
												"nota" : 3.66,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-2252",
												"nota" : 2.63,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-8962",
												"nota" : 2.37,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-9838",
												"nota" : 2.43,
												"creditos" : 2,
												"retirada" : "Si",
												},
											]
								},
					20190373561:{
								"nombres" : "Julio Camilo",
								"apellidos" : "Romero, Sánchez",
								"documento" : 89277860,
								"programa" : "HAMO",
								"materias" : [
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-1882",
												"nota" : 3.1,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-9435",
												"nota" : 2.47,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-7355",
												"nota" : 2.57,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-8141",
												"nota" : 2.47,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20200234229:{
								"nombres" : "Mateo Daniel",
								"apellidos" : "Gómez, Díaz",
								"documento" : 92448136,
								"programa" : "HAMO",
								"materias" : [
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-8238",
												"nota" : 2.34,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-9958",
												"nota" : 1.68,
												"creditos" : 4,
												"retirada" : "Si",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-7355",
												"nota" : 2.15,
												"creditos" : 2,
												"retirada" : "Si",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-1882",
												"nota" : 2.88,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20190184788:{
								"nombres" : "Julián Camilo",
								"apellidos" : "Torres, Sánchez",
								"documento" : 28707171,
								"programa" : "ICIV",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-6894",
												"nota" : 4.56,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-2619",
												"nota" : 2.96,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-8615",
												"nota" : 2.76,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20170269592:{
								"nombres" : "Oscar Jorge",
								"apellidos" : "Ramírez, Córdoba",
								"documento" : 51020471,
								"programa" : "HAMO",
								"materias" : [
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-4916",
												"nota" : 2.51,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-3145",
												"nota" : 3.72,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-1882",
												"nota" : 4.96,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-7667",
												"nota" : 1.79,
												"creditos" : 2,
												"retirada" : "Si",
												},
											]
								},
					20080261436:{
								"nombres" : "Sara Camila",
								"apellidos" : "Jiménez, Suárez",
								"documento" : 10308626,
								"programa" : "IQUI",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "IQUI-3859",
												"nota" : 4.14,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IQUI-3745",
												"nota" : 2.81,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20200272073:{
								"nombres" : "Laura Daniela",
								"apellidos" : "Jiménez, Hernández",
								"documento" : 24876698,
								"programa" : "ISIS",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-2276",
												"nota" : 2.98,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-6328",
												"nota" : 2.48,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-5465",
												"nota" : 2.79,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-8238",
												"nota" : 3.79,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20180197073:{
								"nombres" : "Pablo Juan",
								"apellidos" : "García, Díaz",
								"documento" : 97713967,
								"programa" : "DIGR",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-7837",
												"nota" : 2.44,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-2013",
												"nota" : 2.56,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-5036",
												"nota" : 4.04,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20200137719:{
								"nombres" : "Paula Gabriela",
								"apellidos" : "Jiménez, Gómez",
								"documento" : 67419825,
								"programa" : "DIMD",
								"materias" : [
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-9271",
												"nota" : 3.17,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-4773",
												"nota" : 4.33,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-1670",
												"nota" : 4.26,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-6433",
												"nota" : 3.61,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20170181765:{
								"nombres" : "Juan Jorge",
								"apellidos" : "Hernández, Ochoa",
								"documento" : 53243230,
								"programa" : "ISIS",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-3961",
												"nota" : 4.0,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-6565",
												"nota" : 4.35,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20150366721:{
								"nombres" : "Gabriel Andres",
								"apellidos" : "Díaz, Jiménez",
								"documento" : 73184770,
								"programa" : "MENF",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-9442",
												"nota" : 2.82,
												"creditos" : 0,
												"retirada" : "Si",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-2593",
												"nota" : 3.28,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-9348",
												"nota" : 2.3,
												"creditos" : 4,
												"retirada" : "Si",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-5889",
												"nota" : 3.83,
												"creditos" : 0,
												"retirada" : "No",
												},
											]
								},
					20150332990:{
								"nombres" : "Gabriela Maria",
								"apellidos" : "Ramírez, García",
								"documento" : 63768613,
								"programa" : "ICIV",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-4689",
												"nota" : 3.34,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-6673",
												"nota" : 2.73,
												"creditos" : 3,
												"retirada" : "Si",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-2747",
												"nota" : 2.45,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20150157579:{
								"nombres" : "Juan Andres",
								"apellidos" : "Sánchez, López",
								"documento" : 57433656,
								"programa" : "MEDI",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-7771",
												"nota" : 3.05,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-7732",
												"nota" : 4.55,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-4275",
												"nota" : 4.58,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-8291",
												"nota" : 4.4,
												"creditos" : 1,
												"retirada" : "No",
												},
											]
								},
					20180112245:{
								"nombres" : "Camilo Daniel",
								"apellidos" : "García, Díaz",
								"documento" : 56019795,
								"programa" : "ISIS",
								"materias" : [
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-3843",
												"nota" : 3.9,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-8189",
												"nota" : 4.14,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-1419",
												"nota" : 3.57,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20100133656:{
								"nombres" : "Camila Laura",
								"apellidos" : "Ramírez, Sánchez",
								"documento" : 18406646,
								"programa" : "HART",
								"materias" : [
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-2433",
												"nota" : 2.86,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-3640",
												"nota" : 3.44,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-5327",
												"nota" : 3.64,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20180168437:{
								"nombres" : "Sofia Sara",
								"apellidos" : "García, Ochoa",
								"documento" : 33993048,
								"programa" : "ARQU",
								"materias" : [
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-4664",
												"nota" : 4.59,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-2113",
												"nota" : 4.89,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-9271",
												"nota" : 2.0,
												"creditos" : 3,
												"retirada" : "Si",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-4773",
												"nota" : 2.39,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20190267075:{
								"nombres" : "Jorge Camilo",
								"apellidos" : "Martínez, Guitiérrez",
								"documento" : 16066073,
								"programa" : "DIGR",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-1584",
												"nota" : 4.34,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-2531",
												"nota" : 4.5,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-4810",
												"nota" : 1.52,
												"creditos" : 3,
												"retirada" : "Si",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-2432",
												"nota" : 3.39,
												"creditos" : 1,
												"retirada" : "No",
												},
											]
								},
					20180275287:{
								"nombres" : "Catalina Carolina",
								"apellidos" : "Guitiérrez, Moreno",
								"documento" : 93402879,
								"programa" : "MEDI",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-2169",
												"nota" : 3.06,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-5889",
												"nota" : 2.97,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-5278",
												"nota" : 4.64,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-7278",
												"nota" : 1.76,
												"creditos" : 1,
												"retirada" : "Si",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-7665",
												"nota" : 4.16,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20180121110:{
								"nombres" : "Gabriela Sara",
								"apellidos" : "Torres, Torres",
								"documento" : 38538468,
								"programa" : "DISE",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-4446",
												"nota" : 4.67,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-7393",
												"nota" : 4.23,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-1276",
												"nota" : 3.51,
												"creditos" : 3,
												"retirada" : "Si",
												},
											]
								},
					20190292733:{
								"nombres" : "Gabriel Nicolas",
								"apellidos" : "Pérez, Martínez",
								"documento" : 95898448,
								"programa" : "ARQD",
								"materias" : [
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-5194",
												"nota" : 2.79,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-7589",
												"nota" : 4.03,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-8218",
												"nota" : 4.49,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-5405",
												"nota" : 4.34,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20180157756:{
								"nombres" : "Daniela Paula",
								"apellidos" : "Cuellar, Moreno",
								"documento" : 73658922,
								"programa" : "IBIO",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-4554",
												"nota" : 2.96,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-4554",
												"nota" : 4.94,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-7698",
												"nota" : 3.33,
												"creditos" : 4,
												"retirada" : "Si",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-8942",
												"nota" : 3.8,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-1968",
												"nota" : 3.12,
												"creditos" : 4,
												"retirada" : "No",
												},
											]
								},
					20200284956:{
								"nombres" : "Andrea Sofia",
								"apellidos" : "Gómez, Moreno",
								"documento" : 24588765,
								"programa" : "HAMO",
								"materias" : [
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-8141",
												"nota" : 4.45,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-9576",
												"nota" : 3.47,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-3502",
												"nota" : 1.61,
												"creditos" : 3,
												"retirada" : "Si",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-6328",
												"nota" : 4.93,
												"creditos" : 4,
												"retirada" : "No",
												},
											]
								},
					20180276186:{
								"nombres" : "Gabriel Julio",
								"apellidos" : "Romero, Álvarez",
								"documento" : 53452997,
								"programa" : "ISIS",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-1419",
												"nota" : 3.59,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-4601",
												"nota" : 2.66,
												"creditos" : 4,
												"retirada" : "Si",
												},
											]
								},
					20130117729:{
								"nombres" : "Camilo Juan",
								"apellidos" : "Pardo, Niño",
								"documento" : 51804513,
								"programa" : "IIND",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "IIND-9484",
												"nota" : 4.5,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IIND-9484",
												"nota" : 3.19,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-7278",
												"nota" : 3.8,
												"creditos" : 1,
												"retirada" : "No",
												},
											]
								},
					20170191084:{
								"nombres" : "Nicolas Gabriel",
								"apellidos" : "Niño, Martínez",
								"documento" : 17307732,
								"programa" : "DIMD",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-5431",
												"nota" : 3.87,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-7666",
												"nota" : 3.49,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-7666",
												"nota" : 2.48,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-2837",
												"nota" : 4.96,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20150296881:{
								"nombres" : "Gabriela",
								"apellidos" : "Fernández, Ochoa",
								"documento" : 19409088,
								"programa" : "ISIS",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-2485",
												"nota" : 3.04,
												"creditos" : 2,
												"retirada" : "Si",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-9950",
												"nota" : 4.28,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-7601",
												"nota" : 4.21,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-8189",
												"nota" : 2.45,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20090184597:{
								"nombres" : "Sofia Catalina",
								"apellidos" : "García, Martínez",
								"documento" : 35888833,
								"programa" : "MENF",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-2593",
												"nota" : 3.82,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-4627",
												"nota" : 3.6,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20140224557:{
								"nombres" : "Jose Pablo",
								"apellidos" : "Pardo, Hernández",
								"documento" : 44536160,
								"programa" : "MEDI",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-1186",
												"nota" : 4.73,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-8291",
												"nota" : 3.96,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-6400",
												"nota" : 1.66,
												"creditos" : 2,
												"retirada" : "Si",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-2339",
												"nota" : 4.43,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20150149472:{
								"nombres" : "Catalina Sara",
								"apellidos" : "Córdoba, García",
								"documento" : 89107372,
								"programa" : "HART",
								"materias" : [
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-9958",
												"nota" : 1.74,
												"creditos" : 4,
												"retirada" : "Si",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-4066",
												"nota" : 3.87,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-8458",
												"nota" : 3.09,
												"creditos" : 3,
												"retirada" : "Si",
												},
											]
								},
					20130134592:{
								"nombres" : "Gabriela Camila",
								"apellidos" : "Sánchez, Sánchez",
								"documento" : 80992197,
								"programa" : "DIIN",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-7888",
												"nota" : 3.43,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-3496",
												"nota" : 2.59,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-4822",
												"nota" : 4.72,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20190188795:{
								"nombres" : "Juan",
								"apellidos" : "Cuellar, García",
								"documento" : 90411603,
								"programa" : "MENF",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-5644",
												"nota" : 4.15,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-9442",
												"nota" : 4.77,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-2072",
												"nota" : 3.45,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20180158032:{
								"nombres" : "Mateo Gabriel",
								"apellidos" : "López, Jiménez",
								"documento" : 72342554,
								"programa" : "MENF",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-6232",
												"nota" : 2.76,
												"creditos" : 2,
												"retirada" : "Si",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-9535",
												"nota" : 2.54,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-9114",
												"nota" : 2.58,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-5889",
												"nota" : 4.29,
												"creditos" : 0,
												"retirada" : "No",
												},
											]
								},
					20180568756:{
								"nombres" : "Sofia Natalia",
								"apellidos" : "Romero, Álvarez",
								"documento" : 90763295,
								"programa" : "DIIN",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-9838",
												"nota" : 2.34,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIGR-1403",
												"nota" : 2.27,
												"creditos" : 4,
												"retirada" : "Si",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-5158",
												"nota" : 1.88,
												"creditos" : 4,
												"retirada" : "Si",
												},
											]
								},
					20160296549:{
								"nombres" : "Camilo Daniel",
								"apellidos" : "Ramírez, Ramírez",
								"documento" : 51519517,
								"programa" : "DIIN",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-5158",
												"nota" : 2.9,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-7003",
												"nota" : 2.38,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-3583",
												"nota" : 4.77,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-9442",
												"nota" : 3.62,
												"creditos" : 0,
												"retirada" : "No",
												},
											]
								},
					20200184437:{
								"nombres" : "Gabriel Julián",
								"apellidos" : "García, Ochoa",
								"documento" : 73923971,
								"programa" : "IBIO",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-5465",
												"nota" : 3.24,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-8126",
												"nota" : 3.16,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-4502",
												"nota" : 2.52,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-4502",
												"nota" : 4.7,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20100235453:{
								"nombres" : "Maria Natalia",
								"apellidos" : "Cuellar, Martínez",
								"documento" : 32133868,
								"programa" : "ISIS",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-6565",
												"nota" : 3.92,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-4155",
												"nota" : 3.77,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-4305",
												"nota" : 4.95,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ISIS-5216",
												"nota" : 1.77,
												"creditos" : 2,
												"retirada" : "Si",
												},
											]
								},
					20090136443:{
								"nombres" : "Mateo Oscar",
								"apellidos" : "Ochoa, Gómez",
								"documento" : 26803289,
								"programa" : "MENF",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-5889",
												"nota" : 2.52,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-2668",
												"nota" : 2.67,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-1652",
												"nota" : 2.15,
												"creditos" : 2,
												"retirada" : "Si",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-4996",
												"nota" : 2.71,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20150362232:{
								"nombres" : "Jorge Camilo",
								"apellidos" : "Moreno, Hernández",
								"documento" : 61143392,
								"programa" : "MEDI",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "IQUI-1115",
												"nota" : 4.88,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-4328",
												"nota" : 3.72,
												"creditos" : 4,
												"retirada" : "No",
												},
											]
								},
					20160127320:{
								"nombres" : "Gabriela Catalina",
								"apellidos" : "Ochoa, Pardo",
								"documento" : 40733914,
								"programa" : "IQUI",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "IQUI-3898",
												"nota" : 2.89,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IQUI-9815",
												"nota" : 2.95,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IQUI-4677",
												"nota" : 3.22,
												"creditos" : 0,
												"retirada" : "No",
												},
											]
								},
					20150164760:{
								"nombres" : "Andres Oscar",
								"apellidos" : "Jiménez, Moreno",
								"documento" : 96466972,
								"programa" : "MEDI",
								"materias" : [
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-8159",
												"nota" : 4.96,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-9490",
												"nota" : 4.65,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-9771",
												"nota" : 4.32,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20110215919:{
								"nombres" : "Juan Camilo",
								"apellidos" : "Pérez, Gómez",
								"documento" : 51702064,
								"programa" : "ICIV",
								"materias" : [
											]
								},
					20190181470:{
								"nombres" : "Mateo Nicolas",
								"apellidos" : "Torres, Díaz",
								"documento" : 70114652,
								"programa" : "DISE",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-1626",
												"nota" : 2.37,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-1995",
												"nota" : 4.83,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-9978",
												"nota" : 3.29,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DISE-6981",
												"nota" : 4.86,
												"creditos" : 0,
												"retirada" : "No",
												},
											]
								},
					20170135873:{
								"nombres" : "Jose Daniel",
								"apellidos" : "Romero, Ramírez",
								"documento" : 61689275,
								"programa" : "MENF",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-2072",
												"nota" : 2.43,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-2593",
												"nota" : 3.22,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-6067",
												"nota" : 4.58,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-5889",
												"nota" : 2.59,
												"creditos" : 0,
												"retirada" : "No",
												},
											]
								},
					20190287188:{
								"nombres" : "Daniela Sofia",
								"apellidos" : "García, Córdoba",
								"documento" : 75179813,
								"programa" : "ARQD",
								"materias" : [
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-1564",
												"nota" : 2.72,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-3420",
												"nota" : 2.46,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-1864",
												"nota" : 3.94,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQD-1564",
												"nota" : 3.14,
												"creditos" : 3,
												"retirada" : "Si",
												},
											]
								},
					20170294793:{
								"nombres" : "Jorge Nicolas",
								"apellidos" : "Cuellar, Jiménez",
								"documento" : 49162279,
								"programa" : "DIIN",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-2355",
												"nota" : 3.31,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-4014",
												"nota" : 3.88,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-3467",
												"nota" : 2.69,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-3467",
												"nota" : 2.54,
												"creditos" : 4,
												"retirada" : "No",
												},
											]
								},
					} ))
# Expected return:
# ({'Arquitectura': 3.5, 'Diseño': 3.51, 'Historia del Arte': 3.32, 'Ingenieria': 3.57, 'Medicina': 3.84}, ['ao.moreno72', 'as.moreno65', 'cc.moreno79', 'cd.diaz95', 'cd.ramirez17', 'cj.diaz79', 'cj.nino13', 'cl.sanchez46', 'cp.guitierrez74', 'dn.alvarez66', 'dp.moreno22', 'ds.cordoba13', 'ga.jimenez70', 'gc.pardo14', 'gc.sanchez97', 'gj.alvarez97', 'gj.ochoa71', 'gm.garcia13', 'gn.martinez48', 'go.fernandez88', 'gs.torres68', 'ja.lopez56', 'jc.guitierrez73', 'jc.hernandez92', 'jc.sanchez60', 'jc.sanchez71', 'jd.ramirez75', 'jg.cuellar03', 'jj.cuellar30', 'jj.ochoa30', 'jn.jimenez79', 'jp.hernandez60', 'ld.hernandez98', 'md.diaz36', 'mg.jimenez54', 'mn.diaz52', 'mn.martinez68', 'mo.gomez89', 'ng.martinez32', 'no.ramirez99', 'oj.cordoba71', 'pg.gomez25', 'pj.diaz67', 'sc.martinez33', 'sc.suarez26', 'sn.alvarez95', 'ss.ochoa48']) 

# Prueba 6
print(promedio_facultades({
					20150153158:{
								"nombres" : "Catalina Camila",
								"apellidos" : "Córdoba, Cuellar",
								"documento" : 17976639,
								"programa" : "HART",
								"materias" : [
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-1079",
												"nota" : 2.57,
												"creditos" : 2,
												"retirada" : "Si",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-2000",
												"nota" : 3.58,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-2433",
												"nota" : 4.0,
												"creditos" : 0,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-2081",
												"nota" : 4.77,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20180132253:{
								"nombres" : "Sara Paula",
								"apellidos" : "Romero, Niño",
								"documento" : 38220418,
								"programa" : "ARQU",
								"materias" : [
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-1033",
												"nota" : 2.53,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-9649",
												"nota" : 3.94,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Arquitectura",
												"codigo" : "ARQU-7635",
												"nota" : 3.31,
												"creditos" : 1,
												"retirada" : "No",
												},
											]
								},
					20170167311:{
								"nombres" : "Paula Daniela",
								"apellidos" : "Romero, Sánchez",
								"documento" : 54407086,
								"programa" : "IQUI",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "IQUI-2010",
												"nota" : 2.55,
												"creditos" : None,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IQUI-8933",
												"nota" : 2.41,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IQUI-3898",
												"nota" : 3.89,
												"creditos" : 4,
												"retirada" : "No",
												},
											]
								},
					20110212282:{
								"nombres" : "Andres Nicolas",
								"apellidos" : "Cuellar, Sánchez",
								"documento" : 55861549,
								"programa" : "IBIO",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-3425",
												"nota" : 2.92,
												"creditos" : 4,
												"retirada" : "Si",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-9302",
												"nota" : 2.65,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-4554",
												"nota" : 2.94,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "IBIO-2100",
												"nota" : 2.44,
												"creditos" : 3,
												"retirada" : "No",
												},
											]
								},
					20160111154:{
								"nombres" : "Julián Daniel",
								"apellidos" : "Martínez, Hernández",
								"documento" : 59069740,
								"programa" : "ICIV",
								"materias" : [
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-6894",
												"nota" : 2.76,
												"creditos" : 4,
												"retirada" : "Si",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-4998",
												"nota" : 4.14,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-5962",
												"nota" : 3.16,
												"creditos" : None,
												"retirada" : "No",
												},
												{
												"facultad" : "Ingenieria",
												"codigo" : "ICIV-1968",
												"nota" : 4.28,
												"creditos" : 4,
												"retirada" : "No",
												},
											]
								},
					20150298980:{
								"nombres" : "Pablo Camilo",
								"apellidos" : "Cuellar, Jiménez",
								"documento" : 73709235,
								"programa" : "DIMD",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-3449",
												"nota" : 2.88,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-7539",
												"nota" : 3.23,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-2837",
												"nota" : 3.03,
												"creditos" : 3,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-1670",
												"nota" : 2.99,
												"creditos" : 2,
												"retirada" : "Si",
												},
											]
								},
					20160553540:{
								"nombres" : "Carolina Paula",
								"apellidos" : "Córdoba, Díaz",
								"documento" : 89166334,
								"programa" : "DIMD",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-2868",
												"nota" : 2.73,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-3449",
												"nota" : 4.15,
												"creditos" : 1,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-7470",
												"nota" : 3.83,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIMD-8021",
												"nota" : 2.72,
												"creditos" : 4,
												"retirada" : "No",
												},
											]
								},
					20170328399:{
								"nombres" : "Camilo Julián",
								"apellidos" : "Martínez, Cuellar",
								"documento" : 12195309,
								"programa" : "MEDI",
								"materias" : [
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-4328",
												"nota" : 3.75,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-8634",
												"nota" : 1.99,
												"creditos" : 3,
												"retirada" : "Si",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MENF-2668",
												"nota" : 3.14,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Medicina",
												"codigo" : "MEDI-6400",
												"nota" : 3.22,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					20080310830:{
								"nombres" : "Julio Nicolas",
								"apellidos" : "Niño, López",
								"documento" : 27830207,
								"programa" : "HAMO",
								"materias" : [
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-8141",
												"nota" : 4.28,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HART-3008",
												"nota" : 4.28,
												"creditos" : 2,
												"retirada" : "No",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-9435",
												"nota" : 2.7,
												"creditos" : 2,
												"retirada" : "Si",
												},
												{
												"facultad" : "Historia del Arte",
												"codigo" : "HAMO-6565",
												"nota" : 3.56,
												"creditos" : 4,
												"retirada" : "No",
												},
											]
								},
					20160112900:{
								"nombres" : "Julián Jose",
								"apellidos" : "García, Suárez",
								"documento" : 91356930,
								"programa" : "DIIN",
								"materias" : [
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-7888",
												"nota" : 3.13,
												"creditos" : 2,
												"retirada" : "Si",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-5158",
												"nota" : 3.12,
												"creditos" : 4,
												"retirada" : "No",
												},
												{
												"facultad" : "Diseño",
												"codigo" : "DIIN-7888",
												"nota" : 3.38,
												"creditos" : 2,
												"retirada" : "No",
												},
											]
								},
					}, False ))
# Expected return:
# 'Error numérico.'

