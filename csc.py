import sys
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
        f.write ("<html><head></title>")
        f.write (extract_text(root.find("./title")) + "\n")
        f.write ("</titel></head><body>")
        
        # Copy the script above to edit later to HTML

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
        f.write ("</body></html>")
    print ("HTML conversion durn")
def main():
    if len(sys.argv) < 4:
        print("Usage: python script_name.py input_file.xml output_file format (html/fountain)")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    output_format = sys.argv[3].lower()

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