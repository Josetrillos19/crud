from flask import Flask
from flask_cors import CORS
from flask import jsonify, request
import pymysql

app = Flask(__name__)
CORS(app)

# Cifrado César - Funciones de encriptar y desencriptar
def cifrado_cesar(texto, desplazamiento):
    resultado = ""
    for caracter in texto:
        if caracter.isalpha():  # Solo se encriptan letras
            # Determinar si es mayúscula o minúscula para aplicar desplazamiento en el alfabeto correspondiente
            ascii_offset = 65 if caracter.isupper() else 97
            resultado += chr((ord(caracter) + desplazamiento - ascii_offset) % 26 + ascii_offset)
        else:
            resultado += caracter  # No se modifica si no es una letra
    return resultado

def encriptar_clave(clave):
    return cifrado_cesar(clave, 3)  # Desplazamiento de +3

def desencriptar_clave(clave_encriptada):
    return cifrado_cesar(clave_encriptada, -3)  # Desplazamiento de -3

# Función de conexión a la base de datos
def conectar(vhost, vuser, vpass, vdb):
    conn = pymysql.connect(host=vhost, user=vuser, passwd=vpass, db=vdb, charset='utf8mb4')
    return conn

# Ruta para consulta general
@app.route("/")
def consulta_general():
    try:
        conn = conectar('localhost', 'root', 'root', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute("SELECT * FROM baul")
        datos = cur.fetchall()
        data = []
        for row in datos:
            dato = {
                'id_baul': row[0],
                'Plataforma': row[1],
                'usuario': row[2],
                'clave': desencriptar_clave(row[3])  # Desencriptar clave
            }
            data.append(dato)
        cur.close()
        conn.close()
        return jsonify({'baul': data, 'mensaje': 'Baul de contraseñas'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})

# Consulta individual
@app.route("/consulta_individual/<codigo>", methods=['GET'])
def consulta_individual(codigo):
    try:
        conn = conectar('localhost', 'root', 'root', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute("SELECT * FROM baul WHERE id_baul = %s", (codigo,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            dato = {
                'id_baul': row[0],
                'Plataforma': row[1],
                'usuario': row[2],
                'clave': desencriptar_clave(row[3])  # Desencriptar clave
            }
            return jsonify({'baul': dato, 'mensaje': 'Registro encontrado'})
        else:
            return jsonify({'mensaje': 'Registro no encontrado'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})

# Registro
@app.route("/registro/", methods=['POST'])
def registro():
    try:
        conn = conectar('localhost', 'root', 'root', 'gestor_contrasena')
        cur = conn.cursor()
        # Encriptar la clave antes de guardarla en la base de datos
        clave_encriptada = encriptar_clave(request.json['clave'])
        cur.execute("INSERT INTO baul (plataforma, usuario, clave) VALUES (%s, %s, %s)", (
            request.json['plataforma'],
            request.json['usuario'],
            clave_encriptada
        ))
        conn.commit()  # Confirmar la inserción de la información
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Registro agregado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

# Ruta para eliminar un registro por código
@app.route("/eliminar/<codigo>", methods=['DELETE'])
def eliminar(codigo):
    try:
        conn = conectar('localhost', 'root', '', 'gestor_contrasena')
        cur = conn.cursor()
        cur.execute("DELETE FROM baul WHERE id_baul = %s", (codigo,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Eliminado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

# Ruta para actualizar un registro por código
@app.route("/actualizar/<codigo>", methods=['PUT'])
def actualizar(codigo):
    try:
        conn = conectar('localhost', 'root', 'root', 'gestor_contrasena')
        cur = conn.cursor()
        # Encriptar la clave antes de actualizarla en la base de datos
        clave_encriptada = encriptar_clave(request.json['clave'])
        cur.execute("UPDATE baul SET plataforma = %s, usuario = %s, clave = %s WHERE id_baul = %s", (
            request.json['plataforma'],
            request.json['usuario'],
            clave_encriptada,
            codigo
        ))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'mensaje': 'Registro Actualizado'})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': 'Error'})

# Iniciar la aplicación Flask
if __name__ == "__main__":
    app.run(debug=True)
