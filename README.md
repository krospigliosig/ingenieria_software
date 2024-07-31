# Sistema de elecciones online 
## Error/Exception Handling (constructive)
Este estilo se aplica en todos los métodos del repositorio para manejar posibles errores durante las operaciones con la base de datos. Si ocurre una excepción, la operación se revierte para mantener la integridad de los datos. 
## Cookbook
Con la integración de este estilo, se ve la implementación clara y directa de operaciones CRUD en los métodos del repositorio.

Error/Exception Handling y Cookbook se ven en:

*candidato_repositorio_impl.py:*
```python
class candidato_respositorio_impl:
    def agregar_candidato(self, candidato): # Create
        try:
            db.session.add(candidato)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    def eliminar_candidato(self, candidato): # Delete
        try:
            db.session.delete(candidato)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    def obtener_candidato_por_id(self, id): # Read
        try:
            candidato = Candidato.query.get(id)
            return candidato
        except Exception:
            return None

    def actualizar_candidato(self, id, nueva_candidatura, nueva_propuesta): # Update
        try:
            candidato = Candidato.query.get(id)
            if candidato:
                candidato.candidatura = nueva_candidatura
                candidato.propuesta = nueva_propuesta
                db.session.commit()
                return True
            return False
        except Exception:
            db.session.rollback()
            return False
```
*elector_repositorio_impl.py:*
```python
class elector_repositorio_impl:
    def agregar_elector(self, elector):
        try:
            db.session.add(elector)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    def eliminar_elector(self, elector):
        try:
            db.session.delete(elector)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    def obtener_elector_por_id(self, id):
        try:
            elector = Elector.query.get(id)
            return elector
        except Exception:
            return None
    
    def actualizar_elector(self, id, nuevo_correo, nueva_contrasena, nuevo_nombre, nuevo_apellido, nuevo_estado_voto):
        try:
            elector = Elector.query.get(id)
            if elector:
                elector.correo = nuevo_correo
                elector.contrasena = nueva_contrasena
                elector.nombre = nuevo_nombre
                elector.apellido = nuevo_apellido
                elector.estado_voto = nuevo_estado_voto
                db.session.commit()
                return True
            return False
        except Exception:
            db.session.rollback()
            return False
```
## Persistent-Tables
Este estilo se aplica al definir los modelos de base de datos Candidato y Elector utilizando SQLAlchemy, lo que asegura que los datos se almacenan de manera óptima en la base de datos. 
Estas tablas se pueden ver en:

*En models/Candidato.py:*
```python
from Model.extensions import db

class Candidato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidatura = db.Column(db.String(100), unique=True, nullable=False)
    propuesta = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Candidato {self.candidatura}>'
```
*En models/Elector.py:*
```python
from Model.extensions import db

class Elector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    contrasena = db.Column(db.String(120), nullable=False)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    estado_voto = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Elector {self.nombre} {self.apellido}>'
```
# Repositorios del sistema de elecciones online

Fork del [Sistema de elecciones online](https://github.com/Kiw1i/ingenieria_software)

## Descripción

El objetivo del proyecto original es implementar un sistema que permita a los usuarios programar elecciones para la fecha deseada, entre los candidatos inidicados y para los electores a quienes compete. Este fork implementa la parte de los repositorios al módulo `proceso_electoral` y conexiones a base de datos del sistema, así como modelos de flujo de información entre las diversas capas.

## SOLID

El programa cumple con principios SOLID.

### 1. Principio de única responsabilidad

Cada clase en el programa se encarga de una única cosa.

```python
class EleccionModelo(db.Model):
    codigo = db.Column(db.Integer, primary_key=True)
    tipo_eleccion = db.Column(db.Text)
    fecha_inicio = db.Column(db.DateTime)
    fecha_cierre = db.Column(db.DateTime)
    lista_candidatos = db.Columnd(db.Text)

    def __repr__(self):
        return f'{self.tipo_eleccion}'
```

Las clases modelo solo tienen la función de almacenar los datos de cada objeto. La única razón para cambiarlas es agregar más datos a guardar.

### 2. Principio de apertura/cierre

Las clases implementadas se pueden extender en sus métodos sin modificar los ya existentes.

```python
class AdministradorEleccionRepositorioImpl:
    @staticmethod
    def insertar_administrador(admin):
        try:
            db.session.add(admin)
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()
    
    @staticmethod
    def eliminar_administrador(admin):
        try:
            entrada = db.session.query(AdministradorModelo).filter_by(id = admin.id).one()
            db.session.delete(entrada)
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()
```

Se puede agregar una función `get_administrador_nombre(admin_id)` de tal modo que no modifique la funcionalidad de `insertar_administrador(admin)` ni `eliminar_administrador(admin)`.

```python
    @staticmethod
    def get_administrador_nombre(admin_id):
        admin_nombre = ""
        try:
            entrada = db.session.query(AdministradorModelo).filter_by(id = admin_id).one()
            admin_nombre = entrada.nombre
        except NoResultFound:
            print(f"No se encontró una entrada con la id {admin_id}\n")
            return None
        except SQLAlchemyError as e:
            print(f"Hubo un error al consultar la base de datos: {e}")
            return None
        finally:
            db.session.close()
        return admin_nombre
```

## Estilos

### Manejo de errores/excepciones: Constructivista

El programa intenta seguir con su ejecución si sucede algún error devolviendo valores determinados "razonables".

```python
except NoResultFound:
    print(f"No se encontró una entrada con la id {admin_id}\n")
    return None
except SQLAlchemyError as e:
    print(f"Hubo un error al consultar la base de datos: {e}")
    return None
```

### Tablas de persistencia

Los datos se almacenan en una base de datos relacional a la que se accede mediante consultas SQL.

Se accede a ellos usando las funciones ORM de la biblioteca SQLAlchemy para Flask.

```python
entrada = db.session.query(AdministradorModelo).filter_by(id = admin_id).one()
admin_nombre = entrada.nombre
```

### Trinity (MVC)

La base de datos se comunica con los repositorios a través de una clase (modelo), que a su vez comunica a los repositorios con el dominio y viceversa.

```python
db.session.add(admin)
```

```python
admin_nombre = entrada.nombre
```

## Uso

Se puede acceder a los repositorios mediante su interfaz, enviando la información pertinente a través de su modelo correspondiente. La información, si existe, se extraerá de la base de datos.

## Autor

Kristopher Rospigliosi Gonzales y Leonardo Ponze Bellido
