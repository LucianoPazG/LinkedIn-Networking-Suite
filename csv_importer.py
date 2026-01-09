#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Importador de CSV de LinkedIn para Networking Suite
Importa contactos desde el exportador oficial de LinkedIn
"""

import os
import csv
import re
from typing import List, Dict, Optional
import logging

from database import ContactDatabase

logger = logging.getLogger(__name__)


class LinkedInCSVImporter:
    """Importa contactos desde el exportador oficial de LinkedIn"""

    def __init__(self, db: ContactDatabase):
        """
        Inicializa el importador

        Args:
            db: Instancia de ContactDatabase
        """
        self.db = db

    def import_from_csv(self, csv_file_path: str,
                       dry_run: bool = False) -> Dict[str, int]:
        """
        Importa contactos desde un archivo CSV exportado de LinkedIn

        Args:
            csv_file_path: Ruta al archivo CSV
            dry_run: Si es True, solo muestra qué haría sin importar

        Returns:
            Diccionario con estadísticas de importación
        """
        if not os.path.exists(csv_file_path):
            logger.error(f"Archivo no encontrado: {csv_file_path}")
            return {
                'success': False,
                'error': 'Archivo no encontrado',
                'total': 0,
                'imported': 0,
                'skipped': 0,
                'errors': 0
            }

        stats = {
            'success': True,
            'total': 0,
            'imported': 0,
            'skipped': 0,
            'errors': 0,
            'contacts': []
        }

        try:
            with open(csv_file_path, 'r', encoding='utf-8-sig') as f:
                # Detectar el formato del CSV
                sample = f.read(1024)
                f.seek(0)

                # Intentar diferentes dialectos
                dialect = None
                for delimiter in [',', ';', '\t']:
                    try:
                        sample_lines = sample.split('\n')[:5]
                        reader = csv.DictReader(sample_lines, delimiter=delimiter)
                        if len(list(reader)) > 0:
                            dialect = delimiter
                            break
                    except:
                        continue

                if not dialect:
                    dialect = ','

                # Leer archivo completo para procesar líneas de notes
                lines = f.readlines()

                # Encontrar dónde empiezan los datos reales (línea que contiene "First Name")
                data_start_line = 0
                for i, line in enumerate(lines):
                    if 'First Name' in line or 'LastName' in line or 'Last Name' in line:
                        data_start_line = i
                        break

                logger.info(f"Datos reales encontrados en línea {data_start_line + 1}")

                # Crear reader solo desde los datos reales
                csv_data = ''.join(lines[data_start_line:])
                reader = csv.DictReader(csv_data.splitlines(), delimiter=dialect)

                # Detectar columnas
                fieldnames = reader.fieldnames or []
                logger.info(f"Columnas detectadas: {fieldnames}")

                for row in reader:
                    stats['total'] += 1

                    try:
                        # Mapear campos del CSV a nuestros campos
                        contact = self._map_csv_fields(row, fieldnames)

                        if not contact or not contact.get('linkedin_url'):
                            stats['skipped'] += 1
                            logger.warning(f"Fila {stats['total']}: URL de LinkedIn no encontrada")
                            continue

                        if dry_run:
                            stats['contacts'].append(contact)
                            stats['imported'] += 1
                            print(f"✅ Se importaría: {contact.get('name', 'N/A')}")
                        else:
                            # Verificar si ya existe
                            existing = self.db.get_contact_by_url(contact['linkedin_url'])

                            if existing:
                                stats['skipped'] += 1
                                logger.info(f"Contacto ya existe: {contact.get('name', 'N/A')}")
                            else:
                                # Importar contacto
                                contact_id = self.db.add_contact(contact)

                                if contact_id:
                                    stats['imported'] += 1
                                    stats['contacts'].append(contact)
                                    print(f"✅ Importado: {contact.get('name', 'N/A')}")
                                else:
                                    stats['errors'] += 1
                                    print(f"❌ Error importando: {contact.get('name', 'N/A')}")

                    except Exception as e:
                        stats['errors'] += 1
                        logger.error(f"Error procesando fila {stats['total']}: {e}")
                        continue

            print(f"\n📊 RESUMEN:")
            print(f"   Total de filas: {stats['total']}")
            print(f"   Importados: {stats['imported']}")
            print(f"   Omitidos (ya existían): {stats['skipped']}")
            print(f"   Errores: {stats['errors']}")

            return stats

        except Exception as e:
            logger.error(f"Error leyendo archivo CSV: {e}")
            stats['success'] = False
            stats['error'] = str(e)
            return stats

    def _map_csv_fields(self, row: Dict, fieldnames: List[str]) -> Optional[Dict]:
        """
        Mapea los campos del CSV de LinkedIn a nuestro formato

        Args:
            row: Fila del CSV
            fieldnames: Nombres de columnas

        Returns:
            Diccionario con el contacto mapeado o None
        """
        contact = {}

        # Buscar campos en diferentes idiomas/formatos
        field_mapping = {
            # URL de LinkedIn (varios formatos posibles)
            'linkedin_url': [
                'URL',
                'LinkedIn URL',
                'LinkedIn',
                'Url',
                'Profile URL',
                'Profile Url',
                'Enlace',
                'Link',
                'url'
            ],
            # Nombre
            'name': [
                'First Name',
                'FirstName',
                'Nombre',
                'GivenName',
                'First'
            ],
            # Apellido
            'last_name': [
                'Last Name',
                'LastName',
                'Apellido',
                'FamilyName',
                'Surname',
                'Last'
            ],
            # Email
            'email': [
                'Email Address',
                'Email',
                'E-mail',
                'Correo',
                'Mail'
            ],
            # Empresa
            'company': [
                'Company',
                'Empresa',
                'Position Company',
                'Organization'
            ],
            # Cargo
            'job_title': [
                'Position',
                'Job Title',
                'Title',
                'Cargo',
                'Role',
                'Puesto'
            ],
            # Ubicación
            'location': [
                'Location',
                'Ubicación',
                'City',
                'Ciudad'
            ]
        }

        # Función auxiliar para buscar campo
        def find_field(mapping_key: str) -> Optional[str]:
            possible_names = field_mapping.get(mapping_key, [])

            for possible_name in possible_names:
                # Búsqueda exacta
                if possible_name in fieldnames:
                    value = row.get(possible_name, '').strip()
                    if value:
                        return value

                # Búsqueda case-insensitive
                for fieldname in fieldnames:
                    if possible_name.lower() in fieldname.lower():
                        value = row.get(fieldname, '').strip()
                        if value:
                            return value

            return None

        # Extraer URL de LinkedIn
        linkedin_url = find_field('linkedin_url')

        if not linkedin_url:
            # Intentar extraer URL de otros campos
            for fieldname in fieldnames:
                value = str(row.get(fieldname, '')).strip()
                if 'linkedin.com/in/' in value.lower():
                    linkedin_url = value
                    break

        if not linkedin_url:
            return None

        contact['linkedin_url'] = linkedin_url

        # Extraer nombre y apellido
        first_name = find_field('name') or ''
        last_name = find_field('last_name') or ''

        if first_name and last_name:
            contact['name'] = f"{first_name} {last_name}"
        elif first_name:
            contact['name'] = first_name
        else:
            # Intentar extraer de un campo de nombre completo
            for fieldname in fieldnames:
                value = row.get(fieldname, '').strip()
                if value and len(value.split()) >= 2 and 'name' in fieldname.lower():
                    contact['name'] = value
                    break

            if 'name' not in contact:
                # Usar parte del URL como nombre
                match = re.search(r'/in/([^/]+)', linkedin_url)
                if match:
                    contact['name'] = match.group(1).replace('-', ' ').title()
                else:
                    contact['name'] = 'Contacto sin nombre'

        # Extraer otros campos
        contact['company'] = find_field('company') or None
        contact['job_title'] = find_field('job_title') or None
        contact['location'] = find_field('location') or None

        # Agregar notas con información adicional
        notes = []
        email = find_field('email')
        if email:
            notes.append(f"Email: {email}")

        if notes:
            contact['notes'] = ' | '.join(notes)

        # Marcar como connected por defecto (ya son conexiones)
        contact['status'] = 'connected'
        contact['connection_message_sent'] = 1

        return contact

    def show_import_preview(self, csv_file_path: str, max_contacts: int = 10) -> None:
        """
        Muestra una vista previa de los contactos que se importarían

        Args:
            csv_file_path: Ruta al archivo CSV
            max_contacts: Máximo de contactos a mostrar
        """
        print("\n" + "="*70)
        print("📋 VISTA PREVIA DE IMPORTACIÓN")
        print("="*70)

        stats = self.import_from_csv(csv_file_path, dry_run=True)

        if not stats.get('success'):
            print(f"\n❌ Error: {stats.get('error', 'Desconocido')}")
            return

        print(f"\n✅ Se importarían {stats['imported']} contactos")
        print(f"\n📝 Primeros {min(max_contacts, stats['imported'])} contactos:\n")

        for i, contact in enumerate(stats['contacts'][:max_contacts], 1):
            print(f"{i}. {contact.get('name', 'N/A')}")
            print(f"   🏢 {contact.get('company', 'N/A')} - {contact.get('job_title', 'N/A')}")
            print(f"   🔗 {contact.get('linkedin_url', 'N/A')}")
            print("-" * 70)


def export_linkedin_connections_guide():
    """Muestra instrucciones para exportar conexiones de LinkedIn"""

    guide = """
