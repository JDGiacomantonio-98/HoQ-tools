sample_preferences = {}

def main():

    print('Welcome to the QFD helper tool for prioritaising the Custom Requirements your team highlighted during the assessment\n')
    print("Let's start by SETTING UP THE CUSTOMER REQUIREMENTS ...")

    c_req = set_labels()
    if c_req is None:
        return 

    sel = input('\nHow do you want to run the procedure?\n[1] Run interviews\n[2] Use a pre-existing collection of answers\n\nchoose from the menu : ')
    while sel not in ('1, 2'):
        print('** error : please pick an option from the menu')
        sel = input('\nHow do you want to run the procedure?\n[1] Run interviews\n[2] Use a pre-existing collection of answers\n\nchoose from the menu : ')

    if sel == '1':
        results = analyze(run_interviews(set_partecipants(), c_req))
    else:   
        print('this feature will be released soon!')
        return None

    print('\n++++++++ [ RESULTS ] ++++++++\n')
    print('id\tdescr\tabsolute importance [1-5]')

    for i, cr in enumerate(c_req):
        cr.append(results[0][i])
        print(f'CR{cr[0]}\t{cr[1]}\t{cr[2]}')

    if input('\nDo you want to print the preference distribution of each survied customer? (y/n) ') in ('y','Y'):
        print('\n')
        for i, prf in enumerate(sample_preferences.values()):
            pref_order = '( '
            for j, x in enumerate(prf.values()):
                if j <= 4 and len(x) != 0:
                    if pref_order != '( ':
                        pref_order += ' > ( '
                    if len(x) > 1:
                        for k, y in enumerate(x):
                            pref_order += f'CR{y} = ' if k+1 < len(x) else f'CR{y} )'
                    else:
                        pref_order += f'CR{x[0]} )'
            print(f'ID{i+1}:\t{pref_order}')

def set_labels():
    cr_labels = []
    i = 0

    print('\n*** Customer Requirement labels section ***\n')
    sel = input('How do you want to continue?\n[1] Insert Customer Requirements manually\n[2] Use a pre-existing Customer Requirements table\n\nchoose from the menu : ')
    while sel not in ('1, 2'):
        print('** error : please pick an option from the menu')
        sel = input('How do you want to continue?\n[1] Insert Customer Requirements manually\n[2] Use a pre-existing Customer Requirements table\n\nchoose from the menu : ')
    if sel == '1':
        while input(f'{f"Press ENTER to insert the first C.R. label ... " if i == 0 else "press ENTER to insert the next label or write <f> to close this section ... "}') not in ('f','F'):
            i += 1
            cr_labels.append([i, input(f'****> C.R.{i} label: ').lower()])
        while i < 2:
            print('error: the procedure requires at least 2 Customer Requirement to be identified.')
            while (input('\npress ENTER to upload the next label or write <f> to close this section: ') not in ('f','F')) or i < 2:
                i += 1
                cr_labels.append([i, input(f'C.R.{i} label: ').lower()])

        return cr_labels
    else:   
        print('this feature will be released soon!')
        return None

def set_partecipants():

    n = input('Please set how many people will partecipate to the survey: ')
    while not(n.isdigit()):
        print('Error: insert a numeric value')
        n = input('How many people will partecipate to the survey: ')

    return int(n)


def run_interviews(partecipants, survey_items):
    survey_ans = {}

    for p in range(partecipants):
        ans = []

        print('\n--------------------------------------------------------------------------------------------\n')
        print(f'Hello partecipant n.{p+1}! We will ask you a series of questions about our product lineup.\n')
        print('Your answers will have tremendous impacts on the final product desing. Thanks for helping us!')
        print("Let's start ...\n")

        for cr in survey_items:
            print(f'How do you rate this product aspect: ++ {cr[1].upper()}\n ++')
            print('Not important at all: 1\nLow importance : 2\nMedium important : 3\nHigh importance : 4\nExtremely important : 5\n')

            scr = input('your opinion : ')
            while not(scr.isdigit()) or (scr not in ('1', '2', '3', '4', '5')):
                print('please choose a correct value for the list.')
                scr = input('your opinion : ')
            ans.append([cr[0], scr])
        survey_ans[p], sample_preferences[p] = create_B_matrix(ans)

    return survey_ans


def create_B_matrix(answers):
    B_matrix = []
    preferences = {
                    '5': [],
                    '4': [],
                    '3': [],
                    '2': [],
                    '1': [],
                }

    for ans in answers:
        preferences[ans[1]].append(ans[0])  # sorts interviewed preferences in ascending order
    
    for x in answers:
        B_row = []
        for y in answers:
            if x[1] > y[1]:
                B_row.append(1)
            elif x[1] == y[1]:
                B_row.append(0.5)
            else:
                B_row.append(0)

        B_matrix.append(B_row)

    return B_matrix, preferences


def analyze(survey_ans):

    return compute_scale(convert_in_Z(create_P_matrix(create_F_matrix(survey_ans), partecipants=len(survey_ans))))


def create_F_matrix(survey_ans):

    F_matrix = survey_ans[0]
    for i in survey_ans:
        if i == 0:
            continue
        for j, row in enumerate(survey_ans[i]):
            for k, x in enumerate(row):
                F_matrix[j][k] += x
    
    return F_matrix


def create_P_matrix(F_matrix, partecipants):
    for i, row in enumerate(F_matrix):
        for j, x in enumerate(row):
            F_matrix[i][j] = x/partecipants

    return F_matrix


def convert_in_Z(P_matrix):
    import scipy.stats as st # the scipy library is required to run this code

    for i, row in enumerate(P_matrix):
        for k, x in enumerate(row):
            if x <= 0.001:
                P_matrix[i][k] = 3.09
            elif x >= 0.9999:
                P_matrix[i][k] = -3.09
            else:
                P_matrix[i][k] = st.norm.ppf(x)
    
    return P_matrix


def compute_scale(Z_matrix):
    scale_positions = []
    means = []
    max = 0
    min = 0

    for i, row in enumerate(Z_matrix):
        mean = 0
        for x in row:
            if max < -x:
                max = -x
            if min > -x:
                min = -x
            mean += -x
        means.append(mean/len(Z_matrix))
    for k in range(i+1):
        scale_positions.append((((max-(5*min))/(max-min)) + ((4/(max-min))*means[k])))
    Z_matrix.append(means)

    return scale_positions, Z_matrix


main()
