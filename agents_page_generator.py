import os
import uuid
import qrcode
import pandas as pd

csv_file = 'agents.csv'
agents_data = pd.read_csv(csv_file)

agents_data['Cellphone'] = agents_data['Cellphone'].astype(str)

qr_directory = os.path.join('static', 'qr_codes')
os.makedirs(qr_directory, exist_ok=True)

def format_cellphone(cellphone):
    cellphone = str(cellphone).strip()

    # Eliminar prefijo de país si existe
    if cellphone.startswith('+52'):
        cellphone = cellphone[3:]
    elif cellphone.startswith('52'):
        cellphone = cellphone[2:]

    # Conservar solo dígitos
    cellphone = ''.join(filter(str.isdigit, cellphone))

    # Rellenar con ceros a la izquierda si tiene menos de 10 dígitos
    if len(cellphone) < 10:
        cellphone = cellphone.zfill(10)

    # Formatear en el formato XX XXXX XXXX (10 dígitos)
    formatted = f"{cellphone[:2]} {cellphone[2:6]} {cellphone[6:10]}"

    return formatted

total_agents = len(agents_data)

html_output = """
{% extends "base_template.html" %}
{% block title %}Agentes - Fuerza Inmobiliaria de Occidente{% endblock %}

{% block content %}
<!-- Header de Agentes -->
<header class="hero-section text-white text-center py-5">
    <div class="container">
        <h1 class="display-4 fw-bold">Nuestros Agentes</h1>
        <p class="lead mt-3">Conoce a nuestro equipo de expertos listos para ayudarte.</p>
    </div>
</header>

<main class="py-5">
    <div class="container">
        <div id="agentsCarousel" class="carousel slide" data-bs-ride="carousel">
            <div class="carousel-inner">
"""

for i in range(0, total_agents, 6):
    group = agents_data.iloc[i:i+6]
    active_class = "active" if i == 0 else ""
    html_output += f'<div class="carousel-item {active_class}"><div class="row g-4">'

    for _, row in group.iterrows():
        name = row['Name']
        cellphone = row['Cellphone']
        first_name = name.split()[0]

        formatted_cellphone = format_cellphone(cellphone)

        whatsapp_url = f"https://wa.me/{cellphone}?text=Hola%20{first_name},%20te%20contacto%20desde%20la%20p%C3%A1gina%20web%20de%20FIDO%20ya%20que%20requiero%20de%20tus%20servicios."

        # Generar un nombre único para el QR para evitar sobrescribir
        qr_code_filename = f"{first_name}_{uuid.uuid4().hex[:6]}.png"
        qr_code_path = os.path.join(qr_directory, qr_code_filename)
        qr_code_url = f"{{{{ url_for('static', filename='qr_codes/{qr_code_filename}') }}}}"

        # Generar el código QR si no existe
        if not os.path.exists(qr_code_path):
            qr = qrcode.make(whatsapp_url)
            qr.save(qr_code_path)

        html_output += f"""
                <div class="col-md-4">
                    <div class="card agent-card shadow h-100">
                        <div class="card-body text-center">
                            <h5 class="card-title">{name}</h5>
                            <p class="card-text">Teléfono: {formatted_cellphone}</p>
                            <img src="{qr_code_url}" alt="QR WhatsApp" class="qr-code mb-3">
                            <p class="mt-2">Escanea este QR para mandar mensaje directo al agente en WhatsApp</p>
                            <a href="tel:+{cellphone}" class="btn btn-primary mt-3">
                                <i class="bi bi-telephone-fill"></i> Llamar
                            </a>
                            <a href="{whatsapp_url}" target="_blank" class="btn btn-success mt-3">
                                <i class="bi bi-whatsapp"></i> WhatsApp
                            </a>
                        </div>
                    </div>
                </div>
        """

    html_output += "</div></div>"

html_output += """
            </div>
"""

if total_agents > 6:
    html_output += """
            <button class="carousel-control-prev" type="button" data-bs-target="#agentsCarousel" data-bs-slide="prev">
                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Anterior</span>
            </button>
            <button class="carousel-control-next" type="button" data-bs-target="#agentsCarousel" data-bs-slide="next">
                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Siguiente</span>
            </button>
    """

html_output += """
        </div>
    </div>
</main>
{% endblock %}
"""

with open("templates/agents.html", "w", encoding="utf-8") as file:
    file.write(html_output)

print("Página de Agentes generada exitosamente y compatible con base_template.html.")
