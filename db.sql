CREATE DATABASE Asesorias;
USE Asesorias;
CREATE TABLE Usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    numeroControl TEXT NOT NULL,
    password TEXT NOT NULL,
    is_teacher INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE Materias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    id_usuario INTEGER NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id)
);

CREATE TABLE Asesorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_materia INTEGER NOT NULL,
    id_usuario INTEGER NOT NULL,
    FOREIGN KEY (id_materia) REFERENCES Materias(id),
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id)
);

CREATE TABLE Evaluaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_asesoria INTEGER NOT NULL,
    id_usuario INTEGER NOT NULL,
    preguntaUno INTEGER NOT NULL,
    preguntaDos INTEGER NOT NULL,
    preguntaTres INTEGER NOT NULL,
    preguntaCuatro INTEGER NOT NULL,
    preguntaCinco INTEGER NOT NULL,
    preguntaSeis INTEGER NOT NULL,
    FOREIGN KEY (id_asesoria) REFERENCES Asesorias(id),
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id)
);

CREATE TABLE historial (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    id_asesoria INTEGER NOT NULL,
    calificacion INTEGER NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id),
    FOREIGN KEY (id_asesoria) REFERENCES Asesorias(id)
);