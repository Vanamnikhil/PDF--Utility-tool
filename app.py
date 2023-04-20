#!/usr/bin/env python3
from PIL import Image
import subprocess
from subprocess import run
import os, sys

# Utility Functions
def get_images(path):
    img_list = []
    for file in os.listdir(path):
        f, e = os.path.splitext(file)
        if e ==".jpg" or e == ".jpeg" or e == ".png":
            img_list.append(file)

    return img_list


def get_all_pdf_files_as_list(path):
    pdfs = []
    for file in os.listdir(path):
        f, e = os.path.splitext(file)
        if e == ".pdf":
            pdfs.append(file)
    return pdfs


# Resize image to a given size
def resize_image(image, file_name):
    new_w = int(input("Type the new witdth: "))
    new_h = int(input("Type the new height: "))
    resized_image = image.resize((new_w, new_h)).convert('RGB')
    resized_image.save(file_name)
    return resized_image

# Main app functions
# [1] Resize and Convert an image to pdf
def convert_image_to_pdf(image_path: str ):
    """ Converts an image in a pdf file 
    
    str: image_path The path to the image to convert
    """
    with Image.open(image_path) as im:
        f, e = os.path.splitext(image_path)
        file_name = "{}.pdf".format(f)
        print("New image to process, {} in size ".format(im.size))
        answer = input("Do you want to resize? [y/n]")
        if answer.lower() == "y":
            new_img = resize_image(im, file_name)
            print("image size = {}".format(new_img.size))
        else:
            print("image size = {}".format(im.size))
            im.convert('RGB')
            im.save(file_name)
        return file_name

        
# [2] Merge PDF files
def merge_pdf_files(output_file : str, files_to_merge: list):
    """ ### Merges files into a single pdf 
    Accepts three parameters, "path" a string representing the location of the files,
    "output_file" the name of the resulting file from the merge, and a list "files_to_merge"
    that contains all files name that you want to merge.

    path: str The path to the files to merge \n
    output_file : str The name of the final file \n 
    files_to_merge : list A list of files to merge \n
    """

    files = " ".join(files_to_merge)
    print("The files to merge {}".format(files))
    script = "gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -dAutoRotatePages=/None -sOutputFile={} {}".format(output_file, files)
    print("""The script that I am going to run is: 
    {}
    """.format(script))
    command = script.split(" ")
    print("""The command that I am going to run is: 
    {}
    """.format(command))
    subprocess.run(command)
    return output_file


# [3] Compress a PDF file
def compress_pdf(output_file : str, file_to_compress : str):
    """ # Compress a pdf file 
    output_file : str
    file_to_compress : str
    """
    if output_file == "":
        path, file_name = os.path.split(file_to_compress)
        f, e = os.path.splitext(file_name)
        output_file = "{}/{}_compressed{}".format(path, f, e)

    script = "gs -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -sNAME=setting -sOutputFile={} {}".format(output_file, file_to_compress)
    command = script.split(" ")
    print("This is the command that i will run {}".format(command))
    print("I am compressing the file {} into {}".format(file_to_compress, output_file)) 
    try:
        subprocess.run(command)
        original_file_size = os.path.getsize(file_to_compress)
        final_size = os.path.getsize(output_file)
        saved_size = ((original_file_size - final_size) /1e+6).__round__(2)
        print("Done! I have compressed the file {} and you saved {} Mb".format(file_to_compress, saved_size))
        return output_file
    except FileNotFoundError as e:
        print("Sorry!! There is an error! {}".format(e))



# [4] Compress all PDF files
def compress_all_pdf(path : str):
    """ #Compress all pdf files 
    Compress all PDF files in a given path and prints them. All files compressed will
    have a _compressed suffix at the end 
    
    path: str A string that represents the files path
    """
    files = get_all_pdf_files_as_list(path)
    
    for file in files: 
        file_full_path = "{}{}".format(path, file)
        print( "File path: {}".format(file_full_path))
        compress_pdf(output_file="", file_to_compress=file_full_path)
    print("All files Compressed")
    os.chdir(path)
    print(subprocess.run('ls -alt *_compressed.pdf', shell=True))

def main():

    running = True

    while running:

        print(''' Options: 

        [1] : Resize/Convert images in PDF files
        [2] : Merge PDF files
        [3] : Compress a PDF file
        [4] : Compress all PDF files 
        
        ''')

        option = input("Select on option [1/2/3/4], type [q] to exit: ")

        if option.lower() == '1':
            img_path = input('Type the path where the images are located. ie [/mtn/c/Users/UserName/Photos/] ') 
            images = get_images(img_path)
            print("################################################")
            for img in images: 
                pdf_converted_file = convert_image_to_pdf('{}{}'.format(img_path, img))
                print("Conversion Complete! File {} converted in file {}".format(img, pdf_converted_file))
            print("################################################")

        if option.lower() == '2':
            
            pdf_files_path = input("Type the path where pdf files are located:")
            print("Searching PDF files inside {}".format(pdf_files_path))
            list_pdf_files = get_all_pdf_files_as_list(pdf_files_path)
            print(list_pdf_files)
            output_file = input("Type the name of the final file: ")
            print("All files in {} will be merged in {}".format(list_pdf_files, output_file))
            os.chdir(pdf_files_path)
            merge_pdf_files(output_file, list_pdf_files)

        if option.lower() == '3':
            output_file = input("Type the output file name ie. [sample_compressed.pdf] ")
            filename = input("Type the path of the file that you want to compress. ie. sample.pdf ")
            compress_pdf(output_file, filename)

        if option.lower() == '4':
            files_path = input("Type the path where your pdf files are located. ie [Desktop/pdf_files/]")
            compress_all_pdf(files_path)

        if option.lower() == "q":
            print("Goodbye")
            running = False
            exit()


if __name__ == "__main__":
    main()