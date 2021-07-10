import re
import bs4
import Utility


def getAllSpecFromHtml(html):
    soup = bs4.BeautifulSoup(html, features="html.parser")
    div = soup.find(re.compile("div"), {"class": re.compile("(speclist|specs|spec)")})

    if div is None:
        div = soup.find(re.compile("ul"), {"class": re.compile("(speclist|specs|spec)")})

    specListString = div.get_text(separator=', ')

    all_spec_list_dict = Utility.getDictionaryFromString(specListString)
    return all_spec_list_dict


def searchProductTypeInSpecList(productSpecs):
    tempDictKey = []
    for k in productSpecs:
        if "type" not in k.lower():
            tempDictKey.append(k)

    for i in tempDictKey:
        productSpecs.pop(i)

    # print("Min Spec List: " + str(productSpecs))
    return productSpecs


def getProductDimensions(allSpecs):
    height = 0.0
    width = 0.0
    depth = 0.0
    weight = 0.0
    area = 0.0
    length_unit=""
    weight_unit=""
    area_unit=""
    product_weight=""
    product_area=""
    # print("Printing ALL SPECS")
    # print(allSpecs)

    for k in allSpecs:
        if "height" in k.lower():
            try:
                height = float(allSpecs[k].split()[0])
            except ValueError:
                height = 0
            if height > 0:
                length_unit = getUnit(k)
        if "width" in k.lower():
            try:
                width = float(allSpecs[k].split()[0])
            except ValueError:
                width = allSpecs[k].split()[0]
        if "depth" in k.lower():
            try:
                depth = float(allSpecs[k].split()[0])
            except ValueError:
                depth = allSpecs[k].split()[0]
        if "weight" in k.lower():
            try:
                weight = float(allSpecs[k].split()[0])
            except ValueError:
                weight = 0
            if weight > 0:
                weight_unit = getUnit(k)

        if "area" in k.lower():
            try:
                area = float(allSpecs[k].split()[0])
            except ValueError:
                area = 0
            if area > 0:
                area_unit = getUnit(k)

    product_height_depth_width = str(height)+"x"+str(depth)+"x"+str(width)+"("+length_unit.capitalize()+")"

    if weight > 0.0:
        product_weight = str(weight)+" "+weight_unit

    if area > 0.0:
        product_area = str(area)+" sq "+area_unit

    print(product_height_depth_width+" "+product_weight+" "+product_area)


def getUnit(inputStringKey):
    string_array = inputStringKey.split()
    unit = string_array[len(string_array) - 1]
    return re.sub('[^A-Za-z0-9]+', '', unit)
