"""Сервис учебных заявок с явной проверкой входных данных."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, replace
from pathlib import Path


class ValidationError(ValueError):
    """Входные данные заявки не соответствуют предметным правилам."""


@dataclass(frozen=True)
class Ticket:
    """Заявка с постоянным идентификатором и состоянием."""

    identifier: int
    title: str
    assignee: str
    status: str = "Открыта"


class TicketBoard:
    """Локальный реестр заявок на основе JSON-хранилища."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.tickets: list[Ticket] = []
        self.load()

    def load(self) -> None:
        """Прочитать ранее сохранённые заявки, если файл существует."""
        if self.path.exists():
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(raw, list):
                raise ValidationError("Неверный формат реестра")
            self.tickets = [Ticket(**entry) for entry in raw]

    def save(self) -> None:
        """Сохранить данные в соседнем временном файле и заменить исходный."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(
            json.dumps([asdict(item) for item in self.tickets], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        temporary.replace(self.path)

    def add(self, title: str, assignee: str) -> Ticket:
        """Добавить новую заявку с проверкой обязательных полей."""
        if not isinstance(title, str) or not 1 <= len(title.strip()) <= 80:
            raise ValidationError("Название должно содержать от 1 до 80 символов")
        if not isinstance(assignee, str) or not 1 <= len(assignee.strip()) <= 40:
            raise ValidationError("Имя исполнителя должно содержать от 1 до 40 символов")
        new_id = max((item.identifier for item in self.tickets), default=0) + 1
        ticket = Ticket(new_id, title.strip(), assignee.strip())
        self.tickets.append(ticket)
        self.save()
        return ticket

    def find(self, identifier: int) -> Ticket:
        """Вернуть заявку по номеру или сообщить об отсутствии."""
        for ticket in self.tickets:
            if ticket.identifier == identifier:
                return ticket
        raise ValidationError("Заявка не найдена")

    def close(self, identifier: int) -> Ticket:
        """Закрыть заявку и зафиксировать обновлённое состояние."""
        ticket = self.find(identifier)
        updated = replace(ticket, status="Закрыта")
        self.tickets = [updated if item.identifier == identifier else item for item in self.tickets]
        self.save()
        return updated

    def summary(self) -> dict[str, int]:
        """Подсчитать общее число заявок и число завершённых."""
        return {
            "всего": len(self.tickets),
            "закрыто": sum(item.status == "Закрыта" for item in self.tickets),
        }
