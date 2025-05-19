

# 🎵 wavenaut: Mi Generador de Sonidos Procedurales Open Source

> **wavenaut** es una herramienta FOSS (Libre y de Código Abierto) que he diseñado para la creación de sonidos y efectos musicales procedurales a través de una interfaz gráfica intuitiva. Nace con la misión de empoderar a desarrolladores indie y pequeños creadores, ofreciendo una alternativa potente y accesible para generar SFX, música procedural o presets personalizados sin depender de costosas licencias de software comercial.

-----

## 🌟 ¿Por qué wavenaut? Mi Inspiración

Creo firmemente que la creatividad no debe estar limitada por el presupuesto. `wavenaut` surge de la necesidad que identifiqué de ofrecer a los desarrolladores independientes, estudiantes y aficionados al audio, herramientas robustas y flexibles para la creación sonora. Quiero que puedas dar vida a tus proyectos, ya sean juegos retro, experiencias indie innovadoras o prototipos rápidos, con sonidos únicos y de calidad, sin que el costo sea una barrera. ¡Los pequeños estudios y los creadores apasionados merecen herramientas geniales\!

-----

## 🎯 ¿Qué puedes lograr con wavenaut?

`wavenaut` es un **generador procedural de audio** en evolución que actualmente te permite:

  * ✅ Generar ondas fundamentales: Senoidal, Cuadrada, Triangular, Diente de Sierra y Ruido Blanco.
  * ✅ Aplicar una envolvente ADSR básica para modelar la amplitud de tus sonidos.
  * ✅ Guardar y cargar tus creaciones como presets en formato `.json`.
  * ✅ Escuchar los sonidos directamente desde la interfaz gráfica (`tkinter`).
  * ✅ Visualizar en tiempo real una representación básica de las formas de onda generadas.

**En el horizonte (¡y estoy trabajando en ello\!):**

  * 🚀 **Migración a PySide6:** Para una interfaz de usuario más moderna, potente y personalizable.
  * 🎛️ **Más Poder Sonoro:** Incorporación de filtros (paso bajo, paso alto, etc.), efectos (reverb, delay) y una funcionalidad completa de exportación a formato `.wav`.
  * 🎼 **Composición Procedural:** Herramientas para la generación de secuencias musicales y patrones rítmicos.
  * 🌍 **Comunidad y Recursos:** Creación de un espacio para compartir presets, tutoriales y fomentar la colaboración.

-----

## 🐢 Filosofía de Desarrollo: Lento Pero Seguro

Este proyecto lo estoy desarrollando a fuego lento, adoptando un enfoque **modular, granular y incremental**.

  * **Pequeños Pasos, Grandes Avances:** Cada commit representa una funcionalidad completa y probada.
  * **Aprendizaje Continuo:** Desarrollo y aprendo en cada fase.
  * **Evitar el Burnout:** Un ritmo sostenible para mantener la pasión y la calidad.
  * **Siempre Funcional:** Mi objetivo es tener una base operativa en todo momento.
  * **Código Limpio y Modular:** Facilitando el mantenimiento, la colaboración futura y la escalabilidad.

-----

## ⚙️ Requisitos Técnicos

  * **Python:** 3.10+ (desarrollado y probado principalmente con 3.13).
  * **Bibliotecas Esenciales:**
      * `numpy` (para el manejo numérico y generación de arrays de audio).
      * `sounddevice` (para la reproducción de audio).
      * `soundfile` (para la lectura/escritura de archivos de audio, especialmente `.wav`).
  * **Interfaz Gráfica (Actual):**
      * `tkinter` (generalmente incluido en la instalación estándar de Python).
  * **Interfaz Gráfica (Futura):**
      * `PySide6` (se especificará como dependencia opcional o principal en fases futuras).

-----

## 🧪 Instalación y Ejecución Rápida

¡Pon en marcha wavenaut en pocos pasos\!

```bash
# 1. Clona el repositorio (si aún no lo tienes)
# git clone https://github.com/casmian/wavenaut.git
# cd wavenaut

# 2. Crea y activa un entorno virtual (recomendado)
python -m venv venv
# En Linux/macOS:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# 3. Instala las dependencias
pip install numpy sounddevice soundfile

# 4. Ejecuta la aplicación
# Asegúrate de estar en el directorio raíz del proyecto
python src/wavenaut/ui/gui/main_window.py
```

-----

