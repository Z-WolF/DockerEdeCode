# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger('root')

from validate_email import validate_email
import re
from itertools import cycle
from datetime import datetime
from pytz import timezone
import os
import pandas as pd
import numpy as np
import requests
from sqlalchemy import create_engine


from sqlalchemy import event, func
from sqlalchemy.sql import label
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

@event.listens_for(Engine, "connect")
def sqlite_engine_connect(dbapi_connection, connection_record):
    dbapi_connection.create_function("regexp", 2, sqlite_regexp)
    dbapi_connection.create_function("REGEXP_REPLACE", 3, sqlite_regexp_replace)


def sqlite_regexp(expr, item):
    if(not item): return False
    #logger.info(f"expr: {type(expr)} => {expr}, \nitem: {type(item)} => {item}")
    #reg = re.compile(expr, re.IGNORECASE)
    #reg = re.compile(expr)
    #logger.info(f"reg:{reg}")
    try:
        #logger.info(f"search:{re.search(fr'{expr}',str(item))}")      
        return re.search(expr,str(item)) is not None
    except Exception as e:
        print(f'ERROR: {e}')
        return False

def sqlite_regexp_replace(item, find, repl):
    reg = re.compile(find, re.IGNORECASE)
    return reg.sub(repl, item)

#----------------------------------------------------------------------------
#PASO N° 20 - Transformar el archivo JSON en archivos CSV's. Uno por tabla.
#----------------------------------------------------------------------------

