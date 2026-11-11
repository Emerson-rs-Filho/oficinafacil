-- OficinaFácil - Projeto físico do banco de dados (MySQL 8)
-- A aplicação também cria estas tabelas automaticamente via SQLAlchemy.

CREATE DATABASE IF NOT EXISTS oficinafacil CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE oficinafacil;

CREATE TABLE usuarios (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  nome        VARCHAR(100) NOT NULL,
  email       VARCHAR(120) NOT NULL UNIQUE,
  senha_hash  VARCHAR(255) NOT NULL
);

CREATE TABLE clientes (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  nome       VARCHAR(100) NOT NULL,
  telefone   VARCHAR(20)  NOT NULL,
  email      VARCHAR(120),
  cpf        VARCHAR(14) UNIQUE,
  criado_em  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE veiculos (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  placa       VARCHAR(8)  NOT NULL UNIQUE,
  marca       VARCHAR(50) NOT NULL,
  modelo      VARCHAR(50) NOT NULL,
  ano         INT,
  cliente_id  INT NOT NULL,
  CONSTRAINT fk_veiculo_cliente FOREIGN KEY (cliente_id)
    REFERENCES clientes(id) ON DELETE CASCADE
);

CREATE TABLE ordens_servico (
  id             INT AUTO_INCREMENT PRIMARY KEY,
  veiculo_id     INT NOT NULL,
  descricao      TEXT NOT NULL,
  data_agendada  DATETIME NOT NULL,
  status         VARCHAR(20) NOT NULL DEFAULT 'Agendada',
  valor          DECIMAL(10,2) DEFAULT 0,
  criado_em      DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_os_veiculo FOREIGN KEY (veiculo_id)
    REFERENCES veiculos(id) ON DELETE CASCADE,
  CONSTRAINT ck_os_status CHECK (status IN ('Agendada','Em andamento','Concluída','Cancelada'))
);

CREATE INDEX idx_os_data ON ordens_servico (data_agendada);
CREATE INDEX idx_os_status ON ordens_servico (status);
