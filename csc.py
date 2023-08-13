import sys, getopt, curses, docx
from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties
from odf.text import H,P,Span, LineBreak
import xml.etree.ElementTree as ET
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# csc - comic script converter - Python script that converts csxml into fountain or html right now hopefully later more.

def extract_text(element):
    return element.text.strip() if element is not None and element.text else ""

def convert_to_pdf(root, output_file):
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    story = []

    styles = getSampleStyleSheet()
    title = extract_text(root.find("./title"))
    story.append(Paragraph(title, styles["Title"]))
    
    for page in root.findall("./script/page"):
        page_num = page.get("num")
        story.append(Paragraph("PAGE {}".format(page_num), styles["Heading1"]))

        for panel in page.findall("./panel"):
            panel_num = panel.get("num")
            story.append(Paragraph("<u>PANEL {}</u>".format(panel_num), styles["Heading3"]))

            for element in panel:
                tag_name = element.tag
                text = extract_text(element)
                
                if tag_name == "character":
                    name = element.get("name")
                    character_style = styles["Heading3"].clone('CharacterStyle', leftIndent=47)
                    c_style = style = styles["Normal"].clone ('CharacterStyle', leftIndent =33)
                    story.append(Paragraph(name.upper(), character_style))
                    story.append(Paragraph(text, c_style))
                elif tag_name == "narrator":
                    story.append(Paragraph(text, styles["Italic"]))
                elif tag_name == "action":
                    story.append(Paragraph(text, styles["Italic"]))

        story.append(Spacer(12, 12))

    doc.build(story)
    print("Conversion to PDF complete. Result saved in '{}'".format(output_file))


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

# Output to ODT. I may convert DC output as this also
def convert_to_odt (root, output_file):
    textdoc = OpenDocumentText()

    boldst = Style(name="Bold", family="text")
    boldprop = TextProperties (fontweight = "bold")
    boldst.addElement(boldprop)
    textdoc.automaticstyles.addElement(boldst)

    
    pa=P(text = "ODT output")
    textdoc.text.addElement (pa)
    pb=P(text =extract_text(root.find("./title")) + "\n")
    textdoc.text.addElement (pb)

    for page in root.findall("./script/page"):
        page_num = page.get("num")
        p=P(text= "Page {}\n".format(page_num))
        p.addElement(LineBreak())
        for panel in page.findall("./panel"):
            panel_num = panel.get("num")
            p.addText(u"_Panel_{}_\n\n".format(panel_num))
            p.addElement(LineBreak())

            # Testing is I can just add a varable and ref that
            plb = p.addElement(LineBreak())

            for element in panel:
                tag_name = element.tag
                text = extract_text(element)
                 
                if tag_name == "character":
                    name = element.get("name")
                    p.addText(u"{}: {}\n\n".format(name.upper(), text))
                    p.addElement(LineBreak())
                elif tag_name == "narrator": # Honestly I'll probably drop the Narrator tag
                    p.addText(u"    {}\n".format(text))
                    plb
                elif tag_name == "action":
                    p.addText (u"{}\n\n".format(text))
                    p.addElement(LineBreak())

        textdoc.text.addElement(p)
        p=P()
        p.addElement(LineBreak())

    textdoc.save (output_file)
    print ("ODT format conversion durn")

    # Out put to Microsoft doc format (*.docx)

def convert_to_doc(root, output_file):
    doc = docx.Document()

    p = doc.add_paragraph()
    run = p.add_run (extract_text(root.find("./title")) + "\n\n")
    run.bold = True
    run.font.name = 'Arial'
    run.font.size = docx.shared.Pt(24)

    for page in root.findall("./script/page"):
        page_num = page.get("num")
        run = p.add_run("Page {}\n\n".format(page_num))
        run.bold = True
        run.font.size = docx.shared.Pt (16)

        for panel in page.findall("./panel"):
            panel_num = panel.get("num")
            run = p.add_run("Panel {}\n\n".format(panel_num))
            run.underline = True

            for element in panel:
                tag_name = element.tag
                text = extract_text(element)

                if tag_name == "character":
                    name = element.get("name")
                    run = p.add_run("{}:".format(name.upper()))
                    run.bold = True

                    run = p.add_run("{}\n\n".format(text))
                elif tag_name == "narrator": # Honestly I'll probably drop the Narrator tag
                    run = p.add_run("    {}\n".format(text))
                elif tag_name == "action":
                    run = p.add_run("{}\n\n".format(text))
                    run.italic = True
        p = doc.add_paragraph()
    doc.save (output_file)
    print ("DoC format conversion durn")

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
def convert_to_dc(root, output_file):
   # Modify this function to generate HTML output
    with open(output_file, "w") as f:
        f.write ("DC format")
        f.write (extract_text(root.find("./title")) + "\n")

        for page in root.findall("./script/page"):
            page_num = page.get("num")
            f.write("Page {}\n".format(page_num))

            for panel in page.findall("./panel"):
                panel_num = panel.get("num")
                f.write("_Panel_{}_\n\n".format(panel_num))

                for element in panel:
                    tag_name = element.tag
                    text = extract_text(element)
                    
                    if tag_name == "character":
                        name = element.get("name")
                        f.write("{}: {}\n\n".format(name.upper(), text))
                    elif tag_name == "narrator": # Honestly I'll probably drop the Narrator tag
                        f.write("    {}\n".format(text))
                    elif tag_name == "action":
                        f.write("{}\n\n".format(text))
            f.write("\n")
    print ("DC format conversion durn")
def help():
    print("Usage: python script_name.py [options]")
    print("Options:")
    print("  -i, --input     Input XML file")
    print("  -o, --output    Output file")
    print("  -f, --format    Output format (html, fountain, text, ODT, Docx)")
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
        chunk_size = 100

        for i in range(0, len(parsed_xml), chunk_size):
            chunk = parsed_xml[i:i + chunk_size]
            stdscr.addstr(chunk)
            stdscr.refresh()
            stdscr.getch()
            stdscr.clear()

    finally:
        curses.endwin()



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
        print("Usage: python script_name.py -i input_file.xml -o output_file -f format (HTML, Fountain, txt, ODT, Docx)")
        return

    tree = ET.parse(input_file)
    root = tree.getroot()

    if output_format == "pdf":
        convert_to_pdf(root, output_file)
    elif output_format == "doc":
        convert_to_doc(root, output_file)
    elif output_format == "odt":
        convert_to_odt(root, output_file)
    elif output_format == "txt":# Formally dc needs to be a style not format (Styles hopefully to come in version 2)
        convert_to_dc(root, output_file)
    elif output_format == "fountain":
        convert_to_fountain(root, output_file)
    elif output_format == "html":
        convert_to_html(root, output_file)
    else:
        print("Invalid output format. Please choose 'html' or 'fountain'.")

if __name__ == "__main__":
    main()