class check:
  def __init__(self, args):
    self.args = args
    logger.info(f"tipo de argumento: {type(self.args)}, valores: {self.args}")
    self.functions = {
      "fn0FA": "self.fn0FA(conn)",
      "fn0FB": "self.fn0FB(conn)",
      "fn1FA": "self.fn1FA(conn)",
      "fn1FB": "self.fn1FB(conn)",
      "fn1FC": "self.fn1FC(conn)",
      "fn2FA": "self.fn2FA(conn)",
      "fn2EA": "self.fn2EA(conn)",
      "fn2DA": "self.fn2DA(conn)",
      "fn2DB": "self.fn2DB(conn)",
      "fn2CA": "self.fn2CA(conn)",
      "fn2CB": "self.fn2CB(conn)",
      "fn2BA": "self.fn2BA(conn)",
      "fn2AA": "self.fn2AA(conn)",
      "fn29A": "self.fn29A(conn)",
      "fn29B": "self.fn29B(conn)",
      "fn29C": "self.fn29C(conn)",
      "fn28A": "self.fn28A(conn)",
      "fn28B": "self.fn28B(conn)",
      "fn3F0": "self.fn3F0(conn)",
      "fn3F1": "self.fn3F1(conn)",
      "fn3F2": "self.fn3F2(conn)",
      "fn3F3": "self.fn3F3()",
      "fn3F4": "self.fn3F4()",
      "fn3F5": "self.fn3F5()",
      "fn3F6": "self.fn3F6()",
      "fn3F7": "self.fn3F7()",
      "fn3F8": "self.fn3F8()",
      "fn3F9": "self.fn3F9()",
      "fn3FA": "self.fn3FA()",
      "fn3FB": "self.fn3FB()",
      "fn3FC": "self.fn3FC()",
      "fn3FD": "self.fn3FD()",
      "fn3FE": "self.fn3FE(conn)",
      "fn3FF": "self.fn3FF()",
      "fn3E0": "self.fn3E0(conn)",
      "fn3E1": "self.fn3E1()",
      "fn3E2": "self.fn3E2(conn)",
      "fn3E3": "self.fn3E3()",
      "fn3E4": "self.fn3E4(conn)",
      "fn3E5": "self.fn3E5()",
      "fn3E6": "self.fn3E6()",
      "fn3E7": "self.fn3E7()",
      "fn3E8": "self.fn3E8()",
      "fn3E9": "self.fn3E9()",
      "fn3EA": "self.fn3EA()",
      "fn3EB": "self.fn3EB()",
      "fn3EC": "self.fn3EC()",
      "fn3ED": "self.fn3ED()",
      "fn3EE": "self.fn3EE()",
      "fn3EF": "self.fn3EF(conn)",
      "fn3D0": "self.fn3D0(conn)",
      "fn3D1": "self.fn3D1(conn)",
      "fn3D2": "self.fn3D2(conn)",
      "fn3D3": "self.fn3D3(conn)",
      "fn3D4": "No/Verificado",
      "fn3D5": "No/Verificado",
      "fn3D6": "No/Verificado",
      "fn3D7": "No/Verificado",
      "fn3D8": "No/Verificado",
      "fn3D9": "self.fn3D9(conn)",
      "fn3DA": "self.fn3DA(conn)",
      "fn3DB": "No/Verificado",
      "fn3DC": "No/Verificado",
      "fn3DD": "self.fn3DD(conn)",
      "fn3DE": "No/Verificado",
      "fn3DF": "No/Verificado",
      "fn3C0": "No/Verificado",
      "fn3C1": "No/Verificado",
      "fn3C2": "No/Verificado",
      "fn3C3": "self.fn3C3(conn)",
      "fn3C4": "self.fn3C4(conn)",
      "fn3C5": "self.fn3C5(conn)",
      "fn3C6": "No/Verificado",
      "fn3C7": "No/Verificado",
      "fn3C8": "No/Verificado",
      "fn3C9": "No/Verificado",
      "fn3CA": "self.fn3CA(conn)",
      "fn4FA": "self.fn4FA(conn)",
      "fn5F0": "self.fn5F0(conn)",
      "fn5E0": "self.fn5E0(conn)",
      "fn5E1": "self.fn5E1(conn)",
      "fn5E2": "self.fn5E2(conn)",
      "fn5E3": "self.fn5E3(conn)",
      "fn5E4": "self.fn5E4(conn)",
      "fn5E5": "self.fn5E5(conn)",
      "fn5D0": "self.fn5D0(conn)",
      "fn6F0": "self.fn6F0(conn)",
      "fn6F1": "self.fn6F1(conn)",
      "fn6E0": "self.fn6E0(conn)",
      "fn6E1": "self.fn6E1(conn)",
      "fn6E2": "self.fn6E2(conn)",
      "fn6E3": "self.fn6E3(conn)",
      "fn6E4": "self.fn6E4(conn)",
      "fn6D0": "self.fn6D0(conn)",
      "fn6D1": "self.fn6D1(conn)",
      "fn6C0": "self.fn6C0(conn)",
      "fn6C1": "No/Verificado",
      "fn6C2": "self.fn6C2(conn)",
      "fn6B0": "self.fn6B0(conn)",
      "fn6B1": "No/Verificado",
      "fn6A0": "No/Verificado",
      "fn6A1": "No/Verificado",
      "fn6A2": "No/Verificado",
      "fn6A3": "No/Verificado",
      "fn690": "No/Verificado",
      "fn680": "self.fn680(conn)",
      "fn681": "self.fn681(conn)",
      "fn682": "self.fn682(conn)",
      "fn7F0": "self.fn7F0(conn)",
      "fn7F1": "self.fn7F1(conn)",
      "fn7F2": "self.fn7F2(conn)",
      "fn7F3": "self.fn7F3(conn)",
      "fn7F4": "self.fn7F4(conn)",
      "fn7F5": "self.fn7F5(conn)",
      "fn7F6": "No/Verificado",
      "fn8F0": "self.fn8F0(conn)",
      "fn8F1": "self.fn8F1(conn)",
      "fn8F2": "self.fn8F2(conn)",
      "fn8F3": "self.fn8F3(conn)",
      "fn9F0": "self.fn9F0(conn)",
      "fn9F1": "self.fn9F1(conn)",
      "fn9F2": "self.fn9F2(conn)",
      "fn9F3": "self.fn9F3(conn)"
    }
    print(type(self.args.function))
    if (self.args.function):
      __value = self.functions.get(self.args.function,None)
      if(__value):
        self.functions = {self.args.function:__value}

    self.args._FKErrorsFile = f'./{self.args.t_stamp}_ForenKeyErrors.csv'
    self.listValidations = self.cargarPlanillaConListasParaValidar()

  #----------------------------------------------------------------------------
  # Transforma archivo JSON en un DataFrame de pandas con todas sus columnas.
  # Agrega las columnas que faltan.
  #----------------------------------------------------------------------------
  def execute(self):
    _result = True
    sec = self.args.secPhase
    path = self.args.path_to_DB_file
    engine = create_engine(f"sqlite+pysqlcipher://:{sec}@/{path}?cipher=aes-256-cfb&kdf_iter=64000")
    try:
      conn = engine.connect()

      for key,value in self.functions.items():
        if(value != "No/Verificado"):
          logger.info(f"Ejecutando función {key} con los parámetros {value}")
          eval_ = eval(value)
          logger.info(f"Resultado de la evaluación de la función {key}: {eval_}")
          _result = eval_ and _result

      if(not _result):
        raise Exception("El archivo no cumple con el Estándar de Datos para la Educación.\
           Hay errores en la revisión. Revise el LOG para más detalles")

    except Exception as e:
      _t = "ERROR en la validación: "+str(e)
      logger.info(_t)
      _result = False
    finally:
      #closind database connection
      conn.close()
    return True#_result

  #Carga planilla con todas las listas de validación desde Google Drive
  #https://drive.google.com/open?id=1vZD8ufVm3Z71V9TveQcLI0A02wrmwsz43z3TyWl9C-s
  def cargarPlanillaConListasParaValidar(self):
    #idFile = '1vZD8ufVm3Z71V9TveQcLI0A02wrmwsz43z3TyWl9C-s'
    #url = f'https://docs.google.com/spreadsheets/d/{idFile}/export?format=xlsx&id={idFile}'
    url = './ede/ede/listValidationData.xlsx'
    xd = pd.read_excel(url,'ListValidations')
    _t=f'Planilla {url} cargada satisfactoriamente'; logger.info(_t)
    return xd

  #VERIFICA LA CONEXION A LA BASE DE DATOS
  def fn3F0(self,conn):
    _r = False
    rows = conn.execute("SELECT * FROM PersonList;").fetchall()
    if(len(rows)>0): _r = True
    logger.info("Aprobado") if _r else logger.error("Rechazado")
    return _r

  #VERIFICA LA INTEGRIDAD REFERENCIAL DE LOS DATOS
  def fn3F1(self,conn):
    _r = True; _e = ''
    rows = conn.execute("PRAGMA foreign_key_check;")

    if(rows.returns_rows):
      pd.DataFrame(rows,columns=['Table', 'rowId', 'Parent', 'FkId']).to_csv(
          self.args._FKErrorsFile,sep=self.args._sep,encoding=self.args._encode,index=False)
      _e = f"BD con errores, más detallen en {self.args._FKErrorsFile}"
      _r = False

    logger.info(f"RESULTADO DE LA VERIFICACIÓN DE LA INTEGRIDAD REFERENCIAL: {_r}. {_e}")
    logger.error("Rechazado") if (_e != '') else logger.info("Aprobado")
    return _r

  #VERIFICA SI LA VISTA PersonList contiene información
  def fn3F2(self, conn):
    try:
      rows = conn.execute("""
        SELECT
          RUN
          ,IPE
          ,emailAddress
          ,emailAddressType
          ,TelephoneNumber
          ,telephoneNumberType
          ,numeroListaCurso
          ,numeroMatricula
          ,fechaIncorporacionEstudiante
          ,fechaRetiroEstudiante
          ,fechaCumpleanos
          ,TribalAffiliationDescription
        FROM PersonList;
      """).fetchall()

      logger.info(f"len(personList): {len(rows)}")

      if(len(rows)>0):
        self.rutList = self.convertirArray2DToList(list([m[0] for m in rows if m[0] is not None])) # Valida lista de rut ingresados a la BD
        self.ipeList = self.convertirArray2DToList(list([m[1] for m in rows if m[1] is not None])) # Valida lista de IPE ingresados a la BD
        self.emailList = self.convertirArray2DToList(list([m[2] for m in rows if m[2] is not None])) #Valida que los email tengan el formato correcto
        self.emailTypeList = self.convertirArray2DToList(list([m[3] for m in rows if m[3] is not None])) #Valida que los emailType tengan el formato correcto
        self.phoneList = self.convertirArray2DToList(list([m[4] for m in rows if m[4] is not None])) # Valida que los teléfonos cumplan con el formato E164
        self.phoneTypeList = self.convertirArray2DToList(list([m[5] for m in rows if m[5] is not None])) # Valida que los tipos de teléfonos cumplan con el formato E164
        self.numListaList = self.convertirArray2DToList(list([m[6] for m in rows if m[6] is not None])) # Valida los número de lista de los cursos sean número
        self.numMatriculaList = self.convertirArray2DToList(list([m[7] for m in rows if m[7] is not None])) # Valida los números de matrícula del establecimiento sean número
        self.fechaIncorporacionEstudianteList = self.convertirArray2DToList(list([m[8] for m in rows if m[8] is not None])) # Valida que las fechas cumplan con el formato de fecha
        self.fechaRetiroEstudianteList = self.convertirArray2DToList(list([m[9] for m in rows if m[9] is not None])) # Valida que las fechas cumplan con el formato de fecha
        self.fechaCumpleanosList = self.convertirArray2DToList(list([m[10] for m in rows if m[10] is not None])) # Valida que las fechas cumplan con el formato de fecha
        self.AllDatesList = self.fechaIncorporacionEstudianteList+self.fechaRetiroEstudianteList+self.fechaCumpleanosList # Valida que las fechas cumplan con el formato de fecha
        self.TribalList = self.convertirArray2DToList(list(set([m[11] for m in rows if m[11] is not None]))) # Valida que las afiliaciones tribales sean las permitidas en Chile
        logger.info(f"Aprobado")
      else:
        logger.info(f"S/Datos")

      return True

    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta a la vista personList: {str(e)}")
      logger.error(f"Rechazado")
      return False

  #VERIFICA SI LA LISTA DE RUN INGRESADAS EN EL SISTEMA ES VALIDA
  def fn3F3(self):
    try:
      _l = self.rutList
      if(len(_l)>0):
        _err = set([e for e in _l if not self.validarRUN(e)])
        _r   = False if len(_err)>0 else True
        _t = f"VERIFICACION DEL RUN DE LAS PERSONAS: {_r}. {_err}"
        logger.info(_t) if _r else logger.error(_t)
        logger.info(f"Aprobado") if _r else logger.error(f"Rechazado")
      else:
        logger.info("S/Datos")
      return True
    except Exception as e:
      logger.error(f"NO se pudo ejecutar la verificación: {str(e)}")
      logger.error(f"Rechazado")
      return False

  #VERIFICA SI LA LISTA DE IPE INGRESADOS EN EL SISTEMA ES VALIDA
  def fn3F4(self):
    try:
      _l = self.ipeList
      if(len(_l)>0):
        _err = set([e for e in _l if not self.validarIpe(e)])
        _r   = False if len(_err)>0 else True
        _t = f"VERIFICACION DEL IPE DE LAS PERSONAS: {_r}. {_err}"
        logger.info(_t) if _r else logger.error(_t)
        logger.info(f"Aprobado") if _r else logger.error(f"Rechazado")
      else:
        logger.info("S/Datos")
      return True
    except Exception as e:
      logger.error(f"NO se pudo ejecutar la verificación: {str(e)}")
      logger.error(f"Rechazado")
      return False

  #VERIFICA SI LA LISTA DE e-mails INGRESADOS EN EL SISTEMA CUMPLE CON EL FORMATO
  def fn3F5(self):
    try:
      _l = self.emailList
      if(len(_l)>0):
        _err = set([e for e in _l if not validate_email(e)])
        _r   = False if len(_err)>0 else True
        _t = f"VERIFICACION DE FORMATO DE LOS E-MAILS DE LAS PERSONAS: {_r}. {_err}"
        logger.info(_t) if _r else logger.error(_t)
        logger.info(f"Aprobado") if _r else logger.error(f"Rechazado")
      else:
        logger.info("S/Datos")
      return True
    except Exception as e:
      logger.error(f"NO se pudo ejecutar la verificación: {str(e)}")
      logger.error(f"Rechazado")
      return False

  #VERIFICA SI LA LISTA DE teléfonos INGRESADOS cumple con el formato E164
  def fn3F6(self):
    try:
      _l = self.phoneList
      if(len(_l)>0):
        _err = set([e for e in _l if not self.validaFormatoE164Telefono(e)])
        _r   = False if len(_err)>0 else True
        _t = f"VERIFICACION DEL FORMATO DE LOS TELEFONOS DE LAS PERSONAS: {_r}. {_err}"
        logger.info(_t) if _r else logger.error(_t)
        logger.info(f"Aprobado") if _r else logger.error(f"Rechazado")
      else:
        logger.info("S/Datos")
      return True
    except Exception as e:
      logger.error(f"NO se pudo ejecutar la verificación: {str(e)}")
      logger.error(f"Rechazado")
      return False

  #VERIFICA SI EL NUMERO DE LISTA cumple con el formato
  def fn3F7(self):
    try:
      _l = self.numListaList
      if(len(_l)>0):
        _err = set([e for e in _l if not self.validaFormatoNumero(e)])
        _r   = False if len(_err)>0 else True
        _t = f"VERIFICACION DEL FORMATO DEL NUMERO DE LISTA DE LAS PERSONAS: {_r}. {_err}"
        logger.info(_t) if _r else logger.error(_t)
        logger.info(f"Aprobado") if _r else logger.error(f"Rechazado")
      else:
        logger.info("S/Datos")
      return True
    except Exception as e:
      logger.error(f"NO se pudo ejecutar la verificación: {str(e)}")
      logger.error(f"Rechazado")
      return False

  #VERIFICA SI EL NUMERO DE MATRICULA cumple con el formato
  def fn3F8(self):
    try:
      _l = self.numMatriculaList
      if(len(_l)>0):
        _err = set([e for e in _l if not self.validaFormatoNumero(e)])
        _r   = False if len(_err)>0 else True
        _t = f"VERIFICACION DEL NUMERO DE MATRICULA DE LAS PERSONAS: {_r}. {_err}"
        logger.info(_t) if _r else logger.error(_t)
        logger.info(f"Aprobado") if _r else logger.error(f"Rechazado")
      else:
        logger.info("S/Datos")
      return True
    except Exception as e:
      logger.error(f"NO se pudo ejecutar la verificación: {str(e)}")
      logger.error(f"Rechazado")
      return False

  #VERIFICA SI LA LISTA DE FECHAS INGRESADAS cumple con el formato
  def fn3F9(self):
    try:
      _l = self.AllDatesList
      if(len(_l)>0):
        _err = set([e for e in _l if not self.validaFormatoFecha(e)])
        _r   = False if len(_err)>0 else True
        _t = f"VERIFICACION DEL FORMATO DE LAS DE LAS PERSONAS: {_r}. {_err}"
        logger.info(_t) if _r else logger.error(_t)
        logger.info(f"Aprobado") if _r else logger.error(f"Rechazado")
      else:
        logger.info("S/Datos")
      return True
    except Exception as e:
      logger.error(f"NO se pudo ejecutar la verificación: {str(e)}")
      logger.error(f"Rechazado")
      return False

  #VERIFICA SI LA LISTA DE afiliaciones tribales se encuentra dentro de la lista permitida
  def fn3FA(self):
    try:
      _l = self.TribalList
      if(len(_l)>0):
        _err = set([e for e in _l if not self.validaTribalAffiliation(e)])
        _r   = False if len(_err)>0 else True
        _t = f"VERIFICACION DE LA LISTA DE AFILIACIONES TRIBALES DE LAS PERSONAS: {_r}. {_err}"
        logger.info(_t) if _r else logger.error(_t)
        logger.info(f"Aprobado") if _r else logger.error(f"Rechazado")
      else:
        logger.info("S/Datos")
      return True
    except Exception as e:
      logger.error(f"NO se pudo ejecutar la verificación: {str(e)}")
      logger.error(f"Rechazado")
      return False

  #Valida que la cantidad de #matricula == #Lista == #fechasIncorporaciónes
  def fn3FB(self):
    try:
      _l1 = self.numListaList;_l2 = self.numMatriculaList;_l3 = self.fechaIncorporacionEstudianteList
      if(len(_l1)>0 and len(_l2)>0 and len(_l3)>0):
        _r   = len(_l1) == len(_l2) == len(_l3)
        _t = f"Valida que la cantidad de #matricula == #Lista == #fechasIncorporaciónes: {_r}.  NumLista:{len(_l1)}, NumMat:{len(_l2)}, FechaIncorporación:{len(_l3)}"
        logger.info(_t) if _r else logger.error(_t)
        logger.info(f"Aprobado") if _r else logger.error(f"Rechazado")
      else:
        logger.info("S/Datos")
      return True
    except Exception as e:
      logger.error(f"No se pudo ejecutar la verificación: {str(e)}")
      logger.error(f"Rechazado")
      return False

  #VERIFICA que la cantidad de emails corresponda con los tipos de emails ingresados
  def fn3FC(self):
    try:
      _l1 = self.emailList;_l2 = self.emailTypeList
      if(len(_l1)>0 and len(_l2)>0):
        _r   = len(_l1) == len(_l2)
        _t = f"VERIFICA que la cantidad de e-mails corresponda con los tipos de e-mails ingresados en las personas: {_r}."
        logger.info(_t) if _r else logger.error(_t)
        logger.info(f"Aprobado") if _r else logger.error(f"Rechazado")
      else:
        logger.info("S/Datos")
      return True
    except Exception as e:
      logger.error(f"No se pudo ejecutar la verificación: {str(e)}")
      logger.error(f"Rechazado")
      return False

  #VERIFICA que la cantidad de teléfonos corresponda con los tipos de teléfonos ingresados
  def fn3FD(self):
    try:
      _l1 = self.phoneList;_l2 = self.phoneTypeList
      if(len(_l1)>0 and len(_l2)>0):
        _r   = len(_l1) == len(_l2)
        _t = f"VERIFICA que la cantidad de teléfonos corresponda con los tipos de teléfonos ingresados en las personas: {_r}."
        logger.info(_t) if _r else logger.error(_t)
        logger.info(f"Aprobado") if _r else logger.error(f"Rechazado")
      else:
        logger.info("S/Datos")
      return True
    except Exception as e:
      logger.error(f"No se pudo ejecutar la verificación: {str(e)}")
      logger.error(f"Rechazado")
      return False

  #VERIFICA SI LA VISTA PersonList filtrada por estudiantes contiene información
  def fn3FE(self, conn):
    try:
      rows = conn.execute("""
      SELECT
        personId
        ,ciudadNacimiento
        ,regionNacimiento
        ,paisNacimiento
      FROM PersonList
      WHERE Role like '%Estudiante%';
    """).fetchall()

      logger.info(f"len(estudiantes): {len(rows)}")

      if(len(rows)>0):
        personId  = self.convertirArray2DToList(list([m[0] for m in rows if m[0] is not None]))
        cuidadNac = self.convertirArray2DToList(list([m[1] for m in rows if m[1] is not None]))
        regionNac = self.convertirArray2DToList(list([m[2] for m in rows if m[2] is not None]))
        paisNac   = self.convertirArray2DToList(list([m[3] for m in rows if m[3] is not None]))
        self.comparaEstudiantes = [len(personId) == len(cuidadNac) == len(regionNac) == len(paisNac)]
        logger.info(f"Aprobado")
      else:
        logger.info(f"S/Datos")

      return True

    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta a la vista personList filtrada por estudiantes: {str(e)}")
      logger.error(f"Rechazado")
      return False

  #VERIFICA QUE TODOS LOS ESTUDIANTES TENGAN Pais, Región y cuidad de nacimiento
  def fn3FF(self):
    try:
      _l = self.comparaEstudiantes
      if(len(_l)>0):
        _r   = _l
        _t = f"VERIFICA QUE TODOS LOS ESTUDIANTES TENGAN Pais, Región y cuidad de nacimiento: {_r}."
        logger.info(_t) if _r else logger.error(_t)
        logger.info(f"Aprobado") if _r else logger.error(f"Rechazado")
      else:
        logger.info("S/Datos")
      return True
    except Exception as e:
      logger.error(f"No se pudo ejecutar la verificación: {str(e)}")
      logger.error(f"Rechazado")
      return False

  #VERIFICA SI LA VISTA PersonList filtrada por docentes contiene información
  def fn3E0(self, conn):
    try:
      rows = conn.execute("""
      SELECT
        personId
        ,DegreeOrCertificateTitleOrSubject
        ,DegreeOrCertificateTypeDescription
        ,AwardDate
        ,NameOfInstitution
        ,higherEducationInstitutionAccreditationStatusDescription
        ,educationVerificationMethodDescription
      FROM PersonList
      WHERE Role like '%Docente%';
    """).fetchall()

      logger.info(f"len(docentes): {len(rows)}")

      if(len(rows)>0):
        personId            = self.convertirArray2DToList(list([m[0] for m in rows if m[0] is not None]))
        title               = self.convertirArray2DToList(list([m[1] for m in rows if m[1] is not None]))
        Type                = self.convertirArray2DToList(list([m[2] for m in rows if m[2] is not None]))
        AwardDate           = self.convertirArray2DToList(list([m[3] for m in rows if m[3] is not None]))
        Institution         = self.convertirArray2DToList(list([m[4] for m in rows if m[4] is not None]))
        AccreditationStatus = self.convertirArray2DToList(list([m[5] for m in rows if m[5] is not None]))
        VerificationMethod  = self.convertirArray2DToList(list([m[6] for m in rows if m[6] is not None]))
        self.comparaDocentes = [len(personId) == len(title) == len(Type) == len(AwardDate) == len(Institution) == len(AccreditationStatus) == len(VerificationMethod)]
        logger.info(f"Aprobado")
      else:
        logger.info(f"S/Datos")

      return True

    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta a la vista personList filtrada por docentes: {str(e)}")
      logger.error(f"Rechazado")
      return False

  #VERIFICA QUE TODOS LOS DOCENTES TENGAN su título y la institución de educación ingresados en el sistema
  def fn3E1(self):
    try:
      _l = self.comparaDocentes
      if(len(_l)>0):
        _r   = _l
        _t = f"VERIFICA QUE TODOS LOS DOCENTES TENGAN su título y la institución de educación ingresados en el sistema: {_r}."
        logger.info(_t) if _r else logger.error(_t)
        logger.info(f"Aprobado") if _r else logger.error(f"Rechazado")
      else:
        logger.info("S/Datos")
      return True
    except Exception as e:
      logger.error(f"No se pudo ejecutar la verificación: {str(e)}")
      logger.error(f"Rechazado")
      return False

  #VERIFICA SI LA TABLA k12schoolList unida a organizationList contiene información
  def fn3E2(self, conn):
    try:
      rows = conn.execute("SELECT Identifier FROM k12schoolList INNER JOIN organizationList USING(OrganizationId);").fetchall()
      logger.info(f"len(establecimientos): {len(rows)}")
      if(len(rows)>0):
        self.formatoRBD = self.convertirArray2DToList(list(set([m[0] for m in rows if m[0] is not None])))
        logger.info(f"Aprobado")
      else:
        logger.info(f"S/Datos")

      return True

    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta a la tabla k12schoolList para identificar el RBD del establecimiento: {str(e)}")
      logger.error(f"Rechazado")
      return False

  #VERIFICA QUE EL FORMATO DEL RBD CORRESPONDA
  def fn3E3(self):
    try:
      _l = self.formatoRBD
      if(len(_l)>0):
        _err = set([e for e in _l if not self.validaFormatoRBD(e)])
        _r   = False if len(_err)>0 else True
        _t = f"VERIFICACION DEL FORMATO DEL RBD DEL ESTABLECIMIENTO: {_r}. {_err}"
        logger.info(_t) if _r else logger.error(_t)
        logger.info(f"Aprobado") if _r else logger.error(f"Rechazado")
      else:
        logger.info("S/Datos")
      return True
    except Exception as e:
      logger.error(f"No se pudo ejecutar la verificación: {str(e)}")
      logger.error(f"Rechazado")
      return False

  #VERIFICA SI LA VISTA jerarquiasList contiene información
  def fn3E4(self, conn):
    try:
      rows = conn.execute("SELECT RBD,nombreEstablecimiento,modalidad,jornada,nivel,rama,sector,especialidad,tipoCurso,codigoEnseñanza,grado,letraCurso  FROM jerarquiasList;").fetchall()
      logger.info(f"len(organizaciones): {len(rows)}")
      if(len(rows)>0):
        self.modalidadList = self.convertirArray2DToList(list(set([m[2] for m in rows if m[2] is not None])))
        self.jornadaList = self.convertirArray2DToList(list(set([m[3] for m in rows if m[3] is not None])))
        self.nivelList = self.convertirArray2DToList(list(set([m[4] for m in rows if m[4] is not None])))
        self.ramaList = self.convertirArray2DToList(list(set([m[5] for m in rows if m[5] is not None])))
        self.sectorList = self.convertirArray2DToList(list(set([m[6] for m in rows if m[6] is not None])))
        self.especialidadList = self.convertirArray2DToList(list(set([m[7] for m in rows if m[7] is not None])))
        self.tipoCursoList = self.convertirArray2DToList(list(set([m[8] for m in rows if m[8] is not None])))
        self.codigoEnseList = self.convertirArray2DToList(list(set([m[9] for m in rows if m[9] is not None])))
        self.gradoList = self.convertirArray2DToList(list(set([m[10] for m in rows if m[10] is not None])))
        self.letraCursoList = self.convertirArray2DToList(list(set([m[11] for m in rows if m[11] is not None])))
        logger.info(f"Aprobado")
      else:
        logger.info(f"S/Datos")

      return True

    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta a la vista jerarquiasList para obtener la lista de organizaciones: {str(e)}")
      logger.error(f"Rechazado")
      return False

  #VERIFICA QUE LA MODALIDAD ESTE DENTRO DE LA LISTA PERMITIDA
  def fn3E5(self):
    try:
      _l = self.modalidadList
      if(len(_l)>0):
        _err = set([e for e in _l if not self.validaModalidad(e)])
        _r   = False if len(_err)>0 else True
        _t = f"VERIFICA QUE LA MODALIDAD ESTE DENTRO DE LA LISTA PERMITIDA: {_r}. {_err}"
        logger.info(_t) if _r else logger.error(_t)
        logger.info(f"Aprobado") if _r else logger.error(f"Rechazado")
      else:
        logger.info("S/Datos")
      return True
    except Exception as e:
      logger.error(f"No se pudo ejecutar la verificación: {str(e)}")
      logger.error(f"Rechazado")
      return False

  #VERIFICA QUE LA JORNADA ESTE DENTRO DE LA LISTA PERMITIDA
  def fn3E6(self):
    try:
      _l = self.jornadaList
      if(len(_l)>0):
        _err = set([e for e in _l if not self.validaJornada(e)])
        _r   = False if len(_err)>0 else True
        _t = f"VERIFICA QUE LA JORNADA ESTE DENTRO DE LA LISTA PERMITIDA: {_r}. {_err}"
        logger.info(_t) if _r else logger.error(_t)
        logger.info(f"Aprobado") if _r else logger.error(f"Rechazado")
      else:
        logger.info("S/Datos")
      return True
    except Exception as e:
      logger.error(f"No se pudo ejecutar la verificación: {str(e)}")
      logger.error(f"Rechazado")
      return False

  #VERIFICA QUE EL NIVEL ESTA DENTRO DE LA LISTA PERMITIDA
  def fn3E7(self):
    try:
      _l = self.nivelList
      if(len(_l)>0):
        _err = set([e for e in _l if not self.validaNivel(e)])
        _r   = False if len(_err)>0 else True
        _t = f"VERIFICA QUE EL NIVEL ESTA DENTRO DE LA LISTA PERMITIDA: {_r}. {_err}"
        logger.info(_t) if _r else logger.error(_t)
        logger.info(f"Aprobado") if _r else logger.error(f"Rechazado")
      else:
        logger.info("S/Datos")
      return True
    except Exception as e:
      logger.error(f"No se pudo ejecutar la verificación: {str(e)}")
      logger.error(f"Rechazado")
      return False

  #VERIFICA QUE LA RAMA ESTA DENTRO DE LA LISTA PERMITIDA
  def fn3E8(self):
    try:
      _l = self.ramaList
      if(len(_l)>0):
        _err = set([e for e in _l if not self.validaRama(e)])
        _r   = False if len(_err)>0 else True
        _t = f"VERIFICA QUE LA RAMA ESTA DENTRO DE LA LISTA PERMITIDA: {_r}. {_err}"
        logger.info(_t) if _r else logger.error(_t)
        logger.info(f"Aprobado") if _r else logger.error(f"Rechazado")
      else:
        logger.info("S/Datos")
      return True
    except Exception as e:
      logger.error(f"No se pudo ejecutar la verificación: {str(e)}")
      logger.error(f"Rechazado")
      return False

  #VERIFICA QUE EL SECTOR ESTA DENTRO DE LA LISTA PERMITIDA
  def fn3E9(self):
    try:
      _l = self.sectorList
      if(len(_l)>0):
        _err = set([e for e in _l if not self.validaSector(e)])
        _r   = False if len(_err)>0 else True
        _t = f"VERIFICA QUE EL SECTOR ESTA DENTRO DE LA LISTA PERMITIDA: {_r}. {_err}"
        logger.info(_t) if _r else logger.error(_t)
        logger.info(f"Aprobado") if _r else logger.error(f"Rechazado")
      else:
        logger.info("S/Datos")
      return True
    except Exception as e:
      logger.error(f"No se pudo ejecutar la verificación: {str(e)}")
      logger.error(f"Rechazado")
      return False

  #VERIFICA QUE LA ESPECIALIDAD ESTA DENTRO DE LA LISTA PERMITIDA
  def fn3EA(self):
    try:
      _l = self.especialidadList
      if(len(_l)>0):
        _err = set([e for e in _l if not self.validaEspecialidad(e)])
        _r   = False if len(_err)>0 else True
        _t = f"VERIFICA QUE LA ESPECIALIDAD ESTA DENTRO DE LA LISTA PERMITIDA: {_r}. {_err}"
        logger.info(_t) if _r else logger.error(_t)
        logger.info(f"Aprobado") if _r else logger.error(f"Rechazado")
      else:
        logger.info("S/Datos")
      return True
    except Exception as e:
      logger.error(f"No se pudo ejecutar la verificación: {str(e)}")
      logger.error(f"Rechazado")
      return False

  #VERIFICA QUE EL TIPO DE CURSO ESTE DENTRO DE LA LISTA PERMITIDA
  def fn3EB(self):
    try:
      _l = self.tipoCursoList
      if(len(_l)>0):
        _err = set([e for e in _l if not self.validaTipoCurso(e)])
        _r   = False if len(_err)>0 else True
        _t = f"VERIFICA QUE EL TIPO DE CURSO ESTE DENTRO DE LA LISTA PERMITIDA: {_r}. {_err}"
        logger.info(_t) if _r else logger.error(_t)
        logger.info(f"Aprobado") if _r else logger.error(f"Rechazado")
      else:
        logger.info("S/Datos")
      return True
    except Exception as e:
      logger.error(f"No se pudo ejecutar la verificación: {str(e)}")
      logger.error(f"Rechazado")
      return False

  #VERIFICA QUE EL CODIGO DE ENSEÑANZA ESTE DENTRO DE LA LISTA PERMITIDA
  def fn3EC(self):
    try:
      _l = self.codigoEnseList
      if(len(_l)>0):
        _err = set([e for e in _l if not self.validaCodigoEnse(e)])
        _r   = False if len(_err)>0 else True
        _t = f"VERIFICA QUE EL CODIGO DE ENSEÑANZA ESTE DENTRO DE LA LISTA PERMITIDA: {_r}. {_err}"
        logger.info(_t) if _r else logger.error(_t)
        logger.info(f"Aprobado") if _r else logger.error(f"Rechazado")
      else:
        logger.info("S/Datos")
      return True
    except Exception as e:
      logger.error(f"No se pudo ejecutar la verificación: {str(e)}")
      logger.error(f"Rechazado")
      return False

  #VERIFICA QUE EL GRADO ESTE DENTRO DE LA LISTA PERMITIDA
  def fn3ED(self):
    try:
      _l = self.gradoList
      if(len(_l)>0):
        _err = set([e for e in _l if not self.validaGrado(e)])
        _r   = False if len(_err)>0 else True
        _t = f"VERIFICA QUE EL GRADO ESTE DENTRO DE LA LISTA PERMITIDA: {_r}. {_err}"
        logger.info(_t) if _r else logger.error(_t)
        logger.info(f"Aprobado") if _r else logger.error(f"Rechazado")
      else:
        logger.info("S/Datos")
      return True
    except Exception as e:
      logger.error(f"No se pudo ejecutar la verificación: {str(e)}")
      logger.error(f"Rechazado")
      return False

  #VERIFICA QUE LA LETRA DEL CURSO ESTE DENTRO DE LA LISTA PERMITIDA
  def fn3EE(self):
    try:
      _l = self.letraCursoList
      if(len(_l)>0):
        _err = set([e for e in _l if not self.validaLetraCurso(e)])
        _r   = False if len(_err)>0 else True
        _t = f"VERIFICA QUE LA LETRA DEL CURSO ESTE DENTRO DE LA LISTA PERMITIDA: {_r}. {_err}"
        logger.info(_t) if _r else logger.error(_t)
        logger.info(f"Aprobado") if _r else logger.error(f"Rechazado")
      else:
        logger.info("S/Datos")
      return True
    except Exception as e:
      logger.error(f"No se pudo ejecutar la verificación: {str(e)}")
      logger.error(f"Rechazado")
      return False

  #VERIFICA QUE COINCIDAN LOS ID'S DE LOS CURSOS EN LAS DIFERENTES TABLAS
  def fn3EF(self, conn):
    try:
      courses1 = conn.execute("SELECT OrganizationIdDelCurso FROM jerarquiasList;").fetchall()
      courses2 = conn.execute("SELECT OrganizationIdCurso FROM cursoList;").fetchall()
      logger.info(f"Vista jerarquiasList: {len(courses1)}, Vista cursoList: {len(courses2)}")
      if(len(courses1)>0 and len(courses2)>0):
        # Valida que lista de cursos coincidan
        curso1 = list(set([m[0] for m in courses1 if m[0] is not None]))
        curso2 = list(set([m[0] for m in courses2 if m[0] is not None]))
        _c = len(set(curso1) & set(curso2))
        _err = "No coinciden los ID de Curso en las tablas Organization + Course + K12Course"
        logger.info(f"Aprobado") if _c == len(curso1) == len(curso2) else logger.error(_err)
      else:
        logger.info(f"S/Datos")

      return True

    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta a la vista jerarquiasList para obtener la lista de organizaciones: {str(e)}")
      logger.error(f"Rechazado")
      return False

  # Verifica que cada asignatura se encuentre asociada a un curso.
  # Entrega los organizationID de las asignaturas 
  # que no están asociadas a ningún curso
  def fn3D0(self, conn):
    try:
      _ExistData = conn.execute("""
        SELECT count(OrganizationId)
        FROM OrganizationRelationship
        INNER JOIN Organization USING(OrganizationId)
        WHERE 
          -- PERMITE solo las organizaciones de tipo ASIGNATURA
          RefOrganizationTypeid in (
            SELECT RefOrganizationTypeid
            FROM RefOrganizationType 
            WHERE Description LIKE 'Course Section'
          )
      """).fetchall()
      if(_ExistData[0][0] == 0):
        logger.info(f"S/Datos")
        return True
      asignaturas = conn.execute("""
        /* 
        * Selecciona de la tabla Organization los ID's de todas las asignaturas
        * que no tengan un curso asociado 
        */ 
        WITH refOrganizationTypeAsignatura AS (SELECT RefOrganizationTypeid FROM RefOrganizationType WHERE Description LIKE 'Course Section')
                SELECT o.Organizationid 
                FROM Organization o
                WHERE 
                        -- Selecciona de la lista solo las organizaciones de tipo ASIGNATURA
                        RefOrganizationTypeid in refOrganizationTypeAsignatura AND 
                        -- Con el fin de encontrar las ASIGNATURAS que no se encuentren asociadas a ningún curso, 
                        -- se excluye de la lista las organizaciones que se encuentran correctamente asignadas
                        o.OrganizationId NOT IN (
                                -- Esta consulta obtiene la lista de ASIGNATURAS correctamente asignadas a un CURSO
                                SELECT OrganizationId
                                FROM OrganizationRelationship
                                INNER JOIN Organization USING(OrganizationId)
                                WHERE 
                                        -- PERMITE solo las organizaciones de tipo ASIGNATURA
                                        RefOrganizationTypeid in refOrganizationTypeAsignatura
                                        AND
                                        -- PERMITE solo las asignaciones que tengan como padre un CURSO
                                        Parent_OrganizationId IN (
                                                -- Obtiene la lista de Organizaciones de tipo CURSO
                                                SELECT OrganizationId 
                                                FROM Organization
                                                WHERE RefOrganizationTypeId IN (
                                                        -- Recupera el ID de referencia de las organizaciones tipo CURSO
                                                        SELECT RefOrganizationTypeid FROM RefOrganizationType WHERE Description LIKE 'Course'
                                                )
                                        )
                );
      """)
      if(asignaturas.returns_rows == 0):
        logger.info(f"Aprobado")
        return True
      
      asignaturas = asignaturas.fetchall()
      logger.info(f"Organizaciones no asociadas a ningún curso: {len(asignaturas)}")
      if(len(asignaturas) > 0):
        asignaturasList = list(set([m[0] for m in asignaturas if m[0] is not None]))
        _c = len(set(asignaturasList))
        _err = f"Las siguientes asignaturas no tienen ningún curso asociado: {asignaturasList}"
        logger.error(_err)
        logger.error(f"Rechazado")
        return False          
    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta a la verificación asignaturas sin curso asociado: {str(e)}")
      logger.error(f"Rechazado")
      return False


  # Verifica que el campo MaximumCapacity cumpla con la siguiente expresión regular: '^[1-9]{1}\d{1,3}$'
  #  y que todas las organizaciones de la tabla CourseSection sean de tipo ASIGNATURA
  def fn3D1(self, conn):
    try:
      MaximumCapacityErrors = []
      MaximumCapacityErrors = conn.execute("""
        -- Selecciona los Organizaciones de tipo ASIGNATURA que no cumplen con el criterio de la expresión regular
        SELECT OrganizationId, MaximumCapacity
        FROM CourseSection
        OUTER LEFT JOIN Organization USING(OrganizationId)
        WHERE 
          -- Agrega a la lista todos los registros que no cumplan con la expresión regular
          MaximumCapacity NOT REGEXP "^[1-9]{1}\d{1,3}$"
      """).fetchall()
    except Exception as e:
      pass
    try:  
      organizationMalAsignadas = []
      organizationMalAsignadas = conn.execute("""
          -- Selecciona las Organizaciones que no son de tipo ASIGNATURA 
          SELECT OrganizationId
          FROM CourseSection
          OUTER LEFT JOIN Organization USING(OrganizationId)
          WHERE 
                  -- Agrega a la lista todas las organizaciones que no sean de tipo ASIGNATURA
                  RefOrganizationTypeid NOT IN (
                          -- Rescata desde la tabla de referencia el ID de las organizaciones de tipo ASIGNATURA
                          SELECT RefOrganizationTypeid 
                          FROM RefOrganizationType 
                          WHERE Description LIKE 'Course Section'
                  )
      """).fetchall()
    except Exception as e:
      pass
    
    try:      
      logger.info(f"MaximunCapacity mal asignados: {len(MaximumCapacityErrors)}, Tabla CourseSection con organizacion mal asignadas: {len(organizationMalAsignadas)}")
      if(len(MaximumCapacityErrors)>0 or len(organizationMalAsignadas)>0):
        data1 = list(set([m[0] for m in MaximumCapacityErrors if m[0] is not None]))
        data2 = list(set([m[0] for m in organizationMalAsignadas if m[0] is not None]))
        _c1 = len(set(data1))
        _c2 = len(set(data2))
        _err1 = f"Las siguientes asignaturas no tiene el campo MaximumCapacity declarado correctamente: {data1}"
        _err2 = f"Las siguientes organizaciones no son de tipo asignaturas: {data2}"
        if (_c1 > 0):
          logger.error(_err1)
        if (_c2 > 0):
          logger.error(_err2)
        if (_c1 > 0 or _c2 > 0):
          logger.error(f"Rechazado")
          return False          
      else:
        logger.info(f"Aprobado")
        return True
    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta a la verificación asignaturas sin curso asociado: {str(e)}")
      logger.error(f"Rechazado")
      return False

  # Verifica que el campo MaximumCapacity cumpla con la siguiente expresión regular: '^[1-9]{1}\d{1,3}$'
  #  y que todas las organizaciones de la tabla CourseSection sean de tipo ASIGNATURA
  def fn3D2(self, conn):
    try:
      _ExistData = conn.execute("""
          SELECT count(RoleAttendanceEventId) FROM RoleAttendanceEvent
      """).fetchall()
      if(_ExistData[0][0]==0):
        logger.info(f"S/Datos")
        return True
      
      virtualIndicator = conn.execute("""
        /*
        * Selecciona los eventos que no tienen el campo VirtualIndicator
        * correctamente asignado
        */
        SELECT RoleAttendanceEventId 
        FROM RoleAttendanceEvent
        WHERE VirtualIndicator NOT IN (0,1);
      """)
      
      if(virtualIndicator.returns_rows == 0):
        logger.info(f"Aprobado")
        return True
      
      virtualIndicator = virtualIndicator.fetchall()
      logger.info(f"virtualIndicator mal asignados: {len(virtualIndicator)}")
      if(len(virtualIndicator)>0):
        data1 = list(set([m[0] for m in virtualIndicator if m[0] is not None]))
        _err1 = f"Los siguientes registros de la tabla RoleAttendanceEvent no tienen definidos el indicador de virtualidad del estudiante: {data1}"
        logger.error(_err1)
        logger.error(f"Rechazado")
        return False          
    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta a la verificación asignaturas sin curso asociado: {str(e)}")
      logger.error(f"Rechazado")
      return False

  # Verifica que el campo MaximumCapacity cumpla con la siguiente expresión regular: '^[1-9]{1}\d{1,3}$'
  #  y que todas las organizaciones de la tabla CourseSection sean de tipo ASIGNATURA
  def fn3D3(self, conn):
    try:
      _ExistData = conn.execute("""
        -- Lista todos los registros de la tabla CourseSectionSchedule
        -- si no hay información, se informa SIN DATOS
        SELECT count(ClassMeetingDays), count(ClassPeriod)
        FROM CourseSectionSchedule
      """).fetchall()
      if(_ExistData[0][0] == 0 and _ExistData[0][1] == 0):
        logger.info(f"S/Datos")
        return True      
      
      ClassMeetingDays = conn.execute("""
        -- Lista todos los registro del campo ClassMeetingDays de la tabla CourseSectionSchedule
        -- que no se encuentren dentro de la lista permitida
        WITH split(word, str) AS (
            SELECT '', ClassMeetingDays||',' FROM CourseSectionSchedule
            UNION ALL SELECT
            substr(str, 0, instr(str, ',')),
            substr(str, instr(str, ',')+1)
            FROM split WHERE str!=''
        ) SELECT DISTINCT word FROM split WHERE word!='' AND word NOT IN ('Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes');
      """)#.fetchall()
      ClassPeriod = conn.execute("""
        -- Lista todos los registro del campo ClassMeetingDays de la tabla CourseSectionSchedule
        -- que no se encuentren dentro de la lista permitida
        WITH split(word, str) AS (
            SELECT '', ClassPeriod||',' FROM CourseSectionSchedule
            UNION ALL SELECT
            substr(str, 0, instr(str, ',')),
            substr(str, instr(str, ',')+1)
            FROM split WHERE str!=''
        ) SELECT DISTINCT word FROM split WHERE word!='' AND word NOT IN ('Bloque01','Bloque02','Bloque03','Bloque04','Bloque05','Bloque06','Bloque07','Bloque08','Bloque09','Bloque10','Bloque11','Bloque12','Bloque13','Bloque14','Bloque15','Bloque16','Bloque17','Bloque18','Bloque19','Bloque20');
      """)#.fetchall()
      if(ClassMeetingDays.returns_rows == 0 and ClassPeriod.returns_rows == 0):
        logger.info(f"Aprobado")
        return True
      if(ClassMeetingDays.returns_rows != 0):
        ClassMeetingDays = ClassMeetingDays.fetchall()
        logger.info(f"ClassMeetingDays con formato errorneo: {len(ClassMeetingDays)}")
        data1 = list(set([m[0] for m in ClassMeetingDays if m[0] is not None]))        
        _c1 = len(set(data1))
        if (_c1 > 0):
          logger.error(f"Las siguientes registros tiene mal formateado el campo ClassMeetingDays: {data1}")
                
      if(ClassPeriod.returns_rows != 0):
        ClassPeriod = ClassPeriod.fetchall()
        logger.info(f"ClassPeriod con formato erroneo: {len(ClassPeriod)}")        
        data2 = list(set([m[0] for m in ClassPeriod if m[0] is not None]))
        _c2 = len(set(data2))
        if (_c2 > 0):
          logger.error(f"Las siguientes registros tienen mal formateado el campo ClassPeriod: {data2}")

      if (_c1 > 0 or _c2 > 0):
        logger.error(f"Rechazado")
        return False          
    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta a la verificación: {str(e)}")
      logger.error(f"Rechazado")
      return False

  # Verifica que el campo MaximumCapacity cumpla con la siguiente expresión regular: '^[1-9]{1}\d{1,3}$'
  #  y que todas las organizaciones de la tabla CourseSection sean de tipo ASIGNATURA
  def fn3C4(self, conn):
    try:
      RoleAttendanceEvent = conn.execute("""
        -- Lista todos los IDs que no cumplan con la empresión regular.
        SELECT RoleAttendanceEventId, Date
        FROM RoleAttendanceEvent
        WHERE 
        -- Agrega a la lista todos los registros que no cumplan con la expresión regular
        Date NOT REGEXP '^(19|2[0-9])[0-9]{2}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])([T ])(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])(.[0-9]+)?((\\+|-)(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]))$'
      """).fetchall()
      OrganizationPersonRole = conn.execute("""
        -- Lista todos los IDs que no cumplan con la empresión regular.
        SELECT OrganizationPersonRoleId, EntryDate, ExitDate
        FROM OrganizationPersonRole
        WHERE 
        -- Agrega a la lista todos los registros que no cumplan con la expresión regular
        EntryDate NOT REGEXP '^(19|2[0-9])[0-9]{2}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])([T ])(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])(.[0-9]+)?((\\+|-)(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]))$'
        OR
        ExitDate NOT REGEXP '^(19|2[0-9])[0-9]{2}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])([T ])(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])(.[0-9]+)?((\\+|-)(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]))$'
      """).fetchall()
      logger.info(f"RoleAttendanceEvent.Date con formato errorneo: {len(RoleAttendanceEvent)}, Tabla OrganizationPersonRole.EntryDate o ExitDate con formato errone: {len(OrganizationPersonRole)}")
      if(len(RoleAttendanceEvent)>0 or OrganizationPersonRole>0):
        data1 = list(set([m[0] for m in RoleAttendanceEvent if m[0] is not None]))
        data2 = list(set([m[0] for m in OrganizationPersonRole if m[0] is not None]))
        _c1 = len(set(data1))
        _c2 = len(set(data2))
        _err1 = f"Las siguientes registros tiene mal formateado el campo Date: {data1}"
        _err2 = f"Las siguientes registros tienen mal formateado el campo EntryDate o ExitDate: {data2}"
        if (_c1 > 0):
          logger.error(_err1)
        if (_c2 > 0):
          logger.error(_err2)
        if (_c1 > 0 or _c2 > 0):
          logger.error(f"Rechazado")
          return False          
      else:
        logger.info(f"Aprobado")
        return True
    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta a la verificación asignaturas sin curso asociado: {str(e)}")
      logger.error(f"Rechazado")
      return False

  # Revisar que los cursos del establecimiento tengan bien 
  # calculada la información de la tabla RoleAttendance.
  def fn3D9(self, conn):
    try:
      listInfoSuccesfull = conn.execute("""
        /*
        * verifica que los registro de calendar Session y RoleAttendanceEvent sean consistentes.
        */
        SELECT OrganizationId, RoleAttendanceEventid, OrganizationCalendarSession.OrganizationCalendarSessionId
        FROM Organization
        INNER JOIN RefOrganizationType USING(RefOrganizationTypeId)
        INNER JOIN OrganizationCalendar USING(OrganizationId)
        INNER JOIN OrganizationCalendarSession USING(OrganizationCalendarId)
        INNER JOIN OrganizationPersonRole USING(OrganizationId)
        INNER JOIN RoleAttendanceEvent USING(OrganizationPersonRoleId)
        WHERE
        RefOrganizationType.Description IN ('Course Section')
        AND
        AttendanceTermIndicator = 1
      """).fetchall()
      if(len(listInfoSuccesfull)<=0):
        logger.info("S/DATOS")
        return True
      else:
        RoleAttendance = conn.execute("""
          /*
          * verifica que los registro de calendar Session y RoleAttendanceEvent sean consistentes.
          */
          SELECT OrganizationId, r.RoleAttendanceEventid, OrganizationCalendarSession.OrganizationCalendarSessionId
          FROM (
            SELECT OrganizationId, RoleAttendanceEventid, AttendanceTermIndicator, OrganizationCalendarSession.OrganizationCalendarSessionId,DATETIME(DATE(BeginDate) || 'T' || TIME(SessionStartTime)) as 'InicioClase', RoleAttendanceEvent.Date, DATETIME(DATE(EndDate) || 'T' || TIME(SessionEndTime)) as 'FinClase', *
            FROM Organization
            OUTER LEFT JOIN RefOrganizationType USING(RefOrganizationTypeId)
            OUTER LEFT JOIN OrganizationCalendar USING(OrganizationId)
            OUTER LEFT JOIN OrganizationCalendarSession USING(OrganizationCalendarId)
            OUTER LEFT JOIN OrganizationPersonRole USING(OrganizationId)
            OUTER LEFT JOIN RoleAttendanceEvent USING(OrganizationPersonRoleId)
            WHERE
            RefOrganizationType.Description IN ('Course Section')
            AND
            InicioClase = RoleAttendanceEvent.Date
            AND AttendanceTermIndicator = 1
          ) as r
          INNER JOIN RefOrganizationType USING(RefOrganizationTypeId)
          INNER JOIN OrganizationCalendar USING(OrganizationId)
          INNER JOIN OrganizationCalendarSession USING(OrganizationCalendarId)
          INNER JOIN OrganizationPersonRole USING(OrganizationId)
          INNER JOIN RoleAttendanceEvent USING(OrganizationPersonRoleId)
        """).fetchall()
        logger.info(f"Eventos mal identificados: {len(RoleAttendance)}")
        if(len(RoleAttendance)>0):
          data1 = list(set([m[0] for m in RoleAttendance if m[0] is not None]))
          _c1 = len(set(data1))
          _err1 = f"Las siguientes organizaciones no coinciden: {data1}"
          if (_c1 > 0):
            logger.error(_err1)
            logger.error(f"Rechazado")
            return False          
        else:
          logger.info(f"Aprobado")
          return True
    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta a la verificación: {str(e)}")
      logger.error(f"Rechazado")
      return False


  # Revisar que los cursos del establecimiento tengan bien 
  # calculada la información de la tabla RoleAttendance.
  def fn3DA(self, conn):
    try:
      listInfoSuccesfull = conn.execute("""
        SELECT RoleAttendanceId
        FROM RoleAttendance
        OUTER LEFT JOIN OrganizationPersonRole USING(OrganizationPersonRoleId)
        OUTER LEFT JOIN Organization USING(OrganizationId)
        OUTER LEFT JOIN RefOrganizationType USING(RefOrganizationTypeId)
        OUTER LEFT JOIN Role USING(RoleId)
        OUTER LEFT JOIN RoleAttendanceEvent USING(OrganizationPersonRoleId)
        OUTER LEFT JOIN RefAttendanceStatus USING(RefAttendanceStatusId)
        OUTER LEFT JOIN RefAttendanceEventType USING(RefAttendanceEventTypeId)
        WHERE
        RefOrganizationType.Description IN ('Course')
        AND
        Role.Name IN ('Estudiante') -- filtra la asistencia de los estudiantes
        AND
        RefAttendanceEventType.Description IN ('Daily attendance') -- Filtra la asistencia diaria      
      """).fetchall()
      if(len(listInfoSuccesfull)<=0):
        logger.info("S/DATOS")
        return True
      else:
        RoleAttendance = conn.execute("""
          /*
          * Lista los registros de la Tabla RoleAttendance que no coinciden 
          * con la lista de eventos de asistencia regitrados en la tabla RoleAttendanceEvent
          */
          SELECT 
            ra.RoleAttendanceId,
            ifnull(ra.AttendanceRate, 0) as 'AttendanceRate_o',
            ifnull(result.AttendanceRate, 0) as 'AttendanceRate_r', 
            ifnull(ra.NumberOfDaysInAttendance, 0) as 'NumberOfDaysInAttendance_o', 
            ifnull(result.NumberOfDaysInAttendance, 0) as 'NumberOfDaysInAttendance_r', 
            ifnull(ra.NumberOfDaysAbsent, 0) as 'NumberOfDaysAbsent_o', 
            ifnull(result.NumberOfDaysAbsent, 0) as 'NumberOfDaysAbsent_r', 
            ifnull(result.totalDays, 0) as 'totalDays_r'
          FROM RoleAttendance as ra
          OUTER LEFT JOIN OrganizationPersonRole USING(OrganizationPersonRoleId)
          OUTER LEFT JOIN Organization USING(OrganizationId)
          OUTER LEFT JOIN RefOrganizationType USING(RefOrganizationTypeId)
          LEFT JOIN (
          -- Calcula el campo AttendanceRate a partir de la información de la tabla RoleAttendanceEvent
          SELECT *, CASE WHEN NumberOfDaysInAttendance NOT NULL THEN CAST(NumberOfDaysInAttendance / totalDays AS REAL) * 100 ELSE 0.00 END as 'AttendanceRate'
            FROM (
              -- Agrupando la información por estudiante, se cuenta los días presentes y ausentes de cada uno
              SELECT RoleAttendanceId,PersonId, RefOrganizationType.Description as 'OrganizationType', 
                CASE RefAttendanceStatus.Description 
                  WHEN 'Present' 
                    THEN count(personId)
                END as 'NumberOfDaysInAttendance',
                CASE 
                  WHEN RefAttendanceStatus.Description like '%Absence%' 
                    THEN count(personId)
                END as 'NumberOfDaysAbsent',
                count(personId) as 'totalDays'
              FROM RoleAttendance
              OUTER LEFT JOIN OrganizationPersonRole USING(OrganizationPersonRoleId)
              OUTER LEFT JOIN Organization USING(OrganizationId)
              OUTER LEFT JOIN RefOrganizationType USING(RefOrganizationTypeId)
              OUTER LEFT JOIN Role USING(RoleId)
              OUTER LEFT JOIN RoleAttendanceEvent USING(OrganizationPersonRoleId)
              OUTER LEFT JOIN RefAttendanceStatus USING(RefAttendanceStatusId)
              OUTER LEFT JOIN RefAttendanceEventType USING(RefAttendanceEventTypeId)
              WHERE 
              Role.Name IN ('Estudiante') -- filtra la asistencia de los estudiantes
              AND
              RefAttendanceEventType.Description IN ('Daily attendance') -- Filtra la asistencia diaria
              AND
              RefOrganizationType.Description IN ('Course') -- Filtra que la asistencia diaria se reporte a nivel de curso
              GROUP BY personId
            )) as result
          ON 
            ra.RoleAttendanceId = result.RoleAttendanceId
          WHERE 
          RefOrganizationType.Description IN ('Course') AND
          -- Filtra solo aquellos casos en que la información no coincide
          NOT (AttendanceRate_o = AttendanceRate_r AND NumberOfDaysInAttendance_o = NumberOfDaysInAttendance_r AND NumberOfDaysAbsent_o = NumberOfDaysAbsent_r)
        """).fetchall()
        logger.info(f"Localidades mal asignadas: {len(RoleAttendance)}")
        if(len(RoleAttendance)>0):
          data1 = list(set([m[0] for m in RoleAttendance if m[0] is not None]))
          _c1 = len(set(data1))
          _err1 = f"Los siguientes organizaciones no tienen sus AttendanceRate bien calculados: {data1}"
          if (_c1 > 0):
            logger.error(_err1)
            logger.error(f"Rechazado")
            return False          
        else:
          logger.info(f"Aprobado")
          return True
    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta a la verificación: {str(e)}")
      logger.error(f"Rechazado")
      return False

  # Revisar que la organización del establecimiento, asignaturas y cursos 
  # tengan asignada una localidad dentro del establecimiento.
  def fn3C3(self, conn):
    try:
      _ExistData = conn.execute("""
        SELECT count(OrganizationId)
        FROM Organization
        OUTER LEFT JOIN RefOrganizationType USING(RefOrganizationTypeId)
        WHERE RefOrganizationType.Description IN ('Course','Course Section')
      """).fetchall()
      if(_ExistData[0][0]==0):
        logger.info(f"S/Datos")
        return True      
      
      locations = conn.execute("""
        /*
        * Entrega la lista de organizaciones que no contiene bien definida su ubicación dentro del establecimiento.
        * Los campos obligatorios son: 
        *     RefOrganizationLocationType.Description == 'Physical'
        *     región NOT NULL AND País NOT NULL AND  ApartmentRoomOrSuiteNumber NOT NULL AND BuildingSiteNumber NOT NULL AND
                StreetNumberAndName NOT NULL AND City NOT NULL
        */
        SELECT OrganizationId
        FROM Organization
        OUTER LEFT JOIN RefOrganizationType USING(RefOrganizationTypeId)
        WHERE 
        RefOrganizationType.Description IN ('Course','Course Section')
        AND
        OrganizationId NOT IN (SELECT OrganizationId FROM (SELECT OrganizationId, RefOrganizationType.Description as 'organizationType' , LocationAddress.StreetNumberAndName, LocationAddress.ApartmentRoomOrSuiteNumber, LocationAddress.BuildingSiteNumber, LocationAddress.City, RefState.Description as 'Región', RefCountry.Description as 'País', RefOrganizationLocationType.RefOrganizationLocationTypeId, RefOrganizationLocationType.Description as 'TipoLocalidad'
                FROM Organization
                OUTER LEFT JOIN OrganizationWebsite USING(OrganizationId)
                OUTER LEFT JOIN OrganizationEmail USING(OrganizationId)
                OUTER LEFT JOIN OrganizationTelephone USING(OrganizationId)
                OUTER LEFT JOIN OrganizationLocation USING(OrganizationId)
                OUTER LEFT JOIN RefEmailType USING(RefEmailTypeId)
                OUTER LEFT JOIN RefInstitutionTelephoneType USING(RefInstitutionTelephoneTypeId)
                OUTER LEFT JOIN RefOrganizationLocationType USING(RefOrganizationLocationTypeId)
                OUTER LEFT JOIN LocationAddress USING(LocationId)
                OUTER LEFT JOIN RefState USING(RefStateId)
                OUTER LEFT JOIN RefCountry USING(RefCountryId)
                OUTER LEFT JOIN RefOrganizationType USING(RefOrganizationTypeId)
                WHERE 
                OrganizationType in ('Course','Course Section')
                AND
                tipoLocalidad in ('Physical')
                AND
                región NOT NULL
                AND
                País NOT NULL
                AND 
                ApartmentRoomOrSuiteNumber NOT NULL
                AND
                BuildingSiteNumber NOT NULL
                AND
                StreetNumberAndName NOT NULL
                AND
                City NOT NULL
        ));
      """)
      if(locations.returns_rows==0):
        logger.info(f"Aprobado")
        return True
      
      locations = locations.fetchall()
      logger.info(f"Localidades mal asignadas: {len(locations)}")
      if(len(locations)>0):
        data1 = list(set([m[0] for m in locations if m[0] is not None]))
        _c1 = len(set(data1))
        _err1 = f"Los siguientes organizaciones no tienen sus ubicaciones bien asignadas: {data1}"
        if (_c1 > 0):
          logger.error(_err1)
          logger.error(f"Rechazado")
          return False          
    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta a la verificación: {str(e)}")
      logger.error(f"Rechazado")
      return False

  """ 
  El campo OrganizationWebsite.Website debe estar definido para la organización del establecimiento
  El campo Organizationemail.addressElectronicMailAddress debe estar definido para la organización del establecimiento
  El campo Organizationemail.RefEmailTypeId debe estar definido para la organización del establecimiento, al menos, el tipo Organizational (school) address [3]
  Debe estar definido el número del establecimiento OrganizationTelephone.TelephoneNumber. Para la organización del establecimiento OrganizationTelephone.RefInstitutionTelephoneTypeId debe estar definido, al menos, los códigos Main phone number (2) y Administrative phone number (3), si son iguales se repite. 
  El primer código es para comunicarse directamente con La Dirección del establecimiento, el otro es para los llamados administrativos.
  Para la organización del establecimiento OrganizationLocation.RefOrganizationLocationTypeId debe estar definido Mailing [1], Physical [2] y Shipping [3], si es la misma para todos los casos, se debe repetir.
  """
  def fn3DD(self, conn):
    try:
      webSite = conn.execute("""
        -- Revisa que la organización tipo Establecimiento tenga registrada su página web
        SELECT OrganizationId, RefOrganizationType.Description as 'organizationType',Website
        FROM Organization
        OUTER LEFT JOIN OrganizationWebsite USING(OrganizationId)
        OUTER LEFT JOIN RefOrganizationType USING(RefOrganizationTypeId)
        WHERE 
        RefOrganizationType.Description IN ('K12 School')
        AND
        Website NOT REGEXP '^(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})$'
      """).fetchall()
      ElectronicMailAddress = conn.execute("""
        -- Revisa que la organización tipo Establecimiento tenga registrado su email de contacto
        SELECT OrganizationId, ElectronicMailAddress
        FROM Organization
        OUTER LEFT JOIN RefOrganizationType USING(RefOrganizationTypeId)
        OUTER LEFT JOIN OrganizationEmail USING(OrganizationId)
        OUTER LEFT JOIN RefEmailType USING(RefEmailTypeId)
        WHERE 
        RefOrganizationType.Description IN ('K12 School')
        AND
        ElectronicMailAddress NOT REGEXP '^(?:[a-z0-9!#$%&''*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&''*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])$'
        AND
        RefEmailType.Description IN ('Organizational (school) address')
      """).fetchall()
      phoneNumbers = conn.execute("""
        -- Revisa que la organización tipo Establecimiento tenga registrados sus teléfonos de contacto
        SELECT DISTINCT OrganizationId, RefOrganizationType.Description as 'organizationType', TelephoneNumber, RefInstitutionTelephoneType.Description as 'phoneType'--, LocationAddress.StreetNumberAndName, LocationAddress.ApartmentRoomOrSuiteNumber, LocationAddress.BuildingSiteNumber, LocationAddress.City, RefState.Description as 'Región', RefCountry.Description as 'País', LocationAddress.PostalCode, LocationAddress.Latitude, LocationAddress.Longitude, RefOrganizationLocationType.Description as 'TipoLocalidad'
        FROM Organization
        OUTER LEFT JOIN OrganizationTelephone USING(OrganizationId)
        OUTER LEFT JOIN RefInstitutionTelephoneType USING(RefInstitutionTelephoneTypeId)
        OUTER LEFT JOIN RefOrganizationType USING(RefOrganizationTypeId)
        WHERE 
        OrganizationType in ('K12 School')
        AND
        TelephoneNumber NOT REGEXP '^\+56\d{9,15}$'
        AND 
        phoneType IN ('Main phone number','Administrative phone number')
      """).fetchall()
      locations = conn.execute("""
        -- Revisa que las ubicaciones del establecimiento se encuentren bien definidas.
        SELECT DISTINCT OrganizationId, RefOrganizationType.Description as 'organizationType', LocationAddress.StreetNumberAndName, LocationAddress.ApartmentRoomOrSuiteNumber, LocationAddress.BuildingSiteNumber, LocationAddress.City, RefState.Description as 'Región', RefCountry.Description as 'País', LocationAddress.PostalCode, LocationAddress.Latitude, LocationAddress.Longitude, RefOrganizationLocationType.Description as 'TipoLocalidad'
        FROM Organization
        OUTER LEFT JOIN OrganizationLocation USING(OrganizationId)
        OUTER LEFT JOIN RefOrganizationLocationType USING(RefOrganizationLocationTypeId)
        OUTER LEFT JOIN LocationAddress USING(LocationId)
        OUTER LEFT JOIN RefState USING(RefStateId)
        OUTER LEFT JOIN RefCountry USING(RefCountryId)
        OUTER LEFT JOIN RefOrganizationType USING(RefOrganizationTypeId)
        WHERE 
        OrganizationType in ('K12 School')
        AND
        tipoLocalidad IN ('Physical', 'Mailing', 'Shipping')
        AND
        (ApartmentRoomOrSuiteNumber NOT NULL
        OR
        BuildingSiteNumber IS NULL
        OR
        LocationAddress.City IS NULL
        OR
        RefState.Description IS NULL
        OR
        RefCountry.Description IS NULL
        OR 
        LocationAddress.PostalCode IS NULL
        OR
        LocationAddress.Latitude IS NULL
        OR
        LocationAddress.Longitude IS NULL
        )
      """).fetchall()

      if(len(webSite)>0 or len(ElectronicMailAddress)>0 or len(phoneNumbers)>0 or len(locations)>0):
        data = list(set([m[0] for m in webSite if m[0] is not None]))
        if (len(set(data)) > 0): 
          logger.error(f"Website con formato erroneo: {data}")
          _err = True
        
        data = list(set([m[0] for m in ElectronicMailAddress if m[0] is not None]))
        if (len(set(data)) > 0): 
          logger.error(f"ElectronicMailAddress con formato erroneo: {data}")
          _err = True

        data = list(set([m[0] for m in phoneNumbers if m[0] is not None]))
        if (len(set(data)) > 0): 
          logger.error(f"phoneNumbers con formato erroneo: {data}")
          _err = True

        data = list(set([m[0] for m in locations if m[0] is not None]))
        if (len(set(data)) > 0): 
          logger.error(f"locations con formato erroneo: {data}")
          _err = True

        if (_err):
          logger.error(f"Rechazado")
          return False
      else:
        logger.info(f"Aprobado")
        return True
    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta a la verificación: {str(e)}")
      logger.error(f"Rechazado")
      return False

  def separaRUT(self, *args):
    if (len(args) > 0) and (args[0] is not None):
      dv = ''.join([c for c in list(args[0].upper()) if c.isalpha()])
      aux = ''.join([c for c in list(args[0]) if c.isdigit()])
      if(dv == ''):
        dv = aux[-1:]
        aux = aux[:-1]
    else:
      aux=0
      dv=0
    return aux,dv

  def validarRut(self, aux,dv):
    revertido = map(int, reversed(str(aux)))
    factors = cycle(range(2,8))
    s = sum(d * f for d, f in zip(revertido,factors))
    res = (-s)%11
    if ((str(res) == dv) or (dv=="K" and res==10)):
      return True
    return False

  #VERIFICA SI EL RUT INGRESADO ES VALIDO
  def validarRUN(self, *args):
    aux,dv = self.separaRUT(*args)
    if(aux!=0 and dv!=0):
      if(self.validarRut(aux,dv)):
        if(int(aux)<=47000000):
          return True
    return False

  def validarIpe(self, *args):
    aux,dv = self.separaRUT(*args)
    if(aux!=0 and dv!=0):
      if(self.validarRut(aux,dv)):
        if(int(aux)>=100000000):
          return True
    return False

  def convertirArray2DToList(self, text):
    _l = []
    for e in text:
      if "|" not in str(e):
        _l.append(e)
      else:
        for subE in e.split("|"):
          _l.append(subE)
    return _l

  def imprimeErrores(self, lista,fn,msg):
    _l = self.convertirArray2DToList(lista)
    _err = set([e for e in _l if not fn(e)])
    _r   = False if len(_err)>0 else True
    _t = f"{msg}: {_r}. {_err}";logger.info(_t)
    return _err,_r

  def validaFormatoE164Telefono(self, e):
    r = re.compile('^\+56\d{9,15}$')
    if(isinstance(e,str)):
      return r.match(e) is not None
    return False

  def validaFormatoNumero(self, e):
    r = re.compile('^\d{0,4}$')
    if(isinstance(e,str)):
      return r.match(e) is not None
    return False

  def validaFormatoFecha(self, e):
    r = re.compile('^((19|20)(\d{2})-(1[0-2]|0?[0-9])-([12][0-9]|3[01]|0?[1-9]))[ T]?((0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])(.\d{0,})?)?([+-](0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]))?$')
    if(isinstance(e,str)):
      return r.match(e) is not None
    return False

  def validaTribalAffiliation(self, e):
    _lista = list(set(self.listValidations['TribalAffiliationDescriptionList']))
    return True if e in _lista else False

  def validaBoolean(self, e):
    return e

  # VERIFICA DATOS DE LAS ORGANIZACIONES
  # VERIFICA JERARQUIA DE LOS DATOS
  # la jerarquí es:
  #  RBD -> Modalidad -> Jornada -> Niveles -> Rama ->
  #  Sector Económico -> Especialidad ->
  #  Tipo de Curso -> COD_ENSE -> Grado -> Curso -> Asignatura
  def validaFormatoRBD(self, e):
    r = re.compile('^RBD\d{5}$')
    if(isinstance(e,str)):
      return r.match(e) is not None
    return False

  def validaModalidad(self, e):
    _lista = list(set(self.listValidations['modalidadesList']))
    return True if e in _lista else False

  def validaJornada(self, e):
    _lista =  list(set(self.listValidations['jornadasList']))
    return True if e in _lista else False

  def validaNivel(self, e):
    _lista =  list(set(self.listValidations['nivelList']))
    return True if e in _lista else False

  def validaRama(self, e):
    _lista =  list(set(self.listValidations['ramaList']))
    return True if e in _lista else False

  def validaSector(self, e):
    _lista =  list(set(self.listValidations['sectorList']))
    return True if e in _lista else False

  def validaEspecialidad(self, e):
    _lista =  list(set(self.listValidations['especialidadList']))
    return True if e in _lista else False

  def validaTipoCurso(self, e):
    _lista =  list(set(self.listValidations['tipoCursoList']))
    return True if e in _lista else False

  def validaCodigoEnse(self, e):
    _lista =  list(set(self.listValidations['codigoEnseList']))
    return True if e in _lista else False

  def validaGrado(self, e):
    _lista =  list(set(self.listValidations['gradoList']))
    return True if e in _lista else False

  def validaLetraCurso(self, e):
    r = re.compile('^[A-Z]{1,2}$')
    if(isinstance(e,str)):
      return r.match(e) is not None
    return False

  def validaFormatoClaveAleatoria(self, e):
    r = re.compile('^[0-9]{6}([-]{1}[0-9kK]{1})?$')
    if(isinstance(e,str)):
      return r.match(e) is not None
    return False

  def validaEventosDeAsistencia(self, e):
    _r = False
    if (e[1] == 'Class/section attendance' and e[2] == 'Course Section'):
      _r = True
    elif (e[1] == 'Daily attendance' and e[2] == 'Course'):
      _r = True
    elif (e[0] == 'Reingreso autorizado' and e[2] == 'K12 School'):
      _r = True

    return _r

  # VERIFICA DATOS DE LAS ORGANIZACIONES
  def fn3C5(self, conn):
    try:
      rows = conn.execute("SELECT digitalRandomKey,firmaRatificador FROM RoleAttendanceEvent where digitalRandomKey not null;").fetchall()
      logger.info(f"len(ClaveAleatoriaDocente): {len(rows)}")
      if(len(rows)>0):
        # Valida los números de clave aleatoria de los docentes
        data = list(set([m[0] for m in rows if m[0] is not None])) + list(set([m[1] for m in rows if m[1] is not None]))
        _err,_r = self.imprimeErrores(data,self.validaFormatoClaveAleatoria,"VERIFICA FORMATO Clave Aleatoria Docente")
        logger.info(f"Aprobado") if _r else logger.error(_err)
      else:
        logger.info("La BD no contiene clave aleatoria de los docentes")
        logger.info("S/DATOS")

      return True
    except Exception as e:
      logger.error(f"No se pudieron validar los verificadores de indentidad: {str(e)}")
      logger.error(f"Rechazado")
      return False

  # Verificar que el evento “Daily attendance” sea solo asignado a  organizationId de tipo curso
  # Verificar que el evento “Class/section attendance” sea solo asignado a  organizationId de tipo asignatura
  # Verificar que el estado “Reingreso autorizado” sea solo asignado al organizationId del establecimiento
  def fn3CA(self, conn):
    try:
      rows = conn.execute("""
      SELECT ast.Description as 'RefAttendanceStatus',aet.Description as 'AttendanceEventType', orgt.Description as 'OrganizationType'
      FROM RoleAttendanceEvent rae
      INNER JOIN OrganizationPersonRole opr on opr.OrganizationPersonRoleId = rae.OrganizationPersonRoleId
      INNER JOIN Organization org on org.OrganizationId = opr.OrganizationId
      INNER JOIN RefAttendanceEventType aet on aet.RefAttendanceEventTypeId = rae.RefAttendanceEventTypeId
      INNER JOIN RefOrganizationType orgt on orgt.RefOrganizationTypeId = org.RefOrganizationTypeId
      INNER JOIN RefAttendanceStatus ast on ast.RefAttendanceStatusId = rae.RefAttendanceStatusId;
      """).fetchall()
      logger.info(f"len(OrganizationType): {len(rows)}")
      if(len(rows)>0):
        # Siempre deberían existir elementos de asistencia
        data = list(set([(m[0],m[1],m[2]) for m in rows if m[0] is not None]))
        _err,_r = self.imprimeErrores(data,self.validaEventosDeAsistencia,"VERIFICA que los eventos de asistencia se encuentren correctamente asignados")
        logger.info(f"Aprobado") if _r else logger.error(_err)
      else:
        logger.info("La BD no contiene información de asistencia cargada")
        logger.info("S/DATOS")

      return True
    except Exception as e:
      logger.error(f"No se pudo verificar que los eventos de asistencia esten bien asignados a las Organizaciones: {str(e)}")
      logger.error(f"Rechazado")
      return False



