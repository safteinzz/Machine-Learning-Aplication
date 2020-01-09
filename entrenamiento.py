# -*- coding: utf-8 -*-
"""
Entrenamiento vuelos
Autores: Pablo, Roberto y Sergio
"""
### LIBRERIAS ###

# => imports principales
import sys
import numpy as np
import pandas as pd


# => import clase local
from pandasmodel import PandasModel

# => entorno gráfico
# from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic

# => para alerts
import ctypes  # An included library with Python install.

# Seleccionar archivos
from PyQt5.QtWidgets import QFileDialog


# => algoritmos
## partidor datos Train VS test
from sklearn.model_selection import train_test_split
## Regresion Logistica
from sklearn.linear_model import LogisticRegression
## Support Vector Machines
from sklearn.svm import SVC
## KNN - K Nearest Neighbors
from sklearn.neighbors import KNeighborsClassifier

import pickle
from sklearn.externals import joblib

### Variables Globales ###
df_entrenar_global = None

### CUERPO DEL PROGRAMA ###

# => DIALOGO DEL PROGRAMA a usar diseñado en QT designer
Ui_MainWindow, QtBaseClass = uic.loadUiType("entrenamiento.ui")

# => Clase del Dialogo ppal.
class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)        
        
        # EVENTOS
        # Cargar datos excel
        self.ui.excel_cargar_button.clicked.connect(self.Cargadatos_Entrenar)   
        
        # Lanzar entrenamiento según radiobutton
        self.ui.entrenar_button.clicked.connect(self.Lanzar_Entrenamiento)         
              
        # Guardar modelo
        self.ui.qPBExportarModelo.clicked.connect(self.exportarModelo)  
        
        # Seleccionar fichero a predecir
        self.ui.qPBSelectFicheroAClasificar.clicked.connect(self.cargarDatos_Clasificar)  
        
        # Seleccionar modelo
        self.ui.qPBSeleccionarModelo.clicked.connect(self.cargarModelo)
        
        # Predecir
        self.ui.qPBPredecir.clicked.connect(self.predecirDataFrame)  
        
        # Exportar predicciones a excel
        self.ui.qPBExportar.clicked.connect(self.guardarDatos)  
    ##############################################################################################
    #Fin de metodo      
        
    #---------------------------
    #
    #   FUNCIONES GENERALES
    #
    #---------------------------    
    
    
    ##
    # 
    ##     
    def encryptar(self, textoEncryptar):
        return str(int.from_bytes(textoEncryptar.encode('utf-8'), byteorder='big'))
    ##############################################################################################
    #Fin de metodo
    
    ##
    # 
    ## 
    def desencryptar(self, textoDesencryptar):
        s = int.to_bytes(int(textoDesencryptar), length=100, byteorder='big').decode('utf-8')
        devolver = ""
        for x in range(0,100):
            if ord(s[x]) != 0:
                devolver += s[x]
        return devolver
    ##############################################################################################
    #Fin de metodo
    
    ##
    # 
    ## 
    def encryptarColumna(self, nombreColumna, dataFrame):
        # transforma los datos de la columna en una lista
        listaString = dataFrame[nombreColumna].tolist()
    
        # crear dictionary vacío
        dictId = {}
        
        # recorremos la lista de antes agregandola en el dictionary y su valor sera el número en el que está situado en la lista
        # si un valor se repite pondrá el último identificado obtenido
        for i in range(len(listaString)):
            dictId[listaString[i]] = self.encryptar(listaString[i])
        
        # recorremos el dictonary y agregamos una columna nueva '_encode' con el valor del identificador,
        # este valor se pondrá a partir del valor que hay en la columna
        for k, v in dictId.items():
            dataFrame.loc[dataFrame[nombreColumna].str.contains(k), nombreColumna+'_encode'] = v
        
        dataFrame.drop([nombreColumna], axis=1, inplace=True)
    ##############################################################################################
    #Fin de metodo
     
    ##
    # 
    ## 
    def desencryptarColumna(self, nombreColumna, dataFrame):
        # transforma los datos de la columna en una lista
        listaString = dataFrame[nombreColumna].tolist()
    
        # crear dictionary vacío
        dictId = {}
        
        # recorremos la lista de antes agregandola en el dictionary y su valor sera el número en el que está situado en la lista
        # si un valor se repite pondrá el último identificado obtenido
        for i in range(len(listaString)):
            dictId[listaString[i]] = self.desencryptar(listaString[i])
        
        # recorremos el dictonary y agregamos una columna nueva '_encode' con el valor del identificador,
        # este valor se pondrá a partir del valor que hay en la columna
        for k, v in dictId.items():
            dataFrame.loc[dataFrame[nombreColumna].str.contains(k), nombreColumna+'_desencode'] = v    
    ##############################################################################################
    #Fin de metodo          
        
      
    

    
    
    #---------------------------
    #
    #   FUNCIONES DE EVENTOS
    #
    #---------------------------
    
    ##
    # Guardar el modelo
    ##
    def exportarModelo(self):
        print('sin hacer')
    ##############################################################################################
    #Fin de metodo        
      
    ##
    # Predecir
    ##
    def predecirDataFrame(self):
        
        #Sacar la ruta del fichero de datos que queire usar el user
        rutaPredecir = self.ui.qLEFicheroAClasificar.text()
