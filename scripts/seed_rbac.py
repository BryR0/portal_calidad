from app import create_app, db
from app.models.user import User, Role, Permission

def seed_rbac():
    app = create_app()
    with app.app_context():
        print("Seeding Roles and Permissions...")
        
        # 1. Create Permissions
        perms_data = [
            ('user_manage', 'Gestionar usuarios (crear, editar, desactivar)'),
            ('role_manage', 'Gestionar roles y permisos'),
            ('nc_view', 'Ver no conformidades'),
            ('nc_create', 'Crear no conformidades'),
            ('nc_edit', 'Editar no conformidades propias/abiertas'),
            ('nc_edit_all', 'Editar cualquier no conformidad'),
            ('nc_close', 'Cerrar no conformidades'),
            ('catalog_manage', 'Gestionar catálogos (Empresas, Marcas, Secciones, etc.)'),
            ('export_data', 'Exportar datos a Excel/PDF')
        ]
        
        permissions = {}
        for name, desc in perms_data:
            p = Permission.query.filter_by(name=name).first()
            if not p:
                p = Permission(name=name, description=desc)
                db.session.add(p)
            permissions[name] = p
        
        db.session.flush() # To get IDs
        
        # 2. Create Roles
        roles_data = {
            'admin': {
                'desc': 'Administrador del Sistema',
                'perms': perms_data # All perms
            },
            'calidad': {
                'desc': 'Gestor de Calidad',
                'perms': [
                    'nc_view', 'nc_create', 'nc_edit', 'nc_edit_all', 
                    'nc_close', 'catalog_manage', 'export_data'
                ]
            },
            'user': {
                'desc': 'Usuario Operativo',
                'perms': ['nc_view', 'nc_create', 'nc_edit', 'export_data']
            },
            'viewer': {
                'desc': 'Visualizador (Solo Lectura)',
                'perms': ['nc_view', 'export_data']
            }
        }
        
        roles = {}
        for rname, rinfo in roles_data.items():
            role = Role.query.filter_by(name=rname).first()
            if not role:
                role = Role(name=rname, description=rinfo['desc'])
                db.session.add(role)
            
            # Update permissions
            role.permissions = []
            for pname in rinfo['perms']:
                # If perms is a list of tuples (admin case) or list of strings
                p_lookup = pname[0] if isinstance(pname, tuple) else pname
                role.permissions.append(permissions[p_lookup])
            
            roles[rname] = role

        db.session.commit()
        print("Roles and Permissions created.")

        # 3. Migrate existing users
        print("Migrating users to new roles...")
        users = User.query.all()
        for u in users:
            if u.role in roles:
                target_role = roles[u.role]
                if target_role not in u.roles:
                    u.roles.append(target_role)
            elif not u.roles:
                # Default to 'user' if role string is unknown
                u.roles.append(roles['user'])
        
        db.session.commit()
        print("Users migrated successfully.")

if __name__ == '__main__':
    seed_rbac()