## WebClass INICIO ##
  ## Inicio fn2FA WC ##
  def fn2FA(self, conn):
            try:
                results = conn.execute("""
                select count(distinct PersonId)-(select count(distinct PersonId) from OrganizationPersonRole
                where RoleId=6
                and ExitDate is not null)
                from OrganizationPersonRole
                where  EntryDate is not null and RoleId=6  ;
                """).fetchall()

                resultsTwo = conn.execute("""
                SELECT count(distinct K12StudentEnrollment.OrganizationPersonRoleId)
                from K12StudentEnrollment
                where RefEnrollmentStatusId is not null
                AND FirstEntryDateIntoUSSchool IS NOT NULL;
                """).fetchall()

                if(len(results)>0 and len(resultsTwo)>0):
                    lista = list(set([m[0] for m in results if m[0] is not None]))
                    listaDos = list(set([m[0] for m in resultsTwo if m[0] is not None]))
                    if lista == listaDos:
                        logger.info(f"La cantidad de matriculados corresponder con los alumnos inscritos")
                        logger.info(f"Aprobado")
                        return True
                    else :
                        logger.error(f'La cantidad de alumnos matriculados no cocincide con los inscritos')
                        logger.error(f'Rechazado')
                        return False
                else:
                    logger.info(f"S/Datos")
                    logger.info(f'No hay registros de matriculas')
                    return False
            except Exception as e:
                logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
                logger.error(f"Rechazado")
                return False
  ## Fin fn2FA WC ##

  ##Inicio fn2EA WC ##
  def fn2EA(self, conn):
        try:
            results = conn.execute("""
              SELECT 
                (
                  select identifier  from PersonIdentifier pi 
                  JOIN RefPersonIdentificationSystem rfi on pi.RefPersonIdentificationSystemId=rfi.RefPersonIdentificationSystemId
                  WHERE Code like '%School%' and pi.PersonId=p.PersonId
                ) as "matricula" -- 0
                ,(
                  SELECT identifier from PersonIdentifier pi
                  join RefPersonIdentificationSystem rfi on pi.RefPersonIdentificationSystemId=rfi.RefPersonIdentificationSystemId
                  where (Code like '%IPE%' or Code like '%RUN%') and pi.PersonId=p.PersonId
                ) as "cedula" -- 1
                , p.FirstName as "primer nombre" -- 2
                , p.MiddleName as "otros nombres" -- 3
                , p.LastName as "apellidoPaterno" -- 4
                , p.SecondLastName as "apellidoMaterno" -- 5
                , case when RTA.Description is null then 'ninguna' else RTA.Description end as "tribalAffiationDescription" -- 6
                , Role.Name as rol -- 7
                , rf.Description as sexo -- 8
                , p.Birthdate as "fechaCumpleaños" -- 9
                , opr.EntryDate as "fecha de incorporacion" -- 10
                , RefCountry.Description as pais -- 11
                , rfs.Description as region -- 12
                , pa.City -- 13
                , rfc.Description as comuna -- 14
                , pa.AddressCountyName -- 15
                , pa.StreetNumberAndName as direccion -- 16
                , pa.ApartmentRoomOrSuiteNumber -- 17
                , pa.PostalCode -- 18
                , p2.FirstName as "Nombre Apoderado" -- 19
                , p2.MiddleName as "segundo nombre apoderado" -- 20
                , p2.LastName as "apellidoPaterno apoderado" -- 21
                , p2.SecondLastName as "apellidoMaterno apoderado" -- 22
                , RefCountry2.Description as paisApoderado -- 23
                , rfs2.Description as regionApoderado -- 24
                , pa2.City as ciudadapoderado -- 25
                , rfc2.Description as comunaApoderado -- 26
                , pa2.AddressCountyName -- 27
                , pa2.StreetNumberAndName as direccionApoderado -- 28
                , pa2.ApartmentRoomOrSuiteNumber -- 29
                , pa2.PostalCode as codigoPostalApoderado -- 30
                , rfpiv.Description -- 31
                , pt2.TelephoneNumber as numeroTelefonicoApoderado -- 32
                , rfptnt.Description as tipoNumeroApoderado -- 33
                , pt2.PrimaryTelephoneNumberIndicator -- 34
                , pea2.EmailAddress as emailApoderado -- 35
                , rfet.Description as tipoEmail -- 36
                , opr.ExitDate as fechaRetiro -- 37
                , opr.OrganizationId -- 38
                , p.personId --39
                , rprs.description -- 40
              FROM Person p 
                LEFT JOIN RefSex rf on p.RefSexId = rf.RefSexId
                LEFT JOIN OrganizationPersonRole opr on opr.PersonId=p.PersonId
                LEFT JOIN RefTribalAffiliation RTA on p.RefTribalAffiliationId = RTA.RefTribalAffiliationId
                LEFT JOIN Role on Role.RoleId=opr.RoleId
                LEFT JOIN PersonAddress pa on pa.PersonId=p.PersonId
                LEFT JOIN RefCountry on pa.RefCountryId = RefCountry.RefCountryId
                LEFT JOIN RefState rfs on pa.RefStateId= rfs.RefStateId
                LEFT JOIN RefCounty rfc on pa.RefCountyId = rfc.RefCountyId
                LEFT JOIN PersonRelationship prs on p.PersonId=prs.PersonId
				        LEFT JOIN RefPersonRelationship rprs on prs.RefPersonRelationshipId=rprs.RefPersonRelationshipId
                LEFT JOIN Person p2 on p2.PersonId=prs.RelatedPersonId 
                LEFT JOIN PersonAddress pa2 on pa2.PersonId=p2.PersonId
                LEFT JOIN RefCountry RefCountry2 on pa.RefCountryId = RefCountry2.RefCountryId
                LEFT JOIN RefState rfs2 on pa2.RefStateId= rfs2.RefStateId
                LEFT JOIN RefCounty rfc2 on pa2.RefCountyId = rfc2.RefCountyId
                LEFT JOIN RefPersonalInformationVerification rfpiv on pa2.RefPersonalInformationVerificationId = rfpiv.RefPersonalInformationVerificationId
                LEFT JOIN PersonTelephone pt2 on pt2.PersonId = p2.PersonId
                LEFT JOIN RefPersonTelephoneNumberType rfptnt on pt2.RefPersonTelephoneNumberTypeId = rfptnt.RefPersonTelephoneNumberTypeId
                LEFT JOIN PersonEmailAddress pea2 on p2.PersonId=pea2.PersonId
                LEFT JOIN RefEmailType rfet on rfet.RefEmailTypeId = pea2.RefEmailTypeId
                JOIN Organization o on o.OrganizationId=opr.OrganizationId
              WHERE 
                opr.RoleId IN (
                  SELECT RoleId
                  FROM Role
                  WHERE Name IN ('Estudiante')
                ) 
                AND
                o.RefOrganizationTypeId IN (
                  SELECT RefOrganizationTypeId
                  FROM RefOrganizationType
                  WHERE Description IN ('Course')
                )
              GROUP by  p.PersonId
            """)#.fetchall()
            
            if(results.returns_rows == 0):
              logger.error(f"S/DATOS")
              return True

            results = results.fetchall()
            for fila in results:
                # seccion=fila[38]
                # nivel = conn.execute("""select  Nivel.Name
                #     from Organization Nivel
                #     join RefOrganizationType rft on Nivel.RefOrganizationTypeId = rft.RefOrganizationTypeId
                #     join OrganizationRelationship or1 on or1.OrganizationId=Nivel.OrganizationId
                #     join OrganizationRelationship or2 on or1.OrganizationId=or2.Parent_OrganizationId
                #     join OrganizationRelationship or3 on or2.OrganizationId=or3.Parent_OrganizationId
                #     join OrganizationRelationship or4 on or3.OrganizationId=or4.Parent_OrganizationId
                #     join OrganizationRelationship or5 on or4.OrganizationId=or5.Parent_OrganizationId
                #     join OrganizationRelationship or6 on or5.OrganizationId=or6.Parent_OrganizationId
                #     join OrganizationRelationship or7 on or6.OrganizationId = or7.Parent_OrganizationId
                #     join OrganizationRelationship or8 on or7.OrganizationId = or8.Parent_OrganizationId
                #     where or8.OrganizationId= ?;""",([seccion])).fetchall()
                # cursos = conn.execute("""select asi.name from Organization asi join OrganizationRelationship ors on ors.OrganizationId=asi.OrganizationId
                #     where ors.Parent_OrganizationId = ?;""",([seccion])).fetchall()
                _response = True
                if (fila[0] is None):
                    logger.error(f"alumno sin matricula")
                    logger.error(f"Rechazado")
                    _response = False
                if (fila[1] is None):
                    logger.error(f"alumno sin RUN")
                    logger.error(f"Rechazado")
                    _response = False
                if (fila[2] is None ):
                    logger.error(f"alumno sin nombre")
                    logger.error(f"Rechazado")
                    _response = False
                if (fila[4] is None):
                    logger.error(f"alumno sin apellido paterno")
                    logger.error(f"Rechazado")
                    _response = False
                if (fila[5] is None):
                    logger.error(f"alumno sin apellido materno")
                    logger.error(f"Rechazado")
                    _response = False
                if (fila[6] is None):
                    logger.error(f"alumno sin tribalAffillation")
                    logger.error(f"Rechazado")
                    _response = False
                if (fila[7] is None):
                    logger.error(f"alumno sin rol")
                    logger.error(f"Rechazado")
                    _response = False
                if (fila[8] is None):
                    logger.error(f"alumno sin sexo")
                    logger.error(f"Rechazado")
                    _response = False
                if (fila[9] is None):
                    logger.error(f"alumno sin fecha cumpleaños")
                    logger.error(f"Rechazado")
                    _response = False
                if (fila[10] is None):
                    logger.error(f"alumno sin fecha de entrada")
                    logger.error(f"Rechazado")
                    _response = False
                if (fila[11] is None):
                    logger.error(f"alumno sin pais")
                    logger.error(f"Rechazado")
                    _response = False
                if (fila[12] is None):
                    logger.error(f"alumno sin region")
                    logger.error(f"Rechazado")
                    _response = False
                if (fila[13] is None):
                    logger.error(f"alumno sin ciudad")
                    logger.error(f"Rechazado")
                    _response = False
                if (fila[14] is None):
                    logger.error(f"alumno sin comuna")
                    logger.error(f"Rechazado")
                    _response = False
                if (fila[15] is None or fila[16] is None or fila[17] is None):
                    logger.error(f"alumno sin dirección")
                    logger.error(f"Rechazado")
                    _response = False
                if (fila[18] is None):
                    logger.error(f"alumno sin codigo postal")
                    logger.error(f"Rechazado")
                    _response = False
                if(fila[40] == 'Apoderado(a)/Tutor(a)'): #Verifica si existe un apoderado asignado al estudiante
                  if (fila[19] is None):
                      logger.error(f"apoderado alumno sin nombre")
                      logger.error(f"Rechazado")
                      _response = False
                  if (fila[21] is None):
                      logger.error(f"apoderado alumno sin apellido paterno")
                      logger.error(f"Rechazado")
                      _response = False
                  if (fila[22] is None):
                      logger.error(f"apoderado alumno sin apellido materno")
                      logger.error(f"Rechazado")
                      _response = False
                  if (fila[23] is None):
                      logger.error(f"apoderado alumno sin pais")
                      logger.error(f"Rechazado")
                      _response = False
                  if (fila[24] is None):
                      logger.error(f"apoderado alumno sin region")
                      logger.error(f"Rechazado")
                      _response = False
                  if (fila[25] is None):
                      logger.error(f"apoderado alumno sin ciudad")
                      logger.error(f"Rechazado")
                      _response = False
                  if (fila[26] is None):
                      logger.error(f"apoderado alumno sin comuma")
                      logger.error(f"Rechazado")
                      _response = False
                  if (fila[27] is None or fila[28] is None or fila[29] is None):
                      logger.error(f"apoderado alumno sin direccion")
                      logger.error(f"Rechazado")
                      _response = False
                  if (fila[30] is None):
                      logger.error(f"apoderado alumno sin codigo postal")
                      logger.error(f"Rechazado")
                      _response = False
                  if (fila[32] is None):
                      logger.error(f"apoderado alumno sin numero telefonico")
                      logger.error(f"Rechazado")
                      _response = False
                  if (fila[33] is None):
                      logger.error(f"apoderado alumno sin tipo de numero telefonico")
                      logger.error(f"Rechazado")
                      _response = False
                  if (fila[34] is None):
                      logger.error(f"apoderado alumno sin verificador de numero primario")
                      logger.error(f"Rechazado")
                      _response = False
                  if (fila[35] is None):
                      logger.error(f"apoderado alumno sin email")
                      logger.error(f"Rechazado")
                      _response = False
                  if (fila[36] is None):
                      logger.error(f"apoderado alumno sin tipo de email")
                      logger.error(f"Rechazado")
                      _response = False
                else:
                    logger.error(f"El estudiante no tiene un apoderdo asignado")
                    logger.error(f"Rechazado")
                    _response = False                  
            if(_response):
              logger.info(f"datos de alumnos validados")
              logger.error(f"Aprobado")
            return _response
        except Exception as e:
            logger.info(f"No se pudo ejecutar la consulta: {str(e)}")
            logger.info(f"Rechazado")
            return False
  ## Fin fn2EA WC ##

 ## Inicio fn7F0 WC ##
  def fn7F0(self,conn):
        try:
            _query = conn.execute("""
            SELECT A.AssessmentId,
                  ASSR.PersonId,
                  A.RefAssessmentTypeId
             FROM AssessmentResult R
                    JOIN AssessmentRegistration AR ON AR.AssessmentRegistrationId = R.AssessmentRegistrationId
                    JOIN AssessmentAdministration AA ON AR.AssessmentAdministrationId = AA.AssessmentAdministrationId
                    JOIN Assessment A ON AA.AssessmentId = A.AssessmentId
                    JOIN AssessmentSession ASN ON ASN.AssessmentAdministrationId = AA.AssessmentAdministrationId
                    JOIN AssessmentSessionStaffRole ASSR ON ASN.AssessmentSessionId = ASSR.AssessmentSessionId
                    JOIN OrganizationPersonRole OPR ON OPR.PersonId = ASSR.PersonId
                      WHERE ASSR.RefAssessmentSessionStaffRoleTypeId = 6
                        AND OPR.RoleId = 6
                  GROUP BY ASN.AssessmentAdministrationId, ASN.AssessmentSessionId, ASSR.AssessmentSessionStaffRoleId;
            """).fetchall()
            if(len(_query)>0):
                _contador = 0
                _assessment = int(len(_query))
                _assessmentType = (list([m[2] for m in _query if m[2] is not None]))
                for x in _assessmentType:
                    if (x == 28 or x == 29):
                        _contador += 1
                if _contador == _assessment:
                    logger.info(f'Todas las evaluaciones estan ingresadas como sumativas o formativas')
                    logger.info(f'Aprobado')
                    return True
                else:
                    logger.error(f'No todas las evaluaciones estan ingresadas como sumativas o formativas')
                    logger.error(f'Rechazado')
                    return False
            else:
                logger.error(f'S/Datos')
                logger.error(f'No se encuentran evaluaciones registradas en el establecimiento')
                return False
        except Exception as e:
            logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
            logger.error(f"Rechazado")
            return False
  ## Fin fn7F0 WC ##

  ## Inicio fn7F1 WC ##
  def fn7F1(self,conn):
        try:
            _query = conn.execute("""
            SELECT round(R.ScoreValue, 1) AS value,
                  R.ScoreValue           AS fullValue
            FROM AssessmentResult R
                    JOIN AssessmentRegistration AR ON AR.AssessmentRegistrationId = R.AssessmentRegistrationId
                    JOIN AssessmentAdministration AA ON AR.AssessmentAdministrationId = AA.AssessmentAdministrationId
                    JOIN Assessment A ON AA.AssessmentId = A.AssessmentId
                    JOIN AssessmentSession ASN ON ASN.AssessmentAdministrationId = AA.AssessmentAdministrationId
                    JOIN AssessmentSessionStaffRole ASSR ON ASN.AssessmentSessionId = ASSR.AssessmentSessionId
                    JOIN OrganizationPersonRole OPR ON OPR.PersonId = ASSR.PersonId
            WHERE A.RefAssessmentTypeId = 29
              AND R.RefScoreMetricTypeId IN (1, 2)
              AND ASSR.RefAssessmentSessionStaffRoleTypeId = 6
              AND OPR.RoleId = 6
            GROUP BY ASN.AssessmentAdministrationId, ASN.AssessmentSessionId, ASSR.AssessmentSessionStaffRoleId;
            """).fetchall()
            if(len(_query)>0):
                _contador = 0
                _assessment = int(len(_query))
                _assessmentScoreValue = (list([m[0] for m in _query if m[0] is not None]))
                _assessmentScoreFullValue = (list([m[1] for m in _query if m[1] is not None]))
                for y in _assessmentScoreFullValue:
                    if (len(y)>3):
                        logger.error(f'Se han ingresado calificaciones sumativas con mas de un decimal')
                        logger.error(f'Rechazado')
                        return False
                for x in _assessmentScoreValue:
                    if (x >= 1.0 and x <= 7.0):
                        _contador += 1
                if _contador == _assessment:
                    logger.info(f'Todas las evaluaciones sumativas estan ingresadas correctamente')
                    logger.info(f'Aprobado')
                    return True
                else:
                    logger.error(f'No todas las evaluaciones estan entre el rango permitido de 1.0 - 7.0')
                    logger.error(f'Rechazado')
                    return False
            else:
                logger.error(f'S/Datos')
                logger.error(f'No se encuentran evaluaciones sumativas registradas en el establecimiento')
                return False
        except Exception as e:
            logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
            logger.error(f"Rechazado")
            return False
  ## Fin fn7F1 WC ##

  ## Inicio fn7F2 WC ##
  def fn7F2(self,conn):
        try:
            _query = conn.execute("""
            SELECT DISTINCT PS.PersonId
            FROM OrganizationPersonRole OPR
                    JOIN Person P ON OPR.PersonId = P.PersonId
                    JOIN PersonStatus PS ON P.PersonId = PS.PersonId
            WHERE OPR.RoleId = 6
              AND PS.RefPersonStatusTypeId = 28;
            """).fetchall()
            if(len(_query)>0):
                _scoreQuery = conn.execute("""
                SELECT round((sum(replace(R.ScoreValue, ',', '')) / count(R.ScoreValue)), 0)
                FROM AssessmentResult R
                        JOIN AssessmentRegistration AR ON AR.AssessmentRegistrationId = R.AssessmentRegistrationId
                        JOIN AssessmentAdministration AA ON AR.AssessmentAdministrationId = AA.AssessmentAdministrationId
                        JOIN Assessment A ON AA.AssessmentId = A.AssessmentId
                        JOIN AssessmentSession ASN ON ASN.AssessmentAdministrationId = AA.AssessmentAdministrationId
                        JOIN AssessmentSessionStaffRole ASSR ON ASN.AssessmentSessionId = ASSR.AssessmentSessionId
                WHERE A.RefAssessmentTypeId = 28
                  AND R.RefScoreMetricTypeId IN (1, 2)
                  AND ASSR.RefAssessmentSessionStaffRoleTypeId = 6
                  AND ASSR.PersonId IN (SELECT DISTINCT PS.PersonId
                                        FROM OrganizationPersonRole OPR
                                                JOIN Person P ON OPR.PersonId = P.PersonId
                                                JOIN PersonStatus PS ON P.PersonId = PS.PersonId
                                        WHERE OPR.RoleId = 6
                                          AND PS.RefPersonStatusTypeId = 28
                )
                GROUP BY ASN.AssessmentAdministrationId, ASN.AssessmentSessionId, ASSR.AssessmentSessionStaffRoleId, ASSR.PersonId
                ORDER BY ASSR.PersonId ASC;
                """).fetchall()
                if(len(_scoreQuery)>0):
                    _score = (list([m[0] for m in _scoreQuery if m[0] is not None]))
                    for x in _score:
                        if x < 40:
                            logger.error(f'Existen alumnos promovidos con calificacion final inferior a 4,0')
                            logger.error(f'Rechazado')
                            return False
                    logger.info(f'Todos los alumnos aprobados cuentan con promedio final sobre 4,0')
                    logger.info(f'Aprobado')
                    return True
                else:
                    logger.error(f'Los alumnos ingresados como promovidos no cuentan con un registro de calificaciones en el establecimiento')
                    logger.error(f'Rechazado')
                    return False
            else:
                logger.error(f'No existen estudiantes promovidos en el establecimiento')
                logger.error(f'S/Datos')
                return True
        except Exception as e:
            logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
            logger.error(f"Rechazado")
            return False
  ## Fin fn7F2 WC ##

  ## Inicio fn7F3 WC ##
  def fn7F3(self,conn):
        try:
            _query = conn.execute("""
            SELECT LA.LearnerActivityId,
                LA.PersonId,
                LA.Weight,
                R.ScoreValue
            FROM LearnerActivity LA
                    JOIN AssessmentRegistration AR ON LA.AssessmentRegistrationId = AR.AssessmentRegistrationId
                    JOIN AssessmentAdministration AA ON AR.AssessmentAdministrationId = AA.AssessmentAdministrationId
                    JOIN Assessment A ON AA.AssessmentId = A.AssessmentId
                    JOIN AssessmentResult R ON AR.AssessmentRegistrationId = R.AssessmentRegistrationId
            WHERE A.RefAssessmentTypeId IN (28, 29)
            AND R.RefScoreMetricTypeId IN (1, 2);
            """).fetchall()
            if(len(_query)>0):
                _weight = (list([m[2] for m in _query if m[2] is not None]))
                for x in _weight:
                    if (x is None or x > 100 or x <= 0):
                        logger.error(f'El peso de la/s calificacion/es esta mal ingresado')
                        logger.error(f'Rechazado')
                        return False
                _scoreValue = (list([m[3] for m in _query if m[3] is not None]))
                for y in _scoreValue:
                    if (y is None):
                        logger.error(f'Existen Calificaciones mal ingresadas en el establecimiento')
                        logger.error(f'Rechazado')
                        return False
                logger.info(f'Calificaciones con su ponderacion ingresadas correctamente')
                logger.info(f'Aprobado')
                return True
            else:
                logger.error(f'S/Datos')
                logger.error(f'No se encuentran evaluaciones registradas en el establecimiento')
                return False
        except Exception as e:
            logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
            logger.error(f"Rechazado")
            return False
  ## Fin fn7F3 WC ##

  ## Inicio fn7F4 WC ##
  def fn7F4(self,conn):
        try:
            _query = conn.execute("""
            SELECT LearnerActivityId
            FROM LearnerActivity
            WHERE digitalRandomKey IS NOT NULL
            """).fetchall()
            if(len(_query)>0):
                _digitalRandom = conn.execute("""
                SELECT digitalRandomKey,
                      DateDigitalRandomKey,
                      personIDDigitalRandomKey
                FROM LearnerActivity
                WHERE LearnerActivityId IN (SELECT LearnerActivityId
                                            FROM LearnerActivity
                                            WHERE digitalRandomKey IS NOT NULL)
                AND DateDigitalRandomKey IS NOT NULL
                AND personIDDigitalRandomKey IS NOT NULL
                """).fetchall()
                if(len(_digitalRandom)==len(_query)):
                  _digitalRandomKeyPerson = conn.execute("""
                  SELECT personIDDigitalRandomKey
                  FROM LearnerActivity
                  WHERE LearnerActivityId IN (SELECT LearnerActivityId
                                              FROM LearnerActivity
                                              WHERE digitalRandomKey IS NOT NULL)
                    AND DateDigitalRandomKey IS NOT NULL
                    AND personIDDigitalRandomKey IS NOT NULL
                    AND personIDDigitalRandomKey IN (SELECT P.PersonId
                                                    FROM OrganizationPersonRole OPR
                                                              JOIN Person P ON OPR.PersonId = P.PersonId
                                                    WHERE OPR.RoleId IN (2, 4, 5));
                  """).fetchall()
                  if(len(_digitalRandom) == len(_digitalRandomKeyPerson)):
                    logger.info(f'Las modificaciones a las ponderaciones cuentan con firma del Docente/UTP')
                    logger.info(f'Aprobado')
                    return True
                  else:
                    logger.error(f'Las firmas ingresadas no corresponden a las del Docente/UTP')
                    logger.error(f'Rechazado')
                    return False
                else:
                  logger.error(f'Se han ingresado datos incompletos para las modificaciones de ponderaciones')
                  logger.error(f'Rechazado')
                  return False
            else:
              logger.error(f'No existen cambios realizados a las ponderaciones ')
              logger.error(f'S/Datos')
              return False
        except Exception as e:
            logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
            logger.error(f"Rechazado")
            return False
  ## Fin fn7F4 WC ##

  ## Inicio fn7F5 WC ##
  def fn7F5(self,conn):
        try:
            _query = conn.execute("""
            SELECT LA.LearnerActivityId
            FROM Assessment A
                    JOIN AssessmentAdministration AA ON A.AssessmentId = AA.AssessmentId
                    JOIN AssessmentRegistration AR ON AA.AssessmentAdministrationId = AR.AssessmentAdministrationId
                    JOIN LearnerActivity LA ON LA.AssessmentRegistrationId = AR.AssessmentRegistrationId
            ORDER BY LA.LearnerActivityId;
            """).fetchall()
            if(len(_query)>0):
                _organizationCalendarSession = conn.execute("""
                SELECT OrganizationCalendarSessionId
                FROM LearnerActivity
                WHERE LearnerActivityId IN (
                    SELECT LA.LearnerActivityId
                    FROM Assessment A
                            JOIN AssessmentAdministration AA ON A.AssessmentId = AA.AssessmentId
                            JOIN AssessmentRegistration AR ON AA.AssessmentAdministrationId = AR.AssessmentAdministrationId
                            JOIN LearnerActivity LA ON LA.AssessmentRegistrationId = AR.AssessmentRegistrationId
                    ORDER BY LA.LearnerActivityId)
                  AND OrganizationCalendarSessionId IS NOT NULL
                GROUP BY OrganizationCalendarSessionId;
                """).fetchall()
                if(len(_organizationCalendarSession)>0):
                    _calendar = conn.execute("""
                    SELECT 'Descripcion' as Descrip
                    FROM OrganizationCalendarSession
                    WHERE Description IS NOT NULL
                      AND Description <> ''
                      AND OrganizationCalendarSessionId in (
                        SELECT OrganizationCalendarSessionId
                        FROM LearnerActivity
                        WHERE LearnerActivityId IN (
                            SELECT LA.LearnerActivityId
                            FROM Assessment A
                                    JOIN AssessmentAdministration AA ON A.AssessmentId = AA.AssessmentId
                                    JOIN AssessmentRegistration AR ON AA.AssessmentAdministrationId = AR.AssessmentAdministrationId
                                    JOIN LearnerActivity LA ON LA.AssessmentRegistrationId = AR.AssessmentRegistrationId
                            ORDER BY LA.LearnerActivityId)
                          AND OrganizationCalendarSessionId IS NOT NULL
                        GROUP BY OrganizationCalendarSessionId)
                    """).fetchall()
                    if(len(_calendar) == len(_organizationCalendarSession)):
                      logger.info(f'Todas las evaluaciones registradas en el establecimiento poseen registro de contenidos en los calendarios')
                      logger.info(f'Aprobado')
                      return True
                    else:
                      logger.error(f'No se han ingresado en los calendarios la descripcion del contenido impartido')
                      logger.error(f'Rechazado')
                      return False
                else:
                    logger.error(f'Las evaluaciones registradas no poseen registro en los calendarios')
                    logger.error(f'Rechazdo')
                    return False
            else:
                logger.error(f'No evaluaciones registradas en el establecimiento ')
                logger.error(f'S/Datos')
                return False
        except Exception as e:
            logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
            logger.error(f"Rechazado")
            return False
  ## Fin fn7F5 WC ##

  ## Inicio fn2DA WC ##
  def fn2DA(self,conn):
        try:
            _query = conn.execute("""
            SELECT DISTINCT PS.PersonId
            FROM OrganizationPersonRole OPR
                    join Person P on OPR.PersonId = P.PersonId
                    join PersonStatus PS on P.PersonId = PS.PersonId
            WHERE OPR.RoleId = 6
              and PS.RefPersonStatusTypeId = 27
            """).fetchall()
            if(len(_query)>0):
              _personStatusFile = conn.execute("""
              SELECT fileScanBase64
              FROM PersonStatus
              WHERE PersonId in (
                  SELECT DISTINCT PS.PersonId
                  FROM OrganizationPersonRole OPR
                          join Person P on OPR.PersonId = P.PersonId
                          join PersonStatus PS on P.PersonId = PS.PersonId
                  WHERE OPR.RoleId = 6
                    and PS.RefPersonStatusTypeId = 27
              )
              AND fileScanBase64 is not null;
              """).fetchall()
              if (len(_query) == len(_personStatusFile)):
                  _file = conn.execute("""
                  SELECT documentId
                  FROM Document
                  WHERE fileScanBase64 IS NOT NULL
                      AND fileScanBase64 <> ''
                      AND documentId IN (
                          select fileScanBase64
                          from PersonStatus
                          where PersonId in (
                              select DISTINCT PS.PersonId
                              from OrganizationPersonRole OPR
                                      join Person P on OPR.PersonId = P.PersonId
                                      join PersonStatus PS on P.PersonId = PS.PersonId
                              where OPR.RoleId = 6
                                and PS.RefPersonStatusTypeId = 27
                          )
                            and fileScanBase64 is not null
                      );
                  """).fetchall()
                  if(len(_file) == len(_query)):
                    logger.info(f'Todos los alumnos nuevos con matricula definitiva poseen documento')
                    logger.info(f'Aprobado')
                    return True
                  else:
                    logger.error(f'los alumnos nuevos con matricula definitiva no poseen documento')
                    logger.error(f'Rechazado')
                    return False
              else:
                logger.error(f'Los alumnos nuevos con matricula definitiva no poseen documento')
                logger.error(f'Rechazado')
                return False
            else:
                logger.error(f'No existen alumnos nuevos con matricula definitiva')
                logger.error(f'S/Datos')
                return False
        except Exception as e:
            logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
            logger.error(f"Rechazado")
            return False
  ## Fin fn2DA WC ##

  ## Inicio fn2DB WC ##
  def fn2DB(self,conn):
        try:
            _query = conn.execute("""
            SELECT DISTINCT P.PersonId
            FROM OrganizationPersonRole OPR
                    join Person P on OPR.PersonId = P.PersonId
                    join PersonStatus PS on P.PersonId = PS.PersonId
            where OPR.RoleId = 6
              and PS.RefPersonStatusTypeId = 33;
            """).fetchall()
            if(len(_query)>0):
              _queryType = conn.execute("""
              SELECT PS.fileScanBase64
              FROM PersonStatus PS
              WHERE PS.PersonId in (select DISTINCT P.PersonId
                                    from OrganizationPersonRole OPR
                                            join Person P on OPR.PersonId = P.PersonId
                                            join PersonStatus PS on P.PersonId = PS.PersonId
                                    where OPR.RoleId = 6
                                      and PS.RefPersonStatusTypeId = 33)
                and PS.fileScanBase64 is not null
                and PS.RefPersonStatusTypeId = 33
              """).fetchall
              if(len(_queryType) == len(_query)):
                _file = conn.execute("""
                SELECT documentId
                FROM Document
                WHERE fileScanBase64 IS NOT NULL
                  AND fileScanBase64 <> ''
                  AND documentId in (SELECT PS.fileScanBase64
                                    FROM PersonStatus PS
                                    WHERE PS.PersonId in (select DISTINCT P.PersonId
                                                          from OrganizationPersonRole OPR
                                                                    join Person P on OPR.PersonId = P.PersonId
                                                                    join PersonStatus PS on P.PersonId = PS.PersonId
                                                          where OPR.RoleId = 6
                                                            and PS.RefPersonStatusTypeId = 33)
                                      and PS.fileScanBase64 is not null
                                      and PS.RefPersonStatusTypeId = 33);
                """).fetchall()
                if(len(_file) == len(_query)):
                  logger.info(f'Todos los alumnos matriculados bajo el decreto 152 poseen su documento correspondiente')
                  logger.info(f'Aprobado')
                  return True
                else:
                  logger.error(f'Los alumnos matriculados bajo el decreto 152 no poseen su documento correspondiente')
                  logger.error(f'Rechazado')
                  return False
              else:
                logger.error(f'No existe documento para los alumnos matriculados bajo el decreto 152')
                logger.error(f'Rechazado')
                return False
            else:
                logger.info(f"S/Datos")
                logger.info(f"No existen alumnos matriculados bajo el decreto 152, artículo 60")
                return True
        except Exception as e:
            logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
            logger.error(f"Rechazado")
            return False
  ## Fin fn2DB WC ##

  ## Inicio fn2CA WC ##
  def fn2CA(self,conn):
        try:
            _query = conn.execute("""
              SELECT DISTINCT p.PersonId
              FROM OrganizationPersonRole OPR
              OUTER LEFT JOIN Person P on OPR.PersonId = P.PersonId
              OUTER LEFT JOIN PersonStatus PS on P.PersonId = PS.PersonId
              OUTER LEFT JOIN RefPersonStatusType on RefPersonStatusType.refPersonStatusTypeId = PS.refPersonStatusTypeId
              OUTER LEFT JOIN Document USING(fileScanBase64)
              WHERE RefPersonStatusType.Description IN ('Estudiante retirado definitivamente')
            """).fetchall()
            if(len(_query)>0):
                _queryOK = conn.execute("""
                    SELECT DISTINCT p.PersonId
                    FROM OrganizationPersonRole OPR
                    OUTER LEFT JOIN Person P on OPR.PersonId = P.PersonId
                    OUTER LEFT JOIN PersonStatus PS on P.PersonId = PS.PersonId
                    OUTER LEFT JOIN RefPersonStatusType on RefPersonStatusType.refPersonStatusTypeId = PS.refPersonStatusTypeId
                    OUTER LEFT JOIN Document USING(fileScanBase64)
                    WHERE 
                      RefPersonStatusType.Description IN ('Estudiante retirado definitivamente')
                      and p.personId NOT IN (
                        SELECT DISTINCT p.PersonId
                        FROM OrganizationPersonRole OPR
                        JOIN Person P on OPR.PersonId = P.PersonId
                        JOIN PersonStatus PS on P.PersonId = PS.PersonId
                        JOIN RefPersonStatusType on RefPersonStatusType.refPersonStatusTypeId = PS.refPersonStatusTypeId
                        JOIN Document USING(fileScanBase64)
                        WHERE
                          OPR.RoleId = 6
                          and p.RecordEndDateTime IS NULL and PS.RecordEndDateTime IS NULL and OPR.RecordEndDateTime IS NULL
                          and PS.StatusStartDate IS NOT NULL and PS.StatusEndDate IS NOT NULL and PS.Description IS NOT NULL
                          and RefPersonStatusType.Description IN ('Estudiante retirado definitivamente')	
                          and documentId IS NOT NULL and length(Document.fileScanBase64) > 0
                      )                
                """).fetchall()              
                _data =  list(set([m[0] for m in _queryOK if m[0] is not None]))
                if(len(_query)==len(_data)):
                  logger.info(f'Todos los alumnos retirados del establecimiento cuentan con su fecha, motivo y declaración jurada.')
                  logger.info(f'Aprobado')
                  return True
                else:
                  logger.error(f'Los siguientes alumnos retirados del establecimiento no cuentan su fecha, motivo o declaración jurada: {_data}')
                  logger.error(f'Rechazado')
                  return False
            else:
                logger.error(f'S/Datos')
                logger.error(f'No existen registros de alumnos retirados del establecimiento')
                return True
        except Exception as e:
            logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
            logger.error(f"Rechazado")
            return False
  ## Fin fn2CA WC ##

  ## Inicio fn2CB WC ##
  def fn2CB(self,conn):
        try:
            _query = conn.execute("""
            SELECT OPR.OrganizationPersonRoleId
            FROM OrganizationPersonRole OPR
                    JOIN Person P on OPR.PersonId = P.PersonId
                    JOIN PersonStatus PS on P.PersonId = PS.PersonId
            WHERE OPR.RoleId = 6
              AND PS.RefPersonStatusTypeId = 30;
            """).fetchall()
            if(len(_query)>0):
                _queryEntregaDocumentos = conn.execute("""
                SELECT I.IncidentId
                from Incident I
                        join IncidentPerson IP on I.IncidentId = IP.IncidentId
                where I.RefIncidentBehaviorId = 33
                  and I.OrganizationPersonRoleId in (SELECT OPR.OrganizationPersonRoleId
                                                    from OrganizationPersonRole OPR
                                                              join Person P on OPR.PersonId = P.PersonId
                                                              join PersonStatus PS on P.PersonId = PS.PersonId
                                                    where OPR.RoleId = 6
                                                      and PS.RefPersonStatusTypeId = 30);
                """).fetchall()
                if(len(_query)==len(_queryEntregaDocumentos)):
                  logger.info(f'Todos los alumnos retirados del establecimiento cuentan con una entrega de documentos respectiva al apoderado')
                  logger.info(f'Aprobado')
                  return True
                else:
                  logger.error(f'Los alumnos retirados del establecimiento no cuentan con un registro de entrega de documentos al apoderado')
                  logger.error(f'Rechazado')
                  return False
            else:
                logger.error(f'S/Datos')
                logger.error(f'No existen registro de alumnos retirados del establecimiento')
                return True
        except Exception as e:
            logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
            logger.error(f"Rechazado")
            return False
  ## Fin fn2CB WC ##

   ## Inicio fn2BA WC ##
  def fn2BA(self,conn):
        try:
            _query = conn.execute("""
            SELECT DISTINCT P.PersonId
            from OrganizationPersonRole OPR
                    join Person P on OPR.PersonId = P.PersonId
                    join PersonStatus PS on P.PersonId = PS.PersonId
            where OPR.RoleId = 6
              and PS.RefPersonStatusTypeId IN (25, 24, 31);
            """).fetchall()
            if (len(_query)>0):
              _queryExcedentes = conn.execute("""
              SELECT fileScanBase64
              from PersonStatus
              where PersonId in (
                  SELECT DISTINCT P.PersonId
                  FROM OrganizationPersonRole OPR
                          join Person P on OPR.PersonId = P.PersonId
                          join PersonStatus PS on P.PersonId = PS.PersonId
                  where OPR.RoleId = 6
                    and PS.RefPersonStatusTypeId IN (25, 24, 31))
                and fileScanBase64 is not null
                and RefPersonStatusTypeId IN (25, 24, 31);
              """).fetchall()
              if (len(_queryExcedentes) == len(_query)):
                _file = conn.execute("""
                SELECT documentId
                FROM Document
                WHERE fileScanBase64 IS NOT NULL
                  AND fileScanBase64 <> ''
                  AND documentId in (select fileScanBase64
                                    from PersonStatus
                                    where PersonId in (
                                        select DISTINCT P.PersonId
                                        from OrganizationPersonRole OPR
                                                  join Person P on OPR.PersonId = P.PersonId
                                                  join PersonStatus PS on P.PersonId = PS.PersonId
                                        where OPR.RoleId = 6
                                          and PS.RefPersonStatusTypeId IN (25, 24, 31)
                                    )
                                      and fileScanBase64 is not null
                                      and RefPersonStatusTypeId IN (25, 24, 31)
                )
                """).fetchall()
                if(len(_file) == len(_query)):
                  logger.info(f'Todos los alumnos excedentes cuentan con su documento correspondiente')
                  logger.info(f'Aprobado')
                  return True
                else:
                  logger.error(f'Los alumnos excedentes no cuentan con su documento correspondiente')
                  logger.error(f'Rechazado')
                  return False
              else:
                logger.error(f'Los alumnos excedentes no cuentan con su documento correspondiente')
                logger.error(f'Rechazado')
                return False
            else:
                logger.error(f'S/Datos')
                logger.error(f'No existen alumnos excedentes en el establecimiento')
                return True
        except Exception as e:
            logger.error(f'NO se pudo ejecutar la verificación en la lista')
            logger.error(f'Rechazado')
            return False
  ## Fin fn2BA WC ##

  ## Inicio fn29A WC ##
  def fn29A(self, conn):
        try:
            results = conn.execute("""
            SELECT opr.PersonId,
                  (SELECT o2.OrganizationId
                    from OrganizationPersonRole opr2
                            join Organization o2 on o2.OrganizationId = opr2.OrganizationId
                    where RefOrganizationTypeId = 21
                      and opr2.PersonId = opr.PersonId)                              as seccion,

                  (SELECT opr3.OrganizationPersonRoleId
                    from OrganizationPersonRole opr3
                    where opr3.PersonId = opr.PersonId)                              as personrole,

                  (SELECT grado.OrganizationId
                    from Organization grado
                            join RefOrganizationType rft on grado.RefOrganizationTypeId = rft.RefOrganizationTypeId
                            join OrganizationRelationship or1 on or1.OrganizationId = grado.OrganizationId
                            join OrganizationRelationship or2 on or1.OrganizationId = or2.Parent_OrganizationId
                    where or2.OrganizationId = (SELECT o2.OrganizationId
                                                from OrganizationPersonRole opr2
                                                        join Organization o2 on o2.OrganizationId = opr2.OrganizationId
                                                where o2.RefOrganizationTypeId = 21
                                                  and opr2.PersonId = opr.PersonId)) as grado,
                  o3.Name
            FROM OrganizationPersonRole opr
                    join Organization o on o.OrganizationId = opr.OrganizationId
                    join K12StudentEnrollment k12se on k12se.OrganizationPersonRoleId = personrole
                    join Organization o3 on o3.OrganizationId = grado
                    join PersonStatus ps on opr.PersonId = ps.PersonId
            where o.RefOrganizationTypeId = 47 /*cambiar a id respectivo, este id hace referencia a el nuevo tipo de organizacion agregado para practicaProfesional*/
              and k12se.RefEnrollmentStatusId = 2
              and cast(strftime('%Y', k12se.FirstEntryDateIntoUSSchool) as integer) =
                  cast(strftime('%Y', current_timestamp) as integer)
              and ps.RefPersonStatusTypeId = 26;
            """).fetchall()
            if(len(results)>0):
                lista = list(set([m[0] for m in results if m[0] is not None]))
                lista2 = list(set([m[4] for m in results if m[4] is not None]))
                con=len(lista)
                x=0
                for l1 in lista:
                    grado=(lista2[x][4])
                    if (grado[-8:-1].lower()=="3° medio"):
                        results2 = conn.execute("""
                        SELECT opr.organizationid
                        FROM OrganizationPersonRole opr
                                join K12StudentCourseSection k12cs on opr.OrganizationPersonRoleId = k12cs.OrganizationPersonRoleId
                                join Organization o on o.OrganizationId = opr.OrganizationId
                        where PersonId = ?
                          and k12cs.RefCourseSectionEnrollmentStatusTypeId = 6
                          and cast(strftime('%Y', opr.EntryDate) as integer) = cast(strftime('%Y', current_timestamp) as integer);
                        """,[l1]).fetchall()
                        if (len(results2))<1:
                            logger.error(f"alumno en practica  de 3 año sin requisito de semestre cumplido")
                            logger.error(f"Rechazado")
                            return False
                    x+=x
                logger.info(f"todos los alumnos de practica cumplen con los requisitos")
                logger.info(f"Aprobado")
                return True

            else:
                logger.info(f"S/Datos")
                logger.info(f"No existen alumnos en practica registrados")
                return True

        except Exception as e:
            logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
            logger.error(f"Rechazado")
            return False
  ## Fin fn29A WC ##

  ## Inicio fn29B WC ##
  def fn29B(self, conn):
        try:
            query = conn.execute("""
            SELECT OPR.OrganizationId, P.PersonId, count(P.PersonId)
            from Person P
                    join OrganizationPersonRole OPR on P.PersonId = OPR.PersonId
                    join PersonStatus PS on P.PersonId = PS.PersonId
            where RoleId = 6
              and ps.RefPersonStatusTypeId = 35
              and OrganizationPersonRoleId in (select OrganizationId
                                              from Organization
                                              where RefOrganizationTypeId = 47)
            group by OPR.OrganizationId, P.PersonId;
            """).fetchall()
            k12StudentEnrollment = conn.execute("""
            select OrganizationPersonRoleId
            from K12StudentEnrollment;
            """).fetchall()
            if(len(query)>0 and len(k12StudentEnrollment)>0):
                estudiantes = (list([m[2] for m in query if m[2] is not None]))
                organizaciones = (list([m[0] for m in query if m[0] is not None]))
                organizacionesK12 = (list([m[0] for m in k12StudentEnrollment if m[0] is not None]))
                for x in estudiantes:
                    if(x == 2):
                        logger.error(f"Matriculas repetidas")
                        logger.error(f"Rechazado")
                        return False
                    else:
                        for y in organizacionesK12:
                            for z in organizaciones:
                                if(y in z):
                                    contador = contador + 1
                                else:
                                    logger.error(f"Matricula/s no registrada/s")
                                    logger.error(f"Rechazado")
                                    return False
                logger.info(f'Matriculas ingresadas correctamente')
                logger.info(f'Aprobado')
                return True
            else:
                logger.info(f"S/Datos")
                logger.info(f"No existen alumnos en practica registrados")
                return True
        except Exception as e:
            logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
            logger.error(f"Rechazado")
            return False
  ## Fin fn29B WC ##

  ## Inicio fn29C WC ##
  def fn29C(self, conn):
        try:
            _queryStud = conn.execute("""
            SELECT OPR.OrganizationId
            FROM OrganizationPersonRole OPR
                    join Person P on OPR.PersonId = P.PersonId
                    join Organization O on OPR.OrganizationId = O.OrganizationId
            WHERE OPR.RoleId = 6
              AND O.RefOrganizationTypeId = 47
            GROUP by P.PersonId,
                    OPR.OrganizationId;
            """).fetchall()

            _queryProf = conn.execute("""
            SELECT OPR.OrganizationId
            FROM OrganizationPersonRole OPR
                    join Person P on OPR.PersonId = P.PersonId
                    join Organization O on OPR.OrganizationId = O.OrganizationId
            WHERE OPR.RoleId = 17
              AND O.RefOrganizationTypeId = 47
            GROUP by P.PersonId,
                    OPR.OrganizationId;
            """).fetchall()
            if((len(_queryStud)>0) and (len(_queryProf)>0)):
                _organizationStu = (list([m[5] for m in _queryStud if m[0] is not None]))
                if not _organizationStu :
                    logger.error(f"Sin Alumnos")
                    logger.error(f'Rechazado')
                    return False
                _organizationProf = (list([m[5] for m in _queryProf if m[0] is not None]))
                if not _organizationProf :
                    logger.error(f"Sin profesores")
                    logger.error(f'Rechazado')
                    return False
                _contador = 0
                z = len(_organizationStu)
                for x in _organizationStu:
                    for y in _organizationProf:
                        if x in y:
                            _contador += 1
                if _contador == z:
                    logger.info(f'Todos los alumnos en practica con profesor')
                    logger.info(f'Aprobado')
                    return True
                else:
                    logger.error(f'Alumnos en practica sin profesor')
                    logger.error(f'Rechazado')
                    return False
            else:
                logger.info(f"S/Datos")
                logger.info(f"No existen alumnos en practica registrados")
                return True
        except Exception as e:
            logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
            logger.error(f"Rechazado")
            return False
  ## Fin fn29C WC ##

  ## Inicio fn5E0 WC ##
  def fn5E0(self, conn):
        try:
            _ExistData = conn.execute("""
                SELECT DISTINCT 
                  rae.Date, -- fecha completa de la clase
                  strftime('%Y-%m-%d', rae.Date) as 'fecha', -- rescata solo la fecha desde rae.Date
                  strftime('%H:%M', rae.Date, substr(rae.Date,length(rae.Date)-5,6)) as 'hora', -- rescata solo la hora desde rae.Date
                  CASE 
                    WHEN strftime('%w', rae.Date) = '0' THEN 'Domingo'
                    WHEN strftime('%w', rae.Date) = '1' THEN 'Lunes'
                    WHEN strftime('%w', rae.Date) = '2' THEN 'Martes'
                    WHEN strftime('%w', rae.Date) = '3' THEN 'Miercoles'
                    WHEN strftime('%w', rae.Date) = '4' THEN 'Jueves'
                    WHEN strftime('%w', rae.Date) = '5' THEN 'Viernes'
                    WHEN strftime('%w', rae.Date) = '6' THEN 'Sabado'
                  END as 'diaSemana', -- rescata solo el dpia de la semana desde rae.Date
                  count(refattendancestatusid) as 'totalEstudiantes', -- Cantidad total de estudiantes
                  sum(CASE WHEN refattendancestatusid IN (1) THEN 1 ELSE 0 END) as 'estudiantesPresentes', 
                  group_concat(CASE WHEN refattendancestatusid IN (1) THEN Identifier END) as 'estudiantesPresentesNumLista',
                  sum(CASE WHEN refattendancestatusid IN (2,3) THEN 1 ELSE 0 END) as 'estudiantesAusentes',
                  group_concat(CASE WHEN refattendancestatusid IN (2,3) THEN Identifier END) as 'estudiantesAusentesNumLista',	
                  sum(CASE WHEN refattendancestatusid IN (4) THEN 1 ELSE 0 END) as 'estudiantesRetrasados',
                  group_concat(CASE WHEN refattendancestatusid IN (4) THEN Identifier END) as 'estudiantesRetrasadosNumLista',
                  count(rae.digitalRandomKey) as 'firmadoEnClases'
                FROM Organization O
                  OUTER LEFT JOIN RefOrganizationType rot
                    ON O.RefOrganizationTypeId = rot.RefOrganizationTypeId
                    AND O.RefOrganizationTypeId IN (
                      SELECT RefOrganizationTypeId 
                      FROM RefOrganizationType
                      WHERE Description IN ('Course Section')
                    ) 
                  OUTER LEFT JOIN OrganizationPersonRole opr 
                    ON O.OrganizationId = opr.OrganizationId
                    AND opr.RecordEndDateTime IS NULL
                  OUTER LEFT JOIN RoleAttendanceEvent rae
                    ON opr.OrganizationPersonRoleId = rae.OrganizationPersonRoleId
                    AND rae.RecordEndDateTime IS NULL
                  OUTER LEFT JOIN PersonIdentifier pid
                    ON opr.personId = pid.personId
                    AND pid.refPersonIdentificationSystemId IN (
                      SELECT refPersonIdentificationSystemId
                      FROM refPersonIdentificationSystem
                      WHERE Code IN ('listNumber')
                    )
                    AND pid.RecordEndDateTime IS NULL
                  OUTER LEFT JOIN Role rol
                    ON opr.RoleId = rol.RoleId
                    AND opr.RoleId IN (
                      SELECT RoleId
                      FROM Role
                      WHERE Name IN ('Estudiante')
                    )
                  OUTER LEFT JOIN OrganizationCalendar oc 
                    ON O.OrganizationId = oc.OrganizationId
                    AND oc.RecordEndDateTime IS NULL
                  OUTER LEFT JOIN OrganizationCalendarSession ocs
                    ON oc.OrganizationCalendarId = ocs.OrganizationCalendarId
                    AND ocs.RecordEndDateTime IS NULL
                  OUTER LEFT JOIN CourseSectionSchedule css
                    ON O.OrganizationId = css.OrganizationId
                    AND css.RecordEndDateTime IS NULL
                WHERE 
                  Date is not NULL
                GROUP BY rae.Date         
            """).fetchall()
            if(not _ExistData):
              raise Exception("No hay registros de información")
        except Exception as e:
            logger.info(f"S/Datos")
            logger.info(f'Sin asistencia por bloque: {e}')
            return True
        try:
            asistencia = conn.execute("""
                /*
                6.2 Contenido mínimo, letra b.2 -> validar el registro de asistencia bloque a bloque
                Verifica:
                - Que contenga sea de tipo Asignatura ('Course Section')
                - Que el rol del estudiante este asignado al registro ('Estudiante')
                - Que esten registrados los números de lista (pid.refPersonIdentificationSystemId) 
                de los estudiantes ausentes, atrasados y presentes.
                - Que este presente el verificador de identidad (rae.digitalRandomKey NOT NULL)
                de la persona que se encuentre trabajando con el estudiante.
                - Que se encuentre cargado el indicado de virtualidad (rae.VirtualIndicator).
                - Que se encuentre cargado la descripción de lo realizado en clases (ocs.Description NOT NULL)
                - Que la hora de la toma de asistencia se encuentre en el horario de clases
                (strftime('%H:%M', rae.Date) between ClassBeginningTime and ClassEndingTime) [Aquí no arroja error pero si una advertencia]
                */
                SELECT DISTINCT 
                  --group_concat(rae.Date),
                  rae.Date, -- fecha completa de la clase
                  strftime('%Y-%m-%d', rae.Date) as 'fecha', -- rescata solo la fecha desde rae.Date
                  strftime('%H:%M', rae.Date, substr(rae.Date,length(rae.Date)-5,6)) as 'hora', -- rescata solo la hora desde rae.Date
                  CASE 
                    WHEN strftime('%w', rae.Date) = '0' THEN 'Domingo'
                    WHEN strftime('%w', rae.Date) = '1' THEN 'Lunes'
                    WHEN strftime('%w', rae.Date) = '2' THEN 'Martes'
                    WHEN strftime('%w', rae.Date) = '3' THEN 'Miercoles'
                    WHEN strftime('%w', rae.Date) = '4' THEN 'Jueves'
                    WHEN strftime('%w', rae.Date) = '5' THEN 'Viernes'
                    WHEN strftime('%w', rae.Date) = '6' THEN 'Sabado'
                  END as 'diaSemana', -- rescata solo el dpia de la semana desde rae.Date
                  count(refattendancestatusid) as 'totalEstudiantes', -- Cantidad total de estudiantes
                  sum(CASE WHEN refattendancestatusid IN (1) THEN 1 ELSE 0 END) as 'estudiantesPresentes', 
                  group_concat(CASE WHEN refattendancestatusid IN (1) THEN Identifier END) as 'estudiantesPresentesNumLista',
                  sum(CASE WHEN refattendancestatusid IN (2,3) THEN 1 ELSE 0 END) as 'estudiantesAusentes',
                  group_concat(CASE WHEN refattendancestatusid IN (2,3) THEN Identifier END) as 'estudiantesAusentesNumLista',	
                  sum(CASE WHEN refattendancestatusid IN (4) THEN 1 ELSE 0 END) as 'estudiantesRetrasados',
                  group_concat(CASE WHEN refattendancestatusid IN (4) THEN Identifier END) as 'estudiantesRetrasadosNumLista',
                  count(rae.digitalRandomKey) as 'firmadoEnClases'
                FROM Organization O
                  JOIN RefOrganizationType rot
                    ON O.RefOrganizationTypeId = rot.RefOrganizationTypeId
                    AND O.RefOrganizationTypeId IN (
                      SELECT RefOrganizationTypeId 
                      FROM RefOrganizationType
                      WHERE Description IN ('Course Section')
                    ) 
                  JOIN OrganizationPersonRole opr 
                    ON O.OrganizationId = opr.OrganizationId
                    AND opr.RecordEndDateTime IS NULL
                  JOIN RoleAttendanceEvent rae
                    ON opr.OrganizationPersonRoleId = rae.OrganizationPersonRoleId
                    AND rae.RecordEndDateTime IS NULL
                  JOIN PersonIdentifier pid
                    ON opr.personId = pid.personId
                    AND pid.refPersonIdentificationSystemId IN (
                      SELECT refPersonIdentificationSystemId
                      FROM refPersonIdentificationSystem
                      WHERE Code IN ('listNumber')
                    )
                    AND pid.RecordEndDateTime IS NULL
                  JOIN Role rol
                    ON opr.RoleId = rol.RoleId
                    AND opr.RoleId IN (
                      SELECT RoleId
                      FROM Role
                      WHERE Name IN ('Estudiante')
                    )
                  JOIN OrganizationCalendar oc 
                    ON O.OrganizationId = oc.OrganizationId
                    AND oc.RecordEndDateTime IS NULL
                  JOIN OrganizationCalendarSession ocs
                    ON oc.OrganizationCalendarId = ocs.OrganizationCalendarId
                    AND ocs.RecordEndDateTime IS NULL
                  JOIN CourseSectionSchedule css
                    ON O.OrganizationId = css.OrganizationId
                    AND css.RecordEndDateTime IS NULL
                --GROUP BY rae.Date

                WHERE 
                  -- Verifica que se encuentre cargado el leccionario
                  rae.RefAttendanceEventTypeId = 2
                  AND
                  -- Verifica que se encuentre cargado el leccionario
                  ocs.Description NOT NULL
                  AND
                  -- Verifica que el indicador sea True, ya que en estos casos corresponde la relación	
                  ocs.AttendanceTermIndicator IN (1)
                  AND
                  -- Verifica que la firma se encuentre cargada en el sistema
                  rae.digitalRandomKey NOT NULL
                  AND
                  -- Verifica que se haya especificado si es estudiante asiste presencialmente o no.
                  rae.VirtualIndicator NOT NULL
                  AND
                  -- Verifica que día y horario de firma corresponda con calendario de la asignatura
                  css.ClassMeetingDays like '%'||diaSemana||'%'
                  AND
                  hora between css.ClassBeginningTime and css.ClassEndingTime
                  AND
                  -- Agrega a la lista todos los registros que no cumplan con la expresión regular
                  rae.Date REGEXP '^(19|2[0-9])[0-9]{2}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])([T ])(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])(.[0-9]+)?((\\+|-)(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]))$'
                  AND
                  -- Agrega a la lista todos los registros que no cumplan con la expresión regular
                  rae.digitalRandomKeyDate REGEXP '^(19|2[0-9])[0-9]{2}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])([T ])(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])(.[0-9]+)?((\\+|-)(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]))$'
                  AND
                  -- Agrega a la lista todos los registros que no cumplan con la expresión regular
                  rae.digitalRandomKey REGEXP '^[0-9]{6}([-]{1}[0-9kK]{1})?$'
                  
                GROUP BY rae.Date
            """).fetchall()
        except Exception as e:
            logger.error(f'Rechazado')
            logger.info(f'No cumple con los criterios de la consulta: {e}')
            return True
        try:
            if(len(asistencia)>0):
                totalEstudiantes = list([m[4] for m in asistencia if m[4] is not None])
                estudiantesPresentes = list([m[5] for m in asistencia if m[5] is not None])
                estudiantesAusentes = list([m[7] for m in asistencia if m[7] is not None])
                estudiantesRetrasados = list([m[9] for m in asistencia if m[9] is not None])
                firmadoEnClases = list([m[11] for m in asistencia if m[11] is not None])
                
                for idx_,el_ in enumerate(totalEstudiantes):
                  if(el_ != (estudiantesPresentes[idx_]+estudiantesAusentes[idx_]+estudiantesRetrasados[idx_])):
                    logger.info(f'Rechazado')
                    logger.info(f'Total de estudiantes NO coincide con Presentes+Ausentes+Atrasados')
                    return False    
                    
                  if(el_ != firmadoEnClases[idx_]):
                    logger.info(f'Rechazado')
                    logger.info(f'Total de estudiantes NO coincide con cantidad de firmas')
                    return False
                
            logger.info("Aprobado")    
            return True
        except Exception as e:
            logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
            logger.error(f"Rechazado")
            return False
  ## Fin fn5E0 WC ##

  ## Inicio fn8F1 WC ##
  def fn8F1(self, conn):
          try:
              query = conn.execute("""select * from Incident""").fetchall()
              if(len(query)>0):
                  Incidentes = (list([m[0] for m in query if m[0] is not None]))
                  for x in Incidentes:
                      querySelect = "SELECT * from K12StudentDiscipline where IncidentId = "
                      queryWhere = str(x)
                      queryComplete = querySelect+queryWhere
                      try:
                          query = conn.execute(queryComplete).fetchall()
                          if(len(query)>0):
                              query = len(query)
                              logger.info(f'Total de datos: {query}')
                              logger.info(f'Aprobado')
                              return True
                          else:
                              logger.error(f'S/Datos')
                              logger.error(f'No se encuentran registradas medidas diciplinarias para los incidentes registrados')
                              return False
                      except Exception as e:
                          logger.error(f'No se pudo ejecutar la consulta: {str(e)}')
                          logger.error(f'Rechazado')
                          return False
              else:
                  logger.error(f'S/Datos')
                  logger.error(f'Sin incidentes registrados')
                  return True
          except Exception as e:
            logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
            logger.error(f"Rechazado")
            return False
  ## Fin fn8F1 WC ##

  ## Inicio fn5E4 WC ##
  def fn5E4(self,conn):
      try:
          _query = conn.execute("""
          SELECT RAE.DATE,
                RAE.RefAttendanceStatusId
          FROM OrganizationPersonRole OPR
                  join RoleAttendanceEvent RAE on OPR.OrganizationPersonRoleId = RAE.OrganizationPersonRoleId
          where OPR.RoleId = 6
          and RAE.Date is not null;
          """).fetchall()
          if(len(_query)>0):
            _date = (list(set([m[0] for m in _query if m[0] is not None])))
            if not _date:
              logger.error(f"Sin fecha de asistencia ingresada")
              logger.error(f'Rechazado')
              return False
            _status = (list(set([m[1] for m in _query if m[1] is not None])))
            if not _status:
              logger.error(f"Sin estado de asistencia asignado")
              logger.error(f'Rechazado')
              return False
            logger.info(f'Aprobado')
            logger.info(f'Todos los registros de asistencia cuentan con un estado asignado')
            return True
          else:
              logger.info(f"S/Datos")
              logger.info(f"Sin datos de asistencia")
              return False
      except Exception as e:
            logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
            logger.error(f"Rechazado")
            return False
  ## Fin fn5E4 WC ##

  ## Inicio fn5E5 WC ##
  def fn5E5(self,conn):
        try:
            _query = conn.execute("""
                  SELECT 
                    count(rae_.refattendancestatusid) as 'totalEstudiantesCurso', -- Cantidad total de estudiantes [idx 0]
                    sum(CASE WHEN rae_.refattendancestatusid IN (1) THEN 1 ELSE 0 END) as 'estudiantesPresentesCurso', -- [idx 1]
                    sum(CASE WHEN rae_.refattendancestatusid IN (2,3) THEN 1 ELSE 0 END) as 'estudiantesAusentesv', -- [idx 2]
                    sum(CASE WHEN rae_.refattendancestatusid IN (4) THEN 1 ELSE 0 END) as 'estudiantesRetrasadosCurso' -- [idx 3]
                    ,a.*
                  FROM Organization O
                    JOIN RefOrganizationType rot
                      ON O.RefOrganizationTypeId = rot.RefOrganizationTypeId
                      AND O.RefOrganizationTypeId IN (
                        SELECT RefOrganizationTypeId 
                        FROM RefOrganizationType
                        WHERE Description IN ('Course')
                      ) 
                    OUTER LEFT JOIN OrganizationPersonRole opr_
                      ON O.OrganizationId = opr_.OrganizationId
                      AND opr_.RecordEndDateTime IS NULL
                    OUTER LEFT JOIN RoleAttendanceEvent rae_
                      ON opr_.OrganizationPersonRoleId = rae_.OrganizationPersonRoleId
                      AND rae_.RecordEndDateTime IS NULL
                    OUTER LEFT JOIN
                    (
                    SELECT  
                      rae.Date, -- fecha completa de la clase [idx 0]
                      ors.Parent_OrganizationID,		
                      O.OrganizationId,
                      strftime('%Y-%m-%d', rae.Date) as 'fecha', -- rescata solo la fecha desde rae.Date [idx 1]
                      CASE 
                        WHEN strftime('%w', rae.Date) = '0' THEN 'Domingo'
                        WHEN strftime('%w', rae.Date) = '1' THEN 'Lunes'
                        WHEN strftime('%w', rae.Date) = '2' THEN 'Martes'
                        WHEN strftime('%w', rae.Date) = '3' THEN 'Miercoles'
                        WHEN strftime('%w', rae.Date) = '4' THEN 'Jueves'
                        WHEN strftime('%w', rae.Date) = '5' THEN 'Viernes'
                        WHEN strftime('%w', rae.Date) = '6' THEN 'Sabado'
                      END as 'diaSemana', -- rescata solo el dpia de la semana desde rae.Date [idx 3]
                      count(refattendancestatusid) as 'totalEstudiantes', -- Cantidad total de estudiantes [idx 4]
                      sum(CASE WHEN refattendancestatusid IN (1) THEN 1 ELSE 0 END) as 'estudiantesPresentesAsignatura', -- [idx 5]
                      sum(CASE WHEN refattendancestatusid IN (2,3) THEN 1 ELSE 0 END) as 'estudiantesAusentesAsignatura', -- [idx 6]
                      sum(CASE WHEN refattendancestatusid IN (4) THEN 1 ELSE 0 END) as 'estudiantesRetrasadosAsignatura' -- [idx 7]
                      
                    FROM Organization O
                      JOIN RefOrganizationType rot
                        ON O.RefOrganizationTypeId = rot.RefOrganizationTypeId
                        AND O.RefOrganizationTypeId IN (
                          SELECT RefOrganizationTypeId 
                          FROM RefOrganizationType
                          WHERE Description IN ('Course Section')
                        ) 
                      JOIN OrganizationRelationship ors 
                        ON O.OrganizationId = ors.OrganizationId
                        AND ors.RefOrganizationRelationShipId IN (
                          SELECT RefOrganizationRelationShipId 
                          FROM RefOrganizationRelationShip
                          WHERE Code IN ('InternalOrganization')
                          ) 
                      JOIN OrganizationPersonRole opr 
                        ON O.OrganizationId = opr.OrganizationId
                        AND opr.RecordEndDateTime IS NULL
                      JOIN RoleAttendanceEvent rae
                        ON opr.OrganizationPersonRoleId = rae.OrganizationPersonRoleId
                        AND rae.RecordEndDateTime IS NULL
                      JOIN Role rol
                        ON opr.RoleId = rol.RoleId
                        AND opr.RoleId IN (
                          SELECT RoleId
                          FROM Role
                          WHERE Name IN ('Estudiante')
                        )
                      JOIN OrganizationCalendar oc 
                        ON O.OrganizationId = oc.OrganizationId
                        AND oc.RecordEndDateTime IS NULL
                      JOIN OrganizationCalendarSession ocs
                        ON oc.OrganizationCalendarId = ocs.OrganizationCalendarId
                        AND ocs.RecordEndDateTime IS NULL
                      JOIN CourseSectionSchedule css
                        ON O.OrganizationId = css.OrganizationId
                        AND css.RecordEndDateTime IS NULL
                    --GROUP BY rae.Date

                    WHERE 
                      -- Verifica que se encuentre cargado el leccionario
                      rae.RefAttendanceEventTypeId = 2
                      AND
                      -- Verifica que se encuentre cargado el leccionario
                      ocs.Description NOT NULL
                      AND
                      -- Verifica que el indicador sea True, ya que en estos casos corresponde la relación	
                      ocs.AttendanceTermIndicator IN (1)
                      AND
                      -- Verifica que la firma se encuentre cargada en el sistema
                      rae.digitalRandomKey NOT NULL
                      AND
                      -- Verifica que se haya especificado si es estudiante asiste presencialmente o no.
                      rae.VirtualIndicator NOT NULL
                      AND
                      -- Verifica que día y horario de firma corresponda con calendario de la asignatura
                      diaSemana in (css.ClassMeetingDays)
                      AND
                      -- Agrega a la lista todos los registros que no cumplan con la expresión regular
                      rae.Date REGEXP '^(19|2[0-9])[0-9]{2}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])([T ])(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])(.[0-9]+)?((\\+|-)(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]))$'
                      AND
                      -- Agrega a la lista todos los registros que no cumplan con la expresión regular
                      rae.digitalRandomKeyDate REGEXP '^(19|2[0-9])[0-9]{2}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])([T ])(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])(.[0-9]+)?((\\+|-)(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]))$'
                      AND
                      -- Agrega a la lista todos los registros que no cumplan con la expresión regular
                      rae.digitalRandomKey REGEXP '^[0-9]{6}([-]{1}[0-9kK]{1})?$'
                      AND
                      ClassPeriod in ('Bloque02')
                      
                    GROUP BY rae.Date
                    
                    ) a ON O.OrganizationId = a.Parent_OrganizationID
                  WHERE
                    -- Verifica que el tipo de asistencia sea diaria
                    rae_.RefAttendanceEventTypeId = 1
            """)#.fetchall()
            if(_query.returns_rows == 0):
              logger.info(f"Rechazado")
              logger.info(f"No hay información para evaluar")
              return False
            
            _query = _query.fetchall()
            if(len(_query)>0):
                _totalCurso = (list([m[0] for m in _query if m[0] is not None]))
                _totalAsign = (list([m[9] for m in _query if m[9] is not None]))
                
                _estPresentesCurso = (list([m[1] for m in _query if m[1] is not None]))
                _estPresentesAsign = (list([m[10] for m in _query if m[10] is not None]))
                _estAtradadosAsign = (list([m[12] for m in _query if m[12] is not None]))                

                _estAusentesCurso = (list([m[2] for m in _query if m[2] is not None]))
                _estAusentesAsign = (list([m[11] for m in _query if m[11] is not None]))
                
                for idx_,el_ in enumerate(_totalCurso):
                    if el_ != _totalAsign[idx_]:
                        logger.error(f'Rechazado')
                        logger.error(f'Totales de estudiantes no coinciden')                        

                    if _estPresentesCurso[idx_] != (_estPresentesAsign[idx_]+_estAtradadosAsign[idx_]):
                        logger.error(f'Rechazado')
                        logger.error(f'Total de estudiantes presentes no coinciden')

                    if _estAusentesCurso[idx_] != _estAusentesAsign[idx_]:
                        logger.error(f'Rechazado')
                        logger.error(f'Total de estudiantes ausentes no coinciden')

                    return False                      
        except Exception as e:
            logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
            logger.error(f"Rechazado")
            return False
  ## Fin fn5E5 WC ##

  ## Inicio fn5D0 WC ##
  def fn5D0(self, conn):
        try:
            _oPR = conn.execute("""
                SELECT DISTINCT count(RAE.Date), OPR.PersonId, RAE.Date, RAE.digitalRandomKey,RAE.VirtualIndicator
                FROM OrganizationPersonRole OPR
                        JOIN RoleAttendanceEvent RAE ON OPR.OrganizationPersonRoleId = RAE.OrganizationPersonRoleId
                WHERE OPR.RoleId in(4,5)
                AND RAE.RefAttendanceEventTypeId = 1
                group by OPR.PersonId, RAE.Date, RAE.digitalRandomKey, RAE.VirtualIndicator;
                """
                ).fetchall()
            if(len(_oPR)>0):
                _count = (list([m[0] for m in _oPR if m[0] is not None]))
                _contador = 0
                for x in _count:
                    if(x > 1):
                        _contador += 1
                if(_contador > 0):
                    logger.error('Duplicados')
                    logger.error('Rechazado')
                    return False
                else:
                    logger.info('No hay duplicados')
                    logger.info('Aprobado')
                    return True
            else:
                logger.error(f'No existen Firmas')
                logger.error(f'S/Datos')
                return False
        except Exception as e:
            logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
            logger.error(f"Rechazado")
            return False
  ## fin fn5D0 WC ##

  ## Inicio fn4FA WC ##
  def fn4FA(self, conn):
            try:
            #trae todos los datos bases del alumno y de su apoderado por curso
                idorga = conn.execute("""
                SELECT
                    organizationId,
                    name
                from Organization
                where RefOrganizationTypeId = 21
                """).fetchall()
                x=0
                for org in idorga:
                    listaAlumno = conn.execute("""
                    SELECT op.personid,
                          op.organizationpersonroleid,
                          StudentListNumber                                                                        as "numero de lista",
                          Identifier                                                                               as rut,
                          p.Birthdate                                                                              as "fecha de nacimiento",
                          k12SE.FirstEntryDateIntoUSSchool,
                          rf.Definition                                                                            as sexo,
                          pad.StreetNumberAndName                                                                  as direccion
                            ,
                          (p.FirstName || ' ' || p.MiddleName || ' ' || p.LastName || ' ' || p.SecondLastName)     as "nombre completo"
                            ,
                          (p2.FirstName || ' ' || p2.MiddleName || ' ' || p2.LastName || ' ' || p2.SecondLastName) as "apoderado",
                          pad2.StreetNumberAndName                                                                 as "domicilio Apoderado"
                            ,
                          pt2.TelephoneNumber                                                                      as "fono apoderado",
                          pea2.EmailAddress                                                                        as "email apoderado"
                            ,
                          k12SE.FirstEntryDateIntoUSSchool                                                         as "fecha de inicio"
                    FROM K12StudentEnrollment k12SE
                            JOIN OrganizationPersonRole op 
								on k12SE.OrganizationPersonRoleId = op.OrganizationPersonRoleId
								and op.RoleId IN (
									SELECT RoleId
									from Role
									WHERE role.Name IN ('Estudiante')
								)
                            JOIN PersonIdentifier PI 
								on op.PersonId = PI.PersonId
								  and PI.RefPersonIdentificationSystemId IN (
									Select RefPersonIdentificationSystemId
									from RefPersonIdentificationSystem rpi
									where rpi.Description IN ('ROL UNICO NACIONAL')
								  )
							JOIN Person p on op.PersonId = p.PersonId
                            JOIN RefSex rf on p.RefSexId = rf.RefSexId
                            LEFT join PersonAddress pad on p.PersonId = pad.PersonId
                            JOIN PersonRelationship pr 
                              on p.PersonId = pr.RelatedPersonId
                              and pr.RefPersonRelationshipId IN (
                                Select RefPersonRelationshipId
                                from RefPersonRelationship
                                where RefPersonRelationship.Description IN ('Apoderado(a)/Tutor(a)')
                              )
                            LEFT join Person p2 on p2.PersonId = pr.PersonId -- Datos Apoderado
                            LEFT join PersonAddress pad2 on pad2.PersonId = p2.PersonId  -- Datos Apoderado
                            LEFT join PersonTelephone pt2 on pt2.PersonId = p2.PersonId  -- Datos Apoderado
                            LEFT join PersonEmailAddress pea2 on pea2.PersonId = p2.PersonId  -- Datos Apoderado
                    WHERE
                      op.organizationid = ?
                    GROUP by op.PersonId;
                    """,([org[0]])).fetchall()
                    if(len(listaAlumno)> 0):
                        x=x+1
                        for alumno in listaAlumno:
                            #por cada alumno trae a los profesorees que interactuan con el
                            idAlumno=alumno[0]
                            idAlumnorole=alumno[1]
                            listaProfesionales = conn.execute("""
                            SELECT (p.FirstName || ' ' || p.MiddleName || ' ' || p.LastName || ' ' || p.SecondLastName) as "nombre completo"
                            FROM OrganizationPersonRole op
                                    join OrganizationPersonRole op2 on op.OrganizationId = op2.OrganizationId
                                    join Person p on op.PersonId = p.PersonId
                            WHERE op.roleid != 6
                              AND op2.PersonId = ?
                              AND op2.OrganizationID = ?
                            GROUP by op.PersonId
                            """,(idAlumno,org[0])).fetchall()
                            #lista de becas e identificacion de estudiante preferente, prioritario, etc de ser requerido
                            listaPrograma = conn.execute("""
                            SELECT rpt.description
                            FROM RefParticipationType rpt
                                    join PersonProgramParticipation ppp on rpt.RefParticipationTypeId = ppp.RefParticipationTypeId
                            WHERE ppp.OrganizationPersonRoleId = ?;
                            """,([idAlumnorole])).fetchall()
                            #trae las asignaturas en las que se encuentra el alumno
                            organizacion = conn.execute("""
                            SELECT op.OrganizationId, personid
                            FROM OrganizationPersonRole op
                                    join Organization o on op.OrganizationId = o.OrganizationId
                            WHERE personid in (?);""",([idAlumno])).fetchall()
                            organi=[]
                            evalua_=[]
                            for org2 in organizacion:
                                #por cada asignatura trae el calendario
                                calendario = conn.execute("""
                                SELECT
                                    BeginDate,
                                    EndDate,
                                    SessionStartTime,
                                    SessionEndTime
                                FROM calendarList
                                WHERE OrganizationId = ?
                                and "RefSessionType.Description" like '%Semester%';
                                    """,([org2[0]])).fetchall()
                                if(calendario):
                                    organi.append(calendario)
                                # por cada asignatura trae las evaluaciones
                                evaluaciones = conn.execute("""
                                select aao.OrganizationId
                                from AssessmentAdministration_Organization aao
                                join CourseSection cs on aao.OrganizationId=cs.OrganizationId
                                where CourseId= ?;
                                """,([org2[0]])).fetchall()
                                if (evaluaciones):
                                    evalua_.append(evaluaciones)
                        becasprogramas=(list([m[0] for m in listaPrograma if m[0] is not None]))
                        evalua=(list([m[0] for m in evalua_ if m[0] is not None]))
                        profe=(list([m[0] for m in listaProfesionales if m[0] is not None]))
                        calenda=(list([m[0] for m in organi if m[0] is not None]))
                        print(profe)
                        if not profe:
                            logger.error(f"Sin profesor jefe, o profesor de asignaturas")
                            logger.error(f"Rechazado")
                            return False
                        elif not calenda:
                            logger.error(f"Sin calendario")
                            logger.error(f"Rechazado")
                            return False
                        elif not evalua:
                            logger.error(f"Sin evaluaciones")
                            logger.error(f"Rechazado")
                            return False
                    else:
                        logger.error(f"Sin Datos de alumnos: {org}")
                if x==0:
                  logger.info(f"S/Datos")
                  return False
                logger.info("Se validaron todos los datos")
                logger.info(f"Aprobado")
                return True
            except Exception as e:
                logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
                logger.error(f"Rechazado")
                return False
  ## Fin fn4FA WC ##

  ## Inicio fn5F0 WC ##
  def fn5F0(self, conn):
        try:
          asignaturas = []
          asignaturas = conn.execute("""
--6.2 Contenido mínimo, letra b.1
--Validar la información relacionada con el cumplimiento de los programas de estudio y asistencia de los estudiantes.
-- * día de clases
-- * mes respectivo
-- * hora pedagógica
-- * nombre de la asignatura o sector
-- * total de estudiantes presentes, atrasados y ausentes
-- * observaciones de la clase
-- * Verificador de identidad del docente a cargo

-- Lee desde las organizaciones de tipo asignatura los campos 
-- FirstInstructionDate y LastInstructionDate y con esa información
-- crea una lista de días hábiles en los cuales deberían haber tenido clases
-- los estudiantes del establecimiento.
WITH RECURSIVE dates(Organizationid, date) AS (
  SELECT O.Organizationid, FirstInstructionDate
  --FROM OrganizationCalendarSession ocs
  FROM Organization O
  JOIN RefOrganizationType rot
	ON O.RefOrganizationTypeId = rot.RefOrganizationTypeId
	AND O.RefOrganizationTypeId IN (
	  SELECT RefOrganizationTypeId 
	  FROM RefOrganizationType
	  WHERE Description IN ('Course Section')
	) 
  JOIN OrganizationCalendar oc
	--ON oc.OrganizationCalendarId = ocs.OrganizationCalendarId
	ON oc.OrganizationId = O.Organizationid--'2000096080'
  JOIN OrganizationCalendarSession ocs
	ON oc.OrganizationCalendarId = ocs.OrganizationCalendarId
	AND ocs.FirstInstructionDate NOT NULL
  UNION ALL
  SELECT Organizationid, date(date, '+1 day')
  FROM dates
  WHERE 
	-- Considera la menor fecha entre LastInstructionDate y la fecha actual (now)
	strftime('%Y-%m-%d',date) < strftime('%Y-%m-%d', ( 
		-- Rescata el último día 
		SELECT LastInstructionDate 
		FROM OrganizationCalendarSession ocs 
		JOIN OrganizationCalendar oc 
			ON oc.OrganizationCalendarId = ocs.OrganizationCalendarId 
			AND oc.OrganizationId = Organizationid-- '2000096080'
		WHERE ocs.LastInstructionDate NOT NULL
		)
	) 
	AND
	strftime('%Y-%m-%d',date) < strftime('%Y-%m-%d','now')
)
SELECT Organizationid, date, result.*
FROM dates 
-- con el OrganizationId se hace un cruce con la consulta que calcula los datos a validar
LEFT JOIN (
	-- Esta consulta rescata desde la RoleAttendanceEvent los días con asistencia y calcula 
	-- el total de estudiantes presentes, ausentes y atrasados.
	-- Además revisa si exiten las firmas del docente en cada registro y si esta cargada la 
	-- información del leccionario
	SELECT 
		O.OrganizationId as 'idAsignatura', -- [idx 0]
		O.name as 'nombreAsignatura', -- [idx 1]
		rae.Date as 'fechaClase', -- fecha completa de la clase [idx 2]
		strftime('%Y-%m-%d', rae.Date) as 'fecha', -- rescata solo la fecha desde rae.Date [idx 3]
		CASE 
			WHEN strftime('%w', rae.Date) = '0' THEN 'Domingo'
			WHEN strftime('%w', rae.Date) = '1' THEN 'Lunes'
			WHEN strftime('%w', rae.Date) = '2' THEN 'Martes'
			WHEN strftime('%w', rae.Date) = '3' THEN 'Miercoles'
			WHEN strftime('%w', rae.Date) = '4' THEN 'Jueves'
			WHEN strftime('%w', rae.Date) = '5' THEN 'Viernes'
			WHEN strftime('%w', rae.Date) = '6' THEN 'Sabado'
		END as 'diaSemana', -- rescata solo el dpia de la semana desde rae.Date [idx 4]	
		CASE 
			WHEN strftime('%m', rae.Date) = '1' THEN 'Enero'
			WHEN strftime('%m', rae.Date) = '2' THEN 'Febrero'
			WHEN strftime('%m', rae.Date) = '3' THEN 'Marzo'
			WHEN strftime('%m', rae.Date) = '4' THEN 'Abril'
			WHEN strftime('%m', rae.Date) = '5' THEN 'Mayo'
			WHEN strftime('%m', rae.Date) = '6' THEN 'Junio'
			WHEN strftime('%m', rae.Date) = '7' THEN 'Julio'
			WHEN strftime('%m', rae.Date) = '8' THEN 'Agosto'
			WHEN strftime('%m', rae.Date) = '9' THEN 'Septiembre'
			WHEN strftime('%m', rae.Date) = '10' THEN 'Octubre'
			WHEN strftime('%m', rae.Date) = '11' THEN 'Noviembre'
			WHEN strftime('%m', rae.Date) = '12' THEN 'Diciembre'		
		END as 'Mes', -- rescata solo el mes desde rae.Date [idx 5]
		strftime('%H:%M', rae.Date, substr(rae.Date,length(rae.Date)-5,6)) as 'hora', -- rescata solo la hora desde rae.Date [idx 6]
		count(refattendancestatusid) as 'totalEstudiantes', -- Cantidad total de estudiantes [idx 7]
		sum(CASE WHEN refattendancestatusid IN (1) THEN 1 ELSE 0 END) as 'estudiantesPresentes', -- [idx 8]
		group_concat(CASE WHEN refattendancestatusid IN (1) THEN Identifier END) as 'estudiantesPresentesNumLista', -- [idx 9]
		sum(CASE WHEN refattendancestatusid IN (2,3) THEN 1 ELSE 0 END) as 'estudiantesAusentes', -- [idx 10]
		group_concat(CASE WHEN refattendancestatusid IN (2,3) THEN Identifier END) as 'estudiantesAusentesNumLista', -- [idx 11]
		sum(CASE WHEN refattendancestatusid IN (4) THEN 1 ELSE 0 END) as 'estudiantesRetrasados', -- [idx 12]
		group_concat(CASE WHEN refattendancestatusid IN (4) THEN Identifier END) as 'estudiantesRetrasadosNumLista', -- [idx 13]
		count(rae.digitalRandomKey) as 'cantidadRegistrosFirmados', -- [idx 14]
		group_concat(DISTINCT '"' || ocs.description || '"') as 'observacionesLeccionario' -- [idx 15]
	FROM Organization O
		JOIN RefOrganizationType rot
			ON O.RefOrganizationTypeId = rot.RefOrganizationTypeId
			AND O.RefOrganizationTypeId IN (
				SELECT RefOrganizationTypeId 
				FROM RefOrganizationType
				WHERE Description IN ('Course Section')
			) 
		JOIN OrganizationPersonRole opr 
			ON O.OrganizationId = opr.OrganizationId
			AND opr.RecordEndDateTime IS NULL
		JOIN RoleAttendanceEvent rae
			ON opr.OrganizationPersonRoleId = rae.OrganizationPersonRoleId
			AND rae.RecordEndDateTime IS NULL
		JOIN PersonIdentifier pid
			ON opr.personId = pid.personId
			AND pid.refPersonIdentificationSystemId IN (
				SELECT refPersonIdentificationSystemId
				FROM refPersonIdentificationSystem
				WHERE Code IN ('listNumber')
			)
			AND pid.RecordEndDateTime IS NULL
		JOIN Role rol
			ON opr.RoleId = rol.RoleId
			AND opr.RoleId IN (
				SELECT RoleId
				FROM Role
				WHERE Name IN ('Estudiante')
			)
		JOIN OrganizationCalendar oc 
			ON O.OrganizationId = oc.OrganizationId
			AND oc.RecordEndDateTime IS NULL
		JOIN OrganizationCalendarSession ocs
			ON oc.OrganizationCalendarId = ocs.OrganizationCalendarId
			AND ocs.RecordEndDateTime IS NULL
		JOIN CourseSectionSchedule css
			ON O.OrganizationId = css.OrganizationId
			AND css.RecordEndDateTime IS NULL
	--GROUP BY rae.Date

	WHERE 
		-- Verifica que se encuentre cargado el leccionario
		rae.RefAttendanceEventTypeId = 2
		AND
		-- Verifica que se encuentre cargado el leccionario
		ocs.Description NOT NULL
		AND
		-- Verifica que el indicador sea True, ya que en estos casos corresponde la relación	
		ocs.AttendanceTermIndicator IN (1)
		AND
		-- Verifica que la firma se encuentre cargada en el sistema
		rae.digitalRandomKey NOT NULL
		AND
		-- Verifica que se haya especificado si es estudiante asiste presencialmente o no.
		rae.VirtualIndicator NOT NULL
		AND
		-- Verifica que día y horario de firma corresponda con calendario de la asignatura
		diaSemana in (css.ClassMeetingDays)
		AND
		hora between css.ClassBeginningTime and css.ClassEndingTime
		AND
		-- Agrega a la lista todos los registros que no cumplan con la expresión regular
		rae.Date REGEXP '^(19|2[0-9])[0-9]{2}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])([T ])(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])(.[0-9]+)?((\\+|-)(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]))$'
		AND
		-- Agrega a la lista todos los registros que no cumplan con la expresión regular
		rae.digitalRandomKeyDate REGEXP '^(19|2[0-9])[0-9]{2}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])([T ])(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])(.[0-9]+)?((\\+|-)(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]))$'
		AND
		-- Agrega a la lista todos los registros que no cumplan con la expresión regular
		rae.digitalRandomKey REGEXP '^[0-9]{6}([-]{1}[0-9kK]{1})?$'
	GROUP BY rae.Date
) result 
	ON result.idAsignatura = OrganizationId
	AND result.fecha = date
-- Rescata las fechas desde OrganizationCalendarCrisis y las saca de la lista de días hábiles
JOIN (
			WITH RECURSIVE dates(Organizationid, date) AS (
			  SELECT Organizationid, StartDate
			  FROM OrganizationCalendarCrisis O
			  UNION ALL
			  SELECT Organizationid, date(date, '+1 day')
			  FROM dates
			  WHERE 
				-- Considera la menor fecha entre LastInstructionDate y la fecha actual (now)
				strftime('%Y-%m-%d',date) < strftime('%Y-%m-%d', ( 
					-- Rescata el último día 
					SELECT EndDate 
					FROM OrganizationCalendarCrisis occ
					WHERE occ.OrganizationId = Organizationid
					)
				) 
			)
			SELECT Organizationid as 'org',  group_concat(date) as 'fechasCrisis'
			FROM dates 		
) occ 
	ON occ.org = Organizationid
	AND (occ.fechasCrisis) NOT LIKE "%" || date || "%"
-- Rescata las fechas desde OrganizationCalendarEvent y las saca de la lista de días hábiles
JOIN (
	SELECT oc.Organizationid as 'org', group_concat(oce.EventDate) as 'fechasEventos'
	FROM OrganizationCalendarEvent oce
	JOIN OrganizationCalendar oc
		ON oce.OrganizationCalendarId = oc.OrganizationCalendarId
	JOIN RefCalendarEventType rcet
		ON oce.RefCalendarEventType = rcet.RefCalendarEventTypeId
		AND rcet.Code IN ('EmergencyDay','Holiday','Strike','TeacherOnlyDay')	
	GROUP BY oc.Organizationid
) oce 
	ON oce.org = Organizationid
	AND (oce.fechasEventos) NOT LIKE "%" || date || "%"	 
WHERE 
	CAST(strftime('%w',date) as INTEGER) between 1 and 5
	--AND result.idAsignatura NOT NULl
GROUP BY Organizationid, date
""").fetchall()
        except:
          logger.info(f"Ocurrió un error el la consulta")

        try:
          if(not asignaturas):
            logger.info(f"S/Datos")
            logger.info(f'No hay información disponible para validar. Su registro es obligatorio.')
            logger.info(f'Si hay información en la BD, revise si esta cumpliendo con los criterios de la consulta.')
            return False 
          
          #define listas de errores
          workDayWithoutInfo = []
          courseSectionNameErrors = []
          totalStudentsErrors = []
          tokenRegisteredErrors = []
          descriptionClassErrors = []
          
          for asignaturaRow in asignaturas:
            #define variables a comparar
            organizationId = asignaturaRow[0]
            workDay = asignaturaRow[1]
            CourseSectionId = asignaturaRow[2]
            courseSectionName = asignaturaRow[3]
            totalStudents = asignaturaRow[9]
            presentStudents = asignaturaRow[10]
            ausentStudents = asignaturaRow[12]
            Latestudent = asignaturaRow[14]
            tokenRegistered = asignaturaRow[16]
            descriptionClass = asignaturaRow[17]
            
            #Comienza a validar los datos
            if(not CourseSectionId): 
              #se encontraron días hábiles del calendatio sin información registrada
              workDayWithoutInfo.append(workDay)

            else: #Valida solo si existe información en la fecha
              if(not courseSectionName):
                #Se encontraron asignaturas sin ningún nombre registrado
                courseSectionNameErrors.append(organizationId)

              if(totalStudents != (presentStudents+ausentStudents+Latestudent)):
                #La cantidad total de estudiantes no coincide con la suma de estudiantes presentes+ausentes+atradados.
                totalStudentsErrors.append(organizationId)
                
              if(tokenRegistered != totalStudents):
                #La cantidad de firmas registradas no coinciden con el número total de estudiantes
                tokenRegisteredErrors.append(organizationId)
                
              if(not descriptionClass):
                #La clase registrada en el día X, no contiene descripción de los temas trabajados (Leccionario)
                descriptionClassErrors.append(organizationId)
                
          if(workDayWithoutInfo or courseSectionNameErrors or totalStudentsErrors or tokenRegisteredErrors or descriptionClassErrors): 
            if(workDayWithoutInfo): logger.error(f'Se encontraron días hábiles del calendatio sin información registrada: {workDayWithoutInfo}')
            if(courseSectionNameErrors): logger.error(f'Se encontraron asignaturas sin ningún nombre registrado: {courseSectionNameErrors}')
            if(totalStudentsErrors): logger.error(f'La cantidad total de estudiantes no coincide con la suma de estudiantes presentes+ausentes+atradados en las siguientes asignaturas: {totalStudentsErrors}')
            if(tokenRegisteredErrors): logger.error(f'La cantidad de firmas registradas no coinciden con el número total de estudiantes en las siguientes asignaturas: {tokenRegisteredErrors}')
            if(descriptionClassErrors): logger.error(f'La clase registrada en el día X, no contiene descripción de los temas trabajados (Leccionario). {descriptionClassErrors}')
            return False
          else:
            logger.info(f'Validacion aprobada')
            logger.info(f'Aprobado')
            return True
        except Exception as e:
          logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
          logger.error(f"Rechazado")
          return False
  ## Fin fn5F0 WC ##

  ## Inicio fn8F3 WC ##
  def fn8F3(self, conn):
        try:
          queryTwo = conn.execute("""
          SELECT K12StudentDisciplineId,
                OrganizationPersonRoleId,
                DisciplinaryActionStartDate,
                IncidentId
          FROM K12StudentDiscipline
          WHERE RefDisciplinaryActionTakenId = 8;
          """).fetchall()
          if(len(queryTwo)>0):
              for fila in queryTwo:
                  for dato in fila:
                      if dato is None:
                          a = 0
                      else:
                          logger.error(f'Datos incompletos')
                          logger.error(f'Rechazado')
                          return False
          else:
              logger.error(f'S/Datos')
              logger.error(f'Sin reuniones con los apoderado/s')
              return True
          logger.info(f'Datos Validados')
          logger.info(f'Aprobado')
          return True
        except Exception as e:
            logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
            logger.error(f"Rechazado")
            return False
  ## Fin fn8F3 WC ##

  ## Inicio fn8F2 WC ##
  def fn8F2(self,conn):
        try:
            _queryIncident = conn.execute("""
            SELECT DISTINCT
                I.IncidentId,
                I.IncidentDate,
                I.IncidentTime,
                I.RefIncidentTimeDescriptionCodeId,
                I.IncidentDescription,
                I.OrganizationPersonRoleId,
                OPR.RoleId
                FROM Incident I
                JOIN OrganizationPersonRole OPR on I.OrganizationPersonRoleId = OPR.OrganizationPersonRoleId
                WHERE OPR.RoleId = 6;
                """).fetchall()
            if(len(_queryIncident)>0):
                _incidentId = (list([m[0] for m in _queryIncident if m[0] is not None]))
                if not _incidentId:
                    logger.error(f"Sin Incidentes")
                    logger.error(f'Rechazado')
                    return False
                _incidentDate = (list([m[1] for m in _queryIncident if m[1] is not None]))
                if not _incidentDate:
                    logger.error(f"Sin Fecha registrada para los incidentes")
                    logger.error(f'Rechazado')
                    return False
                _incidentTime = (list([m[2] for m in _queryIncident if m[2] is not None]))
                if not _incidentTime:
                    logger.error(f"Sin Time registrada para los incidentes")
                    logger.error(f'Rechazado')
                    return False
                _incidentTimeDescriptionCodeId = (list([m[3] for m in _queryIncident if m[3] is not None]))
                if not _incidentTimeDescriptionCodeId:
                    logger.error(f"Sin time code en el incidente")
                    logger.error(f'Rechazado')
                    return False
                _incidentDescription = (list([m[4] for m in _queryIncident if m[4] is not None]))
                if not _incidentDescription:
                    logger.error(f"Sin descripcion para el incidente")
                    logger.error(f'Rechazado')
                    return False
                _organizationPersonRoleId = (list([m[5] for m in _queryIncident if m[5] is not None]))
                if not _organizationPersonRoleId:
                    logger.error(f"Sin estudiante en incidente")
                    logger.error(f'Rechazado')
                    return False
                _roleId = (list([m[6] for m in _queryIncident if m[6] is not None]))
                if _roleId[0] != 6:
                    logger.error(f"Sin estudiante en incidente")
                    logger.error(f'Rechazado')
                    return False
                for x in _incidentId:

                    _queryIncidentPerson = conn.execute("""
                    SELECT DISTINCT
                    I.IncidentId,
                    I.PersonId,
                    I.RefIncidentPersonRoleTypeId,
                    OPR.RoleId
                    FROM IncidentPerson I
                            JOIN Person P on I.PersonId = P.PersonId
                            JOIN OrganizationPersonRole OPR on P.PersonId = OPR.PersonId
                    WHERE I.IncidentId =?
                    """,x ).fetchall()
                    if (len(_queryIncidentPerson)>0):
                        _personId = (list([m[1] for m in _queryIncidentPerson if m[1] is not None]))
                        _refRoleType = (list([m[2] for m in _queryIncidentPerson if m[2] is not None]))
                        _role = (list([m[3] for m in _queryIncidentPerson if m[3] is not None]))
                        if not _personId:
                            logger.error(f"Sin personas registradas para el incidente")
                            logger.error(f'Rechazado')
                            return False
                        _profe = 0 #4,5
                        _apoderado = 0 #15
                        _entrevistado = 0  #5
                        _entrevistador = 0 #6
                        for y in _refRoleType:
                            for z in _role:
                                if y == 5:
                                    _entrevistado += 1
                                if y == 6:
                                    _entrevistador += 1
                                if z == 4 or z == 5:
                                    _profe += 1
                                if z == 15:
                                    _apoderado += 1
                        if _entrevistado == 0:
                            logger.error(f'Sin entrevistado en reunion de incidente')
                            logger.error(f'Rechazado')
                            return False
                        if _entrevistador == 0:
                            logger.error(f'Sin entrevistador en reunion de incidente')
                            logger.error(f'Rechazado')
                            return False
                        if _profe == 0:
                            logger.error(f'Sin profesor asignado a incidente')
                            logger.error(f'Rechazado')
                            return False
                        if _apoderado == 0:
                            logger.error(f'Sin apoderado en incidente')
                            logger.error(f'Rechazado')
                            return False
                    else:
                        logger.error(f"Sin personas registradas para el incidente")
                        logger.error(f"Rechazado")
                        return False
                logger.info(f'Incidentes validados')
                logger.info(f'Aprobado')
                return True
            else:
                logger.error(f"S/Datos ")
                logger.error(f"Sin incidentes registrados")
                return True
        except Exception as e:
            logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
            logger.error(f"Rechazado")
            return False
  ## Fin fn8F2 WC ##

  ## Inicio fn2AA WC ##
  def fn2AA(self, conn):
        try:
            results = conn.execute("""
            SELECT p.personId
            FROM Person p
                    JOIN PersonStatus ps on p.PersonId = ps.PersonId
            WHERE p.RefVisaTypeId = 6
              AND ps.StatusValue = 1
              AND ps.RefPersonStatusTypeId = 25;
            """).fetchall()

            resultsTwo = conn.execute("""
            SELECT p.personId
            FROM Person p
                    JOIN PersonStatus ps on p.PersonId = ps.PersonId
            WHERE p.RefVisaTypeId = 6
              and ps.RefPersonStatusTypeId = 25;
            """).fetchall()

            if(len(results)>0 and len(resultsTwo)>0):
                lista = list(set([m[0] for m in results if m[0] is not None]))
                listaDos = list(set([m[0] for m in resultsTwo if m[0] is not None]))

                if lista == listaDos:
                    logger.info(f"todos los alumnos de intercambios fueron aprobados")
                    logger.info(f"Aprobado")
                    return True
                else :
                    logger.error(f'No todos los alumnos de intercambio han sido aprobados')
                    logger.error(f'Rechazado')
                    return False
            else:
                logger.info(f"S/Datos")
                logger.info(f"No hay alumnos de intercambio registrados en el establecimiento")
                return True

        except Exception as e:
            logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
            logger.error(f"Rechazado")
            return False
  ## Fin fn2AA WC ##

  ## Inicio fn28A WC ##
  def fn28A(self, conn):
            try:
                _query = conn.execute("""
                SELECT DISTINCT P.PersonId
                FROM OrganizationPersonRole OPR
                        JOIN Person P on OPR.PersonId = P.PersonId
                        JOIN PersonIdentifier PI on P.PersonId = PI.PersonId
                where PI.RefPersonIdentificationSystemId = 52
                  and OPR.RoleId = 6
                  and PI.Identifier is not null;
                """).fetchall()
                if(len(_query)>0):
                  _personStatus = conn.execute("""
                  SELECT fileScanBase64
                  FROM PersonStatus
                  WHERE PersonId in (SELECT DISTINCT P.PersonId
                                    FROM OrganizationPersonRole OPR
                                              join Person P on OPR.PersonId = P.PersonId
                                              join PersonIdentifier PI on P.PersonId = PI.PersonId
                                    WHERE PI.RefPersonIdentificationSystemId = 52
                                      and OPR.RoleId = 6
                                      and PI.Identifier is not null)
                    and RefPersonStatusTypeId = 34
                    and fileScanBase64 is not null;
                  """).fetchall()
                  if(len(_personStatus) == len(_query)):
                    _file = conn.execute("""
                    SELECT
                          documentId
                    FROM Document
                    WHERE fileScanBase64 IS NOT NULL
                      AND fileScanBase64 <> ''
                      AND documentId in (
                        select fileScanBase64
                        from PersonStatus
                        where PersonId in (select DISTINCT P.PersonId
                                          from OrganizationPersonRole OPR
                                                    join Person P on OPR.PersonId = P.PersonId
                                                    join PersonIdentifier PI on P.PersonId = PI.PersonId
                                          where PI.RefPersonIdentificationSystemId = 52
                                            and OPR.RoleId = 6
                                            and PI.Identifier is not null)
                          and RefPersonStatusTypeId = 34
                          and fileScanBase64 is not null);
                    """).fetchall()
                    if(len(_query) == len(_file)):
                      logger.info(f'Todos los alumnos extranjeros poseen documento de convalidacion de estudios')
                      logger.info(f'Aprobado')
                      return True
                    else:
                      logger.error(f'Existen documentos de convalidacion de ramos incompletos')
                      logger.error(f'Rechazado')
                      return False
                  else:
                    logger.error(f'No todos los alumnos extranjeros no poseen documento de convalidacion de estudios')
                    logger.error(f'Rechazado')
                    return False
                else:
                    logger.info(f"S/Datos")
                    logger.info(f"No existen estudiantes migrantes registrados en el establecimiento")
                    return True
            except Exception as e:
                logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
                logger.error(f"Rechazado")
                return False
  ## Fin fn28A WC ##

  ## Inicio fn5E1 WC ##
  def fn5E1(self,conn):
        try:
            _query = conn.execute("""
            SELECT OPR.OrganizationPersonRoleId,
                (SELECT count(OPR.PersonId)
                    from OrganizationPersonRole OPR
                            join Organization O on OPR.OrganizationId = O.OrganizationId
                            join Course C on O.OrganizationId = C.OrganizationId
                    where OPR.RoleId = 6
                    and O.RefOrganizationTypeId = 21) as MatriculasTotales
            FROM OrganizationPersonRole OPR
                    join Organization O on OPR.OrganizationId = O.OrganizationId
                    join Course C on O.OrganizationId = C.OrganizationId
            WHERE OPR.RoleId = 6
            AND O.RefOrganizationTypeId = 21
            GROUP by OPR.OrganizationPersonRoleId;
            """).fetchall()
            if(len(_query)>0):
                _alumnos = (list([m[0] for m in _query if m[0] is not None]))
                if not _alumnos :
                    logger.error(f"Sin alumnos registrados")
                    logger.error(f'Rechazado')
                    return False
                _matriculasTotales = (list([m[1] for m in _query if m[1] is not None]))
                if not _matriculasTotales :
                    logger.error(f"Sin matriculas registradas")
                    logger.error(f'Rechazado')
                    return False
                _totalAlumnos = int(len(_alumnos))
                if int(_matriculasTotales[0]) == _totalAlumnos:
                        _queryRegistroAsistencia = conn.execute("""
                        SELECT DISTINCT RoleAttendanceEventId,
                                        Date,
                                        RefAttendanceEventTypeId
                        FROM RoleAttendanceEvent
                        WHERE RefAttendanceEventTypeId = 1 and Date is not null
                        GROUP by date;
                        """).fetchall()
                        if(len(_queryRegistroAsistencia)>0):
                            logger.info(f'Matriculas registradas y asistencia diaria realizada')
                            logger.info(f'Aprobado')
                            return True
                        else:
                            logger.error(f'Asistencia diaria no realizada por el establecimiento')
                            logger.error(f'Rechazado')
                            return False
                else:
                    logger.error(f"Sin matriculas no coinciden con total de alumnos registrados")
                    logger.error(f'Rechazado')
                    return False
            else:
                logger.error(f'S/Datos')
                logger.error(f'No existen alumnos matriculados en el establecimiento')
                return False
        except Exception as e:
            logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
            logger.error(f"Rechazado")
            return False
  ## Fin fn531 WC ##

  ## Inicio fn28B WC ##
  def fn28B(self, conn):
        try:
            _query = conn.execute("""
            SELECT DISTINCT PI.PersonId
            FROM OrganizationPersonRole OPR
                    join Person P on OPR.PersonId = P.PersonId
                    join PersonIdentifier PI on P.PersonId = PI.PersonId
            WHERE PI.RefPersonIdentificationSystemId = 52
              AND OPR.RoleId = 6
              AND PI.Identifier is not null;
            """).fetchall()
            if(len(_query)>0):
              _queryDocuments = conn.execute("""
              SELECT PS.fileScanBase64
              FROM PersonStatus PS
              WHERE PS.PersonId in (select DISTINCT PI.PersonId
                                    from OrganizationPersonRole OPR
                                            join Person P on OPR.PersonId = P.PersonId
                                            join PersonIdentifier PI on P.PersonId = PI.PersonId
                                    where PI.RefPersonIdentificationSystemId = 52
                                      and OPR.RoleId = 6
                                      and PI.Identifier is not null)
                AND PS.docNumber IS NOT NULL
                AND PS.docNumber <> ''
                AND PS.Description IS NOT NULL
                AND PS.Description <> ''
                and PS.fileScanBase64 is not null
                and PS.RefPersonStatusTypeId = 34
              """).fetchall()
              if (len(_queryDocuments) == len(_query)):
                _file = conn.execute("""
                SELECT documentId
                FROM Document
                WHERE fileScanBase64 IS NOT NULL
                  AND fileScanBase64 <> ''
                  AND documentId in (SELECT PS.fileScanBase64
                                    FROM PersonStatus PS
                                    WHERE PS.PersonId in (select DISTINCT PI.PersonId
                                                          from OrganizationPersonRole OPR
                                                                    join Person P on OPR.PersonId = P.PersonId
                                                                    join PersonIdentifier PI on P.PersonId = PI.PersonId
                                                          where PI.RefPersonIdentificationSystemId = 52
                                                            and OPR.RoleId = 6
                                                            and PI.Identifier is not null)
                                      AND PS.docNumber IS NOT NULL
                                      AND PS.docNumber <> ''
                                      AND PS.Description IS NOT NULL
                                      AND PS.Description <> ''
                                      and PS.fileScanBase64 is not null
                                      and PS.RefPersonStatusTypeId = 34);
                """).fetchall()
                if(len(_file) == len(_query)):
                  logger.info(f'Todos los estudiantes migrantes cuentan con sus documentos de convalidacion de ramos completos')
                  logger.info(f'Aprobado')
                  return True
                else:
                  logger.error(f'Existen alumnos migrantes con documentos de convalidacion de ramos incompletos')
                  logger.error(f'Rechazado')
                  return False
              else:
                logger.error(f'Existen alumnos migrantes con documentos de convalidacion de ramos incompletos')
                logger.error(f'Rechazado')
                return False
            else:
                logger.info(f"No existen estudiantes migrantes registrados en el establecimiento")
                logger.info(f"S/Datos")
                return True
        except Exception as e:
            logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
            logger.error(f"Rechazado")
            return False
  ## Fin fn28B WC ##

  ## Inicio fn9F2 WC ##
  def fn9F2(self, conn):
        try:
            queryEstudiantes = conn.execute("""
                SELECT DISTINCT o.OrganizationId, o.Name
                FROM Person p
                        join OrganizationPersonRole opr
                              on p.PersonId = opr.PersonId
                        join Organization O on opr.OrganizationId = O.OrganizationId
                WHERE opr.RoleId = 6
                  AND O.RefOrganizationTypeId = 21;
                  """).fetchall()

            if (len(queryEstudiantes)>0):
                organizations = (list([m[0] for m in queryEstudiantes if m[0] is not None]))
                organizations = str(organizations)
                organizations = organizations.replace('[','(')
                organizations = organizations.replace(']',')')
                querySelect = "select CourseId from CourseSection where CourseId in"
                queryComplete = querySelect+organizations
                try:
                    queryAsignaturas = conn.execute(queryComplete).fetchall()
                    if (len(queryAsignaturas)>0):
                        cursos = (list([m[0] for m in queryAsignaturas if m[0] is not None]))
                        cursos = str(cursos)
                        cursos = cursos.replace('[','(')
                        cursos = cursos.replace(']',')')
                        querySelectCalendar = "select * from OrganizationCalendar where OrganizationId in"
                        queryCalendarComplete = querySelectCalendar+cursos
                        try:
                            queryCalendarios = conn.execute(queryCalendarComplete).fetchall()
                            if (len(queryCalendarios)>0):
                                organizationId = (list([m[1] for m in queryCalendarios if m[0] is not None]))
                                calendarCode = (list([m[2] for m in queryCalendarios if m[0] is not None]))
                                calendarDescripction = (list([m[3] for m in queryCalendarios if m[0] is not None]))
                                calendarYear = (list([m[4] for m in queryCalendarios if m[0] is not None]))

                                if not organizationId :
                                    logger.error(f"Sin OrganizationId")
                                    logger.error(f'Rechazado')
                                    return False
                                if not calendarCode :
                                    logger.error(f"Sin CalendarCode")
                                    logger.error(f'Rechazado')
                                    return False
                                if not calendarDescripction :
                                    logger.error(f"Sin CaldendarDescription")
                                    logger.error(f'Rechazado')
                                    return False
                                if not calendarYear :
                                    logger.error(f"Sin CalendarYear")
                                    logger.error(f'Rechazado')
                                    return False
                                logger.info(f'Calendarios ingresados correctamente')
                                logger.info(f'Aprobado')
                                return True
                            else:
                                logger.info(f"S/Datos")
                                logger.info(f"Rechazado")
                                return False
                        except Exception as e:
                            logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
                            logger.error(f"Rechazado")
                            return False
                    else:
                        logger.info(f"S/Datos")
                        logger.info(f"Rechazado")
                        return False
                except Exception as e:
                    logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
                    logger.error(f"Rechazado")
                    return False
            else:
                logger.info(f"S/Datos")
                logger.info(f"Sin datos del registro de implementacion y evaluacion del proceso formativo")
                return False
        except Exception as e:
            logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
            logger.error(f"Rechazado")
            return False
  ## Fin fn9F2 WC ##

  ## Inicio fn9F3 WC ##
  def fn9F3(self, conn):
        try:
            incident = conn.execute("""
              SELECT IncidentId
              from Incident
              WHERE
                RefIncidentBehaviorId IN (
                  SELECT RefIncidentBehaviorId
                  FROM RefIncidentBehavior
                  WHERE RefIncidentBehavior.description IN ('Reunión con apoderados','Entrevista')
                );
            """).fetchall()
            if(len(incident)>0):
                listIncident = (list([m[0] for m in incident if m[0] is not None]))
                for x in listIncident:
                    try:
                        x = str(x)
                        incidentParent = conn.execute("""
                          SELECT IncidentId 
                          FROM IncidentPerson 
                          where 
                          IncidentId = """+x+"""
                          and 
                          (
                            IncidentPerson.RefIncidentPersonRoleTypeId IN (
                              SELECT RefIncidentPersonRoleTypeId
                              FROM RefIncidentPersonRoleType
                              WHERE RefIncidentPersonRoleType.description IN ('Asiste a reunión de apoderados')
                            )
                            and 
                            IncidentPerson.RefIncidentPersonTypeId IN (
                              SELECT RefIncidentPersonTypeId
                              FROM RefIncidentPersonType
                              WHERE RefIncidentPersonType.description IN ('Apoderado')
                            )
                            OR
                            IncidentPerson.RefIncidentPersonRoleTypeId IN (
                              SELECT RefIncidentPersonRoleTypeId
                              FROM RefIncidentPersonRoleType
                              WHERE RefIncidentPersonRoleType.description IN ('Entrevistado')
                            )
                            and 
                            IncidentPerson.RefIncidentPersonTypeId IN (
                              SELECT RefIncidentPersonTypeId
                              FROM RefIncidentPersonType
                              WHERE RefIncidentPersonType.description IN ('Apoderado')
                            )	
                          )                                                      
                        """).fetchall()
                        incidentProfessor = conn.execute("""
                            SELECT IncidentId 
                            FROM IncidentPerson 
                            where 
                            IncidentId = """+x+"""
                            and 
                            (
                              IncidentPerson.RefIncidentPersonRoleTypeId IN (
                                SELECT RefIncidentPersonRoleTypeId
                                FROM RefIncidentPersonRoleType
                                WHERE RefIncidentPersonRoleType.description IN ('Dirige reunión de apoderados')
                              )
                              and 
                              IncidentPerson.RefIncidentPersonTypeId IN (
                                SELECT RefIncidentPersonTypeId
                                FROM RefIncidentPersonType
                                WHERE RefIncidentPersonType.description IN ('Docente')
                              )
                              OR
                              IncidentPerson.RefIncidentPersonRoleTypeId IN (
                                SELECT RefIncidentPersonRoleTypeId
                                FROM RefIncidentPersonRoleType
                                WHERE RefIncidentPersonRoleType.description IN ('Entrevistador')
                              )
                              and 
                              IncidentPerson.RefIncidentPersonTypeId IN (
                                SELECT RefIncidentPersonTypeId
                                FROM RefIncidentPersonType
                                WHERE RefIncidentPersonType.description IN ('Docente')
                              )	
                            )                                                         
                        """).fetchall()
                        parent = 0
                        professor = 0
                        if (len(incidentParent)>0):
                            parent +=1
                        else:
                            logger.info(f"S/Datos")
                            logger.info(f"Sin registros de actividades familiares o comunitarias")
                            return False
                        if (len(incidentProfessor)>0):
                            professor += 1
                        else:
                            logger.info(f"S/Datos")
                            logger.info(f"Sin registros de actividades familiares o comunitarias")
                            return False
                    except Exception as e:
                        logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
                        logger.error(f"Rechazado")
                        return False
                logger.info(f'Reuniones validas')
                logger.info(f'Aprobado')
                return True
            else:
                logger.info(f"S/Datos")
                logger.info(f"Sin registros de actividades familiares o comunitarias")
                return True
        except Exception as e:
            logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
            logger.error(f"Rechazado")
            return False
  ## Fin fn9F3 WC ##

  ## Inicio fn8F0 WC ##
  def fn8F0(self, conn):
        try:
            #Reconocimientos
            _queryStudentAcademicHonor = conn.execute("""
            SELECT
                K12S.HonorDescription
            FROM K12StudentAcademicHonor K12S
                    join OrganizationPersonRole OPR on K12S.OrganizationPersonRoleId = OPR.OrganizationPersonRoleId
            WHERE length(trim(K12S.HonorDescription)) > 0
            and trim(K12S.HonorDescription) is not null
            and OPR.RoleId = 6
            and K12S.RefAcademicHonorTypeId = 9;
            """).fetchall()
            #Medidas diciplinarias aplicadas al estudiantes
            _k12StudentDiscipline = conn.execute("""
            SELECT K12SD.K12StudentDisciplineId,
                K12SD.OrganizationPersonRoleId,
                K12SD.RefDisciplineReasonId,
                K12SD.RefDisciplinaryActionTakenId,
                K12SD.DisciplinaryActionStartDate,
                K12SD.personId,
                K12SD.IncidentId
            FROM K12StudentDiscipline K12SD
                    join OrganizationPersonRole OPR on K12SD.OrganizationPersonRoleId = OPR.OrganizationPersonRoleId
            WHERE OPR.OrganizationPersonRoleId = 6;
            """).fetchall()
            #Anotaciones negativas
            _negative = conn.execute("""
            SELECT IncidentId,
                IncidentIdentifier,
                IncidentDate,
                IncidentTime,
                IncidentDescription,
                RefIncidentBehaviorId,
                OrganizationPersonRoleId
            FROM Incident
            WHERE RefIncidentBehaviorId = 34;
            """).fetchall()
            #Reuniones con el apoderado
            _mettings = conn.execute("""
            SELECT K12StudentDisciplineId,
                  OrganizationPersonRoleId,
                  DisciplinaryActionStartDate,
                  IncidentId
            FROM K12StudentDiscipline
            WHERE RefDisciplinaryActionTakenId = 8;
            """).fetchall()
            if(len(_queryStudentAcademicHonor) == 0 and len(_k12StudentDiscipline) == 0 and len(_negative) == 0 and len(_mettings) == 0):
                logger.info(f"S/Datos")
                logger.info(f"Rechazado")
                return False
            else:
                for a in _queryStudentAcademicHonor:
                    for b in a:
                        if b is None:
                            logger.error(f"Reconocimientos por el cumplimiento del reglamento interno mal ingresados en el sistema")
                            logger.error(f"Rechazado")
                            return False
                for c in _k12StudentDiscipline:
                    for d in c:
                        if d is None:
                            logger.error(f"Medidas diciplinarias ingresadas erroneamente en el sistema")
                            logger.error(f"Rechazado")
                            return False
                for e in _negative:
                    for f in e:
                        if f is None:
                            logger.error(f"Anotaciones negativas ingresadas erroneamente en el sistema")
                            logger.error(f"Rechazado")
                            return False
                for g in _mettings:
                    for h in g:
                        if h is None:
                            logger.error(f"Reuniones con los apoderados mal ingresadas en el sistema")
                            logger.error(f"Rechazado")
                            return False
                logger.info(f'Los datos sobre: Anotaciones positivas y negativas, citaciones a apoderados, medidas diciplinarias y reconocimientos por cumplimiento de reglamento interno estan ingresados correctamente')
                logger.info(f'Aprobado')
                return True
        except Exception as e:
            logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
            logger.error(f"Rechazado")
            return False
  ## Fin fn8F0 WC ##

  ## Inicio fn5E2 WC ##
  def fn5E2(self, conn):
        try:
            rows= conn.execute("""
            select Pi.Identifier,
                  (p.FirstName || ' ' || p.MiddleName || ' ' || p.LastName || ' ' || p.SecondLastName) as "nombre completo",
                  pdc.DegreeOrCertificateTitleOrSubject,
                  pdc.AwardDate,
                  pdc.NameOfInstitution,
                  rae.RefAttendanceStatusId
                    ,
                  rae.observaciones
            from Person P
                    join OrganizationPersonRole opr on p.PersonId = Opr.PersonId
                    join PersonDegreeOrCertificate pdc on p.PersonId = pdc.PersonId
                    join RoleAttendanceEvent rae on rae.OrganizationPersonRoleId = opr.OrganizationPersonRoleId
                    join PersonIdentifier pi on pi.PersonId = p.PersonId
            where RoleId != 6
              and rae.observaciones like '%Falta docente%';
                    """).fetchall()
            if(len(rows)>0):
                identificador = (list(set([m[0] for m in rows if m[0] is not None])))
                if not identificador:
                    logger.error(f"Sin identificador")
                    logger.error(f'Rechazado')
                    return False
                nombre = (list(set([m[1] for m in rows if m[1] is not None])))
                if not nombre:
                    logger.error(f"Sin nombre")
                    logger.error(f'Rechazado')
                    return False
                titulo = (list(set([m[2] for m in rows if m[2] is not None])))
                if not titulo:
                    logger.error(f"Sin titulo")
                    logger.error(f'Rechazado')
                    return False
                fechatitulo = (list(set([m[3] for m in rows if m[3] is not None])))
                if not fechatitulo:
                    logger.error(f"Sin fecha de titulo")
                    logger.error(f'Rechazado')
                    return False
                institucion = (list(set([m[4] for m in rows if m[4] is not None])))
                if not institucion:
                    logger.error(f"Sin institucion")
                    logger.error(f'Rechazado')
                    return False
                observacion = (list(set([m[5] for m in rows if m[5] is not None])))
                if not observacion:
                    logger.error(f"Sin observacion")
                    logger.error(f'Rechazado')
                    return False
                logger.info(f"Docentes validados")
                logger.info(f"Aprobado")
                return True
            else:
                logger.info(f"S/Datos")
                logger.info(f"Sin clases en las que no hay docente/s")
                return True
        except Exception as e:
            logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
            logger.error(f"Rechazado")
            return False
  ## Fin fn5E2 WC ##

  ## Inicio fn5E3 WC ##
  def fn5E3(self,conn):
        try:
            i=0
            suplencias_noidoneas = conn.execute("""
            SELECT
                FirstName,
                MiddleName,
                LastName,
                OCS.claseRecuperadaId,
                digitalRandomKey
            FROM Organization o
            JOIN OrganizationPersonRole OPR on O.OrganizationId = OPR.OrganizationId
            JOIN RoleAttendanceEvent RAE on OPR.OrganizationPersonRoleId = RAE.OrganizationPersonRoleId
            JOIN Person P on OPR.PersonId = P.PersonId
            JOIN PersonDegreeOrCertificate PDOC on P.PersonId = PDOC.PersonId
            JOIN Location L on  L.LocationId = o.OrganizationId
            JOIN Classroom Cr on L.LocationId = Cr.LocationId
            JOIN CourseSectionLocation CSL on Cr.LocationId = CSL.LocationId
            JOIN CourseSection CS on CSL.OrganizationId = CS.OrganizationId
            JOIN OrganizationCalendar OC on CSL.OrganizationId = OC.OrganizationId
            JOIN OrganizationCalendarSession OCS on OC.OrganizationCalendarId = OCS.OrganizationCalendarId
            where OPR.RoleId !=6
            and PDOC.idoneidadDocente != 1
            and LOWER(RAE.observaciones) like '%falta docente%';
            """).fetchall()
            a=len(suplencias_noidoneas)
            if (len(suplencias_noidoneas)>0):
                for fila in suplencias_noidoneas:
                    if fila[3] is None or 0 or fila[4] is None  :
                        logger.error(f'clase con profesor suplente no idoneo no registrada para recuperar o registrada mas no firmada')
                        logger.error(f'Rechazado')
                        return False
                    else:
                        if i == a and fila[a][3] is not None or 0 and fila[a][4] is not None:
                            logger.info(f'verificacion aprobada,Todas las suplencias tienen indicada la recuperacion y estan firmadas')
                            logger.infor(f'Aprobado')
                            return True
                        else:
                            i+=1
            else:
                logger.error(f'S/Datos')
                logger.error(f"Sin clases en las que no hay docente/s")
                return True
        except Exception as e:
            logger.error(f'NO se pudo ejecutar la verificación en la lista')
            logger.error(f'Rechazado')
            return False
  ## fin fn5E3 WC ##

  ## Inicio fn9F0 WC ##
  def fn9F0(self,conn):
        try:
            i=0
            docentes = conn.execute("""
            SELECT
                  P.PersonId,
                  PDOC.DegreeOrCertificateTitleOrSubject
            from Organization o
                    join OrganizationPersonRole OPR on o.OrganizationId = OPR.OrganizationId
                    join Person P on OPR.PersonId = P.PersonId
                    join PersonDegreeOrCertificate PDOC on P.PersonId = PDOC.PersonId
            where OPR.RoleId = 5
            group by P.PersonId
            """).fetchall()
            a=len(docentes)
            if(len(docentes)):
                for fila in docentes:
                    for column in fila:
                        if column is None:
                            logger.info(f'informacion incompleta del profesor')
                            logger.info(f'Rechazado')
                            return False
                        else:
                            if i == a:
                                logger.info(f'Informacion de profesores completa')
                                logger.info(f'Aprobado')
                                return True
                            else:
                                i+=1
            else:
                logger.error(f'S/Datos')
                logger.error(f'Sin datos de docentes')
                return False
        except Exception as e:
            logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
            logger.error(f"Rechazado")
            return False
  ## Fin fn9F0 WC ##

  ## Fin fn9F1 WC ##
  def fn9F1(self,conn):
    try:
        _query = conn.execute("""
        SELECT
              P.PersonId,
              OPR.OrganizationId,
              C.Description,
              CSS.ClassMeetingDays,
              CSS.ClassBeginningTime,
              CSS.ClassEndingTime
        from Person P
                join OrganizationPersonRole OPR on P.PersonId = OPR.PersonId
                join Organization O on OPR.OrganizationId = O.OrganizationId
                join Course C on O.OrganizationId = C.OrganizationId
                join CourseSection CS on C.OrganizationId = CS.CourseId
                join CourseSectionSchedule CSS on CSS.OrganizationId = CS.OrganizationId
        where OPR.RoleId = 6
          and O.RefOrganizationTypeId = 21;
        """).fetchall()
        if (len(_query)>0):
          for x in _query:
            for y in x:
              if y is None:
                logger.error(f'Se encuentran datos incompletos sobre la formacion del los estudientes')
                logger.error(f'Rechazado')
                return False
          logger.info(f'Todos los registros formativos de los estudiantes se encuentran registrados en el sistema')
          logger.info(f'Aprobado')
          return True
        else:
          logger.error(f'S/Datos')
          logger.error(f'Sin datos de la formacion del estudiante')
          return False
    except Exception as e:
        logger.error(f"No se pudo ejecutar la consulta: {str(e)}")
        logger.error(f"Rechazado")
        return False
  ## Fin fn9F1 WC ##

