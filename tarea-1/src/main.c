#include <stdio.h>
#include <string.h>

#define MAX_SYMBOLS 128
#define MAX_STRINGS 2048
#define MAX_LEN 64
#define MAX_STR_LEN 8
#define BUF_SIZE 256
#define MAX_KLEENE 7

typedef struct {
    char name[32];
    char simbolos[MAX_SYMBOLS];
    int size;
} Alfabeto;

typedef struct {
    char cadenas[MAX_STRINGS][MAX_LEN];
    int size;
} Lenguaje;

Lenguaje lenguaje_elemental(char symbol) {
    Lenguaje L;
    L.size = 1;
    L.cadenas[0][0] = symbol;
    L.cadenas[0][1] = '\0';
    return L;
}

Lenguaje seleccion_alternativas(const Lenguaje *A, const Lenguaje *B) {
    Lenguaje R;
    R.size = 0;

    for (int i = 0; i < A->size && R.size < MAX_STRINGS; i++)
        strcpy(R.cadenas[R.size++], A->cadenas[i]);

    for (int i = 0; i < B->size && R.size < MAX_STRINGS; i++)
        strcpy(R.cadenas[R.size++], B->cadenas[i]);

    return R;
}

Lenguaje construir_lenguaje_desde_alfabeto(Alfabeto A) {
    Lenguaje result = lenguaje_elemental(A.simbolos[0]);

    for (int i = 1; i < A.size; i++) {
        Lenguaje elem = lenguaje_elemental(A.simbolos[i]);
        result = seleccion_alternativas(&result, &elem);
    }

    return result;
}

int leer_alfabetos(const char *filename, Alfabeto alphabets[]) {
    FILE *f = fopen(filename, "r");
    char line[BUF_SIZE];
    int count = 0;

    if (!f) {
        perror("No se pudo abrir data.txt");
        return 0;
    }

    while (fgets(line, sizeof(line), f)) {
        if (line[0] == '#')
            continue;

        line[strcspn(line, "\n")] = '\0';

        char *name = strtok(line, ":");
        char *symbols = strtok(NULL, ":");

        strcpy(alphabets[count].name, name);
        strcpy(alphabets[count].simbolos, symbols);
        alphabets[count].size = strlen(symbols);
        count++;
    }

    fclose(f);
    return count;
}

void generar_rest_kleene(FILE *out, const Lenguaje *rest, const char *prefijo,
                         int profundidad) {
    // Escribimos la cadena actual
    fprintf(out, "%s\n", prefijo);

    if (profundidad == 0)
        return;

    char buffer[MAX_LEN];

    for (int i = 0; i < rest->size; i++) {
        if (strlen(prefijo) + strlen(rest->cadenas[i]) > MAX_STR_LEN)
            continue;

        strcpy(buffer, prefijo);
        strcat(buffer, rest->cadenas[i]);

        generar_rest_kleene(out, rest, buffer, profundidad - 1);
    }
}

void generar_identificadores(FILE *out, const Lenguaje *first,
                             const Lenguaje *rest) {
    char buffer[MAX_LEN];

    for (int i = 0; i < first->size; i++) {
        strcpy(buffer, first->cadenas[i]);
        generar_rest_kleene(out, rest, buffer, MAX_KLEENE);
    }
}

int main() {
    Alfabeto alfabetos[3];

    int n = leer_alfabetos("data.txt", alfabetos);

    // Lenguajes base
    Lenguaje L_alpha = construir_lenguaje_desde_alfabeto(alfabetos[0]);
    Lenguaje L_digits = construir_lenguaje_desde_alfabeto(alfabetos[1]);
    Lenguaje L_guion = construir_lenguaje_desde_alfabeto(alfabetos[2]);

    // (letra | _)
    Lenguaje first = seleccion_alternativas(&L_alpha, &L_guion);

    // (letra | digito | _)
    Lenguaje rest = seleccion_alternativas(&first, &L_digits);

    FILE *out = fopen("identificadores.txt", "w");

    generar_identificadores(out, &first, &rest);

    fclose(out);

    printf("Identificadores generados en identificadores.txt\n");
    return 0;
}
