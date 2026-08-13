CREATE TABLE products_services (
    id_products SERIAL PRIMARY KEY,
    pix VARCHAR(50),
    cartao_credito VARCHAR(50),
    conta_corrente VARCHAR(50),
    aplicativo_mobile VARCHAR(50),
    emprestimos VARCHAR(50),
    atendimento VARCHAR(50),
    transferencias VARCHAR(50),
    pagamentos VARCHAR(50)
);

CREATE TABLE channels (
    id_channels SERIAL PRIMARY KEY,
    aplicativo VARCHAR(50),
    chat VARCHAR(50),
    telefone VARCHAR(50),
    agencia VARCHAR(50),
    email VARCHAR(50),
    whatsapp VARCHAR(50)
);

CREATE TABLE manifestation_types (
    id_types SERIAL PRIMARY KEY,
    reclamacao VARCHAR(50),
    elogio VARCHAR(50),
    sugestao VARCHAR(50),
    duvida VARCHAR(50),
    problema_tecnico VARCHAR(50),
    solicitacao VARCHAR(50)
);

CREATE TABLE manifestations (
    id SERIAL PRIMARY KEY,
    product_service_id INT REFERENCES products_services(id) ON DELETE CASCADE,
    channel_id INT REFERENCES channels(id) ON DELETE CASCADE,
    manifestation_type_id INT REFERENCES manifestation_types(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3ª Tabela Filha: Pedidos (Conecta Clientes e Produtos)
CREATE TABLE pedidos (
    id_pedido INT PRIMARY KEY,
    id_cliente INT,
    id_produto INT,
    CONSTRAINT fk_cliente FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    CONSTRAINT fk_produto FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
);