"""
Configuración básica para Behave
"""

import os
import tempfile
import json
from todo_list import TodoListManager


def before_all(context):
    """Configurar antes de todas las pruebas."""
    context.test_mode = True


def before_scenario(context, scenario):
    """Configurar antes de cada escenario"""
    # Crear archivo temporal para cada test
    context.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    
    # Inicializar el archivo con estructura JSON vacía
    initial_data = {
        'next_id': 1,
        'tasks': []
    }
    json.dump(initial_data, context.temp_file, indent=2)
    context.temp_file.close()
    
    context.todo_manager = TodoListManager(context.temp_file.name)


def after_scenario(context, scenario):
    """Limpiar después de cada escenario"""
    # Eliminar archivo temporal
    if hasattr(context, 'temp_file'):
        try:
            os.unlink(context.temp_file.name)
        except:
            pass


def after_all(context):
    """Limpiar después de todas las pruebas."""
    pass