### WebClass FIN ###

### MIAULA INICIO ###

### inicio FN0FA ###
  def fn0FA(self, conn):
    try:
      r_ = []
      r_ = conn.execute("""
              SELECT 
                DISTINCT A.personId
                , CASE WHEN A.RetirarEstudianteIndicador like '%SI%' THEN 'True' ELSE 'False' END as RetirarEstudianteIndicador
              FROM PersonList A
              JOIN OrganizationPersonRole B
                ON A.personId = B.personId
              JOIN jerarquiasList C
                ON B.OrganizationId = C.OrganizationIdDelCurso
              WHERE
                A.Role like '%Estudiante%'
                AND C.nivel NOT IN ('03:Educación Básica Adultos'
                      ,'06:Educación Media Humanístico Científica Adultos'
                      ,'08:Educación Media Técnico Profesional y Artística, Adultos')
    """).fetchall()
    except Exception as e:
      pass
    try:
      logger.info(f"VERIFICA QUE EXISTA LISTADO DE ALUMNOS EN VISTA PERSONLIST Y QUE TENGAN PERSONAS ASOCIADAS Y AUTORIZADAS PARA RETIRO.")
      if(len(r_)>0):
        c_ = 0
        p_ = self.convertirArray2DToList(list([m[0] for m in r_ if m[0] is not None])) 
        r2_ = self.convertirArray2DToList(list([m[1] for m in r_ if m[1] is not None]))        

        for r in r2_:
          if(r == 'True'):
            c_ = c_ + 1

        logger.info(f"Total Alumnos                                     : {len(r_)}")
        logger.info(f"Total Personas asociadas y autorizadas para retiro: {c_}")

        if(c_ >= len(r_)):
          logger.info(f"TODOS los alumnos tienen informacion de personas asociadas y/o autorizadas para retiro.")
          logger.info(f"Apobado")
          return True
        else:
          logger.error(f"No todos los alumnos tienen informacion de personas asociadas y/o autorizadas para retiro.")
          logger.error(f"Rechazado")
          return False

      else:
        logger.info(f"S/Datos")
        return  False

    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta a la vista personList filtrada por alumnos: {str(e)}")
      logger.error(f"Rechazado")
      return False
