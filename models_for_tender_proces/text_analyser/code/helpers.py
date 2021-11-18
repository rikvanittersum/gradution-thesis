from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine


# Functie voor het omzetten van een pdf document in woorden en de relevante daarvan selecteren.
def pdf_woorden(filename):
    # Open het bestand en lees bites(rb)
    fp = open(filename, 'rb')

    # Opzetten pdf parser voor lezen woorden op pagina. Standaard pdfminer setup.
    parser = PDFParser(fp)
    doc = PDFDocument()
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize('')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    laparams.char_margin = 1.0
    laparams.word_margin = 1.0
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # In extracted komen uiteindelijk alle woorden.
    extracted_text = ''

    # Ittereren over elke pagina van de pdf.
    for page in doc.get_pages():
        interpreter.process_page(page)
        layout = device.get_result()

        # Ittereren over objecten op pagina.
        for lt_obj in layout:

            # Als object een woord is, toevoegen aan extracted text
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                extracted_text += lt_obj.get_text()

    # Omzetten van alle letter naar niet-hoofdletter.
    # Keywords maakt van aaneeschakeling van karakters een lijst met woorden, zodat er mee gewerkt kan worden.
    # "dit zijn woorden" wordt: ['dit', 'zijn', 'woorden']
    lower = extracted_text.lower()
    uit_elkaar = lower.split()
    stop_words = stopwords.words("dutch")
    keywords = [word for word in uit_elkaar if not word in stop_words]

    return keywords
