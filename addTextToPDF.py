from PyPDF2 import PdfFileWriter, PdfFileReader
import io
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from unidecode import unidecode                        

def addTextToPDF(teacher ,classes):
    teacher = teacher
    name = classes["name"]
    day = classes["day"]
    time = classes["time"]
    promo = classes["promo"]

    if classes["group"] == "":
        group = "CM"
    else:
        group = classes["group"]

    packet = io.BytesIO()

    can = canvas.Canvas(packet, pagesize=letter)
    #Change font and size

    can.setFont('Times-Bold',12)

    #write data
    day = day.replace("\n", " ").replace("\xa0", " ").replace("\t", " ")
    can.drawString(160, 682, teacher)
    can.drawString(160, 654, name)
    can.drawString(160, 626, day+time)
    can.save()

    pdfModel = group +"_"+promo
    # create a new PDF with Reportlab
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    try :
        existing_pdf = PdfFileReader(open(f"pdfGeneration./models/{promo}/{pdfModel}.pdf", "rb"))
    except:
        raise Exception("Le modèle de pdf n'existe pas")

    output = PdfFileWriter()

    # add the data on the existing page
    page = existing_pdf.getPage(0)
    #merge edited page
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    #add unedited pages
    for i in range(1,existing_pdf.getNumPages()):
        page = existing_pdf.getPage(i)
        output.addPage(page)

    directory = f"./pdfGeneration/results/{teacher}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    #delete old pdf
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory, filename)
            try:
                os.unlink(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    day=day.strip()
    day = unidecode(day)
    #output the new PDF
    outputStream = open(f"./pdfGeneration/results/{teacher}/{promo}_{day}_{time}.pdf", "wb")
    output.write(outputStream)
    outputStream.close()

