import datetime
from icalendar import Calendar, Event

class CalendarGeneratorService():
    def __init__(self) -> None:
        pass


    def is_valid_date(self, date_str: str) -> bool:
        """
        Проверяет, является ли строка корректной датой в формате YYYY-MM-DD.
        """
        try:
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def generate_calendar_file(self, date: str, summary: str = "ABCD"):
        """
        Принимает строку с датой в формате YYYY-MM-DD и название события.
        Возвращает ICS-файл в формате байтов с целодневным событием.
        """
        event_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        
        cal = Calendar()
        cal.add("prodid", "-//My Calendar Application//example.com//")
        cal.add("version", "2.0")
        
        event = Event()
        event.add("summary", summary)
        event.add("dtstart", event_date)
        event.add("dtend", event_date + datetime.timedelta(days=1))
        event.add("uid", f"{datetime.datetime.now().timestamp()}@example.com")
        
        cal.add_component(event)
        
        return cal.to_ical()