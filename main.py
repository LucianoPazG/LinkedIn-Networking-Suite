#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Networking Suite - Aplicación Principal
Suite completa para networking con recruiters en LinkedIn
"""

import sys
import os
import logging
from datetime import datetime

# Forzar UTF-8 en salida estándar (Windows)
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from database import ContactDatabase
from message_generator import MessageGenerator
from reminder_system import ReminderSystem
from export_manager import ExportManager
from csv_importer import LinkedInCSVImporter, export_linkedin_connections_guide


# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('networking_suite.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class LinkedInNetworkingSuite:
    """Aplicación principal de la suite"""

    def __init__(self):
        """Inicializa la aplicación"""
        self.db = ContactDatabase()
        self.msg_generator = MessageGenerator()
        self.reminder_system = ReminderSystem(self.db)
        self.export_manager = ExportManager(self.db)
        self.csv_importer = LinkedInCSVImporter(self.db)

    def clear_screen(self):
        """Limpia la pantalla"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_main_menu(self):
        """Muestra el menú principal"""
        menu = """
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║           🤝 LINKEDIN NETWORKING SUITE 🤝                          ║
║                                                                    ║
║           Suite completa para networking con recruiters             ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝

📋 MENÚ PRINCIPAL:

1. 👥 GESTIÓN DE CONTACTOS
2. 💬 GENERADOR DE MENSAJES
3. ⏰ RECORDATORIOS Y FOLLOW-UP
4. 📊 EXPORTAR DATOS
5. 📈 ESTADÍSTICAS
6. 📥 IMPORTAR DESDE LINKEDIN (CSV)
7. ⚙️  CONFIGURACIÓN
0. 🚪 SALIR

"""

        print(menu)

    def menu_contacts(self):
        """Menú de gestión de contactos"""
        while True:
            self.clear_screen()
            print("""
╔════════════════════════════════════════════════════════════════════╗
║                  👥 GESTIÓN DE CONTACTOS                           ║
╚════════════════════════════════════════════════════════════════════╝

1. ➕ Agregar nuevo contacto
2. 📝 Ver todos los contactos
3. 🔍 Buscar contacto
4. ✏️  Editar contacto
5. 🗑️  Eliminar contacto
6. 📋 Ver detalles de contacto
7. 🏷️  Filtrar por estado
0. ⬅️  Volver

""")
            option = input("Selecciona una opción: ").strip()

            if option == '1':
                self.add_new_contact()
            elif option == '2':
                self.view_all_contacts()
            elif option == '3':
                self.search_contact()
            elif option == '4':
                self.edit_contact()
            elif option == '5':
                self.delete_contact()
            elif option == '6':
                self.view_contact_details()
            elif option == '7':
                self.filter_by_status()
            elif option == '0':
                break
            else:
                print("❌ Opción no válida")
                input("Presiona Enter para continuar...")

    def menu_messages(self):
        """Menú de generador de mensajes"""
        while True:
            self.clear_screen()
            print("""
╔════════════════════════════════════════════════════════════════════╗
║                  💬 GENERADOR DE MENSAJES                          ║
╚════════════════════════════════════════════════════════════════════╝

1. 📨 Generar mensaje de conexión
2. 🔄 Generar mensaje de follow-up
3. 🙏 Generar mensaje de agradecimiento
4. 👁️  Previsualizar mensaje
5. 📋 Ver templates disponibles
0. ⬅️  Volver

""")
            option = input("Selecciona una opción: ").strip()

            if option == '1':
                self.generate_connection_message()
            elif option == '2':
                self.generate_followup_message()
            elif option == '3':
                self.generate_thankyou_message()
            elif option == '4':
                self.preview_message()
            elif option == '5':
                self.view_templates()
            elif option == '0':
                break
            else:
                print("❌ Opción no válida")
                input("Presiona Enter para continuar...")

    def menu_reminders(self):
        """Menú de recordatorios"""
        while True:
            self.clear_screen()
            print("""
╔════════════════════════════════════════════════════════════════════╗
║               ⏰ RECORDATORIOS Y FOLLOW-UP                          ║
╚════════════════════════════════════════════════════════════════════╝

1. 📅 Ver recordatorios pendientes
2. ➕ Crear recordatorio
3. ✅ Completar recordatorio
4. ⏸️  Posponer recordatorio
5. 📆 Ver agenda (próximos 7 días)
6. 📤 Exportar recordatorios a texto
7. 🤖 Crear recordatorios auto para nuevos contactos
0. ⬅️  Volver

""")
            option = input("Selecciona una opción: ").strip()

            if option == '1':
                self.view_pending_reminders()
            elif option == '2':
                self.create_reminder()
            elif option == '3':
                self.complete_reminder()
            elif option == '4':
                self.snooze_reminder()
            elif option == '5':
                self.view_schedule()
            elif option == '6':
                self.export_reminders_text()
            elif option == '7':
                self.auto_create_reminders()
            elif option == '0':
                break
            else:
                print("❌ Opción no válida")
                input("Presiona Enter para continuar...")

    def menu_export(self):
        """Menú de exportación"""
        while True:
            self.clear_screen()
            print("""
╔════════════════════════════════════════════════════════════════════╗
║                    📊 EXPORTAR DATOS                                ║
╚════════════════════════════════════════════════════════════════════╝

1. 📤 Exportar todos los contactos
2. 📤 Exportar contactos por estado
3. 💬 Exportar interacciones de contacto
4. ⏰ Exportar recordatorios
5. 📊 Exportar reporte completo
0. ⬅️  Volver

""")
            option = input("Selecciona una opción: ").strip()

            if option == '1':
                self.export_all_contacts()
            elif option == '2':
                self.export_contacts_by_status()
            elif option == '3':
                self.export_contact_interactions()
            elif option == '4':
                self.export_reminders()
            elif option == '5':
                self.export_full_report()
            elif option == '0':
                break
            else:
                print("❌ Opción no válida")
                input("Presiona Enter para continuar...")

    # ===== MÉTODOS DE IMPORTACIÓN =====

    def menu_import_csv(self):
        """Menú de importación desde LinkedIn"""
        while True:
            self.clear_screen()
            print("""
╔════════════════════════════════════════════════════════════════════╗
║               📥 IMPORTAR DESDE LINKEDIN (CSV)                     ║
╚════════════════════════════════════════════════════════════════════╝

1. 📖 Ver instrucciones para exportar desde LinkedIn
2. 📂 Importar archivo CSV
3. 👁️  Vista previa de archivo CSV
0. ⬅️  Volver

""")
            option = input("Selecciona una opción: ").strip()

            if option == '1':
                self.show_export_linkedin_guide()
            elif option == '2':
                self.import_csv_file()
            elif option == '3':
                self.preview_csv_file()
            elif option == '0':
                break
            else:
                print("❌ Opción no válida")
                input("Presiona Enter para continuar...")

    def show_export_linkedin_guide(self):
        """Muestra instrucciones para exportar desde LinkedIn"""
        self.clear_screen()
        export_linkedin_connections_guide()
        input("\nPresiona Enter para continuar...")

    def import_csv_file(self):
        """Importa un archivo CSV"""
        print("\n" + "="*70)
        print("📂 IMPORTAR ARCHIVO CSV")
        print("="*70)

        print("\n💡 El archivo CSV debe estar en la carpeta del proyecto")
        print("   o ingresa la ruta completa\n")

        csv_file = input("📄 Nombre del archivo CSV (o ruta completa): ").strip()

        # Si no tiene extensión, agregarla
        if not csv_file.endswith('.csv'):
            csv_file += '.csv'

        # Si no es ruta absoluta, asumir que está en el directorio actual
        if not os.path.isabs(csv_file):
            csv_file = os.path.join(os.path.dirname(__file__), csv_file)

        if not os.path.exists(csv_file):
            print(f"\n❌ Archivo no encontrado: {csv_file}")
            input("\nPresiona Enter para continuar...")
            return

        print(f"\n📂 Archivo encontrado: {csv_file}")
        print("\n🔍 Analizando archivo...\n")

        # Mostrar preview
        self.csv_importer.show_import_preview(csv_file, max_contacts=5)

        confirm = input("\n⚠️  ¿Importar estos contactos? (s/n): ").strip().lower()

        if confirm == 's':
            print("\n⏳ Importando... esto puede tomar unos segundos...\n")

            stats = self.csv_importer.import_from_csv(csv_file, dry_run=False)

            if stats.get('success'):
                print(f"\n✅ Importación completada!")
                print(f"   Total: {stats['total']} filas")
                print(f"   Importados: {stats['imported']} contactos nuevos")
                print(f"   Omitidos: {stats['skipped']} (ya existían)")
                print(f"   Errores: {stats['errors']}")

                if stats['imported'] > 0:
                    print(f"\n💡 Ahora puedes ver tus contactos en: Gestión de Contactos → Ver todos")
            else:
                print(f"\n❌ Error en la importación: {stats.get('error', 'Desconocido')}")

        input("\nPresiona Enter para continuar...")

    def preview_csv_file(self):
        """Muestra vista previa del CSV"""
        print("\n" + "="*70)
        print("👁️  VISTA PREVIA DE ARCHIVO CSV")
        print("="*70)

        csv_file = input("\n📄 Nombre del archivo CSV: ").strip()

        if not csv_file.endswith('.csv'):
            csv_file += '.csv'

        if not os.path.isabs(csv_file):
            csv_file = os.path.join(os.path.dirname(__file__), csv_file)

        if not os.path.exists(csv_file):
            print(f"\n❌ Archivo no encontrado: {csv_file}")
            input("\nPresiona Enter para continuar...")
            return

        self.csv_importer.show_import_preview(csv_file, max_contacts=20)

        input("\nPresiona Enter para continuar...")

    # ===== MÉTODOS DE CONTACTOS =====

    def add_new_contact(self):
        """Agrega un nuevo contacto"""
        print("\n" + "="*70)
        print("➕ AGREGAR NUEVO CONTACTO")
        print("="*70)

        contact = {}

        # Campos obligatorios
        contact['linkedin_url'] = input("\n🔗 URL de LinkedIn: ").strip()
        if not contact['linkedin_url']:
            print("❌ La URL de LinkedIn es obligatoria")
            input("Presiona Enter para continuar...")
            return

        contact['name'] = input("👤 Nombre completo: ").strip()
        if not contact['name']:
            print("❌ El nombre es obligatorio")
            input("Presiona Enter para continuar...")
            return

        # Campos opcionales
        print("\n📋 Campos opcionales (presiona Enter para omitir):")
        contact['job_title'] = input("   Cargo/Role: ").strip() or None
        contact['company'] = input("   Empresa: ").strip() or None
        contact['location'] = input("   Ubicación: ").strip() or None
        contact['industry'] = input("   Industria: ").strip() or None
        contact['skills'] = input("   Habilidades (separadas por coma): ").strip() or None
        contact['about'] = input("   Sobre mí: ").strip() or None
        contact['notes'] = input("   Notas: ").strip() or None

        # Agregar a DB
        contact_id = self.db.add_contact(contact)

        if contact_id:
            print(f"\n✅ Contacto agregado exitosamente (ID: {contact_id})")

            # Preguntar si quiere crear recordatorio
            create_rem = input("\n⏰ ¿Crear recordatorio para conectar? (s/n): ").strip().lower()
            if create_rem == 's':
                days = input("   ¿En cuántos días? (default: 3): ").strip()
                days = int(days) if days.isdigit() else 3
                self.reminder_system.create_connection_reminder(contact_id, days)

        else:
            print("\n❌ Error al agregar contacto (quizás ya existe)")

        input("\nPresiona Enter para continuar...")

    def view_all_contacts(self):
        """Muestra todos los contactos"""
        print("\n" + "="*70)
        print("📋 TODOS LOS CONTACTOS")
        print("="*70)

        contacts = self.db.get_all_contacts()

        if not contacts:
            print("\n📭 No hay contactos registrados")
            input("Presiona Enter para continuar...")
            return

        print(f"\nTotal: {len(contacts)} contactos\n")

        for i, contact in enumerate(contacts, 1):
            print(f"{i}. {contact['name']}")
            print(f"   🏢 {contact.get('company', 'N/A')} - {contact.get('job_title', 'N/A')}")
            print(f"   📌 Estado: {contact.get('status', 'pending')}")
            print(f"   🔗 {contact.get('linkedin_url', 'N/A')}")
            print("-" * 70)

        input("\nPresiona Enter para continuar...")

    def search_contact(self):
        """Busca un contacto"""
        print("\n" + "="*70)
        print("🔍 BUSCAR CONTACTO")
        print("="*70)

        query = input("\n🔎 Término de búsqueda (nombre, empresa, cargo): ").strip()

        if not query:
            input("Presiona Enter para continuar...")
            return

        results = self.db.search_contacts(query)

        if not results:
            print("\n📭 No se encontraron resultados")
            input("Presiona Enter para continuar...")
            return

        print(f"\n✅ Se encontraron {len(results)} resultados:\n")

        for i, contact in enumerate(results, 1):
            print(f"{i}. {contact['name']}")
            print(f"   🏢 {contact.get('company', 'N/A')} - {contact.get('job_title', 'N/A')}")
            print(f"   📌 Estado: {contact.get('status', 'pending')}")
            print("-" * 70)

        input("\nPresiona Enter para continuar...")

    def edit_contact(self):
        """Edita un contacto"""
        print("\n" + "="*70)
        print("✏️  EDITAR CONTACTO")
        print("="*70)

        contact_id = input("\n🆔 ID del contacto: ").strip()

        if not contact_id.isdigit():
            print("❌ ID no válido")
            input("Presiona Enter para continuar...")
            return

        contact = self.db.get_contact(int(contact_id))

        if not contact:
            print("❌ Contacto no encontrado")
            input("Presiona Enter para continuar...")
            return

        print(f"\nContacto: {contact['name']}")
        print("\n¿Qué deseas editar?")
        print("1. Estado")
        print("2. Notas")
        print("3. Empresa")
        print("4. Cargo")
        print("5. Habilidades")

        option = input("\nOpción: ").strip()

        updates = {}

        if option == '1':
            print("\nEstados disponibles: pending, connected, responded, rejected, not_interested")
            new_status = input("Nuevo estado: ").strip().lower()
            if new_status:
                updates['status'] = new_status

        elif option == '2':
            new_notes = input("Nuevas notas: ").strip()
            if new_notes:
                updates['notes'] = new_notes

        elif option == '3':
            new_company = input("Nueva empresa: ").strip()
            if new_company:
                updates['company'] = new_company

        elif option == '4':
            new_title = input("Nuevo cargo: ").strip()
            if new_title:
                updates['job_title'] = new_title

        elif option == '5':
            new_skills = input("Nuevas habilidades (separadas por coma): ").strip()
            if new_skills:
                updates['skills'] = new_skills

        if updates:
            if self.db.update_contact(int(contact_id), **updates):
                print("✅ Contacto actualizado")
            else:
                print("❌ Error al actualizar")

        input("\nPresiona Enter para continuar...")

    def delete_contact(self):
        """Elimina un contacto"""
        print("\n" + "="*70)
        print("🗑️  ELIMINAR CONTACTO")
        print("="*70)

        contact_id = input("\n🆔 ID del contacto a eliminar: ").strip()

        if not contact_id.isdigit():
            print("❌ ID no válido")
            input("Presiona Enter para continuar...")
            return

        contact = self.db.get_contact(int(contact_id))

        if not contact:
            print("❌ Contacto no encontrado")
            input("Presiona Enter para continuar...")
            return

        print(f"\nContacto: {contact['name']}")
        confirm = input("\n⚠️  ¿Estás seguro de eliminar este contacto? (s/n): ").strip().lower()

        if confirm == 's':
            if self.db.delete_contact(int(contact_id)):
                print("✅ Contacto eliminado")
            else:
                print("❌ Error al eliminar")

        input("\nPresiona Enter para continuar...")

    def view_contact_details(self):
        """Muestra detalles de un contacto"""
        print("\n" + "="*70)
        print("📋 DETALLES DE CONTACTO")
        print("="*70)

        contact_id = input("\n🆔 ID del contacto: ").strip()

        if not contact_id.isdigit():
            print("❌ ID no válido")
            input("Presiona Enter para continuar...")
            return

        contact = self.db.get_contact(int(contact_id))

        if not contact:
            print("❌ Contacto no encontrado")
            input("Presiona Enter para continuar...")
            return

        print(f"\n{'='*70}")
        print(f"👤 {contact['name']}")
        print(f"{'='*70}")
        print(f"🏢 Empresa: {contact.get('company', 'N/A')}")
        print(f"💼 Cargo: {contact.get('job_title', 'N/A')}")
        print(f"📍 Ubicación: {contact.get('location', 'N/A')}")
        print(f"🏭 Industria: {contact.get('industry', 'N/A')}")
        print(f"📌 Estado: {contact.get('status', 'N/A')}")
        print(f"🔗 LinkedIn: {contact.get('linkedin_url', 'N/A')}")
        print(f"\n💻 Habilidades:")
        print(f"   {contact.get('skills', 'N/A')}")
        print(f"\n📝 Notas:")
        print(f"   {contact.get('notes', 'N/A')}")
        print(f"\n📊 Primer contacto: {contact.get('first_contact_date', 'N/A')}")
        print(f"📊 Último contacto: {contact.get('last_contact_date', 'N/A')}")
        print(f"🔄 Follow-ups: {contact.get('follow_up_count', 0)}")

        # Mostrar interacciones
        interactions = self.db.get_contact_interactions(int(contact_id))
        if interactions:
            print(f"\n💬 Interacciones ({len(interactions)}):")
            for interaction in interactions:
                print(f"   - {interaction['interaction_type']}: {interaction.get('outcome', 'N/A')}")
                print(f"     {interaction.get('created_at', 'N/A')}")

        input("\nPresiona Enter para continuar...")

    def filter_by_status(self):
        """Filtra contactos por estado"""
        print("\n" + "="*70)
        print("🏷️  FILTRAR POR ESTADO")
        print("="*70)

        print("\nEstados disponibles:")
        print("  - pending: Pendiente de contacto")
        print("  - connected: Conectado")
        print("  - responded: Respondió")
        print("  - rejected: Rechazó")
        print("  - not_interested: No interesado")

        status = input("\n📌 Estado a filtrar: ").strip().lower()

        if not status:
            input("Presiona Enter para continuar...")
            return

        contacts = self.db.get_all_contacts(status=status)

        if not contacts:
            print(f"\n📭 No hay contactos con estado '{status}'")
            input("Presiona Enter para continuar...")
            return

        print(f"\n✅ Se encontraron {len(contacts)} contactos con estado '{status}':\n")

        for i, contact in enumerate(contacts, 1):
            print(f"{i}. {contact['name']}")
            print(f"   🏢 {contact.get('company', 'N/A')} - {contact.get('job_title', 'N/A')}")
            print("-" * 70)

        input("\nPresiona Enter para continuar...")

    # ===== MÉTODOS DE MENSAJES =====

    def generate_connection_message(self):
        """Genera mensaje de conexión"""
        print("\n" + "="*70)
        print("📨 GENERAR MENSAJE DE CONEXIÓN")
        print("="*70)

        contact_id = input("\n🆔 ID del contacto: ").strip()

        if not contact_id.isdigit():
            print("❌ ID no válido")
            input("Presiona Enter para continuar...")
            return

        contact = self.db.get_contact(int(contact_id))

        if not contact:
            print("❌ Contacto no encontrado")
            input("Presiona Enter para continuar...")
            return

        # Obtener sugerencias
        suggestions = self.msg_generator.get_template_suggestions(contact)

        print("\n📋 Templates sugeridos (ordenados por relevancia):\n")

        for i, suggestion in enumerate(suggestions[:5], 1):
            print(f"{i}. {suggestion['name']} ({suggestion['tone']})")
            print(f"   Score: {suggestion['score']}")
            if suggestion['reasons']:
                print(f"   Razones: {', '.join(suggestion['reasons'])}")

        template_idx = input("\n📋 Selecciona un template (número) o Enter para aleatorio: ").strip()

        if template_idx.isdigit():
            message = self.msg_generator.generate_connection_message(
                contact,
                template_index=int(template_idx) - 1
            )
        else:
            message = self.msg_generator.generate_connection_message(contact)

        print("\n" + "="*70)
        print("💬 MENSAJE GENERADO")
        print("="*70)
        print(message)
        print("="*70)

        # Preguntar si quiere registrar el envío
        register = input("\n📝 ¿Registrar que se envió el mensaje? (s/n): ").strip().lower()

        if register == 's':
            self.db.add_interaction(
                int(contact_id),
                'connection_request',
                message=message,
                outcome='sent'
            )
            self.db.update_contact(int(contact_id), connection_message_sent=1)
            print("✅ Mensaje registrado")

        input("\nPresiona Enter para continuar...")

    def generate_followup_message(self):
        """Genera mensaje de follow-up"""
        print("\n" + "="*70)
        print("🔄 GENERAR MENSAJE DE FOLLOW-UP")
        print("="*70)

        contact_id = input("\n🆔 ID del contacto: ").strip()

        if not contact_id.isdigit():
            print("❌ ID no válido")
            input("Presiona Enter para continuar...")
            return

        contact = self.db.get_contact(int(contact_id))

        if not contact:
            print("❌ Contacto no encontrado")
            input("Presiona Enter para continuar...")
            return

        message = self.msg_generator.generate_follow_up_message(contact)

        print("\n" + "="*70)
        print("💬 MENSAJE DE FOLLOW-UP")
        print("="*70)
        print(message)
        print("="*70)

        # Preguntar si quiere registrar y crear recordatorio
        register = input("\n📝 ¿Registrar follow-up? (s/n): ").strip().lower()

        if register == 's':
            self.db.add_interaction(
                int(contact_id),
                'follow_up',
                message=message
            )
            print("✅ Follow-up registrado")

        input("\nPresiona Enter para continuar...")

    def generate_thankyou_message(self):
        """Genera mensaje de agradecimiento"""
        print("\n" + "="*70)
        print("🙏 GENERAR MENSAJE DE AGRADECIMIENTO")
        print("="*70)

        contact_id = input("\n🆔 ID del contacto: ").strip()

        if not contact_id.isdigit():
            print("❌ ID no válido")
            input("Presiona Enter para continuar...")
            return

        contact = self.db.get_contact(int(contact_id))

        if not contact:
            print("❌ Contacto no encontrado")
            input("Presiona Enter para continuar...")
            return

        print("\nContexto del agradecimiento:")
        print("1. Aceptación de conexión")
        print("2. Post entrevista")
        print("3. Por referencia")

        ctx = input("\nContexto (1-3): ").strip()

        context_map = {'1': 'connection', '2': 'interview', '3': 'referral'}
        context = context_map.get(ctx, 'connection')

        message = self.msg_generator.generate_thank_you_message(contact, context)

        print("\n" + "="*70)
        print("💬 MENSAJE DE AGRADECIMIENTO")
        print("="*70)
        print(message)
        print("="*70)

        input("\nPresiona Enter para continuar...")

    def preview_message(self):
        """Previsualiza un mensaje"""
        print("\n" + "="*70)
        print("👁️  PREVISUALIZAR MENSAJE")
        print("="*70)

        contact_id = input("\n🆔 ID del contacto: ").strip()

        if not contact_id.isdigit():
            print("❌ ID no válido")
            input("Presiona Enter para continuar...")
            return

        contact = self.db.get_contact(int(contact_id))

        if not contact:
            print("❌ Contacto no encontrado")
            input("Presiona Enter para continuar...")
            return

        print("\nTipo de mensaje:")
        print("1. Conexión")
        print("2. Follow-up")
        print("3. Agradecimiento")

        msg_type = input("\nTipo (1-3): ").strip()

        type_map = {'1': 'connection', '2': 'follow_up', '3': 'thank_you'}
        template_type = type_map.get(msg_type, 'connection')

        message = self.msg_generator.preview_message(contact, template_type)

        print("\n" + "="*70)
        print("💬 PREVISUALIZACIÓN")
        print("="*70)
        print(message)
        print("="*70)

        input("\nPresiona Enter para continuar...")

    def view_templates(self):
        """Muestra templates disponibles"""
        print("\n" + "="*70)
        print("📋 TEMPLATES DISPONIBLES")
        print("="*70)

        templates = self.msg_generator.get_all_templates()

        for category, template_list in templates.items():
            print(f"\n📌 {category.upper().replace('_', ' ')}\n")

            for i, template in enumerate(template_list, 1):
                print(f"{i}. {template['name']}")
                print(f"   Tono: {template.get('tone', 'N/A')}")
                preview = template['template'][:100] + "..." if len(template['template']) > 100 else template['template']
                print(f"   Preview: {preview}")
                print()

        input("\nPresiona Enter para continuar...")

    # ===== MÉTODOS DE RECORDATORIOS =====

    def view_pending_reminders(self):
        """Muestra recordatorios pendientes"""
        reminders = self.reminder_system.check_pending_reminders(days_ahead=30)
        self.reminder_system.display_reminders(reminders)
        input("\nPresiona Enter para continuar...")

    def create_reminder(self):
        """Crea un nuevo recordatorio"""
        print("\n" + "="*70)
        print("➕ CREAR RECORDATORIO")
        print("="*70)

        contact_id = input("\n🆔 ID del contacto: ").strip()

        if not contact_id.isdigit():
            print("❌ ID no válido")
            input("Presiona Enter para continuar...")
            return

        days = input("⏰ ¿En cuántos días? (default: 7): ").strip()
        days = int(days) if days.isdigit() else 7

        reminder_id = self.reminder_system.create_follow_up_reminder(
            int(contact_id),
            days_from_now=days
        )

        if reminder_id:
            print("✅ Recordatorio creado")
        else:
            print("❌ Error al crear recordatorio")

        input("\nPresiona Enter para continuar...")

    def complete_reminder(self):
        """Marca un recordatorio como completado"""
        print("\n" + "="*70)
        print("✅ COMPLETAR RECORDATORIO")
        print("="*70)

        reminder_id = input("\n🆔 ID del recordatorio: ").strip()

        if not reminder_id.isdigit():
            print("❌ ID no válido")
            input("Presiona Enter para continuar...")
            return

        if self.reminder_system.complete_reminder(int(reminder_id)):
            print("✅ Recordatorio completado")
        else:
            print("❌ Error al completar")

        input("\nPresiona Enter para continuar...")

    def snooze_reminder(self):
        """Pospone un recordatorio"""
        print("\n" + "="*70)
        print("⏸️  POSPONER RECORDATORIO")
        print("="*70)

        reminder_id = input("\n🆔 ID del recordatorio: ").strip()

        if not reminder_id.isdigit():
            print("❌ ID no válido")
            input("Presiona Enter para continuar...")
            return

        days = input("⏰ ¿Cuántos días posponer? (default: 7): ").strip()
        days = int(days) if days.isdigit() else 7

        if self.reminder_system.snooze_reminder(int(reminder_id), days):
            print(f"✅ Recordatorio pospuesto {days} días")
        else:
            print("❌ Error al posponer")

        input("\nPresiona Enter para continuar...")

    def view_schedule(self):
        """Muestra la agenda"""
        self.reminder_system.display_schedule(days=7)
        input("\nPresiona Enter para continuar...")

    def export_reminders_text(self):
        """Exporta recordatorios a texto"""
        filename = self.reminder_system.export_reminders_to_text(days=7)
        if filename:
            print(f"✅ Exportado a: {filename}")
        input("\nPresiona Enter para continuar...")

    def auto_create_reminders(self):
        """Crea recordatorios automáticamente"""
        print("\n" + "="*70)
        print("🤖 CREAR RECORDATORIOS AUTOMÁTICAMENTE")
        print("="*70)

        days = input("⏰ ¿En cuántos días? (default: 3): ").strip()
        days = int(days) if days.isdigit() else 3

        count = self.reminder_system.auto_create_reminders_for_new_contacts(days)

        if count > 0:
            print(f"✅ Se crearon {count} recordatorios")
        else:
            print("📭 No se crearon recordatorios (ya existen)")

        input("\nPresiona Enter para continuar...")

    # ===== MÉTODOS DE EXPORTACIÓN =====

    def export_all_contacts(self):
        """Exporta todos los contactos"""
        filename = self.export_manager.export_all_contacts()
        if filename:
            print(f"✅ Exportado a: {filename}")
        input("\nPresiona Enter para continuar...")

    def export_contacts_by_status(self):
        """Exporta contactos filtrados por estado"""
        print("\nEstados: pending, connected, responded, rejected, not_interested")
        status = input("Estado: ").strip().lower()

        if status:
            filename = self.export_manager.export_all_contacts(status_filter=status)
            if filename:
                print(f"✅ Exportado a: {filename}")

        input("\nPresiona Enter para continuar...")

    def export_contact_interactions(self):
        """Exporta interacciones de un contacto"""
        contact_id = input("ID del contacto: ").strip()

        if contact_id.isdigit():
            filename = self.export_manager.export_contact_interactions(int(contact_id))
            if filename:
                print(f"✅ Exportado a: {filename}")

        input("\nPresiona Enter para continuar...")

    def export_reminders(self):
        """Exporta recordatorios"""
        filename = self.export_manager.export_reminders()
        if filename:
            print(f"✅ Exportado a: {filename}")
        input("\nPresiona Enter para continuar...")

    def export_full_report(self):
        """Exporta reporte completo"""
        filename = self.export_manager.export_full_report()
        if filename:
            print(f"✅ Exportado a: {filename}")
        input("\nPresiona Enter para continuar...")

    # ===== MÉTODOS DE ESTADÍSTICAS =====

    def show_statistics(self):
        """Muestra estadísticas"""
        print("\n" + "="*70)
        print("📈 ESTADÍSTICAS")
        print("="*70)

        stats = self.db.get_statistics()

        print(f"\n📊 RESUMEN GENERAL")
        print(f"   Total de contactos: {stats.get('total_contacts', 0)}")
        print(f"   Agregados esta semana: {stats.get('added_this_week', 0)}")
        print(f"   Total de interacciones: {stats.get('total_interactions', 0)}")
        print(f"   Recordatorios pendientes: {stats.get('pending_reminders', 0)}")

        by_status = stats.get('by_status', {})
        if by_status:
            print(f"\n📋 POR ESTADO")
            for status, count in by_status.items():
                print(f"   {status}: {count}")

        top_companies = stats.get('top_companies', [])
        if top_companies:
            print(f"\n🏢 TOP EMPRESAS")
            for company, count in top_companies:
                print(f"   {company}: {count}")

        input("\nPresiona Enter para continuar...")

    # ===== MÉTODO PRINCIPAL =====

    def run(self):
        """Ejecuta la aplicación"""
        while True:
            self.clear_screen()
            self.show_main_menu()

            option = input("Selecciona una opción: ").strip()

            if option == '1':
                self.menu_contacts()
            elif option == '2':
                self.menu_messages()
            elif option == '3':
                self.menu_reminders()
            elif option == '4':
                self.menu_export()
            elif option == '5':
                self.show_statistics()
            elif option == '6':
                self.menu_import_csv()
            elif option == '7':
                print("\n⚙️  Configuración")
                print("Edita el archivo .env para configurar la aplicación")
                input("\nPresiona Enter para continuar...")
            elif option == '0':
                print("\n👋 ¡Gracias por usar LinkedIn Networking Suite!")
                print("Recuerda: El networking manual y auténtico es el más efectivo 🤝\n")
                break
            else:
                print("❌ Opción no válida")
                input("Presiona Enter para continuar...")


def main():
    """Punto de entrada"""
    app = LinkedInNetworkingSuite()
    app.run()


if __name__ == "__main__":
    main()
