import React from 'react';

interface Opportunity {
  id: string;
  title: string;
  description: string;
  organization: string;
  date: string;
  duration: number;
  location: {
    address: string;
    lat: number;
    lng: number;
  };
  category: string;
  participants: string[];
  maxParticipants: number;
  skills: string[];
  image: string;
}

interface OpportunityCardProps {
  opportunity: Opportunity;
}

export const OpportunityCard: React.FC<OpportunityCardProps> = ({ opportunity }) => {
  const formattedDate = new Date(opportunity.date).toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <img 
        src={opportunity.image} 
        alt={opportunity.title}
        className="w-full h-48 object-cover"
      />
      <div className="p-4">
        <h3 className="text-xl font-semibold mb-2">{opportunity.title}</h3>
        <p className="text-gray-600 mb-2">{opportunity.organization}</p>
        <p className="text-sm text-gray-500 mb-4">{opportunity.description}</p>
        
        <div className="mb-4">
          <p className="text-sm">
            <span className="font-semibold">Date:</span> {formattedDate}
          </p>
          <p className="text-sm">
            <span className="font-semibold">Duration:</span> {opportunity.duration} hours
          </p>
          <p className="text-sm">
            <span className="font-semibold">Location:</span> {opportunity.location.address}
          </p>
        </div>

        <div className="flex flex-wrap gap-2 mb-4">
          {opportunity.skills.map((skill) => (
            <span 
              key={skill}
              className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded"
            >
              {skill}
            </span>
          ))}
        </div>

        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">
            {opportunity.participants.length} / {opportunity.maxParticipants} spots filled
          </span>
          <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
            Sign Up
          </button>
        </div>
      </div>
    </div>
  );
};