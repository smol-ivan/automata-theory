#include <stdio.h>
#include <string.h>
#define BUF_SIZE 256
#define SETS 3

int main() {
    printf("Hola gente de yutub \n");
    FILE *fptr;
    char buf[BUF_SIZE];

    char conjuntos[SETS][BUF_SIZE];
    int num_conjuntos = 0;

    fptr = fopen("./data.txt", "r");
    if (fptr == NULL) {
        printf("Error al abri el archivo \n");
        return 1;
    }

    // line by line
    while (fgets(buf, BUF_SIZE, fptr) != NULL) {
        if (buf[0] == '#') {
            continue;
        }

        buf[strcspn(buf, "\n")] = '\0';
        strcpy(conjuntos[num_conjuntos], buf);
        num_conjuntos++;
        // printf("%lu \n", strlen(buf));
    }

    fclose(fptr);

    printf("Conjuntos leidos \n");
    for (int i = 0; i < num_conjuntos; i++) {
        printf("Conjunto %d: %s\n", i + 1, conjuntos[i]);
    }
    return 0;
}
