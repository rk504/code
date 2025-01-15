import { create } from 'zustand';

interface Opportunity {
  id: string;
  title: string;
  description: string;
  organization: string;
  date: string;
  duration: number;
  location: {
    lat: number;
    lng: number;
    address: string;
  };
  category: string;
  participants: string[];
  maxParticipants: number;
  skills: string[];
  image: string;
}

interface StoreState {
  opportunities: Opportunity[];
  setOpportunities: (opportunities: Opportunity[]) => void;
  addParticipant: (opportunityId: string, userId: string) => void;
  removeParticipant: (opportunityId: string, userId: string) => void;
}

export const useStore = create<StoreState>((set) => ({
  opportunities: [],
  
  setOpportunities: (opportunities) => set({ opportunities }),
  
  addParticipant: (opportunityId, userId) => 
    set((state) => ({
      opportunities: state.opportunities.map(opportunity => 
        opportunity.id === opportunityId
          ? {
              ...opportunity,
              participants: [...opportunity.participants, userId]
            }
          : opportunity
      )
    })),
    
  removeParticipant: (opportunityId, userId) =>
    set((state) => ({
      opportunities: state.opportunities.map(opportunity =>
        opportunity.id === opportunityId
          ? {
              ...opportunity,
              participants: opportunity.participants.filter(id => id !== userId)
            }
          : opportunity
      )
    }))
}));