---
name: verificar
description: Verifica que el proyecto esté listo para commit y push (tests, estilo con ruff, que el sistema arranque y responda) y corrige lo que falle. Usar antes de cada push, después de cambios grandes o cuando algo "dejó de andar".
---

# Verificar el proyecto

1. Ejecutá `python herramientas/verificar.py --arreglar` desde la raíz, con el entorno virtual
   activado.
2. Si todo da `[ OK  ]`: avisá que se puede hacer commit y push. Los `[AVISO]` no bloquean.
3. Si algo da `[FALLA]`:
   - **Tests**: leé el error, encontrá la causa en el código y arreglala. Nunca borres, saltees ni
     debilites un test para que pase. Si el test quedó viejo porque cambió el dominio a propósito,
     actualizalo para que pruebe el comportamiento nuevo.
   - **Estilo (ruff)**: el `--arreglar` corrige casi todo solo. Lo que quede (por ejemplo, líneas
     de más de 100 caracteres), arreglalo a mano.
   - **Arranque**: suele ser un error de importación o de plantilla. Leé el mensaje y corregilo.
4. Volvé a correr el paso 1 hasta que no haya `[FALLA]`.
5. Resumí en 3 líneas qué estaba mal y qué cambiaste.
