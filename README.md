# PDF utility script
The PDF utility script is designed to perform a set of operations on images and pdf files. The idea comes from a 
blog post I wrote as reference on how to compress and merge pdf files via terminal using the gostscript, you can
find it here[https://fabiopacifici.com/ubuntu-using-the-ghost-script-to-compress-pdf-files/]
- Converts images in pdf files
- resize images to a given size
- merges pdf files into a single file
- compress a pdf file to save disk space
- compress all pdf files in a given folder


## System requirements:
The pdf utility script uses the Python Pillow package to manipulate images and 
the adobe gost script to work on pdf files. If these are not present in your system 
you will need to install them.

- Gostscript[https://www.ghostscript.com/download/gsdnld.html]
- PILLOW[https://pillow.readthedocs.io/en/stable/installation.html#basic-installation]


## How to use PDFutility
To use the script directly simply run the app.py file inside the terminal

```bash
./app.py
```

### Run the script from anywhere
To run the script from anywhere, we need to add it to the bin directory. For ease of use we will rename the file
as pdfutil.py when moving it.

run the following inside the terminal:
```bash

sudo mv app.py /bin/pdfutil
sudo chmod ug+x /bin/pdfutil

```
Now we can run our script like so:

```bash

pdfutil
```

