$content = @'
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

python manage.py shell << 'EOF'
from accounts.models import User
if not User.objects.filter(email='admin@placement.com').exists():
    u = User.objects.create_superuser(
        email='admin@placement.com',
        password='Admin@123',
        full_name='Admin',
        role='admin'
    )
    print(f'Superuser created: {u.email}')
else:
    u = User.objects.get(email='admin@placement.com')
    u.set_password('Admin@123')
    u.full_name = 'Admin'
    u.role = 'admin'
    u.is_staff = True
    u.is_superuser = True
    u.save()
    print(f'Password reset for: {u.email}')
EOF
'@

$content | Out-File -FilePath "build.sh" -Encoding utf8