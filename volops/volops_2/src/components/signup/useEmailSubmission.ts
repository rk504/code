import { useState } from 'react';
import { supabase } from '../../lib/supabase';

export function useEmailSubmission() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  const submitEmail = async (email: string) => {
    setIsSubmitting(true);
    setError('');

    try {
      const { error: submitError } = await supabase
        .from('email_submissions')
        .insert([{ email }]);

      if (submitError) throw submitError;
      return true;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to submit email');
      return false;
    } finally {
      setIsSubmitting(false);
    }
  };

  return { submitEmail, isSubmitting, error };
}