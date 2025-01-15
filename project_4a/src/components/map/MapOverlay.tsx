import { ReactNode } from 'react';
import { EmailSignup } from '../signup/EmailSignup';

interface Props {
  children: ReactNode;
}

export function MapOverlay({ children }: Props) {
  return (
    <div className="relative z-10 pointer-events-none">
      <div className="pointer-events-auto min-h-screen flex flex-col">
        {/* Spacer to push content to bottom */}
        <div className="flex-1" />
        
        {/* Content starts at bottom of viewport */}
        <div className="bg-white/95 backdrop-blur-sm">
          {children}
          <EmailSignup />
        </div>
      </div>
    </div>
  );
}