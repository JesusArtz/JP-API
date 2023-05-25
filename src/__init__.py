from src.User.auth import login, register
from src.User.userActions import get_user, get_asesorias, send_calificacion, create_asesoria, get_asesorias

ROOT = [
    {
        'path': '/login',
        'methods': ['POST'],
        'function': login
    },
    {
        'path': '/register',
        'methods': ['POST'],
        'function': register
    },
    {
        'path': '/get_user',
        'methods': ['POST'],
        'function': get_user
    },
    {
        'path': '/get_asesorias',
        'methods': ['POST'],
        'function': get_asesorias
    },
    {
        'path': '/send_calificacion',
        'methods': ['POST'],
        'function': send_calificacion
    },
    {
        'path': '/create_asesoria',
        'methods': ['POST'],
        'function': create_asesoria
    },
    {
        'path': '/get_asesorias',
        'methods': ['POST'],
        'function': get_asesorias
    }
]