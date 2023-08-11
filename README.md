# Comic Script Converter
I'm still in the prototyping stage I just wanted to get the git server up. and accedently made it public. So if you use this. It will change alot and the syntax will be a mess.

I use fountain to make comic scripts all the time but markdown isn't really my favorite mostly because you have to find a cheat sheet. Markup has the DTD which can also be used to validate the document. (I know it's it's main purporse)

example of use (This is what I want the final named to be)

csxmlc -f fountain -s script.xml -o script.fountain

for fountain output

say you want to PDF

csxmlc -f pdf -s script.xml -o script.pdf

It'll then convert to latex which will compile the pdf

Also figure the out put may be redundant so just the output format may be enough

example:

csxml -f fountain -i script.xml

output:

script.fountainS

8/10-2023:
cleaned up repository. and added the options.
you can now run using .ccxmlc -i input.xml -o output.fountain -f fountain
also --help or -h for a help menu.
Still need to clean this up and stop using it as a long. I'll b getting to the point where I should of went public.

8/11SS-2023:
I'm tsting if this changes the pages script if so I have a idea. fdfasdf
## TODO

 - [x] Rewrite the files to have better names
 - [ ] Add git milestones for versioning.
 - [ ] Rewrite the README  to look more professional.
 - [x] mycomicmarkuplanguage.xml needs a shorter named and context cleaned up.
 - [ ] ccxmlc needs to be renamed to csxmlc