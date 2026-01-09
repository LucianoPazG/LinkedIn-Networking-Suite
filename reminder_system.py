#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Recordatorios para LinkedIn Networking Suite
Gestiona recordatorios de follow-up y notificaciones
"""

import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
from dotenv import load_dotenv

from database import ContactDatabase
from message_generator import MessageGenerator

load_dotenv()

logger = logging.getLogger(__name__)


class ReminderSystem:
    """Sistema de recordatorios automáticos"""

    def __init__(self, db: ContactDatabase):
        """
        Inicializa el sistema de recordatorios

        Args:
            db: Instancia de ContactDatabase
        """
        self.db = db
        self.msg_generator = MessageGenerator()

        # Configuración desde .env
        self.default_interval_days = int(os.getenv('REMINDER_INTERVAL_DAYS', '7'))

    def create_follow_up_reminder(self, contact_id: int,
                                 days_from_now: Optional[int] = None,
                                 reminder_type: str = 'follow_up',
                                 custom_message: Optional[str] = None) -> Optional[int]:
        """
        Crea un recordatorio de follow-up para un contacto

        Args:
            contact_id: ID del contacto
            days_from_now: Días desde hoy (default: valor de .env)
            reminder_type: Tipo de recordatorio
            custom_message: Mensaje personalizado

        Returns:
            ID del recordatorio creado o None
        """
        contact = self.db.get_contact(contact_id)

        if not contact:
            logger.error(f"Contacto {contact_id} no encontrado")
            return None

        # Calcular fecha del recordatorio
        days = days_from_now or self.default_interval_days
        reminder_date = (datetime.now() + timedelta(days=days)).isoformat()

        # Generar mensaje sugerido si no se proporciona
        if not custom_message:
            custom_message = self.msg_generator.generate_follow_up_message(contact)

        # Crear recordatorio
        reminder_id = self.db.add_reminder(
            contact_id=contact_id,
            reminder_date=reminder_date,
            reminder_type=reminder_type,
            message=custom_message
        )

        if reminder_id:
            logger.info(f"Recordatorio creado para contacto {contact_id} ({days} días)")
            print(f"✅ Recordatorio agendado para {datetime.fromisoformat(reminder_date).strftime('%d/%m/%Y')}")

        return reminder_id

    def create_connection_reminder(self, contact_id: int,
                                  days_from_now: int = 3) -> Optional[int]:
        """
        Crea un recordatorio para enviar conexión manual

        Args:
            contact_id: ID del contacto
            days_from_now: Días desde hoy

        Returns:
            ID del recordatorio o None
        """
        contact = self.db.get_contact(contact_id)

        if not contact:
            return None

        reminder_date = (datetime.now() + timedelta(days=days_from_now)).isoformat()

        # Mensaje de recordatorio
        message = f"Recordatorio: Enviar solicitud de conexión a {contact['name']} ({contact.get('company', 'N/A')})"

        reminder_id = self.db.add_reminder(
            contact_id=contact_id,
            reminder_date=reminder_date,
            reminder_type='connection_request',
            message=message
        )

        if reminder_id:
            logger.info(f"Recordatorio de conexión creado para contacto {contact_id}")

        return reminder_id

    def check_pending_reminders(self, days_ahead: int = 1) -> List[Dict]:
        """
        Verifica recordatorios pendientes

        Args:
            days_ahead: Días adelante para buscar

        Returns:
            Lista de recordatorios pendientes
        """
        reminders = self.db.get_pending_reminders(days_ahead)

        if reminders:
            logger.info(f"Se encontraron {len(reminders)} recordatorios pendientes")

        return reminders

    def display_reminders(self, reminders: List[Dict]) -> None:
        """
        Muestra los recordatorios de forma formateada

        Args:
            reminders: Lista de recordatorios
        """
        if not reminders:
            print("\n✅ No tienes recordatorios pendientes")
            return

        print("\n" + "=" * 70)
        print("📅 RECORDATORIOS PENDIENTES")
        print("=" * 70)

        for i, reminder in enumerate(reminders, 1):
            reminder_date = datetime.fromisoformat(reminder['reminder_date'])
            is_today = reminder_date.date() == datetime.now().date()
            is_past = reminder_date < datetime.now()

            date_str = reminder_date.strftime("%d/%m/%Y")
            time_str = reminder_date.strftime("%H:%M")

            # Indicador de urgencia
            if is_today:
                urgency = "🔴 HOY"
            elif is_past:
                urgency = "⚠️  ATRASADO"
            else:
                urgency = "📅 Próximo"

            print(f"\n{i}. {urgency} - {date_str} a las {time_str}")
            print(f"   👤 Contacto: {reminder['name']}")
            print(f"   🏢 Empresa: {reminder.get('company', 'N/A')}")
            print(f"   📌 Tipo: {reminder['reminder_type'].replace('_', ' ').title()}")

            if reminder.get('message'):
                print(f"   💬 Mensaje sugerido:")
                print(f"   {reminder['message'][:100]}{'...' if len(reminder['message']) > 100 else ''}")

            print("-" * 70)

    def complete_reminder(self, reminder_id: int) -> bool:
        """
        Marca un recordatorio como completado

        Args:
            reminder_id: ID del recordatorio

        Returns:
            True si se completó correctamente
        """
        success = self.db.complete_reminder(reminder_id)

        if success:
            logger.info(f"Recordatorio {reminder_id} completado")
            print("✅ Recordatorio marcado como completado")

        return success

    def snooze_reminder(self, reminder_id: int, days: int = 7) -> bool:
        """
        Posponer un recordatorio

        Args:
            reminder_id: ID del recordatorio
            days: Días a posponer

        Returns:
            True si se pospuso correctamente
        """
        # Primero marcar como completado el actual
        self.db.complete_reminder(reminder_id)

        # Obtener información del recordatorio
        conn = self.db._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT contact_id, reminder_type
                FROM reminders
                WHERE id = ?
            """, (reminder_id,))

            result = cursor.fetchone()

            if result:
                # Crear nuevo recordatorio
                new_reminder_id = self.create_follow_up_reminder(
                    contact_id=result['contact_id'],
                    days_from_now=days,
                    reminder_type=result['reminder_type']
                )

                if new_reminder_id:
                    print(f"✅ Recordatorio pospuesto {days} días")
                    return True

        except Exception as e:
            logger.error(f"Error posponiendo recordatorio: {e}")
        finally:
            conn.close()

        return False

    def auto_create_reminders_for_new_contacts(self, days: int = 3) -> int:
        """
        Crea recordatorios automáticamente para contactos nuevos sin recordatorios

        Args:
            days: Días desde hoy para el recordatorio

        Returns:
            Cantidad de recordatorios creados
        """
        # Obtener contactos pendientes
        pending_contacts = self.db.get_all_contacts(status='pending')

        created_count = 0

        for contact in pending_contacts:
            # Verificar si ya tiene recordatorios
            conn = self.db._get_connection()
            cursor = conn.cursor()

            try:
                cursor.execute("""
                    SELECT COUNT(*) as count
                    FROM reminders
                    WHERE contact_id = ?
                """, (contact['id'],))

                has_reminders = cursor.fetchone()['count'] > 0

                if not has_reminders:
                    reminder_id = self.create_connection_reminder(
                        contact_id=contact['id'],
                        days_from_now=days
                    )

                    if reminder_id:
                        created_count += 1

            except Exception as e:
                logger.error(f"Error creando recordatorio auto: {e}")
            finally:
                conn.close()

        if created_count > 0:
            print(f"✅ Se crearon {created_count} recordatorios automáticamente")

        return created_count

    def get_upcoming_schedule(self, days: int = 7) -> List[Dict]:
        """
        Obtiene el schedule de los próximos días

        Args:
            days: Días a mostrar

        Returns:
            Lista de recordatorios organizados por fecha
        """
        reminders = self.db.get_pending_reminders(days_ahead=days)

        # Agrupar por fecha
        schedule = {}

        for reminder in reminders:
            date_key = reminder['reminder_date'][:10]  # YYYY-MM-DD

            if date_key not in schedule:
                schedule[date_key] = []

            schedule[date_key].append(reminder)

        return schedule

    def display_schedule(self, days: int = 7) -> None:
        """
        Muestra el schedule de manera visual

        Args:
            days: Días a mostrar
        """
        schedule = self.get_upcoming_schedule(days)

        if not schedule:
            print("\n✅ No tienes recordatorios para los próximos días")
            return

        print("\n" + "=" * 70)
        print(f"📅 AGENDA - PRÓXIMOS {days} DÍAS")
        print("=" * 70)

        # Ordenar fechas
        sorted_dates = sorted(schedule.keys())

        for date_key in sorted_dates:
            date_obj = datetime.fromisoformat(date_key)
            is_today = date_obj.date() == datetime.now().date()

            if is_today:
                date_str = f"🔴 HOY ({date_obj.strftime('%d/%m/%Y')})"
            else:
                date_str = f"📅 {date_obj.strftime('%d/%m/%Y')}"

            print(f"\n{date_str}")
            print("-" * 70)

            for reminder in schedule[date_key]:
                time_str = datetime.fromisoformat(reminder['reminder_date']).strftime("%H:%M")
                print(f"  {time_str} - {reminder['name']} ({reminder.get('company', 'N/A')})")
                print(f"           {reminder['reminder_type'].replace('_', ' ').title()}")

    def export_reminders_to_text(self, days: int = 7) -> Optional[str]:
        """
        Exporta recordatorios a un archivo de texto

        Args:
            days: Días a incluir

        Returns:
            Ruta del archivo o None
        """
        reminders = self.db.get_pending_reminders(days_ahead=days)

        if not reminders:
            print("No hay recordatorios para exportar")
            return None

        filename = f"recordatorios_{datetime.now().strftime('%Y%m%d')}.txt"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 70 + "\n")
                f.write(f"RECORDATORIOS - PRÓXIMOS {days} DÍAS\n")
                f.write(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
                f.write("=" * 70 + "\n\n")

                for reminder in reminders:
                    reminder_date = datetime.fromisoformat(reminder['reminder_date'])
                    f.write(f"📅 Fecha: {reminder_date.strftime('%d/%m/%Y %H:%M')}\n")
                    f.write(f"👤 Contacto: {reminder['name']}\n")
                    f.write(f"🏢 Empresa: {reminder.get('company', 'N/A')}\n")
                    f.write(f"📌 Tipo: {reminder['reminder_type']}\n")

                    if reminder.get('message'):
                        f.write(f"💬 Mensaje: {reminder['message']}\n")

                    f.write(f"🔗 LinkedIn: {reminder['linkedin_url']}\n")
                    f.write("-" * 70 + "\n\n")

            print(f"✅ Recordatorios exportados a: {filename}")
            return filename

        except Exception as e:
            logger.error(f"Error exportando recordatorios: {e}")
            return None

    def get_statistics(self) -> Dict:
        """
        Obtiene estadísticas de recordatorios

        Returns:
            Diccionario con estadísticas
        """
        conn = self.db._get_connection()
        cursor = conn.cursor()

        try:
            stats = {}

            # Total de recordatorios
            cursor.execute("SELECT COUNT(*) as total FROM reminders WHERE is_completed = 0")
            stats['total_pending'] = cursor.fetchone()['total']

            # Recordatorios por tipo
            cursor.execute("""
                SELECT reminder_type, COUNT(*) as count
                FROM reminders
                WHERE is_completed = 0
                GROUP BY reminder_type
            """)
            stats['by_type'] = {row['reminder_type']: row['count'] for row in cursor.fetchall()}

            # Recordatorios para hoy
            today = datetime.now().strftime('%Y-%m-%d')
            cursor.execute("""
                SELECT COUNT(*) as total
                FROM reminders
                WHERE is_completed = 0 AND date(reminder_date) = ?
            """, (today,))
            stats['due_today'] = cursor.fetchone()['total']

            # Recordatorios atrasados
            cursor.execute("""
                SELECT COUNT(*) as total
                FROM reminders
                WHERE is_completed = 0 AND reminder_date < ?
            """, (datetime.now().isoformat(),))
            stats['overdue'] = cursor.fetchone()['total']

            return stats

        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            return {}
        finally:
            conn.close()
