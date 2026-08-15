-- Gatilho de mudança de atualização da Tabela Update.
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_manifestations_updated_at
BEFORE UPDATE ON manifestations
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();