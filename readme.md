<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="resources/repo_img/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center"><b>Bezier curves editor</b></h3>
</div>

# Table of Contents

- [About](#about)
  - [Demo](#demo)
- [Getting Started](#getting-started)
- [Features](#features)
  - [Editor](#editor)
  - [Typing Program](#typing-program)
- [Process](#process)
- [License](#license)

# About

A Bézier curve editor created for a contest for participants of a numerical analysis course during my studies at the University of Wrocław.  

The goal of the competition was to develop a font editing program, design a font from scratch, and write a program that allows typing with the created font.  
The typing program was integrated with the editing program.  

### Demo  
**You can watch a video showcasing the program in action by clicking the link below:** 
[YouTube Demo](https://youtu.be/KqQhJ1v5JqQ)

![home](https://i.ibb.co/mcYSQKH/obraz-2024-02-10-132930174.png)

![letter_1](https://i.ibb.co/WG44XBd/letter-grid.png)

![letter_2](https://i.ibb.co/2yZ4rCb/letter-no-grid.png)

![first_photo](https://i.ibb.co/1bnL578/curve-grid-no-letter.png)  

![second_photo](https://i.ibb.co/BfswsYw/edit-off-curve-only.png)  

![third_photo](https://i.ibb.co/kqCSNmW/edit-on-curve-only.png)

![typing](https://i.ibb.co/JmNL9np/obraz-2024-02-05-174625660.png)

# Getting Started  

Download the ```dist``` folder and run ```run.exe```.  

*Note: The `.exe` file was compiled on a Windows machine using Python 3.10.5. The same configuration is recommended.*  

While in the main menu of the editing program, you can load letters created for the contest by clicking ```Load Shape``` and selecting a JSON file from the ```letters_json``` folder.  
It is also possible to load a background by clicking ```Load Background``` and selecting an image from the ```letters_raw_extracted``` folder.  

By clicking ```Type```, you open a view for typing with the letters I designed for the contest.  

# Features

Beside visible UI buttons you can use the following keyboard shortcuts:

### Editor
- **LMB** – Adds a new point to the currently edited curve.  
- **RMB** – Drags a point of the currently edited curve.  
- **E** – Changes the currently edited curve to the one closest to the current cursor position.  
- **N** – Creates a new curve with its first point the same as the last point of the currently edited curve.  
- **2** – Creates a new curve while ensuring continuity of the second derivative (both the first and second derivatives are continuous).  
- **Space** – Deletes the point on the currently edited curve that is closest to the current cursor position.  

### Typing

- ```Tab``` - cursive on/off

# Process

This paragraph provides a brief overview of how the font was created.  

The first step was to sketch the letters using a graphics tablet on the [Miro](https://miro.com) platform. All the letters were then collected in the ```letters_raw``` folder.  
Next, all the screenshots were processed to match the background resolution of the editing program. Here, Photoshop was used, and the results were stored in the ```letters_raw_extracted``` folder.  
After that, each letter was loaded into the editing program and carefully recreated using Bézier curves. The finalized letters were stored in the ```letters_json``` folder.  

# License

[MIT](https://choosealicense.com/licenses/mit/)
