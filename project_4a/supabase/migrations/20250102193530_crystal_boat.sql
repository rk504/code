/*
  # Create email submissions table

  1. New Tables
    - `email_submissions`
      - `id` (uuid, primary key)
      - `email` (text, unique)
      - `created_at` (timestamp)
      - `status` (text) - For tracking email status
  2. Security
    - Enable RLS on `email_submissions` table
    - Add policy for inserting new submissions
*/

CREATE TABLE IF NOT EXISTS email_submissions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email text UNIQUE NOT NULL,
  created_at timestamptz DEFAULT now(),
  status text DEFAULT 'pending'
);

ALTER TABLE email_submissions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can insert email submissions"
  ON email_submissions
  FOR INSERT
  TO anon
  WITH CHECK (true);

CREATE POLICY "Authenticated users can view submissions"
  ON email_submissions
  FOR SELECT
  TO authenticated
  USING (true);

-- Create opportunities table
CREATE TABLE opportunities (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  organization TEXT NOT NULL,
  date TIMESTAMP WITH TIME ZONE NOT NULL,
  duration INTEGER NOT NULL,
  location_lat DOUBLE PRECISION NOT NULL,
  location_lng DOUBLE PRECISION NOT NULL,
  location_address TEXT NOT NULL,
  category TEXT NOT NULL,
  max_participants INTEGER NOT NULL,
  skills TEXT[] NOT NULL,
  image TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create participants junction table
CREATE TABLE opportunity_participants (
  opportunity_id UUID REFERENCES opportunities(id) ON DELETE CASCADE,
  user_id UUID NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  PRIMARY KEY (opportunity_id, user_id)
);

-- Add some sample data
INSERT INTO opportunities (
  title,
  description,
  organization,
  date,
  duration,
  location_lat,
  location_lng,
  location_address,
  category,
  max_participants,
  skills,
  image
) VALUES 
(
  'Chinatown Food Bank',
  'Help distribute food to elderly residents in Chinatown.',
  'SF Community Food Bank',
  '2024-03-15T09:00:00Z',
  4,
  37.7941,
  -122.4078,
  '731 Grant Ave, San Francisco, CA 94108',
  'Community',
  10,
  ARRAY['Customer Service', 'Mandarin/Cantonese'],
  'https://images.unsplash.com/photo-1579975096649-e773152b04cb?auto=format&fit=crop&q=80'
),
(
  'Haight Street Clean-up',
  'Join us in keeping the Haight-Ashbury neighborhood beautiful.',
  'Haight Community Association',
  '2024-03-20T10:00:00Z',
  3,
  37.7695,
  -122.4483,
  '1500 Haight St, San Francisco, CA 94117',
  'Environment',
  15,
  ARRAY['Physical Labor', 'Environmental'],
  'https://images.unsplash.com/photo-1617150119111-09bbb85178b0?auto=format&fit=crop&q=80'
);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER opportunities_updated_at
  BEFORE UPDATE ON opportunities
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();