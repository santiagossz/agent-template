-- Enable the pgvector extension to work with embedding vectors
create extension if not exists vector;

-- Create a table to store your documents
create table {table_name} (
    id uuid primary key,
    content text, -- corresponds to Document.pageContent
    metadata jsonb, -- corresponds to Document.metadata
    embedding vector (1536) -- 1536 works for OpenAI embeddings, change if needed
);

-- Create a function to search for documents
create function match_{table_name} (
  query_embedding vector (1536),
  filter jsonb default '{{}}'
) returns table (
  id uuid,
  content text,
  metadata jsonb,
  similarity float
) language plpgsql as $$
#variable_conflict use_column
begin
  return query
  select
    id,
    content,
    metadata,
    1 - ({table_name}.embedding <=> query_embedding) as similarity
  from {table_name}
  where metadata @> filter
  order by {table_name}.embedding <=> query_embedding;
end;
$$;

alter table {table_name} enable row level security;