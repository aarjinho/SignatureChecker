import json
import os
from fpdf import FPDF
def generate_pdf(etudiants, promotion, group="CM"):

  # Creat PDF
  pdf = FPDF(format='A4')
  pdf.cMargin = 5

  #Footer
  def footer():
    # get page number
    page = pdf.page_no()
    pdf.set_font('Arial', 'I', 15)

    # add page number
    pdf.text(pdf.w - 10, pdf.h - 10, f'{page}')

  pdf.footer = footer

  pdf.add_page()

  # Add header
  pdf.image('./pdfGeneration/header1.png', 0, 0, pdf.w, 0, type='PNG')
  pdf.set_fill_color(217,217,217)
  pdf.set_xy(20 , 30)
  pdf.set_font('Arial', 'B', 18)
  pdf.cell(pdf.w -45, 10, "FEUILLE DE PRESENCE", 0, 1, 'C', 1)
  pdf.set_x(20)
  pdf.cell(pdf.w -45, 10, f"{group} - {promotion}", 0, 1, 'C', 1)

  pdf.set_xy(20 , 50)
  pdf.set_font('Arial', 'B', 12)
  # Add the four lines of text with a filled background
  pdf.cell(0, 10, "Enseignant : ", 0, 1, 'L', 0)
  pdf.set_x(20)
  pdf.cell(0, 10, "UE ou ECUE : ", 0, 1, 'L', 0)
  pdf.set_x(20)
  pdf.cell(0, 10, "Date/salle : ", 0, 1, 'L', 0)

  # la ou il commence les titres du tableau ( je sais pas comment l'expliquer en anglais )
  pdf.set_x(20)
  # Set column widths based on the longest name and prenom
  pdf.cell(15 , 7, 'civilité', 1, 0, 'C')
  pdf.cell(55, 7, 'Nom patronymique', 1, 0, 'C')
  pdf.cell(40 , 7, 'Prénom', 1, 0, 'C')  
  pdf.cell(70, 7, 'Emargement', 1, 0, 'C')


  # Print student table
  y = 87# student table postition 
  for etudiant in etudiants:
    # create new page if table postion > page height 
    if y > pdf.h - 30:
      pdf.add_page()
      y = 40
      pdf.image('./pdfGeneration/header1.png', 0, 0, pdf.w, 0, type='PNG')


    pdf.set_xy(20, y)
    pdf.set_font('Arial', '', 10)

    pdf.cell(15, 8, etudiant['civility'], 1, 0, 'L') 
    pdf.cell(55 , 8, etudiant['lastname'].upper(), 1, 0, 'L') 
    pdf.cell(40, 8, etudiant['firstname'].upper(), 1, 0, 'L') 
    pdf.cell(70, 8, "", 1, 0, 'L')
    y += 8  # update vartical postion 

  directory = f"./pdfGeneration/models/{promotion}"
  if not os.path.exists(directory):
    os.makedirs(directory)

  # save file   
  pdf.output(f'./pdfGeneration/models/{promotion}/{group}_{promotion}.pdf', 'F')



