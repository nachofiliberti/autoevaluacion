from app.models import models

# Imports que son nativos de Python
from datetime import timedelta

# Imports que son nativos del Framework y Librerias
from app import app, db, jwt
from flask import (
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

# Imports de variables generadas por nosotros
from app.models.models import (
    Localidad,
    Pais,
    Persona,
    Provincia,
    User,
)
from app.schemas.schema import (
    UserAdminSchema,
    UserBasicSchema,
    PaisSchema,
    ProvinciaSchema,
    LocalidadSchema
)
from flask.views import MethodView

persona_schema = Persona()
personas_schema = Persona(many=True)

class PersonaView(MethodView):
    def get(self, persona_id):
        if persona_id:
            persona = Persona.query.get(persona_id)
            if persona:
                return persona_schema.jsonify(persona)
            return jsonify({"message": "Persona no encontrada"}), 404
        personas = Persona.query.all()
        return personas_schema.jsonify(personas)

    def post(self):
        data = request.get_json()
        nueva_persona = Persona(
            nombre=data['nombre'],
            apellido=data['apellido'],
            email=data['email'],
            nacimiento=data['nacimiento'],
            activo=data['activo'],
            telefono=data.get('telefono'),
            localidad=data['localidad']
        )
        db.session.add(nueva_persona)
        db.session.commit()
        return persona_schema.jsonify(nueva_persona), 201
