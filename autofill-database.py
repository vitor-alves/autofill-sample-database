import psycopg2
import random
import time
from faker import Factory

######################### CONFIGS - EDIT THIS ###################
DBName = 'mc536'
DBUser = 'postgres'
DBPassword = ''
Host = 'localhost'

#################### GLOBAL ##################
startTime = time.time()
fake = Factory.create('pt_BR')
CPFMedicosInseridos = []
CPFPacientesInseridos = []

########################### GENERATE FUNCTIONS ##################################
def strTimeProp(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(format, time.localtime(ptime))

def randomDate(start, end, prop):
    return strTimeProp(start, end, '%d-%m-%Y', prop)

def genNome():
    return fake.name()

def genCPF():
    cpf = "%0.11d" % random.randint(0,999999999999)
    return cpf

def genDepartamento():
    listaDepartamentos = ['Pronto Atendimento', 'Sala de Recuperação', 'UCI', 'UTI Adulto', 'UTI Infantil', 'Instituto de Diagnóstico por Imagem'] 
    departamento = random.choice(listaDepartamentos)
    return departamento

def genEspecialidade():
    listaEspecialidades = ['Dermatologia', 'Acupuntura', 'Endocrinologia', 'Oftalmologia', 'Cardiologia', 'Psiquiatria', 'Homeopatia']
    especialidade = random.choice(listaEspecialidades)
    return especialidade

def genDataNascimento(tipo):
    if(tipo == 'medico'):
        data =  randomDate("1-1-1990", "1-1-1934", random.random())
    else:
        data =  randomDate("1-1-2016", "1-1-1924", random.random())
    return data

def genLogradouro():
    return fake.address()

def genGenero():
    listaGeneros = ['M', 'F']
    genero = random.choice(listaGeneros)
    return genero

def genTipoSangue():
    listaSangue = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB-', 'AB+']
    sangue = random.choice(listaSangue)
    return sangue

def genSeguroSaude():
    listaSeguro = ['Unimed', 'Zurich', 'Liberty', 'None']
    seguro = random.choice(listaSeguro)
    if(seguro == 'None'):
        return None
    else:
        return seguro

def genDoador():
    listaDoador = ['Coração', 'Fígado', 'Rim', 'Pulmão', 'None']
    doador = random.choice(listaDoador)
    if(doador == 'None'):
        return None
    else:
        return doador

def genTelefone():
    return fake.phone_number()

def genDetalhes():
    return fake.text(300)

def genNomeRemedio():
    fakeLocal = Factory.create('it_IT')
    return fakeLocal.last_name()

def genFabricante():
    fakeLocal = Factory.create('en_US')
    return fakeLocal.last_name()

def genEfeitosColaterais():
    listaEfeitos = ['Náusea', 'Tontura', 'Aumento do metabolismo', 'Dor de cabeça', 'Sono']
    efeito = random.choice(listaEfeitos)
    return efeito

def genIndicacoes():
    listaIndicacoes = ['Dor de cabeca', 'Dor muscular', 'Hipovitaminose A', 'Fatiga']
    indicacao = random.choice(listaIndicacoes)
    return indicacao

def genDataExameAnamnese():
    return randomDate("1-1-2017", "1-1-2005", random.random())

def genNomeExame():
    listaNomeExames = ['Urina', 'Eletrocardiograma', 'Raio X', 'Tomografia']
    exame = random.choice(listaNomeExames)
    return exame

def genResultadoExame():
    return fake.text(100)

def genNomeTratamento():
    listaNomesTratamento = ['Cirurgia', 'Repouso', 'Transplante']
    tratamento = random.choice(listaNomesTratamento)
    return tratamento

def genDescricao():
    return fake.text(50)

def genInicio():
    return randomDate("1-1-2017", "1-1-2005", random.random())

def genTermino(inicio):
    return randomDate(inicio, '1-1-2017', random.random())

def genNomeDiagnostico():
    return fake.text(20)

def genCausas():
    listaCausas = ['Hipovitaminose D', 'Falta de ferro']
    causa = random.choice(listaCausas)
    return causa

def genSintomas():
    listaSintomas = ['Falta de apetite', 'Palidez', 'Pressão baixa']
    sintoma = random.choice(listaSintomas)
    return sintoma

################################ INSERT FUNCIONS ####################################
def insertMedicos():
    f = open('queriesInsertMedicos.txt', 'w')
    for i in range(0,10):
        cur = conn.cursor()
        commandString = "insert into MEDICO values(%s, %s, %s, %s, %s) returning CPF_MEDICO"
        cur.execute(commandString, (genCPF(), genNome(), genEspecialidade(), genDepartamento(), genDataNascimento('medico')))
        f.write(cur.query.decode('utf-8') + "\n")
        CPF_medico = cur.fetchone()[0]
        CPFMedicosInseridos.append(CPF_medico)
    f.close()

def insertPacientes():
    f = open('queriesInsertPacientes.txt', 'w')
    for i in range(0,2000):
        cur = conn.cursor()
        commandString = "insert into PACIENTE values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning CPF_PACIENTE"
        cur.execute(commandString, (genCPF(), genNome(), genLogradouro(), genGenero(), genDataNascimento('paciente'), genTipoSangue(), 
            genSeguroSaude(), genDoador(), genNome(), genTelefone()))
        f.write(cur.query.decode('utf-8') + "\n")
        CPF_paciente = cur.fetchone()[0]
        CPFPacientesInseridos.append(CPF_paciente)
    f.close()

def insertAnamnese():
    f = open('queriesInsertAnamnese.txt', 'w')
    for i in range(0, 4000):
        CPFMedico = random.choice(CPFMedicosInseridos)
        cur = conn.cursor()
        commandString = "insert into ANAMNESE(CPF_medico, data_da_realizacao, detalhes) values(%s, %s, %s)"
        cur.execute(commandString, (CPFMedico, genDataExameAnamnese(), genDetalhes()))
        f.write(cur.query.decode('utf-8') + "\n")
    f.close()

def insertRemedio():
    f = open('queriesInsertRemedio.txt', 'w')
    for i in range(0,100):
        cur = conn.cursor()
        commandString = "insert into REMEDIO(nome, fabricante, efeitos_colaterais, indicacoes) values(%s, %s, %s, %s)"
        cur.execute(commandString, (genNomeRemedio(), genFabricante(), genEfeitosColaterais(), genIndicacoes()))
        f.write(cur.query.decode('utf-8') + "\n")
    f.close()

def insertExame():
    f = open('queriesInsertExame.txt', 'w')
    for i in range(0,1500):
        CPFMedico = random.choice(CPFMedicosInseridos)
        CPFPaciente = random.choice(CPFPacientesInseridos)
        cur = conn.cursor()
        commandString = "insert into EXAME(nome, CPF_medico, CPF_paciente, data_da_realizacao, resultado) values(%s, %s, %s, %s, %s)"
        cur.execute(commandString, (genNomeExame(), CPFMedico, CPFPaciente, genDataExameAnamnese(), genResultadoExame()))
        f.write(cur.query.decode('utf-8') + "\n")
    f.close()

def insertTratamento():
    f = open('queriesInsertTratamento.txt', 'w')
    for i in range(0, 200):
        CPFMedico = random.choice(CPFMedicosInseridos)
        CPFPaciente = random.choice(CPFPacientesInseridos)
        inicio = genInicio()
        cur = conn.cursor()
        commandString = "insert into TRATAMENTO(nome, descricao, CPF_medico, CPF_paciente, inicio, termino) values(%s, %s, %s, %s, %s, %s)"
        cur.execute(commandString, (genNomeTratamento(), genDescricao(), CPFMedico, CPFPaciente, inicio, genTermino(inicio)))
        f.write(cur.query.decode('utf-8') + "\n")
    f.close()

def insertDiagnostico():
    f = open('queriesInsertDiagnostico.txt', 'w')
    for i in range(0, 1600):
        CPFPaciente = random.choice(CPFPacientesInseridos)
        cur = conn.cursor()
        commandString = "insert into DIAGNOSTICO(nome, causas, sintomas, CPF_paciente) values(%s, %s, %s, %s)"
        cur.execute(commandString, (genNomeDiagnostico(), genCausas(), genSintomas(), CPFPaciente))
        f.write(cur.query.decode('utf-8') + "\n")
    f.close()

################################# CREATE TABLE FUNCTIONS #####################

def createTableMedico():
    commandString = "CREATE TABLE medico ( CPF_medico varchar(25), nome character varying(50), especialidade character varying(50), departamento character varying(50), data_de_nascimento date, PRIMARY KEY (CPF_medico) );"
    cur = conn.cursor()
    try:
        cur.execute(commandString)
        f = open('queriesCreateTable.txt', 'w')
        f.write(commandString+'\n')
        f.close()
    except:
        pass

def createTablePaciente():
    commandString = "CREATE TABLE paciente ( CPF_paciente varchar(25), nome character varying(50), logradouro character varying(150), genero character(2), data_de_nascimento date, tipo_de_sangue character varying(3), seguro_de_saude character varying(50), doador varchar(100), nome_de_parente character varying(50), telefone_de_parente varchar(25), PRIMARY KEY (CPF_paciente) );"
    cur = conn.cursor()
    try:
        cur.execute(commandString)
        f = open('queriesCreateTable.txt', 'a')
        f.write(commandString+'\n')
        f.close()
    except:
        pass

def createTableAnamnese():
    commandString = "CREATE TABLE Anamnese ( ID_Anamnese serial, CPF_medico varchar(25), data_da_realizacao date, detalhes varchar(500), PRIMARY KEY (ID_anamnese), FOREIGN KEY (CPF_medico) REFERENCES medico(CPF_medico) );"
    cur = conn.cursor()
    try:
        cur.execute(commandString)
        f = open('queriesCreateTable.txt', 'a')
        f.write(commandString+'\n')
        f.close()
    except:
        pass

def createTableRemedio():
    commandString = "CREATE TABLE Remedio ( ID_Remedio serial, nome character varying(50), fabricante character varying(50), efeitos_colaterais character varying(200), indicacoes character varying(200), PRIMARY KEY (ID_remedio) );"
    cur = conn.cursor()
    try:
        cur.execute(commandString)
        f = open('queriesCreateTable.txt', 'a')
        f.write(commandString+'\n')
        f.close()
    except:
        pass

def createTableExame():
    commandString = "CREATE TABLE Exame ( ID_exame serial, nome character varying(50), CPF_medico varchar(25), CPF_paciente varchar(25), data_da_realizacao date, resultado character varying(200), PRIMARY KEY (ID_exame), FOREIGN KEY (CPF_medico) REFERENCES medico(CPF_medico), FOREIGN KEY (CPF_paciente) REFERENCES paciente(CPF_paciente) );"
    cur = conn.cursor()
    try:
        cur.execute(commandString)
        f = open('queriesCreateTable.txt', 'a')
        f.write(commandString+'\n')
        f.close()
    except:
        pass

def createTableTratamento():
    commandString = "CREATE TABLE Tratamento ( ID_tratamento serial, nome character varying(50), descricao character varying(200), CPF_medico varchar(25), CPF_paciente varchar(25), inicio date, termino date, PRIMARY KEY (ID_tratamento), FOREIGN KEY (CPF_medico) REFERENCES medico(CPF_medico), FOREIGN KEY (CPF_paciente) REFERENCES paciente(CPF_paciente) );"
    cur = conn.cursor()
    try:
        cur.execute(commandString)
        f = open('queriesCreateTable.txt', 'a')
        f.write(commandString+'\n')
        f.close()
    except:
        pass

def createTableDiagnostico():
    commandString = "CREATE TABLE Diagnostico ( ID_diagnostico serial, nome character varying(50), causas character varying(200), sintomas character varying(200), CPF_paciente varchar(25), PRIMARY KEY (ID_diagnostico), FOREIGN KEY (CPF_paciente) REFERENCES paciente(CPF_paciente) );"
    cur = conn.cursor()
    try:
        cur.execute(commandString)
        f = open('queriesCreateTable.txt', 'a')
        f.write(commandString + '\n')
        f.close()
    except:
        pass

################################### MAIN PROGRAM ###################################
try:
    conn = psycopg2.connect("dbname="+DBName+" user="+DBUser+" host="+Host+" password="+DBPassword)
except Exception as e:
    print(e)

createTableMedico()
conn.commit()
createTablePaciente()
conn.commit()
createTableAnamnese()
conn.commit()
createTableRemedio()
conn.commit()
createTableExame()
conn.commit()
createTableTratamento()
conn.commit()
createTableDiagnostico()
conn.commit()

insertMedicos()
insertPacientes()
insertAnamnese()
insertRemedio()
insertExame()
insertTratamento()
insertDiagnostico()
conn.commit()

print("Finished in %s seconds" % (time.time() - startTime)) 
