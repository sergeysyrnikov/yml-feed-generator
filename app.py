import sys
from typing import Any

from django.conf import settings
from django.core.management import execute_from_command_line

# 1. Минимальная конфигурация Django (без БД и лишних приложений)
if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY="dev-secret-key",
        ROOT_URLCONF=__name__,
        ALLOWED_HOSTS=["*"],
        MIDDLEWARE=[],
    )

from django.http import HttpRequest, HttpResponse
from django.urls import path
from django.utils import timezone
from django.views import View

from feed_task import CATEGORIES, PRODUCTS, build_yml


class YMLFeedView(View):
    """
    Пример подключения функции генерации YML-фида к Django View.
    """

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        # В реальном приложении здесь был бы запрос к базе данных
        xml_content = build_yml(
            products=PRODUCTS,
            categories=CATEGORIES,
            generated_at=timezone.now(),
        )

        return HttpResponse(
            xml_content,
            content_type="application/xml; charset=utf-8",
        )


# 2. Маршрутизация
urlpatterns = [
    path("yandex-market.yml", YMLFeedView.as_view()),
]

# 3. Точка входа для запуска сервера
if __name__ == "__main__":
    # Если скрипт запущен без аргументов, по умолчанию запускаем сервер на 8000 порту
    if len(sys.argv) == 1:
        sys.argv.extend(["runserver", "127.0.0.1:8000"])
    execute_from_command_line(sys.argv)
