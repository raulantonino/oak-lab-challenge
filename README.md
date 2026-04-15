# Oak Lab Challenge — Sistema de Agendamiento del Laboratorio del Profesor Oak

Proyecto desarrollado en **Django** para resolver el challenge técnico del **Sistema de Agendamiento: Laboratorio del Profesor Oak**.

La aplicación permite que un entrenador:

- se registre e inicie sesión
- elija una criatura inicial
- seleccione un horario disponible
- confirme su reserva
- revise su reserva en cualquier momento
- cancele su reserva si lo necesita

Además, el **Profesor Oak** puede administrar criaturas, horarios y reservas desde el **panel de administración de Django**.

---

## Características principales

### Flujo del entrenador
- Registro de usuario
- Inicio y cierre de sesión
- Selección de criatura inicial
- Selección de horario disponible
- Confirmación de reserva
- Pantalla de éxito con diseño temático
- Vista **Mi Reserva**
- Cancelación de reserva

### Panel administrativo
- Gestión de criaturas
- Gestión de horarios disponibles
- Visualización de reservas
- Orden y filtros en el admin para facilitar la gestión

---

## Reglas de negocio implementadas

- Un usuario solo puede tener **una reserva activa**
- Solo se muestran criaturas disponibles
- Solo se muestran horarios activos con cupo disponible
- Un horario no puede superar su cupo máximo
- Al cancelar una reserva, el cupo vuelve a quedar disponible automáticamente
- El logout se realiza mediante **POST**, siguiendo el comportamiento esperado de Django

---

## Stack utilizado

- Python 3.12+
- Django 6
- SQLite3
- HTML + Django Templates
- CSS personalizado
- `python-decouple` para variables de entorno

---

## Estructura general del proyecto

```text
oak_lab/
├── booking/
├── config/
├── docs/
├── static/
├── templates/
├── manage.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## Modelos principales

### `Creature`
Representa una criatura inicial disponible para los entrenadores.

Campos principales:
- `name`
- `element_type`
- `description`
- `emoji`
- `is_available`

### `TimeSlot`
Representa un bloque horario configurable por el Profesor Oak.

Campos principales:
- `weekday`
- `start_time`
- `end_time`
- `max_capacity`
- `is_active`

### `Reservation`
Relaciona a un entrenador con una criatura y un horario.

Campos principales:
- `trainer`
- `creature`
- `time_slot`
- `created_at`

---

## Configuración local

### 1. Clonar el repositorio

```bash
git clone https://github.com/raulantonino/oak-lab-challenge.git
cd oak-lab-challenge
```

### 2. Crear y activar entorno virtual

#### Windows PowerShell
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### Linux / macOS
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Crear archivo `.env`

Crea un archivo `.env` en la raíz del proyecto con este contenido base:

```env
SECRET_KEY=tu_clave_secreta
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

También puedes usar `.env.example` como referencia.

### 5. Aplicar migraciones

```bash
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. Levantar servidor local

```bash
python manage.py runserver
```

La aplicación estará disponible en:

```text
http://127.0.0.1:8000/
```

Y el admin en:

```text
http://127.0.0.1:8000/admin/
```

---

## Datos base recomendados para probar el challenge

### Criaturas
- Charmander — Fuego — 🔥
- Bulbasaur — Planta — 🌿
- Squirtle — Agua — 💧

### Horarios sugeridos
- Lunes 10:00 - 10:30
- Lunes 14:00 - 14:30
- Martes 09:00 - 09:30
- Miércoles 11:00 - 11:30
- Jueves 16:00 - 16:30
- Viernes 12:00 - 12:30

---

## Flujo funcional esperado

1. El usuario se registra o inicia sesión
2. Selecciona una criatura disponible
3. Selecciona un horario con cupo disponible
4. Revisa el resumen y confirma la reserva
5. Se crea la reserva en base de datos
6. El usuario puede revisar su reserva en **Mi Reserva**
7. El usuario puede cancelar la reserva si lo desea

---

## Consideraciones técnicas relevantes

- Se utiliza **sesión** para guardar temporalmente la criatura y el horario seleccionados antes de confirmar
- La vista **Mi Reserva** usa `select_related("creature", "time_slot")`
- La creación de reservas se protege con validaciones de servidor
- La confirmación usa transacción para reducir inconsistencias en escenarios de concurrencia
- Los horarios disponibles se calculan dinámicamente según reservas existentes
- La cancelación libera el cupo automáticamente al eliminar la reserva

---

## Vistas principales

- `/signup/`
- `/login/`
- `/choose-creature/`
- `/choose-time-slot/`
- `/confirm-reservation/`
- `/reservation-success/`
- `/my-reservation/`
- `/admin/`


---

## Autor

Desarrollado por **Raúl Antonino Ortega Huenuil**.
