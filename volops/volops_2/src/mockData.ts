import { useStore } from './store/useStore';

const mockOpportunities = [
  {
    id: '1',
    title: 'Meal Delivery Driver',
    description: 'Help deliver nutritious meals to New Yorkers living with severe illness through God\'s Love We Deliver.',
    organization: 'God\'s Love We Deliver',
    date: '2025-03-15T09:00:00',
    duration: 3,
    location: {
      lat: 40.7453,
      lng: -74.0018,
      address: '166 Avenue of the Americas, New York, NY 10013'
    },
    category: 'Community',
    participants: ['user1', 'user2'],
    maxParticipants: 20,
    skills: ['Driving', 'Customer Service'],
    image: 'https://images.unsplash.com/photo-1594708767771-a7502209ff51?auto=format&fit=crop&q=80' 
  },
  {
    id: '2',
    title: 'Kitchen Meal Prep',
    description: 'Join the kitchen team at God\'s Love We Deliver to help prepare nutritious meals for our clients.',
    organization: 'God\'s Love We Deliver',
    date: '2025-03-20T08:00:00',
    duration: 4,
    location: {
      lat: 40.7453,
      lng: -74.0018,
      address: '166 Avenue of the Americas, New York, NY 10013'
    },
    category: 'Food Service',
    participants: ['user3'],
    maxParticipants: 15,
    skills: ['Food Prep', 'Kitchen Safety'],
    image: 'https://images.unsplash.com/photo-1581299894007-aaa50297cf16?auto=format&fit=crop&q=80'
  },
  {
    id: '3',
    title: 'Central Park Conservation',
    description: 'Help maintain the beauty of Central Park through gardening and clean-up activities.',
    organization: 'Central Park Conservancy',
    date: '2025-03-22T09:00:00',
    duration: 4,
    location: {
      lat: 40.7829,
      lng: -73.9654,
      address: 'Central Park, New York, NY 10022'
    },
    category: 'Environment',
    participants: ['user4', 'user5'],
    maxParticipants: 25,
    skills: ['Gardening', 'Physical Labor'],
    image: 'https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?auto=format&fit=crop&q=80'
  },
  {
    id: '4',
    title: 'Food Pantry Assistant',
    description: 'Support the Food Bank For New York City by helping organize and distribute food to those in need.',
    organization: 'Food Bank For New York City',
    date: '2025-03-25T10:00:00',
    duration: 4,
    location: {
      lat: 40.7133,
      lng: -73.9859,
      address: '39 Broadway, New York, NY 10006'
    },
    category: 'Community',
    participants: ['user6'],
    maxParticipants: 15,
    skills: ['Organization', 'Customer Service'],
    image: 'https://images.unsplash.com/photo-1593113598332-cd59c5bc3f90?auto=format&fit=crop&q=80'
  }
];

// Initialize store with mock data
useStore.getState().setOpportunities(mockOpportunities);