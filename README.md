![Personal-Assitant banner image](resources/README/github%20banner%20image.png)

# Aims of The Project:

The goal is to create an artificial assistant that doubles as a friend... 😢

# Project Road Map 🛣:

- ## Stage 1:
  Create the methods of the PersonalAssistant class that are responsible for the lookup and search functionality of the
  project.

- ## Stage 2:
  For each ```PersonalAssistant``` method, make its return value in the form of pseudo-human sentence.

- ## Stage 3:
  Using ```Yake``` library extract keywords from the text inserted, analyze the text, and trigger
  appropriate ```PersonalAssistant``` method.

- ## Stage 4:
  Assign each method a 'difficulty' score, and depending on the score, insert appropriate conversation filler to the
  sentence, to make the response seem more human.

- ## Stage 5:
  For the ```PersonalAssistant``` class, create 2 new attributes to represent happiness, anger and shyness:
  `````````python
  self.happiness_score
  self.anger_score
  self.shyness_score
  `````````
  The score values range from 0 to 100. Depending on the score of the attributes, answer time and attitude may vary. In
  addition, depending on how high the shyness score is, the chosen avatar may 'blush'.

- ## Stage 6:
    - Create a method to the ```PersonalAssistant``` class that saves the valus of the class attributes to a json file.

    - Create a decorator method that is on every other method of the class, to save the values stored in the class. this
      file would be called ```assistant_data.json```.

    - When Initializing the class, in the ```__init__```, the program checks if the ```assistant_data.json``` file
      exits, then loads the class using those values, else the ```__init__``` method would run normally.

    - Create new method ```__reset_class```, which simply delets the ```assistant_data.json``` file, and re-initializes
      the ```PersonalAssistant``` class.

- ## Stage 7:
  Using a GUI library, ```pyqt``` or ```tkinter```, the front end of the project is constructed. The GUI would basically
  involve:

    1. An Anime girl avatar.
    2. A Background behind the avatar inspired by ***Amadeus*** from  *Steins; Gate*.
    3. Interface buttons
    4. Debug Menu that show the values of all the attributes that belong to the ```PersonalAssistant``` class

  The text is inputted through entery filed the sent to the ```process()``` method of the ```PersonalAssistant``` class.

  <h3 align="center">This Concludes <code>Version 1.0.0</code></h3>

<h4 align="center">All the stages left are not set in stone and will be altered</h4>

- ## Stage 8:
  Using ```OpenCV``` library and possibly ```TensorFlow```, access the webcam and using facial recognition, identify the
  faces of the users of the program and possibly reply according to said person.

  <h3 align="center">This Concludes <code>Version 1.5.0</code></h3>

- ## Stage 9:
    - Add Voice recognition to the application.

    - Add text to speech.

- ## Stage 10:
  Refactor and clean up the code


