from email.mime import image
import os
import sys
import fitz

#*** Run Commmand ****
#python extractImagesFromPdf.py O:\paye-employers-documentation-v2\paye-employers-documentation-v2-python-scripts\PITSelfServiceGuide.pdf

#Create ouput directory
print('Script Parameters', sys.argv)
firstParameter = str(sys.argv[1])
# print(firstParameter)

# Define the input PDF and output Markdown filenames
pdf_filename = firstParameter
directoryPath = os.path.dirname(pdf_filename)
# print(directoryPath)
fileNameExtn = os.path.basename(pdf_filename)
fileName = os.path.splitext(fileNameExtn)[0]
# print(fileName)
imageDirectory = os.path.join(directoryPath,fileName,"images")
print(imageDirectory)

if not os.path.exists(imageDirectory):
    os.makedirs(imageDirectory)
    print(fileName + "images created store @ " + imageDirectory)
    

#open PDF file
doc = fitz.open(firstParameter)


#extracts images from each page
image_counter = 1
for page_num in range(len(doc)):
    page = doc[page_num]
    images = page.get_images(full=True)
    for img_index, img in enumerate(images):
        xref=img[0]
        base_images = doc.extract_image(xref)
        image_data = base_images["image"]
        # image_filename = os.path.join(imageDirectory, f"image({image_counter}).png")
        # imageName = "image_"+str(image_counter)+".png"
        imageName = f"image_{image_counter}.png"
        print(imageName)
        image_filename = os.path.join(imageDirectory, imageName)

        #save the image data as a file
        
        with open(image_filename, "wb") as image_file:
            image_file.write(image_data)
        print(f"Saved image {image_counter} from page {page_num + 1} as {image_filename}")
        image_counter += 1

print(f"All images have been extracted and saved to '{imageDirectory}'!") 