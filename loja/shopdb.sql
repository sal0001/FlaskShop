DROP DATABASE IF EXISTS shopdb;
CREATE DATABASE IF NOT EXISTS shopdb; 
USE shopdb;

DROP TABLE IF EXISTS categorias;
CREATE TABLE IF NOT EXISTS categorias (
  id int NOT NULL AUTO_INCREMENT,
  descricao varchar(250) DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO categorias (descricao) VALUES
	('Telemóveis'),
	('Computadores');
	
DROP TABLE IF EXISTS clientes;
CREATE TABLE IF NOT EXISTS clientes (
  id int NOT NULL AUTO_INCREMENT,
  nome varchar(100) DEFAULT NULL,
  morada varchar(100) DEFAULT NULL,
  utilizadorId int DEFAULT NULL,
  PRIMARY KEY (id),
  KEY utilizador_idx (utilizadorId)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS encomendas;
CREATE TABLE IF NOT EXISTS encomendas (
  id int NOT NULL AUTO_INCREMENT,
  clienteId int DEFAULT NULL,
  dataEncomenda date DEFAULT NULL,
  total float DEFAULT NULL,
  PRIMARY KEY (id),
  KEY cliente_idx (clienteId)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS linhas_encomenda;
CREATE TABLE IF NOT EXISTS linhas_encomenda (
  id int NOT NULL AUTO_INCREMENT,
  encomendaId int DEFAULT NULL,
  produtoId int DEFAULT NULL,
  quantidade int DEFAULT NULL,
  PRIMARY KEY (id),
  KEY encomenda_idx (encomendaId),
  KEY produto_idx (produtoId)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS produtos;
CREATE TABLE IF NOT EXISTS produtos (
  id int NOT NULL AUTO_INCREMENT,
  descricao varchar(250) DEFAULT NULL,
  preco float DEFAULT NULL,
  image_url varchar(100) DEFAULT NULL,
  categoriaId int DEFAULT NULL,
  PRIMARY KEY (id),
  KEY categoria_idx (categoriaId)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS roles;
CREATE TABLE IF NOT EXISTS roles (
  id int NOT NULL AUTO_INCREMENT,
  descricao varchar(100) DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO roles (descricao) VALUES
	('administrador'),
	('cliente');
	
DROP TABLE IF EXISTS utilizadores;
CREATE TABLE IF NOT EXISTS utilizadores (
  id int NOT NULL AUTO_INCREMENT,
  email varchar(100) DEFAULT NULL,
  password varchar(100) DEFAULT NULL,
  roleId int DEFAULT NULL,
  PRIMARY KEY (id),
  KEY role_idx (roleId)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO utilizadores (email, password, roleId) VALUES
	('admin@gmail.com', '123', 1);