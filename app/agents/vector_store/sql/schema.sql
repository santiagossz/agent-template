CREATE SCHEMA rag;


GRANT USAGE ON SCHEMA rag TO anon, authenticated, service_role;
GRANT ALL ON ALL TABLES IN SCHEMA rag TO anon, authenticated, service_role;
GRANT ALL ON ALL ROUTINES IN SCHEMA rag TO anon, authenticated, service_role;
GRANT ALL ON ALL SEQUENCES IN SCHEMA rag TO anon, authenticated, service_role;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA rag GRANT ALL ON TABLES TO anon, authenticated, service_role;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA rag GRANT ALL ON ROUTINES TO anon, authenticated, service_role;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA rag GRANT ALL ON SEQUENCES TO anon, authenticated, service_role;


CREATE OR REPLACE FUNCTION rag.pgfunction(query text)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
  EXECUTE query;
END;
$$;