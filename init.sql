-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create roles if they don't exist
DO $$ BEGIN
  CREATE ROLE anon NOLOGIN;
EXCEPTION WHEN duplicate_object THEN
  NULL;
END $$;

-- Create items table
CREATE TABLE IF NOT EXISTS public.items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Enable Row Level Security
ALTER TABLE public.items ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Enable read access for all users" ON public.items;
DROP POLICY IF EXISTS "Enable insert for all users" ON public.items;
DROP POLICY IF EXISTS "Enable update for all users" ON public.items;
DROP POLICY IF EXISTS "Enable delete for all users" ON public.items;

-- Create policies
CREATE POLICY "Enable read access for all users" ON public.items
    FOR SELECT USING (true);

CREATE POLICY "Enable insert for all users" ON public.items
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Enable update for all users" ON public.items
    FOR UPDATE USING (true);

CREATE POLICY "Enable delete for all users" ON public.items
    FOR DELETE USING (true);

-- Grant permissions to anon role
GRANT USAGE ON SCHEMA public TO anon;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.items TO anon;

-- Create index on created_at for faster queries
CREATE INDEX IF NOT EXISTS idx_items_created_at ON public.items(created_at DESC);
