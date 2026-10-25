with open('bookmyseat/settings.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix ALLOWED_HOSTS to allow localhost
content = content.replace(
    "ALLOWED_HOSTS = ['.vercel.app']",
    "ALLOWED_HOSTS = ['*']"
)

# Disable remote PostgreSQL, keep local SQLite only
content = content.replace(
    "DATABASES['default'] = dj_database_url.parse('postgresql://django_bookmyshow_user:uF7eu2GnnDbqvUgYswCYpIS5TKTtsAUS@dpg-cshi84o8fa8c739dsme0-a.oregon-postgres.render.com/django_bookmyshow')",
    "# DATABASES['default'] = dj_database_url.parse('postgresql://...')  # disabled for local dev"
)

with open('bookmyseat/settings.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('settings.py updated successfully!')