## 🧭 Hoja de Ruta Actual del Proyecto

Actualmente me encuentro transitando las **Fases 2.5 → 2.6**.

**Logros Recientes:**

  * Generación de ondas básicas.
  * Implementación de envolvente ADSR.
  * Sistema de guardado y carga de presets.
  * Visualización básica de la forma de onda.
  * Reproducción de audio desde la GUI.

**Siguientes Pasos Inmediatos:**

  * Preparación y primeros pasos para la migración de la interfaz a `PySide6`.
  * Mejora en la validación de parámetros de entrada.
  * Ampliación y refinamiento de la documentación interna y para el usuario.
  * Implementación robusta de exportación a `.wav`.

-----

## 📊 Funcionalidades Clave: ¿Qué puedes hacer ya?

| Acción                                  | Estado Actual                     |
| :-------------------------------------- | :-------------------------------- |
| Generar ondas simples (seno, cuadrada, etc.) | ✅ Implementado                   |
| Aplicar envolvente ADSR                 | ✅ Implementado                   |
| Guardar y cargar presets (`.json`)        | ✅ Implementado                   |
| Visualizar forma de onda generada       | ✅ Implementado (Básico)          |
| Reproducir sonido desde la GUI          | ✅ Implementado                   |
| Exportar sonido como archivo `.wav`     | ⚠️ Parcialmente (Mejoras en curso) |

-----

## 🤝 ¡Tu Colaboración es Bienvenida\!

Aunque actualmente desarrollo `wavenaut` en solitario, ¡las contribuciones son bienvenidas y muy apreciadas\! `wavenaut` es un proyecto con espíritu comunitario. Si tienes interés en ayudar, estas son algunas áreas donde tu experiencia sería valiosa:

  * 🎨 **Diseño de Interfaz (UI/UX):** Especialmente con `PySide6`.
  * 🎹 **Síntesis de Audio Avanzada:** Implementación de más tipos de osciladores, LFOs, modulaciones.
  * 🎧 **Procesamiento de Señales:** Desarrollo de filtros, efectos (delay, reverb, chorus).
  * 🔌 **Soporte MIDI:** Integración para control mediante dispositivos MIDI.
  * 🌍 **Traducciones y Documentación:** Ayúdame a hacer `wavenaut` accesible globalmente con tutoriales, guías y traducciones.
  * 🧪 **Pruebas (Testing):** Creación de tests unitarios y de integración para asegurar la estabilidad.

Si quieres contribuir, por favor, revisa los [**issues abiertos**](https://github.com/casmian/wavenaut/issues) o crea uno nuevo para proponer tus ideas.

-----

## 📜 Licencia

Este proyecto está bajo la licencia **GNU General Public License v3.0**.  
Esto significa que cualquier persona puede usarlo, estudiarlo, modificarlo y distribuirlo libremente, siempre que respete la misma licencia.

Ver el archivo [LICENSE](LICENSE) para más detalles.

-----

## 📬 Contacto y Comunidad

¿Tienes ideas, preguntas, sugerencias o simplemente quieres charlar sobre el proyecto?

  * **Para discusiones técnicas, reportes de bugs o sugerencias de características:** Abre un [**Issue en GitHub**](https://github.com/casmian/wavenaut/issues).
  * **Para contacto más personal o consultas generales:** Puedes encontrarme en mi perfil de [**GitHub: casmian**](https://github.com/casmian).

-----

## ❤️ Apoya a Wavenaut

Wavenaut es un proyecto que desarrollo con pasión y de forma gratuita para la comunidad. Si utilizas Wavenaut y especialmente si generas música que usas en proyectos comerciales (¡lo cual es genial y te animo a ello!):

* **Considera dar crédito:** Una simple mención como "Música creada con Wavenaut por [tu nombre/estudio]" en los créditos de tu juego, video o pista musical ayuda mucho a dar a conocer la herramienta.
* **Comparte tus creaciones (presets):** Si creas presets interesantes, considera compartirlos con la comunidad (crearemos este repositorio pronto).
* **Feedback:** Tus comentarios sobre cómo mejorar Wavenaut son increíblemente valiosos.

---
¡Cualquier forma de apoyo es bienvenida y muy apreciada, pero sobre todo, disfruta creando!


¡Gracias por tu interés en wavenaut\! Espero construir una herramienta sonora increíble y, con futuras colaboraciones, ¡hacerla aún mejor\!