from utils.data_structures import Stack, Queue, HashMap

####################################
#    Ejemplos de uso del Stack     #
####################################

# Instanciar la clase Stack
stack = Stack()
# Agregar elementos al Stack
stack.push(1)
stack.push('dos')   
stack.push(3)
stack.push('cuatro')
stack.push(5.0)
# Desplegar la información del Stack
print(f'Contenido del Stack: {stack.__str__()}')
# Desplegar el tamaño del Stack
print(f'Tamaño del Stack: {stack.size()}')
# Desplegar el elemento en la cima del Stack
print(f'Elemento en la cima del Stack: {stack.peek()}')
# Sacar un elemento del Stack
elemento = stack.pop()
print(f'Elemento sacado del Stack: {elemento}')
# Checar si el Stack está vacío
print(f'¿Está vacío el Stack? {stack.is_empty()}')
# Realizar una copia del Stack
copia_stack = stack.copy()
# Recorrer el Stack sacando elementos hasta que esté vacío
while not stack.is_empty():
    print(f'Elemento sacado del Stack: {stack.pop()}')
# Desplegar ambas versiones del Stack
print(f'Contenido del Stack original: {stack.__str__()}')
print(f'Contenido de la copia del Stack: {copia_stack.__str__()}')

print('\n' + '-'*50 + '\n')
####################################
#    Ejemplos de uso del Queue     #
####################################

# Instanciar la clase Queue
queue = Queue()
# Agregar elementos al Queue
queue.enqueue(1)
queue.enqueue('dos')
queue.enqueue(3)
queue.enqueue('cuatro')
queue.enqueue(5.0)
# Desplegar la información del Queue
print(f'Contenido del Queue: {queue.__str__()}')
# Desplegar el tamaño del Queue
print(f'Tamaño del Queue: {queue.size()}')
# Desplegar el elemento en la cabeza del Queue
print(f'Elemento en la cabeza del Queue: {queue.peek()}')
# Sacar un elemento del Queue
elemento = queue.dequeue()
print(f'Elemento sacado del Queue: {elemento}')
# Checar si el Queue está vacío
print(f'¿Está vacío el Queue? {queue.is_empty()}')
# Realizar una copia del Queue
copia_queue = queue.copy()
# Recorrer el Queue sacando elementos hasta que esté vacío
while not queue.is_empty():
    print(f'Elemento sacado del Queue: {queue.dequeue()}')
# Desplegar ambas versiones del Queue
print(f'Contenido del Queue original: {queue.__str__()}')
print(f'Contenido de la copia del Queue: {copia_queue.__str__()}')

print('\n' + '-'*50 + '\n')
####################################
#    Ejemplos de uso del HashMap   #
####################################

# Instanciar la clase HashMap
hash_map = HashMap()
# Agregar elementos al HashMap
hash_map.put('nombre', 'Christopher')
hash_map.put('edad', 22)
hash_map.put('ciudad', 'Santiago')
hash_map.put('pais', 'México')
# Desplegar la información del HashMap
print(f'Contenido del HashMap: {hash_map.__str__()}')
# Desplegar el tamaño del HashMap
print(f'Tamaño del HashMap: {hash_map.size()}')
# Desplegar el valor de una llave específica
print(f'Valor de la llave "nombre": {hash_map.get("nombre")}')
# Desplegar el valor de una llave que no existe
print(f'Valor de la llave "apellido": {hash_map.get("apellido")}')
# Sacar un elemento del HashMap
elemento = hash_map.remove('nombre')
print(f'Elemento sacado del HashMap: {elemento}')
# Desplegar el tamaño del HashMap después de sacar un elemento
print(f'Tamaño del HashMap después de sacar un elemento: {hash_map.size()}')
# Checar si el HashMap contiene una llave específica
print(f'¿Contiene la llave "ciudad"? {hash_map.contains_key("ciudad")}')
# Checar si el HashMap contiene una llave que no existe
print(f'¿Contiene la llave "nombre"? {hash_map.contains_key("nombre")}')
# Desplegar todas las llaves del HashMap
print(f'Llaves del HashMap: {hash_map.get_keys()}')
# Desplegar todos los valores del HashMap
print(f'Valores del HashMap: {hash_map.get_values()}')
# Crear una copia del HashMap
hash_map_copia = hash_map.copy()
# Recorrer el HashMap sacando elementos hasta que esté vacío
for key in hash_map.get_keys():
    print(f'Elemento sacado del HashMap: {hash_map.get(key)}')
    hash_map.remove(key)
# Desplegar ambas versiones del HashMap
print(f'Contenido del HashMap original: {hash_map.__str__()}')
print(f'Contenido de la copia del HashMap: {hash_map_copia.__str__()}')