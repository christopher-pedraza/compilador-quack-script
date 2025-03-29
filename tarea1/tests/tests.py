import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from tarea1.utils.data_structures import Stack, Queue, HashMap

# Stack Tests
stack = Stack()
assert stack.is_empty() == True, "Error: La pila debería estar vacía al inicio."
assert stack.size() == 0, "Error: El tamaño de la pila debería ser 0."

stack.push(10)
assert stack.peek() == 10, "Error: El tope de la pila debería ser 10."
stack.push(20)
assert stack.peek() == 20, "Error: El tope de la pila debería ser 20."

valor = stack.pop()
assert valor == 20, "Error: El valor extraído debería ser 20."
assert stack.peek() == 10, "Error: El nuevo tope debería ser 10."
stack.pop()
assert stack.is_empty() == True, "Error: La pila debería estar vacía después de eliminar todos los elementos."

stack.push(30)
stack.push(40)
copied_stack = stack.copy()
assert copied_stack != stack, "Error: La copia no debería ser la misma referencia."

assert str(stack) == "[30, 40]", "Error: La representación de la pila no es correcta."

#
# Queue Tests
#

# Importación y Creación de la Cola
queue = Queue()
assert queue.is_empty() == True, "Error: La cola debería estar vacía al inicio."
assert queue.size() == 0, "Error: El tamaño de la cola debería ser 0."

# Prueba de Inserción (enqueue) y Consulta (peek)
queue.enqueue(10)
assert queue.peek() == 10, "Error: El frente de la cola debería ser 10."
queue.enqueue(20)
assert queue.peek() == 10, "Error: El frente de la cola aún debería ser 10."

# Prueba de Eliminación (dequeue)
valor = queue.dequeue()
assert valor == 10, "Error: El valor extraído debería ser 10."
assert queue.peek() == 20, "Error: El nuevo frente debería ser 20."
queue.dequeue()
assert queue.is_empty() == True, "Error: La cola debería estar vacía después de eliminar todos los elementos."

# Prueba de Copia (copy)
queue.enqueue(30)
queue.enqueue(40)
copied_queue = queue.copy()
assert str(copied_queue) == "[30, 40]", "Error: La copia de la cola no es correcta."

# Prueba de Representación en Cadena (**str**)
assert str(queue) == "[30, 40]", "Error: La representación de la cola no es correcta."

#
# HashMap Tests
#

# Importación y Creación del HashMap
hash_map = HashMap()
assert hash_map.size() == 0, "Error: El tamaño del HashMap debería ser 0."

# Prueba de Inserción (put) y Obtención (get)
hash_map.put("a", 10)
assert hash_map.get("a") == 10, "Error: El valor de la clave 'a' debería ser 10."
hash_map.put("b", 20)
assert hash_map.get("b") == 20, "Error: El valor de la clave 'b' debería ser 20."

# Prueba de Eliminación (remove)
hash_map.remove("a")
assert hash_map.get("a") is None, "Error: La clave 'a' debería haber sido eliminada."
assert hash_map.size() == 1, "Error: El tamaño del HashMap debería ser 1."

# Prueba de Existencia de Claves (contains_key)
assert hash_map.contains_key("b") == True, "Error: La clave 'b' debería existir en el HashMap."
assert hash_map.contains_key("a") == False, "Error: La clave 'a' no debería existir en el HashMap."

# Prueba de Obtención de Claves y Valores
hash_map.put("c", 30)
assert set(hash_map.get_keys()) == {"b", "c"}, "Error: Las claves deberían ser 'b' y 'c'."
assert set(hash_map.get_values()) == {20, 30}, "Error: Los valores deberían ser 20 y 30."

# Prueba de Copia
copied_map = hash_map.copy()
assert copied_map.get("b") == 20 and copied_map.get("c") == 30, "Error: La copia del HashMap no es correcta."

# Prueba de Representación en Cadena (**str**)
assert str(hash_map) == "{'b': 20, 'c': 30}", "Error: La representación del HashMap no es correcta."