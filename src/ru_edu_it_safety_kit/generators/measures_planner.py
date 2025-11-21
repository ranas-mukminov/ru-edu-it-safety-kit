from typing import Dict, List

from ru_edu_it_safety_kit.models.school_profile import SchoolProfile, SchoolType


class MeasuresPlanner:
    @staticmethod
    def plan(profile: SchoolProfile) -> Dict[str, List[str]]:
        """
        Generates a list of recommended safety measures based on the school profile.
        Returns a dictionary with categories: 'technical', 'organizational'.
        """
        technical = []
        organizational = []

        # Basic Technical Measures
        technical.append(
            "Настроить DNS-фильтрацию (SkyDNS, Яндекс.DNS или аналог) на всех пограничных маршрутизаторах."
        )
        technical.append("Включить логирование соединений на Firewall (хранение логов не менее 6 месяцев).")
        technical.append("Разделить сеть на VLAN: Администрация, Учителя, Ученики, Гости.")

        if profile.type == SchoolType.SCHOOL:
            technical.append("Настроить 'белые списки' для младших классов (если выделен отдельный сегмент).")

        if profile.is_multi_building:
            technical.append("Настроить защищенный VPN-туннель (IPsec/WireGuard) между зданиями.")
            technical.append("Обеспечить синхронизацию времени (NTP) на всех узлах сети.")

        # Organizational Measures
        organizational.append("Утвердить 'Положение об использовании сети Интернет' (AUP).")
        organizational.append("Назначить ответственного за контентную фильтрацию (приказ директора).")
        organizational.append("Провести инструктаж учителей по основам цифровой гигиены.")

        if profile.type == SchoolType.COLLEGE:
            organizational.append("Разработать регламент использования личных устройств (BYOD) для студентов.")

        return {"technical": technical, "organizational": organizational}