╔════════════════════════════════════════════════════════════════════╗
║         📥 CÓMO EXPORTAR TUS CONEXIONES DE LINKEDIN              ║
╚════════════════════════════════════════════════════════════════════╝

🔷 MÉTODO OFICIAL (Recomendado):

1. Inicia sesión en LinkedIn
2. Ve a tu foto de perfil (arriba a la derecha)
3. Selecciona "Configuración y privacidad"
4. En la pestaña "Datos", busca "Obtener una copia de tus datos"
5. Selecciona "Conexiones" o "Want a copy of your data"
6. Elige "Conexiones" (Connections)
7. Solicita el archivo
8. Espera el email (puede tardar minutos u horas)
9. Descarga el archivo ZIP
10. Extrae el archivo CSV de conexiones

🔷 FORMATOS DE ARCHIVO ESPERADOS:

LinkedIn exporta diferentes formatos según el idioma y fecha.
El importador detecta automáticamente:
- Delimitadores: coma (,), punto y coma (;), tabulación
- Encabezados en diferentes idiomas
- Diferentes nombres de columnas

🔷 DESPUÉS DE EXPORTAR:

1. Coloca el archivo CSV en la carpeta de la suite
2. Ejecuta la opción de importación en el menú
3. Selecciona el archivo CSV
4. Confirma la importación

✅ VENTAJAS:

- 100% legal (método oficial de LinkedIn)
- Todas tus conexiones en segundos
- Incluye nombre, empresa, cargo, email
- No viola términos de servicio

⚠️ NOTAS:

- LinkedIn puede tardar hasta 24h en enviar el archivo
- El formato puede variar según tu región
- Solo incluye conexiones que aceptaron
- Algunos campos pueden estar vacíos

╚════════════════════════════════════════════════════════════════════╝
"""

    print(guide)


if __name__ == "__main__":
    import sys

    print(export_linkedin_connections_guide())

    if len(sys.argv) > 1:
        csv_file = sys.argv[1]

        print(f"\n📂 Procesando archivo: {csv_file}\n")

        db = ContactDatabase()
        importer = LinkedInCSVImporter(db)

        # Mostrar preview
        importer.show_import_preview(csv_file)

        # Importar
        confirm = input("\n¿Deseas importar estos contactos? (s/n): ").strip().lower()

        if confirm == 's':
            stats = importer.import_from_csv(csv_file)

            if stats.get('success'):
                print(f"\n✅ Importación completada: {stats['imported']} contactos")
            else:
                print(f"\n❌ Error en la importación")
