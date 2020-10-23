import pytesseract
import shutil
import os
import random
try:
    from PIL import Image
except ImportError:
    import Image

def gen_txt():
   extractedInformation = pytesseract.image_to_string(Image.open('a3.png')) 
   return extractedInformation   

import os, cv2, pytesseract, re, time, numpy as np, utils as mUT, myYoloDetect as mYD
all_list=[]
prod_list=[]
try:
    from PIL import Image
except ImportError:
    import Image
clsfile = '/content/drive/My Drive/dist/digit.cls'
cfgfile = '/content/drive/My Drive/dist/digit.cfg'
wgtfile = '/content/drive/My Drive/dist/digit.weights'
cnt = 0
mg = 2
fname = ''
workbook = None
east = None
format = None
col_w = 0
row = 0
file_row = 1
zip_code = 0
ref_inv = 0
complete_total = False
complete_one = False
pause = False
cancel = False
Product_Name = [
 'Hyphen', 'Pookula Lehyam', 'Vellulli Lehyam', 'Kesaroop Hair Oil 100 ml.', 'Sallaki - Tablets 400mg.',
 'Diabo Capsules 500 mg.', 'Trazodone', 'Nitrazepam', 'Lunesta',
 'Sonata', 'Ambien', 'Herbal Ambien', 'Temazepam',
 'Trazodone Hcl 25mg', 'Trazodone Hcl 50mg', 'Pankaja Kasthuri 400 gm.', 'REVIG CAPS',
 'DIATEA', 'Pacchjeerakagudam', 'Deepam Kesathali', 'Deepam Kesathali']
Product_Rate = [0, 7.67, 8.947, 4.44, 7.09, 2.97, 26.67, 28.89, 33.33, 53.33, 49.82,
 75.56, 27.78, 2.54, 4.2, 210, 44.44, 38.89, 61.11, 66.67, 55.56]
ten_unit = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
one_unit = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten',
 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
month_err = ['YJan', 'Yan', 'YTan', 'TJan', 'Tan', 'J ul', 'Ju1', 'J un', 'Oc1', 'Now']
month_ok = ['Jan', 'Jan', 'Jan', 'Jan', 'Jan', 'Jul', 'Jul', 'Jun', 'Oct', 'Nov']
month_bname = ['Jan', 'Feb', 'Mar', 'Apr', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
month_pname = ['January', 'February', 'March', 'April', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
month_cname = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Oc1', 'Nov', 'Dec', 'Yan', 'Tan', 'J un', 'J ul', 'Ju1', 'Now']
digit_old = [' ', 'O', 'o', '@', '$', '?', '»', 'G', '§', 'S-', 'S', 's', '%', '£', 'g', 'f', '()', '(', ';', ':', '!', 'i', 'l', 'I', ']', 'L',
 '+', '«', '.', 'K', 'M', '¥', '&', '}', 'H', 'W', 'D', 'B', '€', 'X', ')', 'z', 'm', '#', '\\)', 'J', '°', '~']
digit_new = ['', '0', '0', '69', '8', '2', '2', '6', '6', '84', '8', '5', '5', '5', '5', '5', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1',
 '4', '5', '', '14', '14', '29', '68', '3', '4', '29', '79', '59', '62', '20', '', '2', '00', '4', '70', '3', '2', '7']


def get_SplitPointX(img):
    h, w = img.shape[:2]
    image = img[0:150, 0:w]
    image = apply_brightness_contrast(image, -30, 130)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, thd = cv2.threshold(image, 128, 255, cv2.THRESH_OTSU)
    edges = cv2.Canny(thd, 128, 255, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, (np.pi / 180), 80, minLineLength=30, maxLineGap=10)
    crop_x = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if abs(x2 - x1) < 2:
            crop_x.append(x1)

    crop_x.sort()
    for i in range(len(crop_x) - 2):
        if crop_x[(i + 1)] - crop_x[i] < 5:
            crop_x.remove(crop_x[i])

    return crop_x  

def apply_brightness_contrast(input_img, brightness=0, contrast=0):
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow) / 255
        gamma_b = shadow
        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()
    if contrast != 0:
        f = 131 * (contrast + 127) / (127 * (131 - contrast))
        alpha_c = f
        gamma_c = 127 * (1 - f)
        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)
    return buf    

