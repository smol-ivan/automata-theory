# Instrucciones de Ejecucion Prob5-2

El extractor de URLs acepta texto por archivo, por argumento o por consola.

## Casos de prueba incluidos

- `texto.txt`
- `texto_case2.txt`

## Comandos

```sh
# Caso 1: usando archivo de ejemplo
python3 main.py --text-file texto.txt

# Caso 2: usando segundo archivo de ejemplo
python3 main.py --text-file texto_case2.txt

# Caso 3: texto directo en la linea de comandos
python3 main.py --text "Revisa https://openai.com y docs.python.org para mas informacion"
```

Si no se usa `--text-file` ni `--text`, el programa solicita el texto por consola.
