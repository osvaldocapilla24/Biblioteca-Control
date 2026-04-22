import time
from BibliotecaDigital import BibliotecaDigital   # cambia por el nombre de tu archivo

sis = BibliotecaDigital()

inicio = time.perf_counter()

for i in range(10000):
    sis.registrar_libro(f"L{i}", f"Libro{i}", "Autor", "Categoria", "2010-01-01")

fin = time.perf_counter()

print("Tiempo total:", fin - inicio)