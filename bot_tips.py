import asyncio
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ================= CONFIGURACIÓN =================
TOKEN = "8872233675:AAFjgeCbxveA2KPBfO3t5Rvh1Vrn_4oVQjg"     # SÍ lleva comillas
CHAT_ID = -1003848794032           # NO lleva comillas (Tu número largo con -100)
TEMA_ID = 7                        # NO lleva comillas (Tu número de tema pequeño)
# =================================================

# --- BASE DE DATOS DE 25 TIPS EXPLICATIVOS PARA PRINCIPIANTES ---
TIPS_PYTHON = [
    """💡 **Concepto Clave: ¿Por qué Python usa variables?**
Una variable es como una caja con una etiqueta donde guardas datos para usarlos después. En otros lenguajes tienes que decirle a la PC si vas a guardar texto o números, pero en Python es inteligente y lo adivina solo.

📝 **Ejemplo:**
`edad = 18`  #(Crea la caja 'edad' y le mete el número 18)
`print(edad)` #(Muestra el 18 en pantalla)

⚠️ **Error común:** No uses espacios en los nombres. Si pones `mi edad = 18` dará error. Usa guion bajo: `mi_edad = 18`.""",

    """💡 **Concepto Clave: Cuidado con las Mayúsculas**
A esto los programadores le llamamos 'Case Sensitive'. Para Python, una letra mayúscula y una minúscula son totalmente diferentes. Si creas una variable llamada 'puntuacion', no intentes llamarla después como 'Puntuacion'.

📝 **Ejemplo:**
`mensaje = "Hola"`
`print(Mensaje)`  #❌ Esto romperá tu programa con un error llamado 'NameError'

⚠️ **Consejo:** Acostúmbrate a escribir todo el nombre de tus variables siempre en minúsculas.""",

    """💡 **Concepto Clave: ¿Qué es una f-string?**
Cuando quieres mezclar texto escrito por ti con el valor de una variable, la forma más moderna y fácil de hacerlo es usando una 'f-string'. Solo debes poner una letra `f` antes de las comillas y meter la variable entre llaves `{ }`.

📝 **Ejemplo:**
`nombre = "Carlos"`
`print(f"Bienvenido al curso de Python, {nombre}!")`
# Resultado: Bienvenido al curso de Python, Carlos!

⚠️ **Ahorro de dolores de cabeza:** Te evita tener que usar signos de suma (+) para pegar textos, lo cual suele dar muchos errores.""",

    """💡 **Concepto Clave: El truco de la función input()**
La función `input()` sirve para que el usuario pueda escribir un dato desde su teclado. Pero ojo: Python tiene una regla estricta: **Todo lo que entra por input() se convierte en texto**, aunque el usuario escriba un número.

📝 **Ejemplo:**
`edad = input("¿Cuántos años tienes? ")`
# Si el usuario escribe 20, Python guarda "20" (como palabra, no como número). No podrás sumarle nada.

⚠️ **Solución:** Si vas a hacer matemáticas con ese dato, conviértelo a número entero con `int()` así:
`edad = int(input("¿Cuántos años tienes? "))`""",

    """💡 **Concepto Clave: ¿Para qué sirve el operador % (Módulo)?**
En la escuela nos enseñaron que al división de dos números queda un residuo o sobrante si no es exacta. El signo de porcentaje `%` in Python no calcula porcentajes, sino que te da ese residuo. Es el truco número uno para saber si un número es par.

📝 **Ejemplo:**
`print(10 % 2)` # Da 0 (porque 10 dividido 2 da 5 exacto, sobra 0).
`print(11 % 2)` # Da 1 (porque sobra 1).

⚠️ **Uso real:** Si haces `numero % 2 == 0` and da verdadero, tienes un número par asegurado.""",

    """💡 **Concepto Clave: La Sangría Obligatoria (Indentación)**
En Python, los espacios al inicio de una línea no son por estética; son órdenes para la computadora. Cuando usas un `if` o un bucle, el código que va dentro **debe tener 4 espacios hacia la derecha** (un tabulador). Así Python sabe qué código depende de esa condición.

📝 **Ejemplo correcto:**
```python
if 5 > 3:
    print("Esto está adentro del IF")
print("Esto ya está afuera")
```

⚠️ **Error de principiante:** Si dejas el código pegado a la izquierda después de un `if:`, verás el famoso error `IndentationError: expected an indented block`.""",

    """💡 **Concepto Clave: Distinguir entre = y ==**
Este es el error en el que todos caemos las primeras semanas. 
- Un solo signo `=` sirve para GUARDAR algo en una variable (Asignación).
- Dos signos `==` sirven para PREGUNTAR si dos cosas son iguales (Comparación).

📝 **Ejemplo:**
`precio = 100` # Guarda el 100 en la variable.
`if precio == 100:` # Pregunta: ¿El precio vale 100?

⚠️ **Ten cuidado:** Si pones un solo `=` dentro de un `if`, Python te avisará que hay un error de sintaxis.""",

    """💡 **Concepto Clave: ¿Cómo funciona el rango en un bucle FOR?**
El bucle `for` sirve para repetir una acción. Normalmente lo usamos junto a `range()`. Una regla vital es que **el número final de range nunca se incluye**.

📝 **Ejemplo:**
```python
for x in range(1, 5):
    print(x)
```
# Imprimirá: 1, 2, 3, 4 (El 5 se queda afuera).

⚠️ **Nota:** Si solo pones un número como `range(3)`, empezará automáticamente desde el cero: 0, 1, 2.""",

    """💡 **Concepto Clave: Listas y el Índice Cero**
Las listas son como archivadores donde guardas muchas cosas juntas usando corchetes `[]`. Para la informática, el conteo no empieza en 1, ¡empieza en 0! El primer elemento siempre vive en la posición cero.

📝 **Ejemplo:**
`alumnos = ["Ana", "Pedro", "Luis"]`
`print(alumnos[0])` # Mostrará a Ana.
`print(alumnos[1])` # Mostrará a Pedro.

⚠️ **Error típico:** Si intentas buscar `alumnos[3]`, el programa fallará con un error `IndexError` porque la posición 3 no existe (las posiciones son 0, 1 y 2).""",

    """💡 **Concepto Clave: ¿Qué es la inmutabilidad de una Tupla?**
Las Tuplas son primas hermanas de las listas, pero se crean con paréntesis `()` en vez de corchetes. Su única y gran diferencia es que son "inmutables": una vez que las creas, **está prohibido modificarlas, añadir o borrar elementos**.

📝 **Ejemplo:**
`meses = ("Enero", "Febrero", "Marzo")`
`meses[0] = "Abril"` # ❌ ERROR: Python detendrá el programa de inmediato.

⚠️ **¿Cuándo usarla?:** Úsala para datos que sabes que jamás deben cambiar en tu programa, como los días de la semana.""",

    """💡 **Concepto Clave: Agregar datos con .append()**
Cuando creas una lista, muchas veces querrás meterle nuevos datos mientras tu programa avanza. El método `.append()` sirve exclusivamente para eso: toma lo que le dejes entre paréntesis y lo manda directo al final de tu lista.

📝 **Ejemplo:**
`juegos = ["Zelda", "Mario"]`
`juegos.append("Minecraft")`
`print(juegos)` # Resultado: ['Zelda', 'Mario', 'Minecraft']

⚠️ **Atención:** Solo puedes agregar un elemento a la vez con cada .append().""",

    """💡 **Concepto Clave: Saber el tamaño con len()**
La palabra `len` viene de 'length' (longitud en inglés). Es una función comodín en Python: si le pasas una lista, te dice cuántos elementos tiene guardados. Si le pasas un texto, te cuenta cuántas letras y espacios tiene en total.

📝 **Ejemplo:**
`numeros = [10, 20, 30, 40]`
`print(len(numeros))` # Resultado: 4
`print(len("Hola"))`   # Resultado: 4

⚠️ **Utilidad:** Es vital para controlar condicionales, como verificar si un usuario escribió una contraseña demasiado corta.""",

    """💡 **Concepto Clave: Comentarios con #**
Un comentario es texto que escribes dentro de tu archivo de código pero que la computadora ignora por completo al ejecutarlo. Se activan poniendo el símbolo de numeral `#`. Sirven para dejar notas a ti mismo del futuro o explicarle tu lógica a tus compañeros.

📝 **Ejemplo:**
`x = 100  # Esta variable guarda el puntaje máximo`
`# print("Esto no se ejecutará")`

⚠️ **Buena práctica:** No llenes todo de comentarios obvios. Úsalos solo para explicar partes del código que sean difíciles de entender.""",

    """💡 **Concepto Clave: Operadores Lógicos - El 'and'**
Cuando usas un `if`, a veces necesitas que se cumplan dos condiciones obligatoriamente a la vez para poder avanzar. El operador `and` (que significa 'y') une esas condiciones y exige que ambas resulten verdaderas.

📝 **Ejemplo:**
`usuario = "admin"`
`clave = "1234"`
`if usuario == "admin" and clave == "1234":`
`    print("Acceso concedido")`

⚠️ **Regla estricta:** Si el usuario es correcto pero la clave está mal, o viceversa, el `and` dará Falso y nadie entrará."""
]

