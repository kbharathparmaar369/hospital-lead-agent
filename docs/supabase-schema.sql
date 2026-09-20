-- Supabase schema for Hospital Lead Agent
CREATE TABLE IF NOT EXISTS public.leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    patient_name TEXT NOT NULL,
    patient_phone TEXT,
    patient_email TEXT,
    reason TEXT,
    department TEXT,
    preferred_time TEXT,
    booking_status TEXT DEFAULT 'pending',
    calcom_booking_id TEXT,
    notes TEXT
);

-- Enable Row Level Security (RLS)
ALTER TABLE public.leads ENABLE ROW LEVEL SECURITY;

-- Allow service_role to perform all operations
CREATE POLICY "Allow service role full access" ON public.leads
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- Optional: Allow read access for authenticated staff
CREATE POLICY "Allow authenticated read" ON public.leads
    FOR SELECT
    TO authenticated
    USING (true);
