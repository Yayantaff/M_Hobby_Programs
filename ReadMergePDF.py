# -*- coding: utf-8 -*-

"""
Created on Sat Jun 20 11:58:19 2020

MIT License

Copyright (c) 2020 Yayantaff Levin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

# pdf_splitting.py

from PyPDF2 import PdfFileReader, PdfFileWriter

import pandas as pd

import glob

import os

    
    
def extract_info_csv():
    
    df = pd.read_csv('pdf_nomenclatures.csv', sep=';')
    
    df['Page_Numbers'] = df['Page_Numbers'].apply(lambda x: str(x).split(","))
    
    return df
    
    
def gather_all_pdfs(data_frame):
    
    catalogue_pdf =  'IndexCatalogue_PE.pdf'
    
    pdf_writer = PdfFileWriter()

    for filename in glob.iglob(r'Pop1956_12\*'):
    #glob.iglob(r'F:\Roshan\Python_Programs\PopElect_Assort\*\*'):
        
        if filename.endswith(".pdf"):
            
            # write a function here
            
            pdf = PdfFileReader(filename)
            
            if  pdf.isEncrypted:
                print ("Rut ro, it's encrypted.")
                # skip file? Write to a log?
            else:
                print ("We're clear.")
                # Do stuff with the file.
            
                filepath_pure = os.path.splitext(filename)[0]
            
                filename_pure = os.path.split(filepath_pure)[1]
            
                for row_label, row in data_frame.iterrows():
                    
                    if((row['Nomenclature'] in filename_pure)):
                        
                        page_number_list = list(map(int, data_frame.iloc[row_label,1]))
                        
                        break
                
                for page in page_number_list:
                    
                    pdf_writer.addPage(pdf.getPage(page))
                    
                print(filename_pure)
                
                with open(catalogue_pdf, 'wb') as catalogue:
                    
                    pdf_writer.write(catalogue)
                    
    return
            
        
if __name__ == '__main__':
   
   data_frame = extract_info_csv()
   
   gather_all_pdfs(data_frame)