def func_SplitImage(fname, img, crop_x):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = apply_brightness_contrast(img, -5, 20)
    h, w = img.shape[:2]
    crop1 = img[0:h, crop_x[0]:crop_x[1]]
    #filename1="a1.png"
    #filename2="a2.png"
    #cv2.imwrite(filename1, crop1) 
    func_CropColumnTextBox(fname, crop1)
    crop2 = img[0:h, crop_x[2]:crop_x[3]]
    func_CropColumnTextBox(fname, crop2)
    #cv2.imwrite(filename2, crop2) 

def func_PreProcessCropTextBox(img2gray):
    height, width = img2gray.shape[:2]
    new_img = cv2.bitwise_not(np.zeros((height, width + 20), np.uint8))
    new_img[0:height, 0:width] = img2gray
    ret, thresh = cv2.threshold(new_img, 200, 255, cv2.THRESH_BINARY)
    dilated = cv2.erode(thresh, None, iterations=5)
    line_num = round(height / 20)
    gap = round(height / line_num)
    for i in range(line_num):
        cv2.line(dilated, (0, 19 + gap * i), (width + 20, 19 + gap * i), (0, 0, 0), 3)

    contours, _ = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 20:
            x, y, w, h = cv2.boundingRect(contour)
            if h > 10:
                if w < 25:
                    dx = x + int(0.5 * w) - 5
                else:
                    dx = x + 5
                dy = y + int(0.5 * h) + 3
                cv2.putText(new_img, '/', (dx, dy), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0,
                                                                                    0,
                                                                                    0), 1)

    return new_img

def replace_SCharToDigit(text, old, new, isarray):
    if isarray is True:
        for i in range(0, len(old)):
            text = text.replace(old[i], new[i])

    else:
        for i in range(0, len(old)):
            text = text.replace(old[i], new)

    return text

def func_TesseractOCR(img):
    filename1="a3.png"
    cv2.imwrite(filename1, img) 
    text=gen_txt()
    sep = [' _ ', ' — ', '|', '‘']
    for s in range(0, len(sep)):
        text = text.replace(sep[s], '')

    con1 = [
     '\n', '\n\n', ' A—', ' B—', ' C—', ' D—', ' E—', ' F—', ' G—',
     ' H—', ' I—', ' J—', ' K—', ' L—', ' M—', ' N—', ' O—',
     ' P—', ' Q—', ' R—', ' S—', ' T—', ' U—', ' V—', ' W—',
     ' X—', ' Y—', ' Z—', ' E1', ' E2', ' E3', ' E4', ' E5', ' E6', ' E7', ' E8', ' E9']
    for c in range(0, len(con1)):
        text = text.replace(con1[c], '/' + con1[c])

    for s in range(0, len(sep)):
        text = text.replace(sep[s], '/')

    common_error_char = ['—', '$', '§', '+', '®', '©', 'SP.', '’', ',', ']{', 'ﬁ}']
    common_correct_char = ['-', '8', '8', '4', '69', '89', 'SP-', '', '', ' ', '753']
    text = replace_SCharToDigit(text, common_error_char, common_correct_char, isarray=True)
    split = text.split('/')
    txtlist1 = []
    txtlist = []
    for i in range(0, len(split)):
        if split[i] == '':
            pass
        else:
            txtlist1.append(split[i].strip())

    for j in range(len(txtlist1)):
        if not txtlist1[j] == '':
            if len(txtlist1[j]) < 2:
                pass
            else:
                txtlist.append(txtlist1[j])

    print(txtlist)
    return txtlist

