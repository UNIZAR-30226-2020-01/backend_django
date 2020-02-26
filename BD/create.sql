-- *************** SqlDBM: PostgreSQL ****************;
-- ***************************************************;


-- ************************************** "Usuario"

CREATE TABLE "Usuario"
(
 "id"         integer NOT NULL,
 "correo"     varchar(50) NOT NULL,
 "nombre"     varchar(50) NOT NULL,
 "contraseña" varchar(100) NOT NULL,
 CONSTRAINT "PK_Usuario" PRIMARY KEY ( "id" )
);








-- ************************************** "tipo_audio"

CREATE TABLE "tipo_audio"
(
 "id"   integer NOT NULL,
 "tipo" varchar(10) NOT NULL,
 CONSTRAINT "PK_tipo_audio" PRIMARY KEY ( "id" )
);








-- ************************************** "tipo_album"

CREATE TABLE "tipo_album"
(
 "id"   integer NOT NULL,
 "tipo" varchar(10) NOT NULL,
 CONSTRAINT "PK_tipo_album" PRIMARY KEY ( "id" )
);








-- ************************************** "Lista"

CREATE TABLE "Lista"
(
 "id"      integer NOT NULL,
 "titulo"  varchar(100) NOT NULL,
 "usuario" integer NOT NULL,
 CONSTRAINT "PK_Lista" PRIMARY KEY ( "id" ),
 CONSTRAINT "FK_74" FOREIGN KEY ( "usuario" ) REFERENCES "Usuario" ( "id" )
);

CREATE INDEX "fkIdx_74" ON "Lista"
(
 "usuario"
);








-- ************************************** "Carpeta"

CREATE TABLE "Carpeta"
(
 "id"      integer NOT NULL,
 "titulo"  varchar(100) NOT NULL,
 "usuario" integer NOT NULL,
 CONSTRAINT "PK_Carpeta" PRIMARY KEY ( "id" ),
 CONSTRAINT "FK_99" FOREIGN KEY ( "usuario" ) REFERENCES "Usuario" ( "id" )
);

CREATE INDEX "fkIdx_99" ON "Carpeta"
(
 "usuario"
);








-- ************************************** "Amigos"

CREATE TABLE "Amigos"
(
 "uno"  integer NOT NULL,
 "otro" integer NOT NULL,
 CONSTRAINT "PK_Amigos" PRIMARY KEY ( "uno", "otro" ),
 CONSTRAINT "FK_64" FOREIGN KEY ( "uno" ) REFERENCES "Usuario" ( "id" ),
 CONSTRAINT "FK_67" FOREIGN KEY ( "otro" ) REFERENCES "Usuario" ( "id" )
);

CREATE INDEX "fkIdx_64" ON "Amigos"
(
 "uno"
);

CREATE INDEX "fkIdx_67" ON "Amigos"
(
 "otro"
);








-- ************************************** "Album"

CREATE TABLE "Album"
(
 "id"     integer NOT NULL,
 "titulo" varchar(100) NOT NULL,
 "Fecha"  date NOT NULL,
 "icono"  path NOT NULL,
 "tipo"   integer NOT NULL,
 CONSTRAINT "PK_Album" PRIMARY KEY ( "id" ),
 CONSTRAINT "FK_28" FOREIGN KEY ( "tipo" ) REFERENCES "tipo_album" ( "id" )
);

CREATE INDEX "fkIdx_28" ON "Album"
(
 "tipo"
);








-- ************************************** "ListaEnCarpeta"

CREATE TABLE "ListaEnCarpeta"
(
 "carpeta" integer NOT NULL,
 "lista"   integer NOT NULL,
 CONSTRAINT "PK_ListaEnCarpeta" PRIMARY KEY ( "carpeta", "lista" ),
 CONSTRAINT "FK_90" FOREIGN KEY ( "carpeta" ) REFERENCES "Carpeta" ( "id" ),
 CONSTRAINT "FK_96" FOREIGN KEY ( "lista" ) REFERENCES "Lista" ( "id" )
);

CREATE INDEX "fkIdx_90" ON "ListaEnCarpeta"
(
 "carpeta"
);

CREATE INDEX "fkIdx_96" ON "ListaEnCarpeta"
(
 "lista"
);








-- ************************************** "Audio"

CREATE TABLE "Audio"
(
 "id"      integer NOT NULL,
 "titulo"  varchar(100) NOT NULL,
 "archivo" path NOT NULL,
 "pista"   int NOT NULL,
 "album"   integer NOT NULL,
 "tipo"    integer NOT NULL,
 CONSTRAINT "PK_Audio" PRIMARY KEY ( "id" ),
 CONSTRAINT "FK_16" FOREIGN KEY ( "album" ) REFERENCES "Album" ( "id" ),
 CONSTRAINT "FK_23" FOREIGN KEY ( "tipo" ) REFERENCES "tipo_audio" ( "id" )
);

CREATE INDEX "fkIdx_16" ON "Audio"
(
 "album"
);

CREATE INDEX "fkIdx_23" ON "Audio"
(
 "tipo"
);








-- ************************************** "Favoritos"

CREATE TABLE "Favoritos"
(
 "audio"   integer NOT NULL,
 "usuario" integer NOT NULL,
 CONSTRAINT "PK_table_36" PRIMARY KEY ( "audio", "usuario" ),
 CONSTRAINT "FK_46" FOREIGN KEY ( "audio" ) REFERENCES "Audio" ( "id" ),
 CONSTRAINT "FK_59" FOREIGN KEY ( "usuario" ) REFERENCES "Usuario" ( "id" )
);

CREATE INDEX "fkIdx_46" ON "Favoritos"
(
 "audio"
);

CREATE INDEX "fkIdx_59" ON "Favoritos"
(
 "usuario"
);








-- ************************************** "CancionEnLista"

CREATE TABLE "CancionEnLista"
(
 "cancion" integer NOT NULL,
 "lista"   integer NOT NULL,
 CONSTRAINT "PK_CancionEnLista" PRIMARY KEY ( "cancion", "lista" ),
 CONSTRAINT "FK_78" FOREIGN KEY ( "cancion" ) REFERENCES "Audio" ( "id" ),
 CONSTRAINT "FK_82" FOREIGN KEY ( "lista" ) REFERENCES "Lista" ( "id" )
);

CREATE INDEX "fkIdx_78" ON "CancionEnLista"
(
 "cancion"
);

CREATE INDEX "fkIdx_82" ON "CancionEnLista"
(
 "lista"
);







