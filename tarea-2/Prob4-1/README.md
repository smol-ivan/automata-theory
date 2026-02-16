# Instrucciones de Ejecucion Prob4-1

El simulador ahora acepta el archivo del AFD por argumento, por lo que puedes usar multiples casos de prueba.

## Casos de prueba incluidos

- `formato_entrada.json`
- `formato_entrada_case2.json`

## Comandos

```sh
# Caso 1
python3 main.py --afd-file formato_entrada.json --cadena 1010

# Caso 2
python3 main.py --afd-file formato_entrada_case2.json --cadena 1100
```

Si no envias `--cadena`, el programa la solicita por consola.
