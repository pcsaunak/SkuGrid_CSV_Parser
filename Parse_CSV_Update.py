import csv
import re
import Specification_Parser as Sp
import Constants as C

from bs4 import BeautifulSoup
from Title_Parser import trimTitle, trimTitle2,removeUnwantedWordFromOriginalTitle, removeDuplicateWordsFromTitle

updated_csv_content = []


def readCsv(file):
    current_file = file
    csv_file = open(current_file)
    csv_reader = csv.reader(csv_file)
    return csv_reader


def parseCSV(csv_reader):
    line_count = 0

    for row in csv_reader:
        all_specs_dict = {}
        if line_count == 0:
            line_count += 1
        else:
            productColor = ""
            line_count += 1
            print("Line Processed: " + str(line_count))

            html = row[4]
            brand = row[5]

            new_html = re.sub("Returnable: [5-9][0-9]", "Returnable: 30", html)
            new_html = re.sub("Returnable: 1[0-9][0-9]", "Returnable: 30", new_html)

            pattern = "Warranty"
            soup = BeautifulSoup(new_html, 'html.parser')

            # List tag
            text4 = soup.find_all('li', text=re.compile(pattern))

            for i in text4:
                new_html = new_html.replace(str(i), "")

            warrantyIndexStart = new_html.find("Warranty")

            if warrantyIndexStart > 0:
                warrantyIndexEnd = new_html[warrantyIndexStart:].find("</li>")
                updatedWarrantyHTML = new_html.replace(
                    new_html[warrantyIndexStart + 10:warrantyIndexStart + warrantyIndexEnd], "None")
            else:
                updatedWarrantyHTML = new_html

            colorIndexStart = updatedWarrantyHTML.find(">Color")

            if colorIndexStart == -1:
                colorIndexStart = updatedWarrantyHTML.find("Color")

            if colorIndexStart > 0:
                colorIndexEnd = updatedWarrantyHTML[colorIndexStart:].find("</li>")
                colorLineValue = updatedWarrantyHTML[colorIndexStart:colorIndexStart + colorIndexEnd]
                colorIndexStartDelta = colorLineValue.find(":") + 2
                productColor = updatedWarrantyHTML[
                               colorIndexStart + colorIndexStartDelta:colorIndexStart + colorIndexEnd]
                # print("Color: " + productColor)

            productIndexStart = updatedWarrantyHTML.find("Product")
            productIndexEnd = updatedWarrantyHTML[productIndexStart:].find("</li>")
            productName = updatedWarrantyHTML[productIndexStart:productIndexStart + productIndexEnd]

            if len(productName) <= 0:
                productName = " -- "
            else:
                productName = productName.split(":")[1]

            if not productName.strip().isalpha():
                productName = " -- "

            # print("Brand: " + brand)
            # print("Product Info/Name: " + productName)

            all_specs_dict = Sp.getAllSpecFromHtml(updatedWarrantyHTML)
            specList_dict = Sp.searchProductTypeInSpecList(all_specs_dict.copy())

            Sp.getProductDimensions(all_specs_dict.copy())
            # print("Product Type: " + str(specList_dict))

            processedTitle = trimTitle2(specList_dict.copy(), row[3])

            if len(processedTitle) < 6:
                processedTitle = removeUnwantedWordFromOriginalTitle(row[3])

            finalTitle = brand + " " + processedTitle + " " + productColor

            finalTitle = removeDuplicateWordsFromTitle(re.sub(' +', ' ', finalTitle))
            # print("Original Title: " + str(row[3]))
            # print("Processed Title: " + finalTitle)
            print("***********************************")
            populateCSVContent(row, updatedWarrantyHTML, finalTitle)


def populateCSVContent(row, updatedWarrantyHTML, finalTitle):
    global updated_csv_content
    create_row = [row[0], row[1], row[2], finalTitle, updatedWarrantyHTML,
                  row[5], row[6], row[7],
                  row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17],
                  row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25], row[26], row[27],
                  row[28], row[29], row[30], row[31], row[32], row[33], row[34], row[35], row[36], row[37],
                  row[38], row[39], row[40], row[41], row[42], row[43], row[44], row[45], row[46], row[47],
                  row[48], row[49], row[50], row[51], row[52], row[53], row[54], row[55], row[56], row[57],
                  row[58], row[59], row[60], row[61], row[62], row[63], row[64], row[65], row[66], row[67],
                  row[68], row[69], row[70], row[71], row[72]]
    updated_csv_content.append(create_row)


def writeToCSV(file):
    print(" WRITING TO CSV FILE ")
    op = open(file, "w")
    writer = csv.writer(op, delimiter=',')
    writer.writerow(C.CSV_HEADER)
    writer.writerows(updated_csv_content)


def startProgram(filepath,fileName):
    sample_4_write = "/tmp/"+fileName+"_output.csv"
    myCsv = readCsv(filepath+fileName)
    parseCSV(myCsv)
    writeToCSV(sample_4_write)
    return "Successfully updated CSV", 204