### fin FN0FA ###

### inicio FN0FB ###
  def fn0FB(self, conn):
    try:

      _msg = ""
      _f1 = False
      _drk = 0 #DigitalRandomKey
      _pr = 0 #PersonId autorizada para retiro

      _s1 = """SELECT a.OrganizationPersonRoleId
                      ,date(a.ExitDate) as ExitDate
                      ,time(a.ExitDate) as ExitTime
                      ,a.personId
                FROM OrganizationPersonRole a
                JOIN Organization B
                  ON A.OrganizationId = B.OrganizationId
                JOIN RefOrganizationType D
                  ON B.RefOrganizationTypeId = D.RefOrganizationTypeId
                WHERE 
                  a.RoleId = 6
                  AND 
                  a.ExitDate IS NOT NULL
                  AND 
                  B.name NOT IN ('03:Educación Básica Adultos'
                                    ,'06:Educación Media Humanístico Científica Adultos'
                                    ,'08:Educación Media Técnico Profesional y Artística, Adultos')
                  AND 
                  D.Description = 'K12 School';"""

      _s2 = """SELECT a.OrganizationPersonRoleId
                      ,date(a.ExitDate) as ExitDate
                      ,time(a.ExitDate) as ExitTime
                      ,a.personId
                FROM OrganizationPersonRole a
                JOIN Organization B
                ON A.OrganizationId = B.OrganizationId
                JOIN RefOrganizationType C
                ON B.RefOrganizationTypeId = C.RefOrganizationTypeId
                WHERE date(a.ExitDate) = ?
                AND (c.Description = 'Course Section' or c.Description = 'Course');"""

      _s3 = """SELECT digitalRandomKey,
                      fileScanBase64,
                      observaciones
                FROM RoleAttendanceEvent
              WHERE OrganizationPersonRoleId = ?
                AND (RefAttendanceEventTypeId = 2 OR RefAttendanceEventTypeId = 5)
                AND RefAttendanceStatusId = 5
                AND date(Date) = ?
                and time(Date) = ?;"""

      _s4 = """SELECT a.OrganizationPersonRoleId
                      ,date(a.ExitDate) as ExitDate
                      ,time(a.ExitDate) as ExitTime
                      ,a.personId
                      ,a.RoleId
                FROM OrganizationPersonRole a
                JOIN Organization B
                  ON A.OrganizationId = B.OrganizationId
                JOIN RefOrganizationType C
                  ON B.RefOrganizationTypeId = C.RefOrganizationTypeId
                WHERE 
                  date(a.ExitDate) = ?
                  AND time(a.ExitDate) = ?
                  AND c.Description = 'K12 School';"""

      _s5 = """SELECT A.RelatedPersonId ,A.RetirarEstudianteIndicador
                    FROM PersonRelationship A
                    WHERE A.personId = ?"""

      #VERIFICA SI EXISTE REGISTRO DE RETIROS ANTICIPADOS DEL ESTABLECIMIENTO (OrganizationPersonRole)
      logger.info(f"VERIFICA CONSISTENCIA EN FECHA Y HORA DE REGISTROS DE RETIRO Y LA EXISTENCIA DE FIRMA DIGITAL Y/O DOCUMENTO DIGITALIZADO DE AUTORIZACION PARA EL CASO DE QUIEN RETIRA.")
      _r = conn.execute(_s1).fetchall()
      if(len(_r)>0):
        for r in _r:
          _o = r[0]
          _f = r[1]
          _t = r[2]
          _p = r[3]
          #VERIFICA SI EXISTE REGISTRO DE RETIRO DE CLASES PREVIO AL RETIRO DEL ESTABLECIMIENTO EN LA MISMA FECHA (OrganizationPersonRole)
          _v = (str(_f))
          _r2 = conn.execute(_s2, _v).fetchall()
          if (len(_r2)>0):
            for r2 in _r2:
              _o2 = r2[0]
              _f2 = r2[1]
              _t2 = r2[2]
              _p2 = r2[3]

              if(_p == _p2):
                _v2 = (str(_o2),str(_f2),str(_t2))
                _r3 = conn.execute(_s3, _v2).fetchall()
                if(len(_r3)>0):
                  for r3 in _r3:
                    _drk = r3[0]
                    if _drk is None:
                      logger.error(f"Registro de salida de clases no tiene firma de docente (OrganizationPersonRole).")
                      logger.error(f"Rechazado")
                      return False
                else:
                  logger.error(f"No hay registro de retiro de clases (RoleAttendanceEvent)")
                  logger.error(f"Rechazado")
                  return False

              else:
                _v2 = (str(_o2),str(_f2),str(_t2))
                _r3 = conn.execute(_s3, _v2).fetchall()
                if(len(_r3)>0):
                  for r3 in _r3:
                    _drk2 = r3[0]

                    if _drk2 is None:
                      logger.error(f"Registro de salida de clases no tiene firma de docente (RoleAttendanceEvent).")
                      logger.error(f"Rechazado")
                      return False
          else:
            logger.error(f"NO existe registro de salida de clases previo al retiro del establecimiento del alumno.")
            logger.error(f"Rechazado")
            return False

          #VERIFICA SI EXISTE REGISTRO DE RETIRO DE ESTABLECIMIENTO Y QUE COINCIDA CON FECHA Y HORA (RoleAttendanceEvent)
          _v4 = (str(_f),str(_t))
          _r4 = conn.execute(_s4, _v4).fetchall()
          if(len(_r4)>0):
            for r4 in _r4:
              _o4 = r4[0]
              _f4 = r4[1]
              _t4 = r4[2]
              _p4 = r4[3]
              _rl4 = r4[4]

              _v5 = (str(_o4),str(_f4),str(_t4))
              _r5 = conn.execute(_s3, _v5).fetchall()
              #logger.info(f"_o4 {str(_o4)},_f4 {str(_f4)},_t4 {str(_t4)},_rl {str(_rl4)}")
              if(len(_r5)>0):
                for r5 in _r5:
                  _drk = r5[0]
                  _fsb = r5[1]
                  _obs = r5[2]
                  if(_rl4 == 6):
                    if(_drk is None and _obs is None):
                      logger.error(f"Falta firma y observacion en registro de retiro de estudiante de establecimiento.")
                      logger.error(f"Rechazado")
                      return False
                  elif(_rl4 == 11):
                    if _drk is None:
                      logger.error(f"Falta firma de administrativo en registro de retiro de estudiante de establecimiento.")
                      logger.error(f"Rechazado")
                      return False
                  else:
                    _v6 = (_p4)
                    _r6 = conn.execute(_s5, _v6).fetchall()
                    if(len(_r6)>0):
                      for r6 in _r6:
                        _pr = r6[1]
                        if not _pr:
                          logger.info(f"La persona que retira a alumno no figura como autorizado en el sistema.")
                          logger.info(f"Apobado")
                          return True
                    if(_drk is None and _fsb is None):
                      logger.error(f"Falta firma o documento digitalizado de apoderado en registro de retiro de estudiante de establecimiento.")
                      logger.error(f"Rechazado")
                      return False

        logger.info(f"Apobado")
        return True
      else:
        logger.info(f"NO existen registros de retiro anticipado de alumnos en el establecimiento.")
        logger.info(f"S/DATOS")
        return True

    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta de retiros anticipados: {str(e)}")
      logger.error(f"Rechazado")
      return False
