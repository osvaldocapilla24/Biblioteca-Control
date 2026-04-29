from BibliotecaDigital import BibliotecaDigital

def test_registrar_usuario_correcto():
    sis = BibliotecaDigital()
    ok, msg = sis.registrar_usuario("20230001", "Juan Perez", "1234", "estudiante")
    assert ok is True
    assert msg == "Usuario registrado correctamente."

def test_registrar_usuario_matricula_repetida():
    sis = BibliotecaDigital()
    sis.registrar_usuario("20230001", "Juan Perez", "1234", "estudiante")
    ok, msg = sis.registrar_usuario("20230001", "Juan Perez", "1234", "estudiante")
    assert ok is False
    assert msg == "Matrícula ya registrada."

def test_login_correcto():
    sis = BibliotecaDigital()
    sis.registrar_usuario("20230002", "Maria Lopez", "1234", "estudiante")
    ok, msg, usuario = sis.login("20230002", "1234")
    assert ok is True
    assert usuario is not None
    assert usuario.nombre == "Maria Lopez"

def test_login_password_incorrecto():
    sis = BibliotecaDigital()
    sis.registrar_usuario("20230003", "Pedro Ruiz", "1234", "estudiante")
    ok, msg, usuario = sis.login("20230003", "9999")
    assert ok is False
    assert msg == "Contraseña incorrecta."
    assert usuario is None

def test_registrar_libro_correcto():
    sis = BibliotecaDigital()
    ok, msg = sis.registrar_libro("L100", "Python Basico", "Carlos Perez", "Programacion", "2020-01-01")
    assert ok is True
    assert msg == "Libro registrado correctamente."

def test_registrar_libro_fecha_futura():
    sis = BibliotecaDigital()
    ok, msg = sis.registrar_libro("L101", "Python Basico", "Carlos Perez", "Programacion", "2099-01-01")
    assert ok is False
    assert msg == "La fecha debe ser YYYY-MM-DD y no puede ser futura."

def test_prestar_libro_correcto():
    sis = BibliotecaDigital()
    sis.registrar_usuario("20230004", "Ana Torres", "1234", "estudiante")
    sis.registrar_libro("L102", "Redes", "Juan Perez", "Tecnologia", "2019-05-10")
    ok, msg = sis.prestar("L102", "20230004")
    assert ok is True
    assert "Préstamo registrado" in msg

def test_devolver_libro_correcto():
    sis = BibliotecaDigital()
    sis.registrar_usuario("20230005", "Luis Gomez", "1234", "estudiante")
    sis.registrar_libro("L103", "Base Datos", "Mario Lopez", "Tecnologia", "2018-03-15")
    sis.prestar("L103", "20230005")
    ok, msg = sis.devolver("L103")
    assert ok is True
    assert "Devolución registrada" in msg