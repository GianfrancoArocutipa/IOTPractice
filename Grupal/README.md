# Guía de Exposición: Diapositivas 5 a 8 (Brokers MQTT en la Nube)

Este documento contiene la guía completa para dominar y exponer las **diapositivas 5 a la 8** de la presentación **"Protocolo MQTT con Broker en la Nube"** (asociada a la monografía de investigación del curso).

Cada diapositiva está diseñada y calibrada para una exposición fluida de **1 minuto y medio a 1 minuto con 45 segundos (máximo 2 minutos por diapositiva)**, garantizando profundidad técnica, claridad didáctica y cumplimiento estricto del tiempo.

---

## 🎧 Audios de Práctica Disponibles

En esta misma carpeta (`c:\Users\PC\Desktop\oit\Grupal`) se han generado los archivos de audio en formato MP3 con voz neural profesional en español para escuchar el tono, ritmo y pausas recomendadas:

| Archivo de Audio | Diapositiva | Duración estimada |
| :--- | :--- | :--- |
| [audio_ppt5_ecosistemas_nube.mp3](file:///c:/Users/PC/Desktop/oit/Grupal/audio_ppt5_ecosistemas_nube.mp3) | **PPT 5:** AWS IoT Core vs Azure IoT Hub | ~1 min 30 s |
| [audio_ppt6_prototipado_visualizacion.mp3](file:///c:/Users/PC/Desktop/oit/Grupal/audio_ppt6_prototipado_visualizacion.mp3) | **PPT 6:** Adafruit IO vs ThingsBoard Cloud | ~1 min 35 s |
| [audio_ppt7_analitica_apps.mp3](file:///c:/Users/PC/Desktop/oit/Grupal/audio_ppt7_analitica_apps.mp3) | **PPT 7:** ThingSpeak vs Ubidots | ~1 min 35 s |
| [audio_ppt8_rendimiento_autoalojamiento.mp3](file:///c:/Users/PC/Desktop/oit/Grupal/audio_ppt8_rendimiento_autoalojamiento.mp3) | **PPT 8:** Flespi vs Mosquitto (VPS) | ~1 min 40 s |
| **[audio_completo_ppt_5_a_8.mp3](file:///c:/Users/PC/Desktop/oit/Grupal/audio_completo_ppt_5_a_8.mp3)** | **Audio unificado directo (PPT 5 -> 6 -> 7 -> 8)** | **6 min 03 s** |
| [audio_exposicion_completa_ppt_5_a_8.mp3](file:///c:/Users/PC/Desktop/oit/Grupal/audio_exposicion_completa_ppt_5_a_8.mp3) | Exposición con transiciones guiadas | ~6 min 40 s |

---

## 🗺️ Mapa General del Bloque (Comparativa de Brokers)

Tu bloque comprende la **segunda a la quinta parte** de la gran comparativa de brokers en la nube:
1. **PPT 5 (2/5): Ecosistemas en la nube** $\rightarrow$ Gigantes empresariales con máxima seguridad y servicios integrados (AWS vs Azure).
2. **PPT 6 (3/5): Prototipado y Visualización** $\rightarrow$ Agilidad para microcontroladores y dashboards (Adafruit IO vs ThingsBoard). *(¡Aquí enlazas con la práctica del ESP32!)*.
3. **PPT 7 (4/5): Analítica y Aplicaciones Web** $\rightarrow$ Cálculo matemático avanzado vs aplicaciones web y alertas para clientes (ThingSpeak vs Ubidots).
4. **PPT 8 (5/5): Rendimiento y Autoalojamiento** $\rightarrow$ Especialización telemática de alta velocidad vs soberanía absoluta y código abierto (Flespi vs Mosquitto en VPS).

---

## 📌 DIAPOSITIVA 5: Ecosistemas en la Nube (AWS IoT Core vs Azure IoT Hub)

### 1. ¿De qué trata esta PPT?
Compara las soluciones de los dos mayores proveedores de nube pública a nivel mundial (**Amazon Web Services** y **Microsoft Azure**). Ambas plataformas van mucho más allá de un broker MQTT simple: son **plataformas IoT completas a hiperescala**.

- **AWS IoT Core**:
  - *Autenticación:* Emplea **autenticación mutua TLS (mTLS) con certificados X.509**. No usa simple usuario/contraseña; cada microcontrolador debe tener su propio certificado digital criptográfico y clave privada.
  - *Procesamiento:* Posee un **motor de reglas interno basado en sintaxis SQL**. Si llega un mensaje MQTT en el tópico `sensores/temperatura`, el motor de reglas puede insertar el registro en DynamoDB o ejecutar una función AWS Lambda en milisegundos sin requerir un servidor intermedio.
  - *Integración:* Enlace directo con S3, CloudWatch, Kinesis, SNS, etc.
- **Azure IoT Hub**:
  - *Seguridad:* Gestión centralizada de identidades con tokens SAS (Shared Access Signature) o certificados X.509, y uso de **Device Twins (Gemelos Digitales)** para mantener el estado virtual y configuración del dispositivo sincronizados en la nube.
  - *Protocolos:* Soporta MQTT, pero con **restricciones o implementación parcial del estándar puro** (por ejemplo, exige tópicos predefinidos como `devices/{device_id}/messages/events/` y nombres de usuario específicos).
  - *Integración:* Conexión nativa con Azure Stream Analytics, Event Hubs, Azure Functions y Power BI.

### 2. ¿Cómo exponerla? (Estrategia)
- **Tono:** Seguro, corporativo y técnico.
- **Apertura:** Deja claro que aquí no hablamos de simples brokers, sino de *suites empresariales completas*.
- **Contraste clave:** Resalta que la seguridad aquí es de grado bancario/militar (certificados X.509), pero la contraparte es una **mayor complejidad de configuración y curva de aprendizaje** frente a un broker clásico.
- **Tiempo meta:** ~1 minuto y 30 segundos.

### 3. Guion para Exponer (Palabra por palabra)
> *"Continuando con la comparativa de brokers, en esta quinta diapositiva analizamos los dos mayores ecosistemas en la nube del mercado: **AWS IoT Core** y **Azure IoT Hub**. Ambos son plataformas integrales diseñadas para entornos industriales y corporativos de gran escala.*
>
> *Por un lado, **AWS IoT Core** destaca por su enfoque estricto en la seguridad perimetral. Emplea autenticación mutua mediante certificados digitales X.509, garantizando que cada dispositivo esté plenamente autenticado antes de transmitir un solo byte. Además, cuenta con un potente motor de reglas interno que permite enrutar los mensajes MQTT entrantes directamente hacia bases de datos como DynamoDB o funciones Lambda sin necesidad de programar servidores intermediarios.*
>
> *Por otro lado, **Azure IoT Hub** ofrece una gestión robusta de la identidad de los dispositivos mediante gemelos digitales o Device Twins, lo que permite sincronizar la configuración y el estado de los equipos en la nube aun cuando estos estén desconectados. No obstante, un detalle técnico clave es que Azure implementa un soporte adaptado o parcial del estándar MQTT puro, exigiendo estructuras de tópicos y credenciales muy específicas.*
>
> *En conclusión, ambas opciones son la cúspide en robustez y escalabilidad masiva dentro de la nube empresarial, aunque demandan una mayor curva de configuración frente a un broker convencional."*

### 4. Preguntas típicas del docente y respuestas
- **¿Por qué se dice que Azure IoT Hub tiene soporte "parcial" de MQTT?**  
  *Respuesta:* Porque no permite suscribirse a tópicos completamente libres y arbitrarios como un broker estándar; exige una convención rígida de tópicos (`devices/{id}/messages/...`) y no admite todas las variantes de QoS o tópicos retenidos tradicionales.
- **¿Qué ventaja da un motor de reglas en AWS IoT Core?**  
  *Respuesta:* Elimina el costo y latencia de mantener un backend intermedio (como un servidor Node.js o Python) solo para leer de MQTT y guardar en base de datos. El motor de reglas lo hace nativamente.

---

## 📌 DIAPOSITIVA 6: Prototipado y Visualización (Adafruit IO vs ThingsBoard Cloud)

### 1. ¿De qué trata esta PPT?
Aborda las plataformas orientadas a la **agilidad de despliegue, supervisión gráfica y control de dispositivos**, pasando desde el ámbito académico/maker hasta soluciones comerciales avanzadas.

- **Adafruit IO**:
  - *Interfaz:* Dashboards listos para usar en minutos con widgets prediseñados (indicadores numéricos, medidores tipo aguja, botones deslizantes, gráficas históricas).
  - *Agilidad:* No requiere diseñar un frontend web. Ideal para probar hipótesis y desplegar telemetría en pocas líneas de código.
  - *Hardware:* Soporte de primer nivel para microcontroladores de bajo costo como **ESP32**, ESP8266 y Arduino mediante librerías oficiales (`Adafruit_MQTT.h`).
  - *Vínculo con el trabajo:* **¡Es el broker que utilizamos en el caso práctico de nuestra monografía con el ESP32 y el sensor LDR!**
- **ThingsBoard Cloud**:
  - *Núcleo:* Broker MQTT nativo y escalable de alto rendimiento.
  - *Visualización:* Paneles dinámicos de nivel industrial totalmente personalizables con mapas geográficos, diagramas de planta y widgets interactivos.
  - *Administración:* Gestión integral de flotas: jerarquía de entidades (dispositivos, activos, edificios, clientes) y gestión granular de credenciales (tokens, certificados).
  - *Lógica:* Motor de reglas avanzado basado en diagramas de flujo de nodos (Rule Engine) que procesa filtros, alarmas y cálculos en vuelo.

### 2. ¿Cómo exponerla? (Estrategia)
- **Tono:** Dinámico, conectando la teoría con la práctica.
- **Momento estelar:** Al hablar de Adafruit IO, **menciona con orgullo que este es el broker con el que tu equipo montó la experiencia práctica** del sistema de alumbrado inteligente y telemetría en el laboratorio. Esto demuestra coherencia entre la teoría y la práctica.
- **Contraste clave:** Adafruit IO es el rey de la velocidad y el prototipado; ThingsBoard es el paso natural cuando ese prototipo necesita convertirse en un producto comercial con gestión de flotas.
- **Tiempo meta:** ~1 minuto y 35 segundos.

### 3. Guion para Exponer (Palabra por palabra)
> *"En la sexta diapositiva entramos al grupo de prototipado y visualización, comparando **Adafruit IO** frente a **ThingsBoard Cloud**. Aquí el objetivo cambia de la infraestructura corporativa hacia la velocidad de desarrollo y la supervisión gráfica.*
>
> *Comenzamos con **Adafruit IO**, que es la plataforma líder para educación y prototipado rápido. Su gran ventaja es la agilidad: nos permite crear feeds MQTT y tableros visuales interactivos con botones, medidores y gráficas en cuestión de minutos. Es altamente amigable con microcontroladores como el ESP32 y Arduino. De hecho, esta es la plataforma que implementamos con éxito en la parte práctica de nuestra monografía para supervisar la telemetría del sensor LDR y controlar el alumbrado.*
>
> *En contraparte, **ThingsBoard Cloud** representa el siguiente nivel en madurez operativa. Integra un broker MQTT nativo de alto rendimiento con paneles de control sumamente personalizables. Su gran diferencial radica en la gestión integral de activos y dispositivos, además de un motor de reglas visual basado en nodos que permite programar flujos lógicos, transformaciones de datos y alarmas complejas.*
>
> *En resumen: Adafruit IO es nuestra opción ideal para prototipar y validar soluciones de inmediato, mientras que ThingsBoard es la alternativa para escalar hacia proyectos de supervisión profesional."*

### 4. Preguntas típicas del docente y respuestas
- **¿Cuál es la limitación de Adafruit IO en un entorno productivo?**  
  *Respuesta:* Su plan gratuito impone límites de velocidad (30 puntos de datos por minuto) y retención limitada de datos a 30 días, lo que restringe su uso a pruebas, docencia y prototipos.
- **¿Qué diferencia a un "activo" de un "dispositivo" en ThingsBoard?**  
  *Respuesta:* Un dispositivo es el hardware físico que transmite telemetría (ej. un sensor ESP32), mientras que un activo es una entidad lógica del negocio (ej. un edificio, una sala de servidores o una línea de producción) que agrupa múltiples dispositivos.

---

## 📌 DIAPOSITIVA 7: Analítica y Aplicaciones Web (ThingSpeak vs Ubidots)

### 1. ¿De qué trata esta PPT?
Analiza plataformas que no solo transportan mensajes MQTT, sino que aportan **capacidad de cómputo analítico avanzado** o **creación acelerada de aplicaciones comerciales con sistemas de alerta**.

- **ThingSpeak (respaldado por MathWorks)**:
  - *Computación y Procesamiento:* Integración nativa con **MATLAB en la nube**. Permite escribir y ejecutar scripts de MATLAB directamente sobre los canales de telemetría sin instalar software local.
  - *Análisis:* Filtros digitales de señales, eliminación de ruido, análisis espectral, regresiones estadísticas y algoritmos predictivos.
  - *Casos de uso:* Proyectos de investigación científica, tesis universitarias, monitoreo ambiental y modelado matemático continuo.
- **Ubidots (IoT Application Enablement)**:
  - *Desarrollo:* Permite crear aplicaciones web completas para clientes finales (*white-label*) mediante herramientas tipo *drag-and-drop* (arrastrar y soltar) sin necesidad de programar en React o Angular.
  - *Conectividad:* Soporte MQTT optimizado para datos, con formatos JSON sencillos y variables personalizables.
  - *Notificaciones:* Potente módulo de alertas automáticas multicanal (envío de correos electrónicos, SMS, llamadas de voz automatizadas y webhooks) ante umbrales críticos de variables.

### 2. ¿Cómo exponerla? (Estrategia)
- **Tono:** Explicativo, centrado en el valor del dato y el usuario final.
- **Analogía mental clara:** ThingSpeak es para el *científico/investigador que necesita MATLAB*; Ubidots es para el *integrador/empresa que necesita entregar una app lista con alarmas al cliente*.
- **Tiempo meta:** ~1 minuto y 35 segundos.

### 3. Guion para Exponer (Palabra por palabra)
> *"Pasando a la séptima diapositiva, abordamos las plataformas orientadas a la analítica de datos y aplicaciones web: **ThingSpeak** y **Ubidots**.*
>
> ***ThingSpeak**, desarrollada con el respaldo de MathWorks, tiene como factor diferenciador su integración nativa con **MATLAB** en la nube. Esta plataforma no solo recibe lecturas mediante canales MQTT, sino que permite ejecutar código de análisis numérico, filtrado estadístico y modelos predictivos en tiempo real directamente sobre la telemetría. Es la herramienta predilecta en el ámbito académico y de investigación científica, donde procesar matemáticamente los datos es tan importante como recolectarlos.*
>
> *Por su parte, **Ubidots** está categorizada como una plataforma de habilitación de aplicaciones IoT. Su fortaleza radica en transformar flujos de telemetría en aplicaciones web comerciales e intuitivas mediante herramientas de arrastrar y soltar, sin requerir un desarrollo complejo de frontend. Ofrece soporte MQTT optimizado para datos y un sistema nativo de eventos para disparar alertas automáticas por correo electrónico, SMS o webhooks ante cualquier anomalía.*
>
> *En síntesis: seleccionamos ThingSpeak cuando el valor central radica en el análisis matemático profundo con MATLAB, y optamos por Ubidots cuando necesitamos entregar una aplicación web lista y alertas operativas a usuarios finales."*

### 4. Preguntas típicas del docente y respuestas
- **¿Qué ventaja ofrece usar MQTT en ThingSpeak en lugar de peticiones HTTP REST?**  
  *Respuesta:* MQTT mantiene la conexión TCP abierta con encabezados ultra livianos (2 bytes), lo que ahorra ancho de banda y batería en microcontroladores frente a peticiones HTTP continuas.
- **¿Qué es un webhook en las alertas de Ubidots?**  
  *Respuesta:* Es una llamada HTTP POST automática que Ubidots envía a otro servidor o API externa cuando una variable supera un umbral, permitiendo activar actuadores o notificar a sistemas externos como WhatsApp o Telegram.

---

## 📌 DIAPOSITIVA 8: Rendimiento y Autoalojamiento (Flespi vs Mosquitto en VPS)

### 1. ¿De qué trata esta PPT?
Cierra la comparativa analizando dos extremos tecnológicos: por un lado, un broker comercial hiperoptimizado para telemática de alta velocidad (**Flespi**); por el otro, el rey del código abierto y la soberanía total desplegado en un servidor propio (**Eclipse Mosquitto en VPS**).

- **Flespi (Gurtam)**:
  - *Enfoque:* Diseñado específicamente para el sector B2B de **telemática, seguimiento vehicular (GPS) y gestión de flotas**.
  - *Velocidad:* Latencia ultra baja y rendimiento extremo en el despacho de paquetes MQTT.
  - *Arquitectura:* Sistema 100% impulsado por APIs REST con almacenamiento temporal avanzado (*message buffering*), ideal para dispositivos móviles que sufren cortes frecuentes de señal en carretera.
- **Mosquitto en una VPS (Virtual Private Server)**:
  - *Licencia y Autonomía:* Desarrollado bajo la **Fundación Eclipse**, es software libre y de código abierto (Open Source).
  - *Control:* Otorga soberanía absoluta sobre los datos, sin pagar por mensaje ni depender de las cuotas o caídas de un tercero. Permite configurar puertos estándar (1883 TCP, 8883 TLS, 80/443 WebSockets) a medida.
  - *Requisitos y Retos:* No es un servicio gestionado; exige que el usuario configure y mantenga la seguridad: generación de certificados TLS (ej. con Certbot / Let's Encrypt), cortafuegos (`ufw`), listas de control de acceso (ACLs) y parches del sistema operativo Linux.

### 2. ¿Cómo exponerla? (Estrategia)
- **Tono:** Conclusivo, con solidez en arquitectura y decisiones de infraestructura.
- **Cierre del bloque:** Haz un remate claro que resuma los 8 brokers expuestos, destacando que no existe una opción "única y mejor", sino que la elección depende de los requisitos de latencia, presupuesto, capacidad del equipo técnico y privacidad.
- **Tiempo meta:** ~1 minuto y 40 segundos.

### 3. Guion para Exponer (Palabra por palabra)
> *"Llegamos a la octava diapositiva, que cierra la comparativa evaluando dos alternativas de rendimiento extremo y soberanía de infraestructura: **Flespi** frente a **Mosquitto alojado en una VPS**.*
>
> ***Flespi** es una solución especializada en el sector B2B para telemática y flotas vehiculares. Ofrece una latencia ultra baja en el tránsito de mensajes, almacenamiento temporal inteligente que retiene datos si un vehículo pierde señal en ruta, y una arquitectura totalmente orientada a APIs REST. Es un broker comercial de alta ingeniería para escenarios donde la velocidad y la confiabilidad del dato son críticas.*
>
> *En el otro extremo tenemos a **Eclipse Mosquitto** autoalojado en una máquina virtual o VPS. Mosquitto es el estándar de código abierto más popular del mundo. Al desplegarlo en nuestro propio servidor obtenemos autonomía absoluta y soberanía total sobre los datos, sin costos por mensaje ni límites de proveedores. Sin embargo, su desafío es operativo: exige que el equipo técnico administre manualmente la seguridad, configure el cortafuegos y gestione los certificados TLS con herramientas como Let's Encrypt.*
>
> *Con esto completamos el panorama: Flespi cuando requerimos telemetría ultrarrápida como servicio gestionado, y Mosquitto cuando la prioridad es el control total y la privacidad de nuestra propia infraestructura."*

### 4. Preguntas típicas del docente y respuestas
- **¿Qué puertos son obligatorios abrir si desplegamos Mosquitto en una VPS para producción?**  
  *Respuesta:* En entornos públicos no se debe exponer el puerto 1883 sin cifrar. Se debe configurar el puerto **8883 con cifrado TLS** para microcontroladores y, opcionalmente, el **8884 o 443 con WebSockets protegidos (WSS)** para clientes en navegadores web.
- **¿Cuándo preferirías Mosquitto en VPS antes que una solución como AWS IoT Core?**  
  *Respuesta:* Cuando la empresa requiere estricta soberanía y privacidad de datos (por regulaciones de protección de datos), cuando el volumen de mensajes es gigantesco y pagar tarifas por millón de mensajes en la nube resultaría inviable, y cuando se cuenta con personal capacitado en Linux y DevOps para su mantenimiento.

---

## 📊 Matriz Comparativa Rápida (Las 8 Opciones del Bloque)

Usa esta tabla como "chuleta" o referencia rápida si el docente hace preguntas cruzadas entre plataformas:

| Plataforma | Categoría Principal | Protocolo / Seguridad | Mayor Fortaleza | Mayor Desventaja o Reto |
| :--- | :--- | :--- | :--- | :--- |
| **AWS IoT Core** | Plataforma Cloud Integral | MQTT / mTLS X.509 obligatorio | Motor de reglas nativo y ecosistema AWS | Configuración compleja y costos por consumo |
| **Azure IoT Hub** | Plataforma Cloud Integral | MQTT adaptado / X.509 o SAS | Gemelos digitales (Device Twins) y gestión de identidad | Restricciones en tópicos MQTT tradicionales |
| **Adafruit IO** | Prototipado y Dashboards | MQTT / Llave API (AIO Key) | Rápida visualización y amigable con ESP32 *(Usado en nuestra práctica)* | Límites de mensajes por minuto en plan gratuito |
| **ThingsBoard** | Plataforma IoT Avanzada | MQTT nativo / Tokens y X.509 | Gestión de activos/dispositivos y Rule Engine visual | Requiere mayor aprendizaje para flujos avanzados |
| **ThingSpeak** | Analítica y Cálculo | MQTT / Canales con API Key | Integración nativa con MATLAB en la nube | Frecuencia de actualización limitada en cuentas gratis |
| **Ubidots** | Habilitación de Apps Web | MQTT / Tokens de dispositivo | Apps web comerciales drag-and-drop y alertas SMS/Email | Opciones avanzadas de personalización bajo planes de pago |
| **Flespi** | Alta Latencia Telemática | MQTT hiperoptimizado / Tokens | Latencia ultra baja y buffer para flotas/vehículos | Específico para B2B y requerimientos telemáticos |
| **Mosquitto (VPS)** | Autoalojado Open Source | MQTT 3.1.1 / 5 con TLS configurable | Control total, soberanía de datos y cero costos por mensaje | Mantenimiento, seguridad y parches a cargo del usuario |

---

## 🎯 Consejos Finales para la Exposición Oral

1. **Control de Tiempo:** Cada diapositiva tiene entre 170 y 215 palabras. A un ritmo pausado y claro (130 palabras por minuto), tardarás entre **1:20 y 1:40 minutos por diapositiva**, dejándote margen de sobra bajo el límite de los 2 minutos.
2. **Postura y Señalización:** En cada diapositiva hay dos bloques visuales (izquierda vs derecha). Señala con la mano o el cursor: *"A la izquierda vemos la solución de X... mientras que a la derecha tenemos a Y..."*.
3. **Escucha los Audios:** Reproduce los audios generados (`audio_ppt5...mp3` a `audio_ppt8...mp3`) 2 o 3 veces con audífonos. Repite mentalmente o en voz alta para interiorizar el ritmo, la modulación y las palabras técnicas clave (*mTLS, X.509, Device Twins, Rule Engine, Telemetría, VPS*).