#        print(rutaPredecir)
        
        #Sacar el modelo que ha elegido el user
        rutaModelo = self.ui.qLEModelo.text()
#        print(rutaModelo)
        
        
        #Comprobar que tipo de fichero ha elegido el user
        if rutaPredecir.endswith('.xls'):
            df_entrenar = pd.read_excel(rutaPredecir)
        elif rutaPredecir.endswith('.csv'):
            df_entrenar = pd.read_csv(rutaPredecir)
        
        
        #esto de aqui abajo es lo mismo que hay en el otro, abria que hacer un metodo para no duplicarlo !!
        # eliminamos columna "nada" que no aporta al entrenamiento
        df_entrenar.drop(['nada'], axis=1, inplace=True)           

        # eliminamos columna "nada" que no aporta al entrenamiento
        df_entrenar.drop(['time_scheduled'], axis=1, inplace=True)     
        # eliminamos columna "nada" que no aporta al entrenamiento
        df_entrenar.drop(['time_departured'], axis=1, inplace=True)   
        # eliminamos columna "nada" que no aporta al entrenamiento
        df_entrenar.drop(['fecha_vuelo'], axis=1, inplace=True) 
        df_entrenar.drop(['salida_retrasada'], axis=1, inplace=True)
        self.encryptarColumna("flight_id",df_entrenar)
        self.encryptarColumna("airport_name",df_entrenar)
        self.encryptarColumna("destiny",df_entrenar)
        self.encryptarColumna("airlane_name",df_entrenar)
        self.encryptarColumna("observations",df_entrenar)
        self.encryptarColumna("direccion_viento",df_entrenar)
        self.encryptarColumna("direccion_racha",df_entrenar)       
       
        #Cargar modelo en loader
        classifer = joblib.load(rutaModelo)
#        classifer.fit(X_Train, Y_Train)
        #Predecir el frame usando el modelo
        prediccion = classifer.predict(df_entrenar)
#        print(prediccion)
        
        #Cargar de nuevo el documento del usuario para mostrar la información bien
        global df_p
        if rutaPredecir.endswith('.xls'):
            df_p = pd.read_excel(rutaPredecir)
        elif rutaPredecir.endswith('.csv'):
            df_p = pd.read_csv(rutaPredecir)
        
        #Quitar la columna salida retrasada
        df_p.drop(['salida_retrasada'], axis=1, inplace=True)
        
        #Crear la columna prediccion que los datos de la prediccion
        df_p['Prediccion'] = prediccion
        
        #Hacer mas claro la columna prediccion al usuario
        df_p['Prediccion'].replace([1, 0], ['Se retrasara','No se retrasara'], inplace=True)
        
#        # muestra de registros
#        print ("=================================")
#        print ("Muestra de registros")            
#        print ("=================================")
#        print (df_entrenar.head())  
        
        #Crear modelo para mostrar en la tabla
        p = PandasModel(df_p) 
        
        #Mostrar el modelo en la tabla
        self.ui.qTWVisualizacionPrediccion.setModel(p)
    
    ##############################################################################################
    #Fin de metodo        
        
    ##
    # Guardar datos clasificados
    ##
    def guardarDatos(self):

        #Comprobar que se haya hecho la prediccion
        if not 'df_p' in globals():        
            Messagebox('Primero debe hacer una predicción', 'Error', 1)     
            return 
        
        #Si se ha hecho entonces se trae el dataframe
        global df_p
        
        #Se le pide al usuario donde quiere guardar el archivo y de que tipo desea que sea
        rutaGuardado = seleccionarFichero("xls(*.xls);;csv(*.csv)", 1)