# --- LÓGICA DE PROGRAMACIÓN DEL BOT ---

async def mandar_tip_al_tema(bot):
    tip_seleccionado = random.choice(TIPS_PYTHON)
    try:
        await bot.send_message(
            chat_id=CHAT_ID,
            text=tip_seleccionado,
            message_thread_id=TEMA_ID
        )
        print("🤖 Tip enviado con éxito al tema.")
    except Exception as e:
        print(f"❌ Error al enviar tip: {e}")

async def bucle_temporal(application):
    await asyncio.sleep(10) # Espera 10 segundos al iniciar antes de mandar el primer tip
    while True:
        await mandar_tip_al_tema(application.bot)
        await asyncio.sleep(3600) # Espera exactamente 1 hora (3600 segundos)

async def responder_palabra_tip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id == CHAT_ID and update.effective_message.message_thread_id == TEMA_ID:
        texto_usuario = update.effective_message.text.lower()
        if "tip" in texto_usuario or texto_usuario == "/tip":
            await mandar_tip_al_tema(context.bot)

async def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_palabra_tip))
    application.add_handler(CommandHandler("tip", responder_palabra_tip))
    
    # Aquí activamos el reloj automático en segundo plano para que corra cada hora
    asyncio.create_task(bucle_temporal(application))

    print("🚀 El Bot está encendido y escuchando el chat... (Presiona Ctrl+C para apagar)")
    await application.run_polling()

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())

