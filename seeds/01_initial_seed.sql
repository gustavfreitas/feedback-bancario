-- Dados iniciais (seed) para as tabelas de domínio
INSERT INTO channels (name) VALUES
    ('Aplicativo'), ('Chat'), ('Telefone'),
    ('Agência'), ('E-mail'), ('WhatsApp');

INSERT INTO manifestation_types (name) VALUES
    ('Reclamação'), ('Elogio'), ('Sugestão'),
    ('Dúvida'), ('Problema Técnico'), ('Solicitação');

INSERT INTO products_services (name) VALUES
    ('Pix'), ('Cartão de Crédito'), ('Conta Corrente'),
    ('Aplicativo Mobile'), ('Empréstimos'), ('Atendimento'),
    ('Transferências'), ('Pagamentos');