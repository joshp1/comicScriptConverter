#include <stdio.h>
#include <string.h>

int main() {
    FILE *xmlFile = fopen("mycomicmarkuplanguage.xml", "r");
    if (xmlFile == NULL) {
        printf("Error opening the XML file.\n");
        return 1;
    }

char line[500];
int panelNum=0;

    printf ("Title:Comic Ttiel\n");
    printf ("Draft: rough\n");
    while (fgets (line, sizeof (line),xmlFile)){
               if (strstr(line, "<panel")) {
            panelNum++;
            printf("\n===\n\n");
            printf("INT. COMIC PAGE %d - PANEL %d\n", (panelNum - 1) / 2 + 1, panelNum % 2 + 1);
        } else if (strstr(line, "<character")) {
            char *nameStart = strstr(line, "name=\"") + 6;
            char *nameEnd = strstr(nameStart, "\">");
            *nameEnd = '\0';

            char *moodStart = strstr(nameEnd + 1, "mood=\"") + 6;
            char *moodEnd = strstr(moodStart, "\"");
            *moodEnd = '\0';

            printf("CHARACTER: %s\n", nameStart);
            printf("MOOD: %s\n", moodStart);

            char *dialogStart = strstr(moodEnd + 1, ">");
            printf("%s\n", dialogStart + 1);
        } else if (strstr(line, "<narrator")) {
            printf("NARRATOR\n");
            char *narratorStart = strstr(line, ">") + 1;
            printf("%s\n", narratorStart);
        } else if (strstr(line, "<action")) {
            printf("ACTION\n");
            char *actionStart = strstr(line, ">") + 1;
            printf("%s\n", actionStart);
        }
    }
    fclose(xmlFile);
    return 0;
}