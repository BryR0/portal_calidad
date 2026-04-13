from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer as Serializer
from app import db
from datetime import datetime

roles_permissions = db.Table('roles_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
)

users_roles = db.Table('users_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)

class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f'<Permission {self.name}>'

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(255))
    
    permissions = db.relationship('Permission', secondary=roles_permissions,
                                  backref=db.backref('roles', lazy='dynamic'))

    def __repr__(self):
        return f'<Role {self.name}>'

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='user') # deprecated: migrated to 'roles'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # department_id if users belong to a specific branch/department
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)

    roles = db.relationship('Role', secondary=users_roles,
                            backref=db.backref('users', lazy='dynamic'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_role(self, role_name):
        return any(r.name == role_name for r in self.roles) or self.role == role_name

    def has_permission(self, perm_name):
        # Admin has all permissions
        if self.is_admin():
            return True
        for role in self.roles:
            if any(p.name == perm_name for p in role.permissions):
                return True
        return False

    def is_admin(self):
        return self.role == 'admin' or self.has_role('admin')
        
    def is_calidad(self):
        return self.is_admin() or self.role == 'calidad' or self.has_role('calidad')

    def generate_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'reset_id': self.id})

    @staticmethod
    def verify_reset_token(token, max_age=3600):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=max_age)
        except:
            return None
        return User.query.get(data.get('reset_id'))

    def __repr__(self):
        return f'<User {self.username}>'