### fin FN0FB ###

### inicio fn1FA ###
  def fn1FA(self, conn):
    _Apo=[]
    try:

     # VALIDO LA EXISTENCIA DE ALUMNOS RETIRADOS Y QUE TENGAN REGISTRADA FECHA DE RETIRO
      _s1 = """SELECT A.personId,B.Identifier,C.OrganizationPersonRoleId ,C.ExitDate
                FROM PersonStatus A
                JOIN PersonIdentifier B
                ON A.personId = B.personId
                JOIN OrganizationPersonRole C
                ON A.personId = C.personId
                where A.RefPersonStatusTypeId = 30;"""

      # OBTENGO INFORMACION DE APODERADO
      _s2 = """SELECT A.RelatedPersonId ,A.personId
                FROM PersonRelationship A
                JOIN OrganizationPersonRole B
                  ON A.RelatedPersonId = B.personId
                WHERE A.personId = ?
                AND B.RoleId = 15;"""

      # OBTENGO ID DE INCIDENTE ASOCIADO
      _s3 = """SELECT A.IncidentId
                FROM IncidentPerson A
                JOIN Incident B
                ON A.IncidentId = B.IncidentId
                WHERE A.personId = ?
                AND B.RefIncidentBehaviorId = 33;"""

      # OBTENGO INFORMACION DE PERSONAS ASOCIADAS A INCIDENTE
      _s4 = """SELECT A.personId,A.RefIncidentPersonTypeId ,A.digitalRandomKey, A.fileScanBase64
                FROM IncidentPerson A
                WHERE A.IncidentId = ?;"""

      #VERIFICA SI EXISTE REGISTRO DE RETIROS ANTICIPADOS DEL ESTABLECIMIENTO (OrganizationPersonRole)
      logger.info(f"VERIFICA LA EXISTENCIA DE REGISTRO DE RETIROS DE ESTUDIANTES DEL ESTABLECIMIENTO.")
      _r = conn.execute(_s1).fetchall()
      if(len(_r)>0):
        _p = self.convertirArray2DToList(list([m[0] for m in _r if m[0] is not None]))
        _i = self.convertirArray2DToList(list([m[1] for m in _r if m[1] is not None]))
        _opr = self.convertirArray2DToList(list([m[2] for m in _r if m[2] is not None]))
        _ed = self.convertirArray2DToList(list([m[3] for m in _r if m[3] is not None])) 
        #VALIDO QUE REIGISTRO DE RETIRO TENGA FECHA DEL EVENTO
        if (len(_p)>len(_ed)):
          logger.error(f"Existen registros de retiros de estudiantes del establecimiento sin fecha de evento.")
          logger.error(f"Rechazado")
          return False
        else:
          for p in _p:
            _v = str(p)
            _r2 = conn.execute(_s2,_v).fetchall()
            if(len(_r2)>0):  
              for rp in _r2:
                _v3 = str(rp[0])
                _r3 = conn.execute(_s3, _v3).fetchall()
                if(len(_r3)>0):
                  for r3 in _r3:
                    _v4 = r3
                    _r4 = conn.execute(_s4, _v4).fetchall()
                    if(len(_r4)>0):
                      for r4 in _r4:
                        va1=str(r4[2])
                        va2=str(r4[3])
                        if(str(r4[1]) == "44"): #docente
                          if va1 is None:
                            logger.error(f"No hay registro de firma digital de docente / administrativo para incidente.")
                            logger.error(f"Rechazado")
                            return False
                        elif(str(r4[1]) == "43"): #apoderado
                          if va1 is None: 
                            if va2 is None:
                              logger.error(f"No hay registro de firma digital ni documento digitalizado de apoderado para incidente.")
                              logger.error(f"Rechazado")
                              return False
                    else:
                      logger.error(f"No hay registro de personas asociadas a incidente Id: {str(r3)}")
                      logger.error(f"Rechazado")
                      return False

                else:
                  logger.error(f"No hay registro de entrega de informacion por retiro de estudiante de establecimiento.")
                  logger.error(f"Rechazado")
                  return False
        logger.info(f"Aprobado")
        return True        
      else:
        logger.info(f"NO existen registros de retiro de alumnos del establecimiento.")
        logger.info(f"S/Datos")
        return True

    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta de entrega de informaciÓn: {str(e)}")
      logger.error(f"Rechazado")
      return False
### fin fn1FA ###

### inicio fn1FB ###
  def fn1FB(self, conn):
    try:
      _l = []
      _l2 = []
      # OBTENGO LISTADO DE ALUMNOS
      _s1 = """SELECT personId,run
                FROM personList
                WHERE Role like 'Estudiante';"""

      # OBTENGO INFORMACION DE PERSONAS RELACIONADAS CON ALUMNO REGISTRADAS EN EL SISTEMA
      _s2 = """SELECT A.RelatedPersonId,D.RUN
                FROM PersonRelationship A
                  JOIN OrganizationPersonRole B
                    ON A.RelatedPersonId = B.personId
                  JOIN Role C
                    ON B.RoleId = C.RoleId
                  JOIN personList D
                    ON A.RelatedPersonId = D.personId
                WHERE 
                A.personId = ?
                AND
                B.RoleId = 15;"""

      # OBTENGO ID DE REGISTRO DE ENTREGA DE INFORMACION DE INTERES A LOS APODERADOS
      _s3 = """SELECT A.IncidentId
                FROM IncidentPerson A
                JOIN Incident B
                ON A.IncidentId = B.IncidentId
                WHERE A.personId = ?
                AND B.RefIncidentBehaviorId = 35;"""

      # OBTENGO DETALLE DE EVENTO Y VALIDO FIRMA DE DOCENTE/ADMINISTRATIVO Y DOCUMENTO DIGITALIZADO
      _s4 = """SELECT A.RefIncidentPersonTypeId,A.digitalRandomKey,A.fileScanBase64,C.run
                FROM IncidentPerson A
                JOIN personList C
                ON A.personId = C.personId
                WHERE A.IncidentId = ?;"""

      _q1 = conn.execute(_s1).fetchall()
      if(len(_q1)!=0):
        for q1 in _q1:
          _p = str(q1[0])
          _r = str(q1[0])
          _q2 = conn.execute(_s2,_p).fetchall()
          if(len(_q2)!=0):
            for q2 in _q2:
              _p1 = str(q2[0])
              _r2 = str(q2[1])
              _q3 = conn.execute(_s3,_p1).fetchall()
              logger.info(len(_q3))
              if(len(_q3)!=0):
                for q3 in _q3:
                  _i = str(q3[0])
                  if(_i is None):
                    _l2.append(_r2)
                  else:                  
                    _q4 = conn.execute(_s4,_i).fetchall()
                    if(len(_q4)!=0):
                      _lst = self.convertirArray2DToList(list([str(m[0]) for m in _q4 if m[0] is not None]))
                      if '44' in _lst and '43' in _lst:
                        for q4 in _q4:
                          _pr = q4[0]
                          if(str(_pr)=="44"): #docente
                            _rdk = str(q4[1])
                            if(_rdk is None):
                              logger.error(f"No hay registro de firma de docente para evento de entrega de informacion de interes.")
                              logger.error(f"Rechazado")
                              return False
                          elif(str(_pr)=="43"): #apoderado
                              _fsb = str(q4[2])
                              if(_fsb is None):
                                logger.error(f"No hay registro de documento digitalizado entregado a apoderado para evento de entrega de informacion de interes.")
                                logger.error(f"Rechazado1")
                                return False
                      else:
                        logger.error(f"No hay registro de docente y/o apoderado para evento de entrega de informacion de interes.")
                        logger.error(f"Rechazado")
                        return False

                    else:
                      logger.error(f"No hay registro de personas asociadas al evento de entrega de informacion de interes.")
                      logger.error(f"Rechazado")
                      return False

                if(len(_l2)>0):
                  logger.error(f"Los siguientes apoderados no tienen registro de entrega de informacion de interes por parte del establecimiento: {str(_l2)}")
                  logger.error(f"Rechazado")
                  return False

              else:
                logger.error(f"No hay registro de entrega de informacion de interes del establecimiento al apoderado.")
                logger.error(f"Rechazado")
                return False

          else:
            _l.append(_r)           

        if(len(_l)>0):
          logger.error(f"Los siguientes alumnos no tienen informacion de apoderado asociado en el sistema: {str(_l)}")
          logger.error(f"Rechazado")
          return False
        else:
          logger.info(f"Aprobado")
          return True        

    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta de entrega de informaciÓn: {str(e)}")
      logger.error(f"Rechazado")
      return False