def SharpenImage(img):
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    img = cv2.filter2D(img, -1, kernel)
    filename1="a1.png"
    cv2.imwrite(filename1, img) 
    return img


def get_CropTextBoxData(img2gray):
    img2gray = func_PreProcessCropTextBox(img2gray)
    img2gray = SharpenImage(img2gray) 
    h, w = img2gray.shape[:2]
    new_img = cv2.resize(img2gray, (int(w * 1.8), int(h * 1.6)))
    info = func_TesseractOCR(new_img)
    #excel_data = make_ExcelData(info)
    
    #print(info)
    return info 

def get_ProductTextData(img2gray):
    h, w = img2gray.shape[:2]
    img = cv2.bitwise_not(np.zeros((20, 3 * w + 80), np.uint8))
    for i in range(3):
        crop = img2gray[h - 20 * (3 - i):h - 20 * (2 - i), 0:w]
        img[0:20, (w + 40) * i:w * (i + 1) + 40 * i] = crop
    cv2.imwrite("ab.png",img)
    ret, thresh = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)
    dilated = cv2.erode(thresh, None, iterations=5)
    dilated = cv2.bitwise_not(dilated)
    cv2.line(dilated, (0, 0), (3 * w, 0), (0, 0, 0), 2)
    cv2.line(dilated, (0, 18), (3 * w, 18), (0, 0, 0), 2)
    contours, _ = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnt = 0
    boxes = []
    ref_boxes = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if h > 10:
            ref_boxes.append([x, w])

    ref_boxes.sort(reverse=True)
    for box in ref_boxes:
        if box[1] < 60:
            boxes.append(box)
        else:
            break
    boxes.sort(reverse=False)
    text = []
    for k in range(len(boxes)):
        b = boxes[k]
        crop = img[2:18, b[0] + 3:b[0] + b[1] - 3]
        crop = cv2.resize(crop, (b[1] * 2, 32))
        crop = SharpenImage(crop)
        base_img = cv2.bitwise_not(np.zeros((128, 128), np.uint8))
        base_img[48:80, 10:10 + b[1] * 2] = crop
        base_img = cv2.cvtColor(base_img, cv2.COLOR_GRAY2RGB)
        dvalue = mYD.detect_object(base_img, cfgfile, wgtfile, clsfile, 128, 0.5)
        if not dvalue == '0':
            if dvalue == '':
                pass
            else:
                text.append(dvalue)
    
    #print(text)
    return text

def get_ProductNoQtyVal(text):
    pdt = text.split('-')
    if len(pdt) > 1:
        if len(pdt) > 2:
            pdt_No = int(pdt[0])
            pdt_Qty = int(pdt[(len(pdt) - 1)])
        else:
            pdt_No = int(pdt[0])
            pdt_Qty = int(pdt[1])
    else:
        val = int(pdt[0])
        if val < 210:
            pdt_No = int(val / 10)
            pdt_Qty = val % 10
        else:
            pdt_No = int(val / 100)
            pdt_Qty = int(val % 100)
    #print('pdt', pdt_No, '/', pdt_Qty)
    return (pdt_No, pdt_Qty)


