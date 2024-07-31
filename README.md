# Repositorios del sistema de elecciones online

Fork del [Sistema de elecciones online](https://github.com/Kiw1i/ingenieria_software)

## Descripción

El objetivo del proyecto original es implementar un sistema que permita a los usuarios programar elecciones para la fecha deseada, entre los candidatos inidicados y para los electores a quienes compete. Este fork implementa la parte de los repositorios al módulo `proceso_electoral` y conexiones a base de datos del sistema, así como modelos de flujo de información entre las diversas capas.

## Tabla de contenidos

1. [Prácticas de *clean code*](#practicas-de-clean-code)
    - [Variables, funciones y métodos](#variables-funciones-y-metodos)
    - [Clases](#clases)
    - [Nombres descriptivos](#nombres-descriptivos)
2. [SOLID](#solid)
    - [Principio de única responsabilidad](#1-principio-de-unica-responsabilidad)
    - [Principio de apertura/cierre](#2-principio-de-apertura-cierre)
3. [Estilos](#estilos)
    - [Manejo de errores/excepciones](#manejo-de-errores-excepciones-constructivista)
    - [Tablas de persistencia](#tablas-de-pertinencia)
    - [Trinity (MVC)](#trinity-mvc)
4. [Uso](#uso)
5. [Autor](#autor)

## Prácticas de *clean code*

### Variables, funciones y métodos

Según el PEP8; variables, funciones y métodos deben seguir la convención lower_snake_case.

```python
    def eliminar_eleccion(eleccion):
        try:
            entrada = db.session.query(EleccionModelo).filter_by(codigo = eleccion.codigo).one()
            db.session.delete(entrada)
            db.session.commit
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()
```

### Clases

Según el PEP8, las clases deben seguir la convención UpperCamelCase.

```python
class AdministradorEleccionRepositorioImpl:
    ...
```

### Nombres descriptivos

Es una buena práctica declarar nombres que den un entendimiento más claro del propósito del objeto.

```python
    codigo = db.Column(db.Integer, primary_key=True)
    tipo_eleccion = db.Column(db.Text)
    fecha_inicio = db.Column(db.DateTime)
    fecha_cierre = db.Column(db.DateTime)
    lista_candidatos = db.Columnd(db.Text)
```

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

Kristopher Rospigliosi Gonzales