### fin fn1FB ###

### inicio fn1FC ###
  def fn1FC(self, conn):
    try:
      _l = []
      _l2 = []
      _l3 = 0
      # OBTENGO LISTADO DE ALUMNOS
      _s1 = """SELECT A.personId,B.Identifier,C.OrganizationPersonRoleId ,C.ExitDate
                FROM PersonStatus A
                JOIN PersonIdentifier B
                ON A.personId = B.personId
                JOIN OrganizationPersonRole C
                ON A.personId = C.personId
                where A.RefPersonStatusTypeId = 30;"""

      # OBTENGO INFORMACION DE PERSONAS RELACIONADAS CON ALUMNO REGISTRADAS EN EL SISTEMA
      _s2 = """SELECT A.RelatedPersonId,D.RUN
                FROM PersonRelationship A
                JOIN OrganizationPersonRole B
                  ON A.RelatedPersonId = B.personId
                JOIN Role C
                  ON B.RoleId = C.RoleId
                JOIN personList D
                  ON A.RelatedPersonId = D.personId
                WHERE 
                  A.personId = ?
                  AND
                  B.RoleId = 15;"""

      # OBTENGO ID DE REGISTRO DE ENTREGA DE INFORMACION DE INTERES A LOS APODERADOS
      _s3 = """SELECT A.IncidentId
            FROM IncidentPerson A
            INNER JOIN Incident B ON A.IncidentId = B.IncidentId
            WHERE A.personId = ?
            AND B.RefIncidentBehaviorId = 36;
          """

      # OBTENGO DETALLE DE EVENTO Y VALIDO FIRMA DE DOCENTE/ADMINISTRATIVO Y DOCUMENTO DIGITALIZADO
      _s4 = """SELECT A.RefIncidentPersonTypeId,A.digitalRandomKey,A.fileScanBase64,C.run
                FROM IncidentPerson A
                JOIN personList C
                ON A.personId = C.personId
                WHERE A.IncidentId = ?;"""

      _q1 = conn.execute(_s1).fetchall()
      if(len(_q1)!=0):
        for q1 in _q1:
          _p = str(q1[0])
          _r = str(q1[0])

          _q2 = conn.execute(_s2,_p).fetchall()
          if(len(_q2)!=0):
            for q2 in _q2:
              _p1 = str(q2[0])
              _r2 = str(q2[1])

              _q3 = conn.execute(_s3,_p1).fetchall()
              if(len(_q3)!=0):
                for q3 in _q3:
                  _i = str(q3[0])
                  if(_i is None):
                    _l2.append(_r2)
                  else:                  
                    _q4 = conn.execute(_s4,_i).fetchall()
                    if(len(_q4)!=0):
                      _lst = self.convertirArray2DToList(list([str(m[0]) for m in _q4 if m[0] is not None]))
                      if '44' in _lst and '43' in _lst:
                        for q4 in _q4:
                          _pr = str(q4[0])
                          if(str(_pr)=="44"): #docente
                            _rdk = str(q4[1])
                            if(_rdk is None):
                              logger.error(f"No hay registro de firma de docente/administrativo para evento.")
                              logger.error(f"Rechazado")
                              return False
                            else:
                              _l3 = 1
                          elif(str(_pr)=="43"): #apoderado
                              _fsb = str(q4[2])
                              if(_fsb is None):
                                logger.error(f"No hay registro de documento digitalizado entregado a apoderado para evento.")
                                logger.error(f"Rechazado")
                                return False
                              else:
                                _l3 = 1
                      else:
                        logger.error(f"No har registro de docente y/o apoderado para evento.")
                        logger.error(f"Rechazado")
                        return False

                    else:
                      logger.error(f"No hay registro de personas asociadas al evento.")
                      logger.error(f"Rechazado")
                      return False

                if(len(_l2)>0):
                  logger.error(f"Los siguientes apoderados no tienen registro de evento: {str(_l2)}")
                  logger.error(f"Rechazado")
                  return False

              else:
                logger.error(f"No hay registro de entrega de informacion al apoderado.")
                logger.error(f"Rechazado")
                return False

          else:
            _l.append(_r)

        if(len(_l)>0):
          logger.error(f"Los siguientes alumnos no tienen informacion de apoderado asociado en el sistema: {str(_l)}")
          logger.error(f"Rechazado")
          return False

      if(_l3 == 1):
        logger.info(f"Aprobado")
        return True

    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta de entrega de informaciÓn: {str(e)}")
      logger.error(f"Rechazado")
      return False
### fin fn1FC ###

### inicio fn6F0  ##
  def fn6F0(self,conn):
    arr=[]
    try:
      """
SELECT 
	CAST(julianday('2021-11-26')-julianday('2021-11-25') as INTEGER) as workDays      
      
WITH RECURSIVE dates(date) AS (
  VALUES('2021-03-01')
  UNION ALL
  SELECT date(date, '+1 day')
  FROM dates
  WHERE 
	-- Considera la menor fecha entre LastInstructionDate y la fecha actual (now)
	strftime('%Y-%m-%d',date) < strftime('%Y-%m-%d','2021-10-30') 
	AND
	strftime('%Y-%m-%d',date) < strftime('%Y-%m-%d','now')
)
SELECT date 
FROM dates
WHERE CAST(strftime('%w',date) as INTEGER) between 1 and 5      
      """
      
           # select para listar todos los colegios de tabla organizacion
      _S1= """
SELECT 
  org.OrganizationId,
  org.Name,
  b.OrganizationCalendarId,
  strftime('%Y-%m-%d',c.FirstInstructionDate) as FirstInstructionDate,
  strftime('%Y-%m-%d',c.LastInstructionDate) AS  LastInstructionDate
FROM Organization org
  JOIN OrganizationCalendar b 
	ON org.OrganizationId = b.OrganizationId
  JOIN OrganizationCalendarSession c
	ON b.organizationcalendarid = c.organizationcalendarid 
WHERE 
	org.RefOrganizationTypeId IN (
		SELECT RefOrganizationTypeId
		FROM RefOrganizationType
		WHERE RefOrganizationType.description IN ('K12 School')
	)
      """

      # trae la fechas para calcular los dias feriados 
      _s2=""" 
        select 
          strftime('%Y-%m-%d',StartDate) as StartDate,
          strftime('%Y-%m-%d',EndDate) as EndDate 
        from OrganizationCalendarCrisis 
        where OrganizationId = ?;
      """

       # select para ver todos los dias de eventos por cada organizacion 
      _s3=""" 
        select * 
        from OrganizationCalendarEvent 
        where OrganizationCalendarId = ?;"""

       # contabilizar las crisis de un colegio 
      _s4=""" 
        select 
          b.RUN,
          strftime('%Y-%m-%d',a.EntryDate) as EntryDate,
          strftime('%Y-%m-%d',a.ExitDate) as ExitDate 
        from OrganizationPersonRole a
          join personlist b
            on a.personid=b.personId 
        where 
          OrganizationId = ? 
          and 
          roleId=6
      """
      now=datetime.now()
      _q1 = conn.execute(_S1).fetchall()
      if(len(_q1)!=0):
        for q1 in _q1:
          org_id=str(q1[0])
          org_ca=str(q1[2])
          fecha_in=str(q1[3])
          fecha_ter=str(q1[4])
          f1=datetime.strftime(now, '%Y-%m-%d')
          if (f1 <= fecha_ter):
            fecha_ter=f1          
          diastotal=int(np.busday_count(fecha_in,fecha_ter))  
          _q2 = conn.execute(_s2,org_id).fetchall()
          if(len(_q2)!=0):
            for q2 in _q2:
                f2x=str(q2[0])
                f2=str(q2[1])
                if (f1 <= fecha_ter):
                  f2=f1               
                diastotal2=int(np.busday_count(f2x,f2))
                if diastotal2 > diastotal :
                  contador2 = diastotal2 - diastotal
                else:
                  contador2 = diastotal - diastotal2
          elif(len(_q2)==0): 
            contador2= diastotal          
          _q3 = conn.execute(_s3,org_ca).fetchall()
          if(len(_q3)!=0):
            xx=len(_q3)
            if int(xx)>contador2:
              contador3=int(xx)-contador2
            else:
              contador3=contador2-int(xx)
          elif(len(_q3)==0):
            contador3=contador2
           
          _q4 = conn.execute(_s4,int(org_id)).fetchall()
          if(len(_q4)!=0):
            for w1 in _q4:
              personid=str(w1[0])
              fecha1w=str(w1[1])
              fecha2w=str(w1[2])
              if w1[1] is None:
                fecha1w=fecha_in
              if w1[2] is None:
                fecha2w=fecha_ter              
              if (f1 <= fecha1w):
                fecha2w=f1
              diastotal3=int(np.busday_count(fecha1w,fecha2w))
              if diastotal3 < (contador2 + contador3):
                diastotal3 = (contador2 + contador3)-diastotal3
              else:
                diastotal3 = diastotal3 - (contador2 + contador3)              
              if(contador3!=diastotal3):
                arr.append(personid)
            if(len(arr)!=0):
              logger.error(f"Los siguientes alumnos no tienen la cantidad asistencia igual que el establecimiento : {str(arr)} ")
              logger.error(f"Rechazado")
              return False 
            else:
              logger.info(f"Aprobado")
              return True

          else:  
              logger.error(f"No hubo informacion de resgistros de estudiantes asociados del establecimiento. ")
              logger.error(f"Rechazado")
              return False   

      else:
        logger.error(f"No hay informacion de establecimiento.")
        logger.error(f"Rechazado")
        return False   

    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta de entrega de informaciÓn: {str(e)}")
      logger.error(f"Rechazado")
      return False
### fin fn6F0 ###

### inicio fn6F1 ###
  def fn6F1(self,conn):
    arr=[]
    try:
           
      _S1= """ 
select 
	strftime('%d',rae.Date) as Dia,
	strftime('%m',rae.Date) as Mes,
	strftime('%Y',rae.Date) as Año,
	pid.Identifier as Numerolista ,
	rae.VirtualIndicator 
FROM PersonIdentifier pid 
	JOIN  OrganizationPersonRole opr 
		on opr.personId = pid.personId
	JOIN RoleAttendanceEvent rae 
		on rae.OrganizationPersonRoleId = opr.OrganizationPersonRoleId 
where 
	pid.RefPersonIdentificationSystemId IN (
		SELECT RefPersonIdentificationSystemId
		FROM RefPersonIdentificationSystem
		WHERE RefPersonIdentificationSystem.Description IN ('Número de lista')
	)
	AND
	opr.roleid IN (
		SELECT RoleId
		FROM Role
		WHERE Name IN ('Estudiante')
	)
	AND
	rae.VirtualIndicator = 0
         """
    

      now=datetime.now()
      _q1 = conn.execute(_S1).fetchall()
      XX=0
      if(len(_q1)!=0):
        for q1 in _q1:
          dia=str(q1[0])
          mes=str(q1[1])
          año=str(q1[2])
          numero_l=str(q1[3])
          estado_asis=str(q1[4])
          
          if (dia is None) or (mes is None) or (año is None) or (numero_l is None) or (estado_asis is None): 
            arr.append(numero_l)

          if int(estado_asis)==0:
            asistencia="Presencial"

          if(len(arr)!=0):
              logger.error(f"Los siguientes numero de lista necesita informacion: {str(arr)} ")
              logger.error(f"Rechazado")
              return False
          else:
              logger.info(f"Ningunos de los registros le falta un dato.")
              logger.info(f"Apobado")
              return True
      else:
        logger.error(f"No hay registro Numero de lista asociados .")
        logger.error(f"Rechazado")
        return False   
    
    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta de entrega de informaciÓn: {str(e)}")
      logger.error(f"Rechazado")
      return False
### fin fn6f1  ###

### inicio fn6E2  ###
  def fn6E2(self, conn):
    try:
      _l1 = []
      logger.info(f"fn6E2 - Valida que no exista asistencia registrada para los dias definidos con suspension de clases.")

      _s1 = """SELECT a.Date,c.RUN
                FROM RoleAttendanceEvent a
                JOIN OrganizationPersonRole b
                ON a.OrganizationPersonRoleId = b.OrganizationPersonRoleId
                JOIN personList c ON b.personId = c.personId
                WHERE (a.Date in (SELECT EventDate FROM OrganizationCalendarEvent)
                    OR (a.Date BETWEEN (SELECT StartDate 
                              FROM OrganizationCalendarCrisis) and  
                              (SELECT EndDate 
                                FROM OrganizationCalendarCrisis)));"""     

      _q1 = conn.execute(_s1).fetchall()
      if(len(_q1)!=0):
        for q in _q1:
          _d = str(q[0])
          _r = str(q[1])
          _l1.append(_d+"-"+_r)
          logger.error(f"Existen registros de asistencia para dias con suspension de clases: {str(_l1)}")
          logger.error(f"Rechazado")
          return False
      else:
        logger.error(f"Aprobado")
        return True

    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta de entrega de informaciÓn: {str(e)}")
      logger.error(f"Rechazado")
      return False
### fin fn6E2  ###
 
### inicio fn6D0 ###
  def fn6D0(self, conn):
    logger.info(f"fn6D0 - Valida que las altas y bajas de los alumnos esten registradas en el sistema. El registro debe estar en las tablas PersonStatus y OrganizationPersonRole, y sus fechas deben ser las mismas.")
    try:
      _l = []
      _l2 = []
      _s1 = """
        SELECT 
          opr.OrganizationPersonRoleId
          ,pid.Identifier
          ,opr.EntryDate
          ,opr.ExitDate
          ,pst.StatusStartDate
          ,pst.StatusEndDate
        FROM OrganizationPersonRole opr
          JOIN Organization org 
            ON opr.OrganizationId = org.OrganizationId
            AND org.RefOrganizationTypeId IN (
              SELECT RefOrganizationTypeId
              FROM RefOrganizationType
              WHERE RefOrganizationType.description IN ('K12 School')
            )
          JOIN PersonIdentifier pid 
            ON opr.personId = pid.personId
            AND pid.RecordEndDateTime IS NULL
          JOIN RefPersonIdentificationSystem rpis 
            ON pid.RefPersonIdentificationSystemId = rpis.RefPersonIdentificationSystemId
            AND rpis.description In ('ROL UNICO NACIONAL')
          OUTER LEFT JOIN PersonStatus pst 
            ON opr.personId = pst.personId
            AND pst.RecordEndDateTime IS NULL
        WHERE 
          opr.RoleId IN (
            SELECT RoleId
            FROM Role
            WHERE role.Name IN ('Estudiante')
          )
          AND 
          pst.RefPersonStatusTypeId IN (
            SELECT RefPersonStatusTypeId
            FROM RefPersonStatusType
            WHERE RefPersonStatusType.Description IN ('Estudiante retirado definitivamente')
          )
      """
      _q1 = conn.execute(_s1)
      if(_q1.returns_rows == 0):
        logger.info(f"No hay registros de alta/baja de alumnos en el establecimiento.")
        logger.info(f"S/Datos")
        return True
      
      _q1 = _q1.fetchall()
      if(len(_q1)!=0):
        for q1 in _q1:
          _r = str(q1[1])
          _entryDate = str(q1[2]) # rescata OrganizationPersonRole.entryDate
          _exitDate = str(q1[3]) # rescata OrganizationPersonRole.exitDate
          _statusStartDate = str(q1[4]) # rescata personStatus.statusStartDate
          _statusEndDate = str(q1[5]) # rescata personStatus.statusEndDate

          if(_entryDate is None) or (_statusStartDate is None):
            _l.append(_r)
          elif(_entryDate != _statusStartDate):
            _l2.append(_r)
            
          if(_exitDate is None) or (_statusEndDate is None):
            _l.append(_r)
          elif(_exitDate != _statusEndDate):
            _l2.append(_r)
            
        
        if(len(_l)!=0):
          logger.error(f"Hay alumnos sin rergistro de fecha de alta/baja: {str(_l)}")
          logger.error(f"Rechazado")
          return False

        if(len(_l2)!=0):
          logger.error(f"Hay alumnos con inconsistencia en registros de alta/baja: {str(_l2)}")
          logger.error(f"Rechazado")
          return False
        
        logger.info(f"Aprobado")
        return True
    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta de entrega de informaciÓn: {str(e)}")
      logger.error(f"Rechazado")
      return False
### fin fn6D0 ###

### inicio fn6D1 ###
  def fn6D1(self, conn):
    logger.info(f"fn6D0 - Valida que no exista asistencia anterior al ingreso o posterior al retiro de un alumno en el establecimiento.")
    try:
      _l = []
      _l2 = []
      _s1 = """SELECT A.OrganizationPersonRoleId,C.RUN,A.EntryDate,A.ExitDate
                FROM OrganizationPersonRole A
                JOIN PersonStatus B
                ON A.personId = B.personId
                JOIN personList C
                ON B.personId = C.personId
                WHERE B.RefPersonStatusTypeId = 30;"""

      _s2 = """SELECT Date 
                FROM RoleAttendanceEvent
                WHERE OrganizationPersonRoleId = ?
                AND ((Date <= ?) OR (Date >= ?));"""

      _s3 = """SELECT A.FirstInstructionDate,A.LastInstructionDate
                FROM OrganizationCalendarSession A
                JOIN OrganizationCalendar B
                ON A.OrganizationCalendarId = B.OrganizationCalendarId
                JOIN Organization C
                ON B.OrganizationId = C.OrganizationId
                WHERE C.RefOrganizationTypeId = 10;"""

      _q1 = conn.execute(_s1).fetchall()
      if(len(_q1)!=0):
        for q1 in _q1:
          _o = q1[0]
          _r = str(q1[1])
          _d1 = q1[2]
          _d2 = q1[3]
          if(_d1 is None):
            _q2 = conn.execute(_s3).fetchall()
            if(len(_q2)!=0):
              _d1 = _q2[0]
            else:
              logger.error(f"No hay informacion de calendario academico del establecimiento.")
              logger.error(f"Rechazado")
              return False   
          if(_d2 is None):
            _l.append(_r)
          else:
            _q3 = conn.execute(_s2,_o,_d1,_d2).fetchall()
            if(len(_q3)!=0):
              for q3 in _q3:
                _l2.append(_r+"-"+str(q3[0]))
            else:
              logger.info(f"Apobado")
              return True
        
        if(len(_l)!=0):
          logger.error(f"Hay alumnos retirados sin registro de fecha de retiro: {str(_l)}")
          logger.error(f"Rechazado")
          return False

        if(len(_l2)!=0):
          logger.error(f"Hay alumnos que registran asistencia anterior a la fecha de ingreso o posterior a la fecha de retiro del establecimiento: {str(_l2)}")
          logger.error(f"Rechazado")
          return False 

      else:
        logger.info(f"No hay registros de alta/baja de alumnos en el establecimiento.")
        logger.info(f"Apobado")
        return True

    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta: {str(e)}")
      logger.error(f"Rechazado")
      return False
### fin fn6D1 ###

### inicio fn6C0 ###
  def fn6C0(self, conn):
    try:
      logger.info(f"fn6C0 - Valida que los alumnos excedentes SIN derecho a pago solo tengan asistencia a nivel de asignatura y NO de curso.")
      _l1 = []
      _s1 = """SELECT c.RUN, A.OrganizationPersonRoleId
                FROM OrganizationPersonRole A
                JOIN Organization B
                ON A.OrganizationId = B.OrganizationId
                JOIN PersonList c
                ON a.personId = c.personId
                JOIN PersonStatus D
                ON A.personId = D.personId
                WHERE A.RoleId = 6
                AND B.RefOrganizationTypeId = 21
                AND D.RefPersonStatusTypeId = 24;"""

      _s2 = """SELECT Date 
                FROM RoleAttendanceEvent
                WHERE OrganizationPersonRoleId = ?;"""

      _q1 = conn.execute(_s1).fetchall()
      if(len(_q1)!=0):
        for q1 in _q1:
          _r = str(q1[0])
          _op = q1[1]
          _q2 = conn.execute(_s2,_op).fetchall()
          if(len(_q2)!=0):
            for q2 in _q2:
              _d = str(q2[0])
              _l1.append(f"Alumno: {str(_r)} - fecha: {str(_d)}")

        if(len(_l1)!=0):
          logger.error(f"Los siguientes alumnos excedentes sin derecho a subvencion tienen registro de asistencia a nivel de curso: {str(_l1)}")
          logger.error(f"Rechazado")
          return False
        else:
          logger.info(f"Apobado")
          return True

      else:
        logger.info(f"No hay registros de alumnos excedentes sin derecho a subvencion en el establecimiento.")
        logger.info(f"Apobado")
        return True

    except Exception as e:
        logger.error(f"NO se pudo ejecutar la consulta de entrega de informaciÓn: {str(e)}")
        logger.error(f"Rechazado")
        return False
### fin fn6C0 ###

### inicio fn6E0 ###
  def fn6E0(self,conn):
    arr=[]
    diaSemana=[]
    numero=0
    try:

      _S3=""" select organizationid from Organization where reforganizationtypeid=22  ;"""

      _S4=""" select ClassMeetingDays,strftime('%H:%M',ClassBeginningTime) as ClassBeginningTime,strftime('%H:%M',ClassBeginningTime) as ClassBeginningTime,  
            ClassPeriod from coursesectionschedule where organizationid=?;"""

      _S5=""" select a.OrganizationPersonRoleId,a.OrganizationId,a.PersonId,a.roleid,strftime('%Y-%m-%d %H:%M',a.EntryDate) as EntryDate, strftime('%Y-%m-%d %H:%M',a.ExitDate) as ExitDate,a.RecordStartDateTime,a.RecordEndDateTime,b.Identifier
                    from  OrganizationPersonRole a 
                    join PersonIdentifier b on a.personId=b.personId  
                    where roleid=6;"""

      _S6=""" select a.OrganizationPersonRoleId,strftime('%Y-%m-%d',b.Date) as Date,b.fileScanbase64,b.observaciones 
                    from OrganizationPersonRole a join RoleAttendanceEvent b on a.OrganizationPersonRoleId= b.OrganizationPersonRoleId
                    where a.OrganizationPersonRoleId= ? and b.Date= ?;"""

      now=datetime.now()
      _q1 = conn.execute(_S3).fetchall()
      XX=0
      if(len(_q1)!=0):
        for q1 in _q1:
          organizationid=str(q1)
          _q2 = conn.execute(_S4,organizationid).fetchall()
          if(len(_q2)!=0):
            for q2 in _q2:
              diaSemana=str(q2[2]).split(",")
              hora_comi=str(q2[3])
              hora_final=str(q2[4])
              periodo=str(q2[5])
              cantidad_letras=int(len(periodo))-1
              periodo2=(periodo[-2:])
              _q3 = conn.execute(_S5).fetchall()
              if(int(periodo2.strip())==2):
                 for q3 in _q3:
                   id_alu=str(q3[8])
                   orgaId=str(q3[0])
                   hora1=str(q3[4])
                   hora2=str(q3[5])
                   dfs=datetime.strptime(hora1[:10],'%Y-%m-%d')
                   nombresemana2=dfs.isoweekday()
                   for aa in diaSemana:
                      if str(aa.lower())=='lunes':
                        numero=0
                      elif str(aa.lower())=='martes':
                        numero=1
                      elif str(aa.lower())=='miercoles': 
                        numero=2
                      elif str(aa.lower())=='jueves':
                        numero=3
                      elif str(aa.lower())=='viernes':
                        numero=4
                      if int(nombresemana2)==int(numero):
                        if datetime.strptime(hora1[11:len(hora1)], '%H:%M')> datetime.strptime(hora_comi[:5], '%H:%M'):
                          _q4 = conn.execute(_S6,orgaId,dfs).fetchall()
                          if(len(_q4)!=0):
                            for q4 in _q4:
                              justi=str(q4[2])
                              obv=str(q4[3])
                              if justi=="None" or obv=="None":
                                arr.append(id_alu)                          
                          else:
                            arr.append(id_alu)  

        if(len(arr)!=0):
          logger.error(f"Los siguientes alumnos llegaron tarde o : {str(arr)} ")
          logger.error(f"Rechazado")
          return False  
        else: 
          logger.info("Aprobado")
          return True        

      else:
        logger.error(f"No hay registro Numero de lista asociados .")
        logger.error(f"Rechazado")
        return False   
    
    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta de entrega de informaciÓn: {str(e)}")
      logger.error(f"Rechazado")
      return False
###  fin fn6E0  ###

### inicio  fn681 ###
  def fn681(self,conn):
    arr=[]
    arr2=[]
    arr3=[]
    dias_laborales=[]
    dias_laborales2=[]
    numero=0
    try:
  
      _S1=""" SELECT OrganizationId
                FROM Organization
                WHERE RefOrganizationTypeId = 47;"""

      _S2=""" SELECT Parent_OrganizationId
                FROM OrganizationRelationship
                WHERE OrganizationId = ?;"""
    
      _S3=""" SELECT OrganizationId
                FROM K12Course
                WHERE OrganizationId = ? and RefWorkbasedLearningOpportunityTypeId=1 ;"""      
                
      _S4=""" select personid 
              from OrganizationPersonRole
              where OrganizationId=? and RoleId = 6 ;"""

      _S5=""" select b.Identifier
              from PersonStatus a 
              join personidentifier b 
              on  a.personid = b.personId  
              where a.RefPersonStatusTypeId=35 and a.personid=? """

      now=datetime.now()
      _q1 = conn.execute(_S1).fetchall()
      XX=0
      if(len(_q1)!=0):
        for q1 in _q1:
          parent=str(q1[0])
          _q2 = conn.execute(_S2,parent).fetchall()
          if(len(_q2)!=0):
            for q2 in _q2:
              parent2=str(q2[0])
              _q3 = conn.execute(_S3,parent2).fetchall()
              if(len(_q3)!=0):
                for q3 in _q3:
                  parent3=str(q3[0])
                  _q4 = conn.execute(_S4,parent3).fetchall()
                  if(len(_q4)!=0):
                    for q4 in _q4:
                      personid=str(q4[0])
                      _q5 = conn.execute(_S5,personid).fetchall()
                      if(len(_q5)==0):
                        rut=str(_q5[0])
                        arr.append(rut)

                    if(len(arr)!=0):
                      logger.error(f"Los siguientes alumnos no tienen identificador de Formacion Dual : {str(arr)} ")
                      logger.error(f"Rechazado")
                      return False
                    else:
                      logger.info(f"Aprobado")
                      return True 
                  
                  else:
                    logger.error(f"No tiene alumnos en la asignatura ")
                    logger.error(f"Rechazado")
                    return False  

              else:
                logger.error(f"La asignatura no esta enlazada para que sea de partica profesional")
                logger.error(f"Rechazado")
                return False      
                    
      else:
        logger.info(f"En el colegio no hay asignaturas de pratica profesional.")
        logger.info(f"Aprobado")
        return True   
    
    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta de entrega de informaciÓn: {str(e)}")
      logger.error(f"Rechazado")
      return False
### fin  fn681 ###

### inicio  fn680 ###
  def fn680(self,conn):
    #arr=[]
    #arr2=[]
    #arr3=[]
    #arr4=[]
    #dias_laborales=[]
    #dias_laborales2=[]
    #dias_laborales3=[]
    #dias_laborales4=[]
    #numero=0
    try:
      _queryText = """
          /*
            6.2 Contenido mínimo, letra c.8 (Alumnos de formación Dual)
            verificar que los registros reportados semanalmente por la empresa se encuentren cargados en el sistema
          */

          SELECT 
            pid.Identifier --idx 0
            ,strftime('%Y-%m-%d', rae.Date) as 'fecha' -- rescata solo la fecha desde rae.Date [idx 1]
            ,strftime('%H:%M', rae.Date, substr(rae.Date,length(rae.Date)-5,6)) as 'hora' -- rescata solo la hora desde rae.Date [idx 2]
            ,CASE 
              WHEN strftime('%w', rae.Date) = '0' THEN 'Domingo'
              WHEN strftime('%w', rae.Date) = '1' THEN 'Lunes'
              WHEN strftime('%w', rae.Date) = '2' THEN 'Martes'
              WHEN strftime('%w', rae.Date) = '3' THEN 'Miercoles'
              WHEN strftime('%w', rae.Date) = '4' THEN 'Jueves'
              WHEN strftime('%w', rae.Date) = '5' THEN 'Viernes'
              WHEN strftime('%w', rae.Date) = '6' THEN 'Sabado'
            END as 'diaSemana' -- rescata solo el dpia de la semana desde rae.Date [idx 3]
            ,rae.fileScanBase64 as 'documentId' --idx 4
            ,rae.observaciones as 'observaciones' --idx 5
          FROM person a 
            JOIN PersonStatus pst
              ON a.personId = pst.personId
              AND pst.RecordEndDateTime IS NULL
              AND pst.RefPersonStatusTypeId IN (
                SELECT RefPersonStatusTypeId
                FROM RefPersonStatusType
                WHERE RefPersonStatusType.Description IN ('Estudiante con formación DUAL')
              )
            JOIN PersonIdentifier pid
              ON a.personId = pid.personId
              AND pid.RecordEndDateTime IS NULL
              AND pid.RefPersonIdentificationSystemId IN (
                SELECT RefPersonIdentificationSystemId
                FROM RefPersonIdentificationSystem
                WHERE RefPersonIdentificationSystem.Code IN ('RUN')
              )		
            JOIN organizationpersonrole opr
              on a.personId = opr.personId 
              AND opr.RecordEndDateTime IS NULL
              AND opr.RoleId IN (
                SELECT RoleId
                FROM Role
                WHERE Role.Name IN ('Estudiante')	
              )			
            JOIN Organization O 
              ON opr.OrganizationId = O.OrganizationId
              AND O.RecordEndDateTime IS NULL
              AND O.RefOrganizationTypeId IN (
                SELECT RefOrganizationTypeId
                FROM RefOrganizationType
                WHERE RefOrganizationType.Description IN ('Asignatura de Practica profesional')				
              )		
            JOIN RoleAttendanceEvent rae
              on opr.OrganizationPersonRoleId = rae.OrganizationPersonRoleId 
              AND rae.RecordEndDateTime IS NULL
            JOIN OrganizationCalendar oc 
              ON O.OrganizationId = oc.OrganizationId
              AND oc.RecordEndDateTime IS NULL
            JOIN OrganizationCalendarSession ocs
              ON oc.OrganizationCalendarId = ocs.OrganizationCalendarId
              AND ocs.RecordEndDateTime IS NULL
            JOIN CourseSectionSchedule css
              ON O.OrganizationId = css.OrganizationId
              AND css.RecordEndDateTime IS NULL		
            JOIN Document doc
              ON rae.fileScanBase64 = doc.documentId
              AND doc.fileScanBase64 IS NOT NULL		
          WHERE 
            -- Verifica que se encuentre cargado el leccionario
            rae.RefAttendanceEventTypeId IN (
              SELECT RefAttendanceEventTypeId
              FROM RefAttendanceEventType
              WHERE RefAttendanceEventType.Code IN ('ClassSectionAttendance')
            )
            AND
            -- Verifica que se encuentre cargado el leccionario
            ocs.Description NOT NULL
            AND
            -- Verifica que el indicador sea True, ya que en estos casos corresponde la relación	
            ocs.AttendanceTermIndicator IN (1)
            AND
            -- Verifica que la firma se encuentre cargada en el sistema
            rae.digitalRandomKey NOT NULL
            AND
            -- Verifica que se haya especificado si es estudiante asiste presencialmente o no.
            rae.VirtualIndicator NOT NULL
            AND
            -- Verifica que día y horario de firma corresponda con calendario de la asignatura
            diaSemana in (css.ClassMeetingDays)
            AND
            hora between css.ClassBeginningTime and css.ClassEndingTime
            AND
            -- Agrega a la lista todos los registros que no cumplan con la expresión regular
            rae.Date REGEXP '^(19|2[0-9])[0-9]{2}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])([T ])(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])(.[0-9]+)?((\\+|-)(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]))$'
            AND
            -- Agrega a la lista todos los registros que no cumplan con la expresión regular
            rae.digitalRandomKeyDate REGEXP '^(19|2[0-9])[0-9]{2}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])([T ])(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])(.[0-9]+)?((\\+|-)(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]))$'
            AND
            -- Agrega a la lista todos los registros que no cumplan con la expresión regular
            rae.digitalRandomKey REGEXP '^[0-9]{6}([-]{1}[0-9kK]{1})?$'
            AND 
            documentId NOT NULL
      """

      #_S1="""select a.personId,strftime('%Y-%m-%d', b.entrydate) as entrydate,strftime('%Y-%m-%d',b.ExitDate) as ExitDate 
      #from person a join organizationpersonrole b on a.personId=b.personId where b.roleid=6 """

      #_S6=""" select strftime('%Y-%m-%d',BeginDate) as BeginDate ,strftime('%Y-%m-%d',EndDate) as EndDate 
      #        from OrganizationCalendarSession Where organizationcalendarsessionid=1"""

      #_S7=""" select c.identifier,a.fileScanBase64 from RoleAttendanceEvent a join organizationpersonrole b on a.OrganizationPersonRoleId=b.OrganizationPersonRoleId 
    #join PersonIdentifier c on b.personid=c.personId where strftime('%Y-%m-%d',a.Date)=? and  a.RefAttendanceEventTypeId=1 and b.personId=?;"""

      #now=datetime.now()
      #_q1 = conn.execute(_S1).fetchall()
      _q1 = conn.execute(_queryText)#.fetchall()
      if(_q1.returns_rows == 0):
        logger.error(f"El establecimientos no tiene alumnos de formación DUAL para revisar")
        logger.error(f"Aprobado")
        return True
      
      _q1 = _q1.fetchall()
      XX=0
      if(len(_q1)!=0):
        # for q1 in _q1:
        #   personid=str(q1[0])
        #   fecha_entrada= str(q1[1]) 
        #   fecha_fin=str(q1[2])
        #   _q6 = conn.execute(_S6).fetchall()
        #   if(len(_q6)!=0):
        #     for q6 in _q6:
        #       fecha_inicio=str(q6[0])
        #       fecha_termino=str(q6[1])

        #       if fecha_fin<fecha_termino:
        #         fecha_ter_x=fecha_fin
        #       else:
        #         fecha_ter_x=fecha_termino

        #       if (fecha_entrada>fecha_inicio): 
        #         arr4=self.ListaFechasRango(fecha_inicio,fecha_ter_x,conn)
        #       else:
        #         arr4=self.ListaFechasRango(fecha_entrada,fecha_ter_x,conn)
                
        #       for xx2 in arr4:
        #         fecha=str(xx2)
        #         fechaxx1=fecha.replace(',','')
        #         fechaxx2=fechaxx1.replace('(','')
        #         fechaxx3=datetime.strptime(fechaxx2[2:12],'%Y-%m-%d')
        #         _q8 = conn.execute(_S7,fechaxx3,personid).fetchall()
        #         if(len(_q8)!=0):
        #           for dd in _q8:
        #             rut=str(dd[0])
        #             obser=str(dd[1])
        #             if obser=="None":
        #               arr.append(rut)
        logger.info(f"Aprobado")
        return True     
    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta de entrega de informaciÓn: {str(e)}")
      logger.error(f"Rechazado")
      return False