#        print(rutaGuardado)
        Messagebox('Archivo exportado con exito', 'Error', 1)  
        
        #Se guarda
        if rutaGuardado[1] == 'xls(*.xls)':
            df_p.to_excel(rutaGuardado[0], sheet_name='Hoja 1', index=False)
        else:
            df_p.to_csv(rutaGuardado[0], index=False)      
    ##############################################################################################
    #Fin de metodo

    
    ##
    # Carga el modelo
    ##
    def cargarModelo(self):
        archivo = seleccionarFichero('Modelo(*.pkl)', 0)[0]
        if archivo:
            self.ui.qLEModelo.setText(archivo)
    ##############################################################################################
    #Fin de metodo   
        
    ##
    # Carga el excel a predecir
    ##
    def cargarDatos_Clasificar(self):
#        print (seleccionarFichero("xls(*.xls);;csv(*.csv)"))
        archivo = seleccionarFichero("xls(*.xls);;csv(*.csv)", 0)[0]
        if archivo:
            self.ui.qLEFicheroAClasificar.setText(archivo)
    ##############################################################################################
    #Fin de metodo       
        
    ##
    # Guardar modelo
    ##
    def guardarModelo(self, nombre, dataFrame):
        filename = nombre + '.sav'
        pickle.dump(dataFrame, open(filename, 'wb'))
    ##############################################################################################
    #Fin de metodo        
        
    ##
    # Carga del dataset de entrenamiento => dataframe
    ##
    def Cargadatos_Entrenar( self ):      
        ficheroSeleccionado = seleccionarFichero("xls(*.xls);;csv(*.csv)", 0)
        fileName = ficheroSeleccionado[0]
        if not fileName:
            Messagebox('Por favor, seleccione un fichero de entrenamiento', 'Error', 1)        
            return 
        
        self.ui.fichEntrenamiento_txt.setText(fileName)           
        
        #Leer excel si se elegio formato excel
        if ficheroSeleccionado[1] == 'xls(*.xls)':
            df_entrenar = pd.read_excel (fileName)
        #Leer csv si se eligio formato csv
        else:                
            df_entrenar = pd.read_csv (fileName)
        
        ############## consola
        
        # * mostramos datos cargados al dataframe
        print ("=================================")
        print ("Datos cargados")            
        print ("=================================")
        
        # muestra de registros
        print ("=================================")
        print ("Muestra de registros")            
        print ("=================================")
        print (df_entrenar.head())            
        
        # estructura de datos                        
        print ("=================================")
        print ("nº filas, columnas")
        print ("=================================")                        
        print (df_entrenar.shape)            
        
        # verificamos tipos de datos
        print ("=================================")
        print ("verificamos tipos de datos")
        print ("=================================")            
        print (df_entrenar.info())
        
        # comprobamos campos con datos nulos/erroneos
        print ("===========================================")
        print ("comprobamos campos con datos nulos/erroneos")
        print ("===========================================")            
        print (pd.isnull(df_entrenar).sum())            
        
        # estadísticas dataset
        print ("===========================================")
        print ("estadísticas dataset")
        print ("===========================================")            
        print (df_entrenar.describe())            
        
        # transformos campo label de texto a numerico            
        df_entrenar['salida_retrasada'].replace(['Y', 'N'], [1,0], inplace=True)
        
        # eliminamos columna "nada" que no aporta al entrenamiento
        df_entrenar.drop(['nada'], axis=1, inplace=True)           

        # eliminamos columna "nada" que no aporta al entrenamiento
        df_entrenar.drop(['time_scheduled'], axis=1, inplace=True)     
        # eliminamos columna "nada" que no aporta al entrenamiento
        df_entrenar.drop(['time_departured'], axis=1, inplace=True)   
        # eliminamos columna "nada" que no aporta al entrenamiento
        df_entrenar.drop(['fecha_vuelo'], axis=1, inplace=True)   
                         
                                
        ############## dialogo
        
        # convertimos en modelo con clase PandasModel
        model_entrenar = PandasModel(df_entrenar) 
        
        # visualizar en ui.tableView
        self.ui.mitableView.setModel(model_entrenar)
        
        # datos estadisticos dataframe
        dt_entrenar_info_string=""
        dt_entrenar_info_string+=" - Nº registros: " + str(df_entrenar.shape[0]) ## Gives no. of rows/records 
        dt_entrenar_info_string+="\n"
        dt_entrenar_info_string+=" - Nº columnas: " + str(df_entrenar.shape[1]) ## Gives no. of columns 
        dt_entrenar_info_string+="\n\n"
        dt_entrenar_info_string+="- Más info a poner"
        
        self.ui.label_Info.setText(dt_entrenar_info_string)
            
        # indicamos que es la variable global
        global df_entrenar_global
        # asignamos a la variable global
        df_entrenar_global = df_entrenar            
    ##############################################################################################
    #Fin de metodo        
        
    ##
    # Lanzar entrenamiento
    ##
    def Lanzar_Entrenamiento(self):        
        
        # chequeamos que hemos seleccionado una opción => valorar combobox        
        if not self.ui.rd_Algor_RL.isChecked() and not self.ui.rd_Algor_SVM.isChecked() and not self.ui.rd_Algor_KNN.isChecked():                    
            Messagebox('No ha seleccionado ningún algoritmo', 'Error', 1)
            return
                                
        ### Entrenamiento        
        global df_entrenar_global # indicamos que es la variable global                        
        # igualamos a la variable global
        df_entrenar =  df_entrenar_global        
        
        
        self.encryptarColumna("flight_id",df_entrenar)
        self.encryptarColumna("airport_name",df_entrenar)
        self.encryptarColumna("destiny",df_entrenar)
        self.encryptarColumna("airlane_name",df_entrenar)
        self.encryptarColumna("observations",df_entrenar)
        self.encryptarColumna("direccion_viento",df_entrenar)
        self.encryptarColumna("direccion_racha",df_entrenar)
        
        
        # Separamos columna con la info de salida_retrasada                        
        X =  np.array(df_entrenar.drop(['salida_retrasada'], 1)) # variables del modelo        
        Y =  np.array(df_entrenar['salida_retrasada']) # resultado
        # separamos datos en entrenamiento y prueba para testear algoritmos
        X_Train, X_Test, Y_Train, Y_Test = train_test_split(X, Y, test_size=0.2)
        
        Y_pred=0
        str_algoritmo = ""        
        
        print('\nEntrenamiento lanzado')
        
        
        if self.ui.rd_Algor_RL.isChecked():
            
            # Regresion logistica
            logreg = LogisticRegression()
            logreg.fit(X_Train, Y_Train)
            Y_pred = logreg.predict(X_Test)            
            
            print('Precisión Regresión logística:')
            
            print(logreg.score(X_Train, Y_Train))            
            str_algoritmo="Logístic Regression"        
            
        elif self.ui.rd_Algor_SVM.isChecked():            
            # Support Vectors Machines
            svc = SVC()
            svc.fit(X_Train, Y_Train)
            Y_pred = svc.predict(X_Test)
            
            print('Precisión SVM')
            
            print(svc.score(X_Train, Y_Train))            
            str_algoritmo="SVM - Support Vectors Machine"
            
        elif self.ui.rd_Algor_KNN.isChecked():            
            # KNN - K Nearest Neighbors
            knn = KNeighborsClassifier(n_neighbors = 3)
            knn.fit(X_Train, Y_Train)
            joblib.dump(knn, "model.pkl")
            Y_pred = knn.predict(X_Test)
            
            print('Precisión KNN')
            
            print(knn.score(X_Train, Y_Train))            
            str_algoritmo="KNN - Logístic Regression"
        
        print(Y_pred)        
        
        print('\n\nEntrenamiento con ' + str_algoritmo + ' finalizado')        
    ##############################################################################################
    #Fin de metodo        
##############################################################################################
#Fin de clase
            

##
# función Messagebox para alertas
##
def Messagebox(text, title, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)            
##############################################################################################
#Fin de metodo
    
##
# Seleccionar Ruta de fichero
# @filtro => Sera el tipo de extension
# @guardar => Booleano para saber si se quiere cargar o guardar
#   - 1 = guardar
#   - 0 = cargar
##  
def seleccionarFichero(filtro, guardar):
    qFD = QFileDialog()
    if guardar == 0:                    
        return QFileDialog.getOpenFileName(qFD,"Seleccionar archivo", "",filtro)
    elif guardar == 1:
        return QFileDialog.getSaveFileName(qFD,"Seleccionar archivo", "",filtro)
##############################################################################################
#Fin de metodo  
           
##
# Función MAIN
##
def main():
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec_()
##############################################################################################
#Fin de metodo


## pythonlike
if __name__ == '__main__':
    main()
