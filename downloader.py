import urllib.request as requests   
import urllib.error as exceptions
# urllib belongs to the python standard library but
# the external module "requests" is preferable
import os

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from animals import Animal

def download(animal: Animal) -> int:
    """
    This function attempts to reach a photo of the animal 
    online and to pull it down on a jpg local file

    Returns
    -------
     0 - successful download and image display
     1 - successful display
    -1 - an error occured
    """
    image = f"{animal.name.replace(' ', '-').lower()}.jpg" 
    # Carcharodon carcharias -> "carcharodon-carcharias.jpg"
    image_path = os.path.join("images", image)
    # On Windows -> "...\\images\carcharodon-carcharias.jpg"
    # On MacOS or Linux -> ".../images/carcharodon-carcharias.jpg"

    choice = 'y' # initial value set to 'y' to avoid to enter the second conditional block

    if os.path.exists(image_path): # checks if wanted image is already saved locally
        choice = input("Image already existing. Download again (Y/N)? ")
    
    if choice.lower() not in ['y', 'yes']: #every not y/yes choice will be considered a no
        plt.figure(image_path) # opens a matplotlib window with a costumized heading name
        # display a local image
        img = mpimg.imread(image_path)
        plt.imshow(img)
        plt.axis('off')
        return 1 # succesful opening

    try:
        # try to download bytes from a url
        request = requests.urlopen(f"https://wir.iucnredlist.org/{image}")
        if not os.path.exists("images"):
            os.makedirs("images") # makes a folder named "images" when not already existent
        
        try: # try to write bytes on a binary file
            with open(image_path, 'wb') as output:
                output.write(request.read())
            print(f"Image successfully downloaded as \'{image}\'")
            # display image as soon as correctly downloaded
            plt.figure(image)
            img = mpimg.imread(image_path)
            plt.imshow(img)
            plt.axis('off')
            return 0 #successful download and display
        
        ### handle errors mostly due to incorrect paths
        except FileNotFoundError:
            print("Error in saving the image after download")
            print("FIleNotFoundError")

    ### exceptions handling
    except exceptions.HTTPError:
        # can be raised by a inexistent url
        print("Image not found")
        print("HTTP Error 403: Forbidden")
    except exceptions.URLError: 
        # can be raised by a SSL bad request, by an incorrect 
        # domain name or by a poor Internet connection
        print("Attempt to reach the image at an invalid or unsecure URL")
        print("Check your Internet connection before continuing")
    except: # generic error
        print("Something went wrong. Check your internet connection")
    
    return -1 # failed

# test library
if __name__ == '__main__': 
    Animal.species = pd.read_csv("simple_summary.csv")
    Animal.names = pd.read_csv("common_names.csv")
    download(Animal('White shark'))
