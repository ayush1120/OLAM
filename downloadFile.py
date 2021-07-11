import requests  


file_url = "http://1.droppdf.com/files/5iHzx/automate-the-boring-stuff-with-python-2015-.pdf"
path= '.'
def download(url = file_url, fileName='dataset.zip', path=path):
    filePath = os.path.join(path, fileName)
    r = requests.get(url, stream = True)  
    with open(filePath, "wb") as file:  
        for block in r.iter_content(chunk_size = 1024): 
            if block:  
                file.write(block)  