# -*- coding: utf-8 -*-
import glob, json, pdfquery
from operator import itemgetter

# utilizamos pdfquery
# porque el formato pdf es el mal
# (ver http://www.adobe.com/devnet/pdf/pdf_reference.html)

# Las siguientes restricciones aplican al fichero PDF de preguntas-respuestas:
#   * Las preguntas están resaltadas ('highlighted') con el color 'qcolor'
#     Para cada pregunta existe un 'PDFObject' de tipo 'Annot' y subtipo '/Highlight'
#     El texto de la pregunta está en un 'PDFObject' de tipo 'LTTextBoxHorizontal',
#     cuya bounding-box (o 'bbox') se solapa con una del highlight
#
#   * Las respuestas están resaltadas ('highlighted') con el color 'acolor'
#     Para cada respuesta existe un 'PDFObject' de tipo 'Annot' y subtipo '/Highlight'
#     El texto de la respuesta está en un 'PDFObject' de tipo 'LTTextBoxHorizontal',
#     cuya bounding-box (o 'bbox') se solapa con una del highlight
#
# Crear el pdf con latex y una plantilla parecida a la siguiente cumple la restriccion de la caja de texto:
# \documentclass{article}
# \usepackage[utf8]{inputenc}
# \usepackage{paralist}
# \usepackage{enumitem}
# \title{SLDS Project}
# \author{Jaime Pascual, Albert Lobo}
# \date{December 2016}
# \begin{document}
# \textbf{Encuesta}
# \begin{enumerate}
#  \item ¿De qué color es el caballo blanco de Santiago?
#    \begin{enumerate}[label=\arabic*)]
#      \item Rojo
#      \item Verde
#      \item Azul
#    \end{enumerate}
#  \item Indica la importancia de respirar. \\
#    \begin{inparaenum}[1)]
#      \item Poca \hspace{1ex}
#      \item \hspace{1ex}
#      \item \hspace{1ex}
#      \item \hspace{1ex}
#      \item \hspace{1ex}
#      \item \hspace{1ex}
#      \item \hspace{1ex}
#      \item \hspace{1ex}
#      \item \hspace{1ex}
#      \item Mucha
#    \end{inparaenum}
# \end{enumerate}
# \end{document}
# Utilizar Adobe Reader garantiza que la restriccion del highlight se cumple


#-------------------------------------------------------------------------------
#
# constantes
#
#-------------------------------------------------------------------------------

QUESTIONS_FILE = 'Preguntas/SLDS_Project_Questions.pdf'
ANSWERS_FOLDER = 'Respuestas/'
QCOLOR, ACOLOR = '[0.0, 0.0, 1.0]', '[0.0, 1.0, 0.0]'
QUESTIONS_JSON = 'questions.json'
ANSWERS_JSON = 'answers.json'


#-------------------------------------------------------------------------------
#
# preguntas
#
#-------------------------------------------------------------------------------

def save_json(filename, jsn):
    file = open(filename, 'w')
    file.write(json.dumps(jsn, indent=2))
    file.close()

def get_element_data(page_index, etype, txt_elem):
    tbbox = map(lambda x: float(x), txt_elem.get('bbox')[1:-1].split(', '))
    txt = txt_elem.layout.get_text().encode('utf-8')
    return {
        'page_index': int(page_index),
        'etype': etype,
        'bbox': tbbox,
        'bbox_top': -tbbox[1],
        'bbox_left': tbbox[0],
        'text': txt
    }

def append_page_elements(pdf, page_index, color, etype, elems):
    # Find an 'Annot' whose attribute 'Subtype' is '/Highlight' and 'C' is 'qcolor'
    # inside an 'LTPage' node whose 'page_index' attribute is 'page_index'
    page_query = 'LTPage[page_index="' + page_index + '"]'
    annot_query = 'Annot[Subtype="/Highlight"][C="' + color + '"]'
    qhighlights = pdf.pq(page_query + ' ' + annot_query)
    for highlight in qhighlights:
        # highlight is an instance of pdfquery.pdfquery.LayoutElement
        # which is a subclass of lxml.etree.ElementBase
        # now we need to find an overlapping 'LTTextBoxHorizontal'
        # in the same page, obviously
        hbbox = highlight.get('bbox')
        txt_query = 'LTTextBoxHorizontal:overlaps_bbox("' +  hbbox[1:-1] + '")'
        txt_elem = pdf.pq(page_query + ' ' + txt_query)

        # append the corresponding question or answer data:
        # the page index, bounding box and actual text
        elem = get_element_data(page_index, etype, txt_elem[0])
        elems.append(elem)

