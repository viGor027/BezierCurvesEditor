<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="resources/repo_img/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center"><b>Bezier curves editor</b></h3>
</div>

# Table of Contents

- [About](#about)
- [Getting Started](#getting-started)
- [Features](#features)
  - [Editor](#editor)
  - [Typing Program](#typing-program)
- [Process](#process)
- [License](#license)

# About

Bézier curves editor made for the contest for participants of numerical analysis course during my studies at University of Wroclaw.  

The subject of the competition was to create a font editing program, design a font yourself, and write a program that allows you to type with the created font.

![home](https://i.ibb.co/gPNJrdr/home.png)

![letter_1](https://i.ibb.co/WG44XBd/letter-grid.png)

![letter_2](https://i.ibb.co/2yZ4rCb/letter-no-grid.png)

![first_photo](https://i.ibb.co/1bnL578/curve-grid-no-letter.png)  

![second_photo](https://i.ibb.co/BfswsYw/edit-off-curve-only.png)  

![third_photo](https://i.ibb.co/kqCSNmW/edit-on-curve-only.png)

![typing](https://i.ibb.co/JmNL9np/obraz-2024-02-05-174625660.png)

# Getting started

Create a virtual environment and install:
- [Pygame](https://www.pygame.org)
- [NumPy](https://numpy.org)

You can do this via ```pip install package_name```

If you want to run editor run the ```run.py``` file, and if program for typing then run ```type.py```.  

While in the main menu of editing program you can load letters created for the contest by clicking ```Load shape``` and selecting the json file from the ```letters_json``` folder,
also it is possible to load a background by clicking ```Load background``` and selecting image from ```letters_raw_extracted``` folder.

# Features

Beside visible UI buttons you can use the following keyboard shortcuts:

### Editor

```e``` - changes currently edited curve to curve that is the closest to current cursor position  
```n``` - creates new curve with its first point same as last point of currently edited curve  
```2``` - creates new curve taking care of continuity of second derivative( first and second derivatives are continuous)  
```space``` - deletes point on currently edited curve that is the closest to current cursor position  

### Typing program

```tab``` - cursive on/off

# Process

This paragraph gives a quick insight into how the font was created.  

The first step was to plot the letters using a graphics tablet on the [Miro](miro.com) platform, all the letters were collected to ```letters_raw``` folder.  
Next step was to process all the screenshots to match the background resolution of editing program, here Photoshop helped and the results were stored in ```letters_raw_extracted``` folder.  
After that each letter was loaded to editing program and neatly reproduced with Bézier curves. All the letters were stored in ```letters_json``` folder.

# License

[MIT](https://choosealicense.com/licenses/mit/)