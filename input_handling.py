import os
#######INPUT ERROR HANDLING

####Especial error types:
class Error(Exception):
    pass

#option not available
class NotInScope(Error):
    pass

#grade input impossible (x<0 or x>10)
class NotPossibleGrade(Error):
    pass

#maxgrade < mingrade
class InvalidMaxGrade(Error):
    pass

class DuplicateParameter(Error):
    pass

class InvalidParameter(Error):
    pass

class InvalidSubjectCode(Error):
    pass

class NotASubject(Error):
    pass

class NoPrereqs(Error):
    pass
####Check for error functions:
def add_prereqs(subjects, prereqs):
    try:
        subject_to_add_prereq = input("Insira o nome da disciplina a qual deseja adicionar o pré-requisito ou ENTER para cancelar.\nEntrada do usuário: ")
        if subject_to_add_prereq is not '':
            if subject_to_add_prereq not in subjects:
                raise NotASubject
            subject_new_prereq = input("Insira o novo pré-requisito para a disciplina ou ENTER para cancelar. \nEntrada do usuário: ")
            if subject_new_prereq is not '':
                if subject_new_prereq not in subjects:
                    raise NotASubject
                prereqs.append(subject_new_prereq)
                prereqs.append(subject_to_add_prereq)
                cls()
                #TODO: Implementar list_prereqs_for_subject()
                print("Pré-requisito adicionado com sucesso.")
            else:
                cls()
                print("Operação cancelada.")
                subject_new_prereq = ''
                pass
        else:
            cls()
            print("Operação cancelada.")
    except NotASubject:
        print("Disciplina não existe")
    except ValueError:
        print("Disciplina inválida")
    return prereqs

def list_prereqs(prereqs, subjects):
    try:
        subject_to_list_prereqs = input('Insira a disciplina á listar os pré-requisitos ou ENTER para cancelar. \nEntrada do usuário: ')
        subject_to_list_prereqs = subject_to_list_prereqs.upper()
        if subject_to_list_prereqs is not '':
            if subject_to_list_prereqs not in subjects:
                raise NotASubject
            if subject_to_list_prereqs not in prereqs:
                raise NoPrereqs
            cls()
            first_occurrence = prereqs.index(subject_to_list_prereqs)
            subject_occurrences = [ i for i in range(len(prereqs)) if prereqs[i] == subject_to_list_prereqs and i%2 != 0]
            x = len(subject_occurrences)-1
            individual_prereqs = []
            while(x>-1):
                individual_prereqs.append(prereqs[subject_occurrences[x]-1])
                x = x -1
            if len(individual_prereqs) != 0:
                print("Pré-requisitos para disciplina "+subject_to_list_prereqs+":\n")
                for i in individual_prereqs:
                    print(i)
                print("\nPré-requisitos listados com sucesso.")
                return individual_prereqs
            else:
                print("Não há pre-requisitos para a disciplina")
        else:
                cls()
                print("Operação cancelada.")

    except ValueError:
        print("Insira um valor válido.")
    except NotASubject:
        print("Disciplina não existe")
    except NoPrereqs:
        print("Não há pré-requisitos para a disciplina")

def edit_turmas(subjects, turmas):
    try:
        subject_to_edit_turmas = input("\n Insira o código da disciplina à alterar as turmas ou ENTER para cancelar.\nEntrada do usuário: ")
        if subject_to_edit_turmas is not '':
            if subject_to_edit_turmas in subjects:
                index_to_edit_turmas = subjects.index(subject_to_edit_turmas)
                new_turmas_qtt = int(input("\n Insira a nova quantidade de turmas para a disciplina: "))
                turmas[index_to_edit_turmas] = new_turmas_qtt
                print("Quantidade de turmas alterada com sucesso. Nova quantidade de turmas para "+str(subject_to_edit_turmas)+": "+str(turmas[index_to_edit_turmas]))
            else:
                print("Disciplina não encontrada.")
    except ValueError:
        print("Valor inválido. Operação cancelada.")
    return subjects, turmas

def del_subject(subjects, turmas, semoffers, credits):
    try:
        subject_removed = input("\nInsira o código da disciplina a ser removida ou ENTER para cancelar.\nEntrada do usuário: ")
        if subject_removed is not '':
            if subject_removed in subjects:
                subject_index = subjects.index(subject_removed)
                turmas.pop(subject_index)
                semoffers.pop(subject_index)
                credits.pop(subject_index)
                subjects.remove(subject_removed)
                print("\n\nDisciplina removida com sucesso.")
            else:
                print("Erro. Disciplina não encontrada.")
        else:
            cls()
            print("Operação cancelada.")
    except ValueError:
        print("Operação inválida.")
    return subjects, turmas, semoffers, credits

