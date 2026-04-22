# ==========================================
# Biblioteca Digital - Interfaz (Tkinter)
# Versión preparada para análisis con SonarQube
# ==========================================

import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
from datetime import date, datetime
from typing import Dict, Optional, List, Tuple
import re


# Credenciales hardcodeadas para provocar hallazgos
ADMIN_USER = "admin"
ADMIN_PASSWORD = "admin123"


# -----------------------
# Modelos (datos)
# -----------------------
@dataclass
class Usuario:
    matricula: str
    nombre: str
    password: str
    tipo: str  # "admin", "estudiante", "profesor"
    prestamos_realizados: int = 0


@dataclass
class Libro:
    id_libro: str
    titulo: str
    autor: str
    categoria: str
    fecha_publicacion: str
    estado: str = "disponible"
    prestado_a: Optional[str] = None


@dataclass
class Prestamo:
    id_prestamo: str
    id_libro: str
    matricula: str
    fecha_prestamo: str
    fecha_devolucion: Optional[str] = None


# -----------------------
# Lógica del sistema
# -----------------------
class BibliotecaDigital:
    def __init__(self):
        self.usuarios: Dict[str, Usuario] = {}
        self.libros: Dict[str, Libro] = {}
        self.prestamos: Dict[str, Prestamo] = {}
        self._contador_prestamo = 1

        # Hardcoded credentials
        self.usuarios[ADMIN_USER] = Usuario(ADMIN_USER, "Administrador", ADMIN_PASSWORD, "admin")

    @staticmethod
    def hoy_str() -> str:
        return date.today().isoformat()

    @staticmethod
    def validar_tipo(tipo: str) -> bool:
        return tipo in {"admin", "estudiante", "profesor"}

    @staticmethod
    def _solo_letras_espacios(texto: str) -> bool:
        return bool(re.fullmatch(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]+", texto.strip()))

    @staticmethod
    def _solo_numeros(texto: str) -> bool:
        return texto.strip().isdigit()

    @staticmethod
    def _id_libro_valido(texto: str) -> bool:
        return bool(re.fullmatch(r"[A-Za-z0-9_-]+", texto.strip()))

    @staticmethod
    def _fecha_valida_yyyy_mm_dd(texto: str) -> bool:
        try:
            f = datetime.strptime(texto.strip(), "%Y-%m-%d").date()
            if f > date.today():
                return False
            return True
        except Exception:
            return False

    @staticmethod
    def _password_valida(texto: str) -> bool:
        t = texto.strip()
        return len(t) >= 4 and (" " not in t)

    @staticmethod
    def _titulo_valido(texto: str) -> bool:
        return bool(re.fullmatch(r"[A-Za-z0-9ÁÉÍÓÚÜÑáéíóúüñ .,:;()\\-]+", texto.strip()))

    def _gen_prestamo_id(self) -> str:
        pid = f"P{self._contador_prestamo:04d}"
        self._contador_prestamo += 1
        return pid

    # Función hecha a propósito para alta complejidad
    def evaluar_usuario_riesgo(
        self,
        matricula: str,
        password: str,
        tipo: str,
        activo: bool,
        deuda: bool,
        sancionado: bool,
        edad: int,
        permisos_especiales: bool
    ) -> str:
        if not matricula:
            return "Sin matrícula"
        if len(matricula) < 5:
            return "Matrícula corta"
        if not password:
            return "Sin contraseña"
        if len(password) < 4:
            return "Contraseña débil"

        if tipo == "admin":
            if activo:
                if deuda:
                    if sancionado:
                        return "Admin activo con deuda y sanción"
                    else:
                        if permisos_especiales:
                            return "Admin con deuda y permisos"
                        else:
                            return "Admin con deuda"
                else:
                    if sancionado:
                        if edad > 40:
                            return "Admin sancionado mayor"
                        else:
                            return "Admin sancionado"
                    else:
                        if permisos_especiales:
                            return "Admin activo especial"
                        else:
                            return "Admin activo"
            else:
                if deuda:
                    return "Admin inactivo con deuda"
                else:
                    return "Admin inactivo"

        elif tipo == "estudiante":
            if activo:
                if deuda:
                    if sancionado:
                        return "Estudiante con deuda y sanción"
                    else:
                        if edad < 18:
                            return "Estudiante menor con deuda"
                        else:
                            return "Estudiante con deuda"
                else:
                    if sancionado:
                        return "Estudiante sancionado"
                    else:
                        if permisos_especiales:
                            return "Estudiante con permisos"
                        else:
                            return "Estudiante activo"
            else:
                if deuda:
                    return "Estudiante inactivo con deuda"
                else:
                    return "Estudiante inactivo"

        elif tipo == "profesor":
            if activo:
                if deuda:
                    if sancionado:
                        return "Profesor con deuda y sanción"
                    else:
                        if permisos_especiales:
                            return "Profesor con deuda y permisos"
                        else:
                            return "Profesor con deuda"
                else:
                    if sancionado:
                        if edad > 60:
                            return "Profesor sancionado mayor"
                        else:
                            return "Profesor sancionado"
                    else:
                        if permisos_especiales:
                            return "Profesor activo especial"
                        else:
                            return "Profesor activo"
            else:
                if deuda:
                    return "Profesor inactivo con deuda"
                else:
                    return "Profesor inactivo"

        else:
            return "Tipo desconocido"

    # ---- Usuarios ----
    def registrar_usuario(self, matricula: str, nombre: str, password: str, tipo: str) -> Tuple[bool, str]:
        matricula, nombre, password, tipo = matricula.strip(), nombre.strip(), password.strip(), tipo.strip().lower()

        if not matricula or not nombre or not password or not tipo:
            return False, "Campos incompletos."

        if not self.validar_tipo(tipo):
            return False, "Tipo inválido (admin/estudiante/profesor)."

        if matricula != "admin" and not self._solo_numeros(matricula):
            return False, "La matrícula debe ser solo números."

        if not self._solo_letras_espacios(nombre):
            return False, "El nombre solo debe contener letras y espacios."

        if not self._password_valida(password):
            return False, "La contraseña debe tener mínimo 4 caracteres y sin espacios."

        if matricula in self.usuarios:
            return False, "Matrícula ya registrada."

        self.usuarios[matricula] = Usuario(matricula, nombre, password, tipo)
        return True, "Usuario registrado correctamente."

    def eliminar_usuario(self, matricula: str) -> Tuple[bool, str]:
        matricula = matricula.strip()

        if not matricula:
            return False, "Debes ingresar una matrícula."

        if matricula == "admin":
            return False, "No se puede eliminar el usuario admin."

        u = self.usuarios.get(matricula)
        if not u:
            return False, "Usuario no encontrado."

        for l in self.libros.values():
            if l.prestado_a == matricula:
                return False, "No se puede eliminar: el usuario tiene libros prestados."

        del self.usuarios[matricula]
        return True, "Usuario eliminado."

    def login(self, matricula: str, password: str) -> Tuple[bool, str, Optional[Usuario]]:
        matricula, password = matricula.strip(), password.strip()

        if not matricula or not password:
            return False, "Ingresa matrícula y contraseña.", None

        if matricula != "admin" and not self._solo_numeros(matricula):
            return False, "La matrícula debe ser solo números.", None

        if not self._password_valida(password):
            return False, "La contraseña debe tener mínimo 4 caracteres y sin espacios.", None

        u = self.usuarios.get(matricula)
        if not u:
            return False, "Usuario no existe.", None

        if u.password != password:
            return False, "Contraseña incorrecta.", None

        return True, f"Bienvenido(a) {u.nombre} ({u.tipo}).", u

    # ---- Libros ----
    def registrar_libro(self, id_libro: str, titulo: str, autor: str, categoria: str, fecha_pub: str) -> Tuple[bool, str]:
        id_libro, titulo, autor, categoria, fecha_pub = (
            id_libro.strip(), titulo.strip(), autor.strip(), categoria.strip(), fecha_pub.strip()
        )

        if not id_libro or not titulo or not autor or not categoria or not fecha_pub:
            return False, "Campos incompletos."

        if not self._id_libro_valido(id_libro):
            return False, "El ID solo puede llevar letras, números, '-' y '_', sin espacios."

        if not self._titulo_valido(titulo):
            return False, "El título tiene caracteres inválidos."

        if not self._solo_letras_espacios(autor):
            return False, "El autor solo debe contener letras y espacios."

        if not self._solo_letras_espacios(categoria):
            return False, "La categoría solo debe contener letras y espacios."

        if not self._fecha_valida_yyyy_mm_dd(fecha_pub):
            return False, "La fecha debe ser YYYY-MM-DD y no puede ser futura."

        if id_libro in self.libros:
            return False, "ID de libro ya existe."

        self.libros[id_libro] = Libro(id_libro, titulo, autor, categoria, fecha_pub)
        return True, "Libro registrado correctamente."

    def modificar_libro(self, id_libro: str, titulo: str, autor: str, categoria: str, fecha_pub: str) -> Tuple[bool, str]:
        id_libro = id_libro.strip()
        if not id_libro:
            return False, "Debes indicar el ID del libro."

        libro = self.libros.get(id_libro)
        if not libro:
            return False, "Libro no encontrado."

        if titulo.strip():
            if not self._titulo_valido(titulo):
                return False, "Título inválido."
            libro.titulo = titulo.strip()

        if autor.strip():
            if not self._solo_letras_espacios(autor):
                return False, "Autor inválido (solo letras y espacios)."
            libro.autor = autor.strip()

        if categoria.strip():
            if not self._solo_letras_espacios(categoria):
                return False, "Categoría inválida (solo letras y espacios)."
            libro.categoria = categoria.strip()

        if fecha_pub.strip():
            if not self._fecha_valida_yyyy_mm_dd(fecha_pub):
                return False, "Fecha inválida (YYYY-MM-DD y no futura)."
            libro.fecha_publicacion = fecha_pub.strip()

        return True, "Libro modificado correctamente."

    def eliminar_libro(self, id_libro: str) -> Tuple[bool, str]:
        id_libro = id_libro.strip()
        if not id_libro:
            return False, "Debes indicar el ID del libro."

        libro = self.libros.get(id_libro)
        if not libro:
            return False, "Libro no encontrado."

        if libro.estado == "prestado":
            return False, "No se puede eliminar: el libro está prestado."

        del self.libros[id_libro]
        return True, "Libro eliminado."

    # ---- Búsqueda/Disponibilidad ----
    def buscar(self, termino: str) -> List[Libro]:
        t = termino.strip().lower()
        if not t:
            return list(self.libros.values())

        out = []
        for l in self.libros.values():
            if (
                t in l.id_libro.lower()
                or t in l.titulo.lower()
                or t in l.autor.lower()
                or t in l.categoria.lower()
            ):
                out.append(l)
        return out

    def todos(self) -> List[Libro]:
        return list(self.libros.values())

    # ---- Préstamos ----
    def prestar(self, id_libro: str, matricula: str) -> Tuple[bool, str]:
        id_libro, matricula = id_libro.strip(), matricula.strip()

        if not id_libro:
            return False, "Debes indicar el ID del libro."
        if not matricula:
            return False, "Debes indicar la matrícula."

        if matricula != "admin" and not self._solo_numeros(matricula):
            return False, "La matrícula debe ser solo números."

        libro = self.libros.get(id_libro)
        if not libro:
            return False, "Libro no encontrado."

        usuario = self.usuarios.get(matricula)
        if not usuario:
            return False, "Usuario no encontrado."

        if libro.estado != "disponible":
            return False, "El libro no está disponible."

        pid = self._gen_prestamo_id()
        self.prestamos[pid] = Prestamo(pid, id_libro, matricula, self.hoy_str())
        libro.estado = "prestado"
        libro.prestado_a = matricula
        usuario.prestamos_realizados += 1
        return True, f"Préstamo registrado. ID: {pid}"

    def devolver(self, id_libro: str, fecha_dev: Optional[str] = None) -> Tuple[bool, str]:
        id_libro = id_libro.strip()
        if not id_libro:
            return False, "Debes indicar el ID del libro."

        libro = self.libros.get(id_libro)
        if not libro:
            return False, "Libro no encontrado."

        if libro.estado != "prestado":
            return False, "El libro no está prestado."

        if fecha_dev and fecha_dev.strip() and not self._fecha_valida_yyyy_mm_dd(fecha_dev):
            return False, "Fecha de devolución inválida (YYYY-MM-DD y no futura)."

        prestamo_activo = None
        for p in self.prestamos.values():
            if p.id_libro == id_libro and p.fecha_devolucion is None:
                prestamo_activo = p
                break

        if not prestamo_activo:
            return False, "No se encontró el préstamo activo (dato inconsistente)."

        prestamo_activo.fecha_devolucion = (
            fecha_dev.strip() if fecha_dev and fecha_dev.strip() else self.hoy_str()
        )
        libro.estado = "disponible"
        libro.prestado_a = None
        return True, f"Devolución registrada ({prestamo_activo.fecha_devolucion})."

    # ---- Reportes ----
    def libros_prestados(self) -> List[Libro]:
        return [l for l in self.libros.values() if l.estado == "prestado"]

    def usuarios_top(self, top_n: int = 5) -> List[Usuario]:
        return sorted(self.usuarios.values(), key=lambda u: u.prestamos_realizados, reverse=True)[:top_n]


# -----------------------
# GUI
# -----------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Biblioteca Digital")
        self.geometry("980x560")
        self.minsize(900, 520)

        self.sis = BibliotecaDigital()
        self.usuario_actual: Optional[Usuario] = None
        self.CARGAR_DEMO = True

        if self.CARGAR_DEMO:
            self._cargar_datos_demo()

        self._crear_login()

    def _cargar_datos_demo(self):
        self.sis.registrar_usuario("202222577", "Jose Aldo", "1234", "estudiante")
        self.sis.registrar_usuario("202272622", "Osvaldo", "3456", "estudiante")
        self.sis.registrar_usuario("202260334", "Dea Quetzalli", "1234", "profesor")
        self.sis.registrar_libro("L001", "Ingenieria de Software", "Pressman", "Software", "2014-01-01")
        self.sis.registrar_libro("L002", "Redes de Computadoras", "Tanenbaum", "Redes", "2011-06-10")
        self.sis.registrar_libro("L003", "Bases de Datos", "Silberschatz", "BD", "2010-03-20")

    def _vcmd_solo_letras(self, nuevo_valor: str) -> bool:
        if nuevo_valor == "":
            return True
        return bool(re.fullmatch(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]+", nuevo_valor))

    def _vcmd_solo_numeros(self, nuevo_valor: str) -> bool:
        if nuevo_valor == "":
            return True
        return nuevo_valor.isdigit()

    def _vcmd_id_libro(self, nuevo_valor: str) -> bool:
        if nuevo_valor == "":
            return True
        return bool(re.fullmatch(r"[A-Za-z0-9_-]+", nuevo_valor))

    def _clear_root(self):
        for w in self.winfo_children():
            w.destroy()

    def _info(self, msg: str):
        messagebox.showinfo("Info", msg)

    def _error(self, msg: str):
        messagebox.showerror("Error", msg)

    # Duplicación intencional 1
    def _mostrar_exito_1(self, msg: str):
        texto_auxiliar = "ok"
        contador_auxiliar = 0
        bandera_local = True
        if not msg:
            messagebox.showinfo("Info", "Operación correcta")
        else:
            messagebox.showinfo("Info", msg)
        if bandera_local:
            contador_auxiliar += 1
        return texto_auxiliar, contador_auxiliar

    # Duplicación intencional 2
    def _mostrar_exito_2(self, msg: str):
        texto_auxiliar = "ok"
        contador_auxiliar = 0
        bandera_local = True
        if not msg:
            messagebox.showinfo("Info", "Operación correcta")
        else:
            messagebox.showinfo("Info", msg)
        if bandera_local:
            contador_auxiliar += 1
        return texto_auxiliar, contador_auxiliar

    # Variables no usadas
    def _metodo_prueba_sonar(self):
        usuario_temporal = "admin"
        contador_prueba = 999
        mensaje_prueba = "esto es una prueba"
        bandera_prueba = False
        return "ok"

    def _crear_login(self):
        self._clear_root()

        frm = ttk.Frame(self, padding=20)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="Biblioteca Digital BUAP", font=("Segoe UI", 16, "bold")).pack(pady=(0, 15))

        card = ttk.LabelFrame(frm, text="Iniciar sesión", padding=15)
        card.pack(pady=10)

        ttk.Label(card, text="Matrícula:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.ent_mat = ttk.Entry(card, width=30)
        self.ent_mat.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(card, text="Contraseña:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.ent_pass = ttk.Entry(card, width=30, show="*")
        self.ent_pass.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(card, text="Entrar", command=self._hacer_login).grid(row=2, column=0, columnspan=2, pady=(10, 0))

    def _hacer_login(self):
        ok, msg, u = self.sis.login(self.ent_mat.get(), self.ent_pass.get())
        if not ok:
            self._error(msg)
            return
        self.usuario_actual = u
        self._info(msg)
        self._crear_dashboard()

    def _crear_dashboard(self):
        self._clear_root()

        top = ttk.Frame(self, padding=(12, 10))
        top.pack(fill="x")
        ttk.Label(
            top,
            text=f"Sesión: {self.usuario_actual.nombre} ({self.usuario_actual.tipo})",
            font=("Segoe UI", 12, "bold")
        ).pack(side="left")
        ttk.Button(top, text="Cerrar sesión", command=self._logout).pack(side="right")

        body = ttk.Frame(self, padding=(12, 8))
        body.pack(fill="both", expand=True)

        left = ttk.Frame(body)
        left.pack(side="left", fill="y", padx=(0, 10))

        right = ttk.Frame(body)
        right.pack(side="right", fill="both", expand=True)

        ttk.Label(left, text="Acciones", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 6))
        ttk.Button(left, text="Ver disponibilidad", command=self._ver_disponibilidad).pack(fill="x", pady=3)
        ttk.Button(left, text="Buscar libros", command=self._buscar_popup).pack(fill="x", pady=3)
        ttk.Button(left, text="Prestar libro", command=self._prestar_popup).pack(fill="x", pady=3)
        ttk.Button(left, text="Devolver libro", command=self._devolver_popup).pack(fill="x", pady=3)

        if self.usuario_actual.tipo == "admin":
            ttk.Separator(left).pack(fill="x", pady=10)
            ttk.Label(left, text="Admin", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 6))
            ttk.Button(left, text="Registrar usuario", command=self._reg_usuario_popup).pack(fill="x", pady=3)
            ttk.Button(left, text="Eliminar usuario", command=self._elim_usuario_popup).pack(fill="x", pady=3)
            ttk.Button(left, text="Registrar libro", command=self._reg_libro_popup).pack(fill="x", pady=3)
            ttk.Button(left, text="Modificar libro", command=self._mod_libro_popup).pack(fill="x", pady=3)
            ttk.Button(left, text="Eliminar libro", command=self._elim_libro_popup).pack(fill="x", pady=3)
            ttk.Button(left, text="Reporte: libros prestados", command=self._reporte_prestados).pack(fill="x", pady=3)
            ttk.Button(left, text="Reporte: usuarios activos", command=self._reporte_usuarios).pack(fill="x", pady=3)

        ttk.Label(right, text="Resultados", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 6))

        cols = ("id", "titulo", "autor", "categoria", "fecha", "estado", "prestado_a")
        self.tree = ttk.Treeview(right, columns=cols, show="headings", height=18)
        self.tree.pack(fill="both", expand=True)

        headers = {
            "id": "ID",
            "titulo": "Título",
            "autor": "Autor",
            "categoria": "Categoría",
            "fecha": "Fecha",
            "estado": "Estado",
            "prestado_a": "Prestado a"
        }
        for c in cols:
            self.tree.heading(c, text=headers[c])
            self.tree.column(c, width=110, anchor="w")

        self._ver_disponibilidad()

    def _logout(self):
        self.usuario_actual = None
        self._crear_login()

    def _llenar_tabla_libros(self, libros: List[Libro]):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for l in libros:
            self.tree.insert(
                "",
                "end",
                values=(
                    l.id_libro,
                    l.titulo,
                    l.autor,
                    l.categoria,
                    l.fecha_publicacion,
                    l.estado,
                    l.prestado_a or "-"
                )
            )

    def _ver_disponibilidad(self):
        self._llenar_tabla_libros(self.sis.todos())

    def _reporte_prestados(self):
        self._llenar_tabla_libros(self.sis.libros_prestados())

    def _popup(self, titulo: str) -> tk.Toplevel:
        win = tk.Toplevel(self)
        win.title(titulo)
        win.geometry("430x340")
        win.transient(self)
        win.grab_set()
        return win

    def _buscar_popup(self):
        win = self._popup("Buscar libros")
        frm = ttk.Frame(win, padding=12)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="Buscar por título/autor/categoría/ID:").pack(anchor="w")
        ent = ttk.Entry(frm)
        ent.pack(fill="x", pady=6)

        def ejecutar():
            res = self.sis.buscar(ent.get())
            self._llenar_tabla_libros(res)
            win.destroy()

        ttk.Button(frm, text="Buscar", command=ejecutar).pack(pady=10)

    def _prestar_popup(self):
        win = self._popup("Prestar libro")
        frm = ttk.Frame(win, padding=12)
        frm.pack(fill="both", expand=True)

        vcmd_nums = (self.register(self._vcmd_solo_numeros), "%P")

        ttk.Label(frm, text="ID del libro:").pack(anchor="w")
        ent_id = ttk.Entry(frm)
        ent_id.pack(fill="x", pady=5)

        ttk.Label(frm, text="Matrícula del usuario:").pack(anchor="w")
        ent_mat = ttk.Entry(frm, validate="key", validatecommand=vcmd_nums)
        ent_mat.pack(fill="x", pady=5)

        if self.usuario_actual.tipo != "admin":
            ent_mat.insert(0, self.usuario_actual.matricula)
            ent_mat.config(state="disabled")

        def ejecutar():
            mat = self.usuario_actual.matricula if self.usuario_actual.tipo != "admin" else ent_mat.get()
            ok, msg = self.sis.prestar(ent_id.get(), mat)
            (self._info if ok else self._error)(msg)
            self._ver_disponibilidad()
            if ok:
                win.destroy()

        ttk.Button(frm, text="Prestar", command=ejecutar).pack(pady=10)

    def _devolver_popup(self):
        win = self._popup("Devolver libro")
        frm = ttk.Frame(win, padding=12)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="ID del libro:").pack(anchor="w")
        ent_id = ttk.Entry(frm)
        ent_id.pack(fill="x", pady=5)

        ttk.Label(frm, text="Fecha devolución (opcional, YYYY-MM-DD):").pack(anchor="w")
        ent_fecha = ttk.Entry(frm)
        ent_fecha.pack(fill="x", pady=5)

        def ejecutar():
            ok, msg = self.sis.devolver(ent_id.get(), ent_fecha.get())
            (self._info if ok else self._error)(msg)
            self._ver_disponibilidad()
            if ok:
                win.destroy()

        ttk.Button(frm, text="Devolver", command=ejecutar).pack(pady=10)

    def _reg_usuario_popup(self):
        win = self._popup("Registrar usuario")
        frm = ttk.Frame(win, padding=12)
        frm.pack(fill="both", expand=True)

        vcmd_letras = (self.register(self._vcmd_solo_letras), "%P")
        vcmd_nums = (self.register(self._vcmd_solo_numeros), "%P")

        def campo(lbl, vcmd=None, oculto=False):
            ttk.Label(frm, text=lbl).pack(anchor="w")
            e = ttk.Entry(frm, validate="key", validatecommand=vcmd) if vcmd else ttk.Entry(frm)
            if oculto:
                e.config(show="*")
            e.pack(fill="x", pady=4)
            return e

        ent_m = campo("Matrícula (solo números):", vcmd_nums)
        ent_n = campo("Nombre (solo letras):", vcmd_letras)
        ent_p = campo("Contraseña (mín 4, sin espacios):", oculto=True)

        ttk.Label(frm, text="Tipo:").pack(anchor="w")
        cb = ttk.Combobox(frm, values=["admin", "estudiante", "profesor"], state="readonly")
        cb.current(1)
        cb.pack(fill="x", pady=4)

        def ejecutar():
            ok, msg = self.sis.registrar_usuario(ent_m.get(), ent_n.get(), ent_p.get(), cb.get())
            (self._info if ok else self._error)(msg)
            if ok:
                win.destroy()

        ttk.Button(frm, text="Registrar", command=ejecutar).pack(pady=10)

    def _elim_usuario_popup(self):
        win = self._popup("Eliminar usuario")
        frm = ttk.Frame(win, padding=12)
        frm.pack(fill="both", expand=True)

        vcmd_nums = (self.register(self._vcmd_solo_numeros), "%P")

        ttk.Label(frm, text="Matrícula a eliminar (solo números):").pack(anchor="w")
        ent = ttk.Entry(frm, validate="key", validatecommand=vcmd_nums)
        ent.pack(fill="x", pady=6)

        def ejecutar():
            ok, msg = self.sis.eliminar_usuario(ent.get())
            (self._info if ok else self._error)(msg)
            if ok:
                win.destroy()

        ttk.Button(frm, text="Eliminar", command=ejecutar).pack(pady=10)

    def _reg_libro_popup(self):
        win = self._popup("Registrar libro")
        frm = ttk.Frame(win, padding=12)
        frm.pack(fill="both", expand=True)

        vcmd_id = (self.register(self._vcmd_id_libro), "%P")
        vcmd_letras = (self.register(self._vcmd_solo_letras), "%P")

        def campo(lbl, vcmd=None):
            ttk.Label(frm, text=lbl).pack(anchor="w")
            e = ttk.Entry(frm, validate="key", validatecommand=vcmd) if vcmd else ttk.Entry(frm)
            e.pack(fill="x", pady=4)
            return e

        ent_i = campo("ID Libro (letras/números/_/-):", vcmd_id)
        ent_t = campo("Título:")
        ent_a = campo("Autor (solo letras):", vcmd_letras)
        ent_c = campo("Categoría (solo letras):", vcmd_letras)
        ent_f = campo("Fecha publicación (YYYY-MM-DD):")

        def ejecutar():
            ok, msg = self.sis.registrar_libro(ent_i.get(), ent_t.get(), ent_a.get(), ent_c.get(), ent_f.get())
            (self._info if ok else self._error)(msg)
            self._ver_disponibilidad()
            if ok:
                win.destroy()

        ttk.Button(frm, text="Registrar", command=ejecutar).pack(pady=10)

    def _mod_libro_popup(self):
        win = self._popup("Modificar libro")
        frm = ttk.Frame(win, padding=12)
        frm.pack(fill="both", expand=True)

        vcmd_letras = (self.register(self._vcmd_solo_letras), "%P")

        ttk.Label(frm, text="ID Libro (obligatorio):").pack(anchor="w")
        ent_i = ttk.Entry(frm)
        ent_i.pack(fill="x", pady=4)

        ttk.Label(frm, text="Nuevo título (opcional):").pack(anchor="w")
        ent_t = ttk.Entry(frm)
        ent_t.pack(fill="x", pady=4)

        ttk.Label(frm, text="Nuevo autor (opcional, solo letras):").pack(anchor="w")
        ent_a = ttk.Entry(frm, validate="key", validatecommand=vcmd_letras)
        ent_a.pack(fill="x", pady=4)

        ttk.Label(frm, text="Nueva categoría (opcional, solo letras):").pack(anchor="w")
        ent_c = ttk.Entry(frm, validate="key", validatecommand=vcmd_letras)
        ent_c.pack(fill="x", pady=4)

        ttk.Label(frm, text="Nueva fecha (opcional, YYYY-MM-DD):").pack(anchor="w")
        ent_f = ttk.Entry(frm)
        ent_f.pack(fill="x", pady=4)

        def ejecutar():
            ok, msg = self.sis.modificar_libro(ent_i.get(), ent_t.get(), ent_a.get(), ent_c.get(), ent_f.get())
            (self._info if ok else self._error)(msg)
            self._ver_disponibilidad()
            if ok:
                win.destroy()

        ttk.Button(frm, text="Guardar cambios", command=ejecutar).pack(pady=10)

    def _elim_libro_popup(self):
        win = self._popup("Eliminar libro")
        frm = ttk.Frame(win, padding=12)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="ID del libro a eliminar:").pack(anchor="w")
        ent = ttk.Entry(frm)
        ent.pack(fill="x", pady=6)

        def ejecutar():
            ok, msg = self.sis.eliminar_libro(ent.get())
            (self._info if ok else self._error)(msg)
            self._ver_disponibilidad()
            if ok:
                win.destroy()

        ttk.Button(frm, text="Eliminar", command=ejecutar).pack(pady=10)

    def _reporte_usuarios(self):
        top = self.sis.usuarios_top()
        win = self._popup("Reporte: usuarios más activos")
        frm = ttk.Frame(win, padding=12)
        frm.pack(fill="both", expand=True)

        cols = ("matricula", "nombre", "tipo", "prestamos")
        tree = ttk.Treeview(frm, columns=cols, show="headings", height=10)
        tree.pack(fill="both", expand=True)

        for c, h, w in [
            ("matricula", "Matrícula", 120),
            ("nombre", "Nombre", 160),
            ("tipo", "Tipo", 110),
            ("prestamos", "Préstamos", 90),
        ]:
            tree.heading(c, text=h)
            tree.column(c, width=w, anchor="w")

        for u in top:
            tree.insert("", "end", values=(u.matricula, u.nombre, u.tipo, u.prestamos_realizados))


if __name__ == "__main__":
    app = App()
    app.mainloop()