import sys, getopt, curses
import xml.etree.ElementTree as ET

# csc - comic script converter - Python script that converts csxml into fountain or html right now hopefully later more.

def extract_text(element):
    return element.text.strip() if element is not None and element.text else ""

def convert_to_fountain(root, output_file):
    with open(output_file, "w") as f:
        f.write("Title: " + extract_text(root.find("./title")) + "\n")
        f.write("Author: " + extract_text(root.find("./author")) + "\n")
        f.write("Draft: " + extract_text(root.find("./draft")) + "\n")
        f.write("Date: " + extract_text(root.find("./date")) + "\n\n")

        for page in root.findall("./script/page"):
            page_num = page.get("num")
            f.write("INT. COMIC PAGE {}\n\n".format(page_num))

            for panel in page.findall("./panel"):
                panel_num = panel.get("num")
                f.write("PANEL {}\n\n".format(panel_num))

                for element in panel:
                    tag_name = element.tag
                    text = extract_text(element)
                    
                    if tag_name == "character":
                        name = element.get("name")
                        f.write("    {}\n   {}\n\n".format(name.upper(), text))
                    elif tag_name == "narrator": # Honestly I'll probably drop the Narrator tag
                        f.write("    {}\n".format(text))
                    elif tag_name == "action":
                        f.write("{}\n".format(text))
            f.write("\n")

    print("Conversion to Fountain complete. Result saved in '{}'".format(output_file))

def convert_to_html(root, output_file):
    # Modify this function to generate HTML output
    with open(output_file, "w") as f:
        f.write ("<html>\n\t<head>\n\t\t</title>\n\t\t\t")
        f.write (extract_text(root.find("./title")) + "\n")
        f.write ("\n\t\t</title>\n\t</head>\n\t<body>\n")
        
        # Copy the script above to edit later to HTML

        for page in root.findall("./script/page"):
            page_num = page.get("num")
            f.write("<h1>INT. COMIC PAGE {}</h1>\n".format(page_num))

            for panel in page.findall("./panel"):
                panel_num = panel.get("num")
                f.write("PANEL {}\n\n".format(panel_num))

                for element in panel:
                    tag_name = element.tag
                    text = extract_text(element)
                    
                    if tag_name == "character":
                        name = element.get("name")
                        f.write("    {}\n   {}\n\n".format(name.upper(), text))
                    elif tag_name == "narrator": # Honestly I'll probably drop the Narrator tag
                        f.write("    {}\n".format(text))
                    elif tag_name == "action":
                        f.write("{}\n".format(text))
            f.write("\n")
        f.write ("</body></html>")
    print ("HTML conversion durn")
def help():
    print("Usage: python script_name.py [options]")
    print("Options:")
    print("  -i, --input     Input XML file")
    print("  -o, --output    Output file")
    print("  -f, --format    Output format (html/fountain)")
    print("  -l, --last_name Last name (optional) I need to erase this. you will never have a need for it. Just a old test left over.")
    print("  -h, --help      Show this help message")

def view(root, parsed_xml):
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    try:
        stdscr.addstr("Press any key to view the parsed XML:\n")
        stdscr.refresh()
        stdscr.getch()

        stdscr.clear()
        stdscr.addstr(extract_text(root.find("./title")))
        stdscr.addstr("Parsed XML:\n\n")

        # Define the maximum length of each chunk
        chunk_size = 600

        for i in range(0, len(parsed_xml), chunk_size):
            chunk = parsed_xml[i:i + chunk_size]
            stdscr.addstr(chunk)
            stdscr.refresh()
            stdscr.getch()
            stdscr.clear()

    finally:
        curses.endwin()

# ... previous code ...
def main():
    first_name = None
    last_name = None
    output_format = None
    input_file = None
    output_file = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:l:o:hi:v", 
                                   ["help", "format=", "output=", "input=", "view"])
    except getopt.GetoptError as e:
        print("Error:", e)
        return
    
    for opt, arg in opts:
        if opt in ("-h", '--help'):
            help ()
            return
        
        if opt in ('-f', '--format'):
            output_format = arg.lower()
        elif opt in ('-o', '--output'):
            output_file = arg
        elif opt in ('-i', '--input'):
            input_file = arg
        elif opt in ('-v', '--view'):
            print (input_file)
            tree = ET.parse(input_file)  # Parse the XML file
            root = tree.getroot()  # Get the root element

            parsed_xml = ET.tostring(root, encoding='unicode', method='xml')
            view(root, parsed_xml)
            

    if input_file is None or output_file is None or output_format is None:
        print("Usage: python script_name.py -i input_file.xml -o output_file -f format (html/fountain)")
        return

    tree = ET.parse(input_file)
    root = tree.getroot()

    if output_format == "fountain":
        convert_to_fountain(root, output_file)
    elif output_format == "html":
        convert_to_html(root, output_file)
    else:
        print("Invalid output format. Please choose 'html' or 'fountain'.")

if __name__ == "__main__":
    main()