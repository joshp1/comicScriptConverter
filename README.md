<<<<<<< HEAD
8/10-2023:
cleaned up repository. and added the options.
you can now run using .ccxmlc -i input.xml -o output.fountain -f fountain
also --help or -h for a help menu.
Still need to clean this up and stop using it as a long. I'll b getting to the point where I should of went public.

8/11SS-2023:
I'm tsting if this changes the pages script if so I have a idea. fdfasdf
=======
# Comic Script Converter
Thank you for using my converter. If you like changing your script formats or have clients that want deferent ones. Like some that want docx others odt ext. You can use the XML Script I came up with then convert it to what ever format needed or you want.

## Features
- Export into ODT (Open Document) format
- Export into Fountain (Markdown) format
- Export Docx format
- Export into simple unformated text.
- View script via terminal

## Requirements
I'm not tested installing this yet but it's made with python. The libraries I used are Ncurses, ODFpy, python-docx, and reportLab.

## Known issues
I'm sure there are a lot. So if you test it please report it.
- The biggest issue is formating.
- It needs a makefile to install the script and download libraries
- You have to manually install it.

## Instructions

If I see people using the app I'll make a tutorial for the scripting language but once I get the DTD made you'll see it's pretty straight forward.

but write the script name it what ever you like.xml

Then say you want it in fountain language

`csxmlc -i script_file.xml -o script_file.fountain -f fountain`

in the directory it was ran. you'll have a script_file.fountain file.

## About
I have a move between formats a lot when making my comics. So instead of having to rewrite everything I made a XML script that I'll write the script in. then export it to what ever I feel like that time.

## Guidelines
If you work on this make a branch and put your edits or what ever in that.Try to keep the code as clean as possible and leave plenty comments.

## Release notes

- 0.0.1 - I got it functioning. the output don't look pretty but it works.
>>>>>>> bdf5608 (Fixed readme)
