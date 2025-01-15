import React, { useEffect } from 'react';
import { MainLayout } from './components/layout/MainLayout';
import { MapContainer } from './components/map/MapContainer';
import { OpportunityCard } from './components/OpportunityCard';
import { EmailSignup } from './components/signup/EmailSignup';
import { useStore } from './store/useStore';
import { supabase } from './main';

function App() {
  const { opportunities, setOpportunities } = useStore();

  useEffect(() => {
    async function fetchOpportunities() {
      const { data, error } = await supabase
        .from('opportunities')
        .select(`
          *,
          opportunity_participants (
            user_id
          )
        `);

      if (error) {
        console.error('Error fetching opportunities:', error);
        return;
      }

      // Transform the data to match our store structure
      const formattedOpportunities = data.map(opp => ({
        id: opp.id,
        title: opp.title,
        description: opp.description,
        organization: opp.organization,
        date: opp.date,
        duration: opp.duration,
        location: {
          lat: opp.location_lat,
          lng: opp.location_lng,
          address: opp.location_address
        },
        category: opp.category,
        participants: opp.opportunity_participants.map(p => p.user_id),
        maxParticipants: opp.max_participants,
        skills: opp.skills,
        image: opp.image
      }));

      setOpportunities(formattedOpportunities);
    }

    fetchOpportunities();
  }, [setOpportunities]);

  return (
    <MainLayout>
      <div className="pt-16">
        <div className="h-[60vh]">
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