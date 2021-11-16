from PIL import Image
import pytesseract
from translate import Translator
from PIL import ImageFont, ImageDraw, Image
import os

"""
Python 3 script file for obtaining an image file with text from a user
and using the tesseract OCR engine to generate a .txt file from the image.
The .txt file is then passed to a translator that translates the text to
English and outputs the translation as both a .txt file and a JPG image file.
"""

# The next line may not be needed. Uncomment if needed.
# It is needed if tesseract is not in your PATH
# (Check path for tesseract and modify the line below if needed)
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'


def ocr_core(filename, language):
    """Handles the core OCR processing of the input image.

    :param filename: the name of the input image file
    :type filename: string
    :param language: the choice of input file language
    :type language: string
    """
    choice = 0
    if language == '1':
        choice = 'chi_sim'
    elif language == '2':
        choice = 'deu'
    elif language == '3':
        choice = 'hun'

    text = pytesseract.image_to_string(Image.open(filename), lang=choice)
    return text

def writefile(image_path, strstr):
    """Writes text extracted from image into a txt file named "script.txt" 
    which is saved in the same path as the input image file.

    :param image_path: the path of the input file obtained from the user
    :type image_path: string
    :param strstr: string of words that have been generated by OCR
    :type strstr: string
    """
    wordlist = strstr.split()
    with open(image_path + '/script.txt', 'a') as f:
	    f.writelines("\r".join(wordlist))

def translate_text(image_path, imagename, language):
    """Takes lines of text extracted from txt file and translates them,
    outputs translated version into a txt file called "translated.txt"
    and an image file with the translated text called Capture.JPG.

    :param image_path: the path of the input file obtained from the user
    :type image_path: string
    :param imagename: name of the input image file
    :type imagename: string
    :param language: the choice of input file language
    :type language: string
    """
    # sets target language and input language for translator
    choice = 0
    if language == '1':
        choice = "zh"
    elif language == '2':
        choice = 'de'
    elif language == '3':
        choice = 'hu'

    translator = Translator(to_lang="en", from_lang=choice)

    # opens the OCR output file and reads each line into contents
    with open(image_path + '/script.txt', encoding='utf-8') as f:
        contents = f.readlines()

    # sets the dimensions and background color for the new image object
    oldimg = Image.open(image_path + "/" + imagename)
    # Grab the size of the input image
    # Later we can choose a font size depending on input image size
    width, height = oldimg.size
    # enlarge the output image so text does not need to be tiny (for small input files)
    # width *= 2
    # height *= 2

    # Grab a color sample, to reproduce the background in the output image
    # The code obtains an rgb tuple at position (x,y)
    # grabs pixel from upper left corner
    background = oldimg.getpixel((5, 5))

    newimg = Image.new(mode="RGB", size=(width, height), color=background)

    # Generates a txt file and JPG image file from the translated txt file
    with open(image_path + '/translated.txt', 'a') as n:
        movedown = 20   # variable to help draw multiple text lines to image. This is initial vertical position
        for line in contents:   # iterates thru each line of text in "contents"
            # translate each line and write to file
            n.writelines(translator.translate(line) + "\n")
            draw = ImageDraw.Draw(newimg)
            # font size 20 should be scaled for image size
            font = ImageFont.truetype("arial.ttf", 20)
            # In the next line, first 2 numbers are pixels to right and down of upper corner
            draw.text((5, movedown), translator.translate(line), fill=(0, 0, 0), font=font)  # font color set to black
            movedown += 25     # This is the line spacing that works well for 20 pt font
        newimg.save("Capture.JPG")
        newimg.show()  # I don't think this works

# Change the translator provider
# Default is mymemory but it limits the number of translations per day.
# Template code to change provider:
# secret = '<your secret from Microsoft or DeepL>'
# translator = Translator(provider='<the name of the provider, eg. microsoft or deepl>', to_lang=to_lang, secret_access_key=secret)


# Obtain input path and file name from the user

path = input('Enter a file path: ')
userfile = input('Enter a file name: ')
#OS library methods that check if a filepath and a file exist
isPathExist = os.path.exists(path)
isUserFileExist = os.path.exists(userfile)
directoryValid = os.path.isdir(path)
truthCondition1 = 0
truthCondition2 = 0
truthCondition3 = 0


#checks if directory is valid
if(directoryValid == False):
    print("Error: invalid directory, exiting program")
   

#checks for filepath validity
elif(isPathExist == False ):
    print("Error: invalid file path, exiting program")

#checks for file existance
elif(isUserFileExist == False):
    print("Error: invalid File, exiting program")
 
else:
    #ensures proper input by using isnumeric method to see if input is completely numerical, if input is numerical and one of the specified 
    #numbers, the input is then cast to an int to avoid unnecessary looping then recast as a string so the translation can take place
    print("You have 3 choices for input language. Enter 1 for Chinese, 2 for German, or 3 for Hungarian.")
    inlanguage = (input('Your choice: '))
    if(inlanguage.isnumeric() == True and (int(inlanguage)==1 or int(inlanguage) ==2 or int(inlanguage)==3)):
        inlanguage = int(inlanguage)
    else:
        #Continuously loops until user enters proper language choice, use isnumeric() method and int casting 
        #to do checks and ensure program doesn't crash if improper input is detected
        while(inlanguage != 1 or inlanguage !=2 or inlanguage !=3):
            print("Error: please select specified numbers to translate")
            print("You have 3 choices for input language. Enter 1 for Chinese, 2 for German, or 3 for Hungarian.")
            inlanguage = (input('Your choice:  '))
            if(inlanguage.isnumeric() == True and (int(inlanguage)==1 or int(inlanguage) ==2 or int(inlanguage)==3)):
                inlanguage = int(inlanguage)
                break
        
    inlanguage = str(inlanguage)
    print('\n')

    print("******Starting******")

    # Perform OCR on the input image file and let user know when finished this step
    text = ocr_core(path + "/" + userfile, inlanguage)
    writefile(path, text)
    print("OCR of image " + userfile + " is done.")

    # Perform the translation step
    print("Now performing the translation.")
    print("The bigger your file, to longer the wait...")
    translate_text(path, userfile, inlanguage)

    print("~~~~~~Finished~~~~~~")
