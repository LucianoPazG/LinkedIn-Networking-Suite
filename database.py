#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de Base de Datos para LinkedIn Networking Suite
Maneja el almacenamiento y recuperación de contactos de recruiters
"""

import os
import sqlite3
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class ContactDatabase:
    """Gestiona la base de datos SQLite de contactos"""

    def __init__(self, db_path: str = "data/contacts.db"):
        """Inicializa la conexión a la base de datos"""
        self.db_path = db_path

        # Crear directorio si no existe
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        # Inicializar base de datos
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """Obtiene una conexión a la base de datos"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        """Crea las tablas necesarias si no existen"""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            # Tabla de contactos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    linkedin_url TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    job_title TEXT,
                    company TEXT,
                    location TEXT,
                    industry TEXT,
                    about TEXT,
                    skills TEXT,
                    notes TEXT,
                    first_contact_date TEXT,
                    last_contact_date TEXT,
                    status TEXT DEFAULT 'pending',
                    connection_message_sent INTEGER DEFAULT 0,
                    follow_up_count INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Tabla de interacciones
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    contact_id INTEGER NOT NULL,
                    interaction_type TEXT NOT NULL,
                    message TEXT,
                    outcome TEXT,
                    next_follow_up_date TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (contact_id) REFERENCES contacts(id) ON DELETE CASCADE
                )
            """)

            # Tabla de recordatorios
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    contact_id INTEGER NOT NULL,
                    reminder_date TEXT NOT NULL,
                    reminder_type TEXT NOT NULL,
                    message TEXT,
                    is_completed INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (contact_id) REFERENCES contacts(id) ON DELETE CASCADE
                )
            """)

            # Índices para optimizar búsquedas
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_contacts_status
                ON contacts(status)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_contacts_company
                ON contacts(company)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_interactions_contact_id
                ON interactions(contact_id)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_reminders_date
                ON reminders(reminder_date)
            """)

            conn.commit()
            logger.info("Base de datos inicializada correctamente")

        except Exception as e:
            logger.error(f"Error inicializando base de datos: {e}")
            raise
        finally:
            conn.close()

    def add_contact(self, contact_data: Dict) -> Optional[int]:
        """
        Agrega un nuevo contacto a la base de datos

        Args:
            contact_data: Diccionario con los datos del contacto

        Returns:
            ID del contacto agregado o None si hubo error
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            now = datetime.now().isoformat()

            cursor.execute("""
                INSERT OR REPLACE INTO contacts (
                    linkedin_url, name, job_title, company, location,
                    industry, about, skills, notes, first_contact_date,
                    last_contact_date, status, connection_message_sent,
                    follow_up_count, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                contact_data.get('linkedin_url'),
                contact_data.get('name'),
                contact_data.get('job_title'),
                contact_data.get('company'),
                contact_data.get('location'),
                contact_data.get('industry'),
                contact_data.get('about'),
                contact_data.get('skills'),
                contact_data.get('notes'),
                contact_data.get('first_contact_date', now),
                contact_data.get('last_contact_date', now),
                contact_data.get('status', 'pending'),
                contact_data.get('connection_message_sent', 0),
                contact_data.get('follow_up_count', 0),
                now
            ))

            conn.commit()
            contact_id = cursor.lastrowid
            logger.info(f"Contacto agregado: {contact_data.get('name')} (ID: {contact_id})")
            return contact_id

        except sqlite3.IntegrityError:
            logger.warning(f"El contacto con URL {contact_data.get('linkedin_url')} ya existe")
            return None
        except Exception as e:
            logger.error(f"Error agregando contacto: {e}")
            return None
        finally:
            conn.close()

    def get_contact(self, contact_id: int) -> Optional[Dict]:
        """Obtiene un contacto por su ID"""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
            row = cursor.fetchone()

            if row:
                return dict(row)
            return None

        except Exception as e:
            logger.error(f"Error obteniendo contacto: {e}")
            return None
        finally:
            conn.close()

    def get_contact_by_url(self, linkedin_url: str) -> Optional[Dict]:
        """Obtiene un contacto por su URL de LinkedIn"""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM contacts WHERE linkedin_url = ?", (linkedin_url,))
            row = cursor.fetchone()

            if row:
                return dict(row)
            return None

        except Exception as e:
            logger.error(f"Error obteniendo contacto por URL: {e}")
            return None
        finally:
            conn.close()

    def get_all_contacts(self, status: Optional[str] = None,
                        limit: Optional[int] = None) -> List[Dict]:
        """
        Obtiene todos los contactos, opcionalmente filtrados por estado

        Args:
            status: Filtrar por estado ('pending', 'connected', 'rejected', etc.)
            limit: Limitar cantidad de resultados

        Returns:
            Lista de contactos
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            query = "SELECT * FROM contacts"
            params = []

            if status:
                query += " WHERE status = ?"
                params.append(status)

            query += " ORDER BY created_at DESC"

            if limit:
                query += " LIMIT ?"
                params.append(limit)

            cursor.execute(query, params)
            rows = cursor.fetchall()

            return [dict(row) for row in rows]

        except Exception as e:
            logger.error(f"Error obteniendo contactos: {e}")
            return []
        finally:
            conn.close()

    def update_contact_status(self, contact_id: int, status: str) -> bool:
        """Actualiza el estado de un contacto"""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            now = datetime.now().isoformat()
            cursor.execute("""
                UPDATE contacts
                SET status = ?, updated_at = ?
                WHERE id = ?
            """, (status, now, contact_id))

            conn.commit()
            logger.info(f"Contacto {contact_id} actualizado a estado: {status}")
            return True

        except Exception as e:
            logger.error(f"Error actualizando estado: {e}")
            return False
        finally:
            conn.close()

    def update_contact(self, contact_id: int, **kwargs) -> bool:
        """
        Actualiza campos específicos de un contacto

        Args:
            contact_id: ID del contacto
            **kwargs: Campos a actualizar (name, company, notes, etc.)

        Returns:
            True si se actualizó correctamente
        """
        if not kwargs:
            return False

        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            now = datetime.now().isoformat()
            kwargs['updated_at'] = now

            set_clause = ", ".join(f"{k} = ?" for k in kwargs.keys())
            values = list(kwargs.values()) + [contact_id]

            cursor.execute(f"""
                UPDATE contacts
                SET {set_clause}
                WHERE id = ?
            """, values)

            conn.commit()
            logger.info(f"Contacto {contact_id} actualizado")
            return True

        except Exception as e:
            logger.error(f"Error actualizando contacto: {e}")
            return False
        finally:
            conn.close()

    def delete_contact(self, contact_id: int) -> bool:
        """Elimina un contacto"""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
            conn.commit()
            logger.info(f"Contacto {contact_id} eliminado")
            return True

        except Exception as e:
            logger.error(f"Error eliminando contacto: {e}")
            return False
        finally:
            conn.close()

    def add_interaction(self, contact_id: int, interaction_type: str,
                       message: str = None, outcome: str = None,
                       next_follow_up: str = None) -> Optional[int]:
        """
        Registra una interacción con un contacto

        Args:
            contact_id: ID del contacto
            interaction_type: Tipo de interacción (connection_request, message, email, etc.)
            message: Mensaje enviado
            outcome: Resultado (accepted, rejected, no_response, etc.)
            next_follow_up: Fecha del próximo follow-up

        Returns:
            ID de la interacción o None si hubo error
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            now = datetime.now().isoformat()

            cursor.execute("""
                INSERT INTO interactions (
                    contact_id, interaction_type, message, outcome, next_follow_up_date, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (contact_id, interaction_type, message, outcome, next_follow_up, now))

            conn.commit()
            interaction_id = cursor.lastrowid

            # Actualizar contador de follow-ups si corresponde
            if interaction_type == 'follow_up':
                cursor.execute("""
                    UPDATE contacts
                    SET follow_up_count = follow_up_count + 1,
                        last_contact_date = ?
                    WHERE id = ?
                """, (now, contact_id))
                conn.commit()

            logger.info(f"Interacción registrada para contacto {contact_id}")
            return interaction_id

        except Exception as e:
            logger.error(f"Error registrando interacción: {e}")
            return None
        finally:
            conn.close()

    def get_contact_interactions(self, contact_id: int) -> List[Dict]:
        """Obtiene todas las interacciones de un contacto"""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT * FROM interactions
                WHERE contact_id = ?
                ORDER BY created_at DESC
            """, (contact_id,))

            rows = cursor.fetchall()
            return [dict(row) for row in rows]

        except Exception as e:
            logger.error(f"Error obteniendo interacciones: {e}")
            return []
        finally:
            conn.close()

    def add_reminder(self, contact_id: int, reminder_date: str,
                    reminder_type: str, message: str = None) -> Optional[int]:
        """
        Agrega un recordatorio para follow-up

        Args:
            contact_id: ID del contacto
            reminder_date: Fecha del recordatorio (ISO format)
            reminder_type: Tipo de recordatorio
            message: Mensaje sugerido

        Returns:
            ID del recordatorio o None si hubo error
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO reminders (
                    contact_id, reminder_date, reminder_type, message
                ) VALUES (?, ?, ?, ?)
            """, (contact_id, reminder_date, reminder_type, message))

            conn.commit()
            reminder_id = cursor.lastrowid
            logger.info(f"Recordatorio agregado para contacto {contact_id}")
            return reminder_id

        except Exception as e:
            logger.error(f"Error agregando recordatorio: {e}")
            return None
        finally:
            conn.close()

    def get_pending_reminders(self, days_ahead: int = 1) -> List[Dict]:
        """
        Obtiene recordatorios pendientes

        Args:
            days_ahead: Días adelante para buscar (default: 1 = hoy y mañana)

        Returns:
            Lista de recordatorios con información del contacto
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            now = datetime.now()
            future_date = now + timedelta(days=days_ahead)

            cursor.execute("""
                SELECT
                    r.id as reminder_id,
                    r.reminder_date,
                    r.reminder_type,
                    r.message,
                    c.id as contact_id,
                    c.name,
                    c.company,
                    c.job_title,
                    c.linkedin_url
                FROM reminders r
                JOIN contacts c ON r.contact_id = c.id
                WHERE r.is_completed = 0
                  AND date(r.reminder_date) <= date(?)
                ORDER BY r.reminder_date ASC
            """, (future_date.isoformat(),))

            rows = cursor.fetchall()
            return [dict(row) for row in rows]

        except Exception as e:
            logger.error(f"Error obteniendo recordatorios: {e}")
            return []
        finally:
            conn.close()

    def complete_reminder(self, reminder_id: int) -> bool:
        """Marca un recordatorio como completado"""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE reminders
                SET is_completed = 1
                WHERE id = ?
            """, (reminder_id,))

            conn.commit()
            logger.info(f"Recordatorio {reminder_id} marcado como completado")
            return True

        except Exception as e:
            logger.error(f"Error completando recordatorio: {e}")
            return False
        finally:
            conn.close()

    def get_statistics(self) -> Dict:
        """Obtiene estadísticas de la base de datos"""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            stats = {}

            # Total de contactos
            cursor.execute("SELECT COUNT(*) as total FROM contacts")
            stats['total_contacts'] = cursor.fetchone()['total']

            # Contactos por estado
            cursor.execute("""
                SELECT status, COUNT(*) as count
                FROM contacts
                GROUP BY status
            """)
            stats['by_status'] = {row['status']: row['count'] for row in cursor.fetchall()}

            # Contactos agregados esta semana
            week_ago = (datetime.now() - timedelta(days=7)).isoformat()
            cursor.execute("""
                SELECT COUNT(*) as count FROM contacts
                WHERE created_at >= ?
            """, (week_ago,))
            stats['added_this_week'] = cursor.fetchone()['count']

            # Top empresas
            cursor.execute("""
                SELECT company, COUNT(*) as count
                FROM contacts
                WHERE company IS NOT NULL AND company != ''
                GROUP BY company
                ORDER BY count DESC
                LIMIT 5
            """)
            stats['top_companies'] = [(row['company'], row['count']) for row in cursor.fetchall()]

            # Total de interacciones
            cursor.execute("SELECT COUNT(*) as total FROM interactions")
            stats['total_interactions'] = cursor.fetchone()['total']

            # Recordatorios pendientes
            cursor.execute("SELECT COUNT(*) as total FROM reminders WHERE is_completed = 0")
            stats['pending_reminders'] = cursor.fetchone()['total']

            return stats

        except Exception as e:
            logger.error(f"Error obteniendo estadísticas: {e}")
            return {}
        finally:
            conn.close()

    def search_contacts(self, query: str) -> List[Dict]:
        """
        Busca contactos por nombre, empresa o cargo

        Args:
            query: Término de búsqueda

        Returns:
            Lista de contactos que coinciden
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            search_pattern = f"%{query}%"
            cursor.execute("""
                SELECT * FROM contacts
                WHERE name LIKE ?
                   OR company LIKE ?
                   OR job_title LIKE ?
                   OR skills LIKE ?
                ORDER BY name ASC
            """, (search_pattern, search_pattern, search_pattern, search_pattern))

            rows = cursor.fetchall()
            return [dict(row) for row in rows]

        except Exception as e:
            logger.error(f"Error buscando contactos: {e}")
            return []
        finally:
            conn.close()

    def get_contacts_due_for_followup(self, days_since_last_contact: int = 7) -> List[Dict]:
        """
        Obtiene contactos que necesitan follow-up

        Args:
            days_since_last_contact: Días desde el último contacto

        Returns:
            Lista de contactos que necesitan follow-up
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cutoff_date = (datetime.now() - timedelta(days=days_since_last_contact)).isoformat()

            cursor.execute("""
                SELECT * FROM contacts
                WHERE status IN ('connected', 'responded')
                  AND (last_contact_date IS NULL OR last_contact_date <= ?)
                ORDER BY last_contact_date ASC
            """, (cutoff_date,))

            rows = cursor.fetchall()
            return [dict(row) for row in rows]

        except Exception as e:
            logger.error(f"Error obteniendo contactos para follow-up: {e}")
            return []
        finally:
            conn.close()
