# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 17:36:01 2020

@author: Jenny
"""

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
