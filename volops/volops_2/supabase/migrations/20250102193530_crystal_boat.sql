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