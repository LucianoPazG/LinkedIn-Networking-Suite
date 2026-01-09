#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Mensajes Personalizados para LinkedIn
Crea templates y ayuda a personalizar mensajes para networking
"""

import random
from typing import Dict, List, Optional
import re


class MessageGenerator:
    """Genera mensajes personalizados para conectar con recruiters"""

    # Templates de conexión inicial
    CONNECTION_TEMPLATES = [
        {
            'name': 'Profesional Directo',
            'template': """Hola {name}, vi tu perfil y me interesó tu experiencia en {industry}. Me gustaría conectarme para mantenerme actualizado sobre oportunidades en el área de {role_focus}.

Gracias por considerar mi solicitud!""",
            'tone': 'professional',
            'length': 'short'
        },
        {
            'name': 'Interés Común',
            'template': """Hola {name}, noté que trabajas en {company} y me llamó la atención su enfoque en {industry}. Como {role_focus} con experiencia en {skills_highlight}, estaría interesado en conocer más sobre las oportunidades que puedan surgir.

Quedo a disposición para conversar!""",
            'tone': 'friendly',
            'length': 'medium'
        },
        {
            'name': 'Cambio de Rol',
            'template': """Hola {name}, estoy explorando nuevas oportunidades como {role_focus} y tu experiencia en {industry} me parece muy relevante. Me gustaría conectar y aprender más sobre el mercado actual.

Saludos!""",
            'tone': 'casual',
            'length': 'short'
        },
        {
            'name': 'Específico de Empresa',
            'template': """Hola {name}, he seguido el trabajo de {company} en el ámbito de {industry} y me gustaría ser parte del equipo. Como {role_focus}, creo que podría aportar valor con mi experiencia en {skills_highlight}.

¿Te gustaría que conversemos?""",
            'tone': 'professional',
            'length': 'medium'
        },
        {
            'name': 'Recomendación',
            'template': """Hola {name}, tu perfil fue recomendado por {referrer} como alguien con gran expertise en {industry}. Me gustaría conectar para explorar posibles oportunidades como {role_focus}.

Gracias!""",
            'tone': 'professional',
            'length': 'short'
        }
    ]

    # Templates de follow-up
    FOLLOW_UP_TEMPLATES = [
        {
            'name': 'Check-in Casual',
            'template': """Hola {name}, ¿cómo estás? Espero que todo vaya bien en {company}.

Quería hacer un seguimiento de nuestra última conversación. ¿Hay alguna novedad respecto a oportunidades para {role_focus}?

Quedo atento!""",
            'days_after': 7
        },
        {
            'name': 'Valor Agregado',
            'template': """Hola {name}, vi que {company} está {company_news}. Me parece muy interesante y refuerza mi interés en colaborar con ustedes.

¿Tienen un momento esta semana para conversar sobre cómo puedo aportar como {role_focus}?

Saludos!""",
            'days_after': 10
        },
        {
            'name': 'Actualización',
            'template': """Hola {name}, te contacto para compartir que {my_update}.

Sigo muy interesado en oportunidades en {company}. ¿Hay alguna posición que pueda encajar con mi perfil?

Gracias!""",
            'days_after': 14
        },
        {
            'name': 'Artículo/Recurso',
            'template': """Hola {name}, vi este artículo sobre {topic} y pensé que podría interesarte: {article_link}.

Está alineado con las tendencias en {industry}. ¿Qué opinas?

Además, quería preguntar si hay alguna novedad sobre posiciones de {role_focus}.

Saludos!""",
            'days_after': 7
        }
    ]

    # Templates de agradecimiento
    THANK_YOU_TEMPLATES = [
        {
            'name': 'Aceptación de Conexión',
            'template': """Gracias por conectar, {name}!

Realmente valoro tu tiempo. Me gustaría conocer más sobre tu rol en {company} y las oportunidades que puedan surgir para {role_focus}.

¿Tienes disponibilidad para una breve llamada esta semana?"""
        },
        {
            'name': 'Post Entrevista',
            'template': """Hola {name}, gracias por el tiempo para conversar sobre la posición de {position}.

Me pareció muy interesante el enfoque de {company} en {topic_discussed}. Quedo muy entusiasmado con la posibilidad de unirme al equipo.

Quedo atento a novedades!"""
        },
        {
            'name': 'Por Referencia',
            'template': """Hola {name}, gracias por la referencia de {referrer}!

