# Pruebas para la Clase Stack

## Importación y Creación de la Pila

```python
from utils.data_structures import Stack

stack = Stack()
assert stack.is_empty() == True, "Error: La pila debería estar vacía al inicio."
assert stack.size() == 0, "Error: El tamaño de la pila debería ser 0."
```

## Prueba de Inserción (push) y Consulta (peek)

```python
stack.push(10)
assert stack.peek() == 10, "Error: El tope de la pila debería ser 10."
stack.push(20)
assert stack.peek() == 20, "Error: El tope de la pila debería ser 20."
```

## Prueba de Eliminación (pop)

```python
valor = stack.pop()
assert valor == 20, "Error: El valor extraído debería ser 20."
assert stack.peek() == 10, "Error: El nuevo tope debería ser 10."
stack.pop()
assert stack.is_empty() == True, "Error: La pila debería estar vacía después de eliminar todos los elementos."
```

## Prueba de Copia

```python
stack.push(30)
stack.push(40)
copied_stack = stack.copy()
assert copied_stack == [30, 40], "Error: La copia de la pila no es correcta."
```

## Prueba de Representación en Cadena (**str**)

```python
assert str(stack) == "[30, 40]", "Error: La representación de la pila no es correcta."
```

## Reporte de Evaluación de la Clase `Stack`

### **Descripción General**

La clase `Stack` es una implementación simple de una pila basada en listas de Python. Incluye métodos para operaciones estándar como `push`, `pop`, `peek`, verificación de si está vacía, obtener su tamaño y realizar una copia.

### **Resumen de Pruebas Realizadas**

1. **Inicialización**: Se verifica que una nueva pila esté vacía.
2. **Operación `push` y `peek`**: Se confirma que los elementos se agregan correctamente y `peek` devuelve el valor correcto.
3. **Operación `pop`**: Se evalúa que los elementos se eliminen en el orden adecuado (LIFO).
4. **Verificación de Vacío**: Se prueba que la pila se reconoce vacía tras la eliminación de todos sus elementos.
5. **Copia de la Pila**: Se comprueba que `copy` devuelve una copia fiel del contenido.
6. **Representación en Cadena (`__str__`)**: Se asegura que la representación
   textual de la pila sea correcta.

# Pruebas para la Clase Queue

## Importación y Creación de la Cola

```python
from utils.data_structures import Queue

queue = Queue()
assert queue.is_empty() == True, "Error: La cola debería estar vacía al inicio."
assert queue.size() == 0, "Error: El tamaño de la cola debería ser 0."
```

## Prueba de Inserción (enqueue) y Consulta (peek)

```python
queue.enqueue(10)
assert queue.peek() == 10, "Error: El frente de la cola debería ser 10."
queue.enqueue(20)
assert queue.peek() == 10, "Error: El frente de la cola aún debería ser 10."
```

## Prueba de Eliminación (dequeue)

```python
valor = queue.dequeue()
assert valor == 10, "Error: El valor extraído debería ser 10."
assert queue.peek() == 20, "Error: El nuevo frente debería ser 20."
queue.dequeue()
assert queue.is_empty() == True, "Error: La cola debería estar vacía después de eliminar todos los elementos."
```

## Prueba de Copia

```python
queue.enqueue(30)
queue.enqueue(40)
copied_queue = queue.copy()
assert str(copied_queue) == "[30, 40]", "Error: La copia de la cola no es correcta."
```

## Prueba de Representación en Cadena (**str**)

```python
assert str(queue) == "deque([30, 40])", "Error: La representación de la cola no es correcta."
```

## Reporte de Evaluación de la Clase `Queue`

### **Descripción General**

La clase `Queue` es una implementación de una cola utilizando `deque` de la biblioteca estándar de Python. Incluye métodos para operaciones estándar como `enqueue`, `dequeue`, `peek`, verificación de si está vacía, obtener su tamaño y realizar una copia.

### **Resumen de Pruebas Realizadas**

1. **Inicialización**: Se verifica que una nueva cola esté vacía.
2. **Operación `enqueue` y `peek`**: Se confirma que los elementos se agregan correctamente y `peek` devuelve el valor correcto.
3. **Operación `dequeue`**: Se evalúa que los elementos se eliminen en el orden adecuado (FIFO).
4. **Verificación de Vacío**: Se prueba que la cola se reconoce vacía tras la eliminación de todos sus elementos.
5. **Copia de la Cola**: Se comprueba que `copy` devuelve una nueva instancia de `Queue` con los mismos elementos.
6. **Representación en Cadena (`__str__`)**: Se asegura que la representación textual de la cola sea correcta.

# Pruebas para la Clase HashMap

## Importación y Creación del HashMap

```python
from utils.data_structures import HashMap

hash_map = HashMap()
assert hash_map.size() == 0, "Error: El tamaño del HashMap debería ser 0."
```

## Prueba de Inserción (put) y Obtención (get)

```python
hash_map.put("a", 10)
assert hash_map.get("a") == 10, "Error: El valor de la clave 'a' debería ser 10."
hash_map.put("b", 20)
assert hash_map.get("b") == 20, "Error: El valor de la clave 'b' debería ser 20."
```

## Prueba de Eliminación (remove)

```python
hash_map.remove("a")
assert hash_map.get("a") is None, "Error: La clave 'a' debería haber sido eliminada."
assert hash_map.size() == 1, "Error: El tamaño del HashMap debería ser 1."
```

## Prueba de Existencia de Claves (contains_key)

```python
assert hash_map.contains_key("b") == True, "Error: La clave 'b' debería existir en el HashMap."
assert hash_map.contains_key("a") == False, "Error: La clave 'a' no debería existir en el HashMap."
```

## Prueba de Obtención de Claves y Valores

```python
hash_map.put("c", 30)
assert set(hash_map.get_keys()) == {"b", "c"}, "Error: Las claves deberían ser 'b' y 'c'."
assert set(hash_map.get_values()) == {20, 30}, "Error: Los valores deberían ser 20 y 30."
```

## Prueba de Copia

```python
copied_map = hash_map.copy()
assert copied_map.get("b") == 20 and copied_map.get("c") == 30, "Error: La copia del HashMap no es correcta."
```

## Prueba de Representación en Cadena (**str**)

```python
assert str(hash_map) == "{'b': 20, 'c': 30}", "Error: La representación del HashMap no es correcta."
```

## Reporte de Evaluación de la Clase `HashMap`

### **Descripción General**

La clase `HashMap` es una implementación de un diccionario en Python que permite almacenar pares clave-valor. Incluye métodos para insertar (`put`), obtener (`get`), eliminar (`remove`), verificar la existencia de claves (`contains_key`), obtener claves y valores, copiar la estructura y representarla como cadena.

### **Resumen de Pruebas Realizadas**

1. **Inicialización**: Se verifica que un `HashMap` nuevo comienza vacío.
2. **Operación `put` y `get`**: Se confirma que los pares clave-valor se insertan y recuperan correctamente.
3. **Operación `remove`**: Se evalúa que los elementos se eliminen correctamente.
4. **Verificación de Claves (`contains_key`)**: Se comprueba si una clave está presente en el `HashMap`.
5. **Obtención de Claves y Valores (`get_keys` y `get_values`)**: Se valida que las listas de claves y valores sean correctas.
6. **Copia del `HashMap` (`copy`)**: Se asegura que la copia mantenga los mismos datos sin modificar la estructura original.
7. **Representación en Cadena (`__str__`)**: Se prueba que la conversión a cadena funcione correctamente.
