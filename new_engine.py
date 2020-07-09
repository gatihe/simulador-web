import pandas as pd
import numpy as np
import random
import os
import time
import datetime
from xml.dom import minidom
import xml.etree.ElementTree as ET
from input_handling import *
import webbrowser

#defining parameters
bast_param = [0,5] #ba prefix for below average student
avst_param = [5,7] #av prefix for average student
aast_param = [7,10] #aa prefix for above average student
sorted_sabotage = [3, 3]
semoffers = []
cat_info = []
hard_passes = []
easy_passes = []
anos_inicio = []
#defining parameters 2
menu_keep = 0
params = ["Below Average", 0, 5, 10, "Average", 5, 7, 10, "Above Average", 7, 10, 10]
params_total = len(params)/4
factors = []
students_data = []
tempo_max_integralizacao = 12
ja_simulou = 0
ja_importou = 0
importou_config = 0
real_final_tool_export = []
subs_final_export = []
export_to_tool = []


#Defining Subjects
subjects = ["EB101", "SI100", "SI120", "SI201", "SI250"]

credits = [4,4,4,4,4]

turmas = [1,2,1,2,3]



casos_esporadicos_sorteados = [3, 0, 0, 10] #1 semestre, 1a materia, 0 = ruim (descrescimo na nota)

students = []

prereqs = ["SI100", "SI250"]

def scrambled(orig):
    dest = orig[:]
    random.shuffle(dest)
    return dest


def exporting_to_tool(simulation_array, qtde_de_disciplinas_semestre_par,qtde_de_disciplinas_semestre_impar, subss):
    tool_export_line = []
    tool_export_full = []
    subs_export_line = []
    real_final_tool_export = []
    #getting all subjects
    novo_contador_de_semestre = 1
    novo_index_inicial_do_semestre = 0
    novo_index_final_do_semestre = -1
    novo_contador_de_semestre = 1
    inicio_semestre = 0
    fim_semestre = 0

    while (novo_contador_de_semestre<=tempo_max_integralizacao):
        novo_index_inicial_do_semestre = novo_index_final_do_semestre + 1
        if novo_contador_de_semestre % 2 == 0:
            novo_index_final_do_semestre = novo_index_final_do_semestre + (qtde_de_disciplinas_semestre_par * 3) #3 = APENAS NOTA POR ISSO 1
        if novo_contador_de_semestre % 2 != 0:
            novo_index_final_do_semestre = novo_index_final_do_semestre + (qtde_de_disciplinas_semestre_impar * 3)
        inicio_semestre = novo_index_inicial_do_semestre
        fim_semestre = novo_index_final_do_semestre
        while (inicio_semestre <= fim_semestre ):
            subs_export_line.append(subss[inicio_semestre+1]+"_"+str(novo_contador_de_semestre))
            inicio_semestre = inicio_semestre + 3
        novo_contador_de_semestre = novo_contador_de_semestre + 1

    #passing all grades to array
    l = 0
    c = 1
    while (l < len(students)):
        c = 1
        tool_export_line = []
        while(c<len(subss)):
            tool_export_line.append(simulation_array[l][c])
            c = c + 3
        tool_export_full.append(tool_export_line)
        l = l+1
    #cleaning subs with no students:
    final_tool_export = np.array(tool_export_full)
    column_to_check = []
    c = 0
    l = 0
    no_students = 0
    columns_to_delete = []
    by_columns = []
    while(c<len(tool_export_full[0])):
        l = 0
        column_to_check = []
        while(l<len(students)):
            column_to_check.append(tool_export_full[l][c])
            l = l+1
        by_columns.append(column_to_check)
        c = c +1

    subs_as_np = np.array(subs_export_line)
    l = 0
    c = 0

    while(l<len(by_columns)):
        if all(isinstance(item, str) for item in by_columns[l]) is True and by_columns[l][0] == '--':
            columns_to_delete.append(l)
        l = l+1
    subs_final_export = np.delete(subs_as_np, columns_to_delete)
    real_final_tool_export = np.delete(final_tool_export, columns_to_delete, 1)
    l = 0
    c = 0
    while(l<len(students)):
        c = 0
        while(c<len(subs_final_export)):
            if real_final_tool_export[l][c] == '--':
                real_final_tool_export[l][c] = ''
            else:
                real_final_tool_export[l][c] = float(real_final_tool_export[l][c])
            c = c+1
        l = l+1

    return real_final_tool_export, subs_final_export


def sorteio_de_turmas_dificeis_e_faceis(subjects, tempo_max_integralizacao, even_semester, odd_semester):
    #define how many subjects
    vetor_a_ser_retornado = []


    #sortear um numero de 0 até 10
    qtde_ocorrencias = random.randint(0,10)
    #cont 0 à 10:
    cont = 0
    while(cont<qtde_ocorrencias):
        materia_sorteada = subjects[random.randint(0,len(subjects)-1)]
        vetor_a_ser_retornado.append(materia_sorteada)
        if materia_sorteada in even_semester:
            semestre_sorteado = random.randrange(2, tempo_max_integralizacao +1, 2)
        if materia_sorteada in odd_semester:
            semestre_sorteado = random.randrange(1, tempo_max_integralizacao +1, 2)
        vetor_a_ser_retornado.append(semestre_sorteado)
        vetor_a_ser_retornado.append(random.randint(0,1))
        cont = cont+1
        #sortear um num de 0 até len(subjects)
        #sortear um numero par ou impar
        #sortear entre 0 e 1

    #decide wheter its good (0) or bad (1)



    #turmas_sorteadas = ['EB101', 1, 1, 'EB101', 3, 0, 'EB102', 2, 1]
    return vetor_a_ser_retornado

def sorteio_altera_desempenho(students):
    alunos_alteracao_desempenho = []
    #sortear um numero de alunos < students
    #sortear um semestre de inicio e um semestre de fim para a melhora do desempenho
    #buscar alunos
    qtde_students = random.randint(0, len(students))
    affected_students = random.sample(students, qtde_students)

    alunos_alteracao_desempenho.append(qtde_students)
    for student in affected_students:
        alunos_alteracao_desempenho.append(student)
        alunos_alteracao_desempenho.append(random.randint(0,1))
        alunos_alteracao_desempenho.append(random.randint(2,6))

    return alunos_alteracao_desempenho

def getting_subjects_config_from_file(filename):
    parsed_subjects = []
    tree = ET.parse(filename)
    root = tree.getroot()
    parsed_subjects = []
    for config_param in root.findall('subjects'):
        for subject in config_param.findall('subject'):
            for id in subject.findall('id'):
                parsed_subjects.append(id.text)
    return parsed_subjects

def getting_catalog_info_from_file(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    parsed_cat_info = []
    for cat in root.findall('cat_info'):
        for course_id in cat.findall('course_id'):
            parsed_cat_info.append(int(course_id.text))
        for year in cat.findall('year'):
            parsed_cat_info.append(int(year.text))
        for max_years in cat.findall('max_years'):
            parsed_cat_info.append(int(max_years.text))
    return parsed_cat_info


def export_subjects(subjects,credits, cat_info):
    tpds = []
    j = 0
    while(j<len(subjects)):
        info_line = []
        tpds.append(info_line)
        info_line.append(subjects[j])
        info_line.append(cat_info[1])
        info_line.append(credits[j])
        info_line.append('N')
        j = j+1
    return tpds

def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct

def rank_students(crs_list):
    return positions

def export_student_data(students, tempo_max_integralizacao, qtde_de_disciplinas_semestre_impar, qtde_de_disciplinas_semestre_par, simulation_array, subss, subjects, credits, generic_config_info, cat_info):
    l = 0
    students_data = []
    while (l<len(students)):
        c = 1
        ind_student_data = []
        ind_student_data.append(students[l])
        ind_student_data.append(0)
        novo_index_inicial_do_semestre = 0
        novo_index_final_do_semestre = -1
        novo_contador_de_semestre = 1
        inicio_semestre = 0
        fim_semestre = 0
        while (novo_contador_de_semestre<=tempo_max_integralizacao):
            novo_index_inicial_do_semestre = novo_index_final_do_semestre + 1
            if novo_contador_de_semestre % 2 == 0:
                novo_index_final_do_semestre = novo_index_final_do_semestre + (qtde_de_disciplinas_semestre_par * 3) #3 = TURMA, NOTA, FREQ
            if novo_contador_de_semestre % 2 != 0:
                novo_index_final_do_semestre = novo_index_final_do_semestre + (qtde_de_disciplinas_semestre_impar * 3)
            inicio_semestre = novo_index_inicial_do_semestre
            fim_semestre = novo_index_final_do_semestre
            while (inicio_semestre <= fim_semestre ):
                if simulation_array[l][inicio_semestre] != '--':
                    ind_student_data.append(subss[inicio_semestre+1])
                    ind_student_data.append(simulation_array[l][inicio_semestre+1])
                    ind_student_data.append(simulation_array[l][inicio_semestre+2])
                    ind_student_data.append(novo_contador_de_semestre)
                    #print(credits[subjects.index(subss[inicio_semestre+1])])
                    ind_student_data.append(credits[subjects.index(subss[inicio_semestre+1])])
                inicio_semestre = inicio_semestre + 3
            novo_contador_de_semestre = novo_contador_de_semestre + 1
        students_data.append(ind_student_data)
        l = l +1
    crs, med_crs, desv_padrao = calc_std_crs(students_data)

    info_std = []
    individual_info_std = []
    l = 0
    while(l<len(students_data)):
        creditos_cursados = 0
        individual_info_std = []
        m = 0
        total_creditos_curso = 0
        while (m<len(credits)):
            total_creditos_curso = total_creditos_curso + credits[m]
            m = m +1
        j = 2


        #crp
        individual_cr = crs[crs.index(students_data[l][j-2])+1]
        individual_crp = ((individual_cr - med_crs)/desv_padrao)


        individual_info_std.append(students_data[l][j-2]) #RA                  (0)
        individual_info_std.append(generic_config_info[0]) #ANOING             (1)
        individual_info_std.append(2) #PINGR POR ENQUANTO SERA 2               (2)
        individual_info_std.append(cat_info[1]) #DANOCAT = ANOCATALOGO         (3)
        individual_info_std.append(cat_info[0]) #numero do CURSO               (4)
        individual_info_std.append(generic_config_info[0]) #ANOING             (5)
        individual_info_std.append(cat_info[1]) #ANO_CATALOGO = ANOCATALOGO    (6)
        individual_info_std.append(round(crs[crs.index(students_data[l][j-2])+1],3)) #CR - VAI SER CALCULADO DEPOIS           (7)
        individual_info_std.append(0) #CP -           (8)
        individual_info_std.append(0) #CP FUTURO  (9)
        individual_info_std.append(crs[crs.index(students_data[l][j-2])-1]) #POSICAO_ALUNO_NA_TURMA(10)
        individual_info_std.append(round(individual_crp,3)) #CR PADRAO - VAI SER CALCULADO DEPOIS    (11)
        individual_info_std.append(round(med_crs,3)) #CR MEDIO - VAI SER CALCULADO DEPOIS    (12)
        individual_info_std.append(round(desv_padrao,3)) #DESVIO_PADRAO_TURMA                     (13)
        individual_info_std.append(len(students))  #TOTAL_ALUNOS_TURMA         (14)
        while(j<len(students_data[l])):
            if students_data[l][j+1] >= 5 and students_data[l][j+2] >= 65:
                creditos_cursados = creditos_cursados + students_data[l][j+4]
            j = j+5
        individual_info_std[8] = round(creditos_cursados/total_creditos_curso,3)
        individual_info_std[9] = round(creditos_cursados/total_creditos_curso,3)
        info_std.append(individual_info_std)
        l = l+1

    return info_std, students_data

def calc_desvio_padrao():
    return desvio_padrao




def calc_cr(std_data):
    teste = get_students_records(students_data)
    print(teste)
    return teste

def calc_stdinfo(subjects, students, gradeslc, subss):
    j = 0
    stdinfo = []
    while j < len(students):
        i = 0
        while i < len(subss):

            i = i+1
        j = j+1
    return stdinfo

    #for x in root[0]: # access each subject
        #parsed_subjects.append(x[0].text) # every x is an element. 0 refers to the first element.


def getting_turmas_config_from_file(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    parsed_turmas = []
    for config_param in root.findall('subjects'):
        for subject in config_param.findall('subject'): # access each subject
            individual_qtde_turmas = subject.findall('classes_no')
            for x in individual_qtde_turmas:
                parsed_turmas.append(int(x.text))
    return parsed_turmas

def getting_credits_config_from_file(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    parsed_credits = []
    for config_param in root.findall('subjects'):
        for subject in config_param.findall('subject'): # access each subject
            individual_qtde_credits = subject.findall('credits')
            for x in individual_qtde_credits:
                parsed_credits.append(int(x.text))
    return parsed_credits

def getting_semoffer_config_from_file(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    parsed_semoffers = []
    for config_param in root.findall('subjects'):
        for subject in config_param.findall('subject'): # access each subject
            individual_semoffer = subject.findall('sem_offer')
            for x in individual_semoffer:
                parsed_semoffers.append(int(x.text))
    return parsed_semoffers

def getting_prereqs_config_from_file(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    parsed_prereqs = []
    for config_param in root.findall('subjects'):
        for subject in config_param.findall('subject'):
            individual_parsed_prereq = subject.findall('pre_reqs')
            individual_parsed_subject_id = subject.findall('id')
            for x in individual_parsed_prereq:
                    if x.text is not None:
                        #prereq to add is equal to pre_reqs tag's text inside the current subject being parsed
                        parsed_prereqs.append(x.text)
                        #subject[0].text is equal to subject id
                        parsed_prereqs.append(individual_parsed_subject_id[0].text)
    #print(parsed_prereqs)
    return parsed_prereqs

def getting_prereq_report_from_file(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    parsed_anos_inicio = []
    report_prereqs = []
    for config_param in root.findall('subjects'):
        for subject in config_param.findall('subject'):

            individual_parsed_ano_inicio = subject.findall('ano_inicio')
            individual_parsed_ano_fim = subject.findall('ano_fim')
            individual_parsed_subject_id = subject.findall('id')
            individual_parsed_tipo_nivel_ativ_mae = subject.findall('tipo_nivel_atividade_mae')
            individual_parsed_prerequinho = subject.findall('pre_reqs')
            individual_parsed_cadeia_prereqs = subject.findall('no_cadeia_pre_requisito')
            individual_parsed_tipo_prereq = subject.findall('tipo_pre_requisito')
            individual_parsed_tipo_nivel_atividade_exigida = subject.findall('tipo_nivel_atividade_exigida')
            for (x,y,z,w,v, u) in zip(individual_parsed_prerequinho, individual_parsed_ano_inicio, individual_parsed_ano_fim, individual_parsed_cadeia_prereqs, individual_parsed_tipo_prereq, individual_parsed_tipo_nivel_atividade_exigida):
                    if x.text is not None:
                        parsed_anos_inicio = []
                        #subject[0].text is equal to subject id
                        parsed_anos_inicio.append(individual_parsed_tipo_nivel_ativ_mae[0].text)
                        parsed_anos_inicio.append(individual_parsed_subject_id[0].text)
                        #prereq to add is equal to ano_inicio tag's text inside the current subject being parsed
                        parsed_anos_inicio.append(y.text)
                        if z.text == '0':
                            parsed_anos_inicio.append('')
                        else:
                            parsed_anos_inicio.append(z.text)
                        parsed_anos_inicio.append(w.text)
                        parsed_anos_inicio.append(v.text)
                        parsed_anos_inicio.append(x.text)
                        parsed_anos_inicio.append(u.text)
                        report_prereqs.append(parsed_anos_inicio)

    #print(parsed_anos_inicio)
    return report_prereqs


def getting_hard_pass_from_file(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    parsed_hard_pass = []
    for config_param in root.findall('subj_dificulty'):
        for hp in config_param.findall('hard_pass'):
            individual_hp = hp.findall('sub_id')
            for x in individual_hp:
                    if x.text is not None:
                        #prereq to add is equal to pre_reqs tag's text inside the current subject being parsed
                        parsed_hard_pass.append(x.text)
    return parsed_hard_pass

def getting_easy_pass_from_file(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    parsed_easy_pass = []
    for config_param in root.findall('subj_dificulty'):
        for hp in config_param.findall('easy_pass'):
            individual_ep = hp.findall('sub_id')
            for x in individual_ep:
                    if x.text is not None:
                        #prereq to add is equal to pre_reqs tag's text inside the current subject being parsed
                        parsed_easy_pass.append(x.text)
    return parsed_easy_pass

def getting_params_config_from_file(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    parsed_params = []
    for config_param in root.findall('parameters'):
        for parameter in config_param.findall('parameter'):
            individual_parameter_name = parameter.findall('parameter_name')
            parsed_params.append(individual_parameter_name[0].text)
            individual_parameter_min_grade = parameter.findall('min_grade')
            parsed_params.append(float(individual_parameter_min_grade[0].text))
            individual_parameter_max_grade = parameter.findall('max_grade')
            parsed_params.append(float(individual_parameter_max_grade[0].text))
            individual_parameter_qtde_alunos = parameter.findall('qtde')
            parsed_params.append(int(individual_parameter_qtde_alunos[0].text))
    return parsed_params

def getting_factors_config_from_file(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    parsed_factors = []
    for config_factor in root.findall('factors'):
        easy_pass_factor = config_factor.findall('easy_pass_factor')
        parsed_factors.append(float(easy_pass_factor[0].text))
        hard_pass_factor = config_factor.findall('hard_pass_factor')
        parsed_factors.append(float(hard_pass_factor[0].text))
    return parsed_factors

def getting_generic_info_from_file(filename):
        tree = ET.parse(filename)
        root = tree.getroot()
        parsed_info = []
        for generic_info in root.findall('generic_info'):
            ano_ingresso = generic_info.findall('ano_ingresso')
            parsed_info.append(int(ano_ingresso[0].text))
        return parsed_info

def listar_parametros():
    p = 0
    q = 0
    print('Parâmetros configurados:\n')
    while(p<len(params)/4):
        while(q < len(params)):
            print("Parametro: " + str(params[q]))
            q = q +1
            print("Mínimo: " + str(params[q]))
            q = q +1
            print("Máximo: " + str(params[q]))
            q = q+1
            print("Qtde de alunos: " + str(params[q])+"\n\n")
            q = q+1
        p = p + 1
    return

def listar_disciplinas():
    print("Disciplinas cadastradas:\n")
    for x in subjects:
        print(x)
    print("\n")
    return

def ask_for_input_to_Continue():
    try:
        input("Pressione qualquer tecla para continuar.")
    except SyntaxError:
        pass
    return

def get_students_records(students_data, generic_config_info):
    #EXPORT STUDENTS RECORDS
    all_records = []
    individual_grade_on_record = []
    j = 0
    while(j< len(students_data)):
      m = 2
      while(m<len(students_data[j])):
        individual_grade_on_record = []
        individual_grade_on_record.append(students_data[j][0]) #0
        individual_grade_on_record.append(int(generic_config_info[0]+(students_data[j][m+3]/2))) #1
        individual_grade_on_record.append(students_data[j][m+3])#2
        individual_grade_on_record.append(students_data[j][m])#3
        individual_grade_on_record.append(students_data[j][m+1])#4
        individual_grade_on_record.append(students_data[j][m+2])#5
        if students_data[j][m+1] >= 5 and students_data[j][m+2] >= 65:
            individual_grade_on_record.append(4)#6
        if students_data[j][m+1] < 5 and students_data[j][m+2] >= 65:
            individual_grade_on_record.append(5)#6
        if students_data[j][m+2] < 65:
            individual_grade_on_record.append(6)#6
        if individual_grade_on_record[6] == 4:
            individual_grade_on_record.append("APROVADO POR NOTA/CONCEITO E FREQ")
        if individual_grade_on_record[6] == 5:
            individual_grade_on_record.append("REPROVADO POR NOTA/CONCEITO")
        if individual_grade_on_record[6] == 6:
            individual_grade_on_record.append("REPROVADO POR FREQUENCIA")
        individual_grade_on_record.append(1)
        individual_grade_on_record.append(students_data[j][m+4])
        individual_grade_on_record.append('REGULAR')
        all_records.append(individual_grade_on_record)
        m = m+5
      j = j+1
    return all_records

def calc_std_crs(std_data):
    l = 0
    std_total_credits = 0
    std_total_grades = 0
    nici = 0
    contador = 0
    std_crs = []
    pure_crs = [] #somente crs para poder calclar o desvio padrao da turma
    while(l<len(std_data)):
        c = 2
        while(c<len(std_data[l])):
            individual_nici = 0
            std_total_credits = std_total_credits + std_data[l][c+4]
            std_total_grades = std_total_grades + std_data[l][c+1]
            individual_nici = std_data[l][c+1] * std_data[l][c+4]
            contador = contador + 1
            nici = nici + individual_nici
            c = c+5

        cr = round(nici/(10*std_total_credits),3)
        std_crs.append(std_data[l][0])
        std_crs.append(cr)
        pure_crs.append(cr)
        l = l+1


    to_rank = std_crs
    positions = []
    counter = 1
    while (len(to_rank)>1):
        c = 1
        stored_highest_value = 0
        stored_highest_index = 0
        while (c<len(to_rank)):
            if stored_highest_value < to_rank[c]:
                stored_highest_value = to_rank[c]
                stored_highest_index = c
            c = c +2
        positions.append(counter)
        positions.append(std_crs[stored_highest_index-1])
        positions.append(stored_highest_value)
        to_rank.pop(stored_highest_index)
        to_rank.pop(stored_highest_index-1)
        counter = counter+1

#cr medio da turma
    m = 2
    crs_sum = 0
    instances = 0
    while(m<len(positions)):
        crs_sum = crs_sum+positions[m]
        instances = instances+1
        m = m+3

    med_crs = crs_sum/instances

    desv_padrao = np.std(pure_crs)
    desv_padrao = desv_padrao
    return positions, med_crs, desv_padrao


#counters and variable for grades creation
a = 0
b = 0
newgradeline = []
grade = []

#cut is the min grade to be aproved
cut = 5
even_semester = []
odd_semester = []

def check_for_prereq(subject_to_check, prereqs_list):
    cont1 = 0
    prereqs_for_subject = []
    while (cont1 < len(prereqs_list)):
        if prereqs_list[cont1] == subject_to_check and cont1 % 2 != 0:
            prereqs_for_subject.append(prereqs_list[cont1 - 1])
        cont1 = cont1 + 1
    return prereqs_for_subject

def arrange_semesters(subjects, semoffers, even_semester, odd_semester):
    i = 0
    j = 0
    even_semester.clear()
    odd_semester.clear()
    for i, j in zip(semoffers, subjects):
        if i % 2 == 0:
            even_semester.append(j)
        if i % 2 != 0:
            odd_semester.append(j)
    return


def sort_turmas(subjects, turmas):
    sub = 0
    run_turma = 0
    subs_with_turmas = []
    subs_with_turmas.clear()
    while (sub < len(subjects)):
        subs_with_turmas.append('Turma')
        subs_with_turmas.append(subjects[sub])
        subs_with_turmas.append('Freq')
        sub = sub +1
    return subs_with_turmas

def check_prereqs_are_ok(disciplinas, already_passed): #if 1 ok if 0 not ok
    counter = 0
    ok_or_not = 1
    while(counter<len(disciplinas)):
        if disciplinas[counter] not in already_passed:
            ok_or_not = 0
    return ok_or_not

def sort_sab_rec(students):
    sorted_sab_rec = []
    sort_students = random.randint(1,int(len(students)/3))
    cont = 0
    while (cont < sort_students):
        individual_sorted_student = random.randint(0,len(students)-1)
    return sorted_sab_rec



def new_simulation():



    ################ IMPORTACOES
    ja_simulou = 1
    filename1 = 'default_config.xml'
    if filename1 is not '':
        try:
            f=open('imports/uploads/configs.xml')
            params = getting_params_config_from_file('imports/uploads/configs.xml')
            factors = getting_factors_config_from_file('imports/uploads/configs.xml')
            hard_passes = getting_hard_pass_from_file('imports/uploads/configs.xml')
            easy_passes = getting_easy_pass_from_file('imports/uploads/configs.xml')
            generic_config_info = getting_generic_info_from_file('imports/uploads/configs.xml')
            importou_config = 1
        except SyntaxError:
            print("\nProblema identificado ao importar. Verifique seu arquivo "+filename1+".")
            pass
        except IOError:
            print("\nProblema identificado ao importar. Verifique seu arquivo "+filename1+".")
            pass
    else:
        print("\nImportação de parâmetros cancelada.")


    filename = 'si_cat_2020.xml'
    if filename is not '':
        try:
            f=open('imports/uploads/catalogo.xml')
            subjects = getting_subjects_config_from_file('imports/uploads/catalogo.xml')
            turmas = getting_turmas_config_from_file('imports/uploads/catalogo.xml')
            prereqs = getting_prereqs_config_from_file('imports/uploads/catalogo.xml')
            semoffers = getting_semoffer_config_from_file('imports/uploads/catalogo.xml')
            credits = getting_credits_config_from_file('imports/uploads/catalogo.xml')
            cat_info = getting_catalog_info_from_file('imports/uploads/catalogo.xml')
            prereq_report = getting_prereq_report_from_file('imports/uploads/catalogo.xml')
            ja_importou = 1
        except SyntaxError:
            print("\nProblema identificado ao importar. Verifique seu arquivo "+filename+".")
            pass
        except IOError:
            print("\nProblema identificado ao importar. Verifique seu arquivo "+filename+".")
            pass

    else:
        print("\nImportação de catálogo cancelada.")



        ################ SIMULACAO

    arrange_semesters(subjects, semoffers, even_semester, odd_semester)
    max_years = 6
#intercalando semestres pra criar grade de ofertas
    all_subs = []
    all_subs.clear()
    i = 0
    while (i < 6):
        for odd_sem in odd_semester:
            all_subs.append(odd_sem)
        for even_sem in even_semester:
            all_subs.append(even_sem)
        i = i+1
    #print(all_subs)
    subss = []
    subss.clear()
    subss = sort_turmas(all_subs, turmas)
    sub = 0
    turm = 0
    sab_rec = []
    subjects_with_turmas = []
    while(sub < len(subjects)):
        if turmas[sub] == 1:
            subjects_with_turmas.append(subjects[sub])
        else:
            turm = 0
            strturma = 65
            while (turm < turmas[sub]):
                subjects_with_turmas.append(subjects[sub] + ' '+chr(strturma))
                strturma = strturma + 1
                turm = turm + 1
        sub = sub+1


    grade.clear()
    students.clear()
    params_sort = [x for x in params if not isinstance(x, str)]
    st_total = 0
    st = 3
    while(st < len(params)):
        total = params[st]
        st_total = st_total + total
        st = st + 4
    #creating students and grades
#counter for students ids creation
    i = 0
    j = 2

    while(i < st_total):
        newstudent = random.randint(100000,199999)
        #excluding duplicates
        if newstudent not in students:
            students.append(newstudent)
            i = i+1
    #now grades
    while(j<len(params_sort)):
        a = 0
        while(a < params_sort[j]):
            b = 0
            newgradeline = []
            grade.append(newgradeline)
            while(b < len(subss)):
                #gen_grade = round(random.uniform(params_sort[j-2],params_sort[j-1]),2)
                gen_grade = -1
                newgradeline.append(gen_grade)
                b = b +1
            a = a +1
        j = j + 3

    sort_sub = ['EB101']


    m = 0
    subj_credits = []
    subj_credits.clear()
    while(m<len(subjects)):
        subj_credits.append(subjects[m])
        subj_credits.append(credits[m])
        m = m+1

    k = 0
    l = 0
    c = 0

#emptying values and sorting turmas
    l = 0



    while(l < len(students)):
        c = 0
        while (c < len(subss)):
            if subss[c] in subjects:
                turminha = subjects.index(subss[c])
                sorteio_de_turma = 0
                turma_sorteada = random.randint(0,turmas[turminha]-1)
                turma_sorteada = turma_sorteada + 65
                grade[l][c-1] = chr(turma_sorteada)
            c = c + 1
        l = l+1

    #identificar o que é um semestre na linha, manter primeiros
    #applying prereqs
    l = 0
    c = 0
    creditos_do_semestre = 0
    max_creditos = 28
    grades_to_handle = []
    already_passed = []
    handled_grades = []
    pendentes = []
    qtde_de_disciplinas_semestre_par = len(even_semester)
    qtde_de_disciplinas_semestre_impar = len(odd_semester)
    qtde_itens_na_disciplina = 8 #nome, turma, nota, creditos, semestre de oferta, liberado
    creditos_atuais = 0
    semestre_atual = []
    tempo_max_integralizacao = 12
    line = []
    alldata = []
    vetordeteste = [1,5,10,1,0,6]
    outrovetordeteste = []
    tpds = []




    easy_hard_subjects = sorteio_de_turmas_dificeis_e_faceis(subjects, tempo_max_integralizacao, even_semester, odd_semester)

    meuteste2 = sorteio_altera_desempenho(students)

    aui = 2
    while(aui < len(params_sort)):
        aue = 0
        while(aue<params_sort[aui]):
            outrovetordeteste.append(params_sort[aui-2])
            outrovetordeteste.append(params_sort[aui-1])
            aue = aue + 1
        aui = aui + 3

    contest = 0
    #ra_somacreditos_disc = []



    while(contest<len(outrovetordeteste)):
        l = 0
        while(l<len(students)):
            #ra_somacreditos_disc.clear()
            #ra_somacreditos_disc.append(students[l]) #adicionando o ra do aluno ao vetor
            #ra_somacreditos_disc.append(0) # ra_somacreditos_disc[1] armazena a soma de creditos totais feitos
            index_inicial_do_semestre = 0
            index_final_do_semestre = -1
            inicio_semestre = 0
            contador_de_semestre = 1
            line.clear()
            pendentes.clear()
            c = 1
            already_passed.clear()
            sc_index = 0
            grades_to_handle.clear()
            while(c<len(subss)):
                pendentes.append(subss[c]) #nome
                pendentes.append(grade[l][c-1]) #turma
                pendentes.append(grade[l][c]) #nota
                sc_index = subj_credits.index(subss[c]) ##creditos
                pendentes.append(subj_credits[sc_index+1]) ##creditos
                if subss[c] in even_semester:
                    pendentes.append(2) #semestre de oferta, 1 impar, 2 par
                else:
                    pendentes.append(1)
                pendentes.append(1) #liberado para fazer ou não: 0 não (setup inicial), 1 sim
                pendentes.append(-1) #freq
                pendentes.append(10) #PARA SORTEAR QUEDA OU ALTA DE RENDIMENTO TEMPORÁRIA
                c = c +3
            ####\/ \/ \/ \/ VETOR PARA CONFIGURAR TUDO ESTA CRIADO, MAGICA ACONTECE LOGO ABAIXO \/ \/ \/ \/ CONFIRA:
            ## TRATAR VETOR PENDENTES
            j = 0
            instancias_eb101 = [i for i,d in enumerate(pendentes) if d=='EB101']
            instancias_eb102 = [i for i,d in enumerate(pendentes) if d=='EB102']
            while(contador_de_semestre<=tempo_max_integralizacao):
                index_inicial_do_semestre = index_final_do_semestre + 1
                if contador_de_semestre % 2 == 0:
                    index_final_do_semestre = index_final_do_semestre + (qtde_de_disciplinas_semestre_par * qtde_itens_na_disciplina)
                if contador_de_semestre % 2 != 0:
                    index_final_do_semestre = index_final_do_semestre + (qtde_de_disciplinas_semestre_impar * qtde_itens_na_disciplina)

                #percorrer pendentes inclusas no semestre do contador do semestre
                inicio_semestre = index_inicial_do_semestre
                fim_semestre = index_final_do_semestre
                semestre_atual.clear()
                #dividindo ofertas por semestre
                while(inicio_semestre<=fim_semestre):
                    semestre_atual.append(pendentes[inicio_semestre])
                    inicio_semestre = inicio_semestre + 1
                #bloqueando disciplinas que faltam prereqs ou que o aluno ja foi aprovado
                cont_sub = 0
                #somente bloqueando as que já foram feitas
                while(cont_sub<len(semestre_atual)):
                    if semestre_atual[cont_sub] in already_passed:
                        semestre_atual[cont_sub + 5] = 0
                    cont_sub = cont_sub +8
                #somente bloquando as que tem prereq nao cumprido
                cont_sub = 0
                while(cont_sub<len(semestre_atual)):
                    individual_prereqs = check_for_prereq(semestre_atual[cont_sub], prereqs)
                    if (len(individual_prereqs)>0):
                        novo_contador = 0
                        while(novo_contador<len(individual_prereqs)):
                            if individual_prereqs[novo_contador] not in already_passed:
                                semestre_atual[cont_sub+5] = 0
                            novo_contador = novo_contador + 1
                    cont_sub = cont_sub + 8

                creditos_atuais = 0
                cont_sub = 0
                while(cont_sub<(len(semestre_atual))):
                    test_creditos = 0
                    freq_instance = 100
                    if creditos_atuais + semestre_atual[cont_sub+3] < max_creditos and semestre_atual[cont_sub+5] == 1:
                        creditos_atuais = creditos_atuais+semestre_atual[cont_sub+3]
                        #sorteando nota
                        # print('parametros agora:')
                        # print(outrovetordeteste[contest])
                        # print(outrovetordeteste[contest+1])
                        #criar vetor [ra, somacreditos, disciplina, nota, disciplina, nota, disciplina, nota
                        #ra_somacreditos_disc.append(semestre_atual[cont_sub])
                        freq_instance = round(freq_instance - random.uniform(0,40),2)
                        materia_a_buscar_turmas = subjects.index(semestre_atual[cont_sub])
                        semestre_atual[cont_sub+1] = chr(int(random.uniform(0,turmas[materia_a_buscar_turmas])+65))
                        semestre_atual[cont_sub+6] = freq_instance
                        semestre_atual[cont_sub+2] = round(random.uniform(outrovetordeteste[contest],outrovetordeteste[contest+1]),2)

                        if semestre_atual[cont_sub] in hard_passes:
                            semestre_atual[cont_sub+2] = round(semestre_atual[cont_sub+2] - random.uniform(0,factors[1]),2)
                        if semestre_atual[cont_sub] in easy_passes:
                            semestre_atual[cont_sub+2] = round(semestre_atual[cont_sub+2] + random.uniform(0,factors[0]),2)


                        #turmas dificeis esporadicas
                        #ESSE TRECHO VAI PEGAR O VETOR [DISCIPLINA, SEMESTRE, DISCIPLINA, SEMESTRE E alterar a nota em um range de 1 à 3]
                        ## CASOS ESPORADICOS USANDO FUNCAO sorteio_de_turmas_dificeis_e_faceis()
                        if semestre_atual[cont_sub] in easy_hard_subjects: #[EB101,1, 0, EB101, 3, 1]
                            instancias_disciplina = [i for i,d in enumerate(easy_hard_subjects) if d==semestre_atual[cont_sub]]
                            new_counter = 0
                            while(new_counter < len(instancias_disciplina)):
                                if(contador_de_semestre == easy_hard_subjects[instancias_disciplina[new_counter]+1]):
                                    if easy_hard_subjects[instancias_disciplina[new_counter]+2] == 1:
                                        semestre_atual[cont_sub + 2] = round(semestre_atual[cont_sub + 2] - random.uniform(1,3),2)
                                    if easy_hard_subjects[instancias_disciplina[new_counter]+2] == 0:
                                        semestre_atual[cont_sub +2] = round(semestre_atual[cont_sub + 2] + random.uniform(1,3),2)
                                new_counter = new_counter+1

                        ## se for um aluno sorteado pra ter alteração no desempenho, zerar nota nos semestres sorteados


                        if freq_instance < 65:
                            semestre_atual[cont_sub+2] = 0
                        #treating < 0 and > 10
                        if semestre_atual[cont_sub+2] < 0:
                            semestre_atual[cont_sub+2] = -1
                        if semestre_atual[cont_sub+2] > 10:
                            semestre_atual[cont_sub+2] = 10
                        if semestre_atual[cont_sub+2] >= 5:
                            already_passed.append(semestre_atual[cont_sub])
                            semestre_atual[cont_sub+5] = 0

                    cont_sub = cont_sub + 8


                count_line = 0
                while (count_line<len(semestre_atual)):
                    line.append(semestre_atual[count_line + 1])
                    alldata.append(semestre_atual[count_line + 1])
                    line.append(semestre_atual[count_line + 2])
                    alldata.append(semestre_atual[count_line + 2])
                    line.append(semestre_atual[count_line+6])
                    count_line = count_line + 8

                contador_de_semestre = contador_de_semestre + 1
            l = l+1

        ## PEGAR PENDENTES E DEVOLVER PRAS NOTAS NORMAIS
        holder = 0
        while(holder<len(line)):
            tpds.append(line[holder])
            holder = holder +1
        contest = contest + 2
    l = 0

    #tirando -1 e turmas sem ter feito materia
    jua = 1
    while(jua<len(tpds)):
        if tpds[jua] == -1:
            tpds[jua] = '--'
            tpds[jua-1] = '--'
        jua = jua + 1


    #repassando tudo
    position = 0
    lensub = len(subss)
    while (l < len(students)):
        grade[l] = tpds[position:position+len(subss)]
        position = position + lensub
        l = l+1

    simulation = pd.DataFrame (scrambled(grade),index=students, columns=subss)
    ja_simulou = 1
    simulation_array = simulation.values.tolist()
    test = np.array(simulation_array)


    if len(simulation)>0:
        oteste, students_data = export_student_data(students, tempo_max_integralizacao, qtde_de_disciplinas_semestre_impar, qtde_de_disciplinas_semestre_par, simulation_array, subss, subjects,credits, generic_config_info, cat_info)
        osrecords = get_students_records(students_data, generic_config_info)
        real_final_tool_export, subs_final_export = exporting_to_tool(simulation_array, qtde_de_disciplinas_semestre_par,qtde_de_disciplinas_semestre_impar, subss)


        prereqs_report_export = pd.DataFrame(prereq_report, columns = ['TIPO_NIVEL_ATIVIDADE_MAE', "DISCIPLINA", "ANO_INICIO", "ANO_FIM", "NO_CADEIA_PRE_REQUISITO", "TIPO_PRE_REQUISITO", "DISCIPLINA_EXIGIDA", "TIPO_NIVEL_ATIVIDADE_EXIGIDA"])
        std_records = pd.DataFrame (osrecords, columns=['RA', 'ANO', 'PERIODO', 'DISCIPLINA', 'NOTA', 'FREQUENCIA', 'SITUACAO', 'DESCRICAO_SITUACAO','CURRICULARIDADE', "CREDITO_DISCIPLINA", 'COMO_FOI_CURSADA'])
        std_info_export = pd.DataFrame (oteste,index=students, columns=['RA', 'ANOING', 'PINGR', 'DANOCAT', 'CURSO', 'ANO_INGRESSO', 'ANO_CATALOGO', 'CR', 'CP', 'CP_FUTURO', 'POSICAO_ALUNO_NA_TURMA', 'COEFICIENTE_RENDIMENTO_PADRAO', 'COEFICIENTE_RENDIMENTO_MEDIO', 'DESVIO_PADRAO_TURMA', 'TOTAL_ALUNOS_TURMA'])


    return simulation, simulation_array, tempo_max_integralizacao, qtde_de_disciplinas_semestre_impar, qtde_de_disciplinas_semestre_par, subss, students_data, prereqs_report_export, std_records, std_info_export

####running ,,
