#!/usr/bin/python3
import sys, os, re
import urllib.request # To receive the html source code

### Check for file name and if file already exist ###
def checkFileName():
    # Default file name
    fileName = "output.html"
    # Check if a file named output.html already exist
    # Get the current directory
    dirPath = os.path.dirname(os.path.realpath(__file__))
    completeFileName = dirPath + "\\" + fileName
    # As long the file exist ask to overwrite the old one or rename the new one
    while os.path.isfile(completeFileName):  
        overwrite = input("The file " + fileName + " already exists. Do you want to overwrite the old file or rename the new one? (o)verwrite, (r)ename, (n)othing\n")
        if overwrite == "O" or overwrite == "o" or overwrite == "overwrite" or overwrite == "Overwrite":
            # Delete old file
            os.remove(completeFileName) 
        if overwrite == "R" or overwrite == "r" or overwrite == "rename" or overwrite == "Rename":
            fileName = input("New file name: \n")
            completeFileName = dirPath + "\\" + fileName
            # Add HTML extension if it was not included
            if completeFileName[-4:] != "html":         
                completeFileName += ".html"
        if overwrite == "N" or overwrite == "n" or overwrite == "nothing" or overwrite == "Nothing":
            completeFileName = ""
    return completeFileName

### Extract the identifier of the YouTube URL and embed it into an iframe###    
def youTubeExtract(srcURL):
    # Get the identifier out of the URL
    ident = srcURL.split("?v=",1)[1] 
    ident = ident[:11]
    # If it is a youtube link just embed into an iframe
    code  = '<iframe title="YouTube video player" class="youtube-player" type="text/html"\n'
    code  += 'width="1440" height="810" src="http://www.youtube.com/embed/' + ident + '"\n'
    code  += 'frameborder="0" allowFullScreen></iframe>\n'
    return code

### Request the HTML source code of the given URL and extract the source### 
def defaultExtract(srcURL): 
    try:
        srcCode = urllib.request.urlopen(srcURL)
        # HTML source code will be read as bytearray
        srcCodeBytes = srcCode.read()
        # Convert to UTF8 and ignore errors
        srcCodeString = srcCodeBytes.decode('utf8', 'ignore')
        #Close the request
        srcCode.close()
    except Exception as ex:
        return ""

### Main function which receives the source URL as parameter ###
def main(srcURL):    
    # URL with the source   
    print("Source URL: " + srcURL)
    
    # Get the file name and terminate if it is empty
    completeFileName = checkFileName()
    if completeFileName == "":
        print("Script terminated!")
        return
    
    # Is it a known website or default
    if "youtube.com/" in srcURL:
        code = youTubeExtract(srcURL)
    else:
        code = defaultExtract(srcURL)

    # Check if the source could be extract and terminate if not
    if code == "":
        print("Script terminated!")
        return
    
    
    print(completeFileName)
    
    # Open the output file
    dstHTML = open(completeFileName, "w")
    # Write the output file
    dstHTML.write(code)
    # Close the output file
    dstHTML.close()
    print("Script terminated successfully")
    os.system("pause")
    
if __name__ == "__main__":
    # Check if just one parameter was submitted
    if len(sys.argv) != 2:
        print("Please enter exact one input URL as parameter.")
    else:
        main(sys.argv[1])