Tu experiencia en {industry} es muy valiosa. Me gustaría escuchar más sobre tu trayectoria en {company} y cualquier consejo que puedas darme sobre {role_focus}.

Saludos y gracias nuevamente!"""
        }
    ]

    def __init__(self):
        """Inicializa el generador de mensajes"""
        pass

    def generate_connection_message(self, contact: Dict,
                                   template_index: Optional[int] = None,
                                   custom_vars: Optional[Dict] = None) -> str:
        """
        Genera un mensaje de conexión personalizado

        Args:
            contact: Diccionario con datos del contacto
            template_index: Índice del template a usar (None = aleatorio)
            custom_vars: Variables personalizadas adicionales

        Returns:
            Mensaje personalizado
        """
        # Seleccionar template
        if template_index is not None:
            template = self.CONNECTION_TEMPLATES[template_index]
        else:
            template = random.choice(self.CONNECTION_TEMPLATES)

        message = template['template']

        # Variables básicas del contacto
        variables = {
            'name': contact.get('name', '').split()[0] if contact.get('name') else 'there',
            'company': contact.get('company', 'tu empresa'),
            'industry': contact.get('industry', 'el sector'),
            'job_title': contact.get('job_title', 'tu rol'),
        }

        # Variables personalizadas
        if custom_vars:
            variables.update(custom_vars)
        else:
            # Valores por defecto si no se proporcionan
            variables.update({
                'role_focus': contact.get('skills', 'mi área'),
                'skills_highlight': self._extract_top_skills(contact.get('skills', '')),
                'referrer': 'un colega',
            })

        # Reemplazar variables
        message = self._replace_variables(message, variables)

        return message.strip()

    def generate_follow_up_message(self, contact: Dict,
                                  template_index: Optional[int] = None,
                                  custom_vars: Optional[Dict] = None) -> str:
        """
        Genera un mensaje de follow-up personalizado

        Args:
            contact: Diccionario con datos del contacto
            template_index: Índice del template a usar
            custom_vars: Variables personalizadas adicionales

        Returns:
            Mensaje de follow-up
        """
        if template_index is not None:
            template = self.FOLLOW_UP_TEMPLATES[template_index]
        else:
            template = random.choice(self.FOLLOW_UP_TEMPLATES)

        message = template['template']

        variables = {
            'name': contact.get('name', '').split()[0] if contact.get('name') else 'there',
            'company': contact.get('company', 'tu empresa'),
            'role_focus': contact.get('skills', 'mi área'),
        }

        if custom_vars:
            variables.update(custom_vars)
        else:
            variables.update({
                'company_news': 'lanzando nuevos proyectos',
                'my_update': 'completé una certificación relevante',
                'topic': 'nuestras tendencias de la industria',
                'article_link': '[enlace al artículo]',
            })

        message = self._replace_variables(message, variables)

        return message.strip()

    def generate_thank_you_message(self, contact: Dict,
                                  context: str = 'connection',
                                  custom_vars: Optional[Dict] = None) -> str:
        """
        Genera un mensaje de agradecimiento

        Args:
            contact: Diccionario con datos del contacto
            context: Contexto del agradecimiento (connection, interview, referral)
            custom_vars: Variables personalizadas adicionales

        Returns:
            Mensaje de agradecimiento
        """
        # Filtrar templates por contexto
        if context == 'interview':
            templates = [t for t in self.THANK_YOU_TEMPLATES if 'Entrevista' in t['name']]
        elif context == 'referral':
            templates = [t for t in self.THANK_YOU_TEMPLATES if 'Referencia' in t['name']]
        else:
            templates = [t for t in self.THANK_YOU_TEMPLATES if 'Aceptación' in t['name']]

        if not templates:
            templates = self.THANK_YOU_TEMPLATES

        template = random.choice(templates)
        message = template['template']

        variables = {
            'name': contact.get('name', '').split()[0] if contact.get('name') else 'there',
            'company': contact.get('company', 'tu empresa'),
            'role_focus': contact.get('skills', 'mi área'),
        }

        if custom_vars:
            variables.update(custom_vars)
        else:
            variables.update({
                'position': 'la posición',
                'topic_discussed': 'los desafíos del rol',
                'referrer': 'nuestro contacto en común',
            })

        message = self._replace_variables(message, variables)

        return message.strip()

    def _replace_variables(self, message: str, variables: Dict[str, str]) -> str:
        """Reemplaza variables en el template"""
        for var, value in variables.items():
            placeholder = f"{{{var}}}"
            message = message.replace(placeholder, str(value))

        return message

    def _extract_top_skills(self, skills_string: str, max_skills: int = 2) -> str:
        """
        Extrae las habilidades principales de un string de skills

        Args:
            skills_string: String con habilidades separadas por comas
            max_skills: Máximo de skills a extraer

        Returns:
            String con las habilidades principales
        """
        if not skills_string:
            return 'mis habilidades'

        # Limpiar y separar skills
        skills = [s.strip() for s in skills_string.split(',')]
        skills = [s for s in skills if s][:max_skills]

        if not skills:
            return 'mis habilidades'

        if len(skills) == 1:
            return skills[0]
        else:
            return f"{skills[0]} y {skills[1]}"

    def get_template_suggestions(self, contact: Dict) -> List[Dict]:
        """
        Sugiere los mejores templates basados en el perfil del contacto

        Args:
            contact: Datos del contacto

        Returns:
            Lista de templates sugeridos con puntuación
        """
        suggestions = []

        for idx, template in enumerate(self.CONNECTION_TEMPLATES):
            score = 0
            reasons = []

            # Evaluar coincidencias
            if contact.get('company') and 'Empresa' in template['name']:
                score += 3
                reasons.append('Tienes empresa específica')

            if contact.get('industry'):
                score += 2
                reasons.append('Tienes industria definida')

            if contact.get('skills'):
                score += 1
                reasons.append('Tienes skills identificadas')

            if template['tone'] == 'professional' and contact.get('company'):
                score += 2
                reasons.append('Tono profesional apropiado')

            if len(contact.get('name', '').split()) > 1:
                score += 1
                reasons.append('Tienes nombre completo')

            suggestions.append({
                'index': idx,
                'name': template['name'],
                'tone': template['tone'],
                'length': template['length'],
                'score': score,
                'reasons': reasons
            })

        # Ordenar por score
        suggestions.sort(key=lambda x: x['score'], reverse=True)

        return suggestions

    def preview_message(self, contact: Dict, template_type: str = 'connection',
                       template_index: Optional[int] = None,
                       custom_vars: Optional[Dict] = None) -> str:
        """
        Previsualiza un mensaje sin guardarlo

        Args:
            contact: Datos del contacto
            template_type: Tipo de template (connection, follow_up, thank_you)
            template_index: Índice del template
            custom_vars: Variables personalizadas

        Returns:
            Mensaje previsualizado
        """
        if template_type == 'connection':
            return self.generate_connection_message(contact, template_index, custom_vars)
        elif template_type == 'follow_up':
            return self.generate_follow_up_message(contact, template_index, custom_vars)
        elif template_type == 'thank_you':
            return self.generate_thank_you_message(contact, 'connection', custom_vars)
        else:
            return "Tipo de template no válido"

    def get_all_templates(self) -> Dict[str, List[Dict]]:
        """
        Retorna todos los templates disponibles

        Returns:
            Diccionario con todos los templates organizados por tipo
        """
        return {
            'connection': self.CONNECTION_TEMPLATES,
            'follow_up': self.FOLLOW_UP_TEMPLATES,
            'thank_you': self.THANK_YOU_TEMPLATES
        }

    def create_custom_template(self, template_type: str, name: str,
                              content: str, tone: str = 'professional') -> bool:
        """
        Agrega un template personalizado

        Args:
            template_type: Tipo de template (connection, follow_up, thank_you)
            name: Nombre del template
            content: Contenido del template con variables {var}
            tone: Tono del template (professional, friendly, casual)

        Returns:
            True si se agregó correctamente
        """
        new_template = {
            'name': name,
            'template': content,
            'tone': tone,
            'is_custom': True
        }

        if template_type == 'connection':
            self.CONNECTION_TEMPLATES.append(new_template)
        elif template_type == 'follow_up':
            new_template['days_after'] = 7
            self.FOLLOW_UP_TEMPLATES.append(new_template)
        elif template_type == 'thank_you':
            self.THANK_YOU_TEMPLATES.append(new_template)
        else:
            return False

        return True
