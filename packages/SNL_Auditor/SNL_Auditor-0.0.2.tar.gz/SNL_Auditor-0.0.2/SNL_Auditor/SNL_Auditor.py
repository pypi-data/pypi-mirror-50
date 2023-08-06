# -*- coding: utf-8 -*-
#"""
#Spyder Editor
#
#This is a temporary script file.
#"""
# importa as bibliotecas para trabalhar com o Excel
import pandas as pd
import numpy as np
import easygui


#-----------------------------------------------------------------------------------------------#
# abre o file explorer para o utilizador seleccionar o ficheiro que pretende auditar
caminho=easygui.fileopenbox()
#caminho = 'C:/Users/cacx/Documents/DSC/zAuditoria.XLSX'

#-----------------------------------------------------------------------------------------------#

#-----------------------------------------------------------------------------------------------#
# Abre o livro Excel
livro = pd.ExcelFile(caminho)

# Coloca o livro em um DataFrame
df = pd.read_excel(livro,0)

# Selecciona as Colunas com as quais se pretende trabalhar
df_IBAN = df[['Nº pess.','Nome completo','Recebedor','IBAN']]


#Selecciona todos os duplicados e remove os valores únicos
df_IBAN["Duplicados"] = df_IBAN.duplicated(['IBAN']) # Duplicado = True; Único = False
df_IBAN = df_IBAN.loc[df_IBAN['Duplicados']==True]

# Cria uma nova coluna de controlo que irá conter quantas vezes o IBAN duplica
df_IBAN.insert(5,"Conta",0,True)

#Procura por IBAN's duplicados que possuam titulares diferentes
for i in range(len(df_IBAN.index)-1):
    j=i
    for j in range(len(df_IBAN.index)-1):
        if (len(str(df_IBAN.iat[i, 3])) ==25): # ignora as colunas em branco
            if(str(df_IBAN.iat[i, 3]) == str(df_IBAN.iat[j, 3])):          
                if(str(df_IBAN.iat[i, 0]) != str(df_IBAN.iat[j, 0])):
                    (df_IBAN.iat[i, 5]) = (df_IBAN.iat[i, 5]) + 1 
       
# Remove todos os dados com valor 0 da coluna "Conta"     
df_IBAN = df_IBAN.loc[df_IBAN['Conta']!=0]   
            
#remove os duplicados 
df_IBAN = df_IBAN.drop_duplicates()

# Selecciona as colunas a apresentar
df_IBAN = df_IBAN[['Nº pess.','Nome completo','Recebedor','IBAN']]

# Cria o documento Excel e salva no caminho especificado, este código será melhorado
# para permitir que o utilizador seleccione o directório para salavar o documento
writer = pd.ExcelWriter('C:/Users/cacx/Documents/DSC/Resultado Auditoria.xlsx', engine='xlsxwriter')
df_IBAN.to_excel(writer, index=False,sheet_name='IBANs Duplicados')
workbook = writer.bookworksheet = writer.sheets['IBANs Duplicados']

writer.close()



