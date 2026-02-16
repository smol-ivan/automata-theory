#include <stdio.h>
#include <string.h>
#define MAX_SYMBOLS 128
#define MAX_STRINGS 2048
#define MAX_LEN 32
#define MAX_STR_LEN 8
#define BUF_SIZE 256
#define MAX_KLEENE 3

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

Lenguaje seleccion_alternativas(Lenguaje A, Lenguaje B) {
    Lenguaje R;
    R.size = 0;

    for (int i = 0; i < A.size; i++)
        strcpy(R.cadenas[R.size++], A.cadenas[i]);

    for (int i = 0; i < B.size; i++)
        strcpy(R.cadenas[R.size++], B.cadenas[i]);

    return R;
}

Lenguaje construir_lenguaje_desde_alfabeto(Alfabeto A) {
    Lenguaje result = lenguaje_elemental(A.simbolos[0]);

    for (int i = 1; i < A.size; i++) {
        Lenguaje elem = lenguaje_elemental(A.simbolos[i]);
        result = seleccion_alternativas(result, elem);
    }

    return result;
}

int leer_alfabetos(const char *filename, Alfabeto alphabets[]) {
    FILE *f = fopen(filename, "r");
    char line[BUF_SIZE];
    int count = 0;

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

Lenguaje concatenacion(Lenguaje A, Lenguaje B) {
    Lenguaje R;
    R.size = 0;

    for (int i = 0; i < A.size; i++)
        for (int j = 0; j < B.size; j++) {
            // Limite de largo de cadenas
            if (strlen(A.cadenas[i]) + strlen(B.cadenas[j]) > MAX_STR_LEN)
                continue;
            snprintf(R.cadenas[R.size++], MAX_LEN, "%s%s", A.cadenas[i],
                     B.cadenas[j]);
        }
    return R;
}

Lenguaje kleene(Lenguaje L) {
    Lenguaje R;
    R.size = 1;
    strcpy(R.cadenas[0], ""); // ε

    Lenguaje current = L;

    for (int i = 1; i <= MAX_KLEENE; i++) {
        for (int j = 0; j < current.size; j++)
            strcpy(R.cadenas[R.size++], current.cadenas[j]);

        current = concatenacion(current, L);
    }

    return R;
}

int main() {
    Alfabeto alfabetos[3];
    int n = leer_alfabetos("data.txt", alfabetos);

    // Lenguajes construidos POR seleccion entre alternativas
    Lenguaje L_alpha = construir_lenguaje_desde_alfabeto(alfabetos[0]);
    Lenguaje L_digits = construir_lenguaje_desde_alfabeto(alfabetos[1]);
    Lenguaje L_guion = construir_lenguaje_desde_alfabeto(alfabetos[2]);

    // (letra | _)
    Lenguaje first = seleccion_alternativas(L_alpha, L_guion);

    // (letra | digito | _)
    Lenguaje rest = seleccion_alternativas(first, L_digits);

    // (letra | digito | _)*
    Lenguaje rest_kleene = kleene(rest);

    // identificadores
    Lenguaje identificadores = concatenacion(first, rest_kleene);

    // Buscar cadenas pedidas
    for (int i = 0; i < identificadores.size; i++) {
        if (!strcmp(identificadores.cadenas[i], "amigo_1") ||
            !strcmp(identificadores.cadenas[i], "a1b1c2d1") ||
            !strcmp(identificadores.cadenas[i], "a1z1b2y2")) {
            printf("Encontrado %s en posicion %d\n", identificadores.cadenas[i],
                   i);
        }
    }

    return 0;
}
