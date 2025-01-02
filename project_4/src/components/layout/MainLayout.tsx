import { ReactNode } from 'react';
import { Header } from './Header';

interface Props {
  children: ReactNode;
}

export function MainLayout({ children }: Props) {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      {children}
    </div>
  );
}