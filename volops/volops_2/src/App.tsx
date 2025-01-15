import React from 'react';
import { MainLayout } from './components/layout/MainLayout';
import { MapContainer } from './components/map/MapContainer';
import { OpportunityCard } from './components/OpportunityCard';
import { EmailSignup } from './components/signup/EmailSignup';
import { useStore } from './store/useStore';

function App() {
  const { opportunities } = useStore();

  return (
    <MainLayout>
      <div className="pt-16"> {/* Add padding for fixed header */}
        <div className="h-[60vh]"> {/* Map takes 60% of viewport height */}
          <MapContainer />
        </div>
        
        <div className="bg-white">
          <main className="max-w-7xl mx-auto px-4 py-8">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {opportunities.map((opportunity) => (
                <OpportunityCard key={opportunity.id} opportunity={opportunity} />
              ))}
            </div>
          </main>
          
          <EmailSignup />
        </div>
      </div>
    </MainLayout>
  );
}

export default App;