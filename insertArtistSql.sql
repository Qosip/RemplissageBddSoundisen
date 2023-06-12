INSERT INTO artiste (nom, prenom, nom_scene, date_naissance, date_mort, photo, type_artiste, style_musical) VALUES ("Le Wanksi", "Le Wanksi", "Le Wanksi", '2000-01-01', NULL, "https://i.scdn.co/image/ab6761610000e5eb88078837e4a9e9c82678479f", "artist", "acidcore");
SET @id_artiste := LAST_INSERT_ID();
INSERT INTO album (titre, date_parution) VALUES ("Écume Pastel", "2023-04-26");
SET @id_album := LAST_INSERT_ID();
INSERT INTO a_publie (id_album, id_artiste) VALUES (@id_album, @id_artiste);
