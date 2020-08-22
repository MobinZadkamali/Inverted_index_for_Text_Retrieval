import os
import xlsxwriter

documents = os.listdir('./0Mytest')
n = len(documents)
print("We have " + str(n) + " documents.")

x = ["t-e-r-m", "f-r-e-q-u-e-nc-y"]
for i in documents:
    x.append(i)
matrix = [x]

for d in documents:
    text_IO = open('./0Mytest/' + d, "rt")
    Faults = [",", "!", "'s", "?", ":", "(", ")", "-", '"']
    text = text_IO.read()
    text = text.lower()
    for x in Faults:
        text = text.replace(x, "")
    words = text.split()
    for i in range(len(words)):
        if words[i][-1] == ".":
            words[i] = words[i].replace(".", "")
    for word in words:
        #         print(word)
        if word in [row[0] for row in matrix]:
            matrix_words = [row[0] for row in matrix]
            #             matrix[matrix_words.index(word)][1]+= 1
            matrix[matrix_words.index(word)][matrix[0].index(d)] = 1
        else:
            l = [word, 1]
            for j in range(n):
                l.append(0)
            matrix.append(l)
            matrix_words = [row[0] for row in matrix]
            matrix[matrix_words.index(word)][matrix[0].index(d)] = 1

# computing document frequency
matrix_words = [row[0] for row in matrix]
for i in range(1, len(matrix_words)):
    freq = 0
    for j in range(2, len(matrix[0])):
        if matrix[i][j] == 1:
            freq += 1
    matrix[i][1] = freq

workbook = xlsxwriter.Workbook('./term_document1.xlsx')
worksheet = workbook.add_worksheet()
row = 0
for col, data in enumerate(matrix):
    worksheet.write_column(row, col, data)
workbook.close()


def New_Matrix(p, q):  # create a matrix filled with 0s
    matrix = [[0 for row in range(q)] for col in range(p)]
    return matrix


inverted_index1 = New_Matrix(3, 0)
for i in range(1, len(matrix)):
    inverted_index1[0].append(matrix[i][0])
    inverted_index1[1].append(matrix[i][1])
for i in range(len(inverted_index1[0])):
    inverted_index1[2].append(i)

inverted_index2 = []
for i in range(len(inverted_index1[0])):
    inverted_index2.append([])
for i in range(1, len(matrix)):
    for j in range(2, len(matrix[0])):
        if matrix[i][j] == 1:
            inverted_index2[i - 1].append(matrix[0][j])


workbook = xlsxwriter.Workbook('./inverted_index1.xlsx')
worksheet = workbook.add_worksheet()
row = 0
for col, data in enumerate(inverted_index1):
    worksheet.write_column(row, col, data)
workbook.close()

workbook = xlsxwriter.Workbook('./inverted_index2.xlsx')
worksheet = workbook.add_worksheet()
row = 0
for col, data in enumerate(inverted_index2):
    worksheet.write_column(row, col, data)
workbook.close()

def OR(l1, l2):
    return list(set(l1 + l2))


def AND(l1, l2):
    return list(set(l1).intersection(l2))


def NOT(ld, l1):
    l = OR(ld, l1)
    for i in l1:
        l.remove(i)
    return l


def AND_list(result, terms, inverted_index1, inverted_index2):
    freqs = []
    for i in range(len(terms)):
        freqs.append(inverted_index1[1][inverted_index1[0].index(terms[i])])
    freqs, terms = (list(x) for x in zip(*sorted(zip(freqs, terms))))
    if len(result) == 0:
        l1 = inverted_index2[inverted_index1[2][inverted_index1[0].index(terms[0])]]
        l2 = inverted_index2[inverted_index1[2][inverted_index1[0].index(terms[1])]]
        l = AND(l1, l2)
        if len(terms) > 2:
            for i in range(2, len(terms)):
                l1 = l
                l2 = inverted_index2[inverted_index1[2][inverted_index1[0].index(terms[i])]]
                l = AND(l1, l2)
    else:
        l1 = result
        l2 = inverted_index2[inverted_index1[2][inverted_index1[0].index(terms[0])]]
        l = AND(l1, l2)
        if len(terms) > 1:
            for i in range(1, len(terms)):
                l1 = l
                l2 = inverted_index2[inverted_index1[2][inverted_index1[0].index(terms[i])]]
                l = AND(l1, l2)
    return l


def OR_list(result, terms, inverted_index1, inverted_index2):
    if len(result) == 0:
        l1 = inverted_index2[inverted_index1[2][inverted_index1[0].index(terms[0])]]
        l2 = inverted_index2[inverted_index1[2][inverted_index1[0].index(terms[1])]]
        l = OR(l1, l2)
        if len(terms) > 2:
            for i in range(2, len(terms)):
                l1 = l
                l2 = inverted_index2[inverted_index1[2][inverted_index1[0].index(terms[i])]]
                l = OR(l1, l2)
    else:
        l1 = result
        l2 = inverted_index2[inverted_index1[2][inverted_index1[0].index(terms[0])]]
        l = OR(l1, l2)
        if len(terms) > 1:
            for i in range(1, len(terms)):
                l1 = l
                l2 = inverted_index2[inverted_index1[2][inverted_index1[0].index(terms[i])]]
                l = OR(l1, l2)
    return l


def NOT_list(result, terms, inverted_index1, inverted_index2):
    if len(result) == 0:
        l1 = inverted_index2[inverted_index1[2][inverted_index1[0].index(terms[0])]]
        l2 = inverted_index2[inverted_index1[2][inverted_index1[0].index(terms[1])]]
        l = NOT(l1, l2)
    else:
        l1 = result
        l2 = inverted_index2[inverted_index1[2][inverted_index1[0].index(terms[0])]]
        l = NOT(l1, l2)
    return l


#  text handeling
def search(q, inverted_index1, inverted_index2):
    result = []
    p_start = []
    p_end = []
    query = q.split()
    # print(query)
    if len(query) == 1:
        result = inverted_index2[inverted_index1[2][inverted_index1[0].index(query[0])]]
        return result
    for i in range(len(query)):
        if query[i] == "(":
            p_start.append(i)
        if query[i] == ")":
            p_end.append(i)
    if len(p_start) == 0:
        cu_terms = []
        for i in query:
            if i != "AND" and i != "OR" and i != "NOT":
                cu_terms.append(i)
        if "AND" in query:
            result = AND_list(result, cu_terms, inverted_index1, inverted_index2)
        if "OR" in query:
            result = OR_list(result, cu_terms, inverted_index1, inverted_index2)
        if "NOT" in query:
            result = NOT_list(result, cu_terms, inverted_index1, inverted_index2)
        return result


while (1 == 1):
    q = input("Please Enter The Query :")
    result = search(q, inverted_index1, inverted_index2)
    output = "Result : "
    for i in result:
        output += " " + i + " "
    print(output)