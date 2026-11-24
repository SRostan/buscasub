# 🔬 BuscaSUB - Sistema de Consulta de Socios y Directorio de Seccionales

Aplicación web institucional desarrollada para la **Sociedad Uruguaya de Biociencias (SUB)**, lista para publicar y ejecutarse de forma 100% autónoma en **GitHub Pages**.

---

## 🚀 Módulos y Funcionalidades

### 1. 🔍 Consulta Individual de Estado de Socio (`index.html`)
Página de acceso público para socios e investigadores de la SUB:
* **Entrada:** Campo de búsqueda por número de Cédula de Identidad (8 dígitos, con validación y limpieza automática de puntos y guiones).
* **Privacidad Estricta:** No muestra en ningún momento el nombre ni el correo del investigador, protegiendo su identidad y exhibiendo únicamente su situación asociativa e institucional.
* **Datos consultados:**
  * **Estado de Actividad SUB:** Indicador visual (*Activo* en verde, *Inactivo* en rojo, *Activo - pendiente de pago* en ámbar).
  * **Nivel Académico:** Nivel I, II o III.
  * **Afiliación Institucional:** Institución o facultad de pertenencia.
  * **Año de Ingreso:** Período de ingreso a la SUB.
  * **Seccionales Adscritas:** Clasificación por orden de preferencia (Principal, Secundaria y Terciaria).
  * **Historial de Cuotas (2021 a 2026):** Visualización interactiva con badges de color (*Verde = Sí pagó*, *Rojo = No pagó*, *Gris = No corresponde*).
  * **Movimiento de Pago:** Registro transparente de pagos 2026 reasignados para saldar deudas de años anteriores (2024 o 2025).
  * **Estado de Cuota 2026:** Situación específica respecto al año en curso.

---

### 2. 🔬 Directorio de Seccionales Científicas (`seccionales.html`)
Módulo interno diseñado para directivos de la SUB y coordinadores de seccionales:
* **Selector de Seccionales Oficiales:**
  * `ATGC-U` - Terapia Génica y Celular
  * `CODEUy` - Ecología
  * `LimnoUy` - Limnología
  * `SBBM` - Bioquímica y Biología Molecular
  * `SBF` - Biofísica
  * `SIB/NIB` - Ingeniería Biomédica
  * `SNU` - Neurociencias
  * `SUBI` - Bioinformática
  * `SUG` - Genética
  * `SUMI` - Microscopía e Imagenología
* **Panel de KPIs en Tiempo Real:**
  * Total de investigadores adscritos en la seccional seleccionada.
  * Socios Activos, Inactivos y Pendientes de Pago (con porcentajes automáticos).
  * Desglose por Nivel Académico (Niveles I, II y III).
* **Padrón Detallado:**
  * Tabla completa con N°, Nombre Completo, Cédula, Nivel, Afiliación, Correo, Año de Ingreso, Preferencia, Estado de Actividad, Movimiento de Pago y Estado de Cuota 2026.
  * **Filtro de búsqueda en vivo:** Búsqueda instantánea y responsiva por cualquier término.
  * **Exportación CSV:** Descarga del padrón filtrado para gestión interna.

---

## 🎨 Diseño y Paleta Institucional
* **Azul Marino Principal:** `#0F274A`
* **Azul Medio:** `#1D477C`
* **Fondos Suaves:** `#F4F7FB`
* **Tarjetas Ejecutivas:** Diseño limpio, sombras sutiles y bordes redondeados.
* **100% Responsive:** Adaptado para teléfonos móviles, tablets y computadoras de escritorio.

---

## 📦 Estructura del Proyecto
```text
BuscaSUB/
├── index.html               # Aplicación pública: Consulta individual por cédula
├── seccionales.html         # Aplicación interna: Directorio y KPIs por seccional
├── css/
│   └── styles.css           # Estilos institucionales y diseño responsive
├── data/
│   ├── socios_publico.js    # Base pública (cédula, estado, cuotas - SIN nombres)
│   ├── socios_publico.json  # Copia JSON del dataset público
│   ├── seccionales_data.js  # Directorio para seccionales con padrón completo
│   └── seccionales_data.json# Copia JSON del padrón de seccionales
├── build_datasets.py        # Script para regenerar datos desde el Excel maestro
├── .gitignore
└── README.md
```

---
© **Sociedad Uruguaya de Biociencias (SUB)** • Montevideo, Uruguay