def set_new_subject(subjects, turmas, semoffers, credits):
    try:
        new_subject = input("O código da disciplina deve seguir o seguinte padrão. ABXXX sendo AB duas letras quaisquer e XXX 3 números quaisquer. \nInsira o código da disciplina à ser adicionada ou Enter para cancelar.\nEntrada do usuário: ")
        if len(new_subject) != 5:
            raise InvalidSubjectCode
        new_subject = new_subject.upper()
        print(new_subject)
        int(new_subject[-3:])
        if new_subject not in subjects and new_subject is not '':
            no_turmas = int(input("Insira a quantidade de turmas para esta disciplina. \nEntrada do usuário: "))
            semoffer = int(input("Insira o semestre ideal de oferecimento para esta disciplina. \nEntrada do usuário: "))
            qtt_credit = int(input("Insira a quantidade de créditos desta disciplina. \nEntrada do usuário: "))
            subjects.append(new_subject)
            turmas.append(abs(no_turmas))
            semoffers.append(abs(semoffer))
            credits.append(abs(qtt_credit))
            print("Disciplina adicionada com sucesso.")
        elif new_subject in subjects:
            print("Disciplina já cadastrada.")
    except ValueError:
        print("Valor inválido. Operação cancelada.")
    except InvalidSubjectCode:
        print("Código de disciplina inválido. Operação cancelada.")
    return subjects, turmas, semoffers, credits

def set_new_parameter(params):
    try:
        new_param_name = input("Insira o nome do novo parâmetro ou ENTER para cancelar.\n\n Entrada do usuário: ")
        if new_param_name not in params and new_param_name is not '':
            new_param_min = input("Nota mínima: ")
            float(new_param_min)
            new_param_max = input("Nota máxima: ")
            float(new_param_max)
            new_param_qtd = input("Qtde de alunos: ")
            int(new_param_qtd)
            params.append(new_param_name)
            params.append(float(new_param_min))
            params.append(float(new_param_max))
            params.append(int(new_param_qtd))
            print("Parametros foram adicionados.\n")
            print(params)
        elif new_param_name in params:
            raise DuplicateParameter
        else:
            cls()
            print("Operação cancelada")
    except DuplicateParameter:
        cls()
        print("Este parâmetro já existe")
    except ValueError:
        cls()
        print("Valor inserido inválido")
    return params

def del_parameter(params):
    try:
        removed_param_name = input("Insira o nome do parâmetro à ser removido ou enter para cancelar.\n\nEntrada do Usuário: ")
        if removed_param_name not in params and removed_param_name is not '':
            raise InvalidParameter
        elif removed_param_name is '':
            print("Operação cancelada.")
        elif removed_param_name in params:
            rm_index = [i for i, x in enumerate(params) if x == str(removed_param_name)]
            print(rm_index[0])
            params.pop(rm_index[0]+3)
            params.pop(rm_index[0]+2)
            params.pop(rm_index[0]+1)
            params.pop(rm_index[0])
            cls()
            print("Parâmetro removido com sucesso.")
    except InvalidParameter:
        cls()
        print("Parâmetro não existe.")
    return params

def change_parameter(params):
    try:
        altered_param_name = input("Insira o nome do parâmetro à ser alterado ou enter para cancelar. \n\nEntrada do usuário: ")
        if altered_param_name not in params and altered_param_name is not '':
            raise InvalidParameter
        elif altered_param_name is '':
            print("Operação cancelada.")
        elif altered_param_name in params:
            cls()
            print("Parâmetro encontrado.")
            rm_index = [i for i, x in enumerate(params) if x == str(altered_param_name)]
            paramindex = rm_index[0]
            param_new_name = input("Insira o novo nome para o parâmetro ou ENTER para manter o nome.\nEntrada do usuário: ")
            param_new_min = input("Insira a nova nota mínima para o parâmetro ou -1 para mantê-la.\nEntrada do usuário: ")
            float(param_new_min)
            param_new_max = input("Insira a nova nota máxima para o parâmetro ou -1 para mantê-la.\nEntrada do usuário: ")
            float(param_new_max)
            param_new_std = input("Insira a nova quantidade de alunos para o parâmetro ou -1 para mantê-la.\nEntrada do usuário: ")
            int(param_new_std)
            ## gravando alterações
            if param_new_name is not '':
                params[paramindex] = param_new_name
            if float(param_new_min) != -1.0:
                params[paramindex+1] = float(param_new_min)
            if float(param_new_max) != -1.0:
                params[paramindex+2] = float(param_new_max)
            if int(param_new_std) != -1:
                params[paramindex+3] = int(param_new_std)
    except ValueError:
        print("Valor inválido. Operação cancelada.")
    except InvalidParameter:
        print("Parâmetro não existe.")
    return params



def check_input_in_scope (a,b,user_input):
    try:
        menu_input = int(user_input)
        if menu_input < a or menu_input > b:
            raise NotInScope
    except NotInScope:
        new_param_checklist = 1
        print("Insira uma opção válida")
        ask_for_input_to_Continue()
    except ValueError:
        new_param_checklist = 1
        print("Insira uma opção válida")
        ask_for_input_to_Continue()
    return
########

#check for int between params
def check_for_int(a):
    try:
        menu_input = int(a)
    except ValueError:
        new_param_checklist = 1
        print("Insira uma opção válida!")
    return


def ask_for_input_to_Continue():
    try:
        input("Pressione qualquer tecla para continuar.")
    except SyntaxError:
        pass
    return


def cls():
    os.system('cls' if os.name=='nt' else 'clear')
