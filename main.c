#include <stdio.h>
#include <string.h>
#define BUF_SIZE 256
#define SETS 3

int main() {
    printf("Hola gente de yutub \n");
    FILE *fptr;
    fptr = fopen("./data.txt", "r");
    if (fptr == NULL) {
        printf("Error al abri el archivo \n");
        return 1;
    }
    char buf[BUF_SIZE];

    // line by line
    while (fgets(buf, BUF_SIZE, fptr) != NULL) {
        if (buf[0] == '#') {
            continue;
        }

        buf[strcspn(buf, "\n")] = '\0';
        printf("%lu \n", strlen(buf));
    }

    fclose(fptr);
    return 0;
}
