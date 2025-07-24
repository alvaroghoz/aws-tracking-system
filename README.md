# 📡 Sistema de Tracking WiFi con AWS

Este proyecto implementa una arquitectura serverless para capturar eventos de dispositivos móviles detectados mediante red Wi-Fi (por ejemplo, a través del sistema Aruba Central), y generar reportes diarios de permanencia por zonas.

---

## 🧱 Arquitectura utilizada

- **Amazon SQS** – Para desacoplar la recepción de eventos
- **AWS Lambda** – Para procesar eventos (`procesar_evento`) y generar reportes (`generar_reporte`)
- **Amazon S3** – Almacenamiento de eventos (`raw/`) y reportes (`reports/`)
- **Amazon DynamoDB** – Base de datos para seguimiento de presencia actual
- **Amazon EventBridge** – Para programar la ejecución diaria del reporte
- **Amazon CloudWatch** – Logs y monitoreo

---

## 📁 Estructura del repositorio

```
tracking-system/
├── lambdas/
│   ├── procesar_evento.py
│   └── generar_reporte.py
├── deploy/
│   └── guia_despliegue_tracking.pdf
├── docs/
│   ├── trackingsystem.drawio.pdf.png
│   ├── buenas-practicas aplicadas.pdf
│   ├── demostracion.pdf
│   └── justificacion-diseno.pdf
├── evento-ejemplo/
│   └── evento.json
├── .zip/
│   ├── lambda-procesar.zip
│   └── lambda-reporte.zip
├── README.md

```

---

## 🚀 Cómo desplegar

Consulta el archivo [`guia_despliegue_tracking.docx`](deploy/guia_despliegue_tracking.docx) para seguir el paso a paso de despliegue de la arquitectura completa.

---

## ✅ Cómo probar

1. Envía el archivo `evento.json` a la cola `dispositivos-detectados` en SQS.
2. Verifica que:
   - Se genera un objeto JSON en S3 (`raw/`)
   - Se actualiza un registro en DynamoDB
   - Se crean logs en CloudWatch
3. Ejecuta manualmente la Lambda `generar_reporte` (o espera a la regla diaria).
4. Verifica la creación del archivo en `reports/`.

---

## 📄 Documentación

- **Diagrama de arquitectura**: `docs/diagrama-arquitectura.png`
- **Justificación técnica**: `docs/justificacion-diseno.md`
- **Buenas prácticas aplicadas**: `docs/buenas-practicas.md`
- **Demostración visual**: `docs/demostracion.pdf`
- **Guía técnica**: `deploy/guia_despliegue_tracking.docx`

---

## 🧠 Autor

Álvaro García-Hoz  
Fecha de entrega: 2025-07-24