### fin  fn680 ###

### inicio fn682 ###
  def fn682(self,conn):
    arr=[]
    arr2=[]
    arr3=[]
    arr4=[]
    dias_laborales=[]
    dias_laborales2=[]
    dias_laborales3=[]
    dias_laborales4=[]
    numero=0
    try:
  
      _S1=""" SELECT OrganizationId
                FROM Organization
                WHERE RefOrganizationTypeId = 47;"""

      _S2=""" SELECT Parent_OrganizationId
                FROM OrganizationRelationship
                WHERE OrganizationId = ?;"""
    
      _S3=""" SELECT OrganizationId
                FROM K12Course
                WHERE OrganizationId = ? and RefWorkbasedLearningOpportunityTypeId=1 ;"""      
                
      _S4=""" select personid from OrganizationPersonRole
        where OrganizationId=? and RoleId = 6 ;"""

      _S5=""" select b.personid,strftime('%Y-%m-%d',c.EntryDate) as EntryDate,strftime('%Y-%m-%d',c.ExitDate) as ExitDate
      from PersonStatus a join personidentifier b on  a.personid = b.personId  join organizationpersonrole c on b.personid=c.personId  where a.RefPersonStatusTypeId=35 and a.personid=? ;"""

      _S6=""" select strftime('%Y-%m-%d',BeginDate) as BeginDate ,strftime('%Y-%m-%d',EndDate) as EndDate 
              from OrganizationCalendarSession Where organizationcalendarsessionid=1;"""
 
      _S7=""" select * from RoleAttendanceEvent a join organizationpersonrole b on a.OrganizationPersonRoleId=b.OrganizationPersonRoleId 
            where strftime('%Y-%m-%d',a.Date)=? and  a.RefAttendanceEventTypeId=1 and b.personId=? ;"""
      
      
      now=datetime.now()
      _q1 = conn.execute(_S1).fetchall()
      XX=0
      if(len(_q1)!=0):
        for q1 in _q1:
          parent=str(q1)
          _q2 = conn.execute(_S2,parent).fetchall()
          if(len(_q2)!=0):
            for q2 in _q2:
              parent2=str(q2)
              _q3 = conn.execute(_S3,parent2).fetchall()
              if(len(_q3)!=0):
                for q3 in _q3:
                  parent3=str(q3)
                  _q4 = conn.execute(_S4,parent3).fetchall()
                  if(len(_q4)!=0):
                    for q4 in _q4:
                      peronid=str(q4)
                      _q5 = conn.execute(_S5,peronid).fetchall()
                      if(len(_q5)!=0):
                        for xx in _q5:
                          personid2=str(xx[0])
                          fecha_entrada=str(xx[1])
                          fecha_fin=str(xx[2]) 
                          _q6 = conn.execute(_S6).fetchall()
                          if(len(_q6)!=0):
                            for xx in _q6: 
                              fecha_inicio=str(xx[0])
                              fecha_termino=str(xx[1])
                              if fecha_fin<fecha_termino:
                                fecha_ter_x=fecha_fin
                              else:
                                fecha_ter_x=fecha_termino
                              if (fecha_entrada>fecha_inicio): 
                                arr=self.ListaFechasRango(fecha_inicio,fecha_ter_x,conn)
                              else:
                                arr=self.ListaFechasRango(fecha_entrada,fecha_ter_x,conn)
                 
                          for xx2 in arr:
                            fecha=str(xx2)
                            fechaxx1=fecha.replace(',','')
                            fechaxx2=fechaxx1.replace('(','')
                            fechaxx3=datetime.strptime(fechaxx2[1:11],'%Y-%m-%d')
                            _q8 = conn.execute(_S7,fechaxx3,personid2).fetchall()
                            if(len(_q8)==0):
                              arr4.append(personid2)

                          if(len(arr4)!=0):
                            logger.error(f"Los siguientes alumnos no tienen asistencia:{str(arr4)}")
                            logger.error(f"Rechazado")
                            return False
                          else:
                            logger.info(f"Aprobado")
                            return True
                  else:
                    logger.error(f"No tiene alumnos en la asignatura ")
                    logger.error(f"Rechazado")
                    return False  

              else:
                logger.error(f"La asignatura no esta enlazada para que sea de partica profesional")
                logger.error(f"Rechazado")
                return False  
                    
      else:
        logger.error(f"En el colegio no asignaturas de pratica profesional    .")
        logger.error(f"Rechazado")
        return False   
    
    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta de entrega de informaciÓn: {str(e)}")
      logger.error(f"Rechazado")
      return False
### fin  fn682  ###

### inicio fn6E1 ###
  def fn6E1(self,conn):
    arr=[]
    diaSemana=[]
    numero=0
    try:
  
      _S3=""" select organizationid from Organization where reforganizationtypeid=22  ;"""

      _S4=""" select * from coursesectionschedule where organizationid=?   ;"""

      _S5=""" select a.OrganizationPersonRoleId,a.OrganizationId,a.PersonId,a.roleid,strftime('%Y-%m-%d %H:%M',a.EntryDate) as EntryDate, strftime('%Y-%m-%d %H:%M',a.ExitDate) as ExitDate,a.RecordStartDateTime,a.RecordEndDateTime,b.Identifier
                    from  OrganizationPersonRole a 
                    join PersonIdentifier b on a.personId=b.personId  
                    where roleid=6;"""

      _S6=""" select a.OrganizationPersonRoleId,strftime('%Y-%m-%d',b.Date) as Date,b.fileScanbase64,b.observaciones 
                    from OrganizationPersonRole a join RoleAttendanceEvent b on a.OrganizationPersonRoleId= b.OrganizationPersonRoleId
                    where a.OrganizationPersonRoleId= ? and b.Date= ?;"""

      now=datetime.now()
      _q1 = conn.execute(_S3).fetchall()
      XX=0
      if(len(_q1)!=0):
        for q1 in _q1:
          organizationid=str(q1[0])
          _q2 = conn.execute(_S4,organizationid).fetchall()
          if(len(_q2)!=0):
            for q2 in _q2:
              diaSemana=str(q2[2]).split(",")
              hora_comi=str(q2[3])
              hora_final=str(q2[4])
              periodo=str(q2[5])
              cantidad_letras=int(len(periodo))-1
              periodo2=(periodo[-2:])
              _q3 = conn.execute(_S5).fetchall()
              if(int(periodo2.strip())==3):
                 for q3 in _q3:
                   id_alu=str(q3[8])
                   orgaId=str(q3[0])
                   hora1=str(q3[4])
                   hora2=str(q3[5])
                   dfs=datetime.strptime(hora1[:10],'%Y-%m-%d')
                   nombresemana2=dfs.isoweekday()
                   for aa in diaSemana:
                      if str(aa.lower())=='lunes':
                        numero=0
                      elif str(aa.lower())=='martes':
                        numero=1
                      elif str(aa.lower())=='miercoles': 
                        numero=2
                      elif str(aa.lower())=='jueves':
                        numero=3
                      elif str(aa.lower())=='viernes':
                        numero=4

                      if int(nombresemana2)==int(numero):
                        if datetime.strptime(hora1[11:len(hora1)], '%H:%M')> datetime.strptime(hora_comi[:5], '%H:%M'):
                          _q4 = conn.execute(_S6,orgaId,dfs).fetchall()
                          if(len(_q4)!=0):
                            for q4 in _q4:
                              justi=str(q4[2])
                              obv=str(q4[3])
                              if justi=="None" or obv== "None":
                                arr.append(id_alu)
                          
                          else:
                            arr.append(id_alu)  


          if(len(arr)!=0):
            logger.error(f"Los siguientes alumnos llegaron tarde o : {str(arr)} ")
            logger.error(f"Rechazado")
            return False
          else:
            logger.info(f"Aprobado")
            return True
      else:
        logger.error(f"No hay registro Numero de lista asociados .")
        logger.error(f"Rechazado")
        return False   
    
    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta de entrega de información: {str(e)}")
      logger.error(f"Rechazado")
      return False
### fin fn6E1  ###

### inicio fn6E4 ### 
  def fn6E4(self,conn):
    try:
      _data = []
      _data = conn.execute("""
                SELECT 
                  org
                  ,group_concat(DISTINCT diasSinClases) as 'diasSinClases'
                FROM (
                  WITH RECURSIVE dates(Organizationid, date) AS (
                    SELECT Organizationid, StartDate
                    FROM OrganizationCalendarCrisis O
                    UNION ALL
                    SELECT Organizationid, date(date, '+1 day')
                    FROM dates
                    WHERE 
                    -- Considera la menor fecha entre LastInstructionDate y la fecha actual (now)
                    strftime('%Y-%m-%d',date) < strftime('%Y-%m-%d', ( 
                      -- Rescata el último día sin actividades producto de la crisis
                      SELECT EndDate 
                      FROM OrganizationCalendarCrisis occ
                      WHERE occ.OrganizationId = Organizationid
                      )
                    ) 
                  )
                  SELECT Organizationid as 'org',  group_concat(date) as 'diasSinClases'
                  FROM dates
                  GROUP BY OrganizationId

                  UNION ALL

                  SELECT oc.Organizationid as 'org', group_concat(oce.EventDate) as 'diasSinClases'
                  FROM OrganizationCalendarEvent oce
                  JOIN OrganizationCalendar oc
                    ON oce.OrganizationCalendarId = oc.OrganizationCalendarId
                  JOIN RefCalendarEventType rcet
                    ON oce.RefCalendarEventType = rcet.RefCalendarEventTypeId
                    AND rcet.Code IN ('EmergencyDay','Holiday','Strike','TeacherOnlyDay')	
                  GROUP BY oc.Organizationid
                ) DSC
                GROUP BY org      
      """).fetchall()
      
      if(not _data):
        logger.error(f"S/DATOS")
        return True        
        
    except:
      logger.error(f"S/DATOS")
      return True        

    try:
      _result = []
      _result = conn.execute("""
--  6.2 Contenido mínimo, letra c.2
-- verificar que se encuentren bien registrados los cambios de actividades al calendario escolar.
-- las tablas OrganizationCalendarEvent y OrganizationCalendarCrisis guardan los casos de suspensión
-- excepcionales de clases, por lo tanto, se debe verificar que existan consistencia entre 
-- la suspensión de clases y las clases realizadas.
-- *** Los días de suspensión no deberían existir registros de clases o asistencias ***

SELECT 
	org
	,group_concat(DISTINCT diasSinClases) as 'diasSinClases'
	,group_concat(DISTINCT clases.inicioClase) as 'diasInicioClases'
	,group_concat(DISTINCT clases.finClase) as 'diasfinClases'
	,group_concat(DISTINCT clases.fechaAsistencia) as 'diasFechaAsistencia'
FROM (
	WITH RECURSIVE dates(Organizationid, date) AS (
	  SELECT Organizationid, StartDate
	  FROM OrganizationCalendarCrisis O
	  UNION ALL
	  SELECT Organizationid, date(date, '+1 day')
	  FROM dates
	  WHERE 
		-- Considera la menor fecha entre LastInstructionDate y la fecha actual (now)
		strftime('%Y-%m-%d',date) < strftime('%Y-%m-%d', ( 
			-- Rescata el último día sin actividades producto de la crisis
			SELECT EndDate 
			FROM OrganizationCalendarCrisis occ
			WHERE occ.OrganizationId = Organizationid
			)
		) 
	)
	SELECT Organizationid as 'org',  group_concat(date) as 'diasSinClases'
	FROM dates
	GROUP BY OrganizationId

	UNION ALL

	SELECT oc.Organizationid as 'org', group_concat(oce.EventDate) as 'diasSinClases'
	FROM OrganizationCalendarEvent oce
	JOIN OrganizationCalendar oc
		ON oce.OrganizationCalendarId = oc.OrganizationCalendarId
	JOIN RefCalendarEventType rcet
		ON oce.RefCalendarEventType = rcet.RefCalendarEventTypeId
		AND rcet.Code IN ('EmergencyDay','Holiday','Strike','TeacherOnlyDay')	
	GROUP BY oc.Organizationid
) DSC
JOIN Organization O
	ON org = O.OrganizationId
JOIN RefOrganizationType rot
	ON rot.RefOrganizationTypeId = O.RefOrganizationTypeId
	AND rot.code IN ('CourseSection')
JOIN (
	SELECT DISTINCT
		 O.OrganizationId
		,ocs.BeginDate||"T"||ifnull(ocs.SessionStartTime,"00:00:00") as 'InicioClase'
		,ocs.EndDate||"T"||ifnull(ocs.SessionEndTime,"00:00:00") as 'finClase'
		,rat.Date as 'fechaAsistencia'
		,rat.digitalRandomKeyDate as 'fechafirma'
		,CASE WHEN (rat.Date BETWEEN ocs.BeginDate||"T"||ifnull(ocs.SessionStartTime,"00:00:00") AND ocs.EndDate||"T"||ifnull(ocs.SessionEndTime,"00:00:00")) THEN 'True' ELSE 'False' END as 'rangoHorarioCorrecto'
		,CASE WHEN (rat.digitalRandomKeyDate BETWEEN ocs.BeginDate||"T"||ifnull(ocs.SessionStartTime,"00:00:00") AND ocs.EndDate||"T"||ifnull(ocs.SessionEndTime,"00:00:00")) THEN 'True' ELSE 'False' END as 'rangoFirmaCorrecto'
	FROM Organization O
	JOIN RefOrganizationType rot
		ON rot.RefOrganizationTypeId = O.RefOrganizationTypeId
		AND rot.code IN ('CourseSection')
	JOIN OrganizationCalendar oc
		ON oc.OrganizationId = O.OrganizationId
		AND oc.RecordEndDateTime IS NULL
	LEFT JOIN OrganizationCalendarSession ocs
		ON ocs.OrganizationCalendarId = oc.OrganizationCalendarId
		AND ocs.AttendanceTermIndicator = 1
		AND ocs.RecordEndDateTime IS NULL
	LEFT JOIN OrganizationPersonRole opr
		ON opr.OrganizationId = O.OrganizationId
		AND opr.RecordEndDateTime IS NULL
	LEFT JOIN RoleAttendanceEvent rat
		ON rat.OrganizationPersonRoleId = opr.OrganizationPersonRoleId
		AND rat.RecordEndDateTime IS NULL
) clases 
	ON clases.OrganizationId = org
	AND (
		(DSC.diasSinClases) LIKE "%" || strftime("%Y-%m-%d",clases.InicioClase) || "%"
		OR
		(DSC.diasSinClases) LIKE "%" || strftime("%Y-%m-%d",clases.finClase) || "%"
		OR
		(DSC.diasSinClases) LIKE "%" || strftime("%Y-%m-%d",clases.fechaAsistencia) || "%"
	)

GROUP BY org      
      """).fetchall()
    except:
      pass
    try:
      if(not _result):
        logger.error(f"Aprobado")
        return True  
      
      organizacionesErrors = []
      fechasSesionesErrors = []
      fechasAsistenciasErrors = []
      
      for row in _result:
        organizacion = row[0]
        fechasSesion = row[2]
        fechasAsistencia = row[4]
        
        if(fechasSesion):
          organizacionesErrors.append(organizacion)
          fechasSesionesErrors.append(fechasSesion)
          
        if(fechasAsistencia):
          organizacionesErrors.append(organizacion)
          fechasAsistenciasErrors.append(fechasAsistencia)
      
      if(fechasAsistenciasErrors):
        logger.error(f"Fechas de asistencia de la tabla roleAttendanceEvent en fechas catalogadas como sin clases: {str(set(fechasAsistenciasErrors))}")
        
      if(fechasSesionesErrors):
        logger.error(f"Fechas de sesiones de la tabla OrganizationCalendarSession en fechas catalogadas como sin clases: {str(set(fechasSesionesErrors))}")

      if(organizacionesErrors):
        logger.error(f"Las siguientes organizaciones estan con problemas: {str(set(organizacionesErrors))}")
        logger.error(f"Rechazado")
        return False
    
    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta de entrega de informaciÓn: {str(e)}")
      logger.error(f"Rechazado")
      return False
### fin  fn6E4 ###

### inicio  fn6C2 ###
  def fn6C2(self,conn):
    arr=[]
    arr2=[]
    arr3=[]
    dias_laborales=[]
    dias_laborales2=[]
    numero=0
    try:
  
      _S3="""
          SELECT 
            pid.identifier
            ,pst.docnumber
            ,pst.filescanbase64
            ,pst.StatusStartDate 
          FROM PersonStatus pst 
            OUTER LEFT JOIN PersonIdentifier pid 
              ON pst.personid = pid.personId
              AND pid.RefPersonIdentificationSystemId  IN (
                SELECT RefPersonIdentificationSystemId 
                FROM RefPersonIdentificationSystem
                WHERE RefPersonIdentificationSystem.description IN ('ROL UNICO NACIONAL')
              )
            OUTER LEFT JOIN RefPersonStatusType rpst
              ON pst.RefPersonStatusTypeId = rpst.RefPersonStatusTypeId
              AND rpst.RefPersonStatusTypeId IN (
                SELECT RefPersonStatusTypeId
                FROM RefPersonStatusType
                WHERE RefPersonStatusType.description IN ('Excedente con derecho a subvención')
              )
            """

      now=datetime.now()
      _q1 = conn.execute(_S3)
      if(_q1.returns_rows == 0):
        logger.error(f"No hay informacion de estudiantes excedentes")
        logger.info(f"S/DATOS")
        return True  
      
      _q1 = _q1.fetchall()
      XX=0
      if(len(_q1)!=0):
        for q1 in _q1:
          rut=str(q1[0])
          filescanbase64=q1[2]
          docnumber=q1[1]
          dateF=q1[3]

          if ((filescanbase64 is None) or (docnumber is None) or (dateF is None)):
            arr.append(rut)

        if(len(arr)!=0):
          logger.error(f"Los siguientes alumnos no tienen Rex de aprobacion : {str(arr)} ")
          logger.error(f"Rechazado")
          return False

        logger.info(f"Aprobado")
        return True      
    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta de entrega de informaciÓn: {str(e)}")
      logger.error(f"Rechazado")
      return False
### fin  fn6C2 ###

### inicio  fn6B0 ###
  def fn6B0(self,conn):
    try:
      _rightList = []
      _rightList = conn.execute("""
	WITH RECURSIVE cte_Attendance (RoleAttendanceEventId, OrganizationPersonRoleId, RUN, Fecha, RecordEndDateTime) AS (
		SELECT 
			 rae.RoleAttendanceEventId
			,rae.OrganizationPersonRoleId
			,pid.Identifier as 'RUN'
			,rae.Date
			,rae.RecordEndDateTime
		FROM RoleAttendanceEvent rae
		JOIN OrganizationPersonRole opr 
			on rae.OrganizationPersonRoleId = opr.OrganizationPersonRoleId 
		JOIN RefAttendanceEventType raet
			ON rae.RefAttendanceEventTypeId = raet.RefAttendanceEventTypeId
			AND raet.Code IN ('DailyAttendance','ClassSectionAttendance')
		JOIN PersonIdentifier pid
			ON opr.personid = pid.personid 
		JOIN RefPersonIdentificationSystem rpis
			ON pid.RefPersonIdentificationSystemId = rpis.RefPersonIdentificationSystemId
			AND rpis.Code IN ('RUN')
		JOIN role rol_e
			ON opr.RoleId = rol_e.RoleId
			AND rol_e.Name IN ('Estudiante')
		WHERE 
			rae.RecordEndDateTime IS NOT NULL
			AND
			rae.RecordStartDateTime IS NOT NULL
			AND
			rae.oprIdRatificador IS NULL
			AND
			rae.firmaRatificador IS NULL
			AND 
			rae.fechaRatificador IS NULL
			AND
            -- Agrega a la lista todos los registros que cumplen con la expresión regular
            rae.Date REGEXP '^(19|2[0-9])[0-9]{2}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])([T ])(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])(.[0-9]+)?((\\+|-)(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]))$'
            AND
            -- Agrega a la lista todos los registros que cumplen con la expresión regular
            rae.digitalRandomKeyDate REGEXP '^(19|2[0-9])[0-9]{2}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])([T ])(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])(.[0-9]+)?((\\+|-)(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]))$'			
		
		UNION ALL

		SELECT 
			rae.RoleAttendanceEventId
			,rae.OrganizationPersonRoleId
			,pid.Identifier as 'RUN'
			,rae.Date, rae.RecordEndDateTime
		FROM RoleAttendanceEvent rae
		JOIN cte_Attendance cte 
			ON cte.RecordEndDateTime = rae.Date
			AND cte.OrganizationPersonRoleId = rae.OrganizationPersonRoleId
			AND rae.RecordStartDateTime IS NOT NULL
		JOIN OrganizationPersonRole opr 
			on rae.OrganizationPersonRoleId = opr.OrganizationPersonRoleId 
		JOIN RefAttendanceEventType raet
			ON rae.RefAttendanceEventTypeId = raet.RefAttendanceEventTypeId
			AND raet.Code IN ('DailyAttendance','ClassSectionAttendance')
		JOIN PersonIdentifier pid
			ON opr.personid = pid.personid 
		JOIN RefPersonIdentificationSystem rpis
			ON pid.RefPersonIdentificationSystemId = rpis.RefPersonIdentificationSystemId
			AND rpis.Code IN ('RUN')		
		JOIN role rol_e
			ON opr.RoleId = rol_e.RoleId
			AND rol_e.Name IN ('Estudiante')
		JOIN OrganizationPersonRole opr_ratificador 
			ON rae.oprIdRatificador = opr_ratificador.OrganizationPersonRoleId 
		JOIN role rol_ratificador
			ON opr_ratificador.RoleId = rol_ratificador.RoleId
			AND rol_ratificador.Name IN ('Encargado de la asistencia','Director(a)')
		WHERE 
			-- Agrega a la lista todos los registros que cumplen con la expresión regular
			rae.Date REGEXP '^(19|2[0-9])[0-9]{2}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])([T ])(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])(.[0-9]+)?((\\+|-)(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]))$'
			AND
			-- Agrega a la lista todos los registros que cumplen con la expresión regular
			rae.digitalRandomKeyDate REGEXP '^(19|2[0-9])[0-9]{2}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])([T ])(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])(.[0-9]+)?((\\+|-)(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]))$'			
            AND
            -- Agrega a la lista todos los registros que cumplen con la expresión regular
            rae.fechaRatificador REGEXP '^(19|2[0-9])[0-9]{2}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])([T ])(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])(.[0-9]+)?((\\+|-)(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]))$'			
            AND
			-- Agrega a la lista todos los registros que no cumplan con la expresión regular
            rae.digitalRandomKey REGEXP '^[0-9]{6}([-]{1}[0-9kK]{1})?$'
            AND
			-- Agrega a la lista todos los registros que no cumplan con la expresión regular
            rae.firmaRatificador REGEXP '^[0-9]{6}([-]{1}[0-9kK]{1})?$'			

	)
	SELECT 
		group_concat(RoleAttendanceEventId) as 'roleAttendanceEventIds'
		,OrganizationPersonRoleId
		,RUN
		,min(Fecha) as 'PRIMERA_FECHA_REGISTRADA'
		,max(fecha) as 'ULTIMA_FECHA_REGISTRADA'
	FROM cte_Attendance 
      """).fetchall()
    except:
      pass

    try:
      _errorsList = []
      _errorsList = conn.execute("""
SELECT *
FROM RoleAttendanceEvent rae
JOIN (
	WITH RECURSIVE cte_Attendance (RoleAttendanceEventId, OrganizationPersonRoleId, RUN, Fecha, RecordEndDateTime) AS (
		SELECT 
			 rae.RoleAttendanceEventId
			,rae.OrganizationPersonRoleId
			,pid.Identifier as 'RUN'
			,rae.Date
			,rae.RecordEndDateTime
		FROM RoleAttendanceEvent rae
		JOIN OrganizationPersonRole opr 
			on rae.OrganizationPersonRoleId = opr.OrganizationPersonRoleId 
		JOIN RefAttendanceEventType raet
			ON rae.RefAttendanceEventTypeId = raet.RefAttendanceEventTypeId
			AND raet.Code IN ('DailyAttendance','ClassSectionAttendance')
		JOIN PersonIdentifier pid
			ON opr.personid = pid.personid 
		JOIN RefPersonIdentificationSystem rpis
			ON pid.RefPersonIdentificationSystemId = rpis.RefPersonIdentificationSystemId
			AND rpis.Code IN ('RUN')
		JOIN role rol_e
			ON opr.RoleId = rol_e.RoleId
			AND rol_e.Name IN ('Estudiante')
		WHERE 
			rae.RecordEndDateTime IS NOT NULL
			AND
			rae.RecordStartDateTime IS NOT NULL
			AND
			rae.oprIdRatificador IS NULL
			AND
			rae.firmaRatificador IS NULL
			AND 
			rae.fechaRatificador IS NULL
			AND
            -- Agrega a la lista todos los registros que cumplen con la expresión regular
            rae.Date REGEXP '^(19|2[0-9])[0-9]{2}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])([T ])(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])(.[0-9]+)?((\\+|-)(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]))$'
            AND
            -- Agrega a la lista todos los registros que cumplen con la expresión regular
            rae.digitalRandomKeyDate REGEXP '^(19|2[0-9])[0-9]{2}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])([T ])(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])(.[0-9]+)?((\\+|-)(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]))$'			
		
		UNION ALL

		SELECT 
			rae.RoleAttendanceEventId
			,rae.OrganizationPersonRoleId
			,pid.Identifier as 'RUN'
			,rae.Date, rae.RecordEndDateTime
		FROM RoleAttendanceEvent rae
		JOIN cte_Attendance cte 
			ON cte.RecordEndDateTime = rae.Date
			AND cte.OrganizationPersonRoleId = rae.OrganizationPersonRoleId
			AND rae.RecordStartDateTime IS NOT NULL
		JOIN OrganizationPersonRole opr 
			on rae.OrganizationPersonRoleId = opr.OrganizationPersonRoleId 
		JOIN RefAttendanceEventType raet
			ON rae.RefAttendanceEventTypeId = raet.RefAttendanceEventTypeId
			AND raet.Code IN ('DailyAttendance','ClassSectionAttendance')
		JOIN PersonIdentifier pid
			ON opr.personid = pid.personid 
		JOIN RefPersonIdentificationSystem rpis
			ON pid.RefPersonIdentificationSystemId = rpis.RefPersonIdentificationSystemId
			AND rpis.Code IN ('RUN')		
		JOIN role rol_e
			ON opr.RoleId = rol_e.RoleId
			AND rol_e.Name IN ('Estudiante')
		JOIN OrganizationPersonRole opr_ratificador 
			ON rae.oprIdRatificador = opr_ratificador.OrganizationPersonRoleId 
		JOIN role rol_ratificador
			ON opr_ratificador.RoleId = rol_ratificador.RoleId
			AND rol_ratificador.Name IN ('Encargado de la asistencia','Director(a)')
		WHERE 
			-- Agrega a la lista todos los registros que cumplen con la expresión regular
			rae.Date REGEXP '^(19|2[0-9])[0-9]{2}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])([T ])(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])(.[0-9]+)?((\\+|-)(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]))$'
			AND
			-- Agrega a la lista todos los registros que cumplen con la expresión regular
			rae.digitalRandomKeyDate REGEXP '^(19|2[0-9])[0-9]{2}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])([T ])(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])(.[0-9]+)?((\\+|-)(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]))$'			
            AND
            -- Agrega a la lista todos los registros que cumplen con la expresión regular
            rae.fechaRatificador REGEXP '^(19|2[0-9])[0-9]{2}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])([T ])(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])(.[0-9]+)?((\\+|-)(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]))$'			
            AND
			-- Agrega a la lista todos los registros que no cumplan con la expresión regular
            rae.digitalRandomKey REGEXP '^[0-9]{6}([-]{1}[0-9kK]{1})?$'
            AND
			-- Agrega a la lista todos los registros que no cumplan con la expresión regular
            rae.firmaRatificador REGEXP '^[0-9]{6}([-]{1}[0-9kK]{1})?$'			

	)
	SELECT 
		group_concat(RoleAttendanceEventId) as 'roleAttendanceEventIds'
		,OrganizationPersonRoleId
		,RUN
		,min(Fecha) as 'PRIMERA_FECHA_REGISTRADA'
		,max(fecha) as 'ULTIMA_FECHA_REGISTRADA'
	FROM cte_Attendance 
) result ON (result.roleAttendanceEventIds) NOT LIKE '%' || rae.RoleAttendanceEventId || '%'
LEFT JOIN OrganizationPersonRole opr 
	on rae.OrganizationPersonRoleId = opr.OrganizationPersonRoleId 
LEFT JOIN RefAttendanceEventType raet
	ON rae.RefAttendanceEventTypeId = raet.RefAttendanceEventTypeId
	AND raet.Code IN ('DailyAttendance','ClassSectionAttendance')
LEFT JOIN role rol_e
	ON opr.RoleId = rol_e.RoleId
	AND rol_e.Name IN ('Estudiante')
WHERE
	rae.RecordEndDateTime IS NOT NULL
	OR
	rae.oprIdRatificador IS NOT NULL
	OR
	rae.firmaRatificador IS NOT NULL
	OR
	rae.fechaRatificador IS NOT NULL
	OR 
	rae.RecordStartDateTime != Date	
      """).fetchall()
    except:
      pass
    try:
      _ids = (list([m[0] for m in _rightList if m[0] is not None]))      
      if(not _errorsList and not _ids):
        logger.info(f"S/DATOS")
        return True

      if(not _errorsList and _ids):
        logger.info(f"APROBADO")
        return True

      roleAttendanceEventIds = (list([m[0] for m in _errorsList if m[0] is not None]))
      logger.error(f"Los siguientes roleAttendanceEvent Ids estan con problemas: {str(roleAttendanceEventIds)}")
      logger.error(f"Rechazado")
      return False
    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta de entrega de informaciÓn: {str(e)}")
      logger.error(f"Rechazado")
      return False
### fin fn6B0 ###

# Lista de fechas rango de rango fechas menos sabado y domingo
  def ListaFechasRango(self,fecha_ini,fecha_ter,conn):
    arr=[]
    arr2=[]
    arr3=[]
    arr4=[]
    arr5=[]
    arr6=[]
    arr7=[]
    _Trae_fechas= """     WITH RECURSIVE dates(date) AS (
                        VALUES (?)
                        UNION ALL
                        SELECT date(date, '+1 day')
                        FROM dates
                        WHERE date < ?
                        )
                        SELECT strftime('%Y-%m-%d',date) as date  FROM dates;"""

    _S3x=""" select strftime('%Y-%m-%d',StartDate) as StartDate , strftime('%Y-%m-%d',EndDate) as EndDate from OrganizationCalendarCrisis;"""  

    _S3x2="""select strftime('%Y-%m-%d',EventDate) as EventDate from OrganizationCalendarevent where strftime('%Y-%m-%d',EventDate)>= ?;""" 
 
    fecha_in=datetime.strptime(fecha_ini,'%Y-%m-%d')
    fecha_te=datetime.strptime(fecha_ter,'%Y-%m-%d')
    logger.info(fecha_in)
    logger.info(fecha_te)
    _q1 = conn.execute(_Trae_fechas,fecha_in,fecha_te).fetchall()
    if(len(_q1)!=0):
      for q1 in _q1:
        fecha=str(q1)
        fechaxx1=fecha.replace(',','')
        fechaxx2=fechaxx1.replace('(','')
        fechaxx3=datetime.strptime(fechaxx2[1:11],'%Y-%m-%d')
        if int(fechaxx3.isoweekday())!=6 : #sabado
          if int(fechaxx3.isoweekday())!=7: #domingo
            arr.append(str(datetime.strftime(fechaxx3,'%Y-%m-%d')))

      arr3=np.array(arr)  
      arr2.append(np.unique(arr3))

    _q2 = conn.execute(_S3x).fetchall()
    if(len(_q2)!=0):
      for q2 in _q2:
        fecha_com=datetime.strptime(q2[0],'%Y-%m-%d')
        fecha_fin=datetime.strptime(q2[1],'%Y-%m-%d')
        _q1 = conn.execute(_Trae_fechas,fecha_com,fecha_fin).fetchall()
        if(len(_q1)!=0):
          for q1 in _q1:
            fecha=str(q1)
            fechaxx1=fecha.replace(',','')
            fechaxx2=fechaxx1.replace('(','')
            fechaxx3=datetime.strptime(fechaxx2[1:11],'%Y-%m-%d')
            if int(fechaxx3.isoweekday())!=6 : #sabado
              if int(fechaxx3.isoweekday())!=7: #domingo
                arr.append(str(datetime.strftime(fechaxx3,'%Y-%m-%d')))

    for ar in arr2:
      dia=datetime.strptime(str(ar[0]),'%Y-%m-%d')
      for ar2 in arr:
        dia2=datetime.strptime(str(ar2),'%Y-%m-%d')
        if dia!=dia2:
          arr4.append(str(datetime.strftime(dia,'%Y-%m-%d')))

    _q3 = conn.execute(_S3x2,fecha_in).fetchall()
    if(len(_q3)!=0):
      for q3 in _q3:  
        fecha=str(q3)
        fechaxx1=fecha.replace(',','')
        fechaxx2=fechaxx1.replace('(','')
        fechaxx3=datetime.strptime(fechaxx2[1:11],'%Y-%m-%d')
        dia=fechaxx3
        for ar in arr4:
          fecha=str(ar)
          fechaxx1=fecha.replace(',','')
          fechaxx2=fechaxx1.replace('(','')
          fechaxx3=datetime.strptime(fechaxx2[0:11],'%Y-%m-%d')
          if dia!=fechaxx3:
            arr5.append(str(datetime.strftime(dia,'%Y-%m-%d')))  

    arr6=np.array(arr5)  
    arr7.append(np.unique(arr6))
    return arr7

### inicio fn6E3 ###
  def fn6E3(self,conn):
    _flag1 = 0
    _flag2 = 0
    try:
      #OBTENGO LAS FECHAS CON SUSPENSION DE CLASES
      _s1 = """SELECT rexNumber,rexDate,fileScanBase64
                FROM OrganizationCalendarEvent
                WHERE indicadorSinClases = 1;"""
      
      _s2="""SELECT rexNumber,rexNumber,fileScanBase64
              FROM OrganizationCalendarSession
              WHERE claseRecuperadaId != NULL;"""

      _q1 = conn.execute(_s1).fetchall()
      if(len(_q1)!=0):
        for q1 in _q1:
          _rexNumber = q1[0]
          _rexDate = q1[1]
          _fsb = q1[2]
          if(_rexNumber is None):
            _msg1 = f"No hay información de resolución ministerial para la suspensión de clases (numero de resolución)"
            _flag1 = 1
          if(_rexDate is None):
            _msg1 = f"No hay información de resolución ministerial para la suspensión de clases (fecha de resolución)"
            _flag1 = 1
          if(_fsb is None):
            _msg1 = f"No hay información de resolución ministerial para la suspensión de clases (documento digitalizado)"
            _flag1 = 1        
      
      else:
        logger.info(f"No hay información en el establecimiento de eventos que impliquen suspensión de clases.")
        logger.info(f"Aprobado")
        return True

      _q2 = conn.execute(_s2).fetchall()
      if(len(_q2)!=0):
        for q2 in _q2:
          _rxn = q2[0]
          _rxd = q2[1]
          _rxfbs = q2[2]
          if(_rxn is None):
            _msg2 = f"No hay información de resolución ministerial para recuperación de clases (numero de resolución)"
            _flag2 = 1
          if(_rxd is None):
            _msg2 = f"No hay información de resolución ministerial para  recuperación de clases (fecha de resolución)"
            _flag2 = 1
          if(_rxfbs is None):
            _msg2 = f"No hay información de resolución ministerial para  recuperación de clases (documento digitalizado)"
            _flag1 = 1  

      else:
        logger.info(f"No hay información en el establecimiento de clases recuperadas.")
        logger.info(f"Aprobado")
        return True

      if(_flag1 == 1):
        logger.error(_msg1)
        logger.error(f"Rechazado")
        return False
      elif(_flag2 == 1):
        logger.error(_msg2)
        logger.error(f"Rechazado")
        return False
      else:
        logger.info(f"Aprobado")
        return True

    except Exception as e:
      logger.error(f"NO se pudo ejecutar la consulta: {str(e)}")
      logger.error(f"Rechazado")
      return False
### fin fn6E3 ###

### MIAULA FIN ###