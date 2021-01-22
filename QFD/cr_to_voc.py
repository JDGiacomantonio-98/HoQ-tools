def compute_median(scores):
    if len(scores) > 1:
        return ((scores[int(len(scores)/2)]+scores[int((len(scores)/2)-1)])/2) if len(scores) % 2 == 0 else scores[int(((len(scores)-1)/2)+1)]
    return scores[0]


def compute_mean(scores):
    num = 0

    for x in scores:
        num += x
    
    return num/len(scores)

def sort_list_custom(unsorted, descending=True):
    # sorting the vector in descending order (the bad way: looping all items each time)
    sorted = []

    if descending:
        for i, x in enumerate(unsorted):
            if i == 0:
                max = x
                sorted.append(x)
                continue
            if x >= max:
                max = x
                sorted.append(x)
                continue
            for j, y in enumerate(sorted):
                if x <= y:
                    tail = sorted[j:]
                    if j == 0:
                        sorted = [x]
                    else:
                        sorted = sorted[:j]
                        sorted.append(x)
                    for k in tail:
                        sorted.append(k)
                    break
                
    return sorted

def sort_voc():
    from xlrd import open_workbook

    with open_workbook('team alpha-voc-metrics-py.xlsx') as wb:
        adiacency_matrix = wb.sheet_by_index(0)
        voc_db = wb.sheet_by_index(1)

    cr = {}
    for h in range(1, adiacency_matrix.ncols):
        cr[adiacency_matrix.cell_value(0, h)] = {}

    q_fields = []
    for h in range(1, adiacency_matrix.nrows):
        q_fields.append(adiacency_matrix.cell_value(h, 0))

    k = 1
    try:
        while voc_db.cell_value(k, 0) != '':
            for i, cr_labl in enumerate(cr.keys()):
                scores = []
                for j in range(len(q_fields)):
                    if adiacency_matrix.cell_value(j+1, i+1) == 1:
                        scores.append(voc_db.cell_value(k, j+1))
                # cr[cr_labl][k] = [compute_median(sort_list_custom(scores)), compute_mean(scores)]
                cr[cr_labl][k] = [compute_median(scores.sort()), compute_mean(scores)]
            k += 1
    except IndexError:
        return cr


def main():
    from cr_prioritisation import analyze, create_B_matrix, print_results

    cr_scores = sort_voc()
    print('| \t\tC.R.\t\t\t')
    for k in cr_scores.keys():
        means = []
        medians = []
        for ans in cr_scores[k].values():
            medians.append(ans[0])
            means.append(ans[1])
        cr_scores[k] = [compute_median(medians), compute_mean(means)]
        print(f'|| {k} \t=>\t || median : {cr_scores[k][0]} || mean : {cr_scores[k][1]} ||')
        print('-----------------------------------------------------------------------------------------------')

    print_results(results=analyze(create_B_matrix(cr_scores)),c_req=cr_scores.keys())

main()