def make_fromPdtToEnd(info):
    data = []
    total = 0
    N = len(info)
    if N == 0:
        for c in range(24):
            data.append('-')

    else:
        if len(info[(N - 1)]) < 3 and int(info[(N - 1)]) < 21:
            for i in range(N - 1):
                pdt_No, pdt_Qty = get_ProductNoQtyVal(info[i])
                data.append(str(pdt_No))
                data.append(Product_Name[pdt_No])
                data.append(str(Product_Rate[pdt_No]))
                data.append(str(pdt_Qty))
                total = total + Product_Rate[pdt_No] * pdt_Qty

            for a in range(N - 1, 5):
                for b in range(4):
                    data.append('-')

            discount = int(info[(N - 1)])
        else:
            for i in range(N):
                pdt_No, pdt_Qty = get_ProductNoQtyVal(info[i])
                data.append('' + str(pdt_No))
                data.append('' + Product_Name[pdt_No])
                data.append('' + str(Product_Rate[pdt_No]))
                data.append('' + str(pdt_Qty))
                total = total + Product_Rate[pdt_No] * pdt_Qty

            for a in range(N, 5):
                for b in range(4):
                    data.append(' -')

            discount = 0
        dis_amount = round(total * (100 - discount) / 100, 2)
        data.append('' + str(round(total, 2)))
        if discount == 0:
            data.append(' -')
        else:
            data.append('' + str(discount) + '%')
        data.append('' + str(dis_amount))
        data.append('' + convert_DigitToWord(dis_amount))
    data.append('N.A.')
    return data

def convert_DigitToWord(num):
    num = int(num * 100)
    text = ''
    d1 = int(num / 100000)
    d2 = int(num % 100000 / 10000)
    d3 = int(num % 10000 / 1000)
    if d1:
        text = text + one_unit[d1] + ' Thousand'
    elif d2:
        text = text + ' ' + one_unit[d2] + ' Hundred'
    elif d3 > 1:
        text = text + ' ' + ten_unit[d3]
        d4 = int(num % 1000 / 100)
        if d4 > 0:
            text = text + ' ' + one_unit[d4]
        else:
            d4 = int(num % 1000 / 100)
            text = text + ' ' + one_unit[(d3 * 10 + d4)]
    else:
        text = text + ' Dollars and '
        if int(num % 100) == 0:
            text = text + ' No'
        else:
            d5 = int(num % 100 / 10)
            if d5 > 1:
                text = text + ten_unit[d5]
                d6 = int(num % 10)
                if d6 > 0:
                    text = text + ' ' + one_unit[d6]
            else:
                d6 = int(num % 10)
        text = text + one_unit[(d5 * 10 + d6)]
    text = text + ' Cents'
    if text.startswith(' '):
        text = text[1:]
    return text


def func_CropColumnTextBox(fname, img2gray):
    global file_row
    global row
    ret, mask = cv2.threshold(img2gray, 200, 255, cv2.THRESH_BINARY)
    image_final = cv2.bitwise_and(img2gray, img2gray, mask=mask)
    ret, new_img = cv2.threshold(image_final, 200, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 1))
    dilated = cv2.dilate(new_img, kernel, iterations=2)
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    BBoxes = [cv2.boundingRect(c) for c in contours]
    Boxes = sorted(BBoxes, key=(lambda BBoxes: BBoxes[1]), reverse=False)
    for b in Boxes:
        if b[3] < 90:
            pass
        else:
            crop = img2gray[b[1] + mg:b[1] + b[3] - mg, b[0] + 2 * mg:b[0] + b[2] - 2 * mg]
            
            if cancel == True:
                break
            #func_Pause_Resume()
            print(file_row)
            data1 = get_CropTextBoxData(crop)
            all_list.append(data1)

            #data1=correct_data(data1)
            #print(data1[9:18])
            pdt = get_ProductTextData(crop)
            #print(pdt)
            if len(pdt) > 6:
                pdt1 = pdt[:6]
                pdt2 = pdt[6:len(pdt)]
                data21 = make_fromPdtToEnd(pdt1)
                data22 = make_fromPdtToEnd(pdt2)
                #func_WriteExcelData(fname, data1, data21)
                row += 1
                file_row += 1
                #return data1,pdt,data21
                #func_WriteExcelData(fname, data1, data22)
                row += 1
                file_row += 1
            else:
                data2 = make_fromPdtToEnd(pdt)
                #return data1,pdt,data2
                #func_WriteExcelData(fname, data1, data2)
                print(len(data2),1)
                prod_list.append(data2)
                row += 1
                file_row += 1
           
              