def build_questions_json(elems):
    qidx, aidx = 1, 1
    questions = []
    qobj = {}
    for elem in elems:
        if elem['etype'] == 'q':
            elem['qid'] = qidx
            qobj = {
                'id': qidx,
                'text': elem['text'],
                'numAnswers': 0,
                'answers': []
            }
            questions.append(qobj)
            qidx += 1
            aidx = 1
        elif elem['etype'] == 'a':
            elem['qid'] = qobj['id']
            elem['aid'] = aidx
            aobj = {
                'id': aidx,
                'text': elem['text']
            }
            qobj['numAnswers'] += 1
            qobj['answers'].append(aobj)
            aidx += 1
    return { 'questions': questions }

def get_questions():
    # load pdf
    pdf = pdfquery.PDFQuery(QUESTIONS_FILE)
    pdf.load()

    # print the tree as xml
    # pdf.tree.write("test.xml", pretty_print=True, encoding="utf-8")

    # get all questions and answers
    # then sort them by page and bounding-box top-left coordinates
    elems = []
    pages = pdf.pq('LTPage')
    for page in pages:
        page_index = page.get('page_index')
        append_page_elements(pdf, page_index, QCOLOR, 'q', elems)
        append_page_elements(pdf, page_index, ACOLOR, 'a', elems)
    elems = sorted(elems, key=itemgetter('page_index', 'bbox_top', 'bbox_left'))

    # produce the final json and save it
    qjson = build_questions_json(elems)
    save_json(QUESTIONS_JSON, qjson)
    return elems


#-------------------------------------------------------------------------------
#
# respuestas
#
#-------------------------------------------------------------------------------

# create the basic structure of the answers json object
# it contains:
#   - 'numAnswers': the number of answer pdf files (i guess this should be one per user)
#   - 'answers': an array of objects representing answers to the questions
#                each one of these objects holds:
#                  - 'questionId': id of the corresponding question
#                  - 'answers': an array of integers representing how many times each
#                               answer to that question was selected, in total
#                               (sorted by answer id)
def get_answers_json(elems):
    ans = []
    aobj = None
    for elem in elems:
        if elem['etype'] == 'q':
            aobj = {
                'questionId': elem['qid'],
                'answers': []
            }
            ans.append(aobj)
        elif elem['etype'] == 'a':
            aobj['answers'].append(0)
    return { 'numAnswers': 0, 'answers': ans }


def append_bbox_answers(pdf, page_index, bboxes):
    # find all text highlights in the page
    page_query = 'LTPage[page_index="' + page_index + '"]'
    annot_query = 'Annot[Subtype="/Highlight"]'
    qhighlights = pdf.pq(page_query + ' ' + annot_query)
    for highlight in qhighlights:
        # extract the bounding box
        hbbox = highlight.get('bbox')
        bbox = map(lambda x: float(x), hbbox[1:-1].split(', '))
        aobj = {
            'page_index': int(page_index),
            'bbox': bbox,
            'bbox_top': -bbox[1],
            'bbox_left': bbox[0]
        }
        bboxes.append(aobj)

# get all highlight bboxes from a pdf file
# returns a list where each element represents a selected answer
def get_bboxes_answers(pdf):
    bboxes = []
    pages = pdf.pq('LTPage')
    for page in pages:
        page_index = page.get('page_index')
        append_bbox_answers(pdf, page_index, bboxes)
    return sorted(bboxes, key=itemgetter('page_index', 'bbox_top', 'bbox_left'))

# run-of-the-mill bounding-box overlap function
def bbox_overlap(abbox, bbbox):
    return not (abbox[0]>bbbox[2] or abbox[2]<bbbox[0] or abbox[1]>bbbox[3] or abbox[3]<bbbox[1])

def process_answer_files(ajson, elems):
    answers = ajson['answers']
    for filename in glob.glob(ANSWERS_FOLDER + '*.pdf'):
        pdf = pdfquery.PDFQuery(filename)
        pdf.load()

        # since both 'elems' and 'bboxes' are sorted using the same criteria
        # we can just iterate both lists from start to end and match all answers
        # this means we can't miss any, by construction
        # TODO: error handling,
        # like what if someone highlights more than one answer for a question,
        # or doesn't answer a question
        it = iter(elems)
        bboxes = get_bboxes_answers(pdf)
        for bbox in bboxes:
            elem = next(it)
            while elem['etype']=='q' or not bbox_overlap(bbox['bbox'], elem['bbox']):
                elem = next(it)
            qid, aid = elem['qid'], elem['aid']
            answers[qid - 1]['answers'][aid - 1] += 1

        # don't forget to increment answers counter
        ajson['numAnswers'] += 1

def get_answers(elems):
    ajson = get_answers_json(elems)
    process_answer_files(ajson, elems)
    save_json(ANSWERS_JSON, ajson)

#-------------------------------------------------------------------------------
#
# main
#
#-------------------------------------------------------------------------------
def run():
    elems = get_questions()
    get_answers(elems)

run()
