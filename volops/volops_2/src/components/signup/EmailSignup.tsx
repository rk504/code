import { useState } from 'react';
import { Mail } from 'lucide-react';
import { useEmailSubmission } from './useEmailSubmission';

export function EmailSignup() {
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const { submitEmail, isSubmitting, error } = useEmailSubmission();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const success = await submitEmail(email);
    if (success) {
      setSubmitted(true);
      setEmail('');
    }
  };

  return (
    <div className="bg-rose-600 text-white py-12">
      <div className="max-w-7xl mx-auto px-4">
        <div className="max-w-xl mx-auto text-center">
          <Mail className="w-12 h-12 mx-auto mb-4" />
          <h2 className="text-3xl font-bold mb-4">
            Stay Updated on Volunteer Opportunities
          </h2>
          <p className="mb-6">
            Join our community and receive notifications about new opportunities in your area.
          </p>
          
          {submitted ? (
            <div className="bg-white/10 rounded-lg p-4">
              <p className="text-lg">Thank you for signing up! We'll be in touch soon.</p>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="flex gap-2">
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email"
                required
                className="flex-1 px-4 py-2 rounded-lg text-gray-900"
                disabled={isSubmitting}
              />
              <button
                type="submit"
                disabled={isSubmitting}
                className="px-6 py-2 bg-white text-rose-600 font-semibold rounded-lg hover:bg-rose-50 transition-colors disabled:opacity-50"
              >
                {isSubmitting ? 'Signing Up...' : 'Sign Up'}
              </button>
            </form>
          )}
          {error && <p className="mt-2 text-sm text-rose-200">{error}</p>}
        </div>
      </div>
    </div>
  );
}