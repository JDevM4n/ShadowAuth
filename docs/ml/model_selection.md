# ShadowAuth - Machine Learning Model Selection

## 1. Objetivo

Definir los algoritmos de Machine Learning que serán utilizados por
ShadowAuth para analizar sesiones normalizadas y detectar comportamientos
potencialmente maliciosos.

La selección contempla modelos supervisados y no supervisados debido a que
el sistema contiene tanto sesiones con ground truth conocido como sesiones
reales provenientes del honeypot que todavía no han sido etiquetadas.

---

## 2. Características del dataset

ShadowAuth genera un FeatureVector por sesión.

Entre las características disponibles se encuentran:

- duration_seconds
- command_count
- unique_command_count
- login_attempts
- successful_login
- download_count
- source_port
- destination_port
- process_count
- shell_spawned
- sensitive_file_access
- max_severity
- average_severity
- session_hour
- weekend

Las siguientes columnas son consideradas metadatos y no forman parte
directamente del entrenamiento supervisado:

- session_id
- source_ip
- destination_ip
- protocol
- label

---

## 3. Algoritmos seleccionados

### 3.1 Random Forest

Tipo:

Supervisado.

Rol:

Modelo baseline principal para clasificación binaria.

Clases:

- benign
- attack

Motivos de selección:

- Compatible con datos tabulares.
- Permite modelar relaciones no lineales.
- Requiere poco preprocesamiento.
- Permite obtener importancia de características.
- Es apropiado como modelo baseline.
- Puede integrarse posteriormente al pipeline de inferencia de ShadowAuth.

Random Forest será el primer modelo supervisado implementado y evaluado.

---

### 3.2 XGBoost

Tipo:

Supervisado.

Rol:

Modelo comparativo frente a Random Forest.

Clases:

- benign
- attack

Motivos de selección:

- Buen desempeño en problemas de clasificación con datos tabulares.
- Capacidad para modelar interacciones complejas entre características.
- Permite ajuste de hiperparámetros.
- Permite comparar un enfoque de boosting con el enfoque bagging de
  Random Forest.

Su entrenamiento definitivo dependerá de disponer de un volumen mayor de
sesiones etiquetadas.

---

### 3.3 Isolation Forest

Tipo:

No supervisado.

Rol:

Detección de anomalías.

Motivos de selección:

- No requiere etiquetas de clase para identificar observaciones anómalas.
- Permite aprovechar sesiones unlabeled recopiladas por Cowrie.
- Es compatible con características numéricas tabulares.
- Puede generar un anomaly score por sesión.
- Complementa los modelos supervisados.

Isolation Forest no sustituye la clasificación benign/attack. Su salida será
utilizada como señal adicional de anomalía.

---

## 4. Estrategia de modelos

La estrategia inicial de ShadowAuth será:

1. Random Forest como baseline supervisado.
2. XGBoost como modelo supervisado comparativo.
3. Isolation Forest como mecanismo complementario de detección de anomalías.

Los modelos supervisados serán entrenados únicamente con sesiones que tengan
ground truth conocido.

Las sesiones unlabeled no serán convertidas automáticamente en attack o
benign.

---

## 5. Dataset de entrenamiento

El sistema mantiene dos conjuntos de datos:

### Master dataset

Contiene:

- attack
- benign
- unlabeled

### Training dataset

Contiene únicamente:

- attack
- benign

El training dataset será utilizado para Random Forest y XGBoost.

Isolation Forest podrá utilizar un conjunto de datos no supervisado preparado
a partir de sesiones disponibles, bajo una estrategia específica que será
definida durante la implementación y evaluación del modelo.

---

## 6. Evaluación futura

Los modelos supervisados serán comparados utilizando métricas como:

- Precision
- Recall
- F1-score
- Confusion Matrix
- ROC-AUC, cuando el volumen y distribución de los datos permitan una
  evaluación adecuada.

En un sistema de detección de amenazas se prestará especial atención al recall
de la clase attack y a la tasa de falsos positivos.

---

## 7. Estado actual

La infraestructura para generación del dataset está implementada.

Actualmente existen sesiones con etiquetas attack y benign suficientes para
validar técnicamente el pipeline, pero todavía no existe un volumen suficiente
para considerar definitivo el entrenamiento o la evaluación de los modelos.

La recopilación y etiquetado de nuevas sesiones continuará en paralelo al
desarrollo del módulo de Machine Learning.

---

## 8. Decisión

Algoritmos seleccionados para ShadowAuth ML v1:

- Random Forest: baseline supervisado principal.
- XGBoost: modelo supervisado comparativo.
- Isolation Forest: detección complementaria de anomalías.
