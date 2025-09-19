from flask import Flask, request, jsonify
import jwt
import datetime

# ===============================
# Configuración
# ===============================
app = Flask(__name__)
SECRET_KEY = "mi_clave_secreta"  # en producción ponla en env

# ===============================
# Clases base
# ===============================
class Egresado:
    def __init__(self, cedula, ficha, nombre, perfil):
        self.cedula = cedula
        self.ficha = ficha
        self.nombre = nombre
        self.perfil = perfil

class Empleo:
    def __init__(self, titulo, descripcion, salario, perfil_requerido):
        self.titulo = titulo
        self.descripcion = descripcion
        self.salario = salario
        self.perfil_requerido = perfil_requerido

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "salario": self.salario,
            "perfil_requerido": self.perfil_requerido
        }

class Pila:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop() if not self.esta_vacia() else None

    def esta_vacia(self):
        return len(self.items) == 0

# ===============================
# Datos simulados
# ===============================
egresados = [
    Egresado("123", "456", "Ana Pérez", "Software"),
    Egresado("124", "457", "Luis Gómez", "Contabilidad"),
]

empleos = [
    Empleo("Desarrollador Python", "Desarrollo de backend", 2500000, "Software"),
    Empleo("Tester QA", "Pruebas de software", 2000000, "Software"),
    Empleo("Auxiliar contable", "Balances financieros", 1800000, "Contabilidad"),
]

# ===============================
# Helpers
# ===============================
def generar_token(egresado):
    payload = {
        "cedula": egresado.cedula,
        "perfil": egresado.perfil,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verificar_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# ===============================
# Rutas
# ===============================
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    cedula = data.get("cedula")
    ficha = data.get("ficha")

    # Validar egresado
    egresado = next((e for e in egresados if e.cedula == cedula and e.ficha == ficha), None)
    if not egresado:
        return jsonify({"msg": "Credenciales inválidas"}), 401

    token = generar_token(egresado)

    return jsonify({
        "token": token,
        "perfil": egresado.perfil,
        "nombre": egresado.nombre
    })

@app.route("/trabajos", methods=["GET"])
def get_trabajos():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"msg": "Token requerido"}), 401

    token = auth_header.split(" ")[1]
    data = verificar_token(token)

    if not data:
        return jsonify({"msg": "Token inválido o expirado"}), 401

    perfil = data["perfil"]

    # Filtrar empleos por perfil y meter en pila
    pila = Pila()
    for empleo in empleos:
        if empleo.perfil_requerido == perfil:
            pila.push(empleo)

    trabajos = []
    while not pila.esta_vacia():
        trabajos.append(pila.pop().to_dict())

    return jsonify(trabajos)

# ===============================
# Run server
# ===============================
if __name__ == "__main__":
    app.run(debug=True)
