# Pokemon Grading Center
Pokemon Grading Center is a tool created in hard time for people that want to grade their cards. Most of well known grading companies are 
full of orders right now what results in delays and high prices. 

# Current supported features
## - Card Recognision
All you need is image of your card. Current **database contains >99%** of all english Pokemon cards. Image similarity is based on distance 
between 2 images' hashes. Image hashes are brought by [ImageHash](https://github.com/JohannesBuchner/imagehash). Demo:

https://user-images.githubusercontent.com/45520494/126075393-d690d580-c389-4cd1-9223-050ae741fe3c.mp4

## - Auto Card Centering Ratio
Here high resolution image is very important to get as accurate result as possible. To detect card border i used openCV color detection and 
then I used some filters to find inner and outside contours. Demo: 

https://user-images.githubusercontent.com/45520494/126075952-3398f449-5f41-414b-8ae7-c49082b60357.mp4


## - Manual Card Centering Ratio
Same as above but instead of detecting border and contours by program you type coordiantes by yourself. As a result you receive same 
printed output as from auto detection. Demo: 

![manual showcase](https://user-images.githubusercontent.com/45520494/126076184-d00977c3-14e6-48b5-88fe-50235904ed2b.png)

# Installation
* Clone or download repository to your local storage
* Make sure you got Python installed
* Install dependecies typing `pip install requirements.txt` in you terminal
* Run main.py by typing `py main.py` in cloned directory

# Updates and future of the project
### This is more advanced version of my previous [Pokemon OCR](https://github.com/Antonji-py/Pokemon-OCR). I plan to use maybe in some of my future 
projects. Stuff that has to be done is for sure more precised and faster border detection, japaneese cards and surface grading. If you have any issues
you can open and issue on GitHub or dm me on discord Antonji#